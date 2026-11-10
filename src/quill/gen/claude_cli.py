"""Claude through the `claude -p` command line, with a local cache.

Each call runs with no tools, no settings, no hooks and its own system prompt, so the
Claude Code prompt and the user's style hooks do not colour the text. Sending corpus text
here is a Claude API use: scope.yaml must say `claude_api: yes`.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
SYSTEM = "You are a careful writing assistant. Output only the requested text."
_lock = threading.Lock()


def prompt(name: str, **kw) -> str:
    """Fill configs/prompts/<name>.txt. Plain replacement: the text may hold braces."""
    t = (REPO / "configs" / "prompts" / f"{name}.txt").read_text().strip()
    for k, v in kw.items():
        t = t.replace("{" + k + "}", str(v))
    return t


def check_scope(cfg: dict) -> None:
    f = Path(cfg["paths"]["legal"]) / "scope.yaml"
    scope = (yaml.safe_load(f.read_text()) or {}).get("scope", {}) if f.exists() else {}
    if scope.get("claude_api") is not True:
        raise SystemExit(f"blocked: {f} does not say claude_api: yes")


class Claude:
    def __init__(self, cfg: dict, model: str, workers: int = 4, runner=None):
        check_scope(cfg)
        self.model, self.workers = model, workers
        self.runner = runner or self._run
        d = Path(cfg["paths"]["eval"]) / "cache"
        d.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(d / "claude.sqlite", check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS gen (key TEXT PRIMARY KEY, model TEXT, text TEXT, "
                        "cost REAL, made TEXT)")
        self.calls = self.hits = 0
        self.cost = 0.0

    def _run(self, text: str, system: str) -> tuple[str, float]:
        cmd = ["claude", "-p", "--model", self.model, "--system-prompt", system, "--tools", "",
               "--setting-sources", "", "--strict-mcp-config", "--no-session-persistence",
               "--output-format", "json"]
        last = ""
        for attempt in range(4):
            r = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=600,
                               cwd=tempfile.gettempdir())
            try:
                d = json.loads(r.stdout)
                if not d.get("is_error") and d.get("result", "").strip():
                    used = list(d.get("modelUsage", {}))
                    if used and not any(self.model in m or m in self.model for m in used):
                        raise SystemExit(f"asked for {self.model}, got {used}")
                    return d["result"].strip(), float(d.get("total_cost_usd") or 0)
                last = str(d.get("result") or d.get("subtype"))[:300]
            except json.JSONDecodeError:
                last = (r.stderr or r.stdout)[:300]
            time.sleep(5 * 2 ** attempt)
        raise RuntimeError(f"claude -p failed: {last}")

    def ask(self, text: str, system: str = SYSTEM, sample: int = 0) -> str:
        """sample: an index that makes repeated draws of one prompt distinct cache entries."""
        key = hashlib.sha256(json.dumps([self.model, system, text, sample]).encode()).hexdigest()
        with _lock:
            row = self.db.execute("SELECT text FROM gen WHERE key = ?", (key,)).fetchone()
        if row:
            self.hits += 1
            return row[0]
        out, cost = self.runner(text, system)
        with _lock:
            self.db.execute("INSERT OR REPLACE INTO gen VALUES (?,?,?,?,?)",
                            (key, self.model, out, cost, time.strftime("%Y-%m-%dT%H:%M:%S")))
            self.db.commit()
            self.calls += 1
            self.cost += cost
        return out

    def map(self, jobs: list[tuple]) -> list[str]:
        """jobs: (text,), (text, system) or (text, system, sample). Order is kept."""
        with ThreadPoolExecutor(self.workers) as ex:
            return list(ex.map(lambda j: self.ask(*j), jobs))
