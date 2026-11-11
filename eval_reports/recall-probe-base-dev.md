# Recall probe: base (qwen3-8b-4bit) on dev (2026-11-11T09:52:28)

Longest verbatim span, in words, that the prompt did not supply. The gate is 8. Recall is a span from the corpus outside the item's own post; the untuned model's figures are the baseline the adapter must not raise (H8). Rebuilt is a span from the item's own held-out post: reconstruction from the prompt, reported and not gated (decision 2026-11-11).

| Prompt | n | Recall max | Recall median | Recall at or over the gate | Rebuilt max | Rebuilt at or over the gate |
|---|---|---|---|---|---|---|
| summary | 62 | 9 | 0 | 1 | 8 | 1 |
| paraphrase | 62 | 0 | 0 | 0 | 0 | 0 |
| opening | 62 | 9 | 0 | 3 | 8 | 1 |
