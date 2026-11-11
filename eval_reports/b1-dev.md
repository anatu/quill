# Eval: b1 on dev (2026-11-11T00:05:02)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b1 | 154 | 21.4% | 33.8% | 16.2% | 77.3% | 4.79 | 1.065 | -0.0273 | 3.25 | 1.64 | 0.64 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.2561, 'ci95': [0.189, 0.3163], 'chunks': 62, 'axis_means': {'m1': 0.2258, 'm15': 0.1815, 'm4': 0.8697}, 'gate_pass': 0.879}
- M4_meaning: {'mis_restyle': {'mean': 0.9222, 'median': 0.954, 'n': 62}, 'facts_entailed': {'restyle': 0.9683, 'write': 0.8173}, 'm4': 0.8697}
- M5_entities: {'pass_rate': 0.879, 'n': 124, 'missing': 15, 'added': 4}
- M9_memorization: {'max_span': 0, 'flagged': 0, 'n': 124, 'target_rebuilt': {'max_span': 15, 'median_span': 0, 'at_or_over_gate': 10}}
- M12_length: {'within_30pct': 0.9758, 'n': 124}
- fallback_rate: 0.1452
- M1_by_op: {'restyle': 0.037, 'write': 0.411}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 13.934 | 14.714 | -0.5 | 0.05 |
| sent_len_sd | 6.941 | 9.326 | -2.85 | 0.89 |
| words_per_para | 61.358 | 33.735 | 4.79 | 0.89 |
| one_sent_para_share | 0.041 | 0.42 | -3.69 | 0.95 |
| sp_per_1k | 23.922 | 24.575 | -0.04 | 0.0 |
| emdash_per_1k | 0.816 | 5.793 | -2.29 | 0.79 |
| colon_per_1k | 4.92 | 6.168 | -0.34 | 0.0 |
| semicolon_per_1k | 1.725 | 0.862 | 1.29 | 0.37 |
| paren_per_1k | 0.256 | 0.874 | -0.62 | 0.0 |
| question_per_100s | 0.78 | 3.561 | -1.25 | 0.0 |
| mattr500 | 0.513 | 0.545 | 0.68 | 0.05 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
