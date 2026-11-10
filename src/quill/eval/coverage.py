"""Coverage probe (plan.md Phase 2): briefs from the user's own work, far from the author's topics.

No reference text exists, so outputs are scored on style only, plus topic drift: did the output
move toward the author's pet topics? Drift is the output's similarity to its nearest author
topic centroid minus the input's (content encoder, not the style encoder). The alarm threshold
is set on dev, where inputs and outputs share a topic: the 95th percentile of drift there.

Briefs: <paths.eval>/coverage/briefs.jsonl, one JSON object per line:
  {"id": "c01", "brief": "...", "facts": "- fact\\n- fact", "words": 400}
`facts` and `words` are optional. Outputs: <paths.eval>/outputs/<system>/coverage.jsonl.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from ..corpus import split
from ..scorers import embed
from . import harness

MIN_BRIEFS = 30


def briefs_file(cfg: dict) -> Path:
    return Path(cfg["paths"]["eval"]) / "coverage" / "briefs.jsonl"


def load(cfg: dict) -> list[dict]:
    f = briefs_file(cfg)
    if not f.exists():
        raise SystemExit(f"no coverage briefs: write {f} (see quill/eval/coverage.py for the format)")
    rows = []
    for k, line in enumerate(x for x in f.read_text().splitlines() if x.strip()):
        r = json.loads(line)
        facts = r.get("facts") or ""
        rows.append(dict(id=r.get("id") or f"c{k + 1:02d}", split="coverage", post=None, words=int(r.get("words") or 400),
                         brief=r["brief"], facts=facts, draft="", bucket="300-500"))
    return rows


class Drift:
    def __init__(self, ctx):
        self.cache = Path(ctx.cfg["paths"]["eval"]) / "cache"
        info = json.loads((split.split_dir(ctx.cfg) / "clusters.json").read_text())
        tr = [c for c in ctx.chunks if c["split"] == "train"]
        E = embed.encode([c["text"] for c in tr], "content", self.cache)
        cl = np.array([info["post_cluster"].get(c["post"], -1) for c in tr])
        self.centroids = np.vstack([embed.centroid(E[cl == k]) for k in sorted(set(cl)) if k != -1])

    def nearest(self, texts: list[str]) -> np.ndarray:
        return (embed.encode(texts, "content", self.cache) @ self.centroids.T).max(1)

    def score(self, inputs: list[str], outputs: list[str]) -> np.ndarray:
        return self.nearest(outputs) - self.nearest(inputs)


def threshold(ctx, drift: Drift, systems=("b0", "b1"), part: str = "dev") -> float:
    d = []
    for s in systems:
        f = Path(ctx.cfg["paths"]["eval"]) / "outputs" / s / f"{part}.jsonl"
        if f.exists():
            it = [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
            d += list(drift.score([i["input"] for i in it], [i["text"] for i in it]))
    if not d:
        raise SystemExit("no dev outputs to set the drift threshold on: run `quill baseline b0` or `b1`")
    return float(np.quantile(d, 0.95))


def run(cfg: dict, system: str, ctx=None) -> dict:
    ctx = ctx or harness.Context(cfg)
    items = ctx.items(system, "coverage")
    held = [c["text"] for c in ctx.chunks if c["split"] == "dev"]
    plain = [dict(id=i["id"], text=i["text"]) for i in items]           # no input: style metrics only
    scores = ctx.score(plain, held)
    drift = Drift(ctx)
    thr = threshold(ctx, drift)
    d = drift.score([i["input"] for i in items], [i["text"] for i in items])
    words = [abs(len(i["text"].split()) - i["length_words"]) <= 0.3 * i["length_words"] for i in items if i.get("length_words")]
    rep = dict(system=system, split="coverage", generated=time.strftime("%Y-%m-%dT%H:%M:%S"), briefs=len(items),
               enough_briefs=len(items) >= MIN_BRIEFS, scores=scores,
               topic_drift=dict(mean=round(float(d.mean()), 4), p95=round(float(np.quantile(d, 0.95)), 4),
                                threshold_dev_p95=round(thr, 4), over_threshold=round(float((d > thr).mean()), 4)),
               length_within_30pct=round(float(np.mean(words)), 4) if words else None,
               not_implemented=harness.NOT_IMPLEMENTED, dropped=harness.DROPPED)
    out = harness.REPO / "eval_reports" / f"coverage-{system}.md"
    L = harness.render(rep).splitlines()
    L.insert(3, f"Coverage probe: {len(items)} briefs from outside the author's topics. Topic drift: {rep['topic_drift']}. "
                f"Length within 30%: {rep['length_within_30pct']}.")
    out.write_text("\n".join(L) + "\n")
    out.with_suffix(".json").write_text(json.dumps(rep, indent=1))
    rep["_out"] = str(out)
    return rep
