"""Write curated pairs as mlx-lm chat data (plan.md Phase 3).

  sft-v1-s1  form A (paraphrase -> author)   the bake-off and stage 1
  sft-v1-s2  form B (draft -> author)        stage 2; a row uses the untuned base's draft when
             pairs/local.py made one that passes curation, else the Claude draft
  sft-v1-s2s / s1ps  the s2 / s1p sets, keeping only pairs whose target passes the eval's strict
             entity gate against its input, both ways. Curation's closure check is form-tolerant
             and one-way, so about a third of form A and half of form B pairs show the adapter a
             target that drops or re-forms a name or number of the input.
  sft-v1-s2m s1p and s2 joined: stage 2 on drafts while the paraphrase pairs keep fidelity pressure on
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

SETS = dict(s1="A", s2="B", s1p="A", s2s="B", s1ps="A")
MERGED = {"s1p", "s1ps"}            # stages whose inputs get merge_paragraphs
MIXES = dict(s2m=("s1p", "s2"))     # stage -> the stages whose rows it joins: both forms in one set
STRICT = {"s2s", "s1ps"}            # stages that keep only pairs passing the eval's entity gate
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


def uses_local(row: dict, form: str) -> bool:
    return form == "B" and "L" in row["checks"] and not row["checks"]["L"]["fails"]


def strict_ok(row: dict, form: str) -> bool:
    from ..scorers import entities

    inp = row["draft_local"] if uses_local(row, form) else row[C.FORMS[form]]
    return entities.compare(C.plain(inp), C.plain(row["target"]))["ok"]


def _messages(row: dict, form: str, stage: str) -> list[dict]:
    if uses_local(row, form):
        row = dict(row, draft=row["draft_local"])
    if stage in MERGED:
        key = C.FORMS[form]
        row = dict(row, **{key: merge_paragraphs(row[key], f"{stage}:{row['id']}")})
    return C.messages(row, form)


def data_dir(cfg: dict, stage: str) -> Path:
    return Path(cfg["paths"]["home"]) / "data" / "mlx" / f"sft-{G.VERSION}-{stage}"


def write(cfg: dict, rows: list[dict]) -> dict:
    from ..scorers import entities

    out = {}
    entities.set_common(r["target"] for r in rows)
    ok = {form: {r["id"]: strict_ok(r, form) for r in rows} for form in set(SETS.values())} if rows else {}
    for stage, form in SETS.items():
        d = data_dir(cfg, stage)
        d.mkdir(parents=True, exist_ok=True)
        n = {}
        h = hashlib.sha256()
        for name, part in (("train", "train"), ("valid", "dev")):
            keep = [r for r in rows if r["split"] == part and not r["checks"][form]["fails"]
                    and (stage not in STRICT or ok[form][r["id"]])]
            body = "".join(json.dumps(dict(messages=_messages(r, form, stage)), ensure_ascii=False) + "\n" for r in keep)
            (d / f"{name}.jsonl").write_text(body)
            h.update(body.encode())
            n[name] = len(keep)
        man = dict(form=form, input=C.FORMS[form], merged=stage in MERGED, rows=n,
                   strict=stage in STRICT,
                   local={part: sum(uses_local(r, form) for r in rows if r["split"] == part and not r["checks"][form]["fails"]
                                    and (stage not in STRICT or ok[form][r["id"]]))
                          for part in ("train", "dev")}, hash=h.hexdigest(),
                   target_words=sum(r["words"] for r in rows if r["split"] == "train" and not r["checks"][form]["fails"]))
        (d / "manifest.json").write_text(json.dumps(man, indent=1))
        out[stage] = dict(man, dir=str(d))
    for stage, parts in MIXES.items():
        d = data_dir(cfg, stage)
        d.mkdir(parents=True, exist_ok=True)
        h, n = hashlib.sha256(), {}
        for name in ("train", "valid"):
            body = "".join((data_dir(cfg, x) / f"{name}.jsonl").read_text() for x in parts)
            (d / f"{name}.jsonl").write_text(body)
            h.update(body.encode())
            n[name] = body.count("\n")
        man = dict(mix=list(parts), rows=n, local=out[parts[-1]]["local"], strict=False, hash=h.hexdigest())
        (d / "manifest.json").write_text(json.dumps(man, indent=1))
        out[stage] = dict(man, dir=str(d))
    return out
