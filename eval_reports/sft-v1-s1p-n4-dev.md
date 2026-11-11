# Eval: sft-v1-s1p-n4 on dev (2026-11-11T09:19:08)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p-n4 | 155 | 76.1% | 93.5% | 68.4% | 16.8% | 2.51 | 0.978 | 0.0555 | 3.7 | 1.62 | 0.81 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5078, 'ci95': [0.441, 0.5719], 'chunks': 62, 'axis_means': {'m1': 0.7728, 'm15': 0.6962, 'm4': 0.8479}, 'gate_pass': 0.7016}
- M4_meaning: {'mis_restyle': {'mean': 0.9191, 'median': 0.9469, 'n': 62}, 'facts_entailed': {'restyle': 0.9613, 'write': 0.7767}, 'm4': 0.8479}
- M5_entities: {'pass_rate': 0.7016, 'n': 124, 'missing': 33, 'added': 7}
- M9_memorization: {'max_span': 8, 'flagged': 1, 'n': 124, 'target_rebuilt': {'max_span': 14, 'median_span': 0, 'at_or_over_gate': 53}}
- M12_length: {'within_30pct': 1.0, 'n': 124}
- fallback_rate: 0.2984
- M1_by_op: {'restyle': 0.675, 'write': 0.8533}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.833 | 14.714 | 0.86 | 0.05 |
| sent_len_sd | 7.185 | 9.326 | -2.51 | 0.74 |
| words_per_para | 43.49 | 33.735 | 1.97 | 0.47 |
| one_sent_para_share | 0.372 | 0.42 | -0.8 | 0.26 |
| sp_per_1k | 25.433 | 24.575 | 0.05 | 0.0 |
| emdash_per_1k | 3.591 | 5.793 | -1.02 | 0.05 |
| colon_per_1k | 2.808 | 6.168 | -0.94 | 0.0 |
| semicolon_per_1k | 1.427 | 0.862 | 0.79 | 0.11 |
| paren_per_1k | 0.23 | 0.874 | -0.65 | 0.0 |
| question_per_100s | 1.093 | 3.561 | -1.1 | 0.0 |
| mattr500 | 0.52 | 0.545 | 0.29 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
