# Recall probe: qwen3-8b-sft-v1-s2m-fused-6bit-x3 (qwen3-8b-sft-v1-s2m-fused-6bit) on dev (2026-11-13T11:25:34)

Longest verbatim span, in words, that the prompt did not supply. The gate is 8. Recall is a span from the corpus outside the item's own post; the untuned model's figures are the baseline the adapter must not raise (H8). Rebuilt is a span from the item's own held-out post: reconstruction from the prompt, reported and not gated (decision 2026-11-11).

| Prompt | n | Recall max | Recall median | Recall at or over the gate | Rebuilt max | Rebuilt at or over the gate |
|---|---|---|---|---|---|---|
| summary | 186 | 10 | 0 | 5 | 9 | 7 |
| paraphrase | 186 | 14 | 0 | 9 | 23 | 131 |
| opening | 186 | 8 | 0 | 3 | 12 | 3 |
