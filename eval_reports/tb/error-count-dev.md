# Error count on dev (2026-11-15T17:16:06)

Checker: claude-opus-5-5, blind to the system, given the notes and the book's passage as reference. `human` is the book's own passage run through the same check: its counts are the checker's false-alarm rate.

| System | Passages | Errors | Major | Errors / passage | Major / passage | Clean passages | No major error | Major error of substance |
|---|---|---|---|---|---|---|---|---|
| tb-x1 | 34 | 256 | 72 | 7.53 | 2.12 | 0 | 5 | 24 |
| bt-ex | 34 | 30 | 2 | 0.88 | 0.06 | 14 | 32 | 2 |
| human | 34 | 0 | 0 | 0.0 | 0.0 | 34 | 34 | 0 |

Errors by type, all (major):

| System | logic | misstatement | unsupported | vague | repetition | structure | entity |
|---|---|---|---|---|---|---|---|
| tb-x1 | 37 (14) | 71 (33) | 43 (4) | 44 (7) | 23 (0) | 33 (13) | 5 (1) |
| bt-ex | 4 (1) | 5 (1) | 15 (0) | 1 (0) | 3 (0) | 0 (0) | 2 (0) |
| human | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |

Substance = logic, misstatement, unsupported, entity.
