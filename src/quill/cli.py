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
        gate.record(cfg, args.record)
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
    if args.sanity:
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
    a.set_defaults(fn=_spotcheck)
    a = sub.add_parser("split", help="freeze topic-disjoint train/dev/test splits, or show the frozen ones")
    a.add_argument("--force", action="store_true", help="re-cluster and overwrite the frozen split")
    a.set_defaults(fn=_split)
    a = sub.add_parser("eval", help="score a system on dev or test, or run the metric sanity check")
    a.add_argument("--system", help="human, impostor, llm, or a name under <eval>/outputs/")
    a.add_argument("--split", choices=["dev", "test"], default="dev")
    a.add_argument("--sanity", action="store_true", help="metric sanity check and within-author ceiling on dev")
    a.add_argument("--no-embed", action="store_true", help="skip StyleDistance (M2)")
    a.set_defaults(fn=_eval)
    a = sub.add_parser("gate", help="show the Phase 1 exit gate")
    a.set_defaults(fn=_gate)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
