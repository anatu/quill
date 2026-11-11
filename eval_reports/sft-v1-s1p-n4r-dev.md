# Eval: sft-v1-s1p-n4r on dev (2026-11-11T11:10:57)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p-n4r | 156 | 72.4% | 96.8% | 62.8% | 23.7% | 2.66 | 0.988 | 0.0667 | 3.27 | 1.47 | 0.74 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.6807, 'ci95': [0.6137, 0.7444], 'chunks': 62, 'axis_means': {'m1': 0.7366, 'm15': 0.6438, 'm4': 0.889}, 'gate_pass': 0.9274}
- M4_meaning: {'mis_restyle': {'mean': 0.9191, 'median': 0.9469, 'n': 62}, 'facts_entailed': {'restyle': 0.9613, 'write': 0.859}, 'm4': 0.889}
- M5_entities: {'pass_rate': 0.9274, 'n': 124, 'missing': 8, 'added': 1}
- M9_memorization: {'max_span': 0, 'flagged': 0, 'n': 124, 'target_rebuilt': {'max_span': 16, 'median_span': 0, 'at_or_over_gate': 61}}
- M12_length: {'within_30pct': 0.9677, 'n': 124}
- fallback_rate: 0.1048
- M1_by_op: {'restyle': 0.675, 'write': 0.7763}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.311 | 14.714 | 0.46 | 0.0 |
| sent_len_sd | 7.069 | 9.326 | -2.66 | 0.79 |
| words_per_para | 38.829 | 33.735 | 1.17 | 0.16 |
| one_sent_para_share | 0.421 | 0.42 | -0.26 | 0.16 |
| sp_per_1k | 25.136 | 24.575 | 0.04 | 0.0 |
| emdash_per_1k | 2.793 | 5.793 | -1.36 | 0.21 |
| colon_per_1k | 4.578 | 6.168 | -0.47 | 0.0 |
| semicolon_per_1k | 1.808 | 0.862 | 1.38 | 0.32 |
| paren_per_1k | 0.458 | 0.874 | -0.4 | 0.0 |
| question_per_100s | 1.192 | 3.561 | -1.06 | 0.0 |
| mattr500 | 0.521 | 0.545 | 0.69 | 0.11 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
