# Eval: sft-v1-s1 on dev (2026-11-10T21:36:02)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1 | 156 | 60.3% | 83.3% | 59.6% | 23.1% | 9.39 | 0.982 | 0.0319 | 3.54 | 1.55 | 0.78 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.4246, 'ci95': [0.3554, 0.4948], 'chunks': 62, 'axis_means': {'m1': 0.6156, 'm15': 0.5968, 'm4': 0.8663}, 'gate_pass': 0.6452}
- M4_meaning: {'mis_restyle': {'mean': 0.9269, 'median': 0.9478, 'n': 62}, 'facts_entailed': {'restyle': 0.9613, 'write': 0.8058}, 'm4': 0.8663}
- M5_entities: {'pass_rate': 0.6452, 'n': 124, 'missing': 36, 'added': 13}
- M9_memorization: {'max_span': 9, 'flagged': 3, 'n': 124, 'target_rebuilt': {'max_span': 17, 'median_span': 0, 'at_or_over_gate': 53}}
- M12_length: {'within_30pct': 0.9839, 'n': 124}
- fallback_rate: 0.3629
- M1_by_op: {'restyle': 0.6125, 'write': 0.5921}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.886 | 14.714 | 0.91 | 0.11 |
| sent_len_sd | 7.045 | 9.326 | -2.67 | 0.84 |
| words_per_para | 89.706 | 33.735 | 9.39 | 1.0 |
| one_sent_para_share | 0.018 | 0.42 | -3.88 | 1.0 |
| sp_per_1k | 24.973 | 24.575 | 0.01 | 0.0 |
| emdash_per_1k | 4.097 | 5.793 | -0.8 | 0.05 |
| colon_per_1k | 3.021 | 6.168 | -0.92 | 0.0 |
| semicolon_per_1k | 1.442 | 0.862 | 0.82 | 0.11 |
| paren_per_1k | 0.183 | 0.874 | -0.7 | 0.0 |
| question_per_100s | 1.055 | 3.561 | -1.11 | 0.0 |
| mattr500 | 0.519 | 0.545 | 0.27 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
