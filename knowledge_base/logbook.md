# Experiment logbook

One entry per experiment or finding, newest first. Each entry says what was run, what was seen, and what was decided. Aggregate numbers only: no corpus text. Reports with the full figures are in `eval_reports/`; the plan is [plan.md](plan.md).

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
