# Experiment logbook

One entry per experiment or finding, newest first. Each entry says what was run, what was seen, and what was decided. Aggregate numbers only: no corpus text. Reports with the full figures are in `eval_reports/`; the plan is [plan.md](plan.md).

---

## 2026-11-12: The mixed adapter with the paraphrase tag passes the gates at N=4 and beats stage 1

**Phase 5.** Report: `eval_reports/sft-v1-s2m-ptag-n4-dev.md`. `sft-v1-s2m` (from s1p, one pass over forms A and B joined), `paraphrase` tag, N=4, draft retry, gates as written (strict entity gate).

| Dev, N=4 | s1p, paraphrase | s2m, paraphrase | s2, draft |
|---|---|---|---|
| Composite (95% CI) | 0.681 [0.61, 0.74] | 0.763 [0.70, 0.82] | 0.731 [0.65, 0.80] |
| M1 accept (restyle / write) | 72.4% (67.5 / 77.6) | 85.1% (82.1 / 88.2) | 98.1% (96.2 / 100) |
| M15 author / LLM | 62.8% / 23.7% | 83.1% / 9.1% | 91.6% / 1.9% |
| M4 meaning | 0.889 | 0.896 | 0.873 |
| Facts entailed (restyle / write) | 96.1% / 85.9% | 96.7% / 86.8% | 92.4% / 84.7% |
| M5 entity pass | 92.7% | 89.5% | 79.8% |
| Fallback (limit 15%) | 10.5% | 12.9% | 22.6% |
| M9 final outputs flagged | 0 | 0 | 1 |
| Candidates failing: entities / memorization (of 496) | 67 / 12 | 103 / 18 | 203 / 32 |
| Words per paragraph (author 34) | 39 | 42 | 30 |
| Sentence-length SD (author 9.3) | 7.1 | 7.4 | 7.9 |

- **Paired, s2m minus s1p: +0.082 [+0.034, +0.133].** The CI excludes 0. Minus Qwen3-8B B1: +0.506 [+0.420, +0.599].
- Fallback 12.9% (restyle 3 of 62, write 13 of 62); no final output carries an 8-word corpus span. Meaning is level with s1p.
- **Recall probe with s2m loaded** (`eval_reports/recall-probe-sft-v1-s2m-dev.md`): 3 of 186 prompts at or over the gate, max 9 words (untuned base: 4, max 9). H8's probe half passes. Rebuilt spans (reported, not gated): 49 prompts, 43 on the paraphrase arm, max 17 (s1p: 32, max 15).
- By the follow-up plan's rule this replaces s1p as the best system. It has not been fused or speed-tested; unfused it decodes at 26.4 tok/s.
- Caveat: this is the eighth adapter variant compared on dev. The gain is plausible (style up on both ops, gates held) but the selection is on dev; test confirms it once, in Phase 8.

---

## 2026-11-12: Mixed-form stage 2 makes the tag a fidelity dial; a style-fidelity frontier, no free win

**Phase 5.** Reports: `eval_reports/sft-v1-{s2-mix30-n1,s2m-n1,s2m-ptag-n1}-dev.md`. All N=1 with the draft retry, on dev.

- `sft-v1-s2-mix30`: adapter weights 0.7 × s1p + 0.3 × s2 (no training). Relative weight change s1p → s2 is small, so linear blending is reasonable.
- `sft-v1-s2m`: from s1p, one pass over s1p + s2 joined (1,316 pairs, 82 updates), LR 5e-5. Val on the joined set 0.922 → 0.859 (low 0.762 at step 1280; noisy). Peak 13.46 GB, 182 minutes.

| Dev, N=1 | Tag | Composite | M1 accept | M15 author / LLM | MIS restyle | M5 entity pass | Fallback | M9 flagged (max) |
|---|---|---|---|---|---|---|---|---|
| s1p | paraphrase | 0.565 [0.50, 0.63] | 67.3% | n/r | 0.915 | 86.3% | 17.7% | 2 (8) |
| s2m | paraphrase | 0.625 [0.54, 0.70] | 83.1% | 76.6% / 13.0% | 0.921 | 78.2% | 26.6% | 4 (13) |
| s2-mix30 | draft | 0.631 [0.55, 0.71] | 92.9% | 85.2% / 5.2% | 0.919 | 71.8% | 35.5% | 9 (11) |
| s2m | draft | 0.568 [0.48, 0.65] | 98.0% | 94.2% / 0.7% | 0.879 | 61.3% | 46.8% | 12 (14) |
| s2 | paraphrase | 0.586 [0.50, 0.67] | 99.4% | 94.2% / 0.6% | 0.856 | 63.7% | 43.5% | 8 (14) |
| s2 | draft | 0.501 [0.41, 0.59] | 96.7% | n/r | 0.869 | 54.0% | 53.2% | 8 (14) |

- **These points lie on one frontier.** Every step toward the author's style costs entity pass, and raises verbatim spans. Nothing here beats s1p on the gates; nothing beats it on the composite with a CI clear of 0 (s2m paraphrase +0.059 [-0.025, +0.137]; mix30 +0.066 [-0.017, +0.146]).
- **With both forms in training, the tag works as a dial.** In s2m, `paraphrase` gives 78% entity pass and 83% M1; `draft` gives 61% and 98%. In s2 (form B only) the tag did almost nothing.
- **Memorization rises with style** in every stage 2 variant: 4 to 13 of 124 single candidates flagged, against 2 for s1p. Candidates are filtered by the gate, so this shows up as fallback.
- N=1 exaggerates fallback: s1p went from 17.7% at N=1 to 10.5% at N=4, s2 from 53.2% to 22.6%.

**Much of the entity "loss" is a change of form, not of fact.** First candidates rechecked with the Phase 3 form-tolerant check (`curate.closure`, both ways: number as word, percent sign, acronym, capitalized ordinary word), against the strict eval gate:

| Dev, first candidate | Restyle: strict fail | Restyle: tolerant fail | Write: strict fail | Write: tolerant fail |
|---|---|---|---|---|
| B1 (untuned base) | 4 | 4 | 11 | 10 |
| s1p, paraphrase tag | 3 | 0 | 14 | 8 |
| s2m, paraphrase tag | 14 | 1 | 13 | 11 |
| s2-mix30, draft tag | 14 | 7 | 21 | 16 |
| s2m, draft tag | 21 | 11 | 28 | 17 |
| s2, draft tag | 31 | 21 | 26 | 20 |

(of 62 inputs each)

- For **s2m with the paraphrase tag**, 13 of its 14 strict restyle failures are form changes. Under the tolerant check it fails 12 of 124 (9.7%), close to s1p's 8 (6.5%). The write-op failures that remain are mostly the drafter's (as before).
- For **s2 and s2m with the draft tag** the loss is real: 21 and 11 restyle outputs fail even the tolerant check.
- The author re-forms figures himself, and the training targets show it. A gate that rejects every re-formed figure rejects part of the voice. Whether H7 should be form-tolerant is the user's call (see followup.md). The gate is unchanged.

**Running:** s2m with the `paraphrase` tag at N=4. It passes if fallback is at most 15%, no final output is flagged by M9, and the composite CI against `sft-v1-s1p-n4r` (0.681) is above 0.

---

## 2026-11-11: Strict-pair filtering does not fix stage 2; ten updates of form B are enough to flip it

**Phase 5.** Reports: `eval_reports/sft-v1-{s1p-n1r,s2-n1,s2s-n1,s2-i160-n1}-dev.md`. All N=1 with the draft retry; s1p uses the `paraphrase` tag, the others `draft`.

`sft-v1-s2s`: from `sft-v1-s1p`, 338 strict-pass form B pairs, two passes (676 micro-batches), LR 5e-5. Val 1.308 → 1.156; last train loss 0.917; peak 12.69 GB.

| Dev, N=1 | s1p | s2 step 160 | s2 final | s2s |
|---|---|---|---|---|
| Composite | 0.565 [0.50, 0.63] | 0.500 [0.42, 0.58] | 0.501 [0.41, 0.59] | 0.543 [0.46, 0.63] |
| M1 accept | 67.3% | 90.2% | 96.7% | 98.1% |
| M15 author / LLM | n/r | 85.0% / 3.9% | n/r | 91.0% / 0.6% |
| MIS restyle (mean) | 0.915 | 0.829 | 0.869 | 0.857 |
| Facts entailed (restyle / write) | 96.7% / 86.6% | 88.0% / 84.0% | 89.7% / 86.2% | 90.6% / 82.4% |
| M5 entity pass | 86.3% | 59.7% | 54.0% | 60.5% |
| Fallback | 17.7% | 46.0% | 53.2% | 47.6% |
| M9 flagged (max span) | 2 (8) | 4 (9) | 8 (14) | 13 (14) |

(n/r: not read off the report for this table.)

- **The strict filter is not the fix.** Entity-failing outputs: s2 57, s2s 49, s1p 17. The pair-level finding in the entry below is true but explains little of the loss.
- **s2s copies more:** 13 of 124 outputs flagged. Two passes over 338 pairs is the likely cause. Rejected.
- **Step 160 already has the whole effect.** That is 10 optimizer updates at a warming-up LR. Style jumps to 90% and entity pass falls to 60%. So this is not slow drift or over-training; a lighter stage 2 will not help.
- **Working hypothesis:** the trade-off sits in the task, not the dose. A draft differs from the author's passage in order and structure, so `draft → author` licenses free rewriting, and items fall out. A paraphrase tracks the passage sentence by sentence, so `paraphrase → author` stays close and keeps items, at the cost of weaker style change. The eval's restyle inputs are Claude drafts in both cases; only the tag and the training differ.
- **The tag is not a fidelity dial.** s2 with the `paraphrase` tag at N=1 (`sft-v1-s2-ptag-n1`): M1 99.4%, M15 author 94.2% / LLM 0.6%, entity pass 63.7%, fallback 43.5%, MIS restyle 0.856, M9 flagged 8 (max 14), composite 0.586 [0.50, 0.67]; minus s1p +0.021 [-0.076, +0.111]. Stage 2 moved the whole adapter; the tag changes little.
- **Queue (running overnight, all local, N=1):** (1) `sft-v1-s2-mix30`: adapter weights 70% s1p + 30% s2, `draft` tag, to see whether a point between them keeps entities with more style; (2) `sft-v1-s2m`: from s1p, one pass over s1p + s2 joined (1,316 pairs), LR 5e-5; scored with the `draft` tag and the `paraphrase` tag.

---

## 2026-11-11: Stage 2 nearly closes the style gap but drops entities; fallback gate fails

**Phase 5 (stage 2).** Reports: `eval_reports/sft-v1-s2-n4-dev.md`. Follow-up queue: [followup.md](followup.md).

**Local half of form B** (`quill pairs --local`, `pairs/local.py`). The untuned base drafted 356 marker-free chunks from their fact lists with the Claude draft prompt and the lost-item retry (86 redrafted). 331 pass curation (fails: meaning 16, closure 11). `sft-v1-s2`: 641 train pairs, 296 local (46%); 59 valid, 35 local. Chunks with markers keep Claude drafts. No Claude calls.

**Training** (`sft-v1-s2`): resumed from `sft-v1-s1p`, LR 5e-5 cosine, one pass (641 micro-batches). Val 1.259 → 1.135, flat and noisy after step 160 (1.139, 1.142, 1.066, 1.096). Peak 12.83 GB, 86 minutes.

| Dev, N=4, draft retry | sft-v1-s1p (`paraphrase` tag) | sft-v1-s2 (`draft` tag) |
|---|---|---|
| Composite (95% CI) | 0.681 [0.61, 0.74] | 0.731 [0.65, 0.80] |
| M1 accept (restyle / write) | 72.4% (67.5 / 77.6) | 98.1% (96.2 / 100) |
| M15 author / LLM | 62.8% / 23.7% | 91.6% / 1.9% |
| M4 meaning | 0.889 | 0.873 |
| MIS restyle (mean) | 0.919 | 0.898 |
| Facts entailed (restyle / write) | 96.1% / 85.9% | 92.4% / 84.7% |
| M5 entity pass | 92.7% | 79.8% |
| Fallback (limit 15%) | 10.5% | 22.6% |
| Candidates failing: entities / memorization | 67 / 12 of 496 | 203 / 32 of 496 |
| M9 final outputs flagged (max span) | 0 | 1 (11) |
| Words per paragraph (author 34) | 39 | 30 |
| Sentence-length SD (author 9.3) | 7.1 | 7.9 |
| M7 vocab × | 3.27 | 1.57 |

- Paired, s2 minus s1p: +0.050 [-0.033, +0.134]. Not significant: the style gain is cancelled by outputs that fail the entity gate.
- **Style is at the author's ceiling.** The verifier accepts 94.8% of the author's own held-out passages; it accepts 98.1% of s2's. M15 calls 1.9% LLM.
- **The adapter itself now loses entities.** Restyle: 106 of 248 candidates fail the entity check (s1p: 16); 14 of 62 inputs fall back (s1p: 0). Missing numbers dominate (121 in restyle, 91 in write), then missing names. Form B curation checks that the target adds nothing; it is form-tolerant, and it does not require the target to keep every item of the draft. The adapter may have learned to re-form or drop figures. Not confirmed.
- **Gates:** fallback fails (22.6%); H8 output half fails (1 output, 11 words). So s2 as trained does not replace s1p.
- **Rebuilt spans are not training leakage.** Share of outputs with an 8+ word span from their own held-out post, not supplied by the input: B0 102 of 124, B1 10, s1p 61, s2 85. Of s2's 85, 79 occur only in the item's own post, 6 also in a train chunk. Prompted Opus rebuilds more than either adapter, so the fact lists pin the wording. Median share of an output's 8-grams involved: B0 2.0%, s2 1.4%, s1p 0.7%.

**Root cause found: the training pairs teach it.** The eval's strict entity gate, run on the kept training pairs (input against target, both ways):

| Train pairs | n | Fail the strict gate | Items missing from the target | Items the target adds |
|---|---|---|---|---|
| A: paraphrase → target | 675 | 207 (31%) | 54 names, 51 numbers, 16 dates | 182 names, 31 numbers |
| B: Claude draft → target | 345 | 171 (50%) | 52 names, 108 numbers, 4 dates | 112 names, 39 numbers |
| B: local draft → target | 296 | 132 (45%) | 27 names, 138 numbers, 3 dates | 51 names, 16 numbers |

- Phase 3 curation used a form-tolerant, one-way closure check (the target adds nothing). That was right for "no invented facts", but it lets through pairs where the input has a figure the target lacks or writes another way. Half of form B shows the adapter exactly the behaviour the eval gate rejects.
- Form A is cleaner (31%), which fits s1p's 16 failing restyle candidates against s2's 106.

**Fix under test:** `sft-v1-s2s` and `sft-v1-s1ps` (`pairs/to_mlx.py`, `STRICT`) keep only pairs that pass the strict gate: 338 of 641 form B pairs (164 local), 468 of 675 form A. `sft-v1-s2s` trains from `sft-v1-s1p` at LR 5e-5 for two passes, which matches s2's number of optimizer steps on half the data.

**Queue (running, N=1 with draft retry):** `sft-v1-s1p-n1r` and `sft-v1-s2-n1` from cache as baselines; train and score `sft-v1-s2s`; then the step-160 checkpoint of s2.

---

## 2026-11-11: Fusing into 4-bit erases the adapter; a 6-bit fused copy holds style at 30 tok/s

**Phase 4.** Reports: `eval_reports/sft-v1-s1p-fused-n4-dev.md`, `sft-v1-s1p-fused8-dev.md`, `sft-v1-s1p-fused6-dev.md`. All runs use the draft retry. `quill run --fused PATH` generates from a merged model.

| `sft-v1-s1p` on dev | Candidates | Composite | M1 accept | M15 author / LLM | Tok/s (run overall) | Peak GB |
|---|---|---|---|---|---|---|
| Adapter loaded on the 4-bit base | 4 | 0.681 | 72.4% | 62.8% / 23.7% | 26.7 | 6.1 |
| Fused, re-quantized to 4-bit (`mlx_lm fuse`) | 4 | 0.098 | 7.7% | 3.9% / 84.6% | 42.4 | 5.4 |
| Fused with `--dequantize`, then 8-bit | 1 | 0.587 | 68.2% | 59.7% / 24.0% | 27.2 | 9.5 |
| Fused with `--dequantize`, then 6-bit | 1 | 0.655 | 78.6% | 66.9% / 20.1% | 30.2 | 7.4 |

- **The 4-bit fused copy scores like the untuned base** (paired −0.583 [−0.682, −0.508] against the loaded adapter). Likely cause: re-quantizing to 4 bits rounds away the LoRA delta. Not checked at the weight level; the 8-bit and 6-bit results fit it.
- **This voids the earlier fused-speed entry** (50.5 tok/s): that copy no longer carried the adapter.
- 8-bit keeps the style but is no faster than the loaded adapter and takes 9.5 GB.
- **6-bit keeps the style and reaches 30.2 tok/s** over the whole run, 7.4 GB peak, 6.2 GB on disk. 6-bit minus 8-bit: +0.068 [+0.009, +0.128], so no sign of loss. The speed gate (30) passes by a hair; it is not a comfortable margin.
- The 6-bit copy has not been run at N=4, and the recall probe has not been run on it.

---

## 2026-11-11: Entity failures come from the drafter; a draft retry fixes most

**Phase 4.** Report: `eval_reports/sft-v1-s1p-n4r-dev.md`.

Diagnosis on the N=4 run of `sft-v1-s1p`:

| | Restyle | Write |
|---|---|---|
| Candidates failing the entity check | 19 of 248 | 164 of 248 |
| Inputs with all 4 candidates failing | 0 of 62 | 38 of 62 |

- In `write`, the untuned base drafts from the brief and facts, and the adapter restyles the draft. 41 of 62 drafts already drop or add an item against the brief. Only 9 of the 164 failing write candidates fail against their own draft. The adapter keeps what it is given.
- Lost items: 225 numbers, 165 names.

Fix: `baselines.plain_draft`. A draft with entity errors is redrafted by the base with the lost and added items named (`configs/prompts/draft_fix.txt`); the draft with the fewest errors is kept. The adapter's prompt is untouched. Failing drafts: 41 → 18 with 2 retries, → 10 with 4.

| Dev, N=4 | no draft retry | draft retry (4) |
|---|---|---|
| Composite (95% CI) | 0.508 [0.44, 0.57] | 0.681 [0.61, 0.74] |
| M1 accept (restyle / write) | 76.1% (67.5 / 85.3) | 72.4% (67.5 / 77.6) |
| M15 author / LLM | 68.4% / 16.8% | 62.8% / 23.7% |
| M4 meaning (write facts entailed) | 0.848 (77.7%) | 0.889 (85.9%) |
| M5 entity pass | 70.2% | 92.7% |
| Fallback (H9 limit 15%) | 29.8% | 10.5% |
| M9 flagged | 1 | 0 |

- Paired: +0.173 [+0.119, +0.229] over the run without retry; +0.425 [+0.331, +0.523] over Qwen3-8B B1.
- All 13 remaining fallbacks are in `write`; restyle has none.
- The composite applies the entity gate first, so most of this gain is outputs that now pass the gate, not better style. Write-op M1 fell from 85.3% to 77.6%: fuller drafts are harder to restyle. B0 and B1 got no draft retry, so the comparison with them now favours the adapter pipeline.
- Rebuilt spans against the held-out target rose to 61 of 124 outputs (reported, not gated).

---

## 2026-11-11: N=4 rerank, the adapter's recall probe, and fused speed

**Phase 4.** Reports: `eval_reports/sft-v1-s1p-n4-dev.md`, `recall-probe-sft-v1-s1p-dev.md`.

**N=4 with rerank (`sft-v1-s1p`).** Composite 0.508 [0.44, 0.57]. Paired: +0.065 [+0.031, +0.104] over N=1; +0.252 [+0.159, +0.346] over Qwen3-8B B1; +0.256 [+0.167, +0.349] over B0. M1 76.1% (restyle 67.5, write 85.3). M15 author 68.4%, LLM 16.8%. M4 0.848; write-op facts entailed 77.7% (B1 81.7%). Words per paragraph 43 (author 34).

- **Rerank does not fix entities.** 168 of 496 candidates fail the entity check; fallback falls only from 34.7% to 29.8%; M5 pass 70.2%. The same inputs fail across candidates.
- **Memorization in candidates:** 17 of 496 carry a span of 8+ words (untuned base: 3 of 496). Rerank drops them; 1 of 124 final outputs is flagged, max 8 words.

**Recall probe with the adapter loaded.** 35 of 186 prompts at or over the 8-word gate, max span 15 (untuned base: 6, max 9). By prompt: summary 1, opening 1, paraphrase 33 (median span 8; base 0).

- The paraphrase arm asks for the original of a held-out dev passage from its paraphrase. That is the trained task. Of its 33 flagged spans, 21 occur in the item's own dev chunk, which was never trained on; 4 occur in a train chunk; 11 matched nothing under my simple normalization.
- So the rise is mostly inversion of the input, not recall of training text. It is still a rise, and H8 as written ("the adapter must not raise") fails on this arm. Summary and opening arms do not rise.
- The same effect shows in M9 `target_rebuilt`: 53 of 124 outputs share an 8+ word span with the held-out target (B1: 10).
- **Decision (user, 2026-11-11): do not count it.** The probe now splits each span as M9 does: recall (corpus outside the item's own post, gated) and rebuilt (the item's own post, reported). Rescored from the cache: adapter recall 3 prompts at or over the gate, max 9 words; untuned base 4, max 9. H8's probe half passes. Rebuilt: adapter 32 prompts (31 on the paraphrase arm, max 15); base 2. The probe files no longer store span text.

**Decode speed (superseded: the fused copy here had lost the adapter; see the entry above).** Five dev restyle inputs, temp 0.7. Adapter loaded unfused: 28.4 tok/s. Fused with `mlx_lm fuse` into a local 4-bit copy: 50.5 tok/s, peak 5.32 GB. Untuned base: 50.7 tok/s. The 30 tok/s gate passes fused. Fusing re-quantizes the adapted weights; the fused copy has not been scored yet.

---

## 2026-11-11: Merging input paragraphs in training fixes most of the paragraphing

**Phase 4.** Report: `eval_reports/sft-v1-s1p-dev.md`.

`sft-v1-s1p` is `sft-v1-s1` with input paragraphs left alone in 40% of rows, merged in groups of 2-4 in 40% and fully merged in 20% (`pairs/to_mlx.merge_paragraphs`, fixed per row). Targets are unchanged. Median input breaks fall from 10 to 5. Same config, one pass: val 1.210 → 0.639, peak 12.84 GB, 93 minutes.

| Dev, N=1 | sft-v1-s1 | sft-v1-s1p |
|---|---|---|
| Composite (95% CI) | 0.425 [0.36, 0.49] | 0.443 [0.37, 0.51] |
| M1 accept (restyle / write) | 60.3% (61.2 / 59.2) | 71.2% (62.5 / 80.3) |
| M15 author / LLM | 59.6% / 23.1% | 60.9% / 24.4% |
| M4 meaning | 0.866 | 0.858 |
| Words per paragraph (author 34) | 90 | 52 |
| One-sentence paragraphs (author 42%) | 1.8% | 26.1% |
| M5 entity pass | 64.5% | 66.9% |
| Fallback | 36.3% | 34.7% |

- Paired bootstrap, s1p minus s1: +0.018 [-0.035, +0.073]. Not significant. s1p minus Qwen3-8B B1: +0.187 [+0.097, +0.285].
- The gain is in the write op, where the input is an untuned-base draft.
- Entities and speed (26 tok/s) do not move.

**Decision:** carry `sft-v1-s1p` forward. N=4 with rerank is running on it.

---

## 2026-11-11: Stage-1 adapter on Qwen3-8B beats same-base B1

**Phase 4.** Reports: `eval_reports/sft-v1-s1-dev.md`, `b1-dev.md` (Qwen3-8B), `b1-qwen35-dev.md`, `recall-probe-base-dev.md` (Qwen3-8B), `recall-probe-qwen35-dev.md`.

Training (`sft-v1-s1`): `configs/train/sft.yaml`, `mlx-community/Qwen3-8B-4bit`, 675 form-A pairs, one pass (675 micro-batches, accumulation 16), LoRA rank 16 on all 36 layers, LR 1e-4 cosine.

- Val loss 1.195 → 0.631 (0.580 at step 640). Last train loss 0.758.
- Peak memory 12.84 GB (gate 17). 62 loss-tokens/s. 94 minutes.

Dev results. The adapter ran at N=1 with the `paraphrase` tag; B1 ran at N=4 with rerank.

| | B1 Qwen3.5 | B1 Qwen3-8B | sft-v1-s1 |
|---|---|---|---|
| Composite (95% CI) | 0.057 [0.00, 0.10] | 0.256 [0.19, 0.32] | 0.425 [0.36, 0.49] |
| M1 accept | 1.6% | 21.4% | 60.3% |
| M15 author / LLM | 1.1% / 85.9% | 16.2% / 77.3% | 59.6% / 23.1% |
| M4 meaning | 0.820 | 0.870 | 0.866 |
| M5 entity pass | 91.1% | 87.9% | 64.5% |
| Fallback | 25.8% | 14.5% | 36.3% |
| M9 flagged (max span) | 1 (8) | 0 (0) | 3 (9) |

- **Paired bootstrap, adapter minus Qwen3-8B B1:** +0.169, 95% CI [+0.083, +0.261], 62 chunks. The CI excludes 0: gate passes.
- **Untuned Qwen3-8B is a much stronger B1 than Qwen3.5-9B** (0.26 against 0.06). Its gain is in the write op (M1 41.1%); restyle M1 is 3.7%. The adapter scores 61.2% restyle, 59.2% write.
- **Decode speed fails the gate:** 26 tok/s with the unfused adapter, 24 tok/s for the untuned base in B1, 44-48 tok/s on shorter prompts. Gate is 30.
- **Entities are the adapter's weak point.** 44 of 124 outputs fail (36 missing, 13 added). N=1 gives the reranker nothing to choose from.
- **Paragraphing follows the input.** Outputs run 90 words per paragraph against the author's 34 (z 9.4); one-sentence paragraphs 1.8% against 42%. Eval inputs carry a median of 1 paragraph break; training inputs carry 10, matching their targets. The adapter never had to re-paragraph.
- **Recall probe, untuned Qwen3-8B:** max span 9 words; 6 of 186 prompts at or over the 8-word gate (Qwen3.5: 12 words, 15 prompts). This is the baseline for H8. The adapter has not been probed yet.

**Open:** retrain with paragraph breaks collapsed in part of the inputs; N=4 with rerank; fuse the adapter and re-measure speed; recall probe on the adapter.

---

## 2026-11-10: Qwen3.5-9B cannot be fine-tuned here; base switches to Qwen3-8B

**Phase 4, day-1 probe.** mlx 0.32.4, mlx-lm 0.32.2 (the latest release), M4 Pro 24 GB, `iogpu.wired_limit_mb` at its default.

Setup: `configs/train/sft.yaml`. LoRA rank 16 on all 32 blocks (43.3M trainable parameters, 0.483%), batch 1, gradient checkpointing on, `--mask-prompt`, max sequence 2,048. Model: `mlx-community/Qwen3.5-9B-4bit`.

| Example length (tokens) | Gradient checkpointing | Result |
|---|---|---|
| about 200 | on | trains, 21 tok/s |
| about 600 | on | trains, 20 tok/s |
| about 600 | off | out of memory |
| about 1,000 | on | out of memory |
| about 1,400 | on | out of memory |
| about 1,800 | on | out of memory |
| 1,965 (longest pair) | on | out of memory |

- The form-A pairs have a median of 978 tokens, a 90th percentile of 1,672 and a maximum of 1,965. 140 of 675 exceed 1,536.
- The plan assumed 100-200 tok/s in training. The measured 20 tok/s would make one pass about 9 hours, if it fitted.
- **Cause.** 24 of the 32 layers are Gated DeltaNet (linear attention); every fourth is full attention. In `mlx_lm/models/qwen3_5.py` the layer calls `gated_delta_update(..., use_kernel=not self.training)`. The Metal kernel has no gradient, so training runs `gated_delta_ops`, a Python loop over every token that keeps a state matrix per step for the backward pass.
- This is the risk the plan listed for this candidate ("Gated DeltaNet LoRA support unconfirmed"). It fails the Phase 4 gate of peak memory at most 17 GB at sequence 2,048.
- Inference is unaffected: B1 and the recall probe ran on this model at 4-bit without trouble.

**Decision (user, 2026-11-10):** switch the base to Qwen3-8B, 4-bit (`mlx-community/Qwen3-8B-4bit`, Apache 2.0, dense attention, 36 layers). It is the plan's named fallback. B1 and the recall probe are rerun on it. B0, the verifier, the eval inputs and the training pairs do not depend on the base and stand.

Not tried: chunked checkpointing inside the DeltaNet loop (estimate: a day of work and 10-19 hours per pass); training only the top blocks.

Also settled on the same day, from the mlx-lm source:
- `--iters` counts micro-batches of `batch_size`. The optimizer and the LR schedule step once per `grad_accumulation_steps` iterations. One pass over 675 rows at accumulation 16 is 675 iterations and 42 optimizer updates.
- Batches are sorted by length, grouped, then shuffled; sequences over `max_seq_length` are cut from the end, which would cut the target.
- Chat template: the training render of an example ends `<|im_start|>assistant\n<think>\n\n</think>\n\n<target><|im_end|>`. Inference with `enable_thinking=False` produces the same prefix. With `--mask-prompt` the loss also covers the closing think tag, a constant.
- Base val loss on form A before any training: 0.83 on the longest examples. The paraphrase shares most of its words with the target (median word similarity 0.71), so the task starts easy.

---

## 2026-11-10: Training pairs v1, curation

**Phase 3.** Report: `eval_reports/pairs-v1.md`. 750 chunks (688 train, 62 dev); Sonnet 5.5 paraphrases, Opus 5.5 drafts.

| Train, 688 chunks | First pass | After a targeted retry |
|---|---|---|
| Form A (paraphrase) kept | 622 (90.4%) | 675 (98.1%) |
| Form B (draft) kept | 570 (82.8%) | 641 (93.2%) |
| Both forms | 549 (79.8%) | 637 (92.6%) |

- **Strict fact closure was mostly false alarms.** With the Phase 2 entity gate as the check, 34% of pairs failed. Nearly all were changes of form: a number as a word, "percent" for "%", an inline list number, an idiom ("a 180", "9/11"), an acronym for its expansion, a capitalized ordinary word. A form-tolerant check cut failures to 12% (A) and 15% (B).
- **The real losses are figurative numbers.** Told to remove figures of speech, Claude drops numbers used for emphasis ("100% confident"). A blind resample fixed 18 of about 80 paraphrases. Naming the lost items in the retry prompt fixed 76 paraphrases and 79 drafts.
- **Inputs are plain.** On dev the M1 verifier accepts 7.7% of paraphrase passages and 0% of draft passages, against 94.8% of the author's. On train the paraphrase figure is 28%, but the verifier was fitted on those targets, so the dev figure is the one to read.
- **MIS medians:** 0.947 (A), 0.925 (B). The floor of 0.7 drops 3 A pairs and 19 B pairs on train.
- Four train chunks exceed 2,048 tokens as rendered and are dropped.
- Cost: $21.89.

**Scorer bug found here.** `meaning.candidates` fell back to the whole output when no sentence started near an input window, which happens with very long sentences. A faithful paraphrase scored 0.36. It now takes the two nearest sentence starts. No dev eval item had hit the fallback (0 of 408 windows), so the Phase 2 numbers did not move.

**Process note.** The first scoring run died silently after the paraphrase pass: two chunks carry the corpus bucket `under-150`, which the template rejects, and stderr was discarded. The Mac also slept for two hours mid-run. Long runs now log stderr and run under `caffeinate`.

---

## 2026-11-10: Phase 2 findings worth keeping

Full figures: `eval_reports/baseline-v2.md`, `verifier-check-dev.md`, `m10-dev.md`, `m11-judge-dev.md`.

- **The first verifier leaked on LLM-ness, not topic.** It accepted about half of plain Claude drafts of the author's content. Masking content words made that worse (44-56% accepted). Adding 933 train-draft passages to the negatives fixed it: drafts 0%, B0 23.7%, held-out author 94.8%, other human authors 5.0%.
- **Baselines on dev (decision composite):** B0 (Opus with a style guide and exemplars) 0.25 [0.17, 0.33]; B1 (untuned Qwen3.5-9B) 0.06 [0.00, 0.10]; B2 (the plain draft) 0.
- **Fast-DetectGPT (M10) fails sanity:** AUC 0.50 on B0, 0.49 on B1, 0.40 on plain Opus drafts; 0.91 on older Claude controls. Dropped.
- **Claude judge (M11):** real over impostor 40 of 40; real over B0 32-1 with 7 inconsistent; B0 over B1 40-0.
- **Recall probe, untuned Qwen3.5-9B:** longest verbatim span 12 words; 15 of 186 prompts at or over the 8-word gate.
- **spaCy NER over-tags sentence openers** ("Luck", "Vanity") as names; it is used only to rescue sentence-initial names, minus words seen in lower case in the corpus.
- **M15** passes sanity only with Farnam Street and Naval merged into "other humans" (6 and 8 dev passages are too few for classes of their own).
