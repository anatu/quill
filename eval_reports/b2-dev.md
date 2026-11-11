# Eval: b2 on dev (2026-11-10T18:43:24)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b2 | 81 | 0.0% | 0.0% | 0.0% | 95.1% | 6.49 | 1.087 | -0.0899 | 3.44 | 1.61 | 0.66 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.0, 'ci95': [0.0, 0.0], 'chunks': 62, 'axis_means': {'m1': 0.0, 'm15': 0.0, 'm4': 0.9348}, 'gate_pass': 1.0}
- M4_meaning: {'mis_restyle': {'mean': 0.9348, 'median': 0.9544, 'n': 62}, 'facts_entailed': {'restyle': 0.9714}, 'm4': 0.9348}
- M5_entities: {'pass_rate': 1.0, 'n': 62, 'missing': 0, 'added': 0}
- M9_memorization: {'max_span': 0, 'flagged': 0, 'n': 62, 'target_rebuilt': {'max_span': 0, 'median_span': 0, 'at_or_over_gate': 0}}
- M12_length: {'within_30pct': 1.0, 'n': 62}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 16.17 | 14.714 | 1.08 | 0.0 |
| sent_len_sd | 7.263 | 9.326 | -2.43 | 0.6 |
| words_per_para | 72.641 | 33.735 | 6.49 | 1.0 |
| one_sent_para_share | 0.024 | 0.42 | -3.83 | 1.0 |
| sp_per_1k | 24.813 | 24.575 | -0.03 | 0.0 |
| emdash_per_1k | 0.084 | 5.793 | -2.62 | 1.0 |
| colon_per_1k | 2.72 | 6.168 | -0.99 | 0.0 |
| semicolon_per_1k | 0.293 | 0.862 | -0.82 | 0.0 |
| paren_per_1k | 0.0 | 0.874 | -0.88 | 0.0 |
| question_per_100s | 1.015 | 3.561 | -1.11 | 0.0 |
| mattr500 | 0.547 | 0.545 | 0.56 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
