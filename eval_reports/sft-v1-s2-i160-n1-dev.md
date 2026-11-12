# Eval: sft-v1-s2-i160-n1 on dev (2026-11-11T23:16:30)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2-i160-n1 | 153 | 90.2% | 96.7% | 85.0% | 3.9% | 2.51 | 0.999 | 0.0658 | 2.32 | 1.28 | 0.88 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5003, 'ci95': [0.4191, 0.5809], 'chunks': 62, 'axis_means': {'m1': 0.9073, 'm15': 0.8427, 'm4': 0.8342}, 'gate_pass': 0.5968}
- M4_meaning: {'mis_restyle': {'mean': 0.8286, 'median': 0.9298, 'n': 62}, 'facts_entailed': {'restyle': 0.8798, 'write': 0.8398}, 'm4': 0.8342}
- M5_entities: {'pass_rate': 0.5968, 'n': 124, 'missing': 43, 'added': 16}
- M9_memorization: {'max_span': 9, 'flagged': 4, 'n': 124, 'target_rebuilt': {'max_span': 23, 'median_span': 8, 'at_or_over_gate': 79}}
- M12_length: {'within_30pct': 0.8952, 'n': 124}
- fallback_rate: 0.4597
- M1_by_op: {'restyle': 0.9103, 'write': 0.8933}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 13.538 | 14.714 | -0.84 | 0.11 |
| sent_len_sd | 7.198 | 9.326 | -2.51 | 0.74 |
| words_per_para | 38.489 | 33.735 | 1.05 | 0.26 |
| one_sent_para_share | 0.295 | 0.42 | -1.39 | 0.21 |
| sp_per_1k | 36.683 | 24.575 | 1.02 | 0.21 |
| emdash_per_1k | 1.898 | 5.793 | -1.78 | 0.42 |
| colon_per_1k | 4.461 | 6.168 | -0.5 | 0.0 |
| semicolon_per_1k | 0.712 | 0.862 | -0.22 | 0.0 |
| paren_per_1k | 0.332 | 0.874 | -0.54 | 0.0 |
| question_per_100s | 1.863 | 3.561 | -0.78 | 0.0 |
| mattr500 | 0.495 | 0.545 | -1.24 | 0.21 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
