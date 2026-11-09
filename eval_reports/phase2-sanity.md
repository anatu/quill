# Eval: sanity on dev (2026-11-09T14:57:42)

Split hash `bec0e58ea4a7`. Ratios (×) are against the author's held-out rate.

## Metric sanity (dev)

| Metric | Result | Bar | Pass |
|---|---|---|---|
| M1 AV AUC, author vs impostors | 0.9944 | ≥ 0.90 | True |
| M15 author share on author text; other classes called author | 1.0; over 20%: ['fs', 'llm', 'naval'] | ≥ 0.80; none [P] | False |
| M2 StyleDistance classifier AUC | 0.9939 | ≥ 0.80 | True |
| M6 tic profile, author max \|z\| | 1.6 | ≤ 2 | True |
| M8 signature rate, author vs impostors | 24.096 vs 7.277 | author higher | True |

- M1: ceiling accept 93.5%; impostor accept 3.3%; Claude controls accept 0.1667. Threshold 0.3936 (5% impostor false accepts in training CV).
- M1 impostor accept by author: {'batnick': 0.0, 'brown': 0.0, 'buffett': 0.0, 'carlson': 0.462, 'clear': 0.136, 'clements': 0.083, 'fried': 0.0, 'fs': 0.167, 'godin': 0.0, 'graham': 0.0, 'holiday': 0.333, 'kelly': 0.0, 'lamade': 0.0, 'maggiulli': 0.062, 'marks': 0.0, 'mckenzie': 0.0, 'naval': 0.25, 'sivers': 0.25, 'wiggins': 0.0}
- M15: {'author_share_on_author': 1.0, 'fs_recall': 0.0, 'fs_called_author': 0.833, 'fs_n': 6, 'lamade_recall': 0.94, 'lamade_called_author': 0.06, 'lamade_n': 50, 'llm_recall': 0.667, 'llm_called_author': 0.278, 'llm_n': 18, 'naval_recall': 0.375, 'naval_called_author': 0.625, 'naval_n': 8, 'classes_called_author_over_20pct': ['fs', 'llm', 'naval']}
- Delta: author dev 0.944; impostors 1.003.

## Within-author ceiling, topic-disjoint halves (train + dev)

- Halves: clusters [2, 3, 6, 7, 11] (142,246 words) vs [0, 4, 5, 9, 10, 12] (144,534 words).
- Delta A vs B: 0.765 (random halves on 2026-11-08: 0.753).
- StyleDistance AUC, n=20 per class: 0.475 ± 0.133 (random halves: 0.497).
- StyleDistance AUC, n=60 per class: 0.538 ± 0.07 (random halves: 0.497).

## Built-in systems (dev)

| System | Passages | M1 accept | M15 author | M15 LLM | Tic max \|z\| | Delta | M2 delta | M7 vocab × | M7 struct × | M8 × |
|---|---|---|---|---|---|---|---|---|---|---|
| human | 77 | 93.5% | 100.0% | 0.0% | 1.6 | 0.944 | 0.092 | 1.0 | 1.0 | 1.0 |
| impostor | 519 | 3.3% | 72.8% | 1.5% | 4.24 | 1.003 | 0.03 | 5.09 | 1.01 | 0.3 |
| llm | 43 | 7.0% | 11.6% | 86.1% | 2.63 | 0.969 | -0.0874 | 7.57 | 1.81 | 0.62 |

Not implemented yet: M3 LUAR; M4 MIS / fact entailment; M10 detector; M11 judge; M13 alpha; M14 residue; decision composite (needs M4); spaCy NER in M5.
