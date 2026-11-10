"""Text pools for evaluation: the author's chunks by split, and the impostor pool.

Impostors are the cached passages of the similarity-pass authors (paths.baseline). They
are "close but separable" writers in the same register, plus two Claude controls that
form the LLM class. Each impostor post lands in train, dev or test by a hash of its id.
"""
from __future__ import annotations

import json
import zlib
from pathlib import Path

from ..corpus import split, store
from ..ingest import textlib as T

EXCLUDE = {"housel", "housel_A", "housel_B", "richards", "zweig"}   # self; authorship unverified; WSJ reprints
LLM = {"claude_housel", "claude_plain"}
NEIGHBOURS = ("lamade", "fs", "naval")


def segments(text: str, lo: int = 250, hi: int = 350) -> list[str]:
    """Cut a text into passages of about 300 words on paragraph boundaries, so every
    class is scored at the same length. A text too short to cut comes back whole."""
    out = T.make_passages([dict(id="x", paras=text.split("\n\n"))], lo=lo, hi=hi, carry=False)
    return [p["text"] for p in out] or [text]


def author_chunks(cfg: dict) -> list[dict]:
    """The author's usable chunks with their split: id, split, post, words, text."""
    ids = split.load(cfg)
    db = store.connect(store.db_path(cfg))
    out = [dict(id=r["id"], split=ids[r["id"]], post=r["post_file"], words=r["words"], text=r["text"],
                bucket=r["length_bucket"])
           for r in db.execute("SELECT * FROM usable_chunks ORDER BY id") if r["id"] in ids]
    db.close()
    return out


def part_of(group: str) -> str:
    return ("test", "dev", "train", "train", "train")[zlib.crc32(group.encode()) % 5]


def impostors(cfg: dict) -> list[dict]:
    """Impostor passages: author, kind (human | llm), group, part, text."""
    d = Path(cfg["paths"]["baseline"])
    out = []
    for f in sorted(d.glob("*.jsonl")):
        a = f.stem
        if a in EXCLUDE:
            continue
        for line in f.read_text().splitlines():
            r = json.loads(line)
            g = f"{a}:{r['group']}"
            out.append(dict(author=a, kind="llm" if a in LLM else "human", group=g, part=part_of(g),
                            text="\n\n".join(r["paras"])))
    return out


def m15_class(p: dict) -> str:
    """M15 classes: the author (added by the caller), Lamade, other human writers, LLM. Farnam
    Street and Naval have too little cached text for classes of their own, so they join `other`."""
    return "llm" if p["kind"] == "llm" else "lamade" if p["author"] == "lamade" else "other"
