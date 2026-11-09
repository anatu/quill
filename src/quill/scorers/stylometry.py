"""M6: tic profile and Burrows' Delta.

The tic profile compares a pool of text (>= 2,000 words) with the spread of same-size pools
of the author's own text, feature by feature. It catches caricature: short sentences, no em
dashes, too much "you". Delta is a diagnostic only; it passed a caricature in the 2026-11-08 pass.
"""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

import numpy as np

from ..ingest import textlib as T

FEATURES = ("sent_len_mean", "sent_len_sd", "words_per_para", "one_sent_para_share", "sp_per_1k", "emdash_per_1k",
            "colon_per_1k", "semicolon_per_1k", "paren_per_1k", "question_per_100s", "mattr500")
POOL_WORDS = 2000


def pools(texts: list[str], words: int = POOL_WORDS, draws: int | None = None, seed: int = 0) -> list[list[str]]:
    """Pools of at least `words` words. draws=None cuts the texts once, in shuffled order;
    otherwise each draw samples texts without replacement."""
    rng = random.Random(seed)
    wc = [len(t.split()) for t in texts]
    if sum(wc) < words:
        return [list(texts)] if texts else []
    out = []
    if draws is None:
        idx = list(range(len(texts)))
        rng.shuffle(idx)
        cur, cw = [], 0
        for i in idx:
            cur.append(texts[i])
            cw += wc[i]
            if cw >= words:
                out.append(cur)
                cur, cw = [], 0
        if cur and out:
            out[-1] += cur
        return out
    for _ in range(draws):
        idx = list(range(len(texts)))
        rng.shuffle(idx)
        cur, cw = [], 0
        for i in idx:
            cur.append(texts[i])
            cw += wc[i]
            if cw >= words:
                break
        out.append(cur)
    return out


def features(pool: list[str]) -> np.ndarray:
    s = T.stylometrics([t.split("\n\n") for t in pool])
    return np.array([s[f] for f in FEATURES], dtype=float)


def topic_pools(texts: list[str], groups: list, words: int = POOL_WORDS, draws: int = 300, seed: int = 0):
    """Pools drawn inside one topic group at a time. A held-out topic differs from the average
    of all topics ("you" doubles in advice essays), so the reference spread must include that."""
    rng = random.Random(seed)
    by: dict = {}
    for t, g in zip(texts, groups):
        by.setdefault(g, []).append(t)
    big = {g: v for g, v in by.items() if sum(len(t.split()) for t in v) >= words}
    if not big:
        return pools(texts, words=words, draws=draws, seed=seed)
    keys = sorted(big, key=str)
    weights = [sum(len(t.split()) for t in big[g]) for g in keys]
    out = []
    for _ in range(draws):
        g = rng.choices(keys, weights=weights)[0]
        out += pools(big[g], words=words, draws=1, seed=rng.randrange(10**9))
    return out


class TicProfile:
    def fit(self, texts: list[str], groups: list | None = None, draws: int = 300, seed: int = 0) -> "TicProfile":
        ps = topic_pools(texts, groups, draws=draws, seed=seed) if groups else pools(texts, draws=draws, seed=seed)
        F = np.vstack([features(p) for p in ps])
        self.mu, self.sd = F.mean(0), F.std(0, ddof=1)
        self.sd[self.sd == 0] = 1e-9
        return self

    def score(self, texts: list[str], seed: int = 1) -> dict:
        """Per feature: pooled value, pooled z, and the share of 2,000-word pools with |z| > 2."""
        ps = pools(texts, seed=seed)
        if not ps:
            return dict(n_pools=0, features={})
        Z = np.vstack([(features(p) - self.mu) / self.sd for p in ps])
        whole = features(texts)
        out = {}
        for j, f in enumerate(FEATURES):
            out[f] = dict(value=round(float(whole[j]), 3), reference=round(float(self.mu[j]), 3),
                          z=round(float(Z[:, j].mean()), 2), share_abs_z_gt_2=round(float((np.abs(Z[:, j]) > 2).mean()), 2))
        return dict(n_pools=len(ps), features=out, max_abs_z=round(float(np.abs(Z.mean(0)).max()), 2))


class Delta:
    """Burrows' Delta on the 150 most frequent words of an author-balanced basis."""

    def __init__(self, basis: dict):
        self.mfw = basis["mfw"]
        self.mu, self.sd = np.array(basis["mu"]), np.array(basis["sd"])

    @classmethod
    def load(cls, path: Path) -> "Delta":
        return cls(json.loads(Path(path).read_text()))

    @classmethod
    def build(cls, by_author: dict[str, list[str]], n: int = 150) -> "Delta":
        rel = {}
        for a, texts in by_author.items():
            c = Counter(w for t in texts for w in T.words(t))
            tot = sum(c.values()) or 1
            rel[a] = {w: v / tot for w, v in c.items()}
        vocab = Counter()
        for a in rel:
            for w, v in rel[a].items():
                vocab[w] += v / len(rel)
        mfw = [w for w, _ in vocab.most_common(n)]
        M = np.array([[rel[a].get(w, 0.0) for w in mfw] for a in rel])
        sd = M.std(0, ddof=1)
        sd[sd == 0] = 1e-9
        return cls(dict(mfw=mfw, mu=M.mean(0).tolist(), sd=sd.tolist()))

    def z(self, texts: list[str]) -> np.ndarray:
        f, _ = T.rel_freqs(texts, self.mfw)
        return (np.array(f) - self.mu) / self.sd

    def fit(self, texts: list[str]) -> "Delta":
        self.ref = self.z(texts)
        return self

    def score(self, texts: list[str], words: int = 4000, draws: int = 30, seed: int = 1) -> dict:
        ps = pools(texts, words=words, draws=draws, seed=seed)
        if not ps:
            return dict(delta=None)
        v = [float(np.mean(np.abs(self.z(p) - self.ref))) for p in ps]
        return dict(delta=round(float(np.mean(v)), 3), sd=round(float(np.std(v)), 3),
                    words=min(words, sum(len(t.split()) for t in texts)))
