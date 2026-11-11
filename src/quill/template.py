"""The prompt template. The pair builder and the daemon both render through here, so training
and inference see byte-identical prompts (plan.md 2.3, Phase 3)."""
from __future__ import annotations

VERSION = "quill v2"
OPS = ("restyle",)
INPUTS = ("paraphrase", "draft")
BUCKETS = ("150-300", "300-500", "500-800")
VOICE = "v0"


def bucket(words: int) -> str:
    return BUCKETS[0] if words < 300 else BUCKETS[1] if words < 500 else BUCKETS[2]


def system(op: str, input_kind: str, length: str, voice: str = VOICE) -> str:
    if op not in OPS or input_kind not in INPUTS or length not in BUCKETS:
        raise ValueError(f"bad template fields: {op} {input_kind} {length}")
    return f"{VERSION}\nop: {op}\ninput: {input_kind}\nlength: {length}\nvoice: {voice}"


def messages(op: str, input_kind: str, length: str, text: str, target: str | None = None) -> list[dict]:
    m = [dict(role="system", content=system(op, input_kind, length)), dict(role="user", content=text.strip())]
    if target is not None:
        m.append(dict(role="assistant", content=target.strip()))
    return m
