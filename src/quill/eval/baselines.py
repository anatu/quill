"""Baselines and the recall probe (plan.md Phase 2).

  b0  Claude told to write like the author, with a frozen style guide and 5 exemplars
  b1  the untuned local base with the same prompt
  b2  the input itself (the floor; restyle only)
All sample N candidates and pick one with the same reranker. Outputs go to
<paths.eval>/outputs/<name>/<split>.jsonl, where `quill eval --system <name>` reads them.

The reranker here is a stand-in for Phase 6 [P]: hard gates on entities (M5), length (M12),
memorization (M9) and chat artifacts, then the StyleDistance centroid delta (M2). MIS is not
built, so meaning is not in the rank yet.
"""
from __future__ import annotations

import json
import random
import time
import zlib
from pathlib import Path

from ..gen.claude_cli import Claude, prompt
from ..scorers import entities
from . import inputs, pool

OPS = ("restyle", "write")
GUIDE_CHUNKS, EXEMPLARS = 30, 5


def b0_dir(cfg: dict) -> Path:
    return Path(cfg["paths"]["eval"]) / "b0"


def style_guide(cfg: dict, train: list[dict], claude: Claude | None = None) -> str:
    """Written once by Claude from 30 random train chunks, then frozen."""
    f = b0_dir(cfg) / "style_guide.md"
    if f.exists():
        return f.read_text()
    if claude is None:
        raise SystemExit(f"no style guide at {f}: run `quill baseline b0` first")
    picks = random.Random(0).sample(train, min(GUIDE_CHUNKS, len(train)))
    passages = "\n\n".join(f"[{i}]\n{c['text']}" for i, c in enumerate(picks, 1))
    guide = claude.ask(prompt("style_guide", n=len(picks), author=cfg["author"]["name"], passages=passages))
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(guide)
    (f.parent / "style_guide.json").write_text(json.dumps(dict(
        model=claude.model, made=time.strftime("%Y-%m-%d"), chunks=[c["id"] for c in picks]), indent=1))
    return guide


def exemplars(train: list[dict], row: dict, k: int = EXEMPLARS, max_words: int = 0) -> list[dict]:
    """k random train chunks in the row's length bucket; the draw depends only on the row id."""
    same = [c for c in train if c["bucket"] == row["bucket"] and (not max_words or c["words"] <= max_words)] or train
    return random.Random(zlib.crc32(row["id"].encode())).sample(same, min(k, len(same)))


def jobs_for(cfg: dict, rows: list[dict], train: list[dict], guide: str, n: int, ops=OPS,
             exemplar_max_words: int = 0) -> list[dict]:
    author = cfg["author"]["name"]
    out = []
    for r in rows:
        ex = "\n\n".join(f"[{i}]\n{c['text']}" for i, c in enumerate(exemplars(train, r, max_words=exemplar_max_words), 1))
        system = prompt("b0_system", author=author, guide=guide, exemplars=ex)
        for op in ops:
            if op == "restyle":
                user, given = prompt("b0_restyle", author=author, words=r["words"], input=r["draft"]), r["draft"]
            else:
                user = prompt("b0_write", author=author, words=r["words"], brief=r["brief"], facts=r["facts"])
                given = inputs.write_input(r)
            for s in range(n):
                out.append(dict(id=r["id"], op=op, sample=s, system=system, user=user, input=given, words=r["words"]))
    return out


def check(ctx, text: str, given: str, words: int, chunk_id: str | None = None) -> dict:
    """Hard gates on one candidate. In eval the target's own post is exempt from the memorization
    gate (harness.Context.spans); at run time there is no target."""
    ent = entities.compare(given, text)
    span = ctx.spans(text, given, chunk_id)[0]
    n = len(text.split())
    fails = []
    if not ent["ok"]:
        fails.append("entities")
    if abs(n - words) > 0.3 * words:
        fails.append("length")
    if span >= ctx.memo.n:
        fails.append("memorization")
    if ctx.lexicon.score(text)["hits"]["artifacts"]:
        fails.append("artifacts")
    return dict(fails=fails, words=n, span=span, entities_missing=sum(map(len, ent["missing"].values())),
                entities_added=sum(map(len, ent["added"].values())))


def rerank(ctx, cands: list[str], given: str, words: int, chunk_id: str | None = None) -> dict:
    """Pick the candidate with the best style delta among those that pass every gate. With none
    passing, return the one with the fewest failures and mark the output a fallback."""
    checks = [check(ctx, c, given, words, chunk_id) for c in cands]
    delta = [float(x) for x in ctx.style_delta(cands)] if ctx.use_embeddings else [0.0] * len(cands)
    ok = [i for i, c in enumerate(checks) if not c["fails"]]
    order = ok or sorted(range(len(cands)), key=lambda i: len(checks[i]["fails"]))
    order = [i for i in order if len(checks[i]["fails"]) == len(checks[order[0]]["fails"])]
    best = max(order, key=lambda i: delta[i])
    return dict(choice=best, fallback=not ok, checks=checks, delta=[round(d, 4) for d in delta])


def run(cfg: dict, name: str, part: str, n: int = 4, ctx=None, gen=None, limit: int | None = None, ops=OPS) -> dict:
    from . import harness

    rows = inputs.load(cfg, part)[:limit]
    if part == "coverage":
        ops = ("write",)                # a brief has no draft to restyle
    chunks = pool.author_chunks(cfg)
    bucket = {c["id"]: c["bucket"] for c in chunks}
    for r in rows:
        r["bucket"] = bucket.get(r["id"], "300-500")
    train = [c for c in chunks if c["split"] == "train"]
    out_dir = Path(cfg["paths"]["eval"]) / "outputs" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    g = cfg.get("gen", {})
    if name == "b2":
        items = [dict(id=r["id"], op="restyle", text=r["draft"], input=r["draft"], length_words=r["words"]) for r in rows]
        stats = dict(n=len(items))
    else:
        if name == "b0":
            gen = gen or Claude(cfg, g.get("draft_model", "claude-opus-5-5"), g.get("workers", 4))
            guide = style_guide(cfg, train, gen)
            jobs = jobs_for(cfg, rows, train, guide, n, ops)
            texts = gen.map([(j["user"], j["system"], j["sample"]) for j in jobs])
        elif name == "b1":
            if gen is None:
                from ..gen.local import Local

                gen = Local(cfg)
            guide = style_guide(cfg, train)
            jobs = jobs_for(cfg, rows, train, guide, n, ops)
            texts = gen.map([(j["user"], j["system"], j["sample"], int(j["words"] * 2.2) + 150) for j in jobs])
        else:
            raise SystemExit(f"unknown baseline {name}")
        ctx = ctx or harness.Context(cfg)
        groups: dict = {}
        for j, t in zip(jobs, texts):
            groups.setdefault((j["id"], j["op"]), []).append((j, t))
        items = []
        for (cid, op), g_ in groups.items():
            cands = [t for _, t in g_]
            j = g_[0][0]
            rr = rerank(ctx, cands, j["input"], j["words"], cid)
            items.append(dict(id=cid, op=op, text=cands[rr["choice"]], input=j["input"], length_words=j["words"],
                              fallback=rr["fallback"], candidates=cands, rerank=rr))
        fails = [f for i in items for c in i["rerank"]["checks"] for f in c["fails"]]
        stats = dict(n=len(items), samples=n, model=gen.model, new_calls=gen.calls,
                     fallback_rate=round(sum(i["fallback"] for i in items) / max(1, len(items)), 4),
                     candidate_fail_counts={f: fails.count(f) for f in sorted(set(fails))},
                     candidates=len(texts))
        if hasattr(gen, "cost"):
            stats["cost_usd"] = round(gen.cost, 2)
        if hasattr(gen, "peak_gb"):
            stats.update(tokens=gen.tokens, tok_per_s=round(gen.tokens / max(1e-9, gen.seconds), 1),
                         peak_gb=round(gen.peak_gb, 2))
    if limit is None:
        (out_dir / f"{part}.jsonl").write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in items))
        (out_dir / f"{part}.stats.json").write_text(json.dumps(stats, indent=1))
    return dict(stats, out=str(out_dir / f"{part}.jsonl"), items=items if limit else None)


# ---------------------------------------------------------------- recall probe

def first_sentences(text: str, min_words: int = 12) -> str:
    """The opening of a chunk: whole sentences up to at least min_words."""
    import re

    out = []
    for s in re.split(r"(?<=[.!?])\s+", text.split("\n\n")[0]):
        out.append(s)
        if len(" ".join(out).split()) >= min_words:
            break
    return " ".join(out)


def recall_probe(cfg: dict, part: str = "dev", gen=None, ctx=None, limit: int | None = None, name: str = "base") -> dict:
    """Ask a model for the author's held-out text three ways (a summary, a neutral paraphrase,
    the opening line) and record the longest verbatim span against the whole corpus. Words the
    prompt itself supplied are exempt."""
    from . import harness

    if gen is None:
        from ..gen.local import Local

        gen = Local(cfg)
    ctx = ctx or harness.Context(cfg, use_embeddings=False)
    author = cfg["author"]["name"]
    text = {c["id"]: c["text"] for c in pool.author_chunks(cfg)}
    rows = inputs.load(cfg, part)[:limit]
    jobs = []
    for r in rows:
        op = first_sentences(text[r["id"]])
        jobs += [dict(id=r["id"], kind="summary", given=r["brief"],
                      user=prompt("probe_summary", author=author, words=r["words"], brief=r["brief"])),
                 dict(id=r["id"], kind="paraphrase", given=r["draft"],
                      user=prompt("probe_paraphrase", author=author, input=r["draft"])),
                 dict(id=r["id"], kind="opening", given=op,
                      user=prompt("probe_opening", author=author, words=r["words"], opening=op))]
    outs = gen.map([(j["user"], None, 0, int(next(r["words"] for r in rows if r["id"] == j["id"]) * 2.2) + 150)
                    if hasattr(gen, "peak_gb") else (j["user"],) for j in jobs])
    res = []
    for j, o in zip(jobs, outs):
        m = ctx.memo.longest(o, j["given"])
        res.append(dict(id=j["id"], kind=j["kind"], span=m["span"], text=m.get("text", ""), output_words=len(o.split())))
    by = {}
    for k in ("summary", "paraphrase", "opening"):
        s = sorted(r["span"] for r in res if r["kind"] == k)
        by[k] = dict(n=len(s), max_span=s[-1] if s else 0, flagged=sum(x >= ctx.memo.n for x in s),
                     median_span=s[len(s) // 2] if s else 0)
    rep = dict(system=f"recall-probe:{name}", model=gen.model, split=part, generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
               gate_words=ctx.memo.n, prompts=len(res), max_span=max((r["span"] for r in res), default=0),
               flagged=sum(r["span"] >= ctx.memo.n for r in res), by_kind=by)
    if limit is None:
        d = Path(cfg["paths"]["eval"]) / "recall"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}-{part}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res))
        rd = harness.REPO / "eval_reports"
        (rd / f"recall-probe-{name}-{part}.json").write_text(json.dumps(rep, indent=1))
        L = [f"# Recall probe: {name} ({gen.model}) on {part} ({rep['generated']})", "",
             f"Longest verbatim span shared with the whole corpus, in words. The gate is {ctx.memo.n}. "
             "Words supplied by the prompt are exempt. Spans in an untuned model are the baseline the adapter must not raise (H8).",
             "", "| Prompt | n | Max span | Median | At or over the gate |", "|---|---|---|---|---|"]
        L += [f"| {k} | {v['n']} | {v['max_span']} | {v['median_span']} | {v['flagged']} |" for k, v in by.items()]
        (rd / f"recall-probe-{name}-{part}.md").write_text("\n".join(L) + "\n")
        rep["_out"] = str(rd / f"recall-probe-{name}-{part}.md")
    return dict(rep, results=res if limit else None)
