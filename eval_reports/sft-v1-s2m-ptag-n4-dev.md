# Eval: sft-v1-s2m-ptag-n4 on dev (2026-11-12T06:50:43)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2m-ptag-n4 | 154 | 85.1% | 98.0% | 83.1% | 9.1% | 2.33 | 0.946 | 0.0743 | 2.2 | 1.38 | 0.8 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.7625, 'ci95': [0.7003, 0.8232], 'chunks': 62, 'axis_means': {'m1': 0.8468, 'm15': 0.8266, 'm4': 0.8956}, 'gate_pass': 0.8952}
- M4_meaning: {'mis_restyle': {'mean': 0.923, 'median': 0.9459, 'n': 62}, 'facts_entailed': {'restyle': 0.9669, 'write': 0.8681}, 'm4': 0.8956}
- M5_entities: {'pass_rate': 0.8952, 'n': 124, 'missing': 11, 'added': 5}
- M9_memorization: {'max_span': 0, 'flagged': 0, 'n': 124, 'target_rebuilt': {'max_span': 17, 'median_span': 8, 'at_or_over_gate': 75}}
- M12_length: {'within_30pct': 0.9758, 'n': 124}
- fallback_rate: 0.129
- M1_by_op: {'restyle': 0.8205, 'write': 0.8816}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 15.315 | 14.714 | 0.48 | 0.05 |
| sent_len_sd | 7.365 | 9.326 | -2.33 | 0.68 |
| words_per_para | 42.296 | 33.735 | 1.91 | 0.37 |
| one_sent_para_share | 0.35 | 0.42 | -0.86 | 0.16 |
| sp_per_1k | 29.115 | 24.575 | 0.38 | 0.0 |
| emdash_per_1k | 3.944 | 5.793 | -0.85 | 0.05 |
| colon_per_1k | 5.039 | 6.168 | -0.37 | 0.0 |
| semicolon_per_1k | 1.436 | 0.862 | 0.81 | 0.21 |
| paren_per_1k | 0.456 | 0.874 | -0.42 | 0.0 |
| question_per_100s | 1.466 | 3.561 | -0.97 | 0.0 |
| mattr500 | 0.512 | 0.545 | 0.0 | 0.0 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
