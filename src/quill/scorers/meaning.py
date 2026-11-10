"""M4 meaning preservation.

  MIS    Mutual Implication Score (s-nlp/Mutual_Implication_Score, CC BY-NC-SA 4.0), for `restyle`:
         a symmetric paraphrase score in [0, 1]. The model reads sentence pairs, so a passage is cut
         into windows and each input window takes its best score over output spans near the same position.
  Facts  share of the input's fact lines that the output entails (MNLI model), for `write` and `restyle`.

Both models are local copies; scores are cached by text hash.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path

import numpy as np

MIS_DIR = Path("~/.quill/models/mis").expanduser()
NLI_MODEL = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
SENT = re.compile(r"(?<=[.!?])[\"”’)]*\s+")
_loaded: dict = {}


def _device():
    import torch

    return "mps" if torch.backends.mps.is_available() else "cpu"


class _Cache:
    def __init__(self, cache_dir: Path, name: str):
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(Path(cache_dir) / "scores.sqlite")
        self.db.execute("CREATE TABLE IF NOT EXISTS s (k TEXT PRIMARY KEY, v REAL)")
        self.name = name

    def key(self, a: str, b: str) -> str:
        return hashlib.sha1(f"{self.name}\x00{a}\x00{b}".encode()).hexdigest()

    def get_many(self, pairs: list[tuple[str, str]], compute) -> list[float]:
        keys = [self.key(a, b) for a, b in pairs]
        have = {}
        for i in range(0, len(keys), 500):
            part = keys[i:i + 500]
            have.update(self.db.execute(f"SELECT k, v FROM s WHERE k IN ({','.join('?' * len(part))})", part).fetchall())
        todo = sorted({k: p for k, p in zip(keys, pairs) if k not in have}.items(),
                      key=lambda kp: len(kp[1][0]) + len(kp[1][1]))        # similar lengths batch together
        for i in range(0, len(todo), 256):                                 # save as we go
            part = todo[i:i + 256]
            vals = [float(v) for v in compute([p for _, p in part])]
            with self.db:
                self.db.executemany("INSERT OR REPLACE INTO s VALUES (?,?)", [(k, v) for (k, _), v in zip(part, vals)])
            have.update((k, v) for (k, _), v in zip(part, vals))
        return [have[k] for k in keys]


def sentences(text: str) -> list[str]:
    return [s.strip() for p in text.split("\n\n") for s in SENT.split(p) if s.strip()]


def windows(text: str, words: int = 110) -> list[tuple[float, float, str]]:
    """Whole-sentence windows of about `words` words: (start, end, text), positions as shares of the text."""
    sents = sentences(text)
    total = max(1, sum(len(s.split()) for s in sents))
    out, cur, n, start, seen = [], [], 0, 0, 0
    for s in sents:
        cur.append(s)
        n += len(s.split())
        if n >= words:
            out.append((start / total, (seen + n) / total, " ".join(cur)))
            seen += n
            start, cur, n = seen, [], 0
    if cur:
        if out and n < words / 2:               # fold a short tail into the last window
            a, _, t = out.pop()
            out.append((a, 1.0, t + " " + " ".join(cur)))
        else:
            out.append((start / total, 1.0, " ".join(cur)))
    return out


def candidates(text: str, a: float, b: float, slack: float = 0.07, sizes=(1.0, 1.3)) -> list[str]:
    """Runs of whole sentences in `text` that could match an input window at share range [a, b]:
    they start within `slack` of a and hold about the same share of the text, at a few sizes."""
    sents = sentences(text)
    n = [len(x.split()) for x in sents]
    total = max(1, sum(n))
    starts = np.cumsum([0] + n[:-1]) / total
    out = []
    for i, st in enumerate(starts):
        if abs(st - a) > slack:
            continue
        for k in sizes:
            want, got, j = (b - a) * k * total, 0, i
            while j < len(sents) and got < want:
                got += n[j]
                j += 1
            out.append(" ".join(sents[i:j]))
    return list(dict.fromkeys(out)) or [text]


class MIS:
    def __init__(self, cache_dir: Path):
        self.cache = _Cache(cache_dir, "mis")

    def _raw(self, pairs: list[tuple[str, str]]) -> list[float]:
        import torch
        from safetensors.torch import load_file
        from transformers import AutoTokenizer, RobertaConfig, RobertaModel

        if "mis" not in _loaded:
            if not MIS_DIR.exists():
                raise SystemExit(f"no MIS model at {MIS_DIR}: hf download s-nlp/Mutual_Implication_Score --local-dir {MIS_DIR}")
            sd = load_file(MIS_DIR / "model.safetensors")
            enc = RobertaModel(RobertaConfig.from_pretrained(MIS_DIR), add_pooling_layer=False)
            miss = enc.load_state_dict({k[len("roberta."):]: v for k, v in sd.items() if k.startswith("roberta.")}, strict=False)
            assert not [k for k in miss.missing_keys if "position_ids" not in k], miss.missing_keys
            dev = _device()
            head = {k: sd[f"classifier.{k}"].to(dev) for k in ("dense.weight", "dense.bias", "out_proj_adjusted.weight",
                                                               "out_proj_adjusted.bias")}
            _loaded["mis"] = (AutoTokenizer.from_pretrained(MIS_DIR), enc.to(dev).eval(), head, dev)
        tok, enc, head, dev = _loaded["mis"]
        out = []
        for i in range(0, len(pairs), 8):
            a, b = zip(*pairs[i:i + 8])
            with torch.no_grad():
                h = []
                for x, y in ((a, b), (b, a)):
                    t = tok(list(x), list(y), return_tensors="pt", padding=True, truncation="longest_first", max_length=512)
                    cls = enc(**{k: v.to(dev) for k, v in t.items()}).last_hidden_state[:, 0]
                    h.append(torch.tanh(cls @ head["dense.weight"].T + head["dense.bias"]))
                z = torch.cat(h, 1) @ head["out_proj_adjusted.weight"].T + head["out_proj_adjusted.bias"]
                out += torch.sigmoid(z).squeeze(1).cpu().tolist()
        return out

    def pairs(self, pairs: list[tuple[str, str]]) -> list[float]:
        return self.cache.get_many(pairs, self._raw)

    def score(self, inputs: list[str], outputs: list[str]) -> list[float]:
        """One score per (input, output) passage pair: the mean over the input's windows of the best
        matching output span."""
        jobs, owner = [], []
        for i, (a, b) in enumerate(zip(inputs, outputs)):
            for w, (lo, hi, win) in enumerate(windows(a)):
                for c in candidates(b, lo, hi):
                    jobs.append((win, c))
                    owner.append((i, w))
        best: dict = {}
        for x, k in zip(self.pairs(jobs), owner):
            best[k] = max(best.get(k, 0.0), x)
        return [float(np.mean([v for (o, _), v in best.items() if o == i] or [0.0])) for i in range(len(inputs))]


def fact_lines(facts: str) -> list[str]:
    out = [re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", x).strip() for x in facts.splitlines()]
    return [x for x in out if len(x.split()) >= 3]


class Facts:
    """Per-fact entailment: P(output entails the fact), the best window of the output."""

    def __init__(self, cache_dir: Path, threshold: float = 0.5):
        self.cache = _Cache(cache_dir, "nli:" + NLI_MODEL)
        self.threshold = threshold

    def _raw(self, pairs: list[tuple[str, str]]) -> list[float]:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        if "nli" not in _loaded:
            dev = _device()
            m = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL).to(dev).eval()
            ent = {v.lower(): k for k, v in m.config.id2label.items()}["entailment"]
            _loaded["nli"] = (AutoTokenizer.from_pretrained(NLI_MODEL), m, ent, dev)
        tok, m, ent, dev = _loaded["nli"]
        out = []
        for i in range(0, len(pairs), 16):
            p, h = zip(*pairs[i:i + 16])
            t = tok(list(p), list(h), return_tensors="pt", padding=True, truncation="only_first", max_length=512)
            with torch.no_grad():
                out += torch.softmax(m(**{k: v.to(dev) for k, v in t.items()}).logits, -1)[:, ent].cpu().tolist()
        return out

    def score(self, facts: list[str], outputs: list[str]) -> list[float]:
        """Share of each fact list that its output entails."""
        jobs, owner = [], []
        for i, (f, o) in enumerate(zip(facts, outputs)):
            wins = [w for _, _, w in windows(o, 220)] or [o]
            for j, line in enumerate(fact_lines(f)):
                for w in wins:
                    jobs.append((w, line))
                    owner.append((i, j))
        s = self.cache.get_many(jobs, self._raw)
        best: dict = {}
        for x, k in zip(s, owner):
            best[k] = max(best.get(k, 0.0), x)
        out = []
        for i in range(len(facts)):
            v = [x >= self.threshold for (a, _), x in best.items() if a == i]
            out.append(float(np.mean(v)) if v else 1.0)
        return out
