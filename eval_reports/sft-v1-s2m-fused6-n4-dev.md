# Eval: sft-v1-s2m-fused6-n4 on dev (2026-11-12T09:18:01)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2m-fused6-n4 | 156 | 89.1% | 98.7% | 81.4% | 9.6% | 2.32 | 0.934 | 0.0757 | 2.08 | 1.45 | 0.81 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.7821, 'ci95': [0.7303, 0.8352], 'chunks': 62, 'axis_means': {'m1': 0.9032, 'm15': 0.8065, 'm4': 0.8988}, 'gate_pass': 0.9113}
- M4_meaning: {'mis_restyle': {'mean': 0.9258, 'median': 0.9425, 'n': 62}, 'facts_entailed': {'restyle': 0.9667, 'write': 0.8718}, 'm4': 0.8988}
- M5_entities: {'pass_rate': 0.9113, 'n': 124, 'missing': 10, 'added': 2}
- M9_memorization: {'max_span': 0, 'flagged': 0, 'n': 124, 'target_rebuilt': {'max_span': 17, 'median_span': 9, 'at_or_over_gate': 87}}
- M12_length: {'within_30pct': 0.9919, 'n': 124}
- fallback_rate: 0.0968
- M1_by_op: {'restyle': 0.8734, 'write': 0.9091}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.123 | 14.714 | 0.33 | 0.0 |
| sent_len_sd | 7.358 | 9.326 | -2.32 | 0.74 |
| words_per_para | 37.301 | 33.735 | 0.74 | 0.11 |
| one_sent_para_share | 0.414 | 0.42 | -0.15 | 0.05 |
| sp_per_1k | 29.292 | 24.575 | 0.39 | 0.0 |
| emdash_per_1k | 3.725 | 5.793 | -0.9 | 0.05 |
| colon_per_1k | 4.483 | 6.168 | -0.49 | 0.0 |
| semicolon_per_1k | 1.517 | 0.862 | 1.0 | 0.32 |
| paren_per_1k | 0.368 | 0.874 | -0.52 | 0.0 |
| question_per_100s | 1.46 | 3.561 | -0.95 | 0.0 |
| mattr500 | 0.512 | 0.545 | 0.09 | 0.05 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
