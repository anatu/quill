"""Frozen eval inputs for dev and test chunks (plan.md Phase 2).

Per chunk: a fact list, a generic assistant draft written from the facts (the `restyle`
input) and a 1-3 sentence brief (with the facts, the `write` input). Made once, then
frozen with a hash; every system is scored on the same inputs.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from ..gen.claude_cli import Claude, prompt
from . import pool

VERSION = "v1"


def inputs_dir(cfg: dict) -> Path:
    return Path(cfg["paths"]["eval"]) / "inputs" / VERSION


def load(cfg: dict, part: str) -> list[dict]:
    if part == "coverage":
        from . import coverage

        return coverage.load(cfg)
    f = inputs_dir(cfg) / f"{part}.jsonl"
    if not f.exists():
        raise SystemExit(f"no eval inputs for {part}: run `quill inputs`")
    return [json.loads(x) for x in f.read_text().splitlines() if x.strip()]


def write_input(row: dict) -> str:
    """The text a `write` system is given; also what its output is checked against."""
    return f"{row['brief']}\n\n{row['facts']}"


def make(cfg: dict, parts=("dev", "test"), force: bool = False, limit: int | None = None,
         claude: dict | None = None) -> dict:
    d = inputs_dir(cfg)
    man = d / "manifest.json"
    if man.exists() and not force and limit is None:
        return dict(json.loads(man.read_text()), created=False, dir=str(d))
    g = cfg.get("gen", {})
    claude = claude or {}
    util = claude.get("util") or Claude(cfg, g.get("util_model", "claude-sonnet-5-5"), g.get("workers", 4))
    drafter = claude.get("draft") or Claude(cfg, g.get("draft_model", "claude-opus-5-5"), g.get("workers", 4))
    chunks = [c for c in pool.author_chunks(cfg) if c["split"] in parts]
    if limit:
        chunks = chunks[:limit]
    facts = util.map([(prompt("facts", text=c["text"]),) for c in chunks])
    briefs = util.map([(prompt("brief", text=c["text"]),) for c in chunks])
    drafts = drafter.map([(prompt("draft", facts=f, words=c["words"]),) for c, f in zip(chunks, facts)])
    rows = [dict(id=c["id"], split=c["split"], post=c["post"], words=c["words"], brief=b, facts=f, draft=dr,
                 draft_words=len(dr.split())) for c, f, b, dr in zip(chunks, facts, briefs, drafts)]
    out = dict(version=VERSION, frozen=time.strftime("%Y-%m-%d"), util_model=util.model, draft_model=drafter.model,
               n={p: sum(r["split"] == p for r in rows) for p in parts},
               draft_to_target_words=round(sum(r["draft_words"] for r in rows) / max(1, sum(r["words"] for r in rows)), 3),
               new_calls=util.calls + drafter.calls, cost_usd=round(util.cost + drafter.cost, 2))
    if limit is None:
        d.mkdir(parents=True, exist_ok=True)
        for p in parts:
            (d / f"{p}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows if r["split"] == p))
        out["hash"] = hashlib.sha256(json.dumps(sorted((r["id"], r["brief"], r["facts"], r["draft"]) for r in rows))
                                     .encode()).hexdigest()
        man.write_text(json.dumps(out, indent=1))
    return dict(out, created=True, dir=str(d), rows=rows if limit else None)


def train_drafts_file(cfg: dict) -> Path:
    return Path(cfg["paths"]["eval"]) / "negatives" / "train_drafts.jsonl"


def train_drafts(cfg: dict) -> list[dict]:
    f = train_drafts_file(cfg)
    return [json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.exists() else []


def make_train_drafts(cfg: dict, limit: int | None = None, claude: dict | None = None) -> dict:
    """Facts and a generic draft for every train chunk, with the eval-input prompts. The drafts are
    verifier negatives (the author's content in a plain voice) and Phase 3 pair inputs. They are
    not part of the frozen eval inputs."""
    g = cfg.get("gen", {})
    claude = claude or {}
    util = claude.get("util") or Claude(cfg, g.get("util_model", "claude-sonnet-5-5"), g.get("workers", 4))
    drafter = claude.get("draft") or Claude(cfg, g.get("draft_model", "claude-opus-5-5"), g.get("workers", 4))
    chunks = [c for c in pool.author_chunks(cfg) if c["split"] == "train"][:limit]
    facts = util.map([(prompt("facts", text=c["text"]),) for c in chunks])
    drafts = drafter.map([(prompt("draft", facts=f, words=c["words"]),) for c, f in zip(chunks, facts)])
    rows = [dict(id=c["id"], split="train", post=c["post"], words=c["words"], facts=f, draft=d, draft_words=len(d.split()))
            for c, f, d in zip(chunks, facts, drafts)]
    out = dict(n=len(rows), new_calls=util.calls + drafter.calls, cost_usd=round(util.cost + drafter.cost, 2))
    if limit is None:
        f = train_drafts_file(cfg)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        out["file"] = str(f)
    return out
