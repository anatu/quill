"""Strip Collab Fund furniture and other people's words from parsed posts.

Input blocks come from ingest.collabfund.read_page. Every dropped block gets a reason, so
the cleaning report can show what went and why.
"""
from __future__ import annotations

import re
from collections import Counter

FOOTNOTE = re.compile(r"\[\d+\]|\[[a-z]\]")
RELATED_MARK = re.compile(r"^(more on this topic|related (posts|reading)|further reading|you may also like)\s*:?\s*$",
                          re.I)
# A promo is a short line that sells; a mention inside a sentence ("...in my book, X.") is not.
PROMO = re.compile(
    r"^(check out|order|pre-?order|buy|get|grab)\s+(my|the|a copy of my)\s+(new\s+)?book\b"
    r"|^my (new |latest )?book,?.{0,80}\b(is (now |finally )?(out|available|here)|comes out|is out now)\b"
    r"|^for more, check out my book\b"
    r"|^\(?click here\b"
    r"|^\(?pdf version here\)?\.?$"
    r"|^(subscribe|sign up)\b.{0,60}$"
    r"|^copy link$", re.I)
BYLINE = re.compile(r"^(by\s+)?morgan housel\s*$|^@morganhousel\s*$", re.I)
CAPTION = re.compile(r"^(source|sources|chart|image|photo|credit)s?\s*:", re.I)
ATTRIBUTION = re.compile(r"^\s*[-–—―]{1,2}\s*\S")          # "– Voltaire" under a quote
SEPARATOR = re.compile(r"^[\s*\-–—_~•·#.]+$")            # "***", "—"; a bare "80%?" is text and stays
MAX_QUOTE_PARAS = 8
OPEN_Q, CLOSE_Q = "“\"", "”\""
QUOTE_TAIL = re.compile(r"[”\"]\s*(?:[-–—―]{1,2}\s*[^“”\"]{2,80})?$")


def is_pure_quote(text: str, min_words: int = 8) -> bool:
    """True when the whole paragraph is one quotation, optionally followed by '- Name'.

    Dialogue with narration ("“Sell,” he said. “Now.”") has more than one quote span and stays.
    """
    t = text.strip()
    if not t or t[0] not in OPEN_Q or len(t.split()) < min_words:
        return False
    opens = sum(t.count(c) for c in "“")
    closes = sum(t.count(c) for c in "”")
    straight = t.count('"')
    if straight and not (opens or closes):
        return straight == 2 and bool(QUOTE_TAIL.search(t))
    return opens == 1 and closes == 1 and bool(QUOTE_TAIL.search(t))


def _linky(b: dict, share: float = 0.6, words: int = 40) -> bool:
    return b["kind"] != "media" and b["link_share"] > share and len(b["text"].split()) < words


def clean_post(blocks: list[dict]) -> tuple[list[dict], list[dict]]:
    """Return (kept, dropped). Kept blocks: text, kind, n, and gaps when a quote or an image
    was removed right after the block. Dropped blocks carry a reason."""
    kept, dropped = [], []

    def drop(b, reason):
        dropped.append(dict(text=b["text"], reason=reason, words=len(b["text"].split())))
        if reason in ("blockquote", "inline_quote"):
            gap("quote")

    def gap(kind):
        if kept:
            kept[-1].setdefault("gaps", set()).add(kind)

    # 1. related-post list: the marker and the link-only run that follows it
    related = set()
    for i, b in enumerate(blocks):
        if RELATED_MARK.match(b["text"]):
            related.add(i)
            j = i + 1
            while j < len(blocks) and _linky(blocks[j]):
                related.add(j)
                j += 1
    # 2. trailing run of link-only lines at the end of the post
    j = len(blocks) - 1
    def tail_link(b):
        return b["kind"] == "media" or (b["link_share"] >= 0.9 and len(b["text"].split()) < 20)

    while j >= 0 and (j in related or tail_link(blocks[j])):
        related.add(j)
        j -= 1

    # 3. multi-paragraph quotations: an opening mark with no close runs until the paragraph that closes it
    in_quote = set()
    for i, b in enumerate(blocks):
        t = b["text"].strip()
        if i in in_quote or b["bq"] or not t or t[0] != "“" or t.count("“") != 1 or "”" in t:
            continue
        for j in range(i + 1, min(i + 1 + MAX_QUOTE_PARAS, len(blocks))):
            u = blocks[j]["text"].strip()
            if u.count("”") == 1 and u.count("“") <= (1 if u.startswith("“") else 0) and QUOTE_TAIL.search(u):
                in_quote.update(range(i, j + 1))
                break
            if not (u.startswith("“") and "”" not in u):
                break                    # not a continuation paragraph: leave the run alone

    prev_quote = False
    for i, b in enumerate(blocks):
        text = re.sub(r"\s+", " ", FOOTNOTE.sub("", b["text"])).strip()
        b = dict(b, text=text)
        if b["kind"] == "media":
            if not b["bq"]:
                gap("media")
            continue
        was_quote, prev_quote = prev_quote, False
        if not text:
            continue
        if b["bq"]:
            drop(b, "blockquote")
            prev_quote = True
        elif i in related:
            drop(b, "related_links")
        elif SEPARATOR.match(text):
            drop(b, "separator")
        elif was_quote and ATTRIBUTION.match(text) and len(text.split()) < 20:
            drop(b, "quote_attribution")
        elif i in in_quote or is_pure_quote(text):
            drop(b, "inline_quote")
            prev_quote = True
        elif BYLINE.match(text):
            drop(b, "byline")
        elif len(text.split()) < 25 and PROMO.search(text):
            drop(b, "promo")
        elif CAPTION.match(text) and len(text.split()) < 40:
            drop(b, "caption")
        else:
            kept.append(dict(text=text, kind=b["kind"], n=b.get("n")))
    return kept, dropped


def _norm(t: str) -> str:
    return re.sub(r"\W+", " ", t.lower()).strip()


def drop_repeated(posts: list[dict], min_posts: int = 3, share: float = 0.10) -> list[tuple[str, int]]:
    """Drop paragraphs that repeat in >= max(min_posts, share of posts) posts. Edits posts in place.

    Each post needs `blocks` (kept) and `dropped`. Returns [(paragraph, post count)].
    """
    cnt = Counter()
    for p in posts:
        for t in {_norm(b["text"]) for b in p["blocks"]}:
            cnt[t] += 1
    thr = max(min_posts, int(share * len(posts)))
    rep = {t: c for t, c in cnt.items() if c >= thr and t}
    for p in posts:
        keep = []
        for b in p["blocks"]:
            if _norm(b["text"]) in rep:
                p["dropped"].append(dict(text=b["text"], reason="repeated_boilerplate", words=len(b["text"].split())))
            else:
                keep.append(b)
        p["blocks"] = keep
    return sorted(rep.items(), key=lambda x: -x[1])
