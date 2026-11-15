# Quill build plan, v3

Written 2026-11-15. It replaces v2, which was built around imitating one essayist and is kept at [archive/plan-v2-essayist.md](archive/plan-v2-essayist.md) with every threshold and source. Day-by-day results are in [logbook.md](logbook.md); open decisions and the experiment queue are in [followup.md](followup.md); the corpus search is in [corpus_research.md](corpus_research.md).

## What changed from v2

| | v2 | v3 |
|---|---|---|
| Goal | Sound like one named essayist | Write exposition that reads like a high-quality textbook, better than Claude does when told to |
| Judge | A reader who knows the author; an authorship verifier | The user, an expert reader, picking blind against prompted Claude |
| Task | `restyle`: change the voice, keep the content fixed | `explain`: write the passage from sparse notes. `restyle` stays as a second op |
| Corpus | Morgan Housel's Collaborative Fund essays | Peterson and Davie, *Computer Networks: A Systems Approach* (CC BY 4.0); more open textbooks to follow |
| Why | | Restyling moved the essayist's voice (verifier accept 24% → 85%) but adds nothing a textbook is valued for. See section 3 |

Lay-reader preference is not a goal. The user ruled it out: it is too broad and rewards punchy, theatrical writing.

## 1. Summary

Quill is a small local model that turns notes into textbook-quality prose. Claude, in the session, works out the content: the points to teach and the details available. Quill writes the exposition. It is a QLoRA adapter on Qwen3-8B (4-bit, MLX) trained on an Apple Silicon Mac, to be served to Claude Code as an MCP tool. Prompt-only solutions are out of scope as the product; prompted Claude is the baseline to beat.

Status: the pipeline, eval harness and two corpora are built. A restyling adapter exists for each corpus. The first explain adapter has been trained and compared: it has the register and makes errors; Claude with exemplars is accurate and lacks the register (logbook 2026-11-15). Nothing is served yet.

## 2. Architecture

### 2.1 Runtime (planned; Phase 9)

```
User in Claude Code -> Claude works out CORE points and MATERIAL (details, example data)
   | thin skill routes the request; no style instructions
   v
quill MCP tool -> local daemon
   1 render the shared prompt template (op, input kind, length, voice)
   2 sample N=4 candidates: Qwen3-8B 4-bit + adapter (6-bit fused copy for speed)
   3 hard gates: no name, number, date or link the notes lack, none dropped;
     length within 30%; no 8-word span from the corpus; no chatbot residue
   4 rank the survivors; return the best, or the notes back with the failed check named
```

### 2.2 Offline

```
source text (licence and consent recorded) -> extract, clean, dedupe, chunk 150-800 words
  -> corpus.sqlite -> frozen topic-disjoint splits
  -> pairs:  restyle  paraphrase -> passage, draft -> passage
             explain  notes (CORE + shuffled MATERIAL) -> passage
  -> curate -> mlx chat JSONL -> mlx_lm.lora -> eval on dev -> blind read -> test once
```

### 2.3 Components

| Component | Choice | Notes |
|---|---|---|
| Base model | `mlx-community/Qwen3-8B-4bit` | Qwen3.5-9B cannot be trained with mlx-lm 0.32.2 on 24 GB (logbook 2026-11-10) |
| Adapter | LoRA rank 16, scale 2.0, dropout 0.05, all 36 layers | 43.6M trainable parameters |
| Training | adamw, cosine with warmup, batch 1, accumulation 16, loss on the assistant turn only | `configs/train/sft.yaml`; `--iters` counts micro-batches |
| Serving copy | Fuse with `--dequantize`, re-quantize to 6 bits | Fusing straight into 4-bit erases the adapter; 6-bit holds quality at 32.5 tok/s |
| Template | `quill v2 / op / input / length / voice` | `src/quill/template.py`; identical in training and inference |
| Voices | One config per corpus | `configs/quill.yaml` (essayist), `configs/textbook.yaml` (`voice: tb`); data under `~/.quill/` and `~/.quill/tb/`; reports under `eval_reports/` and `eval_reports/tb/` |
| Claude calls | `claude -p`, cached; blocked unless the consent record allows | Pair building, baselines, judge |

### 2.4 Ground rules

- **Consent and licence first.** Each corpus has a record in `~/.quill/legal/`. A use marked unknown there blocks the step that needs it. For both corpora, publishing model outputs and releasing weights are marked unknown.
- **Honour AI opt-outs.** robots.txt blocks, "no LLM" notices and publisher terms rule a source out unless the rights holder agrees. OpenStax, Quanta, Khan Academy, the Feynman Lectures and several personal sites were excluded on this ground.
- **Local only.** Corpora, adapters and weights stay on the Mac and out of git. Public reports hold aggregate numbers only.
- **No passing off.** Outputs are never presented as an author's own writing. Tool, file and adapter names carry no author's name.
- **No copying.** A hard gate rejects any output with an 8-word span from the corpus. A recall probe checks the adapter does not recite more than the untuned base.
- **Attribution.** Peterson and Davie ask for: title, authors, "Copyright: Elsevier, 2012", the repository URL and the licence.

## 3. Why restyling is not enough for this goal

Style inversion trains a model to turn a plain version of a passage back into the passage. Every fact and every ordering decision in the target is already in the input, by design, so the model never invents. That teaches what is on the surface: rhythm, paragraphing, word choice.

- **For the essayist it worked.** His voice is on the surface. Best adapter on dev: composite 0.763 against 0.256 for the untuned base and 0.25 for prompted Opus.
- **For a textbook it does not.** The surface is plain. A neutral paraphrase of textbook prose is close to a copy (median word overlap 0.81, against 0.72 for the essayist), and a restyled Claude draft is a light edit. Fed Claude's own textbook-prompted prose, the adapter returns it nearly unchanged.
- **What separates a good textbook from prompted Claude is content judgement:** restating a definition a second way, working a numeric example through, separating near-synonyms, linking each sentence to the last, deciding what the reader needs next. A restyler is forbidden from doing any of that and is never shown it being done.

So the task changes.

## 4. The explain task

- **Input: notes.** Claude reduces each passage to CORE (three to six points it teaches; no examples, restatements or motivation) and MATERIAL (the specific details it draws on, as bare data). MATERIAL is shuffled per chunk.
- **Target: the passage.**
- **What the model must supply:** the order of exposition, the restatements, the use of material as worked examples, the distinctions, the connective reasoning.
- **What it may not supply:** facts. Every name and number in a target is in its notes (a missing one is added to MATERIAL during curation), so the entity gate applies unchanged.
- **Curation:** at least two core points and some material; the target adds no name, number, date or link; notes at 0.10-0.75 of the target's length; the example fits 2,048 tokens. First build: 428 of 475 train pairs kept.
- **Known risk:** writing 300 words from notes gives an 8B model more room to garble meaning than restyling does. The restyling adapter already made meaning errors on unfamiliar material in its freer mode.

## 5. Corpora

| | Essayist (voice 1) | Textbook (voice `tb`) |
|---|---|---|
| Source | Morgan Housel, Collaborative Fund blog | Peterson and Davie, *Computer Networks: A Systems Approach*, repository source |
| Basis | Consent from Collaborative Fund, reported by the user; copy pending | CC BY 4.0; consent reported by the user (the publisher signals reluctance about AI use); copy pending |
| Size | 330 posts, 318,971 words, 835 chunks | 61 sections, 213,738 words, 570 chunks |
| Splits (chunks) | 688 train / 62 dev / 85 test | 475 train / 39 dev / 56 test |
| Use now | Finished experiment; adapter kept | Active |

The textbook corpus is below the 300,000 words the first had. Candidates to add, each needing its licence and AI stance read by hand first: the same authors' other open books; DeVoe, *Thermodynamics and Chemistry*; Lane, *Online Statistics Education*; and with ShareAlike, Lebl, Hefferon, OpenIntro, Crowell. See [corpus_research.md](corpus_research.md).

## 6. Evaluation

**The result that counts:** blind pairs, the user picking. Same notes, two passages, order randomized: quill against Claude given the same notes, a textbook instruction and three real passages from the book. Detecting a 65% preference takes about 85 picks; 60% takes about 195.

**Baselines on the same notes**
- `bt`: Claude Opus told to write like a high-quality textbook.
- `bt-ex`: the same with three real passages as exemplars. This is the bar.

**Automatic checks, as guards and diagnostics**

| Check | What it guards | Threshold carried over from v2 |
|---|---|---|
| Entity gate | No name, number, date or link added or dropped | 100% of returned outputs |
| Fallback rate | How often no candidate passes the gates | ≤ 15% |
| Copying | 8-word spans from the corpus in outputs; recall probe against the base | 0 in returned outputs; probe rate no worse than the base (wording under review, followup.md) |
| Tic profile | Sentence length and spread, paragraph length, against the book | Reported |
| Memory, speed | Training peak, decode rate | ≤ 17 GB; ≥ 30 tok/s |

The authorship verifier (M1) and the classifier (M15) were built to tell one essayist from other writers and from plain drafts. They are reported for the textbook voice but are weak instruments there, and they are not the goal. An LLM judge is not used as the referee: judges favour familiar, low-perplexity prose, and a Claude judge favours Claude.

**Dev is small** for the textbook (39 chunks, 34 with usable notes). Differences need the paired bootstrap, and the test split (56 chunks) is touched once, with the final system.

## 7. Phases

| Phase | State |
|---|---|
| 0 Source and consent audit | Done for both corpora; stored consent copies pending |
| 1 Extraction and cleaning | Done for both. Readers: `ingest/collabfund.py` (HTML), `ingest/rst.py` (Sphinx source) |
| 2 Splits, eval harness, baselines | Done for the essayist. Textbook: splits and eval inputs frozen; textbook-specific baselines being run |
| 3 Restyle pairs | Done for both. Textbook: 379 paraphrase pairs, 460 draft pairs |
| 4 Model bake-off | Done. Qwen3-8B |
| 5 Restyle fine-tune | Done for both. Essayist: works. Textbook: does not beat prompted Claude (section 3) |
| 5x Explain task | **First run done.** `tb-x1` matches the book's register (voice check 100% of passages, the book 100%, Claude with exemplars 32%) and averages 2.1 major errors a passage (Claude with exemplars 0.06). Neither system has both. Next: realise a planned backbone of typed moves with bound details, checked per move; design and experiment arms in [harness_research.md](harness_research.md) |
| 6 Inference pipeline | Not started. Drafter retry, gates and rerank exist as eval code |
| 8 Ship gate | Blind picks by the user against `bt-ex`; then one run on test |
| 9 MCP serving in Claude Code | Not started |

## 8. What is settled, with the evidence

- Fine-tuning moves surface style far more than prompting does (essayist: verifier accept 85% against 24%).
- Training on drafts alone reaches the style ceiling and drops names and numbers; paraphrase and draft pairs together hold both.
- Most dropped facts in `write` came from the untuned drafter; a redraft that names the lost items cut fallback from 30% to 10%.
- Fusing an adapter into 4-bit weights erases it; 6-bit after de-quantizing does not.
- The adapter raises recall of training text slightly (2.7-3.0% of probe prompts against 1.6%; not significant). The inference gate keeps it out of returned outputs.
- On unfamiliar material the freer restyle mode makes meaning errors. Dev scores on the author's own content did not predict that.

## 9. Risks

| Risk | Mitigation |
|---|---|
| The explain adapter garbles meaning or invents claims | Entity gate; fact-entailment check; the user's read. If frequent, stop and keep quill as a smoothing pass |
| Claude with exemplars already matches the book | Then the fine-tune is not worth serving for this register; the comparison is run before any serving work |
| One book teaches networking, not exposition | Add open textbooks from other subjects before drawing conclusions about transfer |
| Dev reuse and a small dev set | Paired bootstrap; test touched once |
| Consent records without a stored copy | Both marked `copy: pending`; publishing outputs or weights stays blocked |
| Base model memorized a famous textbook | Recall probe against the untuned base; 8-word gate |

## 10. Open decisions

Kept in [followup.md](followup.md): the wording of the copying criterion, whether the entity gate should tolerate a figure written another way, cleanup of rejected adapters, which books to add, and whether outputs may be published.
