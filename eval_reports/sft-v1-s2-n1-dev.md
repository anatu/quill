# Eval: sft-v1-s2-n1 on dev (2026-11-11T20:29:53)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sft-v1-s2-n1 | 151 | 96.7% | 98.0% | 92.0% | 2.0% | 1.83 | 0.964 | 0.0786 | 1.64 | 1.32 | 1.1 |

- composite: {'axes': ['m1', 'm15', 'm4'], 'value': 0.5008, 'ci95': [0.4079, 0.5902], 'chunks': 62, 'axis_means': {'m1': 0.9677, 'm15': 0.9194, 'm4': 0.8657}, 'gate_pass': 0.5403}
- M4_meaning: {'mis_restyle': {'mean': 0.8694, 'median': 0.9237, 'n': 62}, 'facts_entailed': {'restyle': 0.8972, 'write': 0.8621}, 'm4': 0.8657}
- M5_entities: {'pass_rate': 0.5403, 'n': 124, 'missing': 45, 'added': 22}
- M9_memorization: {'max_span': 14, 'flagged': 8, 'n': 124, 'target_rebuilt': {'max_span': 24, 'median_span': 8, 'at_or_over_gate': 71}}
- M12_length: {'within_30pct': 0.9274, 'n': 124}
- fallback_rate: 0.5323
- M1_by_op: {'restyle': 0.9737, 'write': 0.96}

### Tic profile

| Feature | Value | Author | z | Pools with \|z\| > 2 |
|---|---|---|---|---|
| sent_len_mean | 13.712 | 14.714 | -0.69 | 0.05 |
| sent_len_sd | 8.898 | 9.326 | -1.02 | 0.53 |
| words_per_para | 34.64 | 33.735 | 0.54 | 0.32 |
| one_sent_para_share | 0.356 | 0.42 | -0.87 | 0.21 |
| sp_per_1k | 40.79 | 24.575 | 1.35 | 0.21 |
| emdash_per_1k | 2.875 | 5.793 | -1.33 | 0.26 |
| colon_per_1k | 4.161 | 6.168 | -0.57 | 0.0 |
| semicolon_per_1k | 0.351 | 0.862 | -0.76 | 0.0 |
| paren_per_1k | 0.234 | 0.874 | -0.64 | 0.0 |
| question_per_100s | 2.34 | 3.561 | -0.55 | 0.0 |
| mattr500 | 0.484 | 0.545 | -1.83 | 0.42 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
