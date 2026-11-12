# Eval: sft-v1-s2-n4 on dev (2026-11-11T20:21:52)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2-n4 | 155 | 98.1% | 99.4% | 91.6% | 1.9% | 1.84 | 0.988 | 0.0962 | 1.57 | 1.33 | 1.06 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.7309, 'ci95': [0.6514, 0.8017], 'chunks': 62, 'axis_means': {'m1': 0.9839, 'm15': 0.9153, 'm4': 0.8725}, 'gate_pass': 0.7984}
- M4_meaning: {'mis_restyle': {'mean': 0.8981, 'median': 0.9219, 'n': 62}, 'facts_entailed': {'restyle': 0.9235, 'write': 0.847}, 'm4': 0.8725}
- M5_entities: {'pass_rate': 0.7984, 'n': 124, 'missing': 23, 'added': 7}
- M9_memorization: {'max_span': 11, 'flagged': 1, 'n': 124, 'target_rebuilt': {'max_span': 19, 'median_span': 9, 'at_or_over_gate': 85}}
- M12_length: {'within_30pct': 0.9839, 'n': 124}
- fallback_rate: 0.2258
- M1_by_op: {'restyle': 0.962, 'write': 1.0}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 13.443 | 14.714 | -0.94 | 0.05 |
| sent_len_sd | 7.904 | 9.326 | -1.69 | 0.37 |
| words_per_para | 30.447 | 33.735 | -0.36 | 0.0 |
| one_sent_para_share | 0.411 | 0.42 | -0.29 | 0.16 |
| sp_per_1k | 41.915 | 24.575 | 1.43 | 0.37 |
| emdash_per_1k | 3.324 | 5.793 | -1.14 | 0.21 |
| colon_per_1k | 5.447 | 6.168 | -0.21 | 0.0 |
| semicolon_per_1k | 0.508 | 0.862 | -0.5 | 0.05 |
| paren_per_1k | 0.439 | 0.874 | -0.44 | 0.05 |
| question_per_100s | 2.575 | 3.561 | -0.45 | 0.0 |
| mattr500 | 0.485 | 0.545 | -1.84 | 0.53 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
