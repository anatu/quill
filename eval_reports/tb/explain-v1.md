# Explain pairs v1: notes → passage (2026-11-15T10:04:30)

The input is Claude's reduction of a passage to CORE points and MATERIAL details (shuffled); the target is the passage. A pair is kept when the notes have at least 2 core points and some material, the target adds no name, number, date or link, the notes are 0.1-0.75x the target's length and the example fits 2048 tokens.

Where the notes missed a name or number of the passage, it was added to MATERIAL from the passage.

| Split | Chunks | Kept | Notes/target words | Core bullets | Material bullets | Max tokens | Notes repaired | Fails |
|---|---|---|---|---|---|---|---|---|
| train | 475 | 428 (90.1%) | 0.536 | 5.0 | 7.0 | 1491 | 101 | closure 9, ratio 38 |
| dev | 39 | 34 (87.2%) | 0.514 | 5.0 | 7.0 | 1250 | 9 | closure 1, ratio 4 |
