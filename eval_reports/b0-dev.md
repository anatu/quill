# Eval: b0 on dev (2026-11-10T09:36:06)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b0 | 156 | 23.7% | 44.2% | 8.3% | 72.4% | 3.62 | 1.014 | -0.0248 | 1.03 | 0.9 | 0.87 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.2515, 'ci95': [0.1704, 0.3274], 'chunks': 62, 'axis_means': {'m1': 0.246, 'm15': 0.0927, 'm4': 0.9351}, 'gate_pass': 0.8952}
- M4_meaning: {'mis_restyle': {'mean': 0.9004, 'median': 0.9421, 'n': 62}, 'facts_entailed': {'restyle': 0.9767, 'write': 0.9697}, 'm4': 0.9351}
- M5_entities: {'pass_rate': 0.8952, 'n': 124, 'missing': 7, 'added': 6}
- M9_memorization: {'max_span': 15, 'flagged': 9, 'n': 124, 'target_rebuilt': {'max_span': 25, 'median_span': 10, 'at_or_over_gate': 102}}
- M12_length: {'within_30pct': 1.0, 'n': 124}
- fallback_rate: 0.1613
- M1_by_op: {'restyle': 0.1899, 'write': 0.2857}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 9.907 | 14.714 | -3.62 | 1.0 |
| sent_len_sd | 6.205 | 9.326 | -3.58 | 1.0 |
| words_per_para | 21.548 | 33.735 | -1.97 | 0.48 |
| one_sent_para_share | 0.355 | 0.42 | -0.63 | 0.0 |
| sp_per_1k | 37.988 | 24.575 | 1.11 | 0.14 |
| emdash_per_1k | 2.005 | 5.793 | -1.74 | 0.43 |
| colon_per_1k | 5.508 | 6.168 | -0.2 | 0.0 |
| semicolon_per_1k | 0.106 | 0.862 | -1.12 | 0.0 |
| paren_per_1k | 0.042 | 0.874 | -0.84 | 0.0 |
| question_per_100s | 2.363 | 3.561 | -0.52 | 0.0 |
| mattr500 | 0.507 | 0.545 | -0.24 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
