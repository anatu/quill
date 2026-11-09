# Augmenting a Housel style adapter with similar-author data: evidence, mixture designs, similarity selection, and MLX mapping

Scope: the quill style-inversion SFT recipe (LLM neutral paraphrase as input, Housel verbatim as target, prompt masked), with optional ORPO/CPO after it. Target: Morgan Housel, about 342k words in 351 essays (median 806 words), per the coordinator brief. Base: a 7-9B model with 4-bit QLoRA in mlx-lm or mlx-lm-lora on an M4 Pro with 24 GB. Date: 2026-11-08.

Labels used below: **[measured]** means a number reported from an experiment. **[claim]** means an author's assertion or interpretation. **[not re-verified]** means it comes from prior knowledge or a secondary summary and was not re-fetched in this session. Inferences go only in the Inferences subsections.

## 1. Does adding similar-author data help single-author style fidelity at ~100k-500k target words?

### Takeaway
No published study tests similar-author augmentation for one target author at 100k-500k words with an inverse-paraphrase objective. The positive evidence for pooling comes from the low-resource regime (16 texts, ~500 words per target). In that regime, models trained on many authors, or mixtures of several similar-author adapters, beat single-author training. When target data is plentiful, the few direct comparisons favour a dedicated per-target model, and fine-tuning-scale mixing studies find that mixing helps at low data volume but conflicts at high volume. At 342k words Housel sits above the published ">100k words" per-author threshold. Similar-author data is therefore best treated as a regularizer or prior that the training removes or down-weights at the end, not as a co-equal training source.

### Cited Findings
- **Per-author threshold [claim]:** Existing unsupervised authorship-transfer methods like STRAP have a "high-resource training data requirement (often greater than 100,000 words)". Patel et al. define low-resource as "just 16 posts (on average ~500 words)" of the target. arXiv v3 was revised 4 Nov 2024. — [Patel, Andrews, Callison-Burch, arXiv 2212.08986](https://arxiv.org/abs/2212.08986)
- **STRAP design [claim]:** STRAP (Krishna, Wieting, Iyyer, EMNLP 2020; older) fine-tunes a pretrained LM as an inverse paraphraser from neutral text to style, introducing a ~15M-sentence, 11-style corpus (CDS). Separate inverse paraphrasers are trained per style. — [STRAP arXiv 2010.05700](https://arxiv.org/abs/2010.05700), as summarized in the project's lit review (`/Users/natuanand/quill/knowledge_base/lit_review.md`)
- **ASTRAPOP pooled SFT [measured]:** For individual Reddit authors, ASTRAPOP trains one model on pooled pseudo-parallel data from 10,000 training authors (two texts each), conditioned on target exemplars, rather than one model per author.
  - It cites Patel et al. for the claim that the "exemplar-based approach works better than one model per author" in the low-resource case.
  - In its own preliminary experiment on the community task (ETS, 2,000 training segments of 128 tokens per target L1), "one model per author works better than the few-shot exemplar-based" approach. That is a data-rich target.
  - Individual-task results with LLaMA-7B: SFT joint 0.484; DPO 0.507; CPO 0.505; STRAP 0.414. PO lowered SBERT from 0.754 to 0.726-0.733.
  - [ASTRAPOP, arXiv 2403.08043v2](https://arxiv.org/html/2403.08043v2)
- **TinyStyler [measured]:** The model is trained on 88M Reddit comments pooled across authors, conditioned on mean-pooled Wegmann et al. style embeddings, then self-distilled on about 40k filtered pairs.
  - Low-resource joint scores (Random/Single/Diverse): TinyStyler 0.40/0.45/0.36 (0.43/0.48/0.39 with rerank) vs GPT-4 0.33/0.31/0.30 and STRAP 0.05/0.00/0.04.
  - It has no ablation of target-author fine-tuning or data amount.
  - [TinyStyler, arXiv 2406.15586](https://arxiv.org/html/2406.15586)
- **AuthorMix setup (EMNLP 2026; arXiv v4 16 Sep 2026; closest 2026 work):** One LoRA per high-resource Gutenberg author (10 authors, more than 2,000 texts each; rank 8, alpha 16, all linear layers) on LLaMA-3.1-8B-Instruct and Qwen2.5-7B-Instruct. For a new target with only 16 texts, it learns signed per-layer mixing weights over the top-k most stylistically similar author adapters (GRPO reward = sqrt(Toward × MIS)). — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)
- **AuthorMix results [measured], all from [arXiv 2603.23069](https://arxiv.org/abs/2603.23069) (full PDF):**
  - **Main results:** GRPO layer-wise at k=4 gives Joint_STAR 0.34 and Joint_CAV 0.50 (CAV is held-out).
    - ASTRAPOP-SFT, retrained on pooled data (20k samples = 2,000 texts from each of the 10 authors): 0.29 / 0.37.
    - TinyStyler: 0.31 / 0.40.
    - GPT-5.1 few-shot: 0.20 / 0.39.
    - Neutral text: 0.05 / 0.39.
  - **Number of adapters:** k=1 (a single best-matching adapter) scores about 0.17 joint. k=2 scores 0.23-0.32. GRPO layer-wise peaks at k=4 (0.34), stays competitive through k=6, and degrades at k≥7.
  - **[claim]:** "Identifying a good subset of top-k stylistically similar authors is essential." Irrelevant adapters "can degrade the merged model".
  - **Human evaluation:** AuthorMix ties STYLL and TinyStyler on style (0.63 vs 0.63 / 0.61) and wins on meaning (1.61 vs 0.99-1.27 of 2).
  - **Limitations [claim]:** Evaluation covers only literary Gutenberg text; "authors with highly distinctive or contemporary styles" are untested. A per-author adapter "may capture an averaged style".
- **StyleTunedLM data ablation [measured; reference size per the fetched summary, verify]:** Per-author LoRA on Llama-2-7b for 10 Gutenberg authors, averaged across authors (the summary gave 80k tokens as the 100% reference):

  | Training data | Embedding cosine | Classifier accuracy |
  |---|---|---|
  | 5% | 0.57 | 0.11 |
  | 35% | 0.74 | 0.44 |
  | 70% | 0.92 | 0.81 |
  | 100% | 0.95 | 0.88 |

  Masking named entities in the loss cut training-name reuse for Wodehouse from 0.50 to 0.23, with little style loss. — [StyleTunedLM, arXiv 2409.04574](https://arxiv.org/html/2409.04574v1)
- **Dong et al., SFT data composition [measured]:**
  - "Data composition appears to enhance various abilities under limited data conditions, yet can lead to performance conflicts when data is plentiful." For LLaMA-7B the turning point fell between 1/64 and 1/16 of their full data.
  - [claim]: "The amount of composition data influences performance more than the composition ratio."
  - [Dong et al., arXiv 2310.05492](https://arxiv.org/html/2310.05492)
- **OPPU [measured]:** OPPU trains the base on held-out "other users" first, then plugs in a per-user PEFT.
  - Retrieval + OPPU gave 1.93% and 2.48% relative gains over the non-retrieval and retrieval-only variants on LaMP.
  - There is no ablation of the shared base.
  - [OPPU, arXiv 2402.04401v3](https://arxiv.org/html/2402.04401v3)
- **DITTO and Panza [claim]:** Neither uses other authors' data. DITTO aligns to fewer than 10 demonstrations with self-generated negatives (+33.4 win-rate points over few-shot on Mistral 7B). Panza fine-tunes on a single user's emails. — [DITTO, arXiv 2406.00888](https://arxiv.org/html/2406.00888); [Panza, arXiv 2407.10994](https://arxiv.org/html/2407.10994); both via the project notes `/Users/natuanand/quill/knowledge_base/research_notes/Personal writing style models/academic_style_imitation.md`
- **ITDA [claim]:** Inverse transfer data augmentation (ITDA) has an LLM strip style from stylized texts to make neutral-to-stylized pairs for a small seq2seq model (GPT-3.5 pairs; BART-base). This is the same idea as quill's inversion, and it augments with target-style text only. — [ITDA, OpenReview](https://openreview.net/pdf/7285ef94ef19db8222a532cbdb061aa7b8a5d873.pdf); [GitHub](https://github.com/Vicky-Shao/ITDA)

### Inferences
- **The regime matters.** Every result where other-author data clearly wins has a target with ~16 texts (Patel, TinyStyler, ASTRAPOP-individual, AuthorMix). At 342k words, Housel resembles ASTRAPOP's community setting, where a dedicated per-target model beat the pooled exemplar model. Expect pooling to give little or negative fidelity gain unless the extra data fixes a specific coverage gap.
- **The real problem is representativeness, not volume.** StyleTunedLM's curve flattens between 70% and 100% of its per-author set, which is well below Housel's ~450k tokens (estimate: about 1.3 tokens per word). Housel's corpus is large enough for style capture. The risk the user describes is coverage: registers, topics and lengths Housel never wrote, such as technical explainers or long-form structure. Auxiliary data should target those gaps.
- **Housel probably fits Dong et al.'s "plentiful" side.** At ~600-800-word chunks, 351 essays give roughly 400-500 pairs. At 150-300-word chunks they give roughly 1.2k-2.3k pairs. Dong et al.'s turning point (1/64-1/16 of their data) is on the order of 1-7k samples per ability. This is a loose cross-task analogy only.
- **AuthorMix's k=1 result does not generalize to quill.** k=1 was worse than k≥2 because the target had no adapter of its own. Quill will have a strong Housel adapter, so an auxiliary adapter can only act as a regularizer with a small weight.

### Gaps
- I found no experiment that adds similar-author data to a target with 100k-500k words and measures target fidelity (authorship verification against the target). This includes STRAP, STYLL, TinyStyler, StyleTunedLM, ASTRAPOP, AuthorMix, Panza, DITTO and anything from 2025-2026 that I located.
- I found no 2025-2026 paper on nonfiction or essay authorship transfer with augmentation. AuthorMix is literary only.
- StyleTunedLM's per-author token count (80k as the 100% reference) came from a summarizer and should be confirmed in the PDF.

## 2. Mixture designs and known ratios

### Takeaway
No ratio has been measured for style. The defensible designs are:
1. Tagged pooling with a Housel-majority token share.
2. Two-stage training: a cluster stage, then a Housel-only anneal with optional small replay.
3. A separate Housel LoRA plus a cluster LoRA, combined by weighted rank concatenation with a small auxiliary weight.

Analogues from fine-tuning and pretraining support a final target-only phase and very small replay fractions (DMT k=1/256; upsampling in the last 10-20% of training). LoRA concatenation (CAT) beat data mixing by about 12% in one skill-composition study but not in all of them.

### Cited Findings
- **Pooling with repetition [measured]:** "Up to 4 epochs of repeated data yields negligible changes to loss compared to having unique data"; with more repetition "the value of adding compute eventually decays to zero". This is pretraining scale. — [Muennighoff et al., arXiv 2305.16264](https://arxiv.org/abs/2305.16264)
- **Control tags or metadata [measured]:** MeCo prepends URL metadata for most of pretraining, then runs a cooldown on plain text. A 1.6B model "matches the downstream task performance of standard pre-training while using 33% less data". Conditioning prompts on metadata at inference steers the model. The fraction of training given to cooldown was not in the abstract. — [MeCo, arXiv 2501.01956](https://arxiv.org/abs/2501.01956)
- **User identifiers [measured]:** A single shared model with "fixed, non-trainable user identifiers" added to inputs outperformed prefix-tuning personalization "by up to 13%" on sentiment tasks, with no extra parameters. This dates from 2021-22 (older). — [UserIdentifier, arXiv 2110.00135](https://arxiv.org/abs/2110.00135)
- **Tagged back-translation [not re-verified; older, 2019]:** In MT, marking synthetic data with a tag lets a model use it without being pulled toward its distribution. — [Caswell et al., arXiv 1906.06442](https://arxiv.org/abs/1906.06442)
- **Two-stage DMT [measured]:** Stage 1 trains on specialized data. Stage 2 trains on general data mixed with a fraction k of the specialized data. Tested k: 1, 1/2, 1/4, 1/8, 1/16, 1/32 and 1/256; headline k = 1/256.
  - LLaMA-7B (GSM8K / HumanEval / MT-Bench):

    | Strategy | GSM8K | HumanEval | MT-Bench |
    |---|---|---|---|
    | Multi-task | 47.53 | 14.63 | 5.76 |
    | Sequential | 31.39 | 15.85 | 5.72 |
    | Mixed sequential | 32.60 | 15.24 | 6.02 |
    | DMT | 41.92 | 17.68 | 6.08 |

  - There is a "linear inverse trend" between the two abilities as k rises from 1/256 to 1/4. "k needs to be tuned."
  - [Dong et al., arXiv 2310.05492](https://arxiv.org/html/2310.05492)
- **Domain adaptation then task adaptation [claim; older, 2020]:** DAPT followed by TAPT ("multi-phase adaptive pretraining") gives large gains. TAPT on a task corpus augmented by "simple data selection strategies" is "an effective alternative". — [Gururangan et al., arXiv 2004.10964](https://arxiv.org/abs/2004.10964)
- **Annealing with domain upsampling [measured]:** For a 7B model trained on 1T tokens, upsampling domain data relative to CommonCrawl at the end of training, ablated from 5% to 30% of training, works best at 10-20%. Gains: up to +6.90 pp MMLU, +8.26 pp GSM8K and +6.17 pp HumanEval. — [Blakeney et al., arXiv 2406.03476](https://arxiv.org/abs/2406.03476)
- **LoRA Soups, CAT definition [measured]:** CAT = per-layer weighted sum of frozen skill LoRA updates, ΔW = α1·B1A1 + α2·B2A2, with α in [0,1] learned on at least 5% of each skill's data. Static 0.5/0.5 CAT was worse than learned CAT. — [LoRA Soups, arXiv 2410.13025](https://arxiv.org/html/2410.13025)
- **LoRA Soups results [measured]:**
  - GSM-Hard: math-only LoRA 14.18%; DATA-MIX 18.8%; CAT 21.11% (21.63 ± 1.07 over 3 seeds). CAT beat DATA-MIX by about 12% and model merging by 43% on average.
  - TIES and DARE were worse than data mixing.
  - With three prompt formats, DATA-MIX beat every merge. The authors say data mixing is still best "for many skills".
  - Averaging A and B separately introduces "additional cross-terms" compared with summing the BA products.
  - [LoRA Soups, arXiv 2410.13025](https://arxiv.org/html/2410.13025)
- **AuthorMix weight findings [measured]:**
  - Signed weights are essential. Convex (softmax) mixing collapsed: k=4 joint 0.01, with 94/100 pairs collapsed, vs 0.34 signed.
  - Learned weights are strongest and positive in the middle layers (14-21 of 32) and mostly negative in the deep layers (24-31).
  - It cites StyleRemix (Fisher et al. 2024): merging five or more adapters degrades fluency.
  - [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)
- **Style LoRA plus instruction LoRA [claim]:** StyleTunedLM concatenated A and B matrices of a style LoRA and a LIMA instruction LoRA, kept MMLU at 0.336-0.340 across merge ratios, and claims a higher style proportion improves style alignment. The authors' table is hard to interpret. — [StyleTunedLM, arXiv 2409.04574](https://arxiv.org/html/2409.04574v1)
- **TIES and DARE [not re-verified]:**
  - TIES trims small deltas, elects a per-parameter sign and averages only agreeing deltas. — [TIES, arXiv 2306.01708](https://arxiv.org/abs/2306.01708)
  - DARE randomly drops a fraction p of delta parameters and rescales the rest by 1/(1−p). — [DARE, arXiv 2311.03099](https://arxiv.org/abs/2311.03099)

### Inferences
**Candidate designs.** All are untested for style, and all ratios are mine. Run each against D0.

| ID | Design | Proposed mix | Rationale |
|---|---|---|---|
| D0 | Housel-only baseline | 100% Housel, 2-3 epochs | Required control. Every other design must beat it on held-out Housel. |
| D1 | Tagged pooling | Author tag in the prompt (masked from loss), for example `Author: Morgan Housel` vs `Author: <other>`. Housel is at least 65-75% of target tokens after up to 2× upsampling. Auxiliary authors are at most 25-35% in total, at most about 10% each, from k = 2-4 authors. | Tags let shared features (short paragraphs, anecdote then principle) transfer while the Housel tag isolates his specific features (MeCo, UserIdentifier, tagged back-translation). The k range follows AuthorMix's k=2-4 sweet spot and the reported fluency loss at five or more adapters. |
| D2 | Two-stage anneal (preferred first experiment) | Stage 1: tagged pool with Housel at 30-50%, 1 epoch. Stage 2: Housel-only continuation, 1-2 epochs at about 0.3-0.5× the stage-1 LR, with optional replay of auxiliary data at 0-5%. | The final phase is pure target (Blakeney; DAPT→TAPT; DMT). DMT shows tiny replay fractions (1/256) already help retention. The anneal directly limits dilution, which matches the user's constraint. |
| D3 | Separate LoRAs, weighted concatenation | Housel LoRA (weight 1.0) plus a cluster LoRA trained on auxiliary authors only (or auxiliary plus Housel). Sweep the cluster weight w ∈ {0, 0.1, 0.25, 0.5}, global or split by middle and deep layers. | Cheap to sweep after training and reversible. CAT beat data mixing in one study. AuthorMix suggests middle layers carry style and deep-layer contributions are often suppressed, so try w_middle > 0 and w_deep ≈ 0. |
| D4 | Tag only in ORPO/CPO | SFT on Housel only. In ORPO, use a neighbour author's styled output for the same input as a hard "rejected" alongside the self-generated rejects. | Turns similar authors into a contrast that sharpens Housel-specific features instead of a source to imitate. ASTRAPOP-CPO reproduced idiosyncrasies. |

- **Write ratios in tokens.** Dong et al. found absolute amount matters more than ratio. Specify "N auxiliary tokens" (for example 50k, 100k or 150k words) and report the resulting share, not only percentages. Arithmetic: 342k Housel words at a 70% share allow about 147k auxiliary words without upsampling, or about 293k with 2× Housel upsampling.
- **Upsampling ceiling.** Following Muennighoff, keep total Housel exposures at or below about 4 epochs across stages. Repetition beyond that adds little and risks memorization. Panza and the project plan already flag LR and epoch sensitivity.
- **Expected ordering.** For the "little dilution" constraint I expect D2 ≥ D0 ≈ D1 > naive untagged pooling, with D3 as a cheap post-hoc dial. This is a hypothesis, not a finding.

### Gaps
- No study reports tag-conditioned multi-author SFT for author style with an ablation of the tag. Evidence for tags comes from pretraining (MeCo), classification personalization (UserIdentifier) and MT (tagged back-translation).
- No measured optimum exists for replay fraction or anneal length in style SFT.
- I did not confirm MeCo's metadata-to-cooldown split (often quoted as 90/10). It was not in the abstract.

## 3. Data mixing laws and domain weighting: what they imply at fine-tuning scale

### Takeaway
Mixing laws (Ye et al.), DoReMi and RegMix optimize pretraining mixtures over many domains using many small proxy runs. Quill has 2-5 sources and about 0.5-1M tokens, so a direct sweep of 3-5 mixtures on the real recipe is cheaper and more trustworthy than fitting a law. Their usable lessons are: the end-of-training mix matters most; there is a critical proportion below which the target is forgotten; and amount matters more than ratio at small scale.

### Cited Findings
- **Data mixing laws [measured]:**
  - Performance is "quantitatively predictable" from mixture proportions using fitted function forms, combined with step and size scaling laws.
  - For a 1B model on 100B RedPajama tokens, the optimized mix matched the default mix trained for 48% more steps.
  - [claim]: The laws "accurately predict the critical mixture proportion that avoids catastrophic forgetting" in continual training.
  - [Ye et al., arXiv 2403.16952](https://arxiv.org/abs/2403.16952)
- **DoReMi [not re-verified]:** A small proxy model trained with group DRO sets domain weights for a larger model. Reported gains on The Pile: about +6.5 points average few-shot accuracy, and baseline accuracy in about 2.6× fewer steps. — [DoReMi, arXiv 2305.10429](https://arxiv.org/abs/2305.10429)
- **RegMix [not re-verified]:** Fits a regression over hundreds of tiny proxy runs on random mixtures and picks the predicted best. The authors report results comparable to or better than DoReMi at a fraction of the compute. — [RegMix, arXiv 2407.01492](https://arxiv.org/abs/2407.01492)
- **End-of-training upsampling [measured]:** 10-20% of training is optimal. — [Blakeney et al., arXiv 2406.03476](https://arxiv.org/abs/2406.03476)
- **Fine-tuning scale [measured]:** "The amount of composition data influences performance more than the composition ratio." Mixing helps when data is limited and conflicts when it is plentiful. — [Dong et al., arXiv 2310.05492](https://arxiv.org/html/2310.05492)

### Inferences
- **The objective differs.** Mixing laws target average loss or benchmark accuracy over domains. Quill's objective is fidelity on one domain (held-out Housel), and validation loss is a poor proxy for style. The project plan already notes that quality rose while validation loss did not. So "optimal mixture" should be judged by the Housel-only authorship-verification composite, not loss.
- **A practical "mixing law" for quill.** Sweep auxiliary words in {0, 50k, 150k, 300k} under D1 or D2. Fit nothing. Pick the smallest amount that improves held-out Housel AV or the composite with a CI excluding 0. If none does, use D0.
- **The critical-proportion idea maps onto D2.** Measure the Housel share at which the stage-1 adapter's held-out Housel AV accept rate falls below D0's. That share bounds how much dilution stage 2 must undo.

### Gaps
- I found no application of DoReMi, RegMix or mixing laws to SFT or LoRA style tuning.
- DoReMi and RegMix numbers above are from memory and should be checked against the abstracts if they will be quoted.

## 4. Similarity-based data selection: DSIR, embedding nearest neighbours, AV-score selection; passage vs author level

### Takeaway
Select at two levels. First, admit 2-4 authors by centroid similarity on a content-robust style encoder, which is what AuthorMix does. Second, filter passages within admitted authors by a style score that is debiased against topic. DSIR's hashed n-grams and generic semantic nearest neighbours mostly select by topic, which for Housel means finance passages, not his voice. The encoder used to select data must differ from the encoder used to evaluate, or the evaluation is gamed.

### Cited Findings
- **DSIR [measured]:** Importance resampling on hashed n-gram features. KL reduction on those features "highly correlates with average downstream accuracy (r=0.82)". It performs comparably to expert curation on 8 targets and gives +2-2.5% GLUE over random selection. — [DSIR, arXiv 2302.03169](https://arxiv.org/abs/2302.03169)
- **AuthorMix author-level selection [measured]:** Each author's prototype is the mean style embedding of sampled texts. The target prototype is the mean of its 16 references. The top-k authors by cosine are admitted. Mixing over irrelevant adapters "can even hurt". Selection and reward used STAR embeddings, and evaluation used a held-out, topic-controlled CAV encoder. — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)
- **TinyStyler [claim]:** It separates the conditioning and filter encoder (Wegmann style embeddings) from the evaluation encoder (UAR/LUAR, "held out for evaluation"). — [TinyStyler, arXiv 2406.15586](https://arxiv.org/html/2406.15586)
- **Augmented TAPT [claim; older]:** Augmenting the target corpus via simple data selection from a larger domain pool is effective. — [Gururangan et al., arXiv 2004.10964](https://arxiv.org/abs/2004.10964)
- **Content-similar examples [measured]:** Content-similar demonstrations reduced attribution (Enron AA 69.33 → 36.00). Topical overlap inflates apparent style matching. — [Catch Me If You Can? Not Yet, arXiv 2509.14543](https://arxiv.org/html/2509.14543v1), via the project notes `/Users/natuanand/quill/knowledge_base/research_notes/Personal writing style models/academic_style_imitation.md`

### Inferences
- **Author level first.** Housel's tics are author-level patterns (structure, cadence, recurring moves). Passages selected from many loosely similar authors give a style average with no coherent second voice. Two to four admitted authors also make the tags in D1 meaningful.
- **Passage level second, and debiased.** Within an admitted author, rank passages by a style score that has been residualized against a content embedding, or computed on content-masked text (content words replaced by POS tags, keeping function words and punctuation). Keep the top 30-60%. Also drop passages whose topic is near-duplicate with Housel test essays, to avoid contamination.
- **Treat DSIR as a topic tool.** It can be useful for picking auxiliary passages that cover registers or topics Housel lacks, which is the coverage-gap motive, but not for voice.
- **AV-score selection is a gaming risk.** Selecting passages that a Housel verifier scores high, then evaluating with the same verifier, inflates results. Use, for example, StyleDistance plus function-word Delta for selection, and the char-n-gram AV classifier plus LUAR plus blind human review for evaluation. This matches the plan's separation of rerank and evaluation models.

### Gaps
- I found no published use of authorship-verification scores to select fine-tuning data for style. Evidence is limited to selecting adapters (AuthorMix) and filtering synthetic pairs (TinyStyler).

## 5. Measuring similarity: StyleDistance, LUAR, STEL / Wegmann content control, Burrows' Delta; topic leakage; thresholds

### Takeaway
No single encoder is reliable. StyleDistance is the most content-independent on STEL-or-Content, but even it scores only 0.29. On long-form literary author discrimination it was weak (AUC 0.56), while a topic-controlled encoder trained on in-domain text (CAV, AUC 0.72) and STAR (AUC 0.71) did better. LUAR mixes style with content. Use an ensemble, calibrate every metric against a Housel within-author ceiling and an impostor floor, and admit authors by normalized position between floor and ceiling, not by raw cosine.

### Cited Findings
- **STEL / STEL-or-Content (S-o-C) averages [measured]:**

  | Encoder | STEL | S-o-C |
  |---|---|---|
  | roberta-base | 0.90 | 0.05 |
  | LUAR | 0.86 | 0.03 |
  | LISA | 0.71 | 0.03 |
  | Wegmann et al. 2022 | 0.77 | 0.22 |
  | StyleDistance | 0.87 | 0.29 |
  | StyleDistance (synthetic only) | 0.76 | 0.31 |

  — [StyleDistance, arXiv 2410.12757](https://arxiv.org/html/2410.12757)
- **StyleDistance on other tasks [measured]:** Style-transfer evaluation accuracy: StyleDistance 0.46 vs LUAR 0.38, Wegmann 0.39 and human 0.37. Authorship-verification ROC-AUC: StyleDistance 0.64, LISA 0.57, Wegmann 0.56. — [StyleDistance, arXiv 2410.12757](https://arxiv.org/html/2410.12757)
- **StyleDistance on leakage and limits [claim]:** LUAR "considers both style and content". Proxy metadata (subreddit, conversation) fails as a content control because the same author writes on the same topic across venues. The model is sentence-level and covers 40 synthetic features. — [StyleDistance, arXiv 2410.12757](https://arxiv.org/html/2410.12757)
- **StyleDistance model card [claim]:** A RoBERTa-base sentence-transformer (MIT license) trained on SynthSTEL (40 features) plus Reddit authorship data, claiming "stronger content-independence than other style embedding models". The card does not say whether it suits sentences or passages, and its example uses sentences. — [HF card](https://huggingface.co/StyleDistance/styledistance)
- **LUAR model card [claim]:** LUAR-MUD is trained on the Reddit Million User Dataset. It embeds "episodes" of several documents into 512-d vectors, and episode length must be consistent. The card states no topic caveats. Apache-2.0. — [HF card](https://huggingface.co/rrivera1849/LUAR-MUD)
- **Wegmann content control [measured]:** "Representations trained by controlling for conversation are better than representations trained with domain" or no content control. — [Wegmann et al., arXiv 2204.04907](https://arxiv.org/abs/2204.04907)
- **AuthorMix encoder comparison [measured]:** Held-out 50-author Gutenberg author-retrieval test (R@8 / AUC):

  | Encoder | R@8 | AUC |
  |---|---|---|
  | CAV (topic-controlled, trained on Gutenberg) | 58.3 | 0.72 |
  | STAR | 63.7 | 0.71 |
  | LUAR-MUD | 40.0 | 0.58 |
  | Wegmann style embeddings | 30.9 | 0.59 |
  | StyleDistance | 33.4 | 0.56 |
  | StyleDistance (synthetic) | 28.1 | 0.54 |

  Under CAV, mean within-author similarity was 0.37 vs 0.05 between authors. Human style judgments did not correlate with the embedding-based Toward score (ρ = 0.10, n.s.). — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)
- **CAV construction [claim]:** CAV was trained with pseudo-topics from k-means (k = 50) over MiniLM content embeddings. The triplet objective pulls same-author texts together across topics and pushes different authors apart within a topic. — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)
- **Stable attribution length [claim]:** About 5-10k words are needed for stable stylometric attribution (Eder, as cited by StyleTunedLM and the project plan). — [Eder methodology](https://computationalstylistics.github.io/projects/methodology); `/Users/natuanand/quill/knowledge_base/plan.md`
- **Delta variants [not re-verified]:** Cosine Delta on z-scored most-frequent-word frequencies is generally among the most robust Delta variants for authorship attribution. — [Evert et al. 2017, DSH](https://academic.oup.com/dsh/article/32/suppl_2/ii4/3865676)

### Inferences
- **Topic-leakage failure modes for Housel:**
  1. Finance and investing writers score close on LUAR and SBERT-like encoders because of shared vocabulary (compounding, risk, markets), not voice.
  2. Collaborative Fund colleagues share a house format and editing, which reads as a voice match but may be editorial style.
  3. Sentence-level StyleDistance on short chunks rewards surface punctuation and length features that LLM prose also has (short declaratives, colons).
  4. Episode-level LUAR gives inflated similarity when one episode contains several essays on the same topic.
- **Mitigations:**
  - Compute all similarities on topic-disjoint chunk pairs: cluster Housel and candidates by content embedding and compare only across clusters.
  - Add function-word Cosine Delta on the top 150-300 MFWs, using at least 5k words per side.
  - Train a quill-specific CAV-style encoder with pseudo-topic control (AuthorMix's recipe) if the off-the-shelf encoders fail the sanity check below.
- **Sanity check before use.** Each encoder must place held-out Housel above same-register impostors (AUC ≥ 0.80, as in the plan) on topic-disjoint splits. Drop any encoder that fails.
- **Thresholds (my proposal).** For each metric m and chunk size (for example 800-word chunks, and 5k-word bundles for Delta), compute:
  - Housel ceiling C_m = median sim(held-out Housel chunk, Housel train centroid), on topic-disjoint chunks.
  - Floor F_m = median sim(random same-register impostor chunk, Housel centroid).
  - LLM anchor L_m = median sim(Claude/LLM paraphrase chunk, Housel centroid). Use the neutral inputs of the inversion pairs.
  - Normalized score s_m(a) = (sim(a) − F_m) / (C_m − F_m).

  Admit author a if s_m(a) ≥ 0.5 on at least 2 of 3 metrics (StyleDistance, LUAR or CAV, Delta), and sim(a) − L_m ≥ 0.5·(C_m − L_m) on StyleDistance. Expect no candidate near 1.0; AuthorMix's 0.37 vs 0.05 within/between gap implies authors sit far below the ceiling. Use the rank among candidates (top 2-4) once they pass the floor.
- **Passage threshold.** Within admitted authors, keep passages with s_m ≥ the candidate author's own median, which halves the pool, or ≥ the 25th percentile of the Housel within-author distribution if that keeps enough text.

### Gaps
- I found no published guidance on absolute cosine thresholds for StyleDistance or LUAR "same style" decisions. Thresholds must be calibrated locally.
- The chunk length used in AuthorMix's encoder comparison was not checked. StyleDistance's weakness may partly reflect long inputs, since it was trained at sentence level. Averaging sentence embeddings, which the plan does, may behave differently.
- I did not re-fetch Burrows' Delta and Eder robustness numbers.

## 6. Dilution risks, the LLM-imitation problem, mitigations, and eval metrics that detect dilution

### Takeaway
The main risks are:
1. Style averaging toward a "cluster voice".
2. Loss of Housel's verifier-salient tics.
3. Register mismatch.
4. Drift toward LLM prose, because Housel-like writers, and Housel imitators in particular, sit closer to LLM cadence.

The only dilution test that counts is held-out, topic-disjoint Housel. Pair it with a verifier that discriminates Housel from the admitted auxiliary authors specifically, not only from random impostors.

### Cited Findings
- **Averaged style [claim]:** "An author's style varies across works, genres, topics and periods, so such an adapter may capture an averaged style." — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)
- **Mixing conflicts [measured]:** Mixing more than five adapters degrades fluency (StyleRemix, cited by AuthorMix). Multi-task mixing "hurts general ability most" while preserving specialized ability, and sequential training forgets. — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069); [Dong et al., arXiv 2310.05492](https://arxiv.org/html/2310.05492)
- **Pooled models and quirks [measured]:** Pooled multi-author models capture fewer idiosyncrasies. ASTRAPOP's pooled SFT Toward score was 0.137. CPO raised it to 0.165 and uniquely reproduced idiosyncrasies (the typo "alot", all-lowercase text, a space before commas). — [ASTRAPOP, arXiv 2403.08043v2](https://arxiv.org/html/2403.08043v2), via `/Users/natuanand/quill/knowledge_base/lit_review.md`
- **LLM voice [measured]:** The "LLM voice" is a property of instruction-tuned weights. Biber features separate Llama 3 and GPT-4o from humans, more strongly for instruction-tuned models. — [Reinhart et al., PNAS 2025, arXiv 2410.16107](https://arxiv.org/abs/2410.16107), via `/Users/natuanand/quill/knowledge_base/lit_review.md`
- **Housel and LLM prose [project opinion, not a measurement]:** Housel's "short-sentence 'insight' cadence has been widely imitated, including by LLMs". — `/Users/natuanand/quill/knowledge_base/research_notes/Nonfiction author style corpora/science_business_history_writers.md`; `/Users/natuanand/quill/knowledge_base/style_library.md`
- **Entity leakage [measured]:** Name leakage from training text is real and can be reduced with entity masking in the loss (Wodehouse 0.50 → 0.23). — [StyleTunedLM, arXiv 2409.04574](https://arxiv.org/html/2409.04574v1)
- **Metric validity [measured]:** Embedding-based Toward did not correlate with human style judgments (ρ = 0.10). Automated style metrics alone cannot certify fidelity. — [AuthorMix, arXiv 2603.23069](https://arxiv.org/abs/2603.23069)

### Inferences
- **The LLM-imitation mechanism in style inversion.** The inversion input is an LLM paraphrase. If an auxiliary author's original is already close to LLM prose, the input-to-target pair needs little rewriting, so the model learns to copy the input. Mitigations:
  1. Reject auxiliary authors whose StyleDistance similarity to the LLM-paraphrase centroid L exceeds Housel's own (the gate in section 5).
  2. Prefer auxiliary text written before ChatGPT (before Nov 2022), and drop post-2023 posts with LLM-marker density above Housel's 90th percentile. The project's temporal-prior notes cover this: `/Users/natuanand/quill/knowledge_base/research_notes/AI text weak supervision priors/temporal_priors.md`.
  3. Filter auxiliary pairs by a "style gap", sim(target, Housel) − sim(input, Housel) > 0, so every pair teaches movement toward Housel.
- **Register mismatch.** Prefer auxiliary authors in the same register (short essays, anecdote then principle, second person, about 600-1,200 words). Chunk auxiliary text to Housel's length distribution. Mismatched lengths also skew mlx-lm batches (section 7).
- **Losing tics.** Build a Housel tic inventory from training text: features with high log-odds for Housel against the admitted auxiliary authors, such as sentence-length distribution, one-line paragraphs, rhetorical questions, signature transitions and quote framing. Track the JSD between output and held-out-Housel tic distributions. Rising JSD from D0 to D1 or D2 is dilution.
- **Eval suite to detect dilution.** Housel held-out is the only gold test, topic-disjoint from training.
  1. AV accept rate against Housel with impostors drawn from the admitted auxiliary authors and generic same-register writers. Report both.
  2. An (n+2)-way attribution classifier over {Housel, aux_1..aux_k, LLM}. Track the share of outputs attributed to an auxiliary author or to the LLM class; this is the direct dilution meter.
  3. StyleDistance delta (cos to Housel minus cos to LLM centroid).
  4. Tic-distribution JSD.
  5. MIS and entity gate for meaning.
  6. Blind human pairwise test (D0 vs best mixture), since embedding metrics may not track human style judgment.
- **Acceptance rule.** Adopt a mixture only if it is at least D0 on AV accept rate and on the attribution share to Housel, and better on at least one coverage-gap probe (prompts in registers Housel lacks), with CIs from the plan's bootstrap.

### Gaps
- I found no measurement placing specific Housel-like human authors relative to LLM prose. The "widely imitated" claim is an opinion in the project notes. The separate similarity agent's LLM-centroid distances would settle it.
- I found no study that measures tic loss when pooling authors for style SFT.

## 7. MLX practicalities on a 24 GB M4 Pro

### Takeaway
Neither mlx-lm (v0.32.2, 16 Oct 2026) nor mlx-lm-lora supports per-sample loss weights, mixture sampling probabilities, curricula or multi-adapter merging. Every design is still implementable:
- Upsample by duplicating rows, or by listing a dataset twice in `hf_dataset`.
- Use tags as prompt text.
- Run two stages with `--resume-adapter-file`.
- Merge adapters manually by concatenating LoRA ranks in safetensors, which gives an exact weighted sum of updates.

Memory is unaffected by the mixture; only run count and time grow.

### Cited Findings
- **Release [measured]:** mlx-lm's latest release is v0.32.2 (published 2026-10-16). — [GitHub releases API](https://api.github.com/repos/ml-explore/mlx-lm/releases)
- **Data loading [claim, docs]:** One `train.jsonl` per `--data` directory, or a Hugging Face dataset. `hf_dataset` takes a single mapping or a list. `--mask-prompt` works only for chat and completions formats. The docs describe no per-sample loss weights, mixing or sampling weights, and no multi-adapter merging. — [mlx-lm LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- **Code behaviour [measured, read from source on main, 2026-11-08]:**
  - A list of `hf_dataset` entries is combined by `ConcatenatedDataset` with no weights (`_dataset` index stored, never used for weighting).
  - `iterate_batches` sorts all examples by length, cuts consecutive batches, and shuffles batch order each pass.
  - `default_loss` divides the summed masked cross-entropy by the batch's token count, so longer completions carry proportionally more gradient.
  - `--resume-adapter-file` calls `model.load_weights(...)` on adapter weights.
  - The LR schedule comes from `lr_schedule` in the YAML (`name`, `arguments`, optional `warmup`, `warmup_init`).
  - `LoRALinear` computes `y + scale * ((x @ lora_a) @ lora_b)` with `lora_a` of shape (in, r) and `lora_b` of shape (r, out); `fuse` adds `scale * lora_b.T @ lora_a.T`.
  - [datasets.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/tuner/datasets.py); [trainer.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/tuner/trainer.py); [lora.py (CLI)](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/lora.py); [tuner/lora.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/tuner/lora.py); [tuner/utils.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/tuner/utils.py)
- **mlx-lm-lora [claim, README]:**
  - Modes: sft, dpo, cpo, orpo, dsla, ftpo, grpo, online_dpo, xpo, rlhf-reinforce, ppo, klpo.
  - Local JSONL or HF datasets with custom field names.
  - `--fuse` merges one adapter into the base.
  - There is no dataset mixing, sampling weights, per-sample weights, curriculum or multi-adapter merging. `--reward-weights` weights GRPO reward functions, not data. ORPO rows may carry a `preference_score` field whose use is undocumented.
  - Self-reported M4 Pro 24 GB: Qwen3-8B 4-bit SFT at about 4.1 it/s and about 6-10 GB (batch 1, 4k context, all layers, 100 steps).
  - [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora)
- **Fuse flags [claim]:** `mlx_lm.fuse` takes `--adapter-path`, `--save-path`, `--dequantize` and `--export-gguf`; GGUF export is limited to llama, mistral and mixtral. — [fuse.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/fuse.py), via `/Users/natuanand/quill/knowledge_base/research_notes/Personal writing style models/apple_silicon_stack.md`
- **Serving [claim]:** `mlx_lm.server` accepts a per-request `adapters` path, so merged or variant adapters can be served without fusing. — [SERVER.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md), via `/Users/natuanand/quill/knowledge_base/plan.md`

### Inferences
How each design maps onto mlx-lm (none tested):

- **Upsampling (D0, D1).** Duplicate Housel rows in `train.jsonl` with a fixed seed, shuffling before writing. Alternatively, list the Housel source twice in `hf_dataset` (for example `path: json` with `config: {data_files: ...}`, passed through to `datasets.load_dataset`), which `ConcatenatedDataset` will then include twice. Set `--iters` = (rows × epochs) / (batch × grad-accum).
- **Token-share control.** Because loss is token-weighted per batch and batches are length-sorted, chunk auxiliary text to Housel's length distribution and compute shares in target tokens. Otherwise long auxiliary chunks dominate whole batches.
- **Tags (D1).** Put the tag in the system or user message: `Author: Morgan Housel` for Housel rows, `Author: <name>` for auxiliary rows. With `--mask-prompt` it gets no loss. Always use the Housel tag at inference, including in the quill MCP template. Probe tag use by generating with an auxiliary tag on dev inputs; if outputs do not change, the model is ignoring tags.
- **Two-stage (D2).**
  1. Run `mlx_lm.lora --train --data pool/ --adapter-path ad_stage1 ...`.
  2. Run `mlx_lm.lora --train --data housel/ --resume-adapter-file ad_stage1/adapters.safetensors --adapter-path ad_stage2 --learning-rate <lower> ...`.

  Keep rank, scale and layer count identical across stages. The source I read loads adapter weights only and showed no optimizer-state restore, so expect a fresh Adam state and add a short warmup via `lr_schedule`. For DMT-style replay, put 0-5% auxiliary rows into `housel/train.jsonl`.
- **Separate LoRAs plus weighted rank concatenation (D3).** This is exact, about 20 lines of `mlx.core` code, and needs no dense deltas:
  1. Train both adapters with the same layer set.
  2. For each key, set `A_cat = concat([A_h, A_c], axis=1)` and `B_cat = concat([(w_h·s_h/s)·B_h, (w_c·s_c/s)·B_c], axis=0)`.
  3. Write `adapters.safetensors` plus an `adapter_config.json` with rank r_h + r_c and scale s.
  4. Load with `--adapter-path` or serve per request. Per-layer weights (middle vs deep) are a per-key choice of w_c.

  Do not average A and B separately; LoRA Soups notes this introduces cross-terms.
- **TIES or DARE.** These need dense ΔW per layer. Options: compute `scale·A@B` layer by layer in bf16, apply TIES or DARE, then (a) truncate back to low rank by SVD, which is lossy, or (b) add into a dequantized base. For a 9B model, (b) means about 18 GB of bf16 weights, which is tight on 24 GB; prefer (a) or rank concatenation. Given LoRA Soups' finding that TIES and DARE underperformed data mixing, they are low priority.
- **Memory.** Mixing changes data volume, not peak memory. Expect about the same peak as D0 (about 6-10 GB self-reported for Qwen3-8B 4-bit at 4k context). D2 and D3 cost one extra run each. Merging is offline and light.
- **Preference stage (D4).** mlx-lm-lora ORPO and CPO read `{prompt, chosen, rejected}` (plus an optional system field) per row. Auxiliary-author hard negatives are just extra rows. No weighting exists, so control their share by row count.

### Gaps
- I did not run any of these commands. Behaviour of a duplicated `hf_dataset` entry and of `path: json` with `data_files` is inferred from the source, not tested.
- I did not check mergekit's TIES/DARE CPU path on HF-format, MLX-exported weights.
- I did not verify whether `mlx_lm.lora` saves optimizer state in checkpoints anywhere other than the code paths I grepped.
- Qwen3.5-9B-specific memory or throughput on an M4 Pro 24 GB was not measured independently. The only figure is the self-reported Qwen3-8B number.
