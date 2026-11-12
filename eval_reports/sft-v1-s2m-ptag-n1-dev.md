# Eval: sft-v1-s2m-ptag-n1 on dev (2026-11-12T05:01:59)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2m-ptag-n1 | 154 | 83.1% | 96.8% | 76.6% | 13.0% | 2.39 | 0.942 | 0.0631 | 2.61 | 1.49 | 0.8 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.6245, 'ci95': [0.5412, 0.7034], 'chunks': 62, 'axis_means': {'m1': 0.8226, 'm15': 0.7621, 'm4': 0.8983}, 'gate_pass': 0.7823}
- M4_meaning: {'mis_restyle': {'mean': 0.9214, 'median': 0.9459, 'n': 62}, 'facts_entailed': {'restyle': 0.9678, 'write': 0.8752}, 'm4': 0.8983}
- M5_entities: {'pass_rate': 0.7823, 'n': 124, 'missing': 18, 'added': 11}
- M9_memorization: {'max_span': 13, 'flagged': 4, 'n': 124, 'target_rebuilt': {'max_span': 21, 'median_span': 8, 'at_or_over_gate': 78}}
- M12_length: {'within_30pct': 0.9677, 'n': 124}
- fallback_rate: 0.2661
- M1_by_op: {'restyle': 0.7848, 'write': 0.88}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.23 | 14.714 | 0.4 | 0.0 |
| sent_len_sd | 7.295 | 9.326 | -2.39 | 0.74 |
| words_per_para | 43.801 | 33.735 | 2.08 | 0.53 |
| one_sent_para_share | 0.345 | 0.42 | -0.99 | 0.26 |
| sp_per_1k | 28.378 | 24.575 | 0.31 | 0.0 |
| emdash_per_1k | 3.493 | 5.793 | -1.03 | 0.0 |
| colon_per_1k | 4.886 | 6.168 | -0.44 | 0.0 |
| semicolon_per_1k | 1.552 | 0.862 | 1.01 | 0.21 |
| paren_per_1k | 0.411 | 0.874 | -0.47 | 0.0 |
| question_per_100s | 1.287 | 3.561 | -1.03 | 0.0 |
| mattr500 | 0.513 | 0.545 | 0.18 | 0.11 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
