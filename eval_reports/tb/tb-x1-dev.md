# Eval: tb-x1 on dev (2026-11-15T11:26:23)

Split hash `01d1b806b169`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| tb-x1 | 40 | 97.5% | 95.0% | 97.5% | 2.5% | 1.97 | 0.724 | 0.0081 | 0.96 | 1.89 | 1.2 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.4889, 'ci95': [0.351, 0.6388], 'chunks': 34, 'axis_means': {'m1': 0.9853, 'm15': 0.9706, 'm4': 0.7033}, 'gate_pass': 0.5588}
- M4_meaning: {'mis_restyle': None, 'facts_entailed': {'write': 0.7033}, 'm4': 0.7033}
- M5_entities: {'pass_rate': 0.5588, 'n': 34, 'missing': 14, 'added': 10}
- M9_memorization: {'max_span': 8, 'flagged': 1, 'n': 34, 'target_rebuilt': {'max_span': 16, 'median_span': 8, 'at_or_over_gate': 19}}
- M12_length: {'within_30pct': 0.9412, 'n': 34}
- fallback_rate: 0.5294

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 19.377 | 22.59 | -1.97 | 0.6 |
| sent_len_sd | 9.981 | 11.638 | -1.38 | 0.4 |
| words_per_para | 84.211 | 83.578 | 0.1 | 0.0 |
| one_sent_para_share | 0.203 | 0.223 | -0.27 | 0.0 |
| sp_per_1k | 3.393 | 2.786 | 0.17 | 0.0 |
| emdash_per_1k | 0.982 | 3.163 | -1.45 | 0.2 |
| colon_per_1k | 1.875 | 1.854 | 0.02 | 0.0 |
| semicolon_per_1k | 1.607 | 2.114 | -0.42 | 0.0 |
| paren_per_1k | 10.268 | 8.286 | 0.71 | 0.2 |
| question_per_100s | 1.211 | 1.139 | 0.1 | 0.2 |
| mattr500 | 0.41 | 0.46 | -1.32 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
