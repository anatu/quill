# Eval: sft-v1-s1p-n1r on dev (2026-11-11T20:35:47)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p-n1r | 156 | 67.3% | 94.9% | 55.8% | 30.1% | 2.67 | 0.997 | 0.0517 | 3.23 | 1.52 | 0.74 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5654, 'ci95': [0.5021, 0.6332], 'chunks': 62, 'axis_means': {'m1': 0.668, 'm15': 0.5591, 'm4': 0.8902}, 'gate_pass': 0.8629}
- M4_meaning: {'mis_restyle': {'mean': 0.9146, 'median': 0.9507, 'n': 62}, 'facts_entailed': {'restyle': 0.9665, 'write': 0.8657}, 'm4': 0.8902}
- M5_entities: {'pass_rate': 0.8629, 'n': 124, 'missing': 11, 'added': 7}
- M9_memorization: {'max_span': 8, 'flagged': 2, 'n': 124, 'target_rebuilt': {'max_span': 16, 'median_span': 0, 'at_or_over_gate': 56}}
- M12_length: {'within_30pct': 0.9677, 'n': 124}
- fallback_rate: 0.1774
- M1_by_op: {'restyle': 0.625, 'write': 0.7237}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.465 | 14.714 | 0.59 | 0.0 |
| sent_len_sd | 7.032 | 9.326 | -2.67 | 0.84 |
| words_per_para | 45.325 | 33.735 | 2.42 | 0.63 |
| one_sent_para_share | 0.353 | 0.42 | -1.06 | 0.42 |
| sp_per_1k | 25.888 | 24.575 | 0.09 | 0.0 |
| emdash_per_1k | 2.892 | 5.793 | -1.31 | 0.11 |
| colon_per_1k | 4.69 | 6.168 | -0.42 | 0.0 |
| semicolon_per_1k | 1.662 | 0.862 | 1.19 | 0.37 |
| paren_per_1k | 0.364 | 0.874 | -0.5 | 0.0 |
| question_per_100s | 1.092 | 3.561 | -1.09 | 0.0 |
| mattr500 | 0.519 | 0.545 | 0.6 | 0.05 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
