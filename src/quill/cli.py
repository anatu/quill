"""quill command line."""
from __future__ import annotations

import argparse
import sys

from . import config


def _audit(args) -> int:
    from . import audit

    cfg = config.load(args.config)
    inv = audit.run(cfg, raw=args.raw)
    m = inv["measured"]
    print(f"raw: {inv['raw']}")
    print(f"pages {m['pages']}  kept {m['kept_posts']}  words {m['words']:,}  quote words {m['quote_words']:,}")
    print(f"twin posts {m['twin_posts']}  twin groups {len(inv['twin_groups'])}  "
          f"cross-post 10-gram share {inv['cross_post_ngram_share']:.1%}")
    print(f"post-2022 share {m['share_post_2022']:.1%}  median length {inv['length_words']['median']} words  "
          f"p90 {inv['length_words']['p90']}")
    print(f"dropped under {cfg['corpus']['min_post_words']} words: {len(inv['dropped_short'])}  "
          f"boilerplate paragraphs removed: {len(inv['boilerplate_removed'])}")
    print("\ncheck              expected   measured   ok")
    bad = 0
    for c in inv["checks"]:
        bad += not c["ok"]
        print(f"{c['field']:<18} {c['expected']!s:>9}  {c['measured']!s:>9}   {'yes' if c['ok'] else 'NO'}")
    print(f"\nwrote {inv['_out']}")
    return 1 if bad else 0


def _ingest(args) -> int:
    from .corpus import build

    r = build.build(config.load(args.config), raw=args.raw)
    print(f"pages {r['pages']}  kept {r['kept_posts']}  words {r['words']:,}  tier {r['tier']}  "
          f"(Phase 0: {r['phase0_words']:,}, {r['word_delta']:+,})")
    print(f"quote words stripped {r['quote_words']:,}  duplicate paragraphs {r['duplicate_paragraphs']}  "
          f"twin groups {len(r['twins']['groups'])}")
    c = r["chunks"]
    print(f"chunks {c['n']}  median {c['median']} words  buckets {c['buckets']}")
    print(f"dropped posts {len(r['dropped_posts'])}  PII hits {len(r['pii_hits'])}")
    print(f"wrote {r['_out']}")
    return 0


def _aicheck(args) -> int:
    from .clean import ai_check

    s = ai_check.run(config.load(args.config))
    print(f"baseline posts {s['baseline_posts']}  checked {s['checked_posts']}  flagged {s['flagged']}  "
          f"sustained shifts {len(s['shifts'])}")
    print(f"thresholds per 1k: {s['thresholds_per_1k']}  lexicon items {s['lexicon_items']} "
          f"({s['whitelisted_items']} whitelisted)")
    print(f"wrote {s['lexicon']}\nwrote {s['_out']}")
    return 0


def _flags(args) -> int:
    from .clean import ai_check

    cfg = config.load(args.config)
    if args.slug:
        if not args.decision:
            print("give a decision: keep, drop or pending")
            return 2
        if not ai_check.decide(cfg, args.slug, args.decision, args.note or ""):
            print(f"no flag on {args.slug}")
            return 1
    for r in ai_check.list_flags(cfg):
        print(f"{r['decision']:<8} {r['date']}  {r['slug']:<50} {', '.join(r['flags'])}"
              + (f"  [{r['note']}]" if r["note"] else ""))
    return 0


def _spotcheck(args) -> int:
    from .corpus import gate

    cfg = config.load(args.config)
    if args.record is not None:
        gate.record(cfg, args.record, args.note or "")
        print(f"recorded {args.record} bad chunks")
        return 0
    r = gate.spotcheck(cfg, n=args.n, seed=args.seed)
    print(f"sample {r['n']} of {r['chunks']} chunks (seed {r['seed']})")
    print(f"automatic scan: {r['auto_hits']} chunks with candidate leftovers {r['auto_by_kind']}; "
          f"{r['auto_hits_in_sample']} in the sample")
    print(f"wrote {r['out']}")
    return 0


def _gate(args) -> int:
    from .corpus import gate

    checks = gate.status(config.load(args.config))
    for c in checks:
        mark = {True: "pass", False: "FAIL", None: "pending"}[c["ok"]]
        print(f"{mark:<8} {c['name']}: {c['detail']}")
    return 0 if all(c["ok"] for c in checks) else 1


def _split(args) -> int:
    from .corpus import split

    r = split.make(config.load(args.config), force=args.force)
    print(("froze" if r["created"] else "frozen") + f" split at {r['dir']} ({r['frozen']})  hash {r['hash'][:12]}")
    for s in split.SPLITS:
        print(f"{s:<6} posts {r['posts'][s]:>4}  chunks {r['chunks'][s]:>4}  words {r['words'][s]:>8,}  "
              f"share {r['share'][s]:.1%}")
    print(f"held-out clusters: test {r['test_clusters']}  dev {r['dev_clusters']}")
    if r["unassigned_posts"] or r["missing_posts"]:
        print(f"posts without a split: {len(r['unassigned_posts'])}; frozen posts no longer in the corpus: "
              f"{len(r['missing_posts'])}")
    return 0


def _eval(args) -> int:
    from .eval import harness

    cfg = config.load(args.config)
    if args.compare:
        r = harness.compare(cfg, args.compare[0], args.compare[1], args.split)
        d = r["diff"]
        print(f"composite {r['a']} - {r['b']} on {args.split}: {d['value']:+.4f}  95% CI [{d['ci95'][0]:+.4f}, {d['ci95'][1]:+.4f}]  "
              f"chunks {d['chunks']}  axes {r['axes']}")
        return 0
    if args.report:
        r = harness.baseline_report(cfg, args.split)
        bad = [g["check"] for g in r["exit_gate"] if not g["ok"]]
        print(f"Phase 2 exit gate: {'passes' if not bad else 'FAIL ' + '; '.join(bad)}")
        print(f"wrote {r['_out']}")
        return 0
    if args.detector:
        from .eval import vcheck

        r = vcheck.detector(cfg, args.split)
        print(f"M10 {'passes' if r['pass'] else 'FAILS'}: " + "  ".join(f"{k} AUC {v['auc']}" for k, v in r["sets"].items() if v["auc"]))
        print(f"wrote {r['_out']}")
        return 0
    if args.verifiers:
        from .eval import vcheck

        r = vcheck.run(cfg, args.split)
        for n, x in r["scorers"].items():
            print(f"{n:32s} AUC impostors {x['auc_impostor']:.3f}  drafts {x['auc_draft']:.3f}  "
                  f"accept author {x['accept_author']:.1%}  drafts {x['accept_draft']:.1%}")
        for n, x in vcheck.with_drafts(cfg, args.split)["scorers"].items():
            print(f"with draft negatives: {n:32s} accept author {x['accept_author']:.1%}  drafts {x['accept_draft']:.1%}")
    elif args.sanity:
        r = harness.run_sanity(cfg, use_embeddings=not args.no_embed)
        bad = [k for k, v in r["sanity"].items() if isinstance(v, dict) and v.get("pass") is False]
        print(f"sanity: {'all metrics pass' if not bad else 'FAIL ' + ', '.join(bad)}")
    else:
        if not args.system:
            print("give --system <name> or --sanity")
            return 2
        r = harness.run(cfg, args.system, args.split, use_embeddings=not args.no_embed)
        s = r["scores"]
        print(f"{args.system} on {args.split}: M1 accept {s['M1_av']['accept_rate']:.1%}  "
              f"M15 author {s['M15_attribution'].get('author', 0):.1%}  tic max |z| {s['M6_tic_profile'].get('max_abs_z')}")
    print(f"wrote {r['_out']}")
    return 0


def _pairs(args) -> int:
    from .pairs import build

    r = build.run(config.load(args.config), retries=args.retries)
    for part, v in r["splits"].items():
        print(f"{part}: {v['chunks']} chunks  A kept {v['A']['kept']}  B kept {v['B']['kept']}  both {v['both_share']:.1%}")
    print(f"gate (85% of train chunks keep both forms): {'passes' if r['gate']['passed'] else 'FAILS'}")
    for k, v in r["data"].items():
        print(f"{k}: {v['rows']} -> {v['dir']}")
    return 0 if r["gate"]["passed"] else 1


def _inputs(args) -> int:
    from .eval import inputs

    if args.train_drafts:
        r = inputs.make_train_drafts(config.load(args.config))
        print(f"train drafts {r['n']}  new calls {r['new_calls']}  cost ${r['cost_usd']}  {r['file']}")
        return 0
    r = inputs.make(config.load(args.config), force=args.force)
    print(("froze" if r["created"] else "frozen") + f" eval inputs at {r['dir']} ({r['frozen']})  hash {r['hash'][:12]}")
    print(f"chunks {r['n']}  facts and briefs by {r['util_model']}  drafts by {r['draft_model']}  "
          f"draft/target words {r['draft_to_target_words']}")
    return 0


def _baseline(args) -> int:
    from .eval import baselines, harness

    cfg = config.load(args.config)
    r = baselines.run(cfg, args.name, args.split, n=args.n)
    print({k: v for k, v in r.items() if k != "items"})
    if args.split == "coverage":
        from .eval import coverage

        rep = coverage.run(cfg, args.name)
        print(f"{args.name} on coverage: {rep['briefs']} briefs  topic drift {rep['topic_drift']}")
        print(f"wrote {rep['_out']}")
        return 0
    rep = harness.run(cfg, args.name, args.split)
    s = rep["scores"]
    print(f"{args.name} on {args.split}: M1 accept {s['M1_av']['accept_rate']:.1%}  "
          f"tic max |z| {s['M6_tic_profile'].get('max_abs_z')}  fallback {s.get('fallback_rate')}")
    print(f"wrote {rep['_out']}")
    return 0


def _train(args) -> int:
    from . import train

    r = train.run(config.load(args.config), args.name, stage=args.stage, passes=args.passes, resume=args.resume)
    print(r)
    return r["exit"]


def _run(args) -> int:
    from .eval import baselines, harness

    cfg = config.load(args.config)
    r = baselines.run_adapter(cfg, args.name, args.adapter, args.split, n=args.n, tag=args.tag)
    print({k: v for k, v in r.items() if k != "items"})
    rep = harness.run(cfg, args.name, args.split)
    s = rep["scores"]
    print(f"{args.name} on {args.split}: composite {s.get('composite')}  M1 accept {s['M1_av']['accept_rate']:.1%}  "
          f"fallback {s.get('fallback_rate')}")
    print(f"wrote {rep['_out']}")
    return 0


def _blind(args) -> int:
    from .eval import blind

    cfg = config.load(args.config)
    kit = blind.make(cfg, args.test, args.system, args.split, n=args.n, baseline=args.baseline, op=args.op, seed=args.seed)
    if not args.report:
        blind.session(cfg, kit)
    r = blind.report(cfg, kit)
    print({k: v for k, v in r.items() if k != "reasons"})
    return 0


def _judge(args) -> int:
    from .eval import judge

    r = judge.run(config.load(args.config), args.split, n=args.n)
    v = r["validation_real_vs_impostor"]
    print(f"judge validation: real over impostor {v['x_share']:.1%} ({'pass' if r['pass'] else 'FAIL'})  cost ${r['cost_usd']}")
    print(f"wrote {r['_out']}")
    return 0


def _recall(args) -> int:
    from .eval import baselines

    r = baselines.recall_probe(config.load(args.config), args.split)
    print(f"{r['model']} on {args.split}: {r['prompts']} prompts  max span {r['max_span']} words  "
          f"at or over {r['gate_words']}: {r['flagged']}")
    print(f"by prompt: {r['by_kind']}")
    print(f"wrote {r['_out']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="quill")
    ap.add_argument("--config", help="path to quill.yaml (default: configs/quill.yaml)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit", help="inventory the raw corpus and check the measured figures")
    a.add_argument("--raw", help="raw corpus dir (default: paths.raw)")
    a.set_defaults(fn=_audit)
    a = sub.add_parser("ingest", help="extract, clean, dedupe and chunk the raw pages into corpus.sqlite")
    a.add_argument("--raw", help="raw corpus dir (default: paths.raw)")
    a.set_defaults(fn=_ingest)
    a = sub.add_parser("aicheck", help="build lexicon v0 and flag post-cutoff posts for review")
    a.set_defaults(fn=_aicheck)
    a = sub.add_parser("flags", help="list AI-text flags, or record a decision on one")
    a.add_argument("slug", nargs="?")
    a.add_argument("decision", nargs="?", choices=["keep", "drop", "pending"])
    a.add_argument("--note")
    a.set_defaults(fn=_flags)
    a = sub.add_parser("spotcheck", help="write random chunks for a human read; record the result")
    a.add_argument("--n", type=int, default=100)
    a.add_argument("--seed", type=int, default=1)
    a.add_argument("--record", type=int, metavar="BAD", help="number of bad chunks found in the sample")
    a.add_argument("--note", help="who read the sample, and anything the count needs explained")
    a.set_defaults(fn=_spotcheck)
    a = sub.add_parser("split", help="freeze topic-disjoint train/dev/test splits, or show the frozen ones")
    a.add_argument("--force", action="store_true", help="re-cluster and overwrite the frozen split")
    a.set_defaults(fn=_split)
    a = sub.add_parser("eval", help="score a system on dev or test, or run the metric sanity check")
    a.add_argument("--system", help="human, impostor, llm, or a name under <eval>/outputs/")
    a.add_argument("--split", choices=["dev", "test"], default="dev")
    a.add_argument("--compare", nargs=2, metavar=("A", "B"), help="paired bootstrap of the composite, A minus B")
    a.add_argument("--report", action="store_true", help="write the Phase 2 exit report, eval_reports/baseline-v2")
    a.add_argument("--detector", action="store_true", help="M10 sanity: Fast-DetectGPT on author text vs system outputs")
    a.add_argument("--verifiers", action="store_true", help="compare style scorers on author text vs plain drafts")
    a.add_argument("--sanity", action="store_true", help="metric sanity check and within-author ceiling on dev")
    a.add_argument("--no-embed", action="store_true", help="skip StyleDistance (M2)")
    a.set_defaults(fn=_eval)
    a = sub.add_parser("inputs", help="make and freeze the eval inputs (facts, briefs, generic drafts) with Claude")
    a.add_argument("--force", action="store_true", help="regenerate and overwrite the frozen inputs")
    a.add_argument("--train-drafts", action="store_true", help="facts and drafts for train chunks: verifier negatives")
    a.set_defaults(fn=_inputs)
    a = sub.add_parser("pairs", help="build, curate and write the training pairs (paraphrases through Claude)")
    a.add_argument("--retries", type=int, default=1, help="regenerations of a failed paraphrase")
    a.set_defaults(fn=_pairs)
    a = sub.add_parser("baseline", help="run a baseline (b0 Claude, b1 local base, b2 the input) and score it")
    a.add_argument("name", choices=["b0", "b1", "b2"])
    a.add_argument("--split", choices=["dev", "test"], default="dev")
    a.add_argument("--n", type=int, default=4, help="candidates per input")
    a.set_defaults(fn=_baseline)
    a = sub.add_parser("train", help="train an adapter with mlx-lm on a pairs stage")
    a.add_argument("name", help="adapter name under ~/.quill/adapters/")
    a.add_argument("--stage", default="s1", choices=("s1", "s2", "s1p"))
    a.add_argument("--passes", type=float, default=1.0)
    a.add_argument("--resume", help="adapter to start from")
    a.set_defaults(fn=_train)
    a = sub.add_parser("run", help="generate with a trained adapter on the eval inputs and score it")
    a.add_argument("name", help="system name for the outputs and report")
    a.add_argument("--adapter", required=True)
    a.add_argument("--tag", default="draft", choices=("paraphrase", "draft"), help="the template's input field")
    a.add_argument("--split", choices=["dev", "test"], default="dev")
    a.add_argument("--n", type=int, default=1, help="candidates per input")
    a.set_defaults(fn=_run)
    a = sub.add_parser("blind", help="blind reading test: build the kit, read it in the terminal, report the binomial p")
    a.add_argument("--test", choices=("A", "R"), required=True, help="A: real vs system. R: system vs baseline against a reference")
    a.add_argument("--system", required=True)
    a.add_argument("--baseline", default="b0")
    a.add_argument("--split", default="test", choices=("dev", "test"))
    a.add_argument("--op", default="restyle", choices=("restyle", "write"))
    a.add_argument("--n", type=int, default=40)
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--report", action="store_true", help="show the result so far without reading")
    a.set_defaults(fn=_blind)
    a = sub.add_parser("judge", help="M11: validate the Claude judge on dev and compare the scored systems")
    a.add_argument("--split", default="dev", choices=("dev", "test"))
    a.add_argument("--n", type=int, default=40)
    a.set_defaults(fn=_judge)
    a = sub.add_parser("recall", help="recall probe: longest verbatim spans from the untuned local base")
    a.add_argument("--split", choices=["dev", "test"], default="dev")
    a.set_defaults(fn=_recall)
    a = sub.add_parser("gate", help="show the Phase 1 exit gate")
    a.set_defaults(fn=_gate)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
