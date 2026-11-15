# Eval: bt on dev (2026-11-15T11:29:52)

Split hash `01d1b806b169`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bt | 46 | 4.3% | 4.3% | 0.0% | 100.0% | 3.14 | 0.774 | -0.0061 | 1.33 | 2.25 | 0.92 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.0, 'ci95': [0.0, 0.0], 'chunks': 34, 'axis_means': {'m1': 0.0441, 'm15': 0.0, 'm4': 0.9221}, 'gate_pass': 0.5294}
- M4_meaning: {'mis_restyle': None, 'facts_entailed': {'write': 0.9221}, 'm4': 0.9221}
- M5_entities: {'pass_rate': 0.5294, 'n': 34, 'missing': 8, 'added': 10}
- M9_memorization: {'max_span': 9, 'flagged': 2, 'n': 34, 'target_rebuilt': {'max_span': 27, 'median_span': 10, 'at_or_over_gate': 29}}
- M12_length: {'within_30pct': 1.0, 'n': 34}
- fallback_rate: 0.5294

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 17.844 | 22.59 | -2.91 | 1.0 |
| sent_len_sd | 7.663 | 11.638 | -3.14 | 1.0 |
| words_per_para | 98.73 | 83.578 | 1.04 | 0.0 |
| one_sent_para_share | 0.0 | 0.223 | -2.45 | 1.0 |
| sp_per_1k | 0.074 | 2.786 | -0.93 | 0.0 |
| emdash_per_1k | 0.0 | 3.163 | -2.1 | 1.0 |
| colon_per_1k | 2.218 | 1.854 | 0.33 | 0.17 |
| semicolon_per_1k | 0.518 | 2.114 | -1.53 | 0.33 |
| paren_per_1k | 6.58 | 8.286 | -0.58 | 0.5 |
| question_per_100s | 0.264 | 1.139 | -0.65 | 0.0 |
| mattr500 | 0.475 | 0.46 | 1.33 | 0.17 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
