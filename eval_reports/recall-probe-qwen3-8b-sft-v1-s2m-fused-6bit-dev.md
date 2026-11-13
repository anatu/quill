# Recall probe: qwen3-8b-sft-v1-s2m-fused-6bit (qwen3-8b-sft-v1-s2m-fused-6bit) on dev (2026-11-12T11:44:43)

Longest verbatim span, in words, that the prompt did not supply. The gate is 8. Recall is a span from the corpus outside the item's own post; the untuned model's figures are the baseline the adapter must not raise (H8). Rebuilt is a span from the item's own held-out post: reconstruction from the prompt, reported and not gated (decision 2026-11-11).

| Prompt | n | Recall max | Recall median | Recall at or over the gate | Rebuilt max | Rebuilt at or over the gate |
|---|---|---|---|---|---|---|
| summary | 62 | 10 | 0 | 2 | 9 | 3 |
| paraphrase | 62 | 14 | 0 | 4 | 23 | 41 |
| opening | 62 | 8 | 0 | 2 | 0 | 0 |
