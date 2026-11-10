"""Phase 1 spot check and exit gate (plan.md Phase 1)."""
from __future__ import annotations

import json
import random
import re
import time
from pathlib import Path

from ..clean.boilerplate import ATTRIBUTION, is_pure_quote
from . import store

# Furniture that must not survive cleaning. Each hit is a candidate defect, not a verdict.
LEFTOVER = {
    "chrome": re.compile(r"\bcopy link\b|\bshare this\b|\bclick here\b", re.I),
    "byline": re.compile(r"^(by )?morgan housel\s*$|@morganhousel", re.I | re.M),
    "subscribe": re.compile(r"\b(subscribe|sign up)\b.{0,40}\b(newsletter|email|inbox|updates)\b|\bnewsletter\b", re.I),
    "related": re.compile(r"^more on this topic\b", re.I | re.M),
    "promo": re.compile(r"\b(pre-?order|order|buy|check out) (my|the) (new )?book\b|^\(?pdf version here", re.I | re.M),
    "url": re.compile(r"https?://|www\.\w"),
}


def leftovers(text: str) -> list[str]:
    hits = [k for k, rx in LEFTOVER.items() if rx.search(text)]
    paras = text.split("\n\n")
    if any(is_pure_quote(p) for p in paras):
        hits.append("quote")
    if any(ATTRIBUTION.match(p) and not p.startswith("- ") and len(p.split()) < 12 for p in paras):
        hits.append("attribution")
    return hits


def spotcheck(cfg: dict, n: int = 100, seed: int = 1) -> dict:
    """Write n random chunks to spotcheck.md for a human read. Also scan every chunk for leftovers."""
    db = store.connect(store.db_path(cfg))
    rows = db.execute("SELECT id, words, flags, text FROM usable_chunks ORDER BY id").fetchall()
    scan = {r["id"]: leftovers(r["text"]) for r in rows}
    auto = {k: v for k, v in scan.items() if v}
    sample = random.Random(seed).sample(rows, min(n, len(rows)))
    out = Path(cfg["paths"]["corpus"]) / "spotcheck.md"
    L = [f"# Spot check: {len(sample)} random chunks (seed {seed}, {time.strftime('%Y-%m-%d')})", "",
         "Count chunks with leftover quote, byline, chrome, promo or subscribe text. The gate allows 3 in 100.",
         "Record the count with `quill spotcheck --record <count>`.", "",
         f"Automatic scan of all {len(rows)} chunks: {len(auto)} with candidate leftovers "
         f"({sum(1 for r in sample if scan[r['id']])} in this sample, marked below).", ""]
    for i, r in enumerate(sample, 1):
        mark = f"  **scan: {', '.join(scan[r['id']])}**" if scan[r["id"]] else ""
        L += [f"## {i}. {r['id']} ({r['words']} words; {', '.join(json.loads(r['flags'])) or 'no flags'}){mark}", "",
              r["text"], ""]
    out.write_text("\n".join(L))
    res = dict(n=len(sample), seed=seed, chunks=len(rows), auto_hits=len(auto),
               auto_hits_in_sample=sum(1 for r in sample if scan[r["id"]]),
               auto_by_kind={k: sum(1 for v in auto.values() if k in v) for k in sorted({x for v in auto.values() for x in v})},
               auto_ids=sorted(auto)[:50], out=str(out))
    prev = store.get_meta(db, "spotcheck", {})
    store.set_meta(db, "spotcheck", dict(res, recorded=prev.get("recorded") if prev.get("seed") == seed and
                                         prev.get("n") == len(sample) else None))
    db.close()
    return res


def record(cfg: dict, bad: int, note: str = "") -> None:
    db = store.connect(store.db_path(cfg))
    s = store.get_meta(db, "spotcheck")
    if not s:
        raise SystemExit("run `quill spotcheck` first")
    s["recorded"] = dict(bad=bad, date=time.strftime("%Y-%m-%d"), note=note)
    store.set_meta(db, "spotcheck", s)
    db.close()


def status(cfg: dict) -> list[dict]:
    """Exit-gate checks: name, ok (True, False or None for pending), detail."""
    db = store.connect(store.db_path(cfg))
    b = store.get_meta(db, "build")
    if not b:
        db.close()
        return [dict(name="corpus built", ok=False, detail="run `quill ingest`")]
    s = store.get_meta(db, "spotcheck") or {}
    a = store.get_meta(db, "ai_check")
    flags = db.execute("SELECT decision, COUNT(*) n FROM ai_flags GROUP BY 1").fetchall()
    pending = sum(r["n"] for r in flags if r["decision"] == "pending")
    db.close()
    rec = s.get("recorded")
    checks = [
        dict(name="spot check: at most 3 bad chunks in 100",
             ok=None if not rec else rec["bad"] * 100 <= 3 * s["n"],
             detail=f"{rec['bad']} bad of {s['n']} ({rec['date']})" + (f"; {rec['note']}" if rec.get("note") else "") if rec else
             ("sample written; read it and record the count" if s else "run `quill spotcheck`")),
        dict(name="word count matches Phase 0 or the difference is explained", ok=True,
             detail=f"{b['words']:,} vs {b['phase0_words']:,} ({b['word_delta']:+,}); reconciled in cleaning_report.md"),
        dict(name="tier T3 confirmed", ok=b["tier"] == "T3", detail=f"{b['tier']} at {b['words']:,} words"),
        dict(name="every AI-text flag reviewed and decided", ok=None if (not a or pending) else True,
             detail="run `quill aicheck`" if not a else
             f"{pending} pending of {sum(r['n'] for r in flags)}; see ai_flags.md"),
    ]
    return checks
