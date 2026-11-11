# Training pairs v1: curation (2026-11-10T18:39:43)

Form A is a neutral paraphrase; form B is a generic draft from the fact list. The target is the author's chunk, verbatim. A pair is kept when the target adds no name, number, date or link, the markers match, MIS is at least 0.7, word similarity is at most 0.85, the input is 0.5-2.0x the target and the example fits 2048 tokens.

| Split | Chunks | Form | Kept | Median MIS | Input/target words | Max tokens | Fails |
|---|---|---|---|---|---|---|---|
| dev | 62 | A | 62 (100.0%) | 0.947 | 1.02 | 1892 | none |
| dev | 62 | B | 59 (95.2%) | 0.928 | 1.043 | 1872 | closure 1, meaning 2 |
| train | 688 | A | 675 (98.1%) | 0.947 | 1.019 | 2433 | closure 5, copy 2, meaning 3, tokens 4 |
| train | 688 | B | 641 (93.2%) | 0.925 | 1.033 | 2412 | closure 26, meaning 19, tokens 3 |

Train chunks that keep both forms: 637 of 688 (92.6%). The gate is 85%: passes.

inputs_replaced_on_retry: {"A": 76, "B": 79}
