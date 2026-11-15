# Training pairs v1: curation (2026-11-14T13:32:44)

Form A is a neutral paraphrase; form B is a generic draft from the fact list. The target is the author's chunk, verbatim. A pair is kept when the target adds no name, number, date or link, the markers match, MIS is at least 0.7, word similarity is at most 0.85, the input is 0.5-2.0x the target and the example fits 2048 tokens.

| Split | Chunks | Form | Kept | Median MIS | Input/target words | Max tokens | Fails |
|---|---|---|---|---|---|---|---|
| dev | 39 | A | 31 (79.5%) | 0.951 | 0.96 | 1593 | copy 8 |
| dev | 39 | B | 37 (94.9%) | 0.932 | 1.036 | 1605 | closure 2 |
| train | 475 | A | 379 (79.8%) | 0.951 | 0.963 | 1884 | closure 3, copy 93 |
| train | 475 | B | 460 (96.8%) | 0.932 | 1.035 | 1923 | closure 12, meaning 3 |

Train chunks that keep both forms: 365 of 475 (76.8%). The gate is 85%: fails.

inputs_replaced_on_retry: {"A": 29, "B": 22}
