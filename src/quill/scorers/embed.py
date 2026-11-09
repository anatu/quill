"""Sentence-embedding helper with an on-disk cache keyed by model and text hash.

Two encoders are used and must not be mixed up:
  content  BAAI/bge-large-en-v1.5      topic clustering for the splits
  style    StyleDistance/styledistance  M2, diagnostic only
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import numpy as np

MODELS = {"content": "BAAI/bge-large-en-v1.5", "style": "StyleDistance/styledistance"}
_loaded: dict = {}


def _model(kind: str):
    if kind not in _loaded:
        import torch
        from sentence_transformers import SentenceTransformer

        dev = "mps" if torch.backends.mps.is_available() else "cpu"
        m = SentenceTransformer(MODELS[kind], trust_remote_code=False, device=dev)
        m.max_seq_length = 512
        _loaded[kind] = m
    return _loaded[kind]


def encode(texts: list[str], kind: str, cache_dir: Path) -> np.ndarray:
    """L2-normalized embeddings, one row per text. Texts longer than 512 tokens are truncated."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(cache_dir / f"emb_{kind}.sqlite")
    db.execute("CREATE TABLE IF NOT EXISTS e (h TEXT PRIMARY KEY, v BLOB)")
    hs = [hashlib.sha1(t.encode()).hexdigest() for t in texts]
    have = {}
    for i in range(0, len(hs), 500):
        part = hs[i:i + 500]
        for h, v in db.execute(f"SELECT h, v FROM e WHERE h IN ({','.join('?' * len(part))})", part):
            have[h] = np.frombuffer(v, dtype=np.float32)
    todo = sorted({h: t for h, t in zip(hs, texts) if h not in have}.items())
    if todo:
        E = _model(kind).encode([t for _, t in todo], batch_size=16, normalize_embeddings=True,
                                show_progress_bar=False).astype(np.float32)
        with db:
            db.executemany("INSERT OR REPLACE INTO e VALUES (?,?)", [(h, e.tobytes()) for (h, _), e in zip(todo, E)])
        have.update({h: e for (h, _), e in zip(todo, E)})
    db.close()
    return np.vstack([have[h] for h in hs]) if hs else np.zeros((0, 1), dtype=np.float32)


def centroid(E: np.ndarray) -> np.ndarray:
    c = E.mean(0)
    return c / np.linalg.norm(c)
