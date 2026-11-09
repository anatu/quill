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
from ..scorers import av, embed, entities, memo, stylometry
from ..scorers.lexicon import Lexicon
from . import pool

REPO = Path(__file__).resolve().parents[3]
BUILTIN = ("human", "impostor", "llm")
NOT_IMPLEMENTED = ["M3 LUAR", "M4 MIS / fact entailment", "M10 detector", "M11 judge", "M13 alpha", "M14 residue",
                   "decision composite (needs M4)", "spaCy NER in M5"]


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
        self.verifier = av.Verifier().fit(pos, pos_g, neg, neg_g)

        lab_t, lab_y = list(pos), ["author"] * len(pos)
        for p in itr:
            cls = "llm" if p["kind"] == "llm" else p["author"] if p["author"] in pool.NEIGHBOURS else None
            if cls:
                s = pool.segments(p["text"])
                lab_t += s
                lab_y += [cls] * len(s)
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
        for r in db.execute("SELECT text FROM posts"):
            self.memo.add(r["text"])
        for r in db.execute("SELECT text FROM dropped_blocks WHERE reason = 'duplicate_paragraph'"):
            self.memo.add(r["text"])
        db.close()
        self.lexicon = Lexicon.load(Path(cfg["paths"]["lexicon"]) / "v0.json")

        self.pos, self.neg = pos, neg
        self.pos_g = pos_g
        if use_embeddings:
            cache = Path(cfg["paths"]["eval"]) / "cache"
            self.E_pos = embed.encode(pos, "style", cache)
            self.E_neg = embed.encode(neg, "style", cache)
            llm = [p["text"] for p in self.imp if p["kind"] == "llm"]
            self.c_author = embed.centroid(self.E_pos)
            self.c_llm = embed.centroid(embed.encode(llm, "style", cache))
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler

            self.emb_clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000,
                                                                              class_weight="balanced"))
            self.emb_clf.fit(np.vstack([self.E_pos, self.E_neg]), np.r_[np.ones(len(pos)), np.zeros(len(neg))])

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
            spans = [self.memo.longest(i["text"], i["input"])["span"] for i in with_input]
            ent = [entities.compare(i["input"], i["text"]) for i in with_input]
            out["M9_memorization"] = dict(max_span=max(spans), flagged=sum(1 for s in spans if s >= self.memo.n),
                                          n=len(spans))
            out["M5_entities"] = dict(pass_rate=round(sum(e["ok"] for e in ent) / len(ent), 4), n=len(ent),
                                      missing=sum(1 for e in ent if e["missing"]),
                                      added=sum(1 for e in ent if e["added"]))
        with_len = [i for i in items if i.get("length_words")]
        if with_len:
            ok = [abs(len(i["text"].split()) - i["length_words"]) <= 0.3 * i["length_words"] for i in with_len]
            out["M12_length"] = dict(within_30pct=round(sum(ok) / len(ok), 4), n=len(ok))
        return out


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
    out["M1"]["pass"] = out["M1"]["auc"] >= 0.90
    pred = ctx.attributor.predict(hs)
    m15 = {"author_share_on_author": round(pred.count("author") / len(pred), 4)}
    for cls in ctx.attributor.classes:
        if cls == "author":
            continue
        t = llm if cls == "llm" else [s for s, g in zip(isg, ig) if g == cls]
        if t:
            pr = ctx.attributor.predict(t)
            m15[f"{cls}_recall"] = round(pr.count(cls) / len(pr), 3)
            m15[f"{cls}_called_author"] = round(pr.count("author") / len(pr), 3)
            m15[f"{cls}_n"] = len(t)
    leaks = {k[:-len("_called_author")]: v for k, v in m15.items() if k.endswith("_called_author") and v > 0.20}
    m15["classes_called_author_over_20pct"] = sorted(leaks)
    m15["pass"] = m15["author_share_on_author"] >= 0.80 and not leaks
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
               not_implemented=NOT_IMPLEMENTED)
    return write_report(rep, name or f"{system}-{part}")


def run_sanity(cfg: dict, use_embeddings: bool = True) -> dict:
    ctx = Context(cfg, use_embeddings)
    held = [c["text"] for c in ctx.chunks if c["split"] == "dev"]
    rep = dict(system="sanity", split="dev", generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
               split_hash=split.refresh(cfg)["hash"], sanity=sanity(ctx), ceiling=ceiling(ctx),
               systems={s: ctx.score(ctx.items(s, "dev"), held) for s in BUILTIN},
               signature_phrases=len(ctx.signature.phrases), not_implemented=NOT_IMPLEMENTED)
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
    return (f"| {name} | {s['n_passages']} | {s['M1_av']['accept_rate']:.1%} | "
            f"{s['M15_attribution'].get('author', 0):.1%} | {s['M15_attribution'].get('llm', 0):.1%} | "
            f"{t.get('max_abs_z', '')} | {s['M6_delta'].get('delta', '')} | {sd} | "
            f"{s['M7_lexicon']['vocabulary']['ratio']} | {s['M7_lexicon']['structure']['ratio']} | "
            f"{s['M8_signature']['ratio']} |")


HEAD = ("| System | Passages | M1 accept | M15 author | M15 LLM | Tic max \\|z\\| | Delta | M2 delta | "
        "M7 vocab × | M7 struct × | M8 × |\n|---|---|---|---|---|---|---|---|---|---|---|")


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
              f"Claude controls accept {s['M1']['llm_accept']}. Threshold {s['M1']['threshold']} (5% impostor false accepts in training CV).",
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
        for k in ("M5_entities", "M9_memorization", "M12_length"):
            if k in s:
                L.append(f"- {k}: {s[k]}")
        L += ["", "### Tic profile", "", "| Feature | Value | Author | z | Pools with \\|z\\| > 2 |", "|---|---|---|---|---|"]
        L += [f"| {f} | {v['value']} | {v['reference']} | {v['z']} | {v['share_abs_z_gt_2']} |"
              for f, v in s["M6_tic_profile"]["features"].items()]
    L += ["", "Not implemented yet: " + "; ".join(rep["not_implemented"]) + "."]
    return "\n".join(L) + "\n"
