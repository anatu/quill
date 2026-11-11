"""The local base model through mlx-lm, with a cache. Thinking is off in the chat template."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path

THINK = re.compile(r"<think>.*?</think>\s*", re.S)


class Local:
    def __init__(self, cfg: dict, temp: float = 0.7, top_p: float = 0.95, adapter: str | Path | None = None):
        g = cfg.get("gen", {})
        self.path = Path(g.get("base_model", "~/.quill/models/qwen3.5-9b-4bit")).expanduser()
        self.adapter = Path(adapter).expanduser() if adapter else None
        self.model = self.path.name + (f"+{self.adapter.name}" if self.adapter else "")
        if self.adapter:                # a retrained adapter of the same name must not hit the old cache
            self.model += ":" + hashlib.sha256((self.adapter / "adapters.safetensors").read_bytes()).hexdigest()[:8]
        self.temp, self.top_p = temp, top_p
        d = Path(cfg["paths"]["eval"]) / "cache"
        d.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(d / "local.sqlite")
        self.db.execute("CREATE TABLE IF NOT EXISTS gen (key TEXT PRIMARY KEY, model TEXT, text TEXT, "
                        "tokens INTEGER, tps REAL, peak_gb REAL, made TEXT)")
        self._m = None
        self.calls = self.hits = self.tokens = 0
        self.seconds = 0.0
        self.peak_gb = 0.0

    def _load(self):
        if self._m is None:
            from mlx_lm import load

            self._m = load(str(self.path), adapter_path=str(self.adapter) if self.adapter else None)
        return self._m

    def unload(self) -> None:
        """Free the model, so a second one fits in memory."""
        self._m = None
        import gc

        import mlx.core as mx

        gc.collect()
        mx.clear_cache()

    def render(self, user: str, system: str | None) -> str:
        _, tok = self._load()
        msgs = ([dict(role="system", content=system)] if system else []) + [dict(role="user", content=user)]
        return tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False, enable_thinking=False)

    def ask(self, user: str, system: str | None = None, sample: int = 0, max_tokens: int = 1200) -> str:
        key = hashlib.sha256(json.dumps([self.model, self.temp, self.top_p, system, user, sample, max_tokens])
                             .encode()).hexdigest()
        row = self.db.execute("SELECT text FROM gen WHERE key = ?", (key,)).fetchone()
        if row:
            self.hits += 1
            return row[0]
        import mlx.core as mx
        from mlx_lm import stream_generate
        from mlx_lm.sample_utils import make_sampler

        model, tok = self._load()
        mx.random.seed(int(key[:8], 16))
        t0, parts, last = time.time(), [], None
        for last in stream_generate(model, tok, self.render(user, system), max_tokens=max_tokens,
                                    sampler=make_sampler(temp=self.temp, top_p=self.top_p)):
            parts.append(last.text)
        text = THINK.sub("", "".join(parts)).strip()
        n = last.generation_tokens if last else 0
        tps = last.generation_tps if last else 0.0
        peak = last.peak_memory if last else 0.0
        self.db.execute("INSERT OR REPLACE INTO gen VALUES (?,?,?,?,?,?,?)",
                        (key, self.model, text, n, tps, peak, time.strftime("%Y-%m-%dT%H:%M:%S")))
        self.db.commit()
        self.calls += 1
        self.tokens += n
        self.seconds += time.time() - t0
        self.peak_gb = max(self.peak_gb, peak)
        return text

    def map(self, jobs: list[tuple], progress: bool = True) -> list[str]:
        out = []
        for i, j in enumerate(jobs):
            out.append(self.ask(*j))
            if progress and (i + 1) % 20 == 0:
                print(f"  {i + 1}/{len(jobs)}  new {self.calls}  {self.tokens / max(1e-9, self.seconds):.0f} tok/s overall",
                      flush=True)
        return out
