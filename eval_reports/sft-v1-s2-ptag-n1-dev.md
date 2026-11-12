# Eval: sft-v1-s2-ptag-n1 on dev (2026-11-11T23:57:22)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2-ptag-n1 | 156 | 99.4% | 98.7% | 94.2% | 0.6% | 2.01 | 0.987 | 0.0832 | 1.62 | 1.19 | 1.06 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5859, 'ci95': [0.5018, 0.6651], 'chunks': 62, 'axis_means': {'m1': 0.9919, 'm15': 0.9409, 'm4': 0.8548}, 'gate_pass': 0.6371}
- M4_meaning: {'mis_restyle': {'mean': 0.8564, 'median': 0.92, 'n': 62}, 'facts_entailed': {'restyle': 0.9232, 'write': 0.8531}, 'm4': 0.8548}
- M5_entities: {'pass_rate': 0.6371, 'n': 124, 'missing': 39, 'added': 14}
- M9_memorization: {'max_span': 14, 'flagged': 8, 'n': 124, 'target_rebuilt': {'max_span': 21, 'median_span': 9, 'at_or_over_gate': 92}}
- M12_length: {'within_30pct': 0.9516, 'n': 124}
- fallback_rate: 0.4355
- M1_by_op: {'restyle': 1.0, 'write': 0.987}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 13.817 | 14.714 | -0.66 | 0.0 |
| sent_len_sd | 7.966 | 9.326 | -1.64 | 0.3 |
| words_per_para | 34.328 | 33.735 | 0.33 | 0.05 |
| one_sent_para_share | 0.388 | 0.42 | -0.58 | 0.35 |
| sp_per_1k | 40.493 | 24.575 | 1.34 | 0.2 |
| emdash_per_1k | 3.227 | 5.793 | -1.18 | 0.05 |
| colon_per_1k | 4.908 | 6.168 | -0.37 | 0.0 |
| semicolon_per_1k | 0.704 | 0.862 | -0.22 | 0.1 |
| paren_per_1k | 0.227 | 0.874 | -0.65 | 0.0 |
| question_per_100s | 2.104 | 3.561 | -0.66 | 0.0 |
| mattr500 | 0.483 | 0.545 | -2.01 | 0.45 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
