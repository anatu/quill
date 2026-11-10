"""Phase 1 corpus build: extract, clean, twin-group, dedupe, chunk, store, report."""
from __future__ import annotations

import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

from ..clean import boilerplate, chunk, dedupe, pii_regex
from ..clean.twins import find_twins, split_groups
from ..ingest.collabfund import read_posts
from . import store

QUOTE_REASONS = ("blockquote", "inline_quote", "quote_attribution")


def slug_of(file: str) -> str:
    return re.sub(r"^collabfund\.com_blog_|_?\.html$", "", file)


def _words(p: dict) -> int:
    return sum(len(b["text"].split()) for b in p["blocks"])


def tier(words: int) -> str:
    for name, top in (("T0", 10_000), ("T1", 40_000), ("T2", 100_000), ("T3", 1_000_000)):
        if words < top:
            return name
    return "T4"


def build(cfg: dict, raw: Path | None = None) -> dict:
    raw = Path(raw or cfg["paths"]["raw"])
    c = cfg["corpus"]
    dd, ch = c.get("dedupe", {}), c.get("chunk", {})
    drop_cfg, tag_cfg = c.get("drop_posts") or {}, c.get("post_tags") or {}
    consent_ref = str(cfg.get("decisions", {}).get("consent_record", ""))

    posts = read_posts(raw)
    own_words = sum(len(b["text"].split()) for p in posts for b in p["blocks"] if not b["bq"])
    for p in posts:
        p["slug"] = slug_of(p["file"])
        p["consent_ref"] = consent_ref
        p["tags"] = list(tag_cfg.get(p["slug"], []))
        p["kept"], p["drop_reason"] = True, None
        p["blocks"], p["dropped"] = boilerplate.clean_post(p["blocks"], quotes=(c.get("unmarked_quotes") or {}).get(p["slug"], ()))
        if (p["author"] or "") != cfg["author"]["name"]:
            p["kept"], p["drop_reason"] = False, "other_author"
        elif p["slug"] in drop_cfg:
            p["kept"], p["drop_reason"] = False, drop_cfg[p["slug"]]

    live = [p for p in posts if p["kept"]]
    repeated = boilerplate.drop_repeated(live)
    for p in live:
        if _words(p) < c["min_post_words"]:
            p["kept"], p["drop_reason"] = False, "under_min_words"

    live = [p for p in posts if p["kept"]]
    tw = find_twins({p["file"]: "\n".join(b["text"] for b in p["blocks"]) for p in live},
                    n=c["twin_ngram"], share=c["twin_share"])
    groups = split_groups(tw, min_link=c.get("twin_link_min", 0.05))
    by_file = {p["file"]: p for p in posts}
    for i, g in enumerate(groups, 1):
        for f in g:
            by_file[f]["twin_group"] = f"t{i:02d}"
    for f in tw["twin_posts"]:
        by_file[f]["twin_links"] = [[slug_of(o), s] for o, s in tw["links"].get(f, [])[:5]]
        by_file[f]["tags"].append("twin")

    words_before_dedupe = sum(_words(p) for p in live)
    n_dups = dedupe.dedupe_posts(live, n=dd.get("shingle", 5), jaccard=dd.get("jaccard", 0.85),
                                 min_words=dd.get("min_words", 20))
    for p in live:
        if _words(p) < c["min_post_words"]:
            p["kept"], p["drop_reason"] = False, "under_min_words_after_dedupe"

    pii_hits = []
    for p in posts:
        p["words"] = _words(p)
        p["quote_words"] = sum(d["words"] for d in p["dropped"] if d["reason"] in QUOTE_REASONS)
        p["chunks"] = []
        if not p["kept"]:
            continue
        for i, k in enumerate(chunk.chunk_post(p["blocks"], key=p["slug"], lo=ch.get("min_words", 150),
                                               hi=ch.get("max_words", 800), targets=ch.get("targets"),
                                               markers=ch.get("gap_markers"))):
            k["id"] = f"{p['slug']}#{i:02d}"
            k["flags"] += [t for t in p["tags"] if t != "twin"]
            hits = pii_regex.find(k["text"])
            if hits:
                k["flags"].append("pii")
                pii_hits += [dict(chunk=k["id"], kind=h["kind"], match=h["match"]) for h in hits]
            p["chunks"].append(k)

    kept = [p for p in posts if p["kept"]]
    chunks = [k for p in kept for k in p["chunks"]]
    reasons = Counter(d["reason"] for p in posts if p["kept"] or p["drop_reason"] != "other_author"
                      for d in p["dropped"])
    reason_words = Counter()
    samples = defaultdict(list)
    for p in posts:
        for d in p["dropped"]:
            reason_words[d["reason"]] += d["words"]
            if len(samples[d["reason"]]) < 8 and d["text"][:120] not in samples[d["reason"]]:
                samples[d["reason"]].append(d["text"][:120])
    total = sum(p["words"] for p in kept)
    expected = cfg.get("expected", {}).get("words")
    cw = sorted(k["words"] for k in chunks)
    report = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "raw": str(raw),
        "pages": len(posts),
        "kept_posts": len(kept),
        "words": total,
        "tier": tier(total),
        "phase0_words": expected,
        "word_delta": total - expected if expected else None,
        "own_words_before_cleaning": own_words,
        "words_before_dedupe": words_before_dedupe,
        "quote_words": sum(p["quote_words"] for p in posts),
        "dropped_posts": [dict(slug=p["slug"], reason=p["drop_reason"], words=p["words"], title=p["title"])
                          for p in posts if not p["kept"]],
        "dropped_blocks": {r: dict(blocks=n, words=reason_words[r]) for r, n in reasons.most_common()},
        "dropped_samples": dict(samples),
        "repeated_boilerplate": repeated,
        "duplicate_paragraphs": n_dups,
        "twins": dict(posts=len(tw["twin_posts"]), groups=[[slug_of(f) for f in g] for g in groups],
                      cross_post_ngram_share=round(tw["shared_share"], 4)),
        "chunks": dict(n=len(chunks), words=sum(cw), median=cw[len(cw) // 2] if cw else 0,
                       buckets=dict(Counter(k["bucket"] for k in chunks)),
                       flags=dict(Counter(f for k in chunks for f in k["flags"]))),
        "years": dict(sorted(Counter(p["date"][:4] for p in kept if p["date"]).items())),
        "pii_hits": pii_hits,
        "tagged_posts": {p["slug"]: p["tags"] for p in kept if set(p["tags"]) - {"twin"}},
    }
    db = store.connect(store.db_path(cfg))
    store.write_corpus(db, posts, {"build": {k: v for k, v in report.items() if k != "dropped_samples"}})
    db.close()
    out = Path(cfg["paths"]["corpus"])
    (out / "cleaning_report.json").write_text(json.dumps(report, indent=1))
    (out / "cleaning_report.md").write_text(render_report(report))
    report["_out"] = str(out / "cleaning_report.md")
    return report


def render_report(r: dict) -> str:
    L = [f"# Cleaning report ({r['generated']})", "",
         f"- Pages {r['pages']}; kept posts {r['kept_posts']}; words {r['words']:,}; tier {r['tier']}.",
         f"- Phase 0 figure {r['phase0_words']:,}; difference {r['word_delta']:+,} (explained below).",
         f"- Quote words stripped {r['quote_words']:,}. Duplicate paragraphs dropped {r['duplicate_paragraphs']} "
         f"({r['dropped_blocks'].get('duplicate_paragraph', {}).get('words', 0):,} words).",
         f"- Twin posts {r['twins']['posts']}; split groups {len(r['twins']['groups'])}; "
         f"cross-post 10-gram share before dedupe {r['twins']['cross_post_ngram_share']:.1%}.",
         f"- Chunks {r['chunks']['n']}; median {r['chunks']['median']} words; buckets {r['chunks']['buckets']}; "
         f"flags {r['chunks']['flags']}.",
         f"- PII hits {len(r['pii_hits'])}.", "",
         "## Dropped posts", "", "| Post | Reason | Words left | Title |", "|---|---|---|---|"]
    L += [f"| {p['slug']} | {p['reason']} | {p['words']} | {p['title']} |" for p in r["dropped_posts"]]
    gone = sum(v["words"] for k, v in r["dropped_blocks"].items() if k != "blockquote")
    L += ["", "## Word reconciliation", "",
          f"- Phase 0 reader (generic rules): {r['phase0_words']:,} words in 342 posts.",
          f"- Phase 1 reader, text outside block quotes, all {r['pages']} pages: {r['own_words_before_cleaning']:,}.",
          f"- Minus dropped blocks other than block quotes (table below): {gone:,}.",
          f"- Minus text left in dropped posts: {sum(p['words'] for p in r['dropped_posts']):,}.",
          f"- Kept: {r['words']:,}. Footnote markers and whitespace account for any remainder."]
    L += ["", "## Dropped blocks", "", "| Reason | Blocks | Words |", "|---|---|---|"]
    L += [f"| {k} | {v['blocks']} | {v['words']:,} |" for k, v in r["dropped_blocks"].items()]
    L += ["", "## Samples of dropped blocks", ""]
    for k, v in r["dropped_samples"].items():
        L += [f"**{k}**", ""] + [f"- {t}" for t in v] + [""]
    L += ["## Twin groups (must share a split)", ""] + [f"- {', '.join(g)}" for g in r["twins"]["groups"]]
    L += ["", "## Posts per year", "", ", ".join(f"{y}: {n}" for y, n in r["years"].items()), ""]
    if r["pii_hits"]:
        L += ["## PII hits (review)", ""] + [f"- {h['chunk']}: {h['kind']} `{h['match']}`" for h in r["pii_hits"]]
    if r["tagged_posts"]:
        L += ["", "## Tagged posts", ""] + [f"- {s}: {', '.join(t)}" for s, t in r["tagged_posts"].items()]
    return "\n".join(L) + "\n"
