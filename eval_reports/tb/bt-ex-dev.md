# Eval: bt-ex on dev (2026-11-15T11:33:35)

Split hash `01d1b806b169`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bt-ex | 45 | 37.8% | 40.0% | 17.8% | 82.2% | 2.41 | 0.719 | -0.0054 | 0.98 | 1.61 | 0.96 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.2818, 'ci95': [0.1555, 0.4123], 'chunks': 34, 'axis_means': {'m1': 0.3676, 'm15': 0.1765, 'm4': 0.9117}, 'gate_pass': 0.5294}
- M4_meaning: {'mis_restyle': None, 'facts_entailed': {'write': 0.9117}, 'm4': 0.9117}
- M5_entities: {'pass_rate': 0.5294, 'n': 34, 'missing': 9, 'added': 11}
- M9_memorization: {'max_span': 8, 'flagged': 1, 'n': 34, 'target_rebuilt': {'max_span': 262, 'median_span': 24, 'at_or_over_gate': 34}}
- M12_length: {'within_30pct': 1.0, 'n': 34}
- fallback_rate: 0.5

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 19.403 | 22.59 | -1.92 | 0.5 |
| sent_len_sd | 8.635 | 11.638 | -2.41 | 0.67 |
| words_per_para | 108.016 | 83.578 | 1.74 | 0.5 |
| one_sent_para_share | 0.016 | 0.223 | -2.29 | 0.83 |
| sp_per_1k | 0.364 | 2.786 | -0.83 | 0.0 |
| emdash_per_1k | 0.0 | 3.163 | -2.1 | 1.0 |
| colon_per_1k | 2.916 | 1.854 | 0.92 | 0.17 |
| semicolon_per_1k | 1.166 | 2.114 | -0.91 | 0.17 |
| paren_per_1k | 8.456 | 8.286 | 0.05 | 0.17 |
| question_per_100s | 0.283 | 1.139 | -0.65 | 0.0 |
| mattr500 | 0.458 | 0.46 | 0.39 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
