"""Cut a post into 150-800-word chunks on paragraph boundaries.

Chunk sizes rotate through three targets so every length bucket gets training text.
Word counts ignore list markers, so they stay comparable with the corpus totals.
"""
from __future__ import annotations

import re
import zlib

from ..ingest.textlib import split_sentences

BUCKETS = [(150, 300), (300, 500), (500, 800)]
TARGETS = [400, 225, 650]


def bucket(words: int) -> str:
    if words < BUCKETS[0][0]:
        return "under-150"
    for lo, hi in BUCKETS[:-1]:
        if words < hi:
            return f"{lo}-{hi}"
    return f"{BUCKETS[-1][0]}-{BUCKETS[-1][1]}"


def render(b: dict) -> str:
    """Block -> text line. Ordered items keep their number; bullets get a dash."""
    t = b["text"]
    if b.get("kind") == "oli" and b.get("n") and not re.match(r"^\d+[.)]\s", t):
        return f"{b['n']}. {t}"
    if b.get("kind") == "li":
        return f"- {t}"
    return t


def _split_long(b: dict, hard: int, piece: int) -> list[dict]:
    """Split one over-long paragraph at sentence boundaries into pieces of about `piece` words."""
    if len(b["text"].split()) <= hard:
        return [b]
    out, cur, cw = [], [], 0
    for s in split_sentences(b["text"]):
        sw = len(s.split())
        if cur and cw + sw > piece:
            out.append(" ".join(cur))
            cur, cw = [], 0
        cur.append(s)
        cw += sw
    if cur:
        out.append(" ".join(cur))
    last = len(out) - 1
    return [dict(b, text=t, split=True, kind=b["kind"] if i == 0 else "p",
                 gaps=b.get("gaps", set()) if i == last else set()) for i, t in enumerate(out)]


def _with_markers(i: int, paras: list[dict], markers: dict | None) -> str:
    t = render(paras[i])
    for kind in ("quote", "media"):
        if markers and markers.get(kind) and kind in paras[i].get("gaps", ()):
            t += "\n\n" + markers[kind]
    return t


def chunk_post(blocks: list[dict], key: str = "", lo: int = 150, hi: int = 800,
               targets: list[int] | None = None, markers: dict | None = None) -> list[dict]:
    """Return chunks: text, words, bucket, flags (list), n_paras.

    text is the author's words only. markers, e.g. {"quote": "<QUOTE>", "media": "<IMAGE>"}, adds
    text_marked: the same text with a line where a block quote or an image was removed.
    """
    targets = targets or TARGETS
    paras = [x for b in blocks for x in _split_long(b, hard=min(500, hi), piece=350)]
    w = [len(p["text"].split()) for p in paras]
    start = zlib.crc32(key.encode()) % len(targets)

    groups: list[list[int]] = []
    cur: list[int] = []
    cw = 0
    for i in range(len(paras)):
        target = targets[(start + len(groups)) % len(targets)]
        if cur and cw >= lo and cw + w[i] > target:
            leadin = paras[cur[-1]]["text"].rstrip().endswith(":")
            if leadin and cw + w[i] <= hi:
                pass                                   # keep "A few examples:" with what it introduces
            elif leadin and cw - w[cur[-1]] >= lo:
                carry = cur.pop()
                groups.append(cur)
                cur, cw = [carry], w[carry]
            else:
                groups.append(cur)
                cur, cw = [], 0
        elif cur and cw + w[i] > hi:
            groups.append(cur)
            cur, cw = [], 0
        cur.append(i)
        cw += w[i]
    if cur:
        groups.append(cur)

    # a short tail joins the chunk before it, or the two are re-cut evenly
    if len(groups) > 1 and sum(w[i] for i in groups[-1]) < lo:
        tail = groups.pop()
        both = groups.pop() + tail
        total = sum(w[i] for i in both)
        if total <= hi:
            groups.append(both)
        else:
            acc, cut = 0, 1
            for k, i in enumerate(both[:-1]):
                acc += w[i]
                if acc >= total / 2:
                    cut = k + 1
                    break
            groups += [both[:cut], both[cut:]]

    out = []
    for g in groups:
        words = sum(w[i] for i in g)
        flags = []
        if any(paras[i]["kind"] in ("li", "oli") or re.match(r"^\d+[.)]\s", paras[i]["text"]) for i in g):
            flags.append("list")
        if any(paras[i].get("split") for i in g):
            flags.append("split_para")
        if words < lo:
            flags.append("short")
        if words > hi:
            flags.append("long")
        for kind in ("quote", "media"):
            if any(kind in paras[i].get("gaps", ()) for i in g):
                flags.append(f"{kind}_gap")
        if any(paras[i]["text"].rstrip().endswith(":") and paras[i].get("gaps") for i in g):
            flags.append("dangling_leadin")
        if any("<CODE>" in paras[i]["text"] for i in g):
            flags.append("code")
        k = dict(text="\n\n".join(render(paras[i]) for i in g), words=words, bucket=bucket(words),
                 flags=flags, n_paras=len(g))
        if markers:
            k["text_marked"] = "\n\n".join(_with_markers(i, paras, markers) for i in g)
        out.append(k)
    return out
