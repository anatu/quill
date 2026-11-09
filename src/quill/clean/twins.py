"""Find near-duplicate posts (reposts, book excerpts) by shared word n-grams.

Twins must stay on the same side of every train/dev/test split.
"""
from __future__ import annotations

import re
from collections import defaultdict

TOKEN = re.compile(r"[a-z0-9']+")


def shingles(text: str, n: int) -> list[str]:
    w = TOKEN.findall(text.lower())
    return [" ".join(w[i:i + n]) for i in range(len(w) - n + 1)]


def find_twins(docs: dict[str, str], n: int = 10, share: float = 0.30) -> dict:
    """docs: id -> text.

    Returns:
      shared_share: share of all n-gram tokens that also occur in another doc
      twin_posts:   ids whose own n-grams are > `share` shared with other docs
      groups:       connected components of doc pairs where one doc shares > `share` with the other
    """
    sh = {d: shingles(t, n) for d, t in docs.items()}
    owners = defaultdict(set)
    for d, g in sh.items():
        for x in g:
            owners[x].add(d)

    total = shared = 0
    twin_posts = []
    pair_counts: dict[tuple[str, str], int] = defaultdict(int)
    for d, g in sh.items():
        s = 0
        for x in g:
            o = owners[x]
            if len(o) > 1:
                s += 1
                for other in o:
                    if other != d:
                        pair_counts[(d, other)] += 1
        total += len(g)
        shared += s
        if g and s / len(g) > share:
            twin_posts.append(d)

    parent = {d: d for d in docs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (a, b), c in pair_counts.items():
        if sh[a] and c / len(sh[a]) > share:
            parent[find(a)] = find(b)
    comps = defaultdict(list)
    for d in docs:
        comps[find(d)].append(d)
    groups = sorted((sorted(v) for v in comps.values() if len(v) > 1), key=len, reverse=True)
    # links: for each doc, the docs it shares n-grams with and the share of its own n-grams involved
    links: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for (a, b), c in pair_counts.items():
        links[a].append((b, round(c / len(sh[a]), 4)))
    links = {d: sorted(v, key=lambda x: -x[1]) for d, v in links.items()}
    return dict(shared_share=shared / total if total else 0.0, twin_posts=sorted(twin_posts), groups=groups,
                links=links)


def split_groups(tw: dict, min_link: float = 0.05) -> list[list[str]]:
    """Groups that must share a train/dev/test split.

    Start from the pairwise groups. A twin post that sits in no group (it borrows from several
    posts, none above the pair threshold) joins every source that supplies at least `min_link`
    of its n-grams, so it never lands across a split from the text it repeats.
    """
    parent: dict[str, str] = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for g in tw["groups"]:
        for d in g[1:]:
            parent[find(d)] = find(g[0])
    grouped = {d for g in tw["groups"] for d in g}
    for d in tw["twin_posts"]:
        if d in grouped:
            continue
        for other, s in tw["links"].get(d, []):
            if s >= min_link:
                parent[find(d)] = find(other)
    comps = defaultdict(list)
    for d in list(parent):
        comps[find(d)].append(d)
    return sorted((sorted(v) for v in comps.values() if len(v) > 1), key=lambda g: (-len(g), g))
