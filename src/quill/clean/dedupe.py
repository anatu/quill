"""Keep one copy of each repeated paragraph (MinHash over word 5-gram shingles).

Reposts and book excerpts repeat whole paragraphs. Training on both copies would count
the passage twice, so later copies go. Short paragraphs are left alone: a repeated
one-liner ("Same as ever.") is a habit of voice, not a duplicate passage.
"""
from __future__ import annotations

import re

from datasketch import MinHash, MinHashLSH

TOKEN = re.compile(r"[a-z0-9']+")


def _shingles(text: str, n: int) -> set[str]:
    w = TOKEN.findall(text.lower().replace("’", "'"))
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def find_duplicates(paras: list[str], n: int = 5, jaccard: float = 0.85, min_words: int = 20,
                    num_perm: int = 128) -> dict[int, int]:
    """paras are in keep-priority order (earliest first). Returns {dup index: kept index}."""
    lsh = MinHashLSH(threshold=max(0.5, jaccard - 0.15), num_perm=num_perm)   # loose net, exact check below
    sets: dict[int, set[str]] = {}
    dups: dict[int, int] = {}
    for i, t in enumerate(paras):
        if len(t.split()) < min_words:
            continue
        s = _shingles(t, n)
        if not s:
            continue
        m = MinHash(num_perm=num_perm)
        for x in s:
            m.update(x.encode())
        best = None
        for j in lsh.query(m):
            o = sets[j]
            jac = len(s & o) / len(s | o)
            if jac >= jaccard and (best is None or j < best):
                best = j
        if best is not None:
            dups[i] = best
        else:
            sets[i] = s
            lsh.insert(i, m)
    return dups


def dedupe_posts(posts: list[dict], **kw) -> int:
    """Drop later copies of repeated paragraphs across posts (ordered by date). Edits in place.

    Each post needs date, file, blocks, dropped. Returns the number of paragraphs dropped.
    """
    order = sorted(posts, key=lambda p: (p.get("date") or "9999", p["file"]))
    flat = [(p, i) for p in order for i in range(len(p["blocks"]))]
    dups = find_duplicates([p["blocks"][i]["text"] for p, i in flat], **kw)
    kill: dict[int, set[int]] = {}
    for d, k in dups.items():
        p, i = flat[d]
        kill.setdefault(id(p), set()).add(i)
        b = p["blocks"][i]
        p["dropped"].append(dict(text=b["text"], reason="duplicate_paragraph", words=len(b["text"].split()),
                                 kept_in=flat[k][0]["file"]))
    for p in order:
        gone = kill.get(id(p))
        if gone:
            p["blocks"] = [b for i, b in enumerate(p["blocks"]) if i not in gone]
    return len(dups)
