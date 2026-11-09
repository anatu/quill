"""AI-text check on posts dated after the cutoff (plan.md Phase 1 step 6).

Four signals, all for human review. Nothing here drops a post.
  lexicon      a family rate above the 95th percentile of the author's pre-cutoff posts
  changepoint  a sustained shift in function words, punctuation and sentence shape (PELT)
  llm_mention  the post names an LLM or quotes one
  llm_link     a link in the post carries a chatbot referrer (utm_source=chatgpt.com) or points at a chatbot
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np

from ..corpus import store
from ..ingest import textlib as T
from ..scorers import lexicon as L

FUNCTION_WORDS = (
    "the of and to a in that is it was for on with as but be at by this have from or not are you they we he his "
    "their what which when there if can will more than so one all about who would has had been were no do its "
    "because how most just i").split()
PUNCT = {"comma": ",", "semicolon": ";", "paren": "(", "question": "?", "exclaim": "!", "quote": "“"}
LLM_MENTION = re.compile(
    r"\b(ChatGPT|GPT-?[345o]\w*|OpenAI|Anthropic|large language models?|LLMs?|chatbots?|Copilot|Bard|"
    r"(asked|told|prompted) (an? )?(AI|Claude|Gemini|Grok)|(AI|Claude|Gemini|Grok) (wrote|said|replied|responded|"
    r"answered|generated)|AI[- ](generated|written))\b")


LLM_LINK = re.compile(r"utm_source=(chatgpt|openai|claude|perplexity|gemini|copilot|grok)|"
                      r"//(chatgpt\.com|chat\.openai\.com|claude\.ai|(www\.)?perplexity\.ai|gemini\.google\.com)", re.I)


def features(text: str) -> np.ndarray:
    """Style vector of one post: function-word shares, punctuation per 1k words, sentence shape."""
    paras = text.split("\n\n")
    toks = T.words(text)
    n = max(1, len(toks))
    cnt = {}
    for w in toks:
        cnt[w] = cnt.get(w, 0) + 1
    fw = [cnt.get(w, 0) / n for w in FUNCTION_WORDS]
    k = 1000.0 / n
    emd = text.count("—") + len(re.findall(r"(?<=\w) ?-- ?(?=\w)", text)) + len(re.findall(r" – ", text))
    colons = len(re.findall(r":(?!\d)", text))
    punct = [k * text.count(ch) for ch in PUNCT.values()] + [k * emd, k * colons]
    sl = [len(T.words(s)) for p in paras for s in T.split_sentences(p)]
    sl = [x for x in sl if x] or [0]
    para_sents = [len(T.split_sentences(p)) for p in paras if p.strip()] or [1]
    shape = [float(np.mean(sl)), float(np.std(sl)), float(np.mean([x <= 5 for x in sl])),
             float(np.mean([x >= 30 for x in sl])), n / max(1, len(para_sents)),
             float(np.mean([x == 1 for x in para_sents]))]
    return np.array(fw + punct + shape, dtype=float)


def distances(X: np.ndarray, base: np.ndarray, clip: float = 4.0) -> np.ndarray:
    """RMS z-distance of each row from the centroid of the baseline rows.

    Baseline rows are scored leave-one-out, so they do not look closer than new rows would.
    """
    B = X[base]
    n = len(B)
    mu, sd = B.mean(0), B.std(0, ddof=1)
    sd[sd == 0] = 1.0
    d = np.empty(len(X))
    for i in range(len(X)):
        if base[i]:
            m = (mu * n - X[i]) / (n - 1)
            var = np.maximum(((B - m) ** 2).sum(0) - (X[i] - m) ** 2, 1e-12) / (n - 2)
            z = (X[i] - m) / np.sqrt(var)
        else:
            z = (X[i] - mu) / sd
        d[i] = np.sqrt(np.mean(np.clip(z, -clip, clip) ** 2))
    return d


def sustained_shifts(d: np.ndarray, base: np.ndarray, dates: list[str], after: str, min_size: int = 3,
                     pct: float = 95.0) -> list[dict]:
    """PELT segments (l2 cost) that start on or after `after` and sit above the baseline.

    A segment counts when its mean and its median distance both beat the `pct` percentile
    of the means of all same-length runs of baseline posts.
    """
    import ruptures as rpt

    n = len(d)
    if n < 2 * min_size or base.sum() < min_size + 1:
        return []
    pen = 2 * np.log(n) * float(np.var(d[base]))        # [P] BIC-style penalty on the baseline variance
    bkps = rpt.Pelt(model="l2", min_size=min_size, jump=1).fit(d.reshape(-1, 1)).predict(pen=pen)
    bd = d[base]
    out, lo = [], 0
    for hi in bkps:
        seg = d[lo:hi]
        if dates[lo] >= after and len(seg) >= min_size:
            L_ = min(len(seg), len(bd))
            runs = np.convolve(bd, np.ones(L_) / L_, mode="valid")
            thr = float(np.percentile(runs, pct))
            if seg.mean() > thr and float(np.median(seg)) > thr:      # the median guards against one odd post
                out.append(dict(start=lo, end=hi, mean=float(seg.mean()), threshold=thr,
                                from_date=dates[lo], to_date=dates[hi - 1]))
        lo = hi
    return out


def run(cfg: dict) -> dict:
    ac = cfg["ai_check"]
    cutoff, after, pct = str(ac["cutoff"]), str(ac["sustained_after"]), float(ac.get("percentile", 95))
    min_hits = int(ac.get("min_hits", 2))
    db = store.connect(store.db_path(cfg))
    posts = store.kept_posts(db)
    if not posts:
        raise SystemExit("no corpus: run `quill ingest` first")
    dates = [p["date"] or "0000" for p in posts]
    base = np.array([d < cutoff for d in dates])

    lex_dir = Path(cfg["paths"]["lexicon"])
    baseline = L.read_baseline(cfg["paths"].get("baseline"), before_year=int(cutoff[:4]))
    v0 = L.build_v0([p["text"] for p, b in zip(posts, base) if b], baseline, out=lex_dir / "v0.json")
    lex = L.Lexicon.load(lex_dir / "v0.json")

    scores = [lex.score(p["text"]) for p in posts]
    fams = ("vocabulary", "structure")
    thr = {f: float(np.percentile([s["rates"][f] for s, b in zip(scores, base) if b], pct)) for f in fams}

    X = np.vstack([features(p["text"]) for p in posts])
    d = distances(X, base)
    shifts = sustained_shifts(d, base, dates, after=after, pct=pct)
    in_shift = {i: s for s in shifts for i in range(s["start"], s["end"])}

    flagged = {}
    for i, (p, s) in enumerate(zip(posts, scores)):
        if base[i]:
            continue
        flags, detail = [], dict(words=s["words"], date=p["date"], title=p["title"], url=p["url"],
                                 rates={f: round(s["rates"][f], 2) for f in fams},
                                 thresholds={f: round(thr[f], 2) for f in fams}, style_distance=round(float(d[i]), 3))
        for f in fams:
            if s["rates"][f] > thr[f] and s["hits"][f] >= min_hits:
                flags.append(f"lexicon_{f}")
        if s["hits"]["artifacts"]:
            flags.append("artifacts")
        if flags:
            detail["top_items"] = {k: v for k, v in s["items"].items()
                                   if k not in lex.whitelist and k not in lex.rate_only}
        if i in in_shift:
            flags.append("changepoint")
            detail["shift"] = {k: in_shift[i][k] for k in ("from_date", "to_date", "mean", "threshold")}
        blocks = [p["text"]] + [r["text"] for r in db.execute(
            "SELECT text FROM dropped_blocks WHERE post_file = ?", (p["file"],))]
        mentions = [re.sub(r"\s+", " ", t[max(0, m.start() - 80):m.end() + 80]).strip()
                    for t in blocks for m in LLM_MENTION.finditer(t)]
        if mentions:
            flags.append("llm_mention")
            detail["mentions"] = [f"…{x}…" for x in mentions[:5]]
        links = [h for h in json.loads(p["hrefs"] or "[]") if LLM_LINK.search(h)]
        if links:
            flags.append("llm_link")
            detail["links"] = links[:5]
        if flags:
            flagged[p["file"]] = (flags, detail)

    with db:
        old = {r["post_file"]: r for r in db.execute("SELECT * FROM ai_flags")}
        for f in old:
            if f not in flagged:
                db.execute("DELETE FROM ai_flags WHERE post_file = ?", (f,))
        for f, (flags, detail) in flagged.items():
            if f in old and json.loads(old[f]["flags"]) == flags:
                db.execute("UPDATE ai_flags SET detail = ? WHERE post_file = ?", (json.dumps(detail), f))
            else:       # new flag, or the reasons changed: the earlier decision no longer covers it
                db.execute("INSERT OR REPLACE INTO ai_flags (post_file, flags, detail, decision) VALUES (?,?,?,?)",
                           (f, json.dumps(flags), json.dumps(detail), "pending"))
    summary = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "cutoff": cutoff, "sustained_after": after, "percentile": pct,
        "baseline_posts": int(base.sum()), "checked_posts": int((~base).sum()),
        "thresholds_per_1k": {f: round(thr[f], 2) for f in fams},
        "baseline_median_per_1k": {f: round(float(np.median([s["rates"][f] for s, b in zip(scores, base) if b])), 2)
                                   for f in fams},
        "checked_median_per_1k": {f: round(float(np.median([s["rates"][f] for s, b in zip(scores, base) if not b])), 2)
                                  for f in fams},
        "style_distance": {"baseline_mean": round(float(d[base].mean()), 3),
                           "checked_mean": round(float(d[~base].mean()), 3)},
        "shifts": shifts,
        "flagged": len(flagged),
        "whitelisted_items": len(v0["whitelist"]),
        "lexicon_items": len(v0["items"]),
        "pattern_baseline_words": v0["baseline_words"],
        "author_rates": v0["author_rates"],
        "lexicon": str(lex_dir / "v0.json"),
    }
    store.set_meta(db, "ai_check", summary)
    out = Path(cfg["paths"]["corpus"]) / "ai_flags.md"
    out.write_text(render(db, summary, v0))
    db.close()
    summary["_out"] = str(out)
    return summary


def render(db, s: dict, v0: dict) -> str:
    rows = db.execute("SELECT a.*, p.slug FROM ai_flags a JOIN posts p ON p.file = a.post_file "
                      "ORDER BY p.date").fetchall()
    Ls = [f"# AI-text flags for review ({s['generated']})", "",
          f"Posts before {s['cutoff']} are the baseline ({s['baseline_posts']} posts). "
          f"{s['checked_posts']} later posts were checked; {s['flagged']} carry a flag. Nothing is dropped "
          "until you decide: `quill flags <slug> keep|drop`.", "",
          f"- Lexicon thresholds (95th percentile of baseline posts, hits per 1k words): "
          f"{s['thresholds_per_1k']}. Baseline median {s['baseline_median_per_1k']}; "
          f"checked median {s['checked_median_per_1k']}.",
          f"- Style distance from the pre-cutoff centroid: baseline mean {s['style_distance']['baseline_mean']}, "
          f"checked mean {s['style_distance']['checked_mean']}. Sustained shifts after {s['sustained_after']}: "
          f"{len(s['shifts'])}.",
          f"- Lexicon v0: {s['lexicon_items']} items, {s['whitelisted_items']} whitelisted as the author's own "
          f"habits. Pattern baseline: {s['pattern_baseline_words']:,} words of pre-cutoff human essays.",
          "- M10 (detector) does not exist yet. Review these again with M10 in Phase 2.", "",
          "| Post | Date | Words | Flags | Vocab /1k | Struct /1k | Distance | Decision |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        d = json.loads(r["detail"])
        Ls.append(f"| {r['slug']} | {d['date']} | {d['words']} | {', '.join(json.loads(r['flags']))} | "
                  f"{d['rates']['vocabulary']} | {d['rates']['structure']} | {d['style_distance']} | {r['decision']} |")
    Ls.append("")
    for r in rows:
        d = json.loads(r["detail"])
        Ls += [f"## {r['slug']}", "", f"{d['title']} ({d['date']}). {d['url']}", ""]
        if d.get("top_items"):
            Ls.append("- Hits: " + ", ".join(f"{k} ×{v}" for k, v in list(d["top_items"].items())[:15]))
        if d.get("shift"):
            sh = d["shift"]
            Ls.append(f"- In a shifted run {sh['from_date']} to {sh['to_date']}: mean distance {sh['mean']:.3f} "
                      f"vs threshold {sh['threshold']:.3f}")
        if d.get("links"):
            Ls.append("- Links that carry an LLM referrer or point at a chatbot: " + "; ".join(d["links"]))
        if d.get("mentions"):
            Ls.append("- Mentions: " + "; ".join(d["mentions"]))
        Ls.append("")
    a = v0["author_rates"]
    Ls += ["## The author's own tell rates (pre-cutoff text; whitelist reference)", "",
           "| Habit | Rate |", "|---|---|"] + [f"| {k} | {v} |" for k, v in a.items()]
    wl = [k for k in v0["whitelist"]]
    Ls += ["", "## Whitelisted items", "", ", ".join(wl), ""]
    return "\n".join(Ls) + "\n"


def decide(cfg: dict, slug: str, decision: str, note: str = "") -> bool:
    if decision not in ("keep", "drop", "pending"):
        raise ValueError(decision)
    db = store.connect(store.db_path(cfg))
    with db:
        cur = db.execute(
            "UPDATE ai_flags SET decision = ?, note = ?, decided = ? WHERE post_file IN "
            "(SELECT file FROM posts WHERE slug = ?)", (decision, note, time.strftime("%Y-%m-%d"), slug))
    db.close()
    return cur.rowcount > 0


def list_flags(cfg: dict) -> list[dict]:
    db = store.connect(store.db_path(cfg))
    rows = [dict(slug=r["slug"], date=r["date"], flags=json.loads(r["flags"]), decision=r["decision"],
                 note=r["note"]) for r in db.execute(
        "SELECT a.*, p.slug, p.date FROM ai_flags a JOIN posts p ON p.file = a.post_file ORDER BY p.date")]
    db.close()
    return rows
