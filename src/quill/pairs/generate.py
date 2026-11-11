"""Phase 3 pair inputs (plan.md Phase 3). The target is always the author's chunk, verbatim.

  form A  a neutral paraphrase of the chunk            (input tag: paraphrase)
  form B  a generic assistant draft from the fact list  (input tag: draft)
The Claude half of form B reuses the train drafts made for the verifier (eval.inputs). The
target carries a <QUOTE> or <IMAGE> line where a quotation or image was removed; the input
carries the same lines, so the model learns to keep a marker, never to invent one.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..eval import inputs, pool
from ..gen.claude_cli import SYSTEM, Claude, prompt

VERSION = "v1"
MARKER = re.compile(r"^<(?:QUOTE|IMAGE)>$", re.M)
PARTS = ("train", "dev")          # dev pairs are for loss monitoring only; test is never touched


def pairs_dir(cfg: dict) -> Path:
    return Path(cfg["paths"]["home"]) / "pairs" / VERSION


def markers(text: str) -> list[str]:
    return MARKER.findall(text)


def chunks(cfg: dict, parts=PARTS) -> list[dict]:
    return [c for c in pool.author_chunks(cfg) if c["split"] in parts]


def _util(cfg: dict) -> Claude:
    g = cfg.get("gen", {})
    return Claude(cfg, g.get("util_model", "claude-sonnet-5-5"), g.get("workers", 4))


def _keep(items: list[str] | None) -> str:
    """The retry note that names what an earlier attempt lost. The prompt files end with the text
    block, so the note goes in front of it."""
    return "\n\n" + prompt("keep", keep="\n".join(f"- {x}" for x in items)) if items else ""


def _with_keep(name: str, items: list[str] | None, **kw) -> str:
    head, sep, tail = prompt(name, **kw).rpartition("\n\n")
    return head + _keep(items) + sep + tail if items else prompt(name, **kw)


def paraphrases(cfg: dict, rows: list[dict], sample: int = 0, claude: Claude | None = None,
                keep: list[list[str]] | None = None) -> list[str]:
    claude = claude or _util(cfg)
    keep = keep or [None] * len(rows)
    return claude.map([(_with_keep("paraphrase", k, text=c["marked"]), SYSTEM, sample) for c, k in zip(rows, keep)])


def redraft(cfg: dict, rows: list[dict], facts: list[str], keep: list[list[str]], sample: int,
            claude: Claude | None = None, drafter: Claude | None = None) -> tuple[list[str], list[str]]:
    """New fact lists (only where items were lost) and new drafts, with markers placed."""
    claude = claude or _util(cfg)
    g = cfg.get("gen", {})
    drafter = drafter or Claude(cfg, g.get("draft_model", "claude-opus-5-5"), g.get("workers", 4))
    todo = [i for i, k in enumerate(keep) if k]
    new = claude.map([(_with_keep("facts", keep[i], text=rows[i]["text"]), SYSTEM, sample) for i in todo])
    facts = list(facts)
    for i, f in zip(todo, new):
        facts[i] = f
    drafts = drafter.map([(prompt("draft", facts=f, words=c["words"]), SYSTEM, sample) for c, f in zip(rows, facts)])
    return facts, place_markers(cfg, rows, drafts, claude)


def insert_markers(draft: str, marks: list[str], after: list[int]) -> str:
    """Put each marker line after the draft paragraph it was assigned to (0 = before the first)."""
    paras = [p for p in draft.split("\n\n") if p.strip()]
    out = [m for m, a in zip(marks, after) if a <= 0]
    for i, p in enumerate(paras, 1):
        out.append(p)
        out += [m for m, a in zip(marks, after) if a == i or (i == len(paras) and a > i)]
    return "\n\n".join(out)


def place_markers(cfg: dict, rows: list[dict], drafts: list[str], claude: Claude | None = None) -> list[str]:
    """Drafts were written from fact lists, so they hold no markers. Claude says which draft
    paragraph each marker follows; the insertion itself is done here, so the draft's words
    cannot change. A reply that does not parse puts the markers at the end."""
    claude = claude or _util(cfg)
    todo = [(i, c, d) for i, (c, d) in enumerate(zip(rows, drafts)) if markers(c["marked"])]
    jobs = []
    for _, c, d in todo:
        paras = [p for p in d.split("\n\n") if p.strip()]
        numbered = "\n\n".join(f"[{k}] {p}" for k, p in enumerate(paras, 1))
        jobs.append((prompt("place_markers", n=len(markers(c["marked"])), text=c["marked"], draft=numbered),))
    out = list(drafts)
    for (i, c, d), reply in zip(todo, claude.map(jobs)):
        marks = markers(c["marked"])
        nums = [int(x) for x in re.findall(r"\d+", reply)]
        if len(nums) != len(marks):
            nums = [10 ** 6] * len(marks)
        out[i] = insert_markers(d, marks, sorted(nums))
    return out


def make(cfg: dict, limit: int | None = None, claude: Claude | None = None) -> dict:
    """Write <pairs>/raw.jsonl: one row per train or dev chunk with both inputs."""
    claude = claude or _util(cfg)
    rows = chunks(cfg)
    have = {r["id"]: r for r in inputs.train_drafts(cfg)}
    have.update({r["id"]: r for r in inputs.load(cfg, "dev")})
    rows = [c for c in rows if c["id"] in have][:limit]
    para = paraphrases(cfg, rows, claude=claude)
    drafts = place_markers(cfg, rows, [have[c["id"]]["draft"] for c in rows], claude)
    out = [dict(id=c["id"], split=c["split"], post=c["post"], words=c["words"], bucket=c["bucket"],
                target=c["marked"], facts=have[c["id"]]["facts"], paraphrase=p, draft=d,
                paraphrase_model=claude.model, draft_model=cfg.get("gen", {}).get("draft_model"), sample=0)
           for c, p, d in zip(rows, para, drafts)]
    stats = dict(n=len(out), new_calls=claude.calls, cost_usd=round(claude.cost, 2))
    if limit is None:
        d = pairs_dir(cfg)
        d.mkdir(parents=True, exist_ok=True)
        (d / "raw.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
        stats["file"] = str(d / "raw.jsonl")
    return dict(stats, rows=out if limit else None)
