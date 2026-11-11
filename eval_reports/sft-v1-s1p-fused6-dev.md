# Eval: sft-v1-s1p-fused6 on dev (2026-11-11T14:00:27)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p-fused6 | 154 | 78.6% | 94.2% | 66.9% | 20.1% | 2.49 | 0.974 | 0.0561 | 3.35 | 1.5 | 0.77 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.6554, 'ci95': [0.5882, 0.7212], 'chunks': 62, 'axis_means': {'m1': 0.7863, 'm15': 0.6573, 'm4': 0.889}, 'gate_pass': 0.8629}
- M4_meaning: {'mis_restyle': {'mean': 0.9201, 'median': 0.9471, 'n': 62}, 'facts_entailed': {'restyle': 0.9686, 'write': 0.8579}, 'm4': 0.889}
- M5_entities: {'pass_rate': 0.8629, 'n': 124, 'missing': 11, 'added': 8}
- M9_memorization: {'max_span': 9, 'flagged': 2, 'n': 124, 'target_rebuilt': {'max_span': 17, 'median_span': 8, 'at_or_over_gate': 68}}
- M12_length: {'within_30pct': 0.9758, 'n': 124}
- fallback_rate: 0.1613
- M1_by_op: {'restyle': 0.7821, 'write': 0.7895}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.4 | 14.714 | 0.53 | 0.0 |
| sent_len_sd | 7.212 | 9.326 | -2.49 | 0.74 |
| words_per_para | 43.378 | 33.735 | 2.12 | 0.53 |
| one_sent_para_share | 0.366 | 0.42 | -0.93 | 0.26 |
| sp_per_1k | 26.551 | 24.575 | 0.15 | 0.0 |
| emdash_per_1k | 3.475 | 5.793 | -1.04 | 0.11 |
| colon_per_1k | 4.611 | 6.168 | -0.49 | 0.0 |
| semicolon_per_1k | 1.772 | 0.862 | 1.35 | 0.37 |
| paren_per_1k | 0.363 | 0.874 | -0.51 | 0.0 |
| question_per_100s | 1.189 | 3.561 | -1.07 | 0.0 |
| mattr500 | 0.517 | 0.545 | 0.53 | 0.05 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
