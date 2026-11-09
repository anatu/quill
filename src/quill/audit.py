"""Phase 0 audit: inventory the raw corpus and check it against the measured figures."""
from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

from .clean.twins import find_twins
from .ingest.collabfund import load_posts

# Figures from a different parser may drift a little; exact ones must match.
TOLERANCE = {"pages": 0, "kept_posts": 0, "words": 0, "quote_words": 0.05, "twin_posts": 0.25,
             "share_post_2022": 0.02}


def run(cfg: dict, raw: Path | None = None, out: Path | None = None) -> dict:
    raw = Path(raw or cfg["paths"]["raw"])
    out = Path(out or cfg["paths"]["audit"]) / "inventory.json"
    c = cfg["corpus"]
    posts, removed = load_posts(raw)
    kept = [p for p in posts if p["words"] >= c["min_post_words"]]
    dropped = [p for p in posts if p["words"] < c["min_post_words"]]
    tw = find_twins({p["file"]: "\n".join(p["paras"]) for p in kept}, n=c["twin_ngram"], share=c["twin_share"])
    years = Counter(p["year"] for p in kept)
    post22 = sum(1 for p in kept if p["year"] and p["year"] > 2022)
    lengths = sorted(p["words"] for p in kept)

    measured = {
        "pages": len(posts),
        "kept_posts": len(kept),
        "words": sum(p["words"] for p in kept),
        "quote_words": sum(p["quote_words"] for p in posts),
        "twin_posts": len(tw["twin_posts"]),
        "share_post_2022": round(post22 / len(kept), 3) if kept else 0.0,
    }
    checks = []
    for k, exp in cfg.get("expected", {}).items():
        got = measured.get(k)
        tol = TOLERANCE.get(k, 0)
        ok = got == exp if tol == 0 else abs(got - exp) <= (tol if k == "share_post_2022" else tol * exp)
        checks.append(dict(field=k, expected=exp, measured=got, ok=ok))

    inv = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "raw": str(raw),
        "config": cfg["_file"],
        "measured": measured,
        "checks": checks,
        "years": {str(k): v for k, v in sorted(years.items(), key=lambda x: (x[0] is None, x[0]))},
        "length_words": {"median": lengths[len(lengths) // 2] if lengths else 0,
                         "p90": lengths[int(0.9 * len(lengths))] if lengths else 0,
                         "min": lengths[0] if lengths else 0, "max": lengths[-1] if lengths else 0},
        "authors": Counter(p["author"] for p in posts).most_common(5),
        "cross_post_ngram_share": round(tw["shared_share"], 4),
        "twin_posts": tw["twin_posts"],
        "twin_groups": tw["groups"],
        "dropped_short": [dict(file=p["file"], words=p["words"], title=p["title"][:100]) for p in dropped],
        "boilerplate_removed": removed[:50],
        "posts": [dict(file=p["file"], title=p["title"][:120], year=p["year"], words=p["words"],
                       quote_words=p["quote_words"]) for p in posts],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inv, indent=1))
    inv["_out"] = str(out)
    return inv
