"""Verifier check: which style scorer tells the author's text from plain drafts of the same content?

The drafts (eval inputs, system b2) carry the author's facts and names in a generic voice.
A scorer that leans on content accepts them. No scorer here has trained on any draft.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ..scorers import av, embed
from . import harness, inputs

KEEP_SIZES = (200, 500, 1000, 3000)


def scorers(ctx, keep_sizes=KEEP_SIZES, kinds=("style", "luar")) -> dict:
    """name -> function(texts) -> scores, higher = more like the author. All fitted on train."""
    cache = Path(ctx.cfg["paths"]["eval"]) / "cache"
    human = [p["text"] for p in ctx.imp if p["part"] == "train" and p["kind"] == "human"]
    neg = ctx.neg[:ctx.n_imp_neg]                 # impostors only: this check is about scorers that saw no draft
    y = np.r_[np.ones(len(ctx.pos)), np.zeros(len(neg))]
    raw = av._pipe().fit(np.array(ctx.pos + neg, dtype=object), y)
    out = {"M1 char n-grams, raw": lambda t: raw.predict_proba(np.array(t, dtype=object))[:, 1]}
    for k in keep_sizes:
        keep = av.frequent_words(human, k)
        m = av._pipe(keep).fit(np.array(ctx.pos + neg, dtype=object), y)
        out[f"M1 masked, keep {k}"] = lambda t, m=m: m.predict_proba(np.array(t, dtype=object))[:, 1]
    llm = [p["text"] for p in ctx.imp if p["kind"] == "llm"]
    for kind, label in (("style", "M2 StyleDistance"), ("luar", "M3 LUAR")):
        if kind not in kinds:
            continue
        enc = lambda t, kind=kind: embed.encode(t, kind, cache)
        Ep, En = enc(ctx.pos), enc(neg)
        clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000, class_weight="balanced"))
        clf.fit(np.vstack([Ep, En]), y)
        ca, cl = embed.centroid(Ep), embed.centroid(enc(llm))
        out[f"{label}, classifier"] = lambda t, clf=clf, enc=enc: clf.predict_proba(enc(t))[:, 1]
        out[f"{label}, centroid delta"] = lambda t, enc=enc, ca=ca, cl=cl: enc(t) @ ca - enc(t) @ cl
    return out


def run(cfg: dict, part: str = "dev", ctx=None, systems=("b0", "b1"), write: bool = True, **kw) -> dict:
    ctx = ctx or harness.Context(cfg)
    rows = inputs.load(cfg, part)
    text = {c["id"]: c["text"] for c in ctx.chunks}
    orig, o_g = harness._segs([text[r["id"]] for r in rows], [r["id"] for r in rows])
    draft, d_g = harness._segs([r["draft"] for r in rows], [r["id"] for r in rows])
    imp, _ = harness._segs(*zip(*[(p["text"], p["group"]) for p in ctx.imp if p["part"] == part and p["kind"] == "human"]))
    sys_segs = {}
    for s in systems:
        f = Path(cfg["paths"]["eval"]) / "outputs" / s / f"{part}.jsonl"
        if f.exists():
            it = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
            sys_segs[s] = harness._segs([i["text"] for i in it], [i["id"] for i in it])[0]
    res = {}
    for name, fn in scorers(ctx, **kw).items():
        so, sd, si = fn(orig), fn(draft), fn(imp)
        thr = float(np.quantile(si, 0.95))
        mo = {g: np.mean([x for x, k in zip(so, o_g) if k == g]) for g in set(o_g)}
        md = {g: np.mean([x for x, k in zip(sd, d_g) if k == g]) for g in set(d_g)}
        res[name] = dict(
            auc_impostor=round(harness._auc(so, si), 4), auc_draft=round(harness._auc(so, sd), 4),
            paired_win=round(float(np.mean([mo[g] > md[g] for g in mo])), 4),
            accept_author=round(float((so >= thr).mean()), 4), accept_draft=round(float((sd >= thr).mean()), 4),
            **{f"accept_{s}": round(float((fn(t) >= thr).mean()), 4) for s, t in sys_segs.items()})
    rep = dict(system="verifier-check", split=part, generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
               passages=dict(author=len(orig), draft=len(draft), impostor=len(imp)), scorers=res)
    if write:
        d = harness.REPO / "eval_reports"
        (d / f"verifier-check-{part}.json").write_text(json.dumps(rep, indent=1))
        sy = list(sys_segs)
        L = [f"# Verifier check on {part} ({rep['generated']})", "",
             "Can each style scorer tell the author's held-out text from plain drafts of the same content? "
             "No scorer has trained on a draft. Accept rates use the threshold that passes 5% of the "
             f"{part} impostor passages. Paired: share of chunks where the original outscores its own draft.", "",
             "| Scorer | AUC vs impostors | AUC vs drafts | Paired | Accept: author | drafts | " + " | ".join(sy) + " |",
             "|---|---|---|---|---|---|" + "---|" * len(sy)]
        L += [f"| {n} | {r['auc_impostor']:.3f} | {r['auc_draft']:.3f} | {r['paired_win']:.1%} | {r['accept_author']:.1%} | "
              f"{r['accept_draft']:.1%} | " + " | ".join(f"{r[f'accept_{s}']:.1%}" for s in sy) + " |" for n, r in res.items()]
        (d / f"verifier-check-{part}.md").write_text("\n".join(L) + "\n")
        rep["_out"] = str(d / f"verifier-check-{part}.md")
    return rep


def with_drafts(cfg: dict, part: str = "dev", ctx=None, systems=("b0", "b1"), folds: int = 4, mass: float = 900.0,
                write: bool = True) -> dict:
    """Estimate what draft negatives buy, before any train drafts exist: add the drafts of some
    dev posts to the verifier's negatives and score the other dev posts. Grouped by post. The
    few drafts are weighted up to `mass` passages, about what the train split would give."""
    from sklearn.model_selection import GroupKFold

    ctx = ctx or harness.Context(cfg)
    cache = Path(cfg["paths"]["eval"]) / "cache"
    rows = inputs.load(cfg, part)
    text = {c["id"]: c["text"] for c in ctx.chunks}
    post = {r["id"]: r["post"] for r in rows}
    sets = {"author": harness._segs([text[r["id"]] for r in rows], [r["id"] for r in rows]),
            "draft": harness._segs([r["draft"] for r in rows], [r["id"] for r in rows])}
    for s in systems:
        f = Path(cfg["paths"]["eval"]) / "outputs" / s / f"{part}.jsonl"
        if f.exists():
            it = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
            sets[s] = harness._segs([i["text"] for i in it], [i["id"] for i in it])
    imp, _ = harness._segs(*zip(*[(p["text"], p["group"]) for p in ctx.imp if p["part"] == part and p["kind"] == "human"]))
    human = [p["text"] for p in ctx.imp if p["part"] == "train" and p["kind"] == "human"]
    feats = {"M1 char n-grams, raw": None, "M1 masked, keep 1000": av.frequent_words(human, 1000),
             "M2 StyleDistance, classifier": "style", "M3 LUAR, classifier": "luar"}
    posts = sorted(set(post.values()))
    res = {}
    for name, f in feats.items():
        emb = isinstance(f, str)
        X = (lambda t: embed.encode(list(t), f, cache)) if emb else (lambda t: np.array(list(t), dtype=object))
        acc = {k: [] for k in sets}
        for tr, te in GroupKFold(folds).split(posts, groups=posts):
            trp, tep = {posts[i] for i in tr}, {posts[i] for i in te}
            dr = [t for t, g in zip(*sets["draft"]) if post[g] in trp]
            neg = ctx.neg[:ctx.n_imp_neg]
            texts = ctx.pos + neg + dr
            y = np.r_[np.ones(len(ctx.pos)), np.zeros(len(neg) + len(dr))]
            w = np.r_[np.ones(len(ctx.pos) + len(neg)), np.full(len(dr), mass / len(dr))]
            w[y == 1] *= w[y == 0].sum() / w[y == 1].sum()          # balance the two classes
            m = (make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000)) if emb else av._pipe(f))
            m.fit(X(texts), y, logisticregression__sample_weight=w)
            thr = float(np.quantile(m.predict_proba(X(imp))[:, 1], 0.95))
            for k, (segs, gs) in sets.items():
                held = [t for t, g in zip(segs, gs) if post[g] in tep]
                acc[k] += list(m.predict_proba(X(held))[:, 1] >= thr)
        res[name] = {f"accept_{k}": round(float(np.mean(v)), 4) for k, v in acc.items()}
    rep = dict(system="verifier-check-with-drafts", split=part, folds=folds, draft_mass=mass,
               generated=time.strftime("%Y-%m-%dT%H:%M:%S"), scorers=res)
    if write:
        d = harness.REPO / "eval_reports"
        (d / f"verifier-check-drafts-{part}.json").write_text(json.dumps(rep, indent=1))
        ks = list(sets)
        L = [f"# Verifier check with draft negatives, {part} ({rep['generated']})", "",
             f"Drafts of some {part} posts join the negatives; the other posts are scored ({folds} folds by post). "
             f"Accept rates use the threshold that passes 5% of the {part} impostor passages. An estimate: the real "
             "fix trains on drafts of train chunks.", "",
             "| Scorer | " + " | ".join(f"Accept: {k}" for k in ks) + " |", "|---|" + "---|" * len(ks)]
        L += [f"| {n} | " + " | ".join(f"{r[f'accept_{k}']:.1%}" for k in ks) + " |" for n, r in res.items()]
        (d / f"verifier-check-drafts-{part}.md").write_text("\n".join(L) + "\n")
    return rep


def detector(cfg: dict, part: str = "dev", ctx=None, systems=("b0", "b1", "b2"), n_train: int = 300) -> dict:
    """M10 sanity: Fast-DetectGPT must tell machine text from the author's held-out text (AUC >= 0.80).
    The flag threshold passes 5% of a sample of the author's train passages."""
    import random

    from ..scorers.detect import FastDetect

    ctx = ctx or harness.Context(cfg, use_embeddings=False)
    det = FastDetect(Path(cfg["paths"]["eval"]) / "cache")
    tr = list(ctx.pos)
    random.Random(0).shuffle(tr)
    thr = float(np.quantile(det.score(tr[:n_train]), 0.95))
    hum = [c["text"] for c in ctx.chunks if c["split"] == part]
    sh = np.array(det.score(harness._segs(hum, hum)[0]))
    sets = {}
    for s in systems:
        f = Path(cfg["paths"]["eval"]) / "outputs" / s / f"{part}.jsonl"
        if f.exists():
            t = [json.loads(x)["text"] for x in f.read_text().splitlines() if x.strip()]
            sets[s] = harness._segs(t, t)[0]
    llm = [p["text"] for p in ctx.imp if p["kind"] == "llm"]
    sets["Claude controls (older model)"] = harness._segs(llm, llm)[0]
    imp = [p["text"] for p in ctx.imp if p["part"] == part and p["kind"] == "human"]
    sets["other human authors"] = harness._segs(imp, imp)[0]
    res = {"author, held out": dict(n=len(sh), mean=round(float(sh.mean()), 3), flagged=round(float((sh >= thr).mean()), 4), auc=None)}
    for k, v in sets.items():
        s = np.array(det.score(v))
        res[k] = dict(n=len(s), mean=round(float(s.mean()), 3), flagged=round(float((s >= thr).mean()), 4),
                      auc=round(harness._auc(s, sh), 4))
    ok = all(res[s]["auc"] >= 0.80 for s in systems if s in res)
    rep = dict(system="m10-fast-detectgpt", split=part, generated=time.strftime("%Y-%m-%dT%H:%M:%S"), model="gpt-neo-2.7B",
               threshold=round(thr, 4), sets=res, **{"pass": ok})
    d = harness.REPO / "eval_reports"
    (d / f"m10-{part}.json").write_text(json.dumps(rep, indent=1))
    L = [f"# M10 Fast-DetectGPT on {part} ({rep['generated']})", "",
         "Analytic Fast-DetectGPT with gpt-neo-2.7B. Higher scores read as machine text. The flag threshold passes 5% of "
         "the author's train passages. AUC: each set against the author's held-out passages; the bar for machine text is 0.80.", "",
         "| Set | Passages | Mean score | Flagged | AUC vs author |", "|---|---|---|---|---|"]
    L += [f"| {k} | {r['n']} | {r['mean']} | {r['flagged']:.1%} | {'' if r['auc'] is None else r['auc']} |" for k, r in res.items()]
    L += ["", "Passes." if ok else "FAILS: it cannot tell current Claude or local-model output from the author. Dropped until "
          "Phase 2b decides on a trained detector (M10b)."]
    (d / f"m10-{part}.md").write_text("\n".join(L) + "\n")
    rep["_out"] = str(d / f"m10-{part}.md")
    return rep
