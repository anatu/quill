"""Write curated pairs as mlx-lm chat data (plan.md Phase 3).

  sft-v1-s1  form A (paraphrase -> author)   the bake-off and stage 1
  sft-v1-s2  form B (draft -> author)        stage 2; Claude drafts only until Phase 4 adds the local half
train.jsonl holds train chunks; valid.jsonl holds dev chunks, for loss monitoring only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import curate as C
from . import generate as G

SETS = dict(s1="A", s2="B")


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
            body = "".join(json.dumps(dict(messages=C.messages(r, form)), ensure_ascii=False) + "\n" for r in keep)
            (d / f"{name}.jsonl").write_text(body)
            h.update(body.encode())
            n[name] = len(keep)
        man = dict(form=form, input=C.FORMS[form], rows=n, hash=h.hexdigest(),
                   target_words=sum(r["words"] for r in rows if r["split"] == "train" and not r["checks"][form]["fails"]))
        (d / "manifest.json").write_text(json.dumps(man, indent=1))
        out[stage] = dict(man, dir=str(d))
    return out
