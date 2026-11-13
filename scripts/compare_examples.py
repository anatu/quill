"""Vanilla Claude against quill on briefs that are not the author's material.

    uv run python scripts/compare_examples.py

Claude (the configured draft model, no style instruction) writes each brief. Quill restyles that
same draft: four candidates from the fused adapter, the usual hard gates, rerank by style. The
pairs and a few counts go to ~/.quill/examples/vanilla-vs-quill.jsonl. Nothing is published here.
"""
from __future__ import annotations

import json
import re
import statistics as st
import sys
from pathlib import Path

from quill import config, template
from quill.eval import baselines, harness
from quill.gen.claude_cli import Claude
from quill.gen.local import Local

BRIEFS = [
    dict(id="estimates", words=160, brief="Why software estimates run long.",
         facts=["A team estimated a checkout redesign at 6 weeks.", "It shipped after 14 weeks.",
                "9 of the 14 weeks went to work nobody had listed: tax rules, refunds and an old mobile app."]),
    dict(id="meeting", words=150, brief="What happened when a team cut its weekly status meeting.",
         facts=["The meeting had 12 people and ran 60 minutes every Monday.",
                "It was replaced by a written update that takes 10 minutes to read.",
                "About two decisions a month still need a live call."]),
    dict(id="interviews", words=160, brief="What five user interviews showed that a survey of 2,000 people did not.",
         facts=["In the survey, 71% of users asked for more export formats.",
                "In interviews, 4 of 5 users were exporting only to fix a broken report inside the product.",
                "The team fixed the report instead of adding formats."]),
    dict(id="saving", words=170, brief="Why saving a little early beats saving more later.",
         facts=["One person saves $200 a month from age 25 to 35, then stops: $24,000 in total.",
                "Another saves $200 a month from age 35 to 65: $72,000 in total.",
                "At 7% a year, the first ends with about $281,000 at 65 and the second with about $244,000."]),
]
INFORMATIONAL = [
    dict(id="higgs", words=170, brief="A news summary of the 2012 announcement that the Higgs boson had been found.",
         facts=["CERN announced the discovery on 4 July 2012.",
                "Two experiments at the Large Hadron Collider, ATLAS and CMS, each saw a new particle with a mass near 125 GeV.",
                "Each result reached five sigma, the standard physicists use to claim a discovery.",
                "The particle was predicted in 1964.",
                "Peter Higgs and Francois Englert received the Nobel Prize in Physics in 2013."]),
    dict(id="sky", words=170, brief="A walkthrough of why the sky is blue and sunsets are red.",
         facts=["Sunlight contains all colors.", "Air molecules scatter light, and scattering is proportional to 1 over the wavelength to the fourth power (Rayleigh scattering).",
                "Blue light at 450 nanometers scatters about 4 times more than red light at 650 nanometers.",
                "At sunset the light crosses much more air, so most of the blue has been scattered out of the direct beam."]),
    dict(id="binary-search", words=170, brief="A walkthrough of how binary search works and why it is fast.",
         facts=["The list must be sorted.", "Each step compares the target with the middle item and discards half of the remaining list.",
                "A list of 1,000,000 items needs at most 20 steps, because 2 to the power 20 is 1,048,576.",
                "Checking every item in order could take 1,000,000 steps."]),
    dict(id="odd-numbers", words=160, brief="A walkthrough of why the sum of the first n odd numbers is n squared.",
         facts=["1 + 3 + 5 = 9, which is 3 squared.", "The nth odd number is 2n - 1.",
                "A square of side n grows to a square of side n + 1 by adding an L-shaped border of 2n + 1 dots.",
                "So each new odd number completes the next square."]),
]
SETS = dict(essay=BRIEFS, info=INFORMATIONAL)
VANILLA = ("Write about {words} words on the following.\n\n{brief}\n\nUse these facts:\n{facts}\n\n"
           "Plain paragraphs only: no title, no headings, no lists. Output only the text.")


def counts(text: str) -> dict:
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if x.strip()]
    n = [len(x.split()) for x in sents]
    paras = [p for p in text.split("\n\n") if p.strip()]
    return dict(words=len(text.split()), paragraphs=len(paras), sentences=len(sents),
                sent_mean=round(st.mean(n), 1), sent_sd=round(st.pstdev(n), 1), shortest=min(n), longest=max(n),
                emdashes=text.count("—"))


def main(tag: str = "paraphrase", which: str = "essay", fused: str = "~/.quill/models/qwen3-8b-sft-v1-s2m-fused-6bit", n: int = 4) -> None:
    cfg = config.load(None)
    briefs = SETS[which]
    claude = Claude(cfg, cfg.get("gen", {}).get("draft_model", "claude-opus-5-5"))
    drafts = claude.map([(VANILLA.format(words=b["words"], brief=b["brief"], facts="\n".join("- " + f for f in b["facts"])),)
                         for b in briefs])
    gen = Local(dict(cfg, gen=dict(cfg.get("gen", {}), base_model=str(Path(fused).expanduser()))))
    ctx = harness.Context(cfg)
    out = []
    for b, d in zip(briefs, drafts):
        words = len(d.split())
        system = template.system("restyle", tag, template.bucket(words))
        cands = [baselines.MARKER_LINE.sub("", gen.ask(d, system, s, int(words * 2.2) + 150)).strip() for s in range(n)]
        rr = baselines.rerank(ctx, cands, d, words)
        m1 = [round(float(x), 3) for x in ctx.verifier.prob([d, cands[rr["choice"]]])]     # P(author), per text
        out.append(dict(id=b["id"], tag=tag, brief=b["brief"], facts=b["facts"], claude=d, quill=cands[rr["choice"]],
                        fallback=rr["fallback"], checks=rr["checks"][rr["choice"]], claude_model=claude.model,
                        quill_model=gen.model, verifier=dict(claude=m1[0], quill=m1[1], threshold=round(float(ctx.verifier.threshold), 3)),
                        counts=dict(claude=counts(d), quill=counts(cands[rr["choice"]])),
                        failing_candidates=sum(bool(c["fails"]) for c in rr["checks"])))
    d = Path(cfg["paths"]["home"]) / "examples"
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"vanilla-vs-quill-{which}-{tag}.jsonl"
    f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    print(f"claude calls {claude.calls} (${claude.cost:.2f}); wrote {f}")
    for r in out:
        print(f"\n===== {r['id']}  fallback={r['fallback']}  failing candidates {r['failing_candidates']}/{n}  "
              f"span={r['checks']['span']}  verifier {r['verifier']}")
        print("--- CLAUDE", r["counts"]["claude"], "\n" + r["claude"])
        print("--- QUILL", r["counts"]["quill"], "\n" + r["quill"])


if __name__ == "__main__":
    main(*sys.argv[1:3])
