# Eval: sft-v1-s2m-n1 on dev (2026-11-12T04:21:21)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2m-n1 | 154 | 98.0% | 98.0% | 94.2% | 0.7% | 1.81 | 0.972 | 0.0811 | 1.37 | 1.15 | 1.09 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5675, 'ci95': [0.4835, 0.6529], 'chunks': 62, 'axis_means': {'m1': 0.9798, 'm15': 0.9355, 'm4': 0.8601}, 'gate_pass': 0.6129}
- M4_meaning: {'mis_restyle': {'mean': 0.879, 'median': 0.9258, 'n': 62}, 'facts_entailed': {'restyle': 0.9311, 'write': 0.8413}, 'm4': 0.8601}
- M5_entities: {'pass_rate': 0.6129, 'n': 124, 'missing': 39, 'added': 14}
- M9_memorization: {'max_span': 14, 'flagged': 12, 'n': 124, 'target_rebuilt': {'max_span': 19, 'median_span': 10, 'at_or_over_gate': 93}}
- M12_length: {'within_30pct': 0.9839, 'n': 124}
- fallback_rate: 0.4677
- M1_by_op: {'restyle': 0.9747, 'write': 0.9867}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 14.071 | 14.714 | -0.44 | 0.0 |
| sent_len_sd | 9.468 | 9.326 | -0.8 | 0.26 |
| words_per_para | 37.015 | 33.735 | 0.81 | 0.21 |
| one_sent_para_share | 0.346 | 0.42 | -0.97 | 0.26 |
| sp_per_1k | 41.584 | 24.575 | 1.4 | 0.21 |
| emdash_per_1k | 3.642 | 5.793 | -0.95 | 0.05 |
| colon_per_1k | 4.334 | 6.168 | -0.57 | 0.0 |
| semicolon_per_1k | 0.968 | 0.862 | 0.2 | 0.16 |
| paren_per_1k | 0.922 | 0.874 | -0.05 | 0.05 |
| question_per_100s | 1.979 | 3.561 | -0.69 | 0.0 |
| mattr500 | 0.485 | 0.545 | -1.81 | 0.47 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
