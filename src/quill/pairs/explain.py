"""The explain task: write a textbook passage from sparse notes (logbook 2026-11-14/15).

Restyling holds the content fixed, so it cannot teach the decisions that make textbook prose good:
which point to restate, where to work an example, which near-synonyms to separate. Here the input
is deliberately thin. Claude reduces each passage to CORE (the few points it teaches) and MATERIAL
(the specific details it draws on, as bare data). The adapter learns to write the passage from
those notes. MATERIAL is shuffled, so the order of exposition is the model's to choose. Every name
and number in a target is still in its input, so the entity gate applies as before.
"""
from __future__ import annotations

import json
import random
import re
import time
from pathlib import Path

from .. import config as _config
from .. import template
from ..gen.claude_cli import SYSTEM, prompt
from . import curate as C
from . import generate as G

STAGE = "x1"
RATIO_LO, RATIO_HI = 0.10, 0.75        # notes words / target words. Short chunks get thick notes (median 0.67 under
                                       # 300 words); a fact list runs 0.79 and keeps the passage's order
MIN_CORE = 2
BULLET = re.compile(r"^\s*[-*•]\s+(.*\S)\s*$")


def parse(text: str) -> tuple[list[str], list[str]]:
    """CORE and MATERIAL bullets from Claude's reply. Empty lists if the shape is wrong."""
    m = re.search(r"CORE:\s*(.*?)\s*MATERIAL:\s*(.*)\Z", text, re.S)
    if not m:
        return [], []
    bullets = lambda t: [b.group(1) for b in map(BULLET.match, t.splitlines()) if b]      # noqa: E731
    return bullets(m.group(1)), bullets(m.group(2))


def notes_text(core: list[str], material: list[str], key: str) -> str:
    """The model's input. MATERIAL is shuffled by `key`, so its order tells nothing about the passage's."""
    mat = list(material)
    random.Random(key).shuffle(mat)
    return "CORE:\n" + "\n".join(f"- {x}" for x in core) + "\nMATERIAL:\n" + "\n".join(f"- {x}" for x in mat)


def file(cfg: dict) -> Path:
    return G.pairs_dir(cfg) / "explain.jsonl"


def messages(row: dict) -> list[dict]:
    return template.messages("explain", "notes", template.bucket(row["words"]), row["notes"], row["target"])


def check(row: dict, tokens: int) -> list[str]:
    fails = []
    if len(row["core"]) < MIN_CORE or not row["material"]:
        return ["shape"]
    if C.closure(row["notes"], row["target"]):
        fails.append("closure")
    r = len(row["notes"].split()) / max(1, len(C.plain(row["target"]).split()))
    if not RATIO_LO <= r <= RATIO_HI:
        fails.append("ratio")
    if tokens > C.MAX_TOKENS:
        fails.append("tokens")
    return fails


def build_row(c: dict, core: list[str], material: list[str], model: str, count) -> dict:
    """One pair. A name or number the passage has and the notes lack is added to MATERIAL as it
    stands in the passage, with a few words around it: the notes must supply every such item."""
    r = dict(id=c["id"], split=c["split"], post=c["post"], words=c["words"], target=c["target"] if "target" in c else c["marked"],
             core=core, material=list(material), notes_model=model)
    r["notes"] = notes_text(core, r["material"], r["id"])
    lost = C.lost_items(r["notes"], r["target"]) if core else []
    if lost:
        r["material"] += lost
        r["added_material"] = len(lost)
        r["notes"] = notes_text(core, r["material"], r["id"])
    r["tokens"] = count(messages(r)) if core else 0
    r["fails"] = check(r, r["tokens"])
    return r


def recurate(cfg: dict, count=None) -> dict:
    """Rebuild the pairs from the stored notes with the current rules. No Claude calls."""
    from ..scorers import entities

    old = [json.loads(x) for x in file(cfg).read_text().splitlines()]
    entities.set_common(r["target"] for r in old)
    count = count or C.token_counter(cfg)
    data = [build_row(r, r["core"], r["material"][:len(r["material"]) - r.get("added_material", 0)], r["notes_model"], count)
            for r in old]
    rep = report(cfg, data, dict(recurated=True))
    file(cfg).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in data))
    rep["data"] = write(cfg, data)
    return rep


def make(cfg: dict, limit: int | None = None, claude=None, count=None) -> dict:
    from ..scorers import entities

    claude = claude or G._util(cfg)
    rows = G.chunks(cfg)[:limit]
    outs = claude.map([(prompt("notes", text=c["marked"]), SYSTEM, 0) for c in rows])
    entities.set_common(c["marked"] for c in rows)
    count = count or C.token_counter(cfg)
    data = [build_row(c, *parse(o), claude.model, count) for c, o in zip(rows, outs)]
    rep = report(cfg, data, dict(new_calls=claude.calls, cost_usd=round(claude.cost, 2)))
    if limit is None:
        file(cfg).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in data))
        rep["data"] = write(cfg, data)
    return rep


def write(cfg: dict, data: list[dict]) -> dict:
    from .to_mlx import data_dir

    d = data_dir(cfg, STAGE)
    d.mkdir(parents=True, exist_ok=True)
    n = {}
    for name, part in (("train", "train"), ("valid", "dev")):
        keep = [r for r in data if r["split"] == part and not r["fails"]]
        (d / f"{name}.jsonl").write_text("".join(json.dumps(dict(messages=messages(r)), ensure_ascii=False) + "\n" for r in keep))
        n[name] = len(keep)
    (d / "manifest.json").write_text(json.dumps(dict(task="explain", input="notes", rows=n), indent=1))
    return dict(rows=n, dir=str(d))


def report(cfg: dict, data: list[dict], extra: dict | None = None) -> dict:
    """Aggregate numbers only."""
    import statistics as st

    out = dict(generated=time.strftime("%Y-%m-%dT%H:%M:%S"), splits={}, **(extra or {}))
    for part in G.PARTS:
        rows = [r for r in data if r["split"] == part]
        ok = [r for r in rows if not r["fails"]]
        fails = [f for r in rows for f in r["fails"]]
        ratio = [len(r["notes"].split()) / max(1, r["words"]) for r in ok]
        out["splits"][part] = dict(
            chunks=len(rows), kept=len(ok), material_added=sum(1 for r in rows if r.get("added_material")), fails={f: fails.count(f) for f in sorted(set(fails))},
            notes_to_target_words=round(st.median(ratio), 3) if ratio else None,
            core_bullets=st.median(len(r["core"]) for r in ok) if ok else None,
            material_bullets=st.median(len(r["material"]) for r in ok) if ok else None,
            max_tokens=max((r["tokens"] for r in ok), default=0))
    d = _config.reports_dir(_config.REPO, cfg)
    L = [f"# Explain pairs v1: notes → passage ({out['generated']})", "",
         "The input is Claude's reduction of a passage to CORE points and MATERIAL details (shuffled); the target is the "
         f"passage. A pair is kept when the notes have at least {MIN_CORE} core points and some material, the target adds no "
         f"name, number, date or link, the notes are {RATIO_LO}-{RATIO_HI}x the target's length and the example fits "
         f"{C.MAX_TOKENS} tokens.", "",
         "Where the notes missed a name or number of the passage, it was added to MATERIAL from the passage.", "",
         "| Split | Chunks | Kept | Notes/target words | Core bullets | Material bullets | Max tokens | Notes repaired | Fails |",
         "|---|---|---|---|---|---|---|---|---|"]
    for part, v in out["splits"].items():
        L.append(f"| {part} | {v['chunks']} | {v['kept']} ({v['kept'] / max(1, v['chunks']):.1%}) | {v['notes_to_target_words']} | "
                 f"{v['core_bullets']} | {v['material_bullets']} | {v['max_tokens']} | {v['material_added']} | "
                 f"{', '.join(f'{k} {n}' for k, n in v['fails'].items()) or 'none'} |")
    (d / "explain-v1.json").write_text(json.dumps(out, indent=1))
    (d / "explain-v1.md").write_text("\n".join(L) + "\n")
    return out
