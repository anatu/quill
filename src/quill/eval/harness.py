"""Eval harness (plan.md Phase 2): fit the scorers on train, score a system on dev or test.

A system is a set of texts. Built-in systems need no generation:
  human     the author's own held-out chunks (the ceiling)
  impostor  held-out passages by the impostor authors (the floor)
  llm       the Claude control passages
Any other name is read from <paths.eval>/outputs/<name>/<split>.jsonl, one row per output:
  {"id": chunk id, "op": "restyle" | "write", "text": ..., "input": ..., "length_words": ...}

Reports hold aggregate numbers only, never corpus text.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from ..corpus import split, store
from ..scorers import av, embed, entities, meaning, memo, stylometry
from ..scorers.lexicon import Lexicon
from . import pool

REPO = Path(__file__).resolve().parents[3]
BUILTIN = ("human", "impostor", "llm")
NOT_IMPLEMENTED = ["M13 alpha", "M14 residue (both Phase 2b)"]
DROPPED = ["M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md)"]


def _segs(texts: list[str], groups: list[str]) -> tuple[list[str], list[str]]:
    out, g = [], []
    for t, k in zip(texts, groups):
        s = pool.segments(t)
        out += s
        g += [k] * len(s)
    return out, g


class Context:
    """Everything fitted on train. Nothing here has seen dev or test text, except the
    memorization index, which must hold the whole corpus."""

    def __init__(self, cfg: dict, use_embeddings: bool = True):
        self.cfg = cfg
        self.use_embeddings = use_embeddings
        self.chunks = pool.author_chunks(cfg)
        self.imp = pool.impostors(cfg)
        tr = [c for c in self.chunks if c["split"] == "train"]
        self.train_texts = [c["text"] for c in tr]
        pos, pos_g = _segs(self.train_texts, [c["post"] for c in tr])
        itr = [p for p in self.imp if p["part"] == "train"]
        neg, neg_g = _segs([p["text"] for p in itr], [p["group"] for p in itr])
        # Plain drafts of train chunks: the author's content in a generic voice. Without them the
        # verifier accepts a third of such drafts (eval_reports/verifier-check-dev.md). A draft shares
        # its post's group, so it and its original land in one CV fold.
        from . import inputs

        dr = inputs.train_drafts(cfg)
        self.drafts, self.drafts_g = _segs([r["draft"] for r in dr], [r["post"] for r in dr])
        self.n_imp_neg = len(neg)
        neg, neg_g = neg + self.drafts, neg_g + self.drafts_g
        self.verifier = av.Verifier().fit(pos, pos_g, neg, neg_g)

        lab_t, lab_y = list(pos), ["author"] * len(pos)
        for p in itr:
            s = pool.segments(p["text"])
            lab_t += s
            lab_y += [pool.m15_class(p)] * len(s)
        lab_t += self.drafts
        lab_y += ["llm"] * len(self.drafts)
        self.attributor = av.Attributor().fit(lab_t, lab_y)

        info = json.loads((split.split_dir(cfg) / "clusters.json").read_text())
        self.tics = stylometry.TicProfile().fit(self.train_texts, [info["post_cluster"].get(c["post"]) for c in tr])
        basis = Path(cfg["paths"]["baseline"]).parent / "delta_basis.json"
        if basis.exists():
            self.delta = stylometry.Delta.load(basis)
        else:
            by = {"author": self.train_texts}
            for p in itr:
                by.setdefault(p["author"], []).append(p["text"])
            self.delta = stylometry.Delta.build(by)
        self.delta.fit(self.train_texts)

        self.signature = memo.Signature().fit(self.train_texts, [p["text"] for p in itr if p["kind"] == "human"])
        self.memo = memo.Memo(n=int(cfg.get("eval", {}).get("memo_ngram", 8)))
        db = store.connect(store.db_path(cfg))
        self.post_text = {}
        for r in db.execute("SELECT file, text FROM posts"):
            self.memo.add(r["text"])
            self.post_text[r["file"]] = r["text"]
        self.post_of = {c["id"]: c["post"] for c in self.chunks}
        for r in db.execute("SELECT text FROM dropped_blocks WHERE reason = 'duplicate_paragraph'"):
            self.memo.add(r["text"])
        db.close()
        entities.set_common(self.train_texts + [p["text"] for p in itr])
        self.lexicon = Lexicon.load(Path(cfg["paths"]["lexicon"]) / "v0.json")
        self.cache = Path(cfg["paths"]["eval"]) / "cache"
        self.mis, self.fact_nli = meaning.MIS(self.cache), meaning.Facts(self.cache)
        self.facts = {}
        for part in ("dev", "test"):
            f = inputs.inputs_dir(cfg) / f"{part}.jsonl"
            if f.exists():
                self.facts.update({r["id"]: r["facts"] for r in inputs.load(cfg, part)})

        self.pos, self.neg = pos, neg
        self.axes = ("m1", "m15", "m4") if self.m15_sanity()["pass"] else ("m1", "m4")   # a failing metric is dropped
        self.pos_g = pos_g
        if use_embeddings:
            cache = Path(cfg["paths"]["eval"]) / "cache"
            self.E_pos = embed.encode(pos, "style", cache)
            self.E_neg = embed.encode(neg, "style", cache)
            llm = [p["text"] for p in self.imp if p["kind"] == "llm"] + self.drafts
            self.c_author = embed.centroid(self.E_pos)
            self.c_llm = embed.centroid(embed.encode(llm, "style", cache))
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler

            self.emb_clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000,
                                                                              class_weight="balanced"))
            Xe, ye = np.vstack([self.E_pos, self.E_neg]), np.r_[np.ones(len(pos)), np.zeros(len(neg))]
            from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict

            oof = cross_val_predict(self.emb_clf, Xe, ye, groups=np.array(pos_g + neg_g), method="predict_proba",
                                    cv=StratifiedGroupKFold(5, shuffle=True, random_state=0))[:, 1]
            self.emb_threshold = float(np.quantile(oof[ye == 0], 0.95))     # same rule as M1: 5% false accepts
            self.emb_clf.fit(Xe, ye)

    # ---- systems
    def items(self, system: str, part: str) -> list[dict]:
        if system == "human":
            return [dict(id=c["id"], text=c["text"]) for c in self.chunks if c["split"] == part]
        if system == "impostor":
            return [dict(id=p["group"], text=p["text"], author=p["author"]) for p in self.imp
                    if p["part"] == part and p["kind"] == "human"]
        if system == "llm":
            return [dict(id=p["group"], text=p["text"], author=p["author"]) for p in self.imp if p["kind"] == "llm"]
        f = Path(self.cfg["paths"]["eval"]) / "outputs" / system / f"{part}.jsonl"
        if not f.exists():
            raise SystemExit(f"no outputs for system '{system}': expected {f}")
        return [json.loads(line) for line in f.read_text().splitlines() if line.strip()]

    def style_delta(self, texts: list[str]) -> np.ndarray:
        E = embed.encode(texts, "style", Path(self.cfg["paths"]["eval"]) / "cache")
        return E @ self.c_author - E @ self.c_llm

    def spans(self, text: str, given: str, chunk_id: str | None) -> tuple[int, int]:
        """Longest verbatim span, in words, that the input did not supply: (a) shared with the corpus
        outside the target's own post: memorization; (b) shared with the target's post: the output
        rebuilt the held-out original. (b) is a diagnostic: content and voice force some of it."""
        target = self.post_text.get(self.post_of.get(chunk_id, ""), "")
        other = self.memo.longest(text, given + "\n\n" + target)["span"]
        if not target:
            return other, 0
        m = memo.Memo(n=self.memo.n)
        m.add(target)
        return other, m.longest(text, given)["span"]

    def m15_sanity(self, part: str = "dev") -> dict:
        """M15 passes when it gives the author's held-out text to the author and no other class's
        held-out text to the author on over 20% of passages."""
        hum = [c["text"] for c in self.chunks if c["split"] == part]
        hs, _ = _segs(hum, hum)
        held = [p for p in self.imp if p["part"] == part]
        pred = self.attributor.predict(hs)
        m15 = {"author_share_on_author": round(pred.count("author") / len(pred), 4)}
        for cls in self.attributor.classes:
            t = [x for p in held if pool.m15_class(p) == cls for x in pool.segments(p["text"])]
            if cls == "author" or not t:
                continue
            pr = self.attributor.predict(t)
            m15[f"{cls}_recall"] = round(pr.count(cls) / len(pr), 3)
            m15[f"{cls}_called_author"] = round(pr.count("author") / len(pr), 3)
            m15[f"{cls}_n"] = len(t)
        leaks = {k[:-len("_called_author")]: v for k, v in m15.items() if k.endswith("_called_author") and v > 0.20}
        m15["classes_called_author_over_20pct"] = sorted(leaks)
        m15["pass"] = m15["author_share_on_author"] >= 0.80 and not leaks
        return m15

    def meaning_and_composite(self, items: list[dict], segs: list[str], owner: list[int], p: np.ndarray) -> dict:
        """M4 per output, and the decision composite. M4 is MIS against the input for `restyle`
        and the share of the chunk's facts entailed for `write`."""
        pred = self.attributor.predict(segs)
        acc = p >= self.verifier.threshold
        rs = [k for k, i in enumerate(items) if i.get("op") == "restyle" and i.get("input")]
        mis = dict(zip(rs, self.mis.score([items[k]["input"] for k in rs], [items[k]["text"] for k in rs])))
        fk = [k for k, i in enumerate(items) if i.get("id") in self.facts]
        fs = dict(zip(fk, self.fact_nli.score([self.facts[items[k]["id"]] for k in fk], [items[k]["text"] for k in fk])))
        rows = []
        for k, i in enumerate(items):
            if not i.get("input"):
                continue
            mine = [j for j, o in enumerate(owner) if o == k]
            m4 = mis.get(k) if i.get("op") == "restyle" else fs.get(k)
            rows.append(dict(id=i["id"], op=i.get("op"), gate=bool(entities.compare(i["input"], i["text"])["ok"]),
                             m1=float(np.mean(acc[mine])), m15=float(np.mean([pred[j] == "author" for j in mine])),
                             m4=float(m4) if m4 is not None else 0.0, mis=mis.get(k), facts=fs.get(k)))
        self.last_rows = rows
        out = {"M4_meaning": dict(
            mis_restyle=dict(mean=round(float(np.mean(list(mis.values()))), 4), median=round(float(np.median(list(mis.values()))), 4),
                             n=len(mis)) if mis else None,
            facts_entailed={op: round(float(np.mean([fs[k] for k in fk if items[k].get("op") == op])), 4)
                            for op in sorted({items[k].get("op") for k in fk if items[k].get("op")})},
            m4=round(float(np.mean([r["m4"] for r in rows])), 4))}
        axes = self.axes
        out["composite"] = dict(axes=list(axes), **bootstrap(rows, axes=axes),
                                axis_means={a: round(float(np.mean([r[a] for r in rows])), 4) for a in axes},
                                gate_pass=round(float(np.mean([r["gate"] for r in rows])), 4))
        return out

    # ---- scoring
    def score(self, items: list[dict], held_out: list[str]) -> dict:
        """held_out: the author's own held-out texts, the reference for rate ratios."""
        texts = [i["text"] for i in items]
        segs, _ = _segs(texts, [i["id"] for i in items])
        p = self.verifier.prob(segs)
        out = {
            "n_items": len(items), "n_passages": len(segs), "words": sum(len(t.split()) for t in texts),
            "M1_av": dict(accept_rate=round(float((p >= self.verifier.threshold).mean()), 4),
                          mean_prob=round(float(p.mean()), 4)),
            "M15_attribution": {k: round(v, 4) for k, v in self.attributor.shares(segs).items()},
            "M6_tic_profile": self.tics.score(texts),
            "M6_delta": self.delta.score(texts),
        }
        if self.use_embeddings:
            d = self.style_delta(segs)
            out["M2_styledistance_delta"] = dict(mean=round(float(d.mean()), 4), sd=round(float(d.std()), 4))
            pe = self.emb_clf.predict_proba(embed.encode(segs, "style", Path(self.cfg["paths"]["eval"]) / "cache"))[:, 1]
            out["M2_classifier"] = dict(accept_rate=round(float((pe >= self.emb_threshold).mean()), 4))
        ref = self.lexicon.score("\n\n".join(held_out))["rates"]
        got = self.lexicon.score("\n\n".join(texts))
        out["M7_lexicon"] = {f: dict(per_1k=round(got["rates"][f], 3), author_per_1k=round(ref[f], 3),
                                     ratio=round(got["rates"][f] / ref[f], 2) if ref[f] else None)
                             for f in ("vocabulary", "structure")}
        out["M7_lexicon"]["artifacts"] = dict(hits=got["hits"]["artifacts"])
        sig_ref = self.signature.rate(held_out)
        sig = self.signature.rate(texts)
        out["M8_signature"] = dict(per_1k=round(sig, 3), author_per_1k=round(sig_ref, 3),
                                   ratio=round(sig / sig_ref, 2) if sig_ref else None)
        with_input = [i for i in items if i.get("input")]
        if with_input:
            sp = [self.spans(i["text"], i["input"], i.get("id")) for i in with_input]
            spans, tgt = [a for a, _ in sp], sorted(b for _, b in sp)
            ent = [entities.compare(i["input"], i["text"]) for i in with_input]
            out["M9_memorization"] = dict(max_span=max(spans), flagged=sum(1 for s in spans if s >= self.memo.n),
                                          n=len(spans), target_rebuilt=dict(
                                              max_span=tgt[-1], median_span=tgt[len(tgt) // 2],
                                              at_or_over_gate=sum(1 for s in tgt if s >= self.memo.n)))
            out["M5_entities"] = dict(pass_rate=round(sum(e["ok"] for e in ent) / len(ent), 4), n=len(ent),
                                      missing=sum(1 for e in ent if e["missing"]),
                                      added=sum(1 for e in ent if e["added"]))
        if with_input and self.use_embeddings:
            out.update(self.meaning_and_composite(items, segs, _segs(texts, list(range(len(items))))[1], p))
        if any("fallback" in i for i in items):
            out["fallback_rate"] = round(sum(bool(i.get("fallback")) for i in items) / len(items), 4)
        ops = sorted({i["op"] for i in items if i.get("op")})
        if len(ops) > 1:                # M1 by operation: restyle and write differ in how much the input helps
            out["M1_by_op"] = {}
            for op in ops:
                sg, _ = _segs([i["text"] for i in items if i["op"] == op], [i["id"] for i in items if i["op"] == op])
                out["M1_by_op"][op] = round(float(self.verifier.accept(sg).mean()), 4)
        with_len = [i for i in items if i.get("length_words")]
        if with_len:
            ok = [abs(len(i["text"].split()) - i["length_words"]) <= 0.3 * i["length_words"] for i in with_len]
            out["M12_length"] = dict(within_30pct=round(sum(ok) / len(ok), 4), n=len(ok))
        return out


def composite(rows: list[dict], axes=("m1", "m15", "m4")) -> float:
    """Geometric mean of the axis means, with the entity gate applied first: an output that
    fails the gate scores 0 on every axis."""
    if not rows:
        return 0.0
    v = [np.mean([r[a] if r["gate"] else 0.0 for r in rows]) for a in axes]
    return float(np.prod(v) ** (1 / len(v)))


def bootstrap(rows_a: list[dict], rows_b: list[dict] | None = None, n: int = 2000, seed: int = 0, axes=("m1", "m15", "m4")) -> dict:
    """Composite with a 95% CI, resampling chunks (both operations of a chunk move together).
    With rows_b: the paired difference a - b on the chunks both systems scored."""
    by_a, by_b = {}, {}
    for r in rows_a:
        by_a.setdefault(r["id"], []).append(r)
    for r in rows_b or []:
        by_b.setdefault(r["id"], []).append(r)
    ids = sorted(set(by_a) & set(by_b)) if rows_b is not None else sorted(by_a)
    rng = np.random.default_rng(seed)
    f = lambda by, pick: composite([r for i in pick for r in by[i]], axes)
    full = f(by_a, ids) - (f(by_b, ids) if rows_b is not None else 0.0)
    draws = []
    for _ in range(n):
        pick = [ids[i] for i in rng.integers(0, len(ids), len(ids))]
        draws.append(f(by_a, pick) - (f(by_b, pick) if rows_b is not None else 0.0))
    lo, hi = np.quantile(draws, [0.025, 0.975])
    return dict(value=round(full, 4), ci95=[round(float(lo), 4), round(float(hi), 4)], chunks=len(ids))


def item_scores_file(cfg: dict, system: str, part: str) -> Path:
    return Path(cfg["paths"]["eval"]) / "scores" / f"{system}-{part}.json"


def compare(cfg: dict, a: str, b: str, part: str = "dev") -> dict:
    """Paired bootstrap of the composite difference a - b, from saved per-item scores."""
    ra, rb = (json.loads(item_scores_file(cfg, x, part).read_text()) for x in (a, b))
    return dict(a=a, b=b, split=part, axes=ra["axes"], diff=bootstrap(ra["rows"], rb["rows"], axes=tuple(ra["axes"])))


def _auc(pos: np.ndarray, neg: np.ndarray) -> float:
    from sklearn.metrics import roc_auc_score

    return float(roc_auc_score(np.r_[np.ones(len(pos)), np.zeros(len(neg))], np.r_[pos, neg]))


def auc_cv(EX, gX, ER, gR, n: int, repeats: int, seed: int = 0) -> tuple[float, float, int]:
    """Cross-validated AUC of a logistic regression telling two embedding sets apart, on n
    matched passages per class. Same method as the 2026-11-08 similarity pass."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedGroupKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    rng = np.random.default_rng(seed)
    n = min(n, len(EX), len(ER))
    out = []
    for _ in range(repeats):
        ix, ir = rng.choice(len(EX), n, replace=False), rng.choice(len(ER), n, replace=False)
        X = np.vstack([EX[ix], ER[ir]])
        y = np.r_[np.ones(n), np.zeros(n)]
        g = np.array(["x:" + str(gX[i]) for i in ix] + ["r:" + str(gR[i]) for i in ir])
        k = min(5, len(set(g[:n])), len(set(g[n:])))
        if k < 2:
            continue
        pred = np.zeros(len(y))
        for tr, te in StratifiedGroupKFold(n_splits=k, shuffle=True, random_state=int(rng.integers(1e9))).split(X, y, g):
            clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000))
            pred[te] = clf.fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
        out.append(roc_auc_score(y, pred))
    return (float(np.mean(out)), float(np.std(out)), n) if out else (float("nan"), float("nan"), n)


def ceiling(ctx: Context) -> dict:
    """Within-author ceiling on topic-disjoint halves: can a classifier tell one half of the
    author's topics from the other? Uses train and dev chunks only; test stays untouched."""
    info = json.loads((split.split_dir(ctx.cfg) / "clusters.json").read_text())
    held = set(info["test_clusters"])
    cw = {int(c): w for c, w in info["cluster_words"].items() if int(c) not in held}
    half, wa, wb = {}, 0, 0
    for c in sorted(cw, key=lambda c: -cw[c]):          # greedy balance by words
        if wa <= wb:
            half[c], wa = "A", wa + cw[c]
        else:
            half[c], wb = "B", wb + cw[c]
    A = [c for c in ctx.chunks if c["split"] != "test" and half.get(info["post_cluster"].get(c["post"])) == "A"]
    B = [c for c in ctx.chunks if c["split"] != "test" and half.get(info["post_cluster"].get(c["post"])) == "B"]
    out = dict(clusters_A=sorted(c for c, h in half.items() if h == "A"),
               clusters_B=sorted(c for c, h in half.items() if h == "B"),
               words_A=sum(c["words"] for c in A), words_B=sum(c["words"] for c in B))
    d = stylometry.Delta(dict(mfw=ctx.delta.mfw, mu=ctx.delta.mu, sd=ctx.delta.sd)).fit([c["text"] for c in B])
    out["delta_A_vs_B"] = d.score([c["text"] for c in A])
    if ctx.use_embeddings:
        cache = Path(ctx.cfg["paths"]["eval"]) / "cache"
        sa, ga = _segs([c["text"] for c in A], [c["post"] for c in A])
        sb, gb = _segs([c["text"] for c in B], [c["post"] for c in B])
        EA, EB = embed.encode(sa, "style", cache), embed.encode(sb, "style", cache)
        for n, reps in ((20, 20), (60, 10)):
            m, s, k = auc_cv(EA, ga, EB, gb, n, reps)
            out[f"styledistance_auc_n{n}"] = dict(auc=round(m, 3), sd=round(s, 3), n_per_class=k)
    return out


def sanity(ctx: Context, part: str = "dev") -> dict:
    """Each style metric must rank the author's held-out text above same-register impostor text."""
    hum = [c["text"] for c in ctx.chunks if c["split"] == part]
    hs, _ = _segs(hum, hum)
    imp = [p for p in ctx.imp if p["part"] == part and p["kind"] == "human"]
    isg, ig = _segs([p["text"] for p in imp], [p["author"] for p in imp])
    held_llm = [p["text"] for p in ctx.imp if p["kind"] == "llm" and p["part"] != "train"]
    llm, _ = _segs(held_llm, held_llm)
    ph, pi = ctx.verifier.prob(hs), ctx.verifier.prob(isg)
    out = {
        "part": part, "author_passages": len(hs), "impostor_passages": len(isg), "llm_passages": len(llm),
        "M1": dict(auc=round(_auc(ph, pi), 4), threshold=round(ctx.verifier.threshold, 4),
                   ceiling_accept=round(float((ph >= ctx.verifier.threshold).mean()), 4),
                   impostor_accept=round(float((pi >= ctx.verifier.threshold).mean()), 4),
                   llm_accept=round(float(ctx.verifier.accept(llm).mean()), 4) if llm else None,
                   impostor_accept_by_author={a: round(float(np.mean([x >= ctx.verifier.threshold
                                                                      for x, g in zip(pi, ig) if g == a])), 3)
                                              for a in sorted(set(ig))}),
    }
    out["M1"]["negatives"] = dict(impostor_passages=ctx.n_imp_neg, draft_passages=len(ctx.drafts))
    out["M1"]["pass"] = out["M1"]["auc"] >= 0.90
    m15 = ctx.m15_sanity(part)
    out["M15"] = m15
    if ctx.use_embeddings:
        cache = Path(ctx.cfg["paths"]["eval"]) / "cache"
        EH, EI = embed.encode(hs, "style", cache), embed.encode(isg, "style", cache)
        a = _auc(ctx.emb_clf.predict_proba(EH)[:, 1], ctx.emb_clf.predict_proba(EI)[:, 1])
        b = _auc(EH @ ctx.c_author - EH @ ctx.c_llm, EI @ ctx.c_author - EI @ ctx.c_llm)
        out["M2"] = dict(classifier_auc=round(a, 4), centroid_delta_auc=round(b, 4), **{"pass": a >= 0.80})
    tic = ctx.tics.score(hum)
    out["M6"] = dict(author_max_abs_z=tic.get("max_abs_z"), n_pools=tic["n_pools"],
                     author_delta=ctx.delta.score(hum),
                     impostor_delta=ctx.delta.score([p["text"] for p in imp]))
    out["M6"]["pass"] = tic.get("max_abs_z") is not None and tic["max_abs_z"] <= 2
    sig_h, sig_i = ctx.signature.rate(hum), ctx.signature.rate([p["text"] for p in imp])
    out["M8"] = dict(author_per_1k=round(sig_h, 3), impostor_per_1k=round(sig_i, 3), **{"pass": sig_h > sig_i})
    return out


def run(cfg: dict, system: str, part: str, use_embeddings: bool = True, name: str | None = None) -> dict:
    ctx = Context(cfg, use_embeddings)
    held = [c["text"] for c in ctx.chunks if c["split"] == part]
    rep = dict(system=system, split=part, generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
               split_hash=split.refresh(cfg)["hash"], scores=ctx.score(ctx.items(system, part), held),
               not_implemented=NOT_IMPLEMENTED, dropped=DROPPED)
    if getattr(ctx, "last_rows", None) and name is None:
        f = item_scores_file(cfg, system, part)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(dict(system=system, split=part, axes=list(ctx.axes), rows=ctx.last_rows)))
    return write_report(rep, name or f"{system}-{part}")


def run_sanity(cfg: dict, use_embeddings: bool = True) -> dict:
    ctx = Context(cfg, use_embeddings)
    held = [c["text"] for c in ctx.chunks if c["split"] == "dev"]
    rep = dict(system="sanity", split="dev", generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
               split_hash=split.refresh(cfg)["hash"], sanity=sanity(ctx), ceiling=ceiling(ctx),
               systems={s: ctx.score(ctx.items(s, "dev"), held) for s in BUILTIN},
               signature_phrases=len(ctx.signature.phrases), not_implemented=NOT_IMPLEMENTED, dropped=DROPPED)
    return write_report(rep, "phase2-sanity")


def write_report(rep: dict, name: str) -> dict:
    d = REPO / "eval_reports"
    d.mkdir(exist_ok=True)
    (d / f"{name}.json").write_text(json.dumps(rep, indent=1))
    (d / f"{name}.md").write_text(render(rep))
    rep["_out"] = str(d / f"{name}.md")
    return rep


def _row(name: str, s: dict) -> str:
    t = s["M6_tic_profile"]
    sd = s.get("M2_styledistance_delta", {}).get("mean", "")
    m2 = s.get("M2_classifier", {}).get("accept_rate")
    return (f"| {name} | {s['n_passages']} | {s['M1_av']['accept_rate']:.1%} | {'' if m2 is None else format(m2, '.1%')} | "
            f"{s['M15_attribution'].get('author', 0):.1%} | {s['M15_attribution'].get('llm', 0):.1%} | "
            f"{t.get('max_abs_z', '')} | {s['M6_delta'].get('delta', '')} | {sd} | "
            f"{s['M7_lexicon']['vocabulary']['ratio']} | {s['M7_lexicon']['structure']['ratio']} | "
            f"{s['M8_signature']['ratio']} |")


HEAD = ("| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \\|z\\| | Delta | M2 delta | "
        "M7 vocab × | M7 struct × | M8 × |\n|---|---|---|---|---|---|---|---|---|---|---|---|")


def render(rep: dict) -> str:
    L = [f"# Eval: {rep['system']} on {rep['split']} ({rep['generated']})", "",
         f"Split hash `{rep['split_hash'][:12]}`. Ratios (×) are against the author's held-out rate.", ""]
    if "sanity" in rep:
        s, c = rep["sanity"], rep["ceiling"]
        L += ["## Metric sanity (dev)", "", "| Metric | Result | Bar | Pass |", "|---|---|---|---|",
              f"| M1 AV AUC, author vs impostors | {s['M1']['auc']} | ≥ 0.90 | {s['M1']['pass']} |",
              f"| M15 author share on author text; other classes called author | {s['M15']['author_share_on_author']}; "
              f"over 20%: {s['M15']['classes_called_author_over_20pct'] or 'none'} | ≥ 0.80; none [P] | {s['M15']['pass']} |"]
        if "M2" in s:
            L.append(f"| M2 StyleDistance classifier AUC | {s['M2']['classifier_auc']} | ≥ 0.80 | {s['M2']['pass']} |")
        L += [f"| M6 tic profile, author max \\|z\\| | {s['M6']['author_max_abs_z']} | ≤ 2 | {s['M6']['pass']} |",
              f"| M8 signature rate, author vs impostors | {s['M8']['author_per_1k']} vs {s['M8']['impostor_per_1k']} | author higher | {s['M8']['pass']} |",
              "", f"- M1: ceiling accept {s['M1']['ceiling_accept']:.1%}; impostor accept {s['M1']['impostor_accept']:.1%}; "
              f"Claude controls accept {s['M1']['llm_accept']}. Threshold {s['M1']['threshold']} (5% false accepts on the training negatives, in CV; "
              f"negatives: {s['M1'].get('negatives')}).",
              f"- M1 impostor accept by author: {s['M1']['impostor_accept_by_author']}",
              f"- M15: { {k: v for k, v in s['M15'].items() if k != 'pass'} }",
              f"- Delta: author dev {s['M6']['author_delta'].get('delta')}; impostors {s['M6']['impostor_delta'].get('delta')}.",
              "", "## Within-author ceiling, topic-disjoint halves (train + dev)", "",
              f"- Halves: clusters {c['clusters_A']} ({c['words_A']:,} words) vs {c['clusters_B']} ({c['words_B']:,} words).",
              f"- Delta A vs B: {c['delta_A_vs_B'].get('delta')} (random halves on 2026-11-08: 0.753)."]
        for k in ("styledistance_auc_n20", "styledistance_auc_n60"):
            if k in c:
                L.append(f"- StyleDistance AUC, n={c[k]['n_per_class']} per class: {c[k]['auc']} ± {c[k]['sd']} "
                         "(random halves: 0.497).")
        L += ["", "## Built-in systems (dev)", "", HEAD] + [_row(k, v) for k, v in rep["systems"].items()]
    else:
        s = rep["scores"]
        L += [HEAD, _row(rep["system"], s), ""]
        for k in ("composite", "M4_meaning", "M5_entities", "M9_memorization", "M12_length", "fallback_rate", "M1_by_op"):
            if k in s:
                L.append(f"- {k}: {s[k]}")
        L += ["", "### Tic profile", "", "| Feature | Value | Author | z | Pools with \\|z\\| > 2 |", "|---|---|---|---|---|"]
        L += [f"| {f} | {v['value']} | {v['reference']} | {v['z']} | {v['share_abs_z_gt_2']} |"
              for f, v in s["M6_tic_profile"]["features"].items()]
    L += ["", "Not implemented yet: " + "; ".join(rep["not_implemented"]) + ".",
          "Dropped: " + "; ".join(rep.get("dropped", [])) + "."]
    return "\n".join(L) + "\n"


def baseline_report(cfg: dict, part: str = "dev", systems=("b0", "b1", "b2")) -> dict:
    """The Phase 2 exit report: gathers the saved reports into eval_reports/baseline-v2."""
    d = REPO / "eval_reports"
    get = lambda n: json.loads((d / f"{n}.json").read_text()) if (d / f"{n}.json").exists() else None
    san = get("phase2-sanity")
    sysr = {s: get(f"{s}-{part}") for s in systems}
    rec, jud, m10, vc = get(f"recall-probe-base-{part}"), get(f"m11-judge-{part}"), get(f"m10-{part}"), get(f"verifier-check-{part}")
    s = san["sanity"]
    emb_ok = bool(s.get("M2", {}).get("pass"))
    gate = [("AV AUC >= 0.90 on dev", s["M1"]["pass"], f"{s['M1']['auc']}"),
            ("M15 passes sanity or is dropped", True, "passes" if s["M15"]["pass"] else "dropped from the composite"),
            ("Embedding metrics pass sanity or are dropped", True, f"StyleDistance classifier AUC {s.get('M2', {}).get('classifier_auc')}"
             + ("" if emb_ok else " (dropped)")),
            ("Topic-disjoint ceiling and split hash recorded", "ceiling" in san, san["split_hash"][:12]),
            ("B0 and B1 scored", all(sysr.get(x) for x in ("b0", "b1")), part)]
    rep = dict(system="baseline-v2", split=part, generated=time.strftime("%Y-%m-%dT%H:%M:%S"), split_hash=san["split_hash"],
               exit_gate=[dict(check=a, ok=bool(b), detail=c) for a, b, c in gate], sanity=s, ceiling=san["ceiling"],
               systems={k: v["scores"] for k, v in sysr.items() if v}, builtin=san["systems"], recall_probe=rec, judge=jud,
               m10=m10, dropped=DROPPED, not_implemented=NOT_IMPLEMENTED)
    pairs = [(a, b) for a, b in (("b0", "b1"), ("b0", "b2"), ("b1", "b2"))
             if item_scores_file(cfg, a, part).exists() and item_scores_file(cfg, b, part).exists()]
    rep["composite_diffs"] = [compare(cfg, a, b, part) for a, b in pairs]
    L = [f"# Baseline v2: Phase 2 exit report, {part} ({rep['generated']})", "",
         f"Split hash `{san['split_hash'][:12]}`. Aggregate numbers only. The test split is untouched.", "",
         "## Exit gate", "", "| Check | Result | Detail |", "|---|---|---|"]
    L += [f"| {g['check']} | {'pass' if g['ok'] else 'FAIL'} | {g['detail']} |" for g in rep["exit_gate"]]
    L += ["", "## Systems", "",
          "| System | Composite [95% CI] | M1 accept | M2 clf accept | M15 author | M4 | Entities pass | Tic max \\|z\\| | Fallback |",
          "|---|---|---|---|---|---|---|---|---|"]
    h = san["systems"]["human"]
    L.append(f"| author, held out (ceiling) | | {h['M1_av']['accept_rate']:.1%} | {h.get('M2_classifier', {}).get('accept_rate', 0):.1%} | "
             f"{h['M15_attribution'].get('author', 0):.1%} | | | {h['M6_tic_profile'].get('max_abs_z')} | |")
    for k, v in rep["systems"].items():
        c, m4 = v.get("composite", {}), v.get("M4_meaning", {})
        fb = v.get("fallback_rate")
        L.append(f"| {k} | {c.get('value')} {c.get('ci95')} | {v['M1_av']['accept_rate']:.1%} | "
                 f"{v.get('M2_classifier', {}).get('accept_rate', 0):.1%} | {v['M15_attribution'].get('author', 0):.1%} | "
                 f"{m4.get('m4')} | {v.get('M5_entities', {}).get('pass_rate', 0):.1%} | {v['M6_tic_profile'].get('max_abs_z')} | "
                 f"{'' if fb is None else format(fb, '.1%')} |")
    i = san["systems"]["impostor"]
    L.append(f"| other human authors | | {i['M1_av']['accept_rate']:.1%} | {i.get('M2_classifier', {}).get('accept_rate', 0):.1%} | "
             f"{i['M15_attribution'].get('author', 0):.1%} | | | {i['M6_tic_profile'].get('max_abs_z')} | |")
    ax = next((v["composite"]["axes"] for v in rep["systems"].values() if "composite" in v), [])
    L += ["", f"Composite: geometric mean of {ax}, entity gate first. M4 is MIS against the input for `restyle` and the share of "
          "facts entailed for `write`.", "", "Paired composite differences (bootstrap over chunks):", ""]
    L += [f"- {c['a']} - {c['b']}: {c['diff']['value']:+.4f}, 95% CI {c['diff']['ci95']}" for c in rep["composite_diffs"]]
    if rec:
        L += ["", "## Recall probe, untuned base", "",
              f"{rec['prompts']} prompts; longest verbatim span {rec['max_span']} words; {rec['flagged']} at or over the {rec['gate_words']}-word gate."]
    if jud:
        L += ["", "## M11 judge (diagnostic)", "", f"Validation, real over impostor: {jud['validation_real_vs_impostor']['x_share']:.1%} "
              f"({'pass' if jud['pass'] else 'FAIL'}). " + " ".join(
                  f"{k.replace('_', ' ')}: {t['x_wins']}-{t['y_wins']} ({t['inconsistent']} inconsistent)."
                  for k, t in jud.items() if isinstance(t, dict) and "pairs" in t and not k.startswith("validation"))]
    if m10:
        L += ["", "## M10 detector", "", f"{'Passes' if m10['pass'] else 'Fails'} sanity: " + "; ".join(
            f"{k} AUC {v['auc']}" for k, v in m10["sets"].items() if v["auc"] is not None) + "."]
    L += ["", "Dropped: " + "; ".join(DROPPED) + ".", "Not built (Phase 2b): " + "; ".join(NOT_IMPLEMENTED) + ".",
          "Waiting on the user: coverage-probe briefs; blind reads (the kit is built)."]
    (d / "baseline-v2.json").write_text(json.dumps(rep, indent=1))
    (d / "baseline-v2.md").write_text("\n".join(L) + "\n")
    rep["_out"] = str(d / "baseline-v2.md")
    return rep
