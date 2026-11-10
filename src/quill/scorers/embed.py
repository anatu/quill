"""Sentence-embedding helper with an on-disk cache keyed by model and text hash.

Two encoders are used and must not be mixed up:
  content  BAAI/bge-large-en-v1.5      topic clustering for the splits
  style    StyleDistance/styledistance  M2, diagnostic only
  luar     rrivera1849/LUAR-MUD         M3, diagnostic only; a local copy with its own model code
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import numpy as np

MODELS = {"content": "BAAI/bge-large-en-v1.5", "style": "StyleDistance/styledistance"}
LUAR_DIR = Path("~/.quill/models/luar-mud").expanduser()
EPISODE = 8
_loaded: dict = {}


def _luar(texts: list[str]) -> np.ndarray:
    """One LUAR embedding per text. The text is cut into EPISODE equal token windows, which
    stand in for the short posts LUAR was trained on. The model code is the local copy's."""
    import torch
    from transformers import AutoModel, AutoTokenizer

    if "luar" not in _loaded:
        if not LUAR_DIR.exists():
            raise SystemExit(f"no LUAR model at {LUAR_DIR}: hf download rrivera1849/LUAR-MUD --local-dir {LUAR_DIR}")
        dev = "cpu"                     # the model's pooling code fails on MPS
        _loaded["luar"] = (AutoTokenizer.from_pretrained(LUAR_DIR, trust_remote_code=True),
                           AutoModel.from_pretrained(LUAR_DIR, trust_remote_code=True).to(dev).eval(), dev)
    tok, model, dev = _loaded["luar"]
    out = []
    for i in range(0, len(texts), 8):
        eps = []
        for t in texts[i:i + 8]:
            ids = tok(t, add_special_tokens=False)["input_ids"][:EPISODE * 126] or [tok.unk_token_id]
            n = -(-len(ids) // EPISODE)
            eps.append([[tok.bos_token_id] + ids[j * n:(j + 1) * n] + [tok.eos_token_id] for j in range(EPISODE)])
        L = max(len(w) for e in eps for w in e)
        ids = torch.tensor([[w + [tok.pad_token_id] * (L - len(w)) for w in e] for e in eps])
        att = torch.tensor([[[1] * len(w) + [0] * (L - len(w)) for w in e] for e in eps])
        with torch.no_grad():
            v = model(ids.to(dev), att.to(dev))
        out.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
    return np.vstack(out).astype(np.float32)


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
        E = _luar([t for _, t in todo]) if kind == "luar" else _model(kind).encode(
            [t for _, t in todo], batch_size=16, normalize_embeddings=True, show_progress_bar=False).astype(np.float32)
        with db:
            db.executemany("INSERT OR REPLACE INTO e VALUES (?,?)", [(h, e.tobytes()) for (h, _), e in zip(todo, E)])
        have.update({h: e for (h, _), e in zip(todo, E)})
    db.close()
    return np.vstack([have[h] for h in hs]) if hs else np.zeros((0, 1), dtype=np.float32)


def centroid(E: np.ndarray) -> np.ndarray:
    c = E.mean(0)
    return c / np.linalg.norm(c)
