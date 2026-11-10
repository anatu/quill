# Verifier check on dev (2026-11-10T05:11:16)

Can each style scorer tell the author's held-out text from plain drafts of the same content? No scorer has trained on a draft. Accept rates use the threshold that passes 5% of the dev impostor passages. Paired: share of chunks where the original outscores its own draft.

| Scorer | AUC vs impostors | AUC vs drafts | Paired | Accept: author | drafts | b0 | b1 |
|---|---|---|---|---|---|---|---|
| M1 char n-grams, raw | 0.994 | 0.944 | 98.4% | 93.5% | 34.6% | 55.1% | 39.5% |
| M1 masked, keep 200 | 0.993 | 0.926 | 95.2% | 97.4% | 46.9% | 93.6% | 54.0% |
| M1 masked, keep 500 | 0.995 | 0.947 | 98.4% | 98.7% | 44.4% | 85.9% | 54.0% |
| M1 masked, keep 1000 | 0.996 | 0.957 | 100.0% | 98.7% | 55.6% | 86.5% | 60.0% |
| M1 masked, keep 3000 | 0.996 | 0.957 | 100.0% | 97.4% | 42.0% | 66.7% | 42.7% |
| M2 StyleDistance, classifier | 0.994 | 0.992 | 98.4% | 98.7% | 9.9% | 62.2% | 20.5% |
| M2 StyleDistance, centroid delta | 0.862 | 1.000 | 100.0% | 26.0% | 0.0% | 0.0% | 0.0% |
| M3 LUAR, classifier | 0.996 | 0.979 | 100.0% | 98.7% | 28.4% | 86.5% | 40.0% |
| M3 LUAR, centroid delta | 0.826 | 1.000 | 100.0% | 32.5% | 0.0% | 0.0% | 0.0% |
