"""Blind reading tests (plan.md Phase 2 and Phase 8).

  A  absolute: the author's real passage against a system's output on the same content.
     The reader picks the real one. Indistinguishable means at most 25 of 40 correct.
  R  relative: a reference excerpt from a train post, then the system and a baseline on the
     same input. The reader picks the one that reads more like the reference's author.

A kit is built once and frozen. Texts are length-matched, with whitespace and quotes normalized,
and the order of each pair is shuffled. Kits hold corpus text and stay under <paths.eval>/blind/.
"""
from __future__ import annotations

import json
import random
import re
import time
from math import comb
from pathlib import Path

from . import pool

QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", " ": " "})
SENT_END = re.compile(r"(?<=[.!?])[\"')]*\s+")


def normalize(text: str) -> str:
    text = text.translate(QUOTES).replace("**", "")
    return "\n\n".join(re.sub(r"\s+", " ", p).strip() for p in text.split("\n\n") if p.strip())


def trim(text: str, words: int) -> str:
    """Cut to at most `words` words at a sentence end; keep paragraph breaks."""
    out, n = [], 0
    for p in text.split("\n\n"):
        keep = []
        for s in SENT_END.split(p):
            k = len(s.split())
            if n + k > words and (out or keep):
                return "\n\n".join(out + ([" ".join(keep)] if keep else []))
            keep.append(s)
            n += k
        out.append(" ".join(keep))
    return "\n\n".join(out)


def match(a: str, b: str, cap: int = 350) -> tuple[str, str]:
    a, b = normalize(a), normalize(b)
    w = min(len(a.split()), len(b.split()), cap)
    return trim(a, w), trim(b, w)


def binom_p(k: int, n: int) -> float:
    """One-sided P(X >= k) for X ~ Binomial(n, 0.5)."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def kit_dir(cfg: dict, test: str, system: str, part: str) -> Path:
    return Path(cfg["paths"]["eval"]) / "blind" / f"{test}-{system}-{part}"


def _outputs(cfg: dict, system: str, part: str, op: str) -> dict:
    f = Path(cfg["paths"]["eval"]) / "outputs" / system / f"{part}.jsonl"
    if not f.exists():
        raise SystemExit(f"no outputs for system '{system}' on {part}: expected {f}")
    return {r["id"]: r["text"] for r in map(json.loads, f.read_text().splitlines()) if r.get("op", op) == op}


def make(cfg: dict, test: str, system: str, part: str = "test", n: int = 40, baseline: str = "b0", op: str = "restyle",
         seed: int = 0, chunks: list[dict] | None = None, outputs: dict | None = None) -> dict:
    d = kit_dir(cfg, test, system, part)
    if (d / "kit.json").exists():
        return json.loads((d / "kit.json").read_text())
    chunks = chunks if chunks is not None else pool.author_chunks(cfg)
    out = outputs or {s: _outputs(cfg, s, part, op) for s in ([system] if test == "A" else [system, baseline])}
    rng = random.Random(seed)
    held = [c for c in chunks if c["split"] == part and all(c["id"] in o for o in out.values())]
    by_post: dict = {}
    for c in held:                                  # one chunk per post, so no essay repeats
        by_post.setdefault(c["post"], []).append(c)
    picks = [rng.choice(v) for _, v in sorted(by_post.items())]
    rng.shuffle(picks)
    extra = [c for c in held if c not in picks]
    rng.shuffle(extra)
    picks = (picks + extra)[:n]
    train = [c for c in chunks if c["split"] == "train"]
    items = []
    for c in picks:
        flip = rng.random() < 0.5
        if test == "A":
            real, sys_ = match(c["text"], out[system][c["id"]])
            pair, truth = ((sys_, real), 2) if flip else ((real, sys_), 1)
            items.append(dict(id=c["id"], first=pair[0], second=pair[1], truth=truth))
        else:
            s, b = match(out[system][c["id"]], out[baseline][c["id"]])
            pair, truth = ((b, s), 2) if flip else ((s, b), 1)
            ref = trim(normalize(rng.choice(train)["text"]), 250)
            items.append(dict(id=c["id"], reference=ref, first=pair[0], second=pair[1], truth=truth))
    kit = dict(test=test, system=system, baseline=baseline if test == "R" else None, split=part, op=op, seed=seed,
               made=time.strftime("%Y-%m-%d"), n=len(items), items=items,
               question="Which passage is the real one?" if test == "A" else
               "Which passage reads more like the author of the reference?")
    d.mkdir(parents=True, exist_ok=True)
    (d / "kit.json").write_text(json.dumps(kit, ensure_ascii=False, indent=1))
    return kit


def answers(d: Path) -> list[dict]:
    f = d / "answers.jsonl"
    return [json.loads(x) for x in f.read_text().splitlines() if x.strip()] if f.exists() else []


def session(cfg: dict, kit: dict, ask=input, show=print) -> None:
    """Interactive read. Resumes where the last session stopped; `q` quits."""
    d = kit_dir(cfg, kit["test"], kit["system"], kit["split"])
    done = {a["id"] for a in answers(d)}
    todo = [i for i in kit["items"] if i["id"] not in done]
    for k, it in enumerate(todo, 1):
        show(f"\n{'=' * 78}\nPair {len(done) + k} of {kit['n']}\n")
        if "reference" in it:
            show(f"REFERENCE\n\n{it['reference']}\n\n{'-' * 78}")
        show(f"PASSAGE 1\n\n{it['first']}\n\n{'-' * 78}\nPASSAGE 2\n\n{it['second']}\n")
        pick = ""
        while pick not in ("1", "2", "q"):
            pick = ask(f"{kit['question']} [1/2, q to stop] ").strip().lower()
        if pick == "q":
            return
        reason = ask("One-line reason: ").strip()
        seen = ask("Did you recognize either passage? [y/N] ").strip().lower().startswith("y")
        with (d / "answers.jsonl").open("a") as f:
            f.write(json.dumps(dict(id=it["id"], pick=int(pick), correct=int(pick) == it["truth"], reason=reason,
                                    recognized=seen, at=time.strftime("%Y-%m-%dT%H:%M:%S")), ensure_ascii=False) + "\n")


def report(cfg: dict, kit: dict) -> dict:
    """A: `hits` counts correct picks of the real passage. R: `hits` counts picks of the system."""
    ans = answers(kit_dir(cfg, kit["test"], kit["system"], kit["split"]))
    fresh = [a for a in ans if not a["recognized"]]
    out = dict(test=kit["test"], system=kit["system"], baseline=kit["baseline"], split=kit["split"], n=kit["n"],
               answered=len(ans), hits=sum(a["correct"] for a in ans), recognized=len(ans) - len(fresh))
    out["p_one_sided"] = round(binom_p(out["hits"], len(ans)), 4)
    out["unrecognized"] = dict(answered=len(fresh), hits=sum(a["correct"] for a in fresh),
                               p_one_sided=round(binom_p(sum(a["correct"] for a in fresh), len(fresh)), 4))
    if len(ans) == kit["n"] == 40:
        out["verdict"] = (("indistinguishable (H1 met)" if out["hits"] <= 25 else "reader detects the system (H1 failed)")
                          if kit["test"] == "A" else
                          ("system beats the baseline (H2 met)" if out["hits"] >= 26 else "no reliable preference (H2 not met)"))
    out["reasons"] = [a["reason"] for a in ans if a["reason"]]
    return out
