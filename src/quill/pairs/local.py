"""The local half of form B (plan.md Phase 4, step 9).

The untuned base drafts from the fact list with the Claude draft prompt, so stage 2 trains on
the kind of draft the runtime `write` drafter makes. Chunks with <QUOTE>/<IMAGE> markers keep
their Claude draft: placing markers in a new draft takes a Claude call. Nothing here leaves the Mac.
"""
from __future__ import annotations

import json
import zlib

from . import curate as C
from . import generate as G
from . import to_mlx

CLAUDE_SHARE = 8        # one in this many marker-free chunks keeps its Claude draft


def wants_local(row: dict) -> bool:
    return not G.markers(row["target"]) and zlib.crc32(row["id"].encode()) % CLAUDE_SHARE != 0


def run(cfg: dict, retries: int = 2, limit: int | None = None, base=None) -> dict:
    from ..eval.baselines import draft_from, prompt
    from ..gen.local import Local

    f = G.pairs_dir(cfg) / "curated.jsonl"
    rows = [json.loads(x) for x in f.read_text().splitlines()]
    todo = [r for r in rows if wants_local(r) and not r["checks"]["B"]["fails"]][:limit]
    base = base or Local(cfg)
    for i, r in enumerate(todo):
        r["draft_local"], r["draft_local_tries"] = draft_from(
            base, prompt("draft", facts=r["facts"], words=r["words"]), r["facts"], r["words"], retries)
        r["draft_local_model"] = base.model
        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(todo)}  new {base.calls}", flush=True)
    if hasattr(base, "unload"):
        base.unload()
    trial = [dict(r, draft=r["draft_local"], checks={}) for r in todo]
    C.score(cfg, trial, forms=("B",))
    for r, t in zip(todo, trial):
        r["checks"]["L"] = t["checks"]["B"]
    fails = [x for r in todo for x in r["checks"]["L"]["fails"]]
    out = dict(drafted=len(todo), kept=sum(not r["checks"]["L"]["fails"] for r in todo),
               fails={k: fails.count(k) for k in sorted(set(fails))},
               redrafted=sum(r["draft_local_tries"] > 1 for r in todo), model=base.model)
    if limit is None:
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        out["data"] = {k: dict(rows=v["rows"], local=v.get("local")) for k, v in to_mlx.write(cfg, rows).items()}
    return out
