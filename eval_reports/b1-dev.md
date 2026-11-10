# Eval: b1 on dev (2026-11-10T09:37:43)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b1 | 184 | 1.6% | 2.2% | 1.1% | 85.9% | 3.54 | 1.045 | -0.0564 | 3.06 | 1.35 | 0.55 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.0567, 'ci95': [0.0, 0.1002], 'chunks': 62, 'axis_means': {'m1': 0.0202, 'm15': 0.0121, 'm4': 0.8197}, 'gate_pass': 0.9113}
- M4_meaning: {'mis_restyle': {'mean': 0.7409, 'median': 0.8093, 'n': 62}, 'facts_entailed': {'restyle': 0.9672, 'write': 0.8985}, 'm4': 0.8197}
- M5_entities: {'pass_rate': 0.9113, 'n': 124, 'missing': 8, 'added': 6}
- M9_memorization: {'max_span': 8, 'flagged': 1, 'n': 124, 'target_rebuilt': {'max_span': 15, 'median_span': 0, 'at_or_over_gate': 10}}
- M12_length: {'within_30pct': 0.8065, 'n': 124}
- fallback_rate: 0.2581
- M1_by_op: {'restyle': 0.0337, 'write': 0.0}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 12.131 | 14.714 | -1.73 | 0.4 |
| sent_len_sd | 6.438 | 9.326 | -3.54 | 0.92 |
| words_per_para | 21.348 | 33.735 | -1.13 | 0.52 |
| one_sent_para_share | 0.693 | 0.42 | 1.65 | 0.64 |
| sp_per_1k | 27.681 | 24.575 | 0.23 | 0.04 |
| emdash_per_1k | 0.071 | 5.793 | -2.63 | 1.0 |
| colon_per_1k | 3.768 | 6.168 | -0.68 | 0.0 |
| semicolon_per_1k | 1.411 | 0.862 | 0.82 | 0.24 |
| paren_per_1k | 0.036 | 0.874 | -0.85 | 0.0 |
| question_per_100s | 1.213 | 3.561 | -1.04 | 0.0 |
| mattr500 | 0.521 | 0.545 | 0.2 | 0.04 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
