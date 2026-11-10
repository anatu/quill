# Eval: sanity on dev (2026-11-10T09:24:41)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

## Metric sanity (dev)

| Metric | Result | Bar | Pass |
|---|---|---|---|
| M1 AV AUC, author vs impostors | 0.9925 | ≥ 0.90 | True |
| M15 author share on author text; other classes called author | 0.8831; over 20%: none | ≥ 0.80; none [P] | True |
| M2 StyleDistance classifier AUC | 0.9941 | ≥ 0.80 | True |
| M6 tic profile, author max \|z\| | 1.6 | ≤ 2 | True |
| M8 signature rate, author vs impostors | 24.097 vs 7.277 | author higher | True |

- M1: ceiling accept 94.8%; impostor accept 5.0%; Claude controls accept 0.1111. Threshold 0.2991 (5% false accepts on the training negatives, in CV; negatives: {'impostor_passages': 1818, 'draft_passages': 933}).
- M1 impostor accept by author: {'batnick': 0.0, 'brown': 0.333, 'buffett': 0.0, 'carlson': 0.538, 'clear': 0.091, 'clements': 0.083, 'fried': 0.0, 'fs': 0.333, 'godin': 0.0, 'graham': 0.0, 'holiday': 0.333, 'kelly': 0.0, 'lamade': 0.0, 'maggiulli': 0.062, 'marks': 0.042, 'mckenzie': 0.0, 'naval': 0.75, 'sivers': 0.5, 'wiggins': 0.0}
- M15: {'author_share_on_author': 0.8831, 'lamade_recall': 0.74, 'lamade_called_author': 0.0, 'lamade_n': 50, 'llm_recall': 0.875, 'llm_called_author': 0.125, 'llm_n': 8, 'other_recall': 0.977, 'other_called_author': 0.015, 'other_n': 469, 'classes_called_author_over_20pct': []}
- Delta: author dev 0.944; impostors 1.003.

## Within-author ceiling, topic-disjoint halves (train + dev)

- Halves: clusters [2, 3, 6, 7, 11] (142,113 words) vs [0, 4, 5, 9, 10, 12] (144,315 words).
- Delta A vs B: 0.765 (random halves on 2026-11-08: 0.753).
- StyleDistance AUC, n=20 per class: 0.486 ± 0.128 (random halves: 0.497).
- StyleDistance AUC, n=60 per class: 0.515 ± 0.05 (random halves: 0.497).

## Built-in systems (dev)

| System | Passages | M1 accept | M2 clf accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| human | 77 | 94.8% | 98.7% | 88.3% | 1.3% | 1.6 | 0.944 | 0.094 | 1.0 | 1.0 | 1.0 |
| impostor | 519 | 5.0% | 5.4% | 1.4% | 1.0% | 4.95 | 1.003 | 0.0204 | 5.09 | 1.01 | 0.3 |
| llm | 43 | 4.7% | 0.0% | 2.3% | 93.0% | 2.66 | 0.97 | -0.074 | 7.57 | 1.81 | 0.62 |

Not implemented yet: M13 alpha; M14 residue (both Phase 2b).
Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
