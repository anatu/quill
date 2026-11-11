# Eval: sft-v1-s1p-fused-n4 on dev (2026-11-11T12:43:41)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s1p-fused-n4 | 156 | 7.7% | 39.7% | 3.9% | 84.6% | 8.79 | 1.092 | -0.0348 | 4.52 | 1.7 | 0.6 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.0975, 'ci95': [0.0, 0.1439], 'chunks': 62, 'axis_means': {'m1': 0.0645, 'm15': 0.0282, 'm4': 0.8807}, 'gate_pass': 0.9274}
- M4_meaning: {'mis_restyle': {'mean': 0.9294, 'median': 0.9519, 'n': 62}, 'facts_entailed': {'restyle': 0.9701, 'write': 0.8319}, 'm4': 0.8807}
- M5_entities: {'pass_rate': 0.9274, 'n': 124, 'missing': 8, 'added': 2}
- M9_memorization: {'max_span': 0, 'flagged': 0, 'n': 124, 'target_rebuilt': {'max_span': 14, 'median_span': 0, 'at_or_over_gate': 16}}
- M12_length: {'within_30pct': 0.9758, 'n': 124}
- fallback_rate: 0.0968
- M1_by_op: {'restyle': 0.0494, 'write': 0.1067}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.731 | 14.714 | 0.77 | 0.0 |
| sent_len_sd | 6.802 | 9.326 | -2.95 | 0.95 |
| words_per_para | 82.076 | 33.735 | 8.79 | 1.0 |
| one_sent_para_share | 0.076 | 0.42 | -3.59 | 0.95 |
| sp_per_1k | 19.746 | 24.575 | -0.41 | 0.0 |
| emdash_per_1k | 0.471 | 5.793 | -2.45 | 0.95 |
| colon_per_1k | 4.218 | 6.168 | -0.58 | 0.0 |
| semicolon_per_1k | 1.593 | 0.862 | 1.07 | 0.2 |
| paren_per_1k | 0.337 | 0.874 | -0.54 | 0.0 |
| question_per_100s | 0.847 | 3.561 | -1.2 | 0.0 |
| mattr500 | 0.517 | 0.545 | 0.67 | 0.1 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
