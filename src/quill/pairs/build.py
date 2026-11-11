"""The Phase 3 pipeline: generate, curate, regenerate failed paraphrases, write the mlx data."""
from __future__ import annotations

import json

from . import curate as C
from . import generate as G
from . import to_mlx


def run(cfg: dict, retries: int = 1) -> dict:
    claude = G._util(cfg)
    stats = G.make(cfg, claude=claude)
    f = G.pairs_dir(cfg) / "raw.jsonl"
    rows = [json.loads(x) for x in f.read_text().splitlines()]
    count = C.token_counter(cfg)
    C.score(cfg, rows, count=count)
    marked = {c["id"]: c for c in G.chunks(cfg)}
    redone = dict(A=0, B=0)

    def retry(form: str, s: int) -> None:
        """Regenerate the failed inputs of one form, naming what the last attempt lost. A new input
        replaces the old one only when it fails fewer checks."""
        key = C.FORMS[form]
        bad = [r for r in rows if set(r["checks"][form]["fails"]) - {"tokens"}]
        if not bad:
            return
        keep = [C.lost_items(r[key], r["target"]) for r in bad]
        src = [marked[r["id"]] for r in bad]
        if form == "A":
            trial = [dict(r, paraphrase=p, checks={}) for r, p in zip(bad, G.paraphrases(cfg, src, s, claude, keep))]
        else:
            facts, drafts = G.redraft(cfg, src, [r["facts"] for r in bad], keep, s, claude)
            trial = [dict(r, facts=f, draft=d, checks={}) for r, f, d in zip(bad, facts, drafts)]
        C.score(cfg, trial, count=count, forms=(form,))
        for r, t in zip(bad, trial):
            if len(t["checks"][form]["fails"]) < len(r["checks"][form]["fails"]):
                r.update({k: t[k] for k in (key, "facts")}, **{f"{key}_sample": s})
                r["checks"][form] = t["checks"][form]
                redone[form] += 1

    for s in range(1, retries + 1):
        retry("A", s)
        retry("B", s)
    (G.pairs_dir(cfg) / "curated.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    data = to_mlx.write(cfg, rows)
    rep = C.report(cfg, rows, dict(inputs_replaced_on_retry=redone))
    return dict(rep, data={k: dict(rows=v["rows"], dir=v["dir"]) for k, v in data.items()},
                new_calls=stats["new_calls"] + claude.calls, cost_usd=round(claude.cost, 2))
