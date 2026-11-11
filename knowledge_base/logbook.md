# Experiment logbook

One entry per experiment or finding, newest first. Each entry says what was run, what was seen, and what was decided. Aggregate numbers only: no corpus text. Reports with the full figures are in `eval_reports/`; the plan is [plan.md](plan.md).

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
