# Eval: sft-v1-s2-mix30-n1 on dev (2026-11-12T00:38:34)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2-mix30-n1 | 155 | 92.9% | 97.4% | 85.2% | 5.2% | 2.14 | 0.944 | 0.0717 | 2.33 | 1.33 | 0.9 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.6314, 'ci95': [0.5521, 0.7054], 'chunks': 62, 'axis_means': {'m1': 0.9315, 'm15': 0.8589, 'm4': 0.8912}, 'gate_pass': 0.7177}
- M4_meaning: {'mis_restyle': {'mean': 0.9193, 'median': 0.9405, 'n': 62}, 'facts_entailed': {'restyle': 0.9573, 'write': 0.8632}, 'm4': 0.8912}
- M5_entities: {'pass_rate': 0.7177, 'n': 124, 'missing': 24, 'added': 15}
- M9_memorization: {'max_span': 11, 'flagged': 9, 'n': 124, 'target_rebuilt': {'max_span': 24, 'median_span': 8, 'at_or_over_gate': 73}}
- M12_length: {'within_30pct': 0.9758, 'n': 124}
- fallback_rate: 0.3548
- M1_by_op: {'restyle': 0.8974, 'write': 0.961}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 14.707 | 14.714 | 0.02 | 0.0 |
| sent_len_sd | 7.524 | 9.326 | -2.14 | 0.74 |
| words_per_para | 40.613 | 33.735 | 1.33 | 0.32 |
| one_sent_para_share | 0.34 | 0.42 | -0.97 | 0.26 |
| sp_per_1k | 34.389 | 24.575 | 0.8 | 0.0 |
| emdash_per_1k | 4.054 | 5.793 | -0.83 | 0.05 |
| colon_per_1k | 5.459 | 6.168 | -0.23 | 0.0 |
| semicolon_per_1k | 1.428 | 0.862 | 0.78 | 0.21 |
| paren_per_1k | 0.415 | 0.874 | -0.45 | 0.0 |
| question_per_100s | 1.762 | 3.561 | -0.81 | 0.0 |
| mattr500 | 0.508 | 0.545 | -0.25 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
