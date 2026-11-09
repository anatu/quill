"""M9 memorization and M8 signature phrases.

M9: the longest run of words an output shares verbatim with the author's corpus. Runs that
also appear in the input are exempt: a restyle may keep what the draft already said.
M8: how often an output uses the author's most distinctive n-grams, against his own rate.
"""
from __future__ import annotations

import math
import re
from collections import Counter

TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.lower().replace("’", "'"))


class Memo:
    def __init__(self, n: int = 8):
        self.n = n
        self.grams: set[int] = set()

    def add(self, text: str) -> None:
        t = tokens(text)
        self.grams.update(hash(tuple(t[i:i + self.n])) for i in range(len(t) - self.n + 1))

    def longest(self, output: str, input_text: str = "") -> dict:
        """Longest shared span in words (0 if under n), and the span text."""
        t = tokens(output)
        n = self.n
        exempt = set()
        if input_text:
            it = tokens(input_text)
            exempt = {hash(tuple(it[i:i + n])) for i in range(len(it) - n + 1)}
        best, best_at, run, start = 0, 0, 0, 0
        for i in range(len(t) - n + 1):
            h = hash(tuple(t[i:i + n]))
            if h in self.grams and h not in exempt:
                if run == 0:
                    start = i
                run += 1
                if run > best:
                    best, best_at = run, start
            else:
                run = 0
        span = best + n - 1 if best else 0
        return dict(span=span, text=" ".join(t[best_at:best_at + span]) if span else "")


class Signature:
    """Top-k author-distinctive word n-grams by log-odds with a Dirichlet prior (Monroe et al.)."""

    def __init__(self, k: int = 50, ns: tuple[int, ...] = (2, 3, 4), min_count: int = 10, min_docs: int = 8):
        self.k, self.ns, self.min_count, self.min_docs = k, ns, min_count, min_docs

    def _grams(self, text: str) -> list[str]:
        out = []
        for para in text.split("\n\n"):
            t = tokens(para)
            for n in self.ns:
                out += [" ".join(t[i:i + n]) for i in range(len(t) - n + 1)]
        return out

    def fit(self, author_docs: list[str], other_docs: list[str]) -> "Signature":
        a, docs = Counter(), Counter()
        for d in author_docs:
            g = self._grams(d)
            a.update(g)
            docs.update(set(g))
        b = Counter(g for d in other_docs for g in self._grams(d))
        na, nb = sum(a.values()), sum(b.values())
        prior = {g: a[g] + b[g] for g in a}
        a0 = sum(prior.values()) or 1
        scale = 0.01 * (na + nb) / a0            # prior worth 1% of the data
        z = {}
        for g, ca in a.items():
            if ca < self.min_count or docs[g] < self.min_docs:
                continue
            pa = scale * prior[g]
            la = math.log((ca + pa) / (na + scale * a0 - ca - pa))
            lb = math.log((b[g] + pa) / (nb + scale * a0 - b[g] - pa))
            z[g] = (la - lb) / math.sqrt(1 / (ca + pa) + 1 / (b[g] + pa))
        self.phrases = [g for g, _ in sorted(z.items(), key=lambda x: -x[1])[:self.k]]
        self._set = set(self.phrases)
        return self

    def rate(self, texts: list[str]) -> float:
        """Signature-phrase hits per 1,000 words."""
        hits = sum(1 for t in texts for g in self._grams(t) if g in self._set)
        words = sum(len(tokens(t)) for t in texts) or 1
        return 1000.0 * hits / words
