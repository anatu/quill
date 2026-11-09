"""M1 authorship verification and M15 attribution.

Both use character 3-5-gram TF-IDF (top 10k features) and logistic regression. They are
decision metrics, so they share nothing with the rerank scorers.
"""
from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline


def _pipe():
    return make_pipeline(
        TfidfVectorizer(analyzer="char", ngram_range=(3, 5), max_features=10_000, sublinear_tf=True, lowercase=False),
        LogisticRegression(C=10.0, max_iter=3000, class_weight="balanced"))


class Verifier:
    """M1. P(author) per passage. The accept threshold sits at a fixed impostor false-accept rate,
    set from cross-validated predictions on the training impostors."""

    def fit(self, pos: list[str], pos_groups: list[str], neg: list[str], neg_groups: list[str],
            fpr: float = 0.05, seed: int = 0) -> "Verifier":
        X = np.array(pos + neg, dtype=object)
        y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
        g = np.array(list(pos_groups) + list(neg_groups))
        oof = np.zeros(len(y))
        k = min(5, len(set(pos_groups)), len(set(neg_groups)))
        for tr, te in StratifiedGroupKFold(n_splits=k, shuffle=True, random_state=seed).split(X, y, g):
            oof[te] = _pipe().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
        self.threshold = float(np.quantile(oof[y == 0], 1 - fpr))
        self.cv_accept_pos = float((oof[y == 1] >= self.threshold).mean())
        self.model = _pipe().fit(X, y)
        return self

    def prob(self, texts: list[str]) -> np.ndarray:
        return self.model.predict_proba(np.array(texts, dtype=object))[:, 1] if texts else np.zeros(0)

    def accept(self, texts: list[str]) -> np.ndarray:
        return self.prob(texts) >= self.threshold


class Attributor:
    """M15. One class per label; reports the share of passages assigned to each."""

    def fit(self, texts: list[str], labels: list[str]) -> "Attributor":
        self.model = _pipe().fit(np.array(texts, dtype=object), np.array(labels))
        self.classes = list(self.model.classes_)
        return self

    def predict(self, texts: list[str]) -> list[str]:
        return list(self.model.predict(np.array(texts, dtype=object))) if texts else []

    def shares(self, texts: list[str]) -> dict[str, float]:
        p = self.predict(texts)
        return {c: (p.count(c) / len(p) if p else 0.0) for c in self.classes}
