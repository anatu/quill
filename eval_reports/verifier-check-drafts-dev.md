# Verifier check with draft negatives, dev (2026-11-10T05:13:22)

Drafts of some dev posts join the negatives; the other posts are scored (4 folds by post). Accept rates use the threshold that passes 5% of the dev impostor passages. An estimate: the real fix trains on drafts of train chunks.

| Scorer | Accept: author | Accept: draft | Accept: b0 | Accept: b1 |
|---|---|---|---|---|
| M1 char n-grams, raw | 88.3% | 6.2% | 24.4% | 10.8% |
| M1 masked, keep 1000 | 90.9% | 7.4% | 50.0% | 8.6% |
| M2 StyleDistance, classifier | 98.7% | 1.2% | 44.9% | 7.0% |
| M3 LUAR, classifier | 97.4% | 9.9% | 81.4% | 19.5% |
