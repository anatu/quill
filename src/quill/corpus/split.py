"""Frozen topic-disjoint splits (plan.md Phase 2).

Posts are embedded with a content encoder and clustered. Whole clusters are held out
for test and dev, so style metrics cannot ride on topic. A twin group moves as one unit.

The frozen thing is the post -> split map (posts.json and its hash). Chunk id lists are
derived from it and the current corpus, so a cleaning change cannot move a post between
splits. A post that is not in the map has no split.
"""
from __future__ import annotations

import hashlib
import json
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

from . import store

SPLITS = ("train", "dev", "test")


def split_dir(cfg: dict) -> Path:
    return Path(cfg["paths"]["splits"]) / cfg["split"]["version"]


def assignment_hash(posts: dict[str, str]) -> str:
    return hashlib.sha256("\n".join(f"{k}\t{v}" for k, v in sorted(posts.items())).encode()).hexdigest()


def pick_clusters(words: dict[int, int], target: float, total: int, exclude: set[int] = frozenset(),
                  max_clusters: int = 4) -> tuple[int, ...]:
    """Clusters whose words sum closest to target x total. Ties go to more clusters, then lower ids."""
    ids = sorted(c for c in words if c not in exclude)
    best = None
    for r in range(1, min(max_clusters, len(ids)) + 1):
        for combo in combinations(ids, r):
            gap = abs(sum(words[c] for c in combo) - target * total)
            key = (round(gap), -r, combo)
            if best is None or key < best[0]:
                best = (key, combo)
    return best[1]


def cluster_posts(rows: list, cfg: dict) -> np.ndarray:
    """Cluster label per post. A post vector is the word-weighted mean of its chunk embeddings."""
    from sklearn.cluster import KMeans

    from ..scorers import embed

    db = store.connect(store.db_path(cfg))
    vecs = []
    for p in rows:
        ch = db.execute("SELECT text, words FROM chunks WHERE post_file = ? ORDER BY seq", (p["file"],)).fetchall()
        E = embed.encode([c["text"] for c in ch], "content", Path(cfg["paths"]["eval"]) / "cache")
        w = np.array([c["words"] for c in ch], dtype=float)
        v = (E * w[:, None]).sum(0)
        vecs.append(v / np.linalg.norm(v))
    db.close()
    s = cfg["split"]
    return KMeans(n_clusters=s["clusters"], n_init=10, random_state=s["seed"]).fit_predict(np.vstack(vecs))


def assign(rows: list[dict], labels: list[int], test_share: float, dev_share: float) -> tuple[dict, dict]:
    """rows: file, words, twin_group. Returns (file -> split, info)."""
    units: dict[str, list[int]] = defaultdict(list)
    for i, p in enumerate(rows):
        units[p["twin_group"] or p["file"]].append(i)
    unit_cluster, straddle = {}, []
    for u, idx in units.items():
        w = Counter()
        for i in idx:
            w[int(labels[i])] += rows[i]["words"]
        unit_cluster[u] = max(sorted(w), key=lambda c: w[c])
        if len(w) > 1:
            straddle.append(u)
    cw: Counter = Counter()
    for u, idx in units.items():
        cw[unit_cluster[u]] += sum(rows[i]["words"] for i in idx)
    total = sum(cw.values())
    test = pick_clusters(cw, test_share, total)
    dev = pick_clusters(cw, dev_share, total, exclude=set(test))
    posts = {}
    for u, idx in units.items():
        s = "test" if unit_cluster[u] in test else "dev" if unit_cluster[u] in dev else "train"
        for i in idx:
            posts[rows[i]["file"]] = s
    info = dict(cluster_words={int(c): int(n) for c, n in sorted(cw.items())}, test_clusters=list(test),
                dev_clusters=list(dev), straddling_twin_groups=sorted(straddle),
                post_cluster={rows[i]["file"]: int(labels[i]) for i in range(len(rows))})
    return posts, info


def make(cfg: dict, force: bool = False) -> dict:
    d = split_dir(cfg)
    if (d / "manifest.json").exists() and not force:
        return refresh(cfg)
    db = store.connect(store.db_path(cfg))
    rows = [dict(r) for r in store.kept_posts(db)]
    db.close()
    labels = cluster_posts(rows, cfg)
    s = cfg["split"]
    posts, info = assign(rows, list(labels), s["test_share"], s["dev_share"])
    d.mkdir(parents=True, exist_ok=True)
    (d / "posts.json").write_text(json.dumps(posts, indent=0, sort_keys=True))
    (d / "clusters.json").write_text(json.dumps(info, indent=1))
    manifest = dict(version=s["version"], frozen=time.strftime("%Y-%m-%d"), hash=assignment_hash(posts),
                    encoder="BAAI/bge-large-en-v1.5", clusters=s["clusters"], seed=s["seed"],
                    test_clusters=info["test_clusters"], dev_clusters=info["dev_clusters"])
    (d / "manifest.json").write_text(json.dumps(manifest, indent=1))
    return refresh(cfg, created=True)


def load(cfg: dict) -> dict[str, str]:
    """Chunk id -> split, for usable chunks of posts in the frozen map. Verifies the hash."""
    d = split_dir(cfg)
    manifest = json.loads((d / "manifest.json").read_text())
    posts = json.loads((d / "posts.json").read_text())
    if assignment_hash(posts) != manifest["hash"]:
        raise SystemExit(f"split {manifest['version']}: posts.json does not match the frozen hash")
    db = store.connect(store.db_path(cfg))
    out = {r["id"]: posts[r["post_file"]] for r in db.execute("SELECT id, post_file FROM usable_chunks")
           if r["post_file"] in posts}
    db.close()
    return out


def refresh(cfg: dict, created: bool = False) -> dict:
    """Rewrite the .ids files from the frozen map and the current corpus; return a summary."""
    d = split_dir(cfg)
    ids = load(cfg)
    manifest = json.loads((d / "manifest.json").read_text())
    posts = json.loads((d / "posts.json").read_text())
    db = store.connect(store.db_path(cfg))
    words = {r["id"]: r["words"] for r in db.execute("SELECT id, words FROM usable_chunks")}
    current = {r["file"] for r in store.kept_posts(db)}
    post_words = {r["file"]: r["words"] for r in store.kept_posts(db)}
    db.close()
    for s in SPLITS:
        (d / f"{s}.ids").write_text("\n".join(sorted(i for i, v in ids.items() if v == s)) + "\n")
    total = sum(words[i] for i in ids) or 1
    return dict(created=created, dir=str(d), hash=manifest["hash"], frozen=manifest["frozen"],
                chunks={s: sum(1 for v in ids.values() if v == s) for s in SPLITS},
                words={s: sum(words[i] for i, v in ids.items() if v == s) for s in SPLITS},
                share={s: round(sum(words[i] for i, v in ids.items() if v == s) / total, 4) for s in SPLITS},
                posts={s: sum(1 for f, v in posts.items() if v == s and f in current) for s in SPLITS},
                unassigned_posts=sorted(current - set(posts)), missing_posts=sorted(set(posts) - current),
                test_clusters=manifest["test_clusters"], dev_clusters=manifest["dev_clusters"],
                post_words=sum(post_words.values()))
