# Follow-up plan: Phase 4-5 auto-research queue

Written 2026-11-11 while the stage 2 dev eval ran unattended. Review with the user before acting on anything under "Needs a decision". Results go in [logbook.md](logbook.md); the plan of record is [plan.md](plan.md).

## Where things stand

- Base: Qwen3-8B 4-bit. Stage 1 adapter `sft-v1-s1p` (form A, merged input paragraphs). Stage 2 adapter `sft-v1-s2` (form B, 46% local drafts, resumed from s1p at LR 5e-5).
- Best scored system: `sft-v1-s1p` at N=4 with the draft retry. Dev composite 0.681 [0.61, 0.74], fallback 10.5%, recall probe no worse than the base.
- Speed: 27 tok/s with the adapter loaded; 30.2 tok/s as a 6-bit fused copy (N=1 only so far).
- The test split is untouched. Everything below runs on dev.

## Rules for unattended runs

1. Local only. No Claude calls: they cost money and send corpus text out. Anything that needs one goes under "Needs a decision".
2. One GPU job at a time, under `caffeinate`, with stderr logged to `~/.quill/logs/`.
3. Every run ends in a logbook entry with numbers only, no corpus text.
4. A change is kept only if the paired bootstrap of the composite against the current best has a 95% CI that excludes 0, or if it fixes a failing gate without a significant composite loss.
5. Gates that must hold for any candidate: fallback at most 15%; recall probe no worse than the base; 0 final outputs with an 8-word corpus span; training peak at most 17 GB.
6. No commits or pushes without being asked. No deletions of models or data.
7. Dev is being reused heavily. Each extra comparison raises the chance of a lucky win. Keep the list short and confirm the finalist once on test (Phase 8), nowhere else.

## Update, 2026-11-11 evening

Queue item 1 is done: stage 2 reaches the author's ceiling on style (M1 98%, M15 LLM 1.9%) but fails the fallback gate (22.6%), because the adapter itself now drops or re-forms names and numbers. Cause: 45-50% of form B training pairs fail the eval's strict entity gate (31% of form A). See the logbook.

That reorders the queue. New first items, ahead of the table below:

| # | Experiment | GPU time | Decision rule |
|---|---|---|---|
| 0a | `sft-v1-s2s`: stage 2 on the 338 strict-pass pairs, two passes (running) | 1.5 h train + 1 h eval at N=1 | Against `sft-v1-s2-n1` and `sft-v1-s1p-n1r`: fallback and entity pass near s1p's with M1 near s2's |
| 0b | If 0a works: `sft-v1-s2s` at N=4, then its recall probe | 5 h | All gates in rule 5; composite CI above s1p's 0.681 |
| 0c | If 0a only half works: retrain stage 1 on `s1ps` (468 strict pairs), then s2s on top | 3 h + eval | Same |
| 0d | Step-160 checkpoint of s2 at N=1 | 1 h | Only a fallback if strict data does not fix it |

Caveats on 0a: two passes over 338 pairs raises memorization risk; watch M9 and the recall probe. The strict filter also removes the pairs where the author's text itself re-forms a figure, so the adapter may write figures more literally than the author does. That is the right trade for a restyling tool.

A cleaner long-term fix is to repair the pairs instead of dropping them: regenerate the failing drafts so each carries exactly the target's items (Claude calls for the Claude half; local for the local half). Needs a decision on the Claude spend.

## Update, 2026-11-12 early morning

What the night's runs showed (all in the logbook):

1. **Strict-pair filtering (0a) failed.** Entity pass 60.5% against s2's 54.0%; copying rose. Rejected.
2. **A lighter stage 2 will not help (0d).** Ten updates of form B already flip style to 90% and entity pass to 60%.
3. **In form-B-only s2 the tag does nothing.** In the mixed-form adapter `sft-v1-s2m` the tag is a dial: `paraphrase` is the faithful setting, `draft` the stylish one.
4. **Style, entity pass and verbatim spans move together.** No variant beats s1p on the gates as written.
5. **Most of s2m-paraphrase's entity failures are form changes** (number as word and the like): 13 of 14 in restyle. Under the form-tolerant check it is level with s1p.

**Best candidates now**

| | M1 accept (N=1) | Strict entity pass | Tolerant fail | Status |
|---|---|---|---|---|
| `sft-v1-s1p`, paraphrase tag | 67% | 86% | 6.5% | Passes every gate at N=4 (composite 0.681, fallback 10.5%) |
| `sft-v1-s2m`, paraphrase tag | 83% | 78% | 9.7% | N=4 run in progress |

**Decision needed: should the entity gate (H7) be form-tolerant?**

- For: the author writes figures as words and the training targets do the same; the strict gate fails outputs for sounding like him. The tolerant check already exists and was accepted for Phase 3 curation.
- Against: a restyling tool that turns "100%" into "a hundred percent" changes what the user typed, and a user may want figures left exactly as written. A tolerant gate also has to be trusted not to miss a real change of value.
- A middle path: keep the strict gate for `restyle` of the user's own draft, and add an inference-time rule that copies each figure's original form back when the value matches. That keeps the voice and the user's figures. About a day of work, local.
- If the gate becomes tolerant, B0, B1 and every adapter run must be rescored with it before any comparison is quoted. Scores are cached; it is CPU work.

**Next experiments I would run** (not started unless noted)

| # | Experiment | Why | GPU time |
|---|---|---|---|
| N1 | `sft-v1-s2m` paraphrase tag at N=4 (running) | Is the mixed adapter within the gates as written? | 3.5 h |
| N2 | Recall probe on `sft-v1-s2m` | Verbatim spans rose in every stage 2 variant; H8 must be rechecked | 1 h |
| N3 | Candidate pool from both tags (2 `draft` + 2 `paraphrase`), one rerank | Take the stylish candidate when it passes the gates, the faithful one otherwise | 0 if candidates are cached; else 2 h |
| N4 | Figure-form restore at inference (the middle path above) | Removes form-change failures without touching the gate | CPU |
| N5 | 6-bit fused copy of the chosen adapter at N=4 | Speed gate | 3 h |

**Housekeeping created overnight, not deleted:** adapters `sft-v1-s2`, `sft-v1-s2s`, `sft-v1-s2m`, `sft-v1-s2-i160`, `sft-v1-s2-i320`, `sft-v1-s2-mix30` (175 MB each plus checkpoints, about 4 GB in all) and datasets `sft-v1-{s2s,s1ps,s2m}`. `s2s`, `i160`, `i320` have no further use.

## Queue, in order

Each item: what, why, cost, and the rule that decides it.

| # | Experiment | Why | GPU time | Decision rule |
|---|---|---|---|---|
| 1 | `sft-v1-s2` at N=4, `draft` tag (running) | Does stage 2 help on draft inputs? | 4 h | Keep s2 if composite minus `sft-v1-s1p-n4r` has a CI above 0, or write-op M1 rises with no composite loss |
| 2 | Recall probe on the winner of 1 | H8 must hold for whatever ships | 1 h | Recall flagged and max span no worse than the base (4 prompts, 9 words) |
| 3 | If s2 loses or ties: the step-480 checkpoint of s2 at N=1 | Val loss was lowest there (1.066) | 1 h | Same rule as 1, against the final s2 at N=1 |
| 4 | Decode sweep on the winner, N=1: temp 0.5 / 0.7 / 0.9 | Sentence-length spread is low (z about -2.6); a higher temperature may widen it, a lower one may cut entity errors | 3 h | Pick by composite; check fallback and M9 |
| 5 | Second pass of stage 1 (`--passes 2`) | Stage 1 val loss was still falling at the end (0.58 at step 640) | 3 h train + 1 h eval | Keep only if composite rises and M9 / recall do not; memorization is the risk |
| 6 | Merged-paragraph inputs for stage 2 (`s2p`) | It helped stage 1's paragraphing; stage 2 inputs are not merged | 1.5 h train + 4 h eval | Words per paragraph closer to the author's 34, no composite loss |
| 7 | 6-bit fused copy of the final adapter at N=4, plus its recall probe | The speed gate passes only fused, and only N=1 was scored | 3 h | Composite within noise of the unfused run; 30 tok/s or more |
| 8 | LR sweep for stage 1: 5e-5 against 1e-4 | The plan calls for it; not yet run | 1.5 h train + 1 h eval | Composite at N=1 |

Items 5, 6 and 8 each cost half a day. Run them only after 1-4 settle which adapter is the baseline.

## Open problems, with what I would try

- **Sentence-length spread is too low** (SD 7.1 against the author's 9.3) in every adapter run. Queue item 4 tests temperature. If that fails, the reranker could prefer candidates whose spread is closer.
- **Write-op facts entailed is 86%**, under restyle's 96%. 10 of 62 dev drafts still miss an item after four retries. Next: let the retry fall back to appending the missing fact as a plain sentence before the adapter restyles it.
- **Rebuilt spans.** 61 of 124 outputs share an 8+ word span with their own held-out target. Not gated by decision, but worth one check that it comes from the facts pinning the wording (B0 showed the same effect) and not from near-duplicate passages across posts.
- **Marker chunks have no local drafts.** 296 train chunks keep Claude drafts because marker placement used Claude. The adapter may learn "markers mean Claude-style input". A local rule (put each marker after the paragraph that precedes it in the target, by fact overlap) would remove the Claude dependency.
- **Speed margin is thin** at 30.2 tok/s. Fewer candidates on short inputs, or early stop when the first candidate passes every gate, would cut wall time more than decode speed does.

## Needs a decision (not started)

1. **Hand check of 50 training pairs** (Phase 3 exit). Still not done. Only the user can do it.
2. **Stored copy of the consent.** `~/.quill/legal/scope.yaml` still says `copy: pending`. The whole project rests on it.
3. **Blind reading test** (ship gate H1). The kit exists; it needs a reader who knows the author.
4. **Claude calls for marker placement** in local drafts (about 300 short calls) versus the local rule above.
5. **Speed gate.** Accept 30.2 tok/s fused at 6-bit, relax the gate for the unfused adapter (27 tok/s), or spend time on it.
6. **Delete the 8-bit fused copy** (8.1 GB, `~/.quill/models/qwen3-8b-sft-v1-s1p-fused-8bit`). No further use.
7. **Fair baselines.** B0 and B1 ran without the draft retry. Rerun B1's write op with it (2 h, local) so the headline comparison is like for like. B0 would need Claude calls.
8. **Coverage briefs** for the user's own PM work: still none, so there is no evidence yet on the inputs the tool is actually for.
9. **Uncommitted work** since `85478f3`: local drafts module, stage 2 dataset change, `--local` / `--lr` flags, tests, this file, logbook entries.
