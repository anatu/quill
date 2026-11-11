# Eval: sft-v1-s1p-fused8 on dev (2026-11-11T13:22:29)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p-fused8 | 154 | 68.2% | 91.6% | 59.7% | 24.0% | 2.75 | 0.987 | 0.0509 | 3.3 | 1.53 | 0.75 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.587, 'ci95': [0.5133, 0.6606], 'chunks': 62, 'axis_means': {'m1': 0.7016, 'm15': 0.5927, 'm4': 0.8906}, 'gate_pass': 0.8387}
- M4_meaning: {'mis_restyle': {'mean': 0.9207, 'median': 0.9488, 'n': 62}, 'facts_entailed': {'restyle': 0.96, 'write': 0.8605}, 'm4': 0.8906}
- M5_entities: {'pass_rate': 0.8387, 'n': 124, 'missing': 12, 'added': 11}
- M9_memorization: {'max_span': 9, 'flagged': 3, 'n': 124, 'target_rebuilt': {'max_span': 16, 'median_span': 8, 'at_or_over_gate': 63}}
- M12_length: {'within_30pct': 0.9597, 'n': 124}
- fallback_rate: 0.1935
- M1_by_op: {'restyle': 0.7089, 'write': 0.6533}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.324 | 14.714 | 0.49 | 0.0 |
| sent_len_sd | 6.976 | 9.326 | -2.74 | 0.84 |
| words_per_para | 48.813 | 33.735 | 2.75 | 0.68 |
| one_sent_para_share | 0.294 | 0.42 | -1.41 | 0.32 |
| sp_per_1k | 25.934 | 24.575 | 0.1 | 0.0 |
| emdash_per_1k | 2.953 | 5.793 | -1.29 | 0.16 |
| colon_per_1k | 5.173 | 6.168 | -0.36 | 0.0 |
| semicolon_per_1k | 2.152 | 0.862 | 1.9 | 0.47 |
| paren_per_1k | 0.458 | 0.874 | -0.4 | 0.0 |
| question_per_100s | 1.157 | 3.561 | -1.09 | 0.0 |
| mattr500 | 0.52 | 0.545 | 0.66 | 0.05 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
