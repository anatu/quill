# Recall probe: sft-v1-s2m-x3 (qwen3-8b-4bit+sft-v1-s2m:89020586) on dev (2026-11-13T10:38:41)

Longest verbatim span, in words, that the prompt did not supply. The gate is 8. Recall is a span from the corpus outside the item's own post; the untuned model's figures are the baseline the adapter must not raise (H8). Rebuilt is a span from the item's own held-out post: reconstruction from the prompt, reported and not gated (decision 2026-11-11).

| Prompt | n | Recall max | Recall median | Recall at or over the gate | Rebuilt max | Rebuilt at or over the gate |
|---|---|---|---|---|---|---|
| summary | 186 | 9 | 0 | 3 | 9 | 6 |
| paraphrase | 186 | 9 | 0 | 8 | 18 | 124 |
| opening | 186 | 9 | 0 | 4 | 12 | 8 |
