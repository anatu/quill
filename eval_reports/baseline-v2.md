# Baseline v2: Phase 2 exit report, dev (2026-11-10T18:43:30)

Split hash `bec0e58ea4a7`. Aggregate numbers only. The test split is untouched.

## Exit gate

| Check | Result | Detail |
|---|---|---|
| AV AUC >= 0.90 on dev | pass | 0.9925 |
| M15 passes sanity or is dropped | pass | passes |
| Embedding metrics pass sanity or are dropped | pass | StyleDistance classifier AUC 0.9941 |
| Topic-disjoint ceiling and split hash recorded | pass | bec0e58ea4a7 |
| B0 and B1 scored | pass | dev |

## Systems

| System | Composite [95% CI] | M1 accept | M2 clf accept | M15 author | M4 | Entities pass | Tic max \|z\| | Fallback |
|---|---|---|---|---|---|---|---|---|
| author, held out (ceiling) | | 94.8% | 98.7% | 88.3% | | | 1.6 | |
| b0 | 0.2515 [0.1704, 0.3274] | 23.7% | 44.2% | 8.3% | 0.9351 | 89.5% | 3.62 | 16.1% |
| b1 | 0.0567 [0.0, 0.1002] | 1.6% | 2.2% | 1.1% | 0.8197 | 91.1% | 3.54 | 25.8% |
| b2 | 0.0 [0.0, 0.0] | 0.0% | 0.0% | 0.0% | 0.9348 | 100.0% | 6.49 |  |
| other human authors | | 5.0% | 5.4% | 1.4% | | | 4.95 | |

Composite: geometric mean of ['m1', 'm15', 'm4'], entity gate first. M4 is MIS against the input for `restyle` and the share of facts entailed for `write`.

Paired composite differences (bootstrap over chunks):

- b0 - b1: +0.1948, 95% CI [0.1116, 0.2902]
- b0 - b2: +0.2515, 95% CI [0.1704, 0.3274]
- b1 - b2: +0.0567, 95% CI [0.0, 0.1002]

## Recall probe, untuned base

186 prompts; longest verbatim span 12 words; 15 at or over the 8-word gate.

## M11 judge (diagnostic)

Validation, real over impostor: 100.0% (pass). real vs b0: 32-1 (7 inconsistent). real vs b1: 40-0 (0 inconsistent). b0 vs b1: 40-0 (0 inconsistent).

## M10 detector

Fails sanity: b0 AUC 0.5009; b1 AUC 0.4926; b2 AUC 0.3957; Claude controls (older model) AUC 0.9139; other human authors AUC 0.3933.

Dropped: M10 Fast-DetectGPT: fails sanity on dev (eval_reports/m10-dev.md).
Not built (Phase 2b): M13 alpha; M14 residue (both Phase 2b).
Waiting on the user: coverage-probe briefs; blind reads (the kit is built).
