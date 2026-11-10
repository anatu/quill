# M11 judge on dev (2026-11-10T09:14:11)

Model claude-sonnet-5-5. Each pair is asked in both orders; a win needs the same pick both times. The judge is valid if it picks the author's real passage over a human impostor's on at least 75% of pairs. Diagnostic only. The judge is a Claude model, and b0 is Claude output.

| Comparison (x vs y) | Pairs | x wins | y wins | Inconsistent | x share |
|---|---|---|---|---|---|
| validation real vs impostor | 40 | 40 | 0 | 0 | 100.0% |
| real vs b0 | 40 | 32 | 1 | 7 | 80.0% |
| real vs b1 | 40 | 40 | 0 | 0 | 100.0% |
| b0 vs b1 | 40 | 40 | 0 | 0 | 100.0% |

Validation passes.
