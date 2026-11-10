# M10 Fast-DetectGPT on dev (2026-11-10T09:32:45)

Analytic Fast-DetectGPT with gpt-neo-2.7B. Higher scores read as machine text. The flag threshold passes 5% of the author's train passages. AUC: each set against the author's held-out passages; the bar for machine text is 0.80.

| Set | Passages | Mean score | Flagged | AUC vs author |
|---|---|---|---|---|
| author, held out | 77 | 0.03 | 5.2% |  |
| b0 | 156 | 0.057 | 7.7% | 0.5009 |
| b1 | 183 | 0.212 | 15.8% | 0.4926 |
| b2 | 81 | -0.334 | 4.9% | 0.3957 |
| Claude controls (older model) | 43 | 1.77 | 58.1% | 0.9139 |
| other human authors | 519 | -0.402 | 8.1% | 0.3933 |

FAILS: it cannot tell current Claude or local-model output from the author. Dropped until Phase 2b decides on a trained detector (M10b).
