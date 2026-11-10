"""M11 frontier judge (optional, diagnostic): Claude picks which of two passages reads more like
the author of some reference excerpts. Each pair is asked in both orders; only consistent picks
count. The judge is usable only if it picks the author's real text over an impostor's on at
least 75% of dev pairs. It is never told the author's name.
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path

from ..gen.claude_cli import Claude, prompt
from . import blind, harness, pool

BAR = 0.75


def _refs(train: list[dict], rng: random.Random, k: int = 3) -> str:
    return "\n\n---\n\n".join(blind.trim(blind.normalize(c["text"]), 150) for c in rng.sample(train, k))


def ask(claude: Claude, pairs: list[tuple[str, str, str]]) -> list[int]:
    """pairs: (references, x, y). Returns +1 if x wins in both orders, -1 if y does, 0 if the picks disagree."""
    jobs = []
    for refs, x, y in pairs:
        jobs += [(prompt("judge", references=refs, a=x, b=y),), (prompt("judge", references=refs, a=y, b=x),)]
    out = [o.strip().upper()[:1] for o in claude.map(jobs)]
    res = []
    for i in range(0, len(out), 2):
        first, second = out[i], out[i + 1]
        res.append(1 if (first, second) == ("A", "B") else -1 if (first, second) == ("B", "A") else 0)
    return res


def _tally(v: list[int]) -> dict:
    n = len(v)
    return dict(pairs=n, x_wins=v.count(1), y_wins=v.count(-1), inconsistent=v.count(0),
                x_share=round(v.count(1) / n, 4) if n else None)


def run(cfg: dict, part: str = "dev", n: int = 40, systems=("b0", "b1"), seed: int = 0, claude: Claude | None = None) -> dict:
    g = cfg.get("gen", {})
    claude = claude or Claude(cfg, g.get("judge_model", g.get("util_model", "claude-sonnet-5-5")), g.get("workers", 4))
    rng = random.Random(seed)
    chunks = pool.author_chunks(cfg)
    train = [c for c in chunks if c["split"] == "train"]
    held = [c for c in chunks if c["split"] == part]
    rng.shuffle(held)
    held = held[:n]
    imp = [p for p in pool.impostors(cfg) if p["part"] == part and p["kind"] == "human"]
    rep = dict(system="judge", split=part, model=claude.model, generated=time.strftime("%Y-%m-%dT%H:%M:%S"), bar=BAR)
    # validation: the author's held-out passage (x) against a human impostor's (y)
    val = [(_refs(train, rng), *blind.match(c["text"], rng.choice(imp)["text"], cap=300)) for c in held]
    rep["validation_real_vs_impostor"] = v = _tally(ask(claude, val))
    rep["pass"] = v["x_share"] >= BAR
    out = {}
    for s in systems:
        f = Path(cfg["paths"]["eval"]) / "outputs" / s / f"{part}.jsonl"
        if f.exists():
            out[s] = {r["id"]: r["text"] for r in map(json.loads, f.read_text().splitlines()) if r.get("op") == "restyle"}
    # the author's real passage (x) against each system on the same content (y)
    for s, o in out.items():
        prs = [(_refs(train, rng), *blind.match(c["text"], o[c["id"]], cap=300)) for c in held if c["id"] in o]
        rep[f"real_vs_{s}"] = _tally(ask(claude, prs))
    names = list(out)
    for i, a in enumerate(names):                   # system against system, same input
        for b in names[i + 1:]:
            prs = [(_refs(train, rng), *blind.match(out[a][c["id"]], out[b][c["id"]], cap=300)) for c in held
                   if c["id"] in out[a] and c["id"] in out[b]]
            rep[f"{a}_vs_{b}"] = _tally(ask(claude, prs))
    rep["new_calls"], rep["cost_usd"] = claude.calls, round(claude.cost, 2)
    d = harness.REPO / "eval_reports"
    (d / f"m11-judge-{part}.json").write_text(json.dumps(rep, indent=1))
    L = [f"# M11 judge on {part} ({rep['generated']})", "",
         f"Model {claude.model}. Each pair is asked in both orders; a win needs the same pick both times. "
         f"The judge is valid if it picks the author's real passage over a human impostor's on at least {BAR:.0%} of pairs. "
         "Diagnostic only. The judge is a Claude model, and b0 is Claude output.", "",
         "| Comparison (x vs y) | Pairs | x wins | y wins | Inconsistent | x share |", "|---|---|---|---|---|---|"]
    for k, t in rep.items():
        if isinstance(t, dict) and "pairs" in t:
            L.append(f"| {k.replace('_', ' ')} | {t['pairs']} | {t['x_wins']} | {t['y_wins']} | {t['inconsistent']} | {t['x_share']:.1%} |")
    L += ["", f"Validation {'passes' if rep['pass'] else 'FAILS'}."]
    (d / f"m11-judge-{part}.md").write_text("\n".join(L) + "\n")
    rep["_out"] = str(d / f"m11-judge-{part}.md")
    return rep
