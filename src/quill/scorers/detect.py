"""M10 machine-text detector: Fast-DetectGPT, analytic form (Bao et al. 2024), with gpt-neo-2.7B
as both the scoring and the sampling model. The score is the conditional probability curvature:
higher reads as more machine-like. Diagnostic only: it never certifies an output.
"""
from __future__ import annotations

from pathlib import Path

from .meaning import _Cache, _device

MODEL_DIR = Path("~/.quill/models/gpt-neo-2.7b").expanduser()
_loaded: dict = {}


class FastDetect:
    def __init__(self, cache_dir: Path, max_tokens: int = 512):
        self.cache = _Cache(cache_dir, f"fast-detectgpt:gpt-neo-2.7b:{max_tokens}")
        self.max_tokens = max_tokens

    def _raw(self, pairs: list[tuple[str, str]]) -> list[float]:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if "m" not in _loaded:
            if not MODEL_DIR.exists():
                raise SystemExit(f"no detector model at {MODEL_DIR}: hf download EleutherAI/gpt-neo-2.7B --local-dir {MODEL_DIR}")
            dev = _device()
            _loaded["m"] = (AutoTokenizer.from_pretrained(MODEL_DIR),
                            AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float16).to(dev).eval(), dev)
        tok, model, dev = _loaded["m"]
        out = []
        for text, _ in pairs:
            ids = tok(text, return_tensors="pt", truncation=True, max_length=self.max_tokens)["input_ids"].to(dev)
            if ids.shape[1] < 8:
                out.append(0.0)
                continue
            with torch.no_grad():
                lp = torch.log_softmax(model(ids).logits[0, :-1].float(), -1)
            p = lp.exp()
            ll = lp.gather(1, ids[0, 1:, None]).squeeze(1)
            mean = (p * lp).sum(-1)
            var = (p * lp * lp).sum(-1) - mean * mean
            out.append(float((ll.sum() - mean.sum()) / var.sum().sqrt()))
        return out

    def score(self, texts: list[str]) -> list[float]:
        return self.cache.get_many([(t, "") for t in texts], self._raw)
