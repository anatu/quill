# Recall probe: sft-v1-s2m (qwen3-8b-4bit+sft-v1-s2m:89020586) on dev (2026-11-12T07:25:42)

Longest verbatim span, in words, that the prompt did not supply. The gate is 8. Recall is a span from the corpus outside the item's own post; the untuned model's figures are the baseline the adapter must not raise (H8). Rebuilt is a span from the item's own held-out post: reconstruction from the prompt, reported and not gated (decision 2026-11-11).

| Prompt | n | Recall max | Recall median | Recall at or over the gate | Rebuilt max | Rebuilt at or over the gate |
|---|---|---|---|---|---|---|
| summary | 62 | 0 | 0 | 0 | 9 | 3 |
| paraphrase | 62 | 9 | 0 | 2 | 17 | 43 |
| opening | 62 | 8 | 0 | 1 | 12 | 3 |
