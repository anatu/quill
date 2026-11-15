"""Evaluate the explain task: a passage written from notes (pairs/explain.py).

Systems write from the same held-out notes: an adapter (N candidates, the usual gates, rerank), or
Claude told to write like a textbook, with or without real passages from the book as exemplars.
Outputs go where the harness reads them (op `write`, input = the notes), so `quill eval` scores them.
A blind kit pairs two systems' passages on the same notes for a human pick.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from .. import template
from ..gen.claude_cli import Claude, prompt
from ..pairs import explain as X
from . import baselines, pool

EXEMPLAR_NOTE = "\nThese passages are from the textbook whose manner you should match:\n\n{body}\n"


def rows(cfg: dict, part: str = "dev") -> list[dict]:
    return [r for r in map(json.loads, X.file(cfg).read_text().splitlines()) if r["split"] == part and not r["fails"]]


def exemplar_text(cfg: dict, k: int = 3, seed: int = 0) -> str:
    """k train passages of middling length with no gap marker, the same for every item."""
    ok = [c for c in pool.author_chunks(cfg) if c["split"] == "train" and c["bucket"] == "300-500" and c["marked"] == c["text"]]
    pick = random.Random(seed).sample(ok, k)
    return EXEMPLAR_NOTE.format(body="\n\n".join(f"[{i}]\n{c['text']}" for i, c in enumerate(pick, 1)))


def _save(cfg: dict, name: str, part: str, items: list[dict], stats: dict) -> dict:
    d = Path(cfg["paths"]["eval"]) / "outputs" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{part}.jsonl").write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in items))
    (d / f"{part}.stats.json").write_text(json.dumps(stats, indent=1))
    return dict(stats, out=str(d / f"{part}.jsonl"))


def run_adapter(cfg: dict, name: str, adapter: str, part: str = "dev", n: int = 4, ctx=None, limit: int | None = None) -> dict:
    from ..gen.local import Local
    from ..train import adapter_dir

    data = rows(cfg, part)[:limit]
    gen = Local(cfg, adapter=adapter_dir(cfg, adapter))
    jobs = [dict(id=r["id"], op="write", sample=s, input=r["notes"], words=r["words"],
                 system=template.system("explain", "notes", template.bucket(r["words"])))
            for r in data for s in range(n)]
    texts = gen.map([(j["input"], j["system"], j["sample"], int(j["words"] * 2.2) + 150) for j in jobs])
    texts = [baselines.MARKER_LINE.sub("", t).strip() for t in texts]
    items, stats = baselines._pick(cfg, jobs, texts, n, gen, ctx)
    stats.update(adapter=adapter, task="explain")
    return _save(cfg, name, part, items, stats) if limit is None else dict(stats, items=items)


def run_claude(cfg: dict, name: str, part: str = "dev", exemplars: bool = False, ctx=None, claude=None,
               limit: int | None = None) -> dict:
    data = rows(cfg, part)[:limit]
    g = cfg.get("gen", {})
    claude = claude or Claude(cfg, g.get("draft_model", "claude-opus-5-5"), g.get("workers", 4))
    ex = exemplar_text(cfg) if exemplars else ""
    jobs = [dict(id=r["id"], op="write", sample=0, input=r["notes"], words=r["words"]) for r in data]
    texts = claude.map([(prompt("explain_claude", words=r["words"], notes=r["notes"], exemplars=ex),) for r in data])
    items, stats = baselines._pick(cfg, jobs, [t.strip() for t in texts], 1, claude, ctx)
    stats.update(task="explain", exemplars=exemplars)
    return _save(cfg, name, part, items, stats) if limit is None else dict(stats, items=items)


def kit(cfg: dict, a: str, b: str, part: str = "dev", seed: int = 0, show_notes: bool = True) -> dict:
    """A blind reading kit: for each item the two systems' passages as X and Y in random order.
    The key is a separate file. Local files only; nothing is published."""
    def load(name):
        f = Path(cfg["paths"]["eval"]) / "outputs" / name / f"{part}.jsonl"
        return {i["id"]: i for i in map(json.loads, f.read_text().splitlines())}

    A, B = load(a), load(b)
    ids = sorted(set(A) & set(B))
    rng = random.Random(seed)
    rng.shuffle(ids)
    L, key = [f"# Blind read: two systems, same notes ({len(ids)} items)", "",
              "For each item pick the passage that reads more like a good textbook: X, Y, or = for no preference.", ""], {}
    for n, i in enumerate(ids, 1):
        flip = rng.random() < 0.5
        x, y = (B[i], A[i]) if flip else (A[i], B[i])
        key[str(n)] = dict(id=i, X=b if flip else a, Y=a if flip else b)
        L += [f"## {n}", ""] + (["<details><summary>Notes</summary>", "", "```", A[i]["input"], "```", "", "</details>", ""] if show_notes else [])
        L += ["**X**", "", x["text"], "", "**Y**", "", y["text"], "", "Pick: ", "", "---", ""]
    d = Path(cfg["paths"]["home"]) / "examples"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"blind-{a}-vs-{b}.md").write_text("\n".join(L))
    (d / f"blind-{a}-vs-{b}.key.json").write_text(json.dumps(key, indent=1))
    return dict(items=len(ids), kit=str(d / f"blind-{a}-vs-{b}.md"), key=str(d / f"blind-{a}-vs-{b}.key.json"))
