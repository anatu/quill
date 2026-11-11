"""Write curated pairs as mlx-lm chat data (plan.md Phase 3).

  sft-v1-s1  form A (paraphrase -> author)   the bake-off and stage 1
  sft-v1-s2  form B (draft -> author)        stage 2; Claude drafts only until Phase 4 adds the local half
  sft-v1-s1p form A with input paragraphs merged in part of the rows, so the adapter learns to
             set its own paragraph breaks instead of copying the input's
train.jsonl holds train chunks; valid.jsonl holds dev chunks, for loss monitoring only.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from . import curate as C
from . import generate as G

SETS = dict(s1="A", s2="B", s1p="A")
MERGED = {"s1p"}                    # stages whose inputs get merge_paragraphs
KEEP, PARTIAL = 0.4, 0.4            # shares left as is / merged in groups of 2-4; the rest fully merged


def merge_paragraphs(text: str, key: str) -> str:
    """Join neighbouring paragraphs of an input. Marker lines stay paragraphs of their own.
    The choice is fixed by `key`, so the set is reproducible."""
    rng = random.Random(key)
    u = rng.random()
    if u < KEEP:
        return text
    out, run = [], []

    def flush():
        while run:
            k = len(run) if u >= KEEP + PARTIAL else rng.randint(2, 4)
            out.append(" ".join(run[:k]))
            del run[:k]

    for para in (x.strip() for x in text.split("\n\n") if x.strip()):
        if G.MARKER.fullmatch(para):
            flush()
            out.append(para)
        else:
            run.append(para)
    flush()
    return "\n\n".join(out)


def _messages(row: dict, form: str, stage: str) -> list[dict]:
    if stage in MERGED:
        key = C.FORMS[form]
        row = dict(row, **{key: merge_paragraphs(row[key], f"{stage}:{row['id']}")})
    return C.messages(row, form)


def data_dir(cfg: dict, stage: str) -> Path:
    return Path(cfg["paths"]["home"]) / "data" / "mlx" / f"sft-{G.VERSION}-{stage}"


def write(cfg: dict, rows: list[dict]) -> dict:
    out = {}
    for stage, form in SETS.items():
        d = data_dir(cfg, stage)
        d.mkdir(parents=True, exist_ok=True)
        n = {}
        h = hashlib.sha256()
        for name, part in (("train", "train"), ("valid", "dev")):
            keep = [r for r in rows if r["split"] == part and not r["checks"][form]["fails"]]
            body = "".join(json.dumps(dict(messages=_messages(r, form, stage)), ensure_ascii=False) + "\n" for r in keep)
            (d / f"{name}.jsonl").write_text(body)
            h.update(body.encode())
            n[name] = len(keep)
        man = dict(form=form, input=C.FORMS[form], merged=stage in MERGED, rows=n, hash=h.hexdigest(),
                   target_words=sum(r["words"] for r in rows if r["split"] == "train" and not r["checks"][form]["fails"]))
        (d / "manifest.json").write_text(json.dumps(man, indent=1))
        out[stage] = dict(man, dir=str(d))
    return out
