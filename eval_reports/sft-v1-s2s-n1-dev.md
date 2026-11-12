# Eval: sft-v1-s2s-n1 on dev (2026-11-11T22:36:42)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2s-n1 | 156 | 98.1% | 98.7% | 91.0% | 0.6% | 1.95 | 1.005 | 0.0851 | 1.11 | 1.11 | 1.07 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5425, 'ci95': [0.458, 0.6259], 'chunks': 62, 'axis_means': {'m1': 0.9839, 'm15': 0.9046, 'm4': 0.8404}, 'gate_pass': 0.6048}
- M4_meaning: {'mis_restyle': {'mean': 0.857, 'median': 0.9153, 'n': 62}, 'facts_entailed': {'restyle': 0.9064, 'write': 0.8238}, 'm4': 0.8404}
- M5_entities: {'pass_rate': 0.6048, 'n': 124, 'missing': 41, 'added': 19}
- M9_memorization: {'max_span': 14, 'flagged': 13, 'n': 124, 'target_rebuilt': {'max_span': 21, 'median_span': 9, 'at_or_over_gate': 84}}
- M12_length: {'within_30pct': 0.9516, 'n': 124}
- fallback_rate: 0.4758
- M1_by_op: {'restyle': 0.9875, 'write': 0.9737}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 13.454 | 14.714 | -0.91 | 0.05 |
| sent_len_sd | 7.78 | 9.326 | -1.82 | 0.5 |
| words_per_para | 32.987 | 33.735 | 0.09 | 0.1 |
| one_sent_para_share | 0.389 | 0.42 | -0.48 | 0.05 |
| sp_per_1k | 43.785 | 24.575 | 1.6 | 0.25 |
| emdash_per_1k | 3.715 | 5.793 | -0.92 | 0.05 |
| colon_per_1k | 4.855 | 6.168 | -0.4 | 0.0 |
| semicolon_per_1k | 0.593 | 0.862 | -0.38 | 0.0 |
| paren_per_1k | 0.433 | 0.874 | -0.45 | 0.0 |
| question_per_100s | 2.423 | 3.561 | -0.52 | 0.0 |
| mattr500 | 0.484 | 0.545 | -1.95 | 0.5 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
