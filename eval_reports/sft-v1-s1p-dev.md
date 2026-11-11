# Eval: sft-v1-s1p on dev (2026-11-11T07:33:41)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p | 156 | 71.2% | 89.1% | 60.9% | 24.4% | 3.37 | 0.989 | 0.0386 | 3.73 | 1.55 | 0.81 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.4428, 'ci95': [0.3724, 0.5147], 'chunks': 62, 'axis_means': {'m1': 0.6922, 'm15': 0.5995, 'm4': 0.8582}, 'gate_pass': 0.6694}
- M4_meaning: {'mis_restyle': {'mean': 0.9146, 'median': 0.9507, 'n': 62}, 'facts_entailed': {'restyle': 0.9665, 'write': 0.8018}, 'm4': 0.8582}
- M5_entities: {'pass_rate': 0.6694, 'n': 124, 'missing': 34, 'added': 11}
- M9_memorization: {'max_span': 8, 'flagged': 3, 'n': 124, 'target_rebuilt': {'max_span': 16, 'median_span': 0, 'at_or_over_gate': 54}}
- M12_length: {'within_30pct': 1.0, 'n': 124}
- fallback_rate: 0.3468
- M1_by_op: {'restyle': 0.625, 'write': 0.8026}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.872 | 14.714 | 0.9 | 0.05 |
| sent_len_sd | 7.107 | 9.326 | -2.59 | 0.89 |
| words_per_para | 51.852 | 33.735 | 3.37 | 0.79 |
| one_sent_para_share | 0.261 | 0.42 | -1.8 | 0.47 |
| sp_per_1k | 25.554 | 24.575 | 0.06 | 0.0 |
| emdash_per_1k | 3.752 | 5.793 | -0.94 | 0.05 |
| colon_per_1k | 3.088 | 6.168 | -0.87 | 0.0 |
| semicolon_per_1k | 1.418 | 0.862 | 0.8 | 0.26 |
| paren_per_1k | 0.16 | 0.874 | -0.72 | 0.0 |
| question_per_100s | 0.944 | 3.561 | -1.16 | 0.0 |
| mattr500 | 0.519 | 0.545 | 0.28 | 0.05 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
