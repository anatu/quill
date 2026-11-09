# Personal Writing-Style Models: Literature Review

As of 2026-11-07. Earlier research in this conversation: none.

Sources: five research notes in `knowledge_base/research_notes/Personal writing style models/`, compiled 2026-11-07: `academic_style_imitation.md`, `data_and_objectives.md`, `style_evaluation.md`, `practitioner_examples.md`, `apple_silicon_stack.md`. Every web source in those notes was fetched or searched on 2026-11-07. The build plan is a separate document: `/Users/natuanand/quill/knowledge_base/plan.md`.

**Question.** How can one person build a tool whose output is stylistically indistinguishable from their own writing, using a model trained or adapted on that writing, with all training done locally on an Apple M4 Pro with 24 GB unified memory? What do the literature and practitioners say about prompting, retrieval, fine-tuning and style-transfer rewriting; data volume; data construction; evaluation; and local tooling?

**Evidence markers.**
- **[unverified]**: the notes saw this only in a search summary, snippet, mirror or secondary review.
- **[self-reported]**: a tool author's or practitioner's own numbers.
- **[estimate]**: scaled or triangulated figure, not measured.
- **[vendor claim]**: marketing or company documentation.
- **[inference]**: reasoning by the notes' author or by this review, not a source finding.

Dates are publication dates, using the arXiv month where available. Practitioner posts without a visible year carry the year the notes inferred from the models mentioned.

---

## 1. Key findings

1. **Prompting alone fails on informal personal writing.** With 5 same-author examples, frontier models pass a blog authorship verifier 16.7–21.3% of the time, against 95–97% for news and email (Wang et al. 2025). Expert readers reject prompted imitations of authors (fidelity OR 0.16) and prefer fine-tuned ones (OR 8.16) (Chakrabarty et al. 2025).
2. **The "LLM voice" lives in instruction-tuned weights.** It persists across model sizes, is stronger after instruction tuning, and survives rewriting by another LLM (Reinhart et al. 2025; Sun et al. 2025).
3. **Retrieval wins on ROUGE-scored benchmarks and loses on style-scored ones.** RAG gives +14.92% on LaMP against +1.07% for per-user LoRA (Salemi & Zamani 2024). On style metrics, RAG "largely fail[s] to match a given user's writing style" (Panza 2024). The defensible design is hybrid: weights for voice, retrieval for facts.
4. **Weight updates have the only strong human-judged wins.** Acquaintances identify which person a Panza model imitates ~64% of the time (chance 25%). 29 of 30 fine-tuned author models beat expert human imitators on fidelity (Chakrabarty). DITTO beats few-shot prompting by 33.4 win-rate points with 7 demonstrations.
5. **Data needs are modest for tone and larger for distributional style.** Panza reaches ~90% of maximum BLEU at 25 emails and calls 50–100 emails "convincing." StyleTunedLM needs ~56k–80k tokens for strong stylometric fidelity. A rank-8 LoRA on 73 paragraphs gave near-zero stylometric gain (InMyStyle 2026).
6. **Data construction converges on inversion.** Neutralize the author's text, then train neutral → original (STRAP, TinyStyler, ASTRAPOP). The best human-judged fine-tunes train on LLM-written content descriptions or reverse instructions paired with the untouched real text (Chakrabarty; Panza).
7. **Preference optimization adds a modest gain at a meaning cost.** ASTRAPOP joint score rises 0.484 → 0.507 while SBERT similarity falls 0.754 → 0.733. Pushed further, DPO degrades writing quality and lexical diversity (Antislop 2025).
8. **Small rewriters beat frontier prompting on style and lose on meaning.** TinyStyler with reranking scores joint 0.43–0.48 against GPT-4's 0.30–0.33, with meaning similarity 0.59 against 0.71. Every system moves text only a short way toward the target author (Towards ≤ ~0.16).
9. **No single evaluation metric is trustworthy.** Style embeddings vary in content leakage (LUAR STEL-or-Content 0.03; StyleDistance 0.29). Local 8B LLM judges score below chance. Self-ratings correlate weakly with embeddings (r ≈ 0.24). Use a calibrated battery plus blind human tests.
10. **Practitioners agree on the shape of the problem.** About 30 projects (2023–2026) report that fine-tuning captures voice and fails on facts, that cleaning data is most of the work, that training loss misleads, and that a frontier model for content plus a small tuned model for voice is the converging design. None published a blind head-to-head against a well-prompted frontier model.
11. **Commercial "write in my voice" products prompt; they do not train per user.** Most build a style profile and inject it into prompts. Per-user fine-tuning is left to open-source and local tools.
12. **On a 24 GB M4 Pro, QLoRA on 7–9B models via mlx-lm is the practical path.** mlx-lm v0.32.2 (2026-10-16) handles SFT. Preference stages need the community package mlx-lm-lora. `mlx_lm.server` serves adapters per request without fusing.

---

## 2. The "LLM voice" problem

Default assistant prose is a distinct, measurable register.

- **Grammar and rhetoric.** Reinhart et al., "Do LLMs write like humans? Variation in grammatical and rhetorical styles" (PNAS 122, 2025; arXiv:2410.16107). Biber features on parallel corpora separate Llama 3 variants and GPT-4o from humans. The gap persists from small to large models and is larger for instruction-tuned models than base models.
- **Fingerprints.** Sun, Yin, Xu, Kolter, Liu, "Idiosyncrasies in Large Language Models" (ICML 2025; arXiv:2502.12150). A fine-tuned embedding classifier identifies ChatGPT, Claude, Grok, Gemini and DeepSeek outputs at 97.1% in a five-way task. The fingerprints survive rewriting, translation and summarization by another LLM, so part of them lives in content choices.
- **Averaging.** DITTO (Shaikh et al., ICLR 2025; arXiv:2406.00888): models "aligned to emulate the collective voice of many" produce "outputs that align with no one in particular."
- **Probability.** StyleMC (Khan, Wang, Hager, Andrews 2023; arXiv:2312.17242): human writing dips into low-probability regions; LM sampling picks likely tokens.
- **Perplexity.** Jemama & Kumar (IEEE UEMCON 2025; arXiv:2509.24930): imitations that pass a style verifier still average perplexity ~15.2 against ~29.5 for human essays. Style fidelity and detectability are separable.
- **Default style.** Spohn, Girrbach, Akata, "APM" (arXiv:2605.21063, May 2026): "Typical LLM responses tend to follow a default style." For implicit style preferences on Llama-3.1-8B and Qwen-3.5-27B, routing was most reliable, RAG helped only with the stronger base, and soft-prompt optimization did not beat a non-personalized baseline.
- **What experts penalize.** Chakrabarty, Ginsburg, Dhillon (arXiv:2510.13939, 2025): clichés, purple prose, over-exposition, missing subtext, mixed metaphors. Each unit of Pangram detector score cut MFA readers' odds of choosing an excerpt for fidelity by a factor of 6.3. Mediation analysis shows fine-tuning removes the quirks that drive both detection and dispreference.
- **Post-editing does not escape it.** Baumler et al., "Can You Make It Sound Like You? Post-Editing LLM-Generated Text for Personal Style" (UMD; arXiv:2604.24444, Apr 2026; pre-registered, n=81). Post-editing an o4-mini draft moved text toward the author (g=0.55) and away from LLM text (g=−0.41). The result stayed far closer to the draft than to the author's unassisted writing (g=−1.43) and was more homogeneous across people (g=1.42).

[inference] The target is a register the base weights resist. Prompts and post-editing push against it. Weight updates move it.

---

## 3. Prompting vs retrieval vs fine-tuning

### 3.1 Prompting and few-shot imitation

The largest study is Wang, Tripto, Park, Li, Zhou, "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors" (Findings of EMNLP 2025; arXiv:2509.14543). Setup: 40,000+ generations per model from 400+ real authors (Enron 150, Blog 100, CCAT50 50, Reddit 100). Models: GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, Gemma-3-27B, DeepSeek-V3, Llama-4-Maverick. Scoring: authorship attribution (AA), authorship verification (AV), style matching (LIWC-22 + WritePrints, Mahalanobis distance) and GPTZero.

| Corpus | GPT-4o top-5 AA, 5-shot vs 0-shot | AV pass rate, 5-shot, range across models |
|---|---|---|
| CCAT50 news | 86.64 vs 83.88 | 94.68–97.44% |
| Enron email | 59.65 vs 28.62 | 95.65–96.64% |
| Reddit | 27.12 vs 18.77 | 49.97% (DeepSeek-V3) – 65.88% (Gemini) |
| Blog | 39.39 vs 17.22 | 16.72% (Gemma-3-27B) – 21.25% (Gemini); 0-shot 8.15–10.35% |

Further results from the same paper:
- **Detection.** Share labeled "human" by GPTZero at 5-shot: GPT-4o Enron 16.86%, CCAT50 0.08%, Reddit 0.67%, Blog 0.47%. Gemini-2.0-Flash 18.74–54.25%. Gemma-3-27B at most 43.63% (Enron). Real human text 99.2–100%. The authors caution GPTZero may favor detecting GPT-family output.
- **More shots.** 2 → 10 demonstrations gave "limited gains" (figure only).
- **Topic-matched shots hurt.** Averaged over three LLMs, content-similar demonstrations cut AA: Enron 69.33 → 36.00, Reddit 35.43 → 16.63, Blog 43.93 → 22.13. Length matching cut Reddit style accuracy 71.80 → 56.60.
- **Opening snippets help.** Adding the opening of the target text roughly doubled "human" rates on Reddit and Blog.
- **Generic tone.** Outputs "often default to an average, generic tone."
- **Limits.** No large human evaluation. Within-genre only. Zero-shot AA sits above chance because of topic overlap. Code: github.com/jaaack-wang/llms-implicit-writing-styles-imitation.

Other academic evidence:
- **Expert readers.** Chakrabarty et al. (2025), preregistered; MFA-trained writers vs ChatGPT/GPT-4o, Claude 3.5 Sonnet and Gemini 1.5 Pro emulating 50 award-winning authors in ≤450-word excerpts; 28 MFA readers and 516 college-educated readers. In-context prompting (instructions + few-shot) was disfavored by MFA readers for fidelity (OR 0.16) and quality (OR 0.13). General readers showed no fidelity preference (OR 1.06). Pangram flagged 97% as AI. Conclusion: "models cannot emulate an author's style properly just by prompting."
- **Instruction tuning hurts few-shot imitation.** StyleMC (Khan et al. 2023): instruction-tuned models "can struggle to reproduce author-specific style demonstrated in a prompt" from a few hundred words. GPT-3.5 did worse than earlier generations.
- **Fine-tuning vs shots on a 7B.** StyleTunedLM (Liu, Diddee, Ippolito; INLG 2024; arXiv:2409.04574): LoRA beat 5-shot, 10-shot and instruct prompting. Classifier accuracy 0.879 vs 0.693 / 0.680 / 0.263. Lexical MSE 1.39 vs 3.80 / 3.31 / 2.67. Surface MSE 2.04 vs 5.43 (5-shot). Caveats: famous authors, likely in pretraining; no frontier models tested.
- **Counter-evidence.** Jemama & Kumar (2025): five open models (Llama, Qwen, Mixtral) on academic essays. Few-shot gave up to 23.5× zero-shot style-matching accuracy. Completion prompting reached 99.9% agreement under the paper's own TF-IDF + embedding verifier. Prompt strategy mattered more than model size. One formal genre, custom verifier.
- **Agent tone.** arXiv:2507.04889 (Jul 2025): fine-tuning beat system prompting for agent tone of voice with 100 samples [unverified].
- **Claude styles vs fine-tuning.** A dev.to experiment (thatechmaestro) on Steven Pressfield's writing found fine-tuning "the more reliable though often more resource intensive option" against Claude's custom styles and manual prompting [unverified].

Practitioner reports agree for informal and idiosyncratic voices:
- **grapeot (2024-12-23)** tried abstract style descriptions, references to famous writers, random few-shot, retrieval-based few-shot ("no significant gain") and commercial style features. All failed. Fine-tuned Qwen came "often very close to the reference."
- **Sarah Constantin:** prompting is "lousy for making a bot with a writing style that's substantially different from the generic ChatGPT 'character'." With pasted samples, "it inexorably reverts to the bland 'house style.'"
- **Gabor Cselle (2023-11-29):** his earlier few-shot approach at Pebble failed to match users' voices.
- **Writekin (2026-07-28):** a SKILL.md of anti-AI-phrasing rules "improved the surface somewhat"; Pangram still rated output nearly 100% AI.
- **Nic Lydon (2026, inferred):** "Prompt engineering has a ceiling for voice matching." His baseline was the untuned base model, a weak comparison.

Counter-views:
- **NicAI (2026-09-20):** "Prompting comes first." "The real baseline is a well-prompted frontier model, not a generic one."
- **Reddit commenter (~2025-11, snapshot 2026-05-08):** fine-tuning is "overkill" for personal style; put 10–15 of your sentences in a system prompt.
- **OpenAI's Ted Sanders (2023-04-15, quoted by Simon Willison):** fine-tuning is not recommended "as a way to teach the model knowledge."
- **Miller HN thread (2023-04):** sounding like someone differs from thinking like them; "you won't get more facts out than you provide as input" (MayeulC).

Gaps: no study runs the Wang protocol on GPT-5-class, Claude 4.x or Gemini 2.5/3 models. No controlled study compares LLM-extracted style guides against raw demonstrations for individual authors. No practitioner ran a blind head-to-head against a strong frontier prompt.

### 3.2 Retrieval-augmented personalization

- **LaMP** (Salemi, Mysore, Bendersky, Zamani; arXiv:2304.11406, Apr 2023; venue commonly cited as ACL 2024, venue not verified in the academic note; the data note cites an ACL 2024 Anthology preview). Seven tasks (3 classification, 4 generation). Term-matching, semantic and time-aware retrievers all help. A secondary review reports ~23.5% gains for fine-tuned and 12.2% for zero-shot models [unverified].
- **LongLaMP** (Kumar, Viswanathan, Yerra, Salemi, Rossi, Dernoncourt, Deilamsalehy, Chen; arXiv:2407.11016, 2024). Personalized emails, abstracts, reviews and topic writing. BM25/Contriever RAG improved metrics 5.7% to 128% over non-personalized baselines. Metrics: ROUGE-1, ROUGE-L.
- **REST-PG** (Salemi et al., Google; arXiv:2501.04167, Jan 2025). Reasoning over a user's past preferences and style plus EM-style reinforced self-training. +14.5% average relative gain on LongLaMP.
- **"Teach LLMs to Personalize"** (Li et al., Google; arXiv:2308.07968, 2023). Retrieval → ranking → summarization → synthesis → generation beat baselines on three datasets.
- **Fine-grained linguistic control benchmark** (Alhafni, Kulkarni, Kumar, Raheja; arXiv:2402.04914, 2024). Personalization over lexical and syntactic attributes.
- **RAG vs PEFT head-to-head.** Salemi & Zamani, "Comparing Retrieval-Augmentation and Parameter-Efficient Fine-Tuning for Privacy-Preserving Personalization of LLMs" (arXiv:2409.09510, Sep 2024). FlanT5-XXL (11B), 512-token input, 128-token output, LoRA trained 50 epochs per user.
  - RAG +14.92%, per-user LoRA +1.07%, RAG+PEFT +15.98% average over non-personalized.
  - PEFT helped 5/7 datasets; RAG helped all 7.
  - PEFT gains rise with profile size; RAG gains fall. RAG suits cold start; PEFT suits data-rich users.
  - PEFT gained most on LaMP-6 (email subjects from the private Avocado corpus), i.e. data unlikely to be in pretraining.
  - ~200 MB per adapter, ~20 PB for 100M users.
- **Style-scored evidence against RAG alone.** Panza (Nicolicioiu et al.; arXiv:2407.10994, Jul 2024): base LLMs with RAG "largely fail to match a given user's writing style." All fine-tuning variants beat Pretrained+RAG "by a large margin." Leading closed LLMs "yielded similarly poor results."
- **Surveys.** Zhang et al., "Personalization of LLMs: A Survey" (TMLR; arXiv:2411.00027, Nov 2024). Liu et al., "A Survey of Personalized LLMs: Progress and Future Directions" (arXiv:2502.11528, Feb 2025), with a prompting / adapter / alignment taxonomy.

Why the rankings disagree [inference in notes]: LaMP scores short outputs (titles, headlines, tweets) with ROUGE, where retrieving topical history directly raises n-gram overlap. Distributional style metrics (MAUVE) and expert or acquaintance judges flip the ranking toward fine-tuning.

### 3.3 Weight-based adaptation

**Per-user PEFT**
- **OPPU** (Tan, Zeng, Tian, Liu, Yin, Jiang, "Democratizing LLMs via Personalized PEFT"; EMNLP 2024; arXiv:2402.04401). One LoRA per user (~0.5% of parameters) on a task-adapted base, plus retrieval and profiles. Beat prompt-based methods on all seven LaMP tasks. Strongest under user behavior shift. "Integrating non-parametric and parametric knowledge performs the best." Examples: 17.38% relative MAE gain on LaMP-3; +3.42% ROUGE-1 on scholarly title generation. Main test set: the 100 most active users.
- **PER-PCS** (Tan, Liu, Jiang, "Personalized Pieces"; EMNLP 2024; arXiv:2406.10471). Users share PEFT pieces; target users assemble one from their history. Comparable to OPPU at lower storage and compute.
- **CARD** (Song et al.; arXiv:2601.06352, Jan 2026). Group LoRAs over style clusters, plus per-user preference vectors and low-rank logit corrections at decoding. Motivated by per-user parameters being costly and unstable with sparse histories. Gains on LaMP and LongLaMP.
- **Panza** (2024): RoSA (sparse + low-rank) ≈ full fine-tuning > LoRA, especially on MAUVE, across backbones and users. Training was "highly sensitive to learning rate and the number of training epochs." Models kept >98% of Llama-3-8B-Instruct performance on six Open LLM Leaderboard tasks. Acquaintances identified which person a model imitated at ~64% precision/recall (chance 25%). Only 28–32% of Panza emails were judged suspicious by evaluators who knew the author.

**Full and API fine-tuning**
- **Chakrabarty et al. (2025).** GPT-4o fine-tuned through the OpenAI API on each of 30 living authors' complete works, cut into 250–650-word excerpts paired with GPT-4o content descriptions. 1 epoch for large oeuvres (Atwood, Ishiguro, Rushdie, Murakami), 3 otherwise; batch 1; LR multiplier 2; one author had only two books.
  - MFA readers favored the fine-tuned AI for fidelity (OR 8.16) and quality (OR 1.87). General readers favored it for fidelity (OR 16.65).
  - 29 of 30 author models exceeded parity on fidelity (median win rate 0.83).
  - Cost $25–$276 per author, median $81.
- **Related blind pairwise study** (arXiv:2601.18353; title and authors not confirmed; a search summary attributes it to Chakrabarty & Dhillon, CHI 2026 [unverified]). 28 MFA writers, 131 Prolific readers, 150 in-context pairs and 90 fine-tuned pairs (GPT-4o, 30 authors). Against fine-tuned GPT-4o, experts chose the AI for fidelity 81.1% and lay readers 80.0%.

**Why LoRA works as a regularizer**
- Biderman et al., "LoRA Learns Less and Forgets Less" (TMLR 2024; arXiv:2405.09673, May 2024). LoRA trails full fine-tuning in-domain, preserves out-of-domain performance better, regularizes more than weight decay or dropout, and keeps generations more diverse.
- Schulman et al., "LoRA Without Regret" (Thinking Machines blog, Sep 2025; HF TRL replication docs). Apply LoRA to all weight matrices, especially MLP and MoE layers, even with small data. Attention-only LoRA underperforms at matched parameter count. Optimal LoRA LR is ~10× full-FT LR and roughly rank-independent. Low ranks fall off the full-FT curve after a step count tied to rank. LoRA tolerates large batches poorly.

### 3.4 Training-free steering and decoding-time control

- **StyleVector** (Zhang et al., "Personalized Text Generation with Contrastive Activation Steering"; arXiv:2503.05213, 2025; ACL 2025 venue [unverified]). Style as an activation-space vector, to separate content from style. +8% relative improvement; 1700× less storage than PEFT.
- **Style vectors** (Konen et al.; Findings of EACL 2024; arXiv:2402.01618). Activation steering for sentiment, emotion and writing style, added at hidden layers (e.g. LLaMA layers 18–20). Shown mainly on coarse styles; writing-style numbers not retrieved.
- **n-gram logit injection** (Ahmed; arXiv:2601.16224, Jan 2026; TinyLlama-1.1B). Works only in a narrow window (λ=0.1 on a single-author corpus: style perplexity −24.7%) and collapses fluency above it. "Consistently outperformed by prompting and LoRA." LoRA (r=8, α=16, LR 2e-4, 800 steps) was "the most reliable and effective method overall." Comparisons not like-for-like.
- **PsPLUG** (Song et al.; arXiv:2601.06362, Jan 2026). Names "personalization collapse": explicit style instructions ("be formal") override user-specific characteristics. Proposes a user-specific residual with tunable strength.

### 3.5 Comparison of approaches

Magnitudes come from different genres, models and metrics. No paper compares all families on the same users with human evaluation.

| Approach | Target-author data | Strongest evidence for | Strongest evidence against | Runs locally on 24 GB M4 Pro |
|---|---|---|---|---|
| Prompting / few-shot ICL, incl. style guides | 2–10 samples in context | Email/news AV 95–97% at 5-shot (Wang 2025). Completion prompting 97–100% pass on a custom verifier (Jemama & Kumar 2025) | Blog AV 16.7–21.3%; flat beyond ~5 shots; topic-matched shots hurt (Wang 2025). Expert fidelity OR 0.16, 97% detected (Chakrabarty 2025). Anti-AI rules still ~100% AI on Pangram (Writekin) | Frontier API; any local model |
| Retrieval-augmented prompting | Any history; best at cold start | +14.92% on LaMP vs +1.07% PEFT (Salemi & Zamani 2024). LongLaMP +5.7–128% ROUGE | "Largely fail to match a given user's writing style" (Panza 2024). Gains fall as profiles grow. Helps only with a strong base (APM 2026) | Yes |
| Per-user PEFT (LoRA, DoRA, RoSA), incl. OPPU, PER-PCS | ~25–100 emails for most content gain; ~56–80k tokens for strong stylometry | OPPU beats prompting on 7/7 LaMP tasks. Panza identifiable by acquaintances (~64% vs 25%). StyleTunedLM 0.879 vs 0.693 (5-shot) | Small gains with sparse data (Salemi & Zamani). LoRA < RoSA/FFT on MAUVE (Panza). Rank-8 LoRA on 73 paragraphs near-zero stylometric gain (InMyStyle 2026) | Yes: QLoRA at 7–9B, bf16 LoRA at 3–4B |
| Full / API fine-tuning | Hundreds of emails to whole oeuvres | Fine-tuned GPT-4o: expert fidelity OR 8.16, lay OR 16.65, 29/30 authors above parity, median $81 (Chakrabarty 2025). FFT ≈ RoSA > LoRA (Panza) | Hyperparameter-sensitive. Rare regurgitation and content omission needed resampling (Chakrabarty) | Full FT only below ~1–2B |
| Preference / online imitation (DITTO, ASTRAPOP, GRPO, ORPO/SimPO) | 5–10 demonstrations (DITTO, ASTRAPOP) | DITTO +11 over SFT, +33.4 over few-shot at 7 demos. ASTRAPOP joint 0.484 → 0.507 | Meaning drops (SBERT 0.754 → 0.726–0.733). DPO degrades quality and diversity (Antislop). Evaluated mostly by GPT-4 win rate or embeddings | ORPO/DPO via mlx-lm-lora; 8–9B memory unmeasured |
| Style-transfer rewriters (STRAP, STYLL, TinyStyler, ParaGuide, StyleMC) | STRAP >100k words; universal models 5–16 samples (~500 words) | TinyStyler + rerank joint 0.43–0.48 vs GPT-4 0.30–0.33, 0.47 s per example. StyleMC beats prompted GPT-4 | Towards ≤ ~0.16 for all systems. Sim 0.59 vs GPT-4 0.71. "Not yet mastery" (Patel 2022). Short Reddit text only | TinyStyler (800M) yes |
| Activation steering / logit injection | Some user texts, no training | StyleVector +8% relative, 1700× less storage | Coarse styles or ROUGE benchmarks only. Logit injection beaten by prompting and LoRA (Ahmed 2026) | Requires layer hooks; research effort |

---

## 4. Style-transfer rewriters

This line separates content from style by design. Paraphrase the text to a neutral form, then reconstruct it in the target style.

- **STRAP** (Krishna, Wieting, Iyyer, "Reformulating Unsupervised Style Transfer as Paraphrase Generation"; EMNLP 2020; arXiv:2010.05700). An inverse paraphraser per style learns neutral → styled. Introduced a ~15M-sentence, 11-style corpus (CDS). Significantly beat prior systems on human and automatic evaluations. A survey of 23 papers found automatic style-transfer metrics "can be easily gamed."
- **STYLL / low-resource authorship style transfer** (Patel, Andrews, Callison-Burch, "Low-Resource Authorship Style Transfer: Can Non-Famous Authors Be Imitated?"; arXiv:2212.08986, Dec 2022). STRAP-style models need "often greater than 100,000 words," so they suit famous authors. The task caps targets at 16 Reddit posts (~500 words). In-context STYLL was the strongest baseline; "current approaches do not yet achieve mastery." Introduced Away / Towards / Sim / Joint metrics on authorship embeddings.
- **TinyStyler** (Horvitz, Patel, Singh, Callison-Burch, McKeown, Yu; Findings of EMNLP 2024; arXiv:2406.15586, Jun 2024; model huggingface.co/tinystyler/tinystyler).
  - An 800M T5 (T5-v1.1-Large) reconstructs text from a Pegasus paraphrase (`tuner007/pegasus_paraphrase`, top-p 0.80, temperature 1.5) plus a projected 768-d Wegmann style embedding. Target-author embeddings are mean-pooled over any number of examples.
  - Trained unsupervised on ~88M Reddit Million User Dataset comments (≤60 tokens): LR 1e-5, batch 16 × grad-accum 4, 230k steps.
  - Self-distillation on filtered synthetic pairs: drop outputs identical to the input or with hallucinated links; keep MIS and SimCSE ≥ 0.7, Away < 0.9, Towards < 0.30; choose by geometric mean. ~40k pairs remain, so no paraphraser is needed at inference.
  - Evaluation uses held-out UAR/LUAR embeddings. Wegmann embeddings serve only training and reranking. 15 source × 15 target Reddit users, 16 samples each, 3,600 transformations per split.

  | System | Joint (Random / Single / Diverse) |
  |---|---|
  | STYLL-GPT-3 | 0.23 / 0.29 / 0.30 |
  | STYLL-BLOOM | 0.34 / 0.40 / 0.36 |
  | ParaGuide variants | 0.22–0.27 |
  | GPT-4 | 0.33 / 0.31 / 0.30 (Sim 0.68–0.72) |
  | GPT-3.5 | 0.35 / 0.41 / 0.37 |
  | TinyStyler, unsupervised | 0.32 / 0.37 / 0.28 (strong Away/Towards, Sim 0.31–0.44) |
  | TinyStyler, distilled | 0.40 / 0.45 / 0.36 |
  | TinyStyler + rerank(5) | 0.43 / 0.48 / 0.39 |

  - Towards was ≤ ~0.16 for every system (GPT-4 0.07–0.09; TinyStyler ~0.13–0.15). On the Random split GPT-4 kept meaning better (Sim 0.71 vs 0.59). On formality transfer GPT-4 still led (joint 0.85 vs 0.76–0.78). Speed: 0.47 s per example vs 1.56 s for GPT-4.
  - No human evaluation of authorship ("difficult for humans to evaluate"). The authors say it can "personalize generic outputs from chat models to match a user's preferences" and flag impersonation risk.
- **ParaGuide** (Horvitz, Patel, Callison-Burch, Yu, McKeown; arXiv:2308.15459, Aug 2023; AAAI 2024 venue [unverified]). Paraphrase-conditioned diffusion with gradient guidance from classifiers and style embedders; target style set at inference. Beat baselines on Enron email for formality, sentiment and authorship transfer.
- **ASTRAPOP** (Liu, Agarwal, May, "Authorship Style Transfer with Policy Optimization"; USC ISI; arXiv:2403.08043, Mar 2024, rev. Jul 2024).
  - Stage 1: SFT on pseudo-parallel neutral → original pairs, "following STRAP." Neutral inputs come from a LLaMA paraphraser fine-tuned on GPT-3.5-turbo paraphrases (SBERT 0.764 vs 0.738 for GPT-3.5-turbo itself). LLaMA-2-7B base, LoRA r=16, α=32, dropout 0.05, on q_proj/v_proj.
  - Stage 2: PPO / DPO / CPO directly on Towards/Away, with LUAR authorship similarity as reward.
  - Individual-author task: Reddit MUD, 2 training texts per author, 16 for evaluation, 5 exemplars at inference. SFT joint 0.484 vs STRAP 0.414 vs STYLL-GPT-3.5 0.370. Works "with as few as five examples per author."
  - Notes that Patel et al. found STRAP-style SFT does not beat ICL at this scale, and that one exemplar-conditioned model beats one model per author in the extreme low-resource case.
- **STAMP** (same authors; arXiv:2406.11581, Jun 2024). Multi-iteration preference optimization extension.
- **StyleMC** (Khan et al. 2023). Contrastively trained stylometric representations (LUAR-style, 1M Reddit users with ≥100 comments) plus an author-adapted LM and MCMC sequence-level inference. With a few hundred words of target text it beat GPT-4 prompted with demonstrations. Its zero-shot samples were harder to detect as machine text. Also proposed for anonymization.
- **STEER** (Hallinan et al.; arXiv:2311.07167, Nov 2023). Expert-guided synthetic pairs plus offline-then-online RL for arbitrary-source → target-style transfer. Beat 175B GPT-3 at 226× smaller.
- **StyleRemix** (Fisher et al.; arXiv:2408.15666, Aug 2024). Pre-trained LoRA modules per fine-grained style axis for authorship obfuscation. Released AuthorMix (30K texts, 14 authors).
- **GRPO with an authorship reward** (Liu, Bahja, Kovatchev, Lee, "Capturing Classic Authorial Style in Long-Form Story Generation with GRPO Fine-Tuning"; CoNLL 2026; arXiv:2512.05747, Dec 2025). An AV-supervised style judge is the GRPO reward for an 8B generator. Average style score 0.893 across Twain, Austen, Dickens and Hardy, above open-weight baselines. A search summary says the paper notes token-level style distances are topic-confounded and that "imitation" can come from copying names and settings [unverified].
- **Unslopper-30B-A3B** (N8Programs, early 2026). Qwen3-VL-30B-A3B-Instruct fine-tuned on ~1,000 `unslop-good` pairs (Project Gutenberg passage vs an AI-rewritten version) to "reverse the AI-ification process."
  - On 100 GPT-5.2 short stories: 30% AI / 45% mixed / 25% human, vs 99% AI for the untuned control. Quality dropped slightly.
  - The author warns of local coherence problems and advises use inside a larger pipeline. Commenters doubted ~1k examples was enough.
  - The main HF card returned HTTP 401. Data construction was verified only from the GGUF card and a Reddit snapshot (2026-01-15).
  - Smaller derivatives: a Qwen3-0.6B LoRA on the same data ("pilot project"); chartreuse-verte prose-rewriter 1.7B (fiction, not instruction-tuned).
- **InMyStyle** (Chakravorty, "Small Is Enough: Per-User Style Rewriting of AI-Edited Text via LoRA Adapters"; arXiv:2607.29238, Jul 2026). Rank-8, 3-epoch LoRAs on Qwen2.5 0.5B–7B rewrite AI-edited text toward one author, with no instruction prompt. 73 paragraphs of scientific writing, 219 eval pairs.
  - Composite score plateaued across sizes (Q 0.689–0.695). Authorship probability stayed at 0.51–0.53. "Stylometric improvement [was] near zero."
  - LLM judges rated outputs >20% lower in perceived AI-ness than the inputs. Gains favored "content-preserving naturalization more than recovery of personal style."

Data tiers [inference in notes]:
- **≥100k words:** per-author inverse paraphraser (STRAP).
- **5–16 samples (~500 words):** universal exemplar-conditioned rewriter (TinyStyler, ASTRAPOP, STYLL).
- **Hundreds of samples to whole oeuvres:** per-author fine-tuning (Sections 3.3 and 6).

Cautions:
- Low Towards scores make "beats GPT-4" a relative claim.
- Many systems use authorship embeddings for both guidance and evaluation, so metric gaming is live. TinyStyler mitigates this with a held-out evaluator.
- No study has people who know the target author judge TinyStyler or ASTRAPOP output.
- Results are on short Reddit text. Long emails and documents are untested.

---

## 5. Decoupling content from style

Direct precedent exists for "a frontier model supplies content, a personal model supplies voice."

**Evidence for**
- The authorship-transfer line is built on it (STRAP, TinyStyler, ParaGuide, ASTRAPOP). TinyStyler later distills away the paraphraser.
- The best human-judged fine-tunes learn content → prose. Chakrabarty: GPT-4o content description → author excerpt, with novel descriptions at inference. Panza: reverse instructions, where an LLM writes the instruction that would yield each real email.
- Small restylers beat frontier prompting on style; frontier models keep meaning better (TinyStyler Sim 0.71 vs 0.59).
- Practitioners converged on it in 2025–26:
  - Nic Lydon: a frontier model drafts and a 3B voice model rewrites. "Frontier LLMs are good at figuring out *what* to say. They're bad at saying it the way you would."
  - NicAI (2026-09-20, plan): a Qwen2.5-1.5B rewriter of frontier drafts, with 169 draft-and-sent email pairs as "the strongest supervision."
  - Writekin (2026-07-28): a Compose screen that drafts and rewrites in the user's voice.

**Risks**
- **Content-borne fingerprints.** Source-model idiosyncrasies survive LLM rewriting (Sun et al. 2025). Restyling the surface can leave the drafter's content choices in place.
- **Draft anchoring.** Post-edited text stayed closer to the LLM draft than to the author (g=−1.43). Participants corrected facts in ~31% of drafts. Generic drafts were the most cited reason to avoid an LLM-draft workflow; 58 of 81 still preferred post-editing to writing alone (Baumler et al. 2026).
- **Meaning drift and fact loss.** TinyStyler Sim 0.59; ASTRAPOP SBERT drop under PO; NicAI: "The rewriter washes out the facts."
- **Coherence.** Unslopper's local coherence breaks.
- **Naturalization without personalization.** InMyStyle's small LoRA removed AI-ness and recovered little personal style.
- **Plausible nonsense.** codebyandy: "The model will sound like you while saying plausible nonsense."
- **Complexity.** NicAI warns that two tiers add failure points and latency.

**Mitigations in the sources**
- TinyStyler's filter (drop hallucinated links; MIS and SimCSE ≥ 0.7) and best-of-5 reranking by geometric mean of style and similarity.
- CIPHER-style learning from the user's edits to final output (Gao et al. 2024).
- [inference in notes] Score each candidate for meaning (embedding similarity or bidirectional NLI vs the draft), entity/number/date/URL preservation (all present, none added) and style. Return the best, or fall back to the draft and flag it. Optionally ask the frontier model "does B say anything not in A?"
- [inference in notes] Train the rewriter on generic-LLM-draft inputs so training matches deployment. Rewrite long documents paragraph by paragraph at low temperature. Expose a style-strength knob through LoRA scale, embedding interpolation or draft/rewrite blending.

**Open questions**
- A sparse content description (Chakrabarty) may leave less AI residue than a full draft. Untested head-to-head [inference].
- No controlled study compares (a) frontier with style prompt and exemplars, (b) local fine-tuned model alone, and (c) frontier draft → local restyle on one person's corpus with human judges.

---

## 6. How much data

| Source | Setting | Data | Finding |
|---|---|---|---|
| DITTO (ICLR 2025; arXiv:2406.00888) | Online imitation, Mistral 7B | 7 demonstrations per author; 20 authors from CMCC and CCAT50 | +11 win-rate points over SFT, +20.2 over SPIN, +33.4 over few-shot; +18 vs few-shot GPT-4. 16-person email study: +12 over SFT, +23.9 over few-shot, +27.9 over user-written prompts. Demonstrations "an order of magnitude more sample-efficient" than pairwise preferences |
| ASTRAPOP (2024) | Shared SFT + PO rewriter | 2 training texts, 5 exemplars | Beats ICL and SFT alone |
| STYLL benchmark (2022) | Few-shot transfer | 16 posts, ~500 words | "Not yet mastery" |
| Panza (2024) | RoSA on Llama-3-8B-Instruct, 7 users | 25 to 100 emails; full data "several hundred or thousand" | 25 emails: BLEU ~90% of max, MAUVE ~0.85. BLEU saturates at ~75–100; "MAUVE scores take longer to saturate." "As few as 50-100 emails suffice to make a convincing imitation" |
| InMyStyle (2026) | Rank-8 LoRA, Qwen2.5 0.5–7B | 73 paragraphs | Near-zero stylometric gain |
| StyleTunedLM (INLG 2024) | Raw-text LoRA, Llama-2-7B base | 5% / 35% / 70% / 100% of ~80k tokens | Classifier accuracy 0.11 / 0.44 / 0.81 / 0.88; cosine 0.57 / 0.74 / 0.92 / 0.95; lexical MSE 6.04 / 3.49 / 1.44 / 1.39 |
| Eder (2010; 2013; 2015) | Classical attribution | Word counts | ~5,000–10,000 words for stable attribution; later work lowered the floor below 2,000 |
| Salemi & Zamani (2024) | Per-user LoRA on LaMP | Profile size | PEFT gains correlate positively with profile size |
| Chakrabarty (2025) | GPT-4o API fine-tune | Whole oeuvres (≥2 books) | "Near zero" slope of preference on corpus size in this range |
| Apple FM adapter toolkit (2025–26) | LoRA on Apple's ~3B model | n/r | Apple suggests 100–1,000 samples for basic tasks, 5,000+ for complex |
| Practitioners, small | Various | 20–200 examples | ~20: "Probably not" ready (Pandey). 50 on GPT-4o: "less AI flavor" (grapeot). 81: style captured (Griffiths). 114 (~91k tokens): views and style (Nottingham). 124 quotes: transfer "clearly happening" (Constantin). 200 tweets: tone matched; ~4,000 only "a little bit better" (Cselle) |
| Practitioners, large | Various | 15.8k–488k messages | All captured style. None fixed coherence, context or register |

Interpretation:
- **Tone** appears at ~50–200 clean examples.
- **Content metrics** saturate around ~100 email-length samples (perhaps 10–30k words [inference]).
- **Distributional style** (MAUVE, stylometric classifiers) keeps improving to ~50k–80k tokens. StyleTunedLM found 4k tokens (5%) and 28k (35%) inadequate and 56k–80k strong.
- **Below ~10 samples** plain SFT overfits ("problems that plague SFT in low-data regimes," DITTO). Objectives that contrast the user's text with the model's own outputs are the documented fix.
- **Adapter capacity** matters at low data. Rank 8 on 73 paragraphs failed (InMyStyle).
- **Beyond a few hundred examples**, practitioners report more gain from cleaning, filtering and register matching than from volume.

Caveats:
- StyleTunedLM's Gutenberg authors are likely in pretraining data; the authors say so and list low-resource users (they frame targets as having "1k-50k tokens of prior work") as untested.
- Chakrabarty's flat slope covers book-length corpora only.
- No scaling study exists across users, ranks and model sizes for single-author style. Panza's exact per-size points live in its Figure 5.

Weakly sourced rules of thumb:
- "Start with hundreds of paired examples, ideally 1,000+," LoRA rank ~16, 1–3 epochs (daehnhardt.com, 2025-10-16) [unverified].
- Fine-tuning "requires hundreds of your own examples" with modest gains over a well-prompted base (Reddit r/AI_Agents, ~2025-11).
- An Apple-silicon playbook suggests LoRA r=4 for style ("~0.1% of parameters"), r=8 for general use, 100–10,000 examples (mac-playbooks). Practitioners who reported rank found r=16 better than r=8 (Lopes; Lydon), contradicting it.

---

## 7. Building training data

### 7.1 Style inversion: neutral input → original text

The authorship-transfer recipe: neutralize each real unit (one email body, one doc section, one post), then train neutral → original (STRAP; TinyStyler; ASTRAPOP). The same idea underlies Gutenberg-DPO prompts and Unslopper. grapeot (2024-12-23) used a cross-lingual variant: an LLM's English translation of each Chinese blog paragraph as input, the original Chinese as target.

Input forms. No paper compares them for one person's style; the trade-offs below are reasoning in the notes.

| Input form | What it teaches | Risk |
|---|---|---|
| Neutral paraphrase | Surface style: lexicon, punctuation, rhythm; highest content alignment | Teaches "copy and lightly edit" |
| Bullet outline or content description (Chakrabarty) | Structure and expansion choices as well | The model invents connective content; more hallucination |
| Generic LLM draft of the same content | Matches deployment input for draft → restyle; de-AI-ification (Unslopper) | Learns the quirks of one drafter |

Notes' recommendations [inference]:
- Train on a mix of all three, tagged by input type, so the model handles whichever arrives.
- Use a neutralizer from a different model family than the deployment drafter, or several.
- Carry over TinyStyler's similarity/novelty filter and best-of-N reranking.

### 7.2 Synthetic task prompts: plausible request → real text

Reverse instructions turn unlabeled human text into SFT data.
- **Humpback / Instruction Backtranslation** (Li et al., Meta; arXiv:2308.06259, Aug 2023; ICLR 2024; published title "Self-Alignment with Instruction Backtranslation," from this reviewer's prior knowledge, not the notes). A seed model writes instructions for web documents (self-augmentation), then scores and keeps the best pairs (self-curation). Two iterations on LLaMa "outperform all other LLaMa-based models on the Alpaca leaderboard" without distillation data. Seed size and curation ablations not verified.
- **LongForm / Reverse Instructions** (Köksal, Schick, Korhonen, Schütze; arXiv:2304.08460, Apr 2023; Findings of EMNLP 2024; ICLR 2024 listing). LLM-written instructions for human C4/Wikipedia passages. LongForm-OPT-2.7B beat OPT-30B on long text generation; >35% over prior models across text-generation tasks. Human-written outputs beat noisy Self-Instruct data.
- **Instruction Back-and-Forth Translation** (Nguyen et al.; arXiv:2408.04614, Aug 2024; Findings of EMNLP 2024). After backtranslating instructions for Dolma documents, Llama-2-70B-chat rewrites each response into assistant style: +3.6% AlpacaEval over prior backtranslation data at equal volume. For personal style this rewrite step is the one to skip. It replaces the person's text with assistant prose.
- **Panza:** reverse instructions per real email.
- **StyleTunedLM eval prompts:** 50 GPT-4-generated prompts plus 50 built from the first 6–8 words of held-out sentences. A template for a held-out test set.

Practitioner prompt constructions:
- Prevost: "reverse prompting" with Llama 3.3 70B for ~6,200 posts (~18 min), since ~75% lacked inputs; a second LLM filter removed tautological or hallucinated pairs.
- Kevin Leary: a metadata template, `write a blog post in markdown for kevinleary.net entitled "{title} - {lead-in}" as if it were originally published on {date}`.
- Gabor Cselle: tweetnlp NER tags as the prompt (planned).
- Lydia Nottingham: 20 full-post completions ("Write a blog post about AI safety:"), 33 instructions, 61 Q&A. The mix "produced a more versatile model."
- Sarah Constantin: hand-written questions with target quotes as answers.
- Michael Daigler: instruction plus blank input → newsletter.
- OpenAI forum (2023-01): fixed "tweet in the style of [user]:" prompt, topic summaries, or GPT-written prompts per tweet ("could get expensive at scale").
- Didier Lopes: 91 posts → ~2,100 Q&A. Output length moved from 865 to 382 characters (references 406). Q&A conversion pulls toward answer length and knowledge more than essay voice [inference in notes].

The main failure is prompts that omit facts. The model then learns to invent them.
- codebyandy: "plausible nonsense."
- zwischenzugs (2025-11-04): Qwen2.5-3B-Instruct trained on his Gmail Sent folder wrote "Hey, how are you? I was thinking of going out for a drink..." signed with his name, and hallucinated a date. The base model wrote "Subject: Exciting Plans for Our Drink Date! Dear [Friend's Name]".

Notes' recommendations [inference]:
- Put recipient, purpose, key points, numbers and dates into every synthetic prompt. Include thread context for replies.
- Curate Humpback-style: an LLM judge scores whether the prompt plausibly elicits the text; drop low scorers, near-duplicates and boilerplate.
- Vary phrasing (terse and detailed, imperative and conversational). Generate 2–3 prompts per text as augmentation.
- Keep the response verbatim after cleaning.

### 7.3 Raw text vs instruction SFT, base vs instruct, masking, mixing

**StyleTunedLM** (Liu, Diddee, Ippolito, CMU; INLG 2024; ACL Anthology 2024.inlg-main.34; arXiv:2409.04574; published title "Customizing Large Language Model Generation Style using Parameter-Efficient Finetuning," from this reviewer's prior knowledge, not the notes) is the best-measured small-corpus recipe.
- Raw next-token LoRA on Llama-2-7B base; books in 256-token chunks; LR 5e-5; 3 epochs; batch 4 per GPU; max length 256; 2× A6000. Held-out perplexity −7.0% on average.
- Instruction following restored by merging the style LoRA with a LIMA-trained LoRA (A concatenated vertically, B horizontally). Style vs general ability, Woolf:LIMA ratio → cosine: 0:1 0.57; 0.8:1 0.59; 0.9:1 0.64; 1:1 0.70. Benchmark performance reportedly maintained.
- Named-entity loss masking: spaCy name tokens get label −100. For Wodehouse, copied names fell from 50% to 23% with cosine 1.0 → 0.98. Effectiveness depends on NER accuracy.

**Base vs instruct**
- Rathod (2024-08-18): an instruct model trained on free text gave one- or two-word replies; he switched to the base model ("I should be training the _base_ models instead").
- passo.uno: the base model "mostly autocompleted raw corpus text"; instruct fine-tunes kept the target register better.
- sciences44: instruct Mistral-Nemo-12B ignored the LoRA format 43% of the time because "its instruction tuning competes with the LoRA format push." The 2B did best. Validation loss misled.
- Larson (2026-03-13): with an instruct model, "raw text wastes training signal."
- Lopes (2025-09-02): early failures came from the wrong chat template and a missing system prompt.
- HF forum (Qwen3.5-4B-Base on novels): raw text on a base model is plain causal LM; no chat template needed.
- [inference in notes] Base + raw text suits pure voice continuation. Instruct + chat/completions data + `--mask-prompt` suits a callable "rewrite/draft in my voice" tool. No controlled comparison exists.

**Prompt-loss masking**
- Huerta-Enochian & Ko, "Instruction Fine-Tuning: Does Prompt Loss Matter?" (EMNLP 2024; arXiv:2401.13586). Prompt-loss weight matters for short completions (best PLW 0.01–0.5). For medium and long completions, masking "can be safely ignored."
- Shi et al., "Instruction Modelling" (NeurIPS 2024; arXiv:2405.14394). Loss on instruction tokens helps most with long instructions and short outputs or in low-data settings; best case >100% relative on AlpacaEval 1.0, attributed to less overfitting.
- Unsloth guide (2025–26): completions-only training gains "a few points," especially multi-turn (`train_on_responses_only`).
- mlx-lm `--mask-prompt`: loss on the completion only, for chat and completions formats; the last chat message is the completion.
- [inference in notes] For long emails and documents, masking barely matters. For short Slack replies with long thread context, mask the context or use a small PLW, so the model does not spend capacity on other people's messages.

**General-data mixing**
- Prevost: 500 French Alpaca rows. Larson: 161 OpenHermes rows. Daigler: Alpaca-cleaned first, then his newsletters.
- [inference in notes] Mix ~10–30% general instruction data and spot-check instruction following and MMLU before and after. No measured optimum exists.

### 7.4 Data hygiene

Email cleaning is the dominant data-quality risk.

**Tools**
- Use Sent mail only, exported via Google Takeout `.mbox` (note.com Mac guide; zwischenzugs).
- Talon (Mailgun) offers `quotations.extract_from_plain`, HTML quote removal and `extract_signature`. It sometimes keeps reply headers and quoted lines and is confused by signatures above quotes; it detects Outlook separators and From/Sent headers (AgentMail docs).
- email-reply-parser (Zapier port of GitHub's parser): plain text only, ~0.03 ms.
- Unquote's benchmark on 4,000 real reply pairs: Talon P 0.592 / R 0.455; email-reply-parser P 0.719 / R 0.367. Unquote is a competing tool. Rules that assume `>`-prefixed quotes fail often, especially outside English (Unquote; email-reply-extractor on PyPI).

**Pipeline from the notes [inference], in order**
1. Parse MIME; prefer text/plain, else HTML → text.
2. Drop auto-replies, calendar invites, newsletters and pure forwards ("---------- Forwarded message").
3. Strip quoted history: a tool, then regex for "On <date>, <name> wrote:", "From: ... Sent: ...", `>` lines and "-----Original Message-----".
4. Strip signatures and disclaimers; learn your own signature blocks by frequency.
5. Replace code blocks, stack traces, tables and pasted logs with a placeholder.
6. Drop texts under ~5 words or down-sample them heavily.
7. Near-dedup (MinHash/Jaccard).
8. Scrub PII (emails, phones, addresses, account numbers) to typed placeholders such as `<PERSON_1>` and `<EMAIL>`, which preserve sentence rhythm.
9. Keep other people's turns only as masked context.

**Practitioner evidence**
- Noise: tapbacks, images and links (Miller); a counting channel leaking numbers (Stroet); quoted replies and duplicates (Lydon).
- Short messages: Prevost removed messages under 6 words. Rathod: "I was literally conditioning it to give really short responses." furiousteabag: "ok" and "busy" dominated. A Mistral-7B Telegram persona replied in single characters and emoji until short messages were filtered [unverified].
- AI-written text: NicAI found 99 of 1,185 notes AI-written: "Train on those and the voice model learns to imitate an imitation." Heralax's role-swapped ChatGPT export made the model "slightly stilted" [unverified].
- PII: WeClone filters with Microsoft Presidio ("100% detection is not guaranteed"). muttled's scripted name and address swaps made the model hallucinate fake personal details. Presidio and dedup tooling were not separately researched.
- Register: Lazerowitz found work chat may not represent general style. Lydon suggests oversampling formal writing.

**Register and recipient conditioning**
- codebyandy: system prompt "You are Andy. You are messaging {contact} in {channel}," last 6 turns as context, reply as target; same tag at inference.
- Lydon: source labels to route between email, chat and post voices. Leary: the date in the prompt.
- Wang et al.'s genre gap (email ~96% vs blog ~20% AV) supports tagging registers.
- [inference in notes] Tags such as `register={email_formal, email_casual, slack, doc, post}` and `recipient_type={manager, peer, external, friend}`. One tagged adapter shares data across a small corpus; per-register adapters suit one dominant register. Up-sample minority registers. Reuse the tags as retrieval filters. Consider down-weighting old writing as style drifts.
- Split evaluation data by entity, not row (NicAI).

### 7.5 Hyperparameters for small-data style LoRA

Consensus across LoRA Without Regret, the Unsloth guide and practitioners:
- **Modules:** all linear layers (q/k/v/o/gate/up/down). Lydon: q/k/v only gave "right structure but the wrong vocabulary."
- **Rank:** 16–32; α = r to 2r; dropout 0 (up to 0.1 if overfitting). Rank 8 underfit for Lopes, Lydon and InMyStyle.
- **LR:** ~1e-4 to 2e-4 for SFT LoRA; ~5e-6 for DPO/GRPO-type stages (Unsloth).
- **Epochs:** 1–3; "beyond 3 ... overfitting risk." Training loss below ~0.2 signals memorization. Fixes: lower LR or epochs, more decay or dropout, early stopping on eval loss, or halving α at inference.
- **Batch:** effective 8–16 (e.g. 2 × accum 8); weight decay 0.01–0.1; warmup 5–10%; linear or cosine schedule.
- **Chunks:** 256–1024 tokens on paragraph or section boundaries, keeping the title or header as context; one email per example.

Published configurations:
- StyleTunedLM: LR 5e-5, 3 epochs, 256-token chunks, Llama-2-7B.
- ASTRAPOP: r=16, α=32, dropout 0.05, q/v only.
- codebyandy (mlx-lm): Qwen3-4B-8bit, r16, LR 1e-4, 1,000 iters, max_seq_length 1024, batch 4 "safe for 16 GB," ~1–2 h on an M1.
- Griffiths: Unsloth r16/α32, 60 steps, LR 1e-4. Lydon: r16/α32 on all 7 projections, 3 epochs. Prevost: r32, 2 epochs.
- mlx-lm defaults sit below the consensus: rank 8, scale 20, top 16 layers, LR 1e-5. MLX counts iterations, not epochs (mac-playbooks).

Loss is a poor guide. Donner's quality kept rising while loss rose. NicAI: "Lower training loss can mean memorisation. Judge on held-out data only." Larson's loss of 0.09 at 97% token accuracy on six articles indicated memorization.

Decoding belongs to the recipe. Donner fixed early surreal, repetitive output through prompt, format and decoding changes. Lazerowitz fixed erratic output at temperature 1.0 by lowering temperature and raising frequency penalty. Miller used beam search and temperature 0.75.

---

## 8. Preference optimization

The standard construction: chosen = human original; rejected = an LLM's text for the same prompt.

**Community creative-writing practice**
- **Gutenberg-DPO v0.1** (jondurbin, 2024; cc-by-4.0). Books split into chapters with `chapterize`. An LLM wrote a prompt and summary per chapter; later prompts include the previous chapter's summary, so each target is reachable from its prompt. Rejected chapters from llama-2-13b-chat, bagel-7b and dolphin-2.2-34b. 918 rows, 16 books; HF lists 462 models using it.
- **nbeerbower derivatives:** gutenberg2-dpo and gutenberg-moderne-dpo (rejected from Mahou-1.5-mistral-nemo). Models mostly ORPO: mistral-nemo-gutenberg3-12B ("ORPO tuned with 8x A100 for 2 epochs"), Qwen2.5-Gutenberg-Doppel-14B ("ORPO tuned with 4x A40 for 3 epochs"). No before/after EQ-Bench numbers published.
- **Quill-v1** (sam-paech, 2024; gemma-2-9b-it). ORPO "gently," then SimPO "less gently," on Gutenberg3 (629 public-domain novels). Rejected = gemma-2-9b-it's own generation from a description of the passage, to "steer the model away from its default style." EQ-Bench creative writing 79.75; no base comparison.
- **gemma-2-Ifable-9B** (ifable). SimPO on gutenberg-dpo-v0.1 plus a proprietary set; #1 on EQ-Bench Creative Writing on 2024-09-10 [self-reported].

**Controlled evidence for individual authors.** ASTRAPOP (LLaMA-2-7B LoRA, LUAR reward):

| Method | Toward | Away | SBERT | Joint |
|---|---|---|---|---|
| SFT | 0.137 | 0.707 | 0.754 | 0.484 |
| +PPO | 0.147 | 0.773 | 0.729 | 0.495 |
| +DPO | 0.164 | 0.748 | 0.733 | 0.507 |
| +CPO | 0.165 | 0.752 | 0.726 | 0.505 |

- DPO ≈ CPO, both above PPO.
- Meaning fell because "our reward function does not take semantic similarity into account."
- ASTRAPOP-CPO uniquely reproduced idiosyncrasies: the typo "alot," all-lowercase text, a space before commas.

**Online imitation.** DITTO uses demonstrations with comparisons against the model's own outputs, replay and inter-checkpoint comparisons, designed to counter low-data SFT overfitting. It beat SFT by 11 points at 7 demos (Section 6).

**Over-optimization risk.** Antislop (Paech, Roush, Goldfeder, Shwartz-Ziv; arXiv:2510.15061, Oct 2025; ICLR 2026 poster), gemma-3-12b, identical preference pairs for banned-pattern suppression:

| Method | Writing quality | Lexical diversity | MMLU |
|---|---|---|---|
| Baseline | 67.80 | 100 | 0.590 |
| DPO 2k | 62.98 | 91.03 | 0.541 |
| DPO 8k | 54.61 | 73.92 | 0.571 |
| FTPO 2k | 68.93 | 101.05 | 0.559 |
| FTPO 8k | 67.49 | 95.09 | 0.592 |

DPO "logits diverge unconstrained as training continues." FTPO (Final Token Preference Optimization: token-level preference with MSE tethers to reference logits) suppressed up to 92% of patterns with minimal quality loss (secondary sources: 85–92%).

**Other**
- **COPE**, "Personalized LLM Decoding via Contrasting Personal Preference": DPO with synthetic generic negatives chosen by distance from the user's historical style, plus contrastive decoding [unverified; secondary summary only].
- **GRPO with an AV-trained judge as reward** (Liu et al., CoNLL 2026) is the RL variant (Section 4).
- **Algorithms** (not re-fetched): ORPO (arXiv:2403.07691) is reference-free and folds an odds-ratio penalty into SFT. SimPO (arXiv:2405.14734) is reference-free with a length-normalized reward. KTO (arXiv:2402.01306) uses unpaired good/bad labels.
- **LR:** ~5e-6 for DPO/GRPO-type methods (Unsloth). The notes suggest 5e-7 to 5e-6 for ~1 epoch [inference].

**Synthesis [inference in notes]**
- Sequence: SFT first; then pairs from a held-out slice with prompt = synthetic instruction or neutral input, chosen = real text, rejected = the SFT model's output, the base instruct model's output, or a frontier model's output.
- Self-generated rejects (Quill) are the most targeted, since they penalize what this model still does wrong.
- Chosen and rejected share content, so the signal is mostly stylistic. Rejects that omit facts reward content drift; add a semantic-similarity floor between chosen and rejected.
- Expect a modest gain: ASTRAPOP saw ~+5% relative joint and ~+20% relative Toward.
- Memory: DPO needs a reference policy (the adapter-disabled base with LoRA) and extra forward passes on two sequences per example. ORPO and SimPO are reference-free and lighter. Paired sequences double activation memory; cap length (e.g. 1024) and use batch 1 with accumulation. At 14B, PO is likely feasible only with QLoRA.

Gaps: no paper runs DPO or ORPO with one real person's emails or documents as chosen and measures the result. ASTRAPOP (Reddit authors, LUAR reward) is the closest. No controlled before/after numbers exist for the Gutenberg ORPO models.

---

## 9. Inference-time complements

- **Retrieval of the user's own writing.** OPPU: PEFT plus retrieval beats either alone. Wang et al.: topic-matched exemplars hurt attribution, sharply on Blog and Enron, plausibly by inviting content copying. The notes recommend retrieving style exemplars by register, recipient type and length, and keeping topic retrieval for facts, separate from style exemplars [inference].
- **Retrieval inside a fine-tuned model.** Panza: adding RAG at inference to a fine-tuned model lowered BLEU, likely from "re-using the RAG context too aggressively... emails that are very similar to past emails." Training with retrieval in the loop (RAFT) mitigated it.
- **Phrase banning.** Antislop sampler (sam-paech; code github.com/sam-paech/auto-antislop, MIT):
  - Finds over-represented patterns by frequency ratio against human baselines (wordfreq; Reddit creative writing and Gutenberg n-grams), e.g. "elara" at 85,513×.
  - On a banned match it backtracks to the pattern's first token, multiplies its probability by 10^(−10s) and resamples. Handles 8,000 patterns; plain token banning "becomes unusable at just 2,000." Regex bans fully suppressed "It's not X, it's Y."
  - Throughput falls 69% at 1,000 patterns and up to 96% at 8,000 (worst case), so the authors prefer FTPO for production.
  - [inference in notes] Build a personal list by comparing n-gram frequencies of model output against the user's own corpus. Keep it to a few hundred patterns on a laptop; use llama.cpp logit bias for single tokens.
- **Learning from edits.** PRELUDE/CIPHER (Gao et al., Microsoft, "Aligning LLM Agents by Learning Latent Preference from User Edits"; NeurIPS 2024; arXiv:2404.15269). Learns a textual preference description from the user's edits to agent drafts and retrieves preferences from the k closest past contexts. Lowest edit-distance cost in simulated email-writing and summarization tasks, with no fine-tuning.
- **Strength control.** llama.cpp per-request LoRA scale; TinyStyler embedding interpolation; PsPLUG's tunable residual; halving α at inference to reduce overfit style (Unsloth).
- **Activation steering** on a Mac requires hooking MLX or PyTorch layers. No evidence shows it beating a LoRA for a single person's idiolect.

---

## 10. Failure modes

| Failure | Evidence | Mitigation in the sources |
|---|---|---|
| Topic leakage into models and metrics | AV-trained style representations encode content (Wegmann et al. 2022); triplet training risks "content leakage" (StyleDistance); zero-shot AA above chance from topic (Wang 2025); copied names and settings count as "style" (Liu et al. 2026 [unverified]) | Content-independent embeddings; held-out-topic evaluation; entity loss masking |
| Verbatim regurgitation | Rare; Chakrabarty resampled such cases and reports low word overlap (Fig. 19). Donner searched and found none | Overlap checks; resampling |
| Content omission | Chakrabarty's SFT model sometimes skipped requested details | Fact checks; resampling |
| Copying from retrieved context | Panza: RAG over a fine-tuned model lowered BLEU | Retrieval in training (RAFT) |
| SFT overfitting on tiny data | DITTO; Larson (loss 0.09) | Preference objectives; fewer epochs; early stopping |
| Hyperparameter fragility | Panza: "highly sensitive to learning rate and the number of training epochs" | LR and epoch sweeps |
| Personalization collapse | Explicit style instructions override learned style (PsPLUG) | Tunable user residual |
| Short or generic output | Rathod; furiousteabag; Telegram persona [unverified] | Length filters; merge message bursts |
| Repetition loops | Donner (endless rescheduling); Rathod ("i love rust"); Stroet (echoes) | Decoding penalties; FTPO (repairs repetition loops, in mlx-lm-lora) |
| Caricature and tics | Miller ("optimized for outrageous behavior"); Constantin (bot "will spontaneously argue with and belittle the user"); NicAI (markers "become tics after too many epochs on few examples"); Lazerowitz (brusque tone) | Lower LR; fewer epochs; rank 16; decoding controls |
| Confident fabrication | Jeff Wang (invented prices); Larson ("hallucinated code. Confidently."); codebyandy; muttled (astronaut mother); NicAI (facts washed out) | Facts in prompts; entity checks; frontier content stage |
| Capability loss | Lazerowitz's model was worse at other tasks; Panza kept >98% | LoRA; general-data mix; adapter merging |
| Register mismatch | Lazerowitz; Lydon (weak long-form) | Register tags; oversample minority registers |
| Training on AI text | NicAI; Heralax [unverified] | Exclude AI-written and AI-assisted text |
| Misleading loss | Donner; NicAI; sciences44 | Blind held-out evaluation |
| PII and consent | mlx-whatsapp warns fused models leak chat data; Prevost calls scrubbing "absolutely critical" for release; Donner removed a deceased friend's data as "extremely poor taste"; HN consent concerns; codebyandy: train locally, never publish adapters | Local training; placeholders; private adapters |
| Model too small | opt-125m nonsense (Stroet); R1-distill 1.5B gibberish (BitsOfChris) | ≥3B models |
| Memory limits | Qwen 3.5 9B ran inference but OOM in training (Lydon); Mistral Small 24B OOM on save (Prevost) | QLoRA; shorter sequences |
| Detectability | 97% of in-context imitations detected (Chakrabarty); perplexity gap (Jemama & Kumar); idiosyncrasies survive rewriting (Sun) | Fine-tuning removed detector-driving quirks (Chakrabarty) |

Gaps: no paper measures "mode collapse to signature phrases." No IFEval-style study of instruction following after per-user style tuning of frontier-scale models.

---

## 11. Evaluating style fidelity

### 11.1 Style embeddings

| Model | Size | STEL / STEL-or-Content | PAN 2011–15 AV ROC-AUC | Notes |
|---|---|---|---|---|
| LUAR-MUD (Rivera-Soto et al., "Learning Universal Authorship Representations," EMNLP 2021) | 82.5M, 512-d, F32, Apache-2.0 | 0.86 / 0.03 | n/r | Input is an "episode" of several texts; `trust_remote_code=True`; trained on Reddit MUD; strongest authorship ID; topic-leaky at sentence level |
| LUAR-MUD-MV-Qwen | n/r | n/r | n/r | Multi-vector successor; MUD test MRR 0.6564 vs 0.5706 for LUAR-MUD (0.6283 single-vector mode) |
| Wegmann Style-Embedding / CISR (Wegmann, Schraagen, Nguyen, RepL4NLP 2022; arXiv:2204.04907) | RoBERTa-base, 768-d | 0.77 / 0.22 | 0.56 (0.65 / 0.39 / 0.57 / 0.63) | Conversation-controlled training beats domain or no control |
| StyleDistance (Patel, Zhu, Qiu, Horvitz, Apidianaki, McKeown, Callison-Burch; NAACL 2025; arXiv:2410.12757) | ~0.1B, BF16, MIT | 0.87 / 0.29 | 0.64 (0.62 / 0.68 / 0.58 / 0.67); LISA 0.57 | Trained on SynthSTEL plus real Reddit authorship data; sentence-level |
| mStyleDistance (Qiu, Zhu, Patel, Apidianaki, Callison-Burch; arXiv:2502.15168) | not confirmed | n/r | n/r | Multilingual, ~40 features across 9 non-English languages; reported to beat existing models on multilingual style benchmarks |
| roberta-base (reference) | 125M | 0.90 / 0.05 | n/r | High STEL alone is content-confounded |

Details:
- **LUAR family.** LUAR-CRUD: Pushshift Reddit 2015–2019, ~5M users with ≥100 comments. LUSR: a style representation trained without authorship labels, aimed at machine-text detection. A sentence-transformers port exists (gabrielloiseau/LUAR-MUD-sentence-transformers). Code: github.com/llnl/luar (Apache-2.0).
- **Wegmann.** Code github.com/nlpsoc/style-embeddings. Evaluated with the STEL framework (Wegmann & Nguyen, EMNLP 2021).
- **StyleDistance.** SynthSTEL covers 40 features in 7 categories, 100 positive/negative pairs per feature, generated by GPT-4 through DataDreamer; ~320K triplets sampled. Human validation: 92% match, Krippendorff's α 0.55; content similarity of parallel examples 0.88. Style-transfer-evaluation accuracy: StyleDistance 0.46, Wegmann 0.39, LUAR 0.38, humans 0.37. The synthetic-only variant keeps 65% of performance out of domain and 50% out of distribution. Limitations: 40 features, LLM biases, sentence level, some feature/content overlap.
- **Jangra et al., "Evaluating Style-Personalized Text Generation: Challenges and Directions"** (EMNLP 2026 main; arXiv:2508.06374v4). 8 datasets (Amazon reviews, ArXiv, blogs, Enron, lyrics, Reddit, Reuters, short stories), 636 instances, ~500 reference tokens; pairwise "which is closer in style." Settings: domain discrimination (DD), authorship attribution (AA), personalized vs non-personalized LLM output (LLM).

  | Metric | DD | AA | LLM | Mean |
  |---|---|---|---|---|
  | Wegmann | 0.910 | 0.670 | 0.558 | 0.713 |
  | StyleDistance | 0.926 | 0.665 | 0.575 | 0.722 |
  | BLEU | 0.869 | 0.700 | 0.631 | 0.733 |

  Embeddings degraded most from DD to LLM (−38.3%), against −26.7% for n-gram metrics and −11.3% for LLM judges. LUAR untested. The authors warn n-gram metrics may be inflated by contamination.
- **Baumler et al. (2026)** chose LUAR cosine because it "performed best on authorship identification using their control texts." Self-ratings correlated with LUAR at r ≈ 0.24.

Use [inference in notes]:
- Score against the centroid of the user's held-out texts in StyleDistance or Wegmann space (content-robust), plus LUAR on multi-text episodes (strong signal, topic-leaky). Report both; distrust LUAR gains when topics overlap.
- First check that the embedding ranks the user's held-out texts above other authors' texts on the same topic.
- For paragraphs or documents, embed per sentence or paragraph and average, or use LUAR episodes.
- All three are ~0.1B (~0.3–0.5 GB fp32 [estimate]) and run on CPU or `device="mps"`. LUAR's custom code on MPS is untested.

### 11.2 Authorship verification as the metric

- **Wang et al. (2025).** AA: fine-tuned Longformer-base-4096 and ModernBERT-base (20 epochs, lr 2e-5), top-5 accuracy averaged over both. AV: same backbones on label-balanced pairs (4:6 positive:negative, 10 epochs), top-1 accuracy. Style matching: per-author LIWC-22 + WritePrints model, correct if Mahalanobis distance is closer to the true author. Generation: 5-shot plus a GPT-4.1 summary of the target, temperature 0. Semantic similarity: METEOR, ROUGE-L, SBERT. No AV decision thresholds reported.
- **TinyStyler.** Away and Towards computed with held-out UAR/LUAR embeddings, distinct from the training and reranking embeddings. Meaning by Mutual Implication Score. Joint scores reported.
- **Training-free verifier.** Jemama & Kumar (2025): cosine distance over TF-IDF character 3–5-grams (top 10k) plus all-MiniLM-L6-v2 embeddings. 97.49% accuracy (ROC-AUC 0.997) same-domain; 94.48% (AUC 0.981) cross-domain on student essays. Imitation pass rates: zero-shot with a style profile ~3–7%, one-shot 68–95%, few-shot 91–100%, completion 97–100%. Code: github.com/rajeshjnu2006/writing-style-uemcon2025.
- **Local protocol [inference in notes].** Collect user texts plus a same-genre impostor pool (public Reddit, blog or email corpora). Hold out 20%. Calibrate a verifier: a cosine threshold on StyleDistance or LUAR, char-n-gram TF-IDF, or a fine-tuned ModernBERT-base (small enough for MPS). Report the accept rate on generations next to the rate on held-out real texts (ceiling) and impostors (floor), per genre.

### 11.3 Classical stylometry

- **faststylometry** (Fast Data Science; PyPI `faststylometry`). Burrows' Delta on function-word frequencies. `calibrate(train_corpus)` estimates authorship probability from known same/different-author Deltas; `corpus.split(1000)` handles unequal lengths. The tutorial notes its two-class demo is easy because the model "has learnt from entire books." No published minimum length.
- **Sample size.** Eder, "Does Size Matter? Authorship Attribution, Small Samples, Big Problem" (DH 2010; Literary and Linguistic Computing 2013, doi:10.1093/llc/fqt066): samples under ~5,000 words gave "poor guessing." Eder's later "Short Samples in Authorship Attribution" lowered the floor below 2,000 words; his methodology page says the earlier findings were "(partially) falsified." A Cosine Delta study on Estonian fiction found stable accuracy only at ≥5,000 words. StyleTunedLM cites Eder (2015) for 5,000–10,000 words.
- **stylo** (R; Eder, Rybicki, Kestemont) is the reference implementation for Delta variants, clustering and bootstrap consensus trees. Not fetched. The original Writeprints paper (Abbasi & Chen 2008) was not fetched.
- **slop-score** also computes n-gram repetition, MATTR-500, Flesch-Kincaid grade and dialogue frequency.
- **n-gram overlap.** In Jangra et al., BLEU beat both style embeddings on mean accuracy (0.733) and on the LLM setting (0.631).

Use [inference in notes]:
- A per-feature z-score diff of outputs against the user corpus: top 100–300 function words; sentence length mean and SD; punctuation per 1k characters (em-dash, semicolon, colon, parentheses, exclamation, ellipsis); contraction rate; paragraph length; MATTR; readability; emoji and capitalization. Each output gets an explainable diff ("3× fewer semicolons").
- Pool generations to 2,000+ words per condition before computing Delta to the user and to impostors.
- No study validates a composite classical score against human judgments of personal style.

### 11.4 LLM-as-judge

Jangra et al. (2026), pairwise "closer in style" judging. Random baseline 0.500.

| Judge | Mean accuracy | DD / AA / LLM |
|---|---|---|
| gpt-4.1 | 0.815 | 0.961 / 0.807 / 0.678 |
| o4-mini | 0.755 | n/r |
| DeepSeek-V3 | 0.658 | n/r |
| Qwen3-32B | 0.607 | n/r |
| Mistral-24B | 0.467 | n/r |
| Ministral-3B | 0.324 | n/r |
| Llama-3.1-8B | 0.279 | n/r |

- Small models often answered "Both" or "None."
- Prompt sensitivity (Llama-3.1-8B): a structured-output prompt was ~24% worse; a binary-choice prompt ~34.5% better. Automatic prompt optimization was inconsistent and possibly overfit.
- Ensembles: all evaluators with performance-weighted voting reached 0.821, using oracle-style weights and not significantly above gpt-4.1. The best non-LLM ensemble (BLEU, ROUGE, METEOR, Wegmann, StyleDistance) reached 0.780, +6.4% relative over BLEU.
- Human agreement ratios: content 0.779, style 0.641, copy-editing 0.400. Style preferences are subjective.

Other evidence:
- Expert MFA writers reached κ 0.54–0.58 on stylistic fidelity; lay Prolific judges 0.07–0.22 (arXiv:2601.18353).
- Four of five LLM judges preferred markdown well above the human baseline (arXiv:2604.23178, 2026).
- A search snippet claimed a fixed style-embedding baseline beat a GPT-4o judge on GPT continuations (82% vs 68%) and lost on LLaMA continuations (85% vs 81%, not significant). The paper could not be identified [unverified].

Use [inference in notes]:
- Pairwise, forced binary choice, both orders; count only consistent wins.
- Absolute 1–10 "sounds like me" scores are unvalidated.
- A 4-bit Qwen3-32B-class judge (~18–20 GB [estimate]) is borderline and slow on 24 GB; 8B-class judges scored below chance. A frontier judge is more defensible if privacy allows. Calibrate any local judge on known pairs (user's real text vs another author, same topic).
- LLM judges may prefer polished LLM-ish text over the user's real idiosyncrasies. Untested for personal style.

### 11.5 Slop and AI detection as negative signals

These are regression checks, separate from fidelity. Imitations can pass a verifier and still be flagged as AI.

- **slop-score** (sam-paech, MIT). Matches text against word and trigram lists over-represented in LLM output relative to a wordfreq human baseline. Adds a contrastive-negation detector for the "not X, but Y" pattern: 10 surface regexes plus 35 POS-tagged patterns via wink-pos-tagger. Composite weights: slop words 60%, contrastive pattern 25%, trigrams 15%. Lists in the repo's `data/` folder. Runs in the browser (`python -m http.server`) or at eqbench.com/slop-score.html; custom human baselines via `--force-recalc-human`. No documented validation against human judgments or score normalization. A Go port (SlopScoreTool) states it is "not an AI-authorship detector and not a measure of writing quality" and may cover technical text less well.
- **EQ-Bench Creative Writing** shows a Slop column and a "GPT-Slop Control" slider.
- **Antislop** measured some patterns at >1,000× their human frequency.
- **Binoculars** (Hans et al.; arXiv:2401.12070, Jan 2024; github.com/ahans30/Binoculars, BSD-3). Ratio of perplexity to cross-perplexity between two LLMs; "detects over 90% of generated samples from ChatGPT (and other LLMs) at a false positive rate of 0.01%," with no training data. Default pair Falcon-7B + Falcon-7B-Instruct with a fixed global threshold; stronger in English; not to be used without human supervision. Sources disagree on which Falcon model is observer vs performer (HF blog vs Weaviate summary). Two 7B models in bf16 ≈ 28 GB [estimate], over budget; quantizing shifts the calibrated threshold.
- **Fast-DetectGPT** (Bao et al.; arXiv:2310.05130, Oct 2023). Local demo defaults to gpt-neo-2.7B; `--sampling_model_name gpt-j-6B` is more accurate. Average AUROC ~0.9887 white-box vs 0.9554 for DetectGPT [unverified; secondary summary]. ~5–11 GB [estimate].
- **Perplexity gap.** Human essays ~29.5 vs ~15–16 for imitations (GPT-2 scorer). At threshold 20, ~90% of AI texts fall below vs ~15% of human texts, even for imitations that passed the verifier (Jemama & Kumar).
- **GPTZero** rated GPT-4o 5-shot imitations "human" 0.08–0.67% outside email (Wang). **Pangram** was used with LUAR in the UMD post-editing study; residual LLM style remained after editing.
- GPTZero and Pangram are API-only [inference; local availability not checked].

Use [inference in notes]:
- Calibrate any detector threshold on the user's own writing; some people score AI-like. The false-positive rate on the user's corpus is the number that matters.
- Count slop-list hits and the contrastive pattern per 1k words, compared with the user's own baseline rate, and track it across model versions.
- Smaller same-family detector pairs (1.5B–3B base/instruct) or Fast-DetectGPT with gpt-neo-2.7B fit in memory; both need recalibration.

### 11.6 Meaning preservation

- **Mutual Implication Score** (Babakov et al., ACL 2022 SRW; `s-nlp/Mutual_Implication_Score`, also under `SkolkovoInstitute/`). Symmetric score from a RoBERTa-large NLI model fine-tuned on QQP paraphrases. Beats other measures on paraphrase detection and matches the best for style transfer. ~355M params, ~1.4 GB fp32 [estimate]. License CC BY-NC-SA 4.0 per a third-party listing (PromptLayer); verify on the card.
- **TinyStyler** uses MIS for meaning, reranks by the geometric mean of Away, Towards and Sim, and computes formality joint as the geometric mean of accuracy, Sim and CoLA-classifier fluency.
- **Wang et al.** report METEOR ~0.30–0.32, ROUGE-L ~0.23–0.26 and SBERT ~0.75–0.78 between imitation and target (SBERT variant unspecified).
- A bidirectional-NLI content score correlated among the highest with human judgments in formality transfer (arXiv:2308.09055).

Use [inference in notes]:
- Content = MIS(brief or draft, output), or SBERT cosine (`all-MiniLM-L6-v2` or `all-mpnet-base-v2`). Style = similarity to the user centroid minus similarity to a generic-LLM centroid. Report a geometric mean so collapse on either axis tanks the score.
- For open-ended tasks with no source text, check task adherence: every required fact entailed by the output. No validated metric exists for this.

### 11.7 Human blind tests

- No study measures whether people can pick their own writing out of a pair with an imitation.
- **Self-judgment is weak.** Baumler et al.: participants rated post-edited text as representative of their style as their own writing; self-ratings correlated with LUAR at r ≈ 0.24. The LMU "AI ghostwriter effect" study (ACM TOCHI): some participants put their name on pseudo-personalized LLM text they neither wrote nor felt they owned.
- **Familiar and expert readers discriminate better.** Panza acquaintances ~64% vs 25% chance. Experts κ 0.54–0.58 vs lay 0.07–0.22. Against in-context imitations, experts picked the human text as more faithful 72.0% of the time, lay readers 52.7%. On quality, experts preferred human text over in-context AI 82.7% and preferred fine-tuned AI 62.2% (arXiv:2601.18353).
- **Protocol in arXiv:2601.18353.** Blind pairwise; for fidelity, judges see the original author's excerpt next to a human and an AI imitation; 3 experts and 5 lay judges per pair (majority vote) with 2–5-sentence rationales.
- **Practitioner precedents.** Prevost's 10-pair blind survey (66% recognition; 50% = indistinguishable). Lydon's 12-prompt blind A/B against the base. NicAI's planned frozen 30-pair blind test against "Claude with SOUL.md." codebyandy's planned blind quiz with a 20-example frontier baseline. Every Spiral's LLM-judge blind lineup on every draft [vendor claim: 87% indistinguishable].

Suggested self-blind 2AFC protocol [inference in notes; unvalidated]:
1. Generate from a brief derived from one of your held-out real texts (same brief, same length).
2. Strip formatting cues; normalize length, quotes and whitespace.
3. Present in random order: "which did you write?" Delay the test by days so content memory does not decide.
4. Run 20+ trials and report the "fooled" rate. At n=20, a one-sided binomial test needs ≤6 correct for "fails to detect" and ≥15 for "reliably detects."
5. Record a one-line reason per trial. Feed the reasons into the tic list for the stylometry and slop checks.
6. Add a familiar-reader arm (partner, colleague, editor) and a 3-way variant (real reference plus two candidates) that mirrors the automated pairwise evaluators.

### 11.8 Evaluator hygiene

- Keep the evaluation embedding distinct from any embedding used in training, reranking or best-of-N (TinyStyler). STRAP warned that style-transfer metrics are easy to game.
- Hold out topics and entities (Wegmann; StyleDistance; NicAI).
- Report per register (Wang's genre gap).
- Validate automatic metrics against blind human results on the user's own data (Baumler; Jangra).
- Compare against a well-prompted frontier model (NicAI).
- Suggested dashboard per model version [inference in notes]: StyleDistance and LUAR similarity against the user centroid and an impostor baseline; AV accept rate; classical-feature z-score diff; slop rate relative to the user's baseline; detector score calibrated on the user's text; MIS or SBERT content score; periodic blind 2AFC "fooled" rate as ground truth.

---

## 12. Practitioner case studies

About 30 verifiable projects from 2023 to 2026. Most are hobbyist LoRA/QLoRA runs on 3B–13B open models (a few at 65–70B) or OpenAI fine-tuning API runs. Evaluation is mostly informal. "MLX" marks Apple-silicon training.

| Project (date) | Data | Model and method | Hardware, cost | Evaluation | Reported outcome |
|---|---|---|---|---|---|
| Izzy Miller, "Replacing my best friends with an LLM trained on 500,000 group chat messages" (2023-04-10) | ~488k iMessage group-chat messages, 6 people, ~7 years, from `chat.db`; 4-hour session gaps; Alpaca format | LLaMA 7B full fine-tune (Stanford Alpaca code, FSDP `full_shard`), 3 epochs, LR 2e-5 | 4× A100 on vast.ai, "a few hours," ~$100 credits; served on Modal A10G | Heavy use with friends | "It really, really nailed the voice and perspectives of my friends." Over-used tapbacks; "optimized for outrageous behavior" |
| Jeff Wang, "Automating Your Newsletters" (2023-04-19) | ~40 crypto newsletters, 2 MB raw text | LLaMA 7B LoRA, Oobabooga | n/r | Informal | "Already sounds like me"; reproduced format; invented prices; off-topic drift; "you cannot automate a financial newsletter based on previous data" |
| Duarte O. Carmo (2023-05-24) | 20k Telegram messages; ≤10 prior messages as context; 120-minute gaps | flan-t5-small | A100, ~20 min | None | Short Portuguese replies; learning exercise |
| muttled, Show HN "I trained a 65B LLM on my texts to talk to myself" (2023-07-21) | ~30k own texts, 2 years; scripted swaps of real names and addresses | LLaMA-1 65B LoRA r128, 5 epochs, batch 1, 256-token cutoff, bitsandbytes 4-bit (Oobabooga) | 2× RTX 3090, ~16 h | Informal | Most coherent at loss ~1.5; hallucinated fake personal details; "talk[s] as if it's already friends with the user" |
| Ross Lazerowitz (2023-09-04) | 140k Slack messages at Observe Inc., 4 years, 10.4M tokens; preceding messages → his reply | GPT-3.5-turbo, OpenAI fine-tuning API | ~3 h, $83.20 | Informal | Captured multi-line Slack structure; erratic at T=1.0 (fixed with lower temperature, higher frequency penalty); brusque; worse at other tasks |
| Gabor Cselle, `write-my-posts` livestream (2023-11-29) | ~10.9k tweets; 200/40 then ~4,000/500 non-reply tweets | GPT-3.5-turbo API; NER-tag prompts planned | n/r | Informal | Tone "reasonably well" at 200; 4k "a little bit better but not phenomenally so"; content often incoherent |
| Timo Stroet (2024-01-02) | 150k Discord messages, 4-hour session gaps, Alpaca format | facebook/opt-125m, TRL SFTTrainer | GTX 1660 Super, ~2 weeks | None | Nonsense and echoes; counting channel leaked numbers |
| Edward Donner, "A simulation of me" plus 4-part series (2024-01-02) | 240,805 SMS/iMessage/WhatsApp messages with 288 people (iMazing) → 25,087 chunks of 7–10 messages, ≤200 tokens | Llama 2 7B, then 13B ("a marked improvement"), QLoRA; extensive hyperparameter search | Google Cloud V100, ~$100 | Subjective; searched for regurgitation, found none | "More than half of the conversations would pass a Turing Test." Early surreal loops; fictional personas worse |
| Heralax_Tekran, r/LocalLLaMA (2024-04-08) [unverified: snippet and mirror] | Annotated notes, a book he wrote, role-swapped ChatGPT export | Full fine-tune with GaLore | Rented H100, ~2 h | Informal | "Slightly stilted," attributed to the ChatGPT data; recalled training content |
| Michael Daigler, "Making AI Write Like You" (2024-05-04) | Newsletters as instruction/output, blank input | Llama 3, Unsloth Colab; Alpaca-cleaned stage first | Colab | None | Draft "showcased a writing style similar to my own" |
| furiousteabag (Alex), Telegram (2024-06-13) | 5 years, 15,789 sessions from 466 chats, mostly Russian; ChatML, loss on all turns | Dolphin-2.2.1-Mistral-7B LoRA; Mistral 7B full FT | RTX 3090 5.5 h ~$2; 8× A100 ~20 min ~$3 | Cherry-picked samples | LoRA "definitely captures the style"; full FT "not significantly better"; weak context; "ok"/"busy" replies; Russian grammar errors |
| Aditya Rathod (2024-08-18), MLX | >291k Discord messages, ~4 years; bursts <15 min merged; `{"text"}` JSONL | Mistral 7B v0.3 base, 4-bit QLoRA, 5,000 iters | M1 Pro 16 GB, ~5 h, ~7.2 GB peak | Informal; Discord bot | "Copied my all-lowercase typing style and brevity"; instruct model gave 1–2-word replies; loops ("i love rust") |
| grapeot, "From Prompting to Fine-tuning" (2024-12-23) | Chinese blog paragraphs; LLM English translation as input, original as target | GPT-4o FT (50 ex; larger run ~$100, inconsistent); Qwen 2.5 3B/7B LoRA | Lambda GH200 ~$1.80/h | Informal against references | Every prompting method failed; Qwen tone "often very close to the reference answer" |
| BitsOfChris (2025-04-25) | ~2k Obsidian notes → 50 QA pairs by gpt-4o-mini | DeepSeek-R1-distill 1.5B; 8B; LoRA via LLaMA-Factory | Colab | Informal | 1.5B "gibberish"; 8B worked after tuning; abandoned |
| Didier Lopes (2025-09-02), MLX | 91 posts → ~2,100 Q&A | Phi-3-mini-4k-instruct LoRA r16 (r8 worse), 2,000 iters, early stop ~1,500 | M3 Max 48 GB | Jaccard overlap 0.157 → 0.201 (+27.6%) | Knowledge transfer weaker than hoped; exact chat template and system prompt mattered |
| Kevin Leary (2025-09-18), MLX | WordPress posts since 2009; templated title/date prompt | mlx-community/Meta-Llama-3.1-8B-Instruct-4bit, `mlx_lm.lora`, batch 1, 16 layers, 600 iters, LR 1e-5 | MacBook Pro "M3+" | None | No outputs shown |
| zwischenzugs (2025-11-04) | Gmail Sent folder | Qwen2.5-3B-Instruct, LLaMA-Factory | n/r | Sample outputs | Casual email signed with his name; spurious date |
| Lydia Nottingham (2025-11-20) | 114 examples (~91k tokens) from Substack RSS: 20 completions, 33 instructions, 61 Q&A | Llama 3.1 70B via Thinking Machines' Tinker, 3 epochs, LR 5e-5; loss 2.65 → 0.23 | ~10 min, $0.13 | Informal | "Captures my actual views + lydia-coded stylistic elements" |
| Jonathan Prevost (Feb 17, likely 2026) | 8,581 forum posts → 5,136 entries incl. 100 hand-written Q&A ×4 and 500 French Alpaca rows; reverse prompting | Gemma 3 12B, Unsloth LoRA r32, 2 epochs (24B attempt OOM) | RTX 4060 Ti 16 GB, ~1.5 h | Blind survey, 10 real-vs-clone pairs | 66% recognition; two clone replies judged more "real" than originals |
| Shane Larson (2026-03-13) | 6 own articles + 161 OpenHermes (224 total) | Mistral-7B-Instruct-v0.3 LoRA r32, 5 epochs | DGX Spark | Loss, token accuracy | Loss 1.05 → 0.09, 97% token accuracy; "convincingly adopted the writing voice"; "hallucinated code. Confidently." |
| Andrea Griffiths, GitHub (dev.to 2026-03-24; update 2026-03-17) | 81 examples from newsletters, talks, conversations; ChatML | Qwen3 8B (after Llama 3.1 8B), Unsloth LoRA r16/α32, 60 steps, LR 1e-4 | Colab T4; q4_k_m runs on a 16 GB MacBook Pro | Informal | Switching to Qwen3 8B "improved the output more than any hyperparameter tweak"; the model learned how she writes and did not learn how she thinks |
| Nic Lydon (May 9, likely 2026) | 75,329 samples (~3.1M tokens), 12 platforms, ~23 years; tapbacks, URL/emoji-only, quotes, PII stripped | Qwen 2.5 3B Instruct 4-bit, Unsloth QLoRA r16/α32 on all 7 projections, ShareGPT, 3 epochs (14,127 steps) | AMD Radeon 8060S 96 GB (ROCm), ~17 h | Blind A/B on 12 prompts vs base | Strong on casual chat, work chat, short email; weak long-form; r8 underfit; q/k/v-only "wrong vocabulary"; deployed as rewriter of frontier drafts |
| Shrestha Pandey (Jun 7, year not shown) | ~20 LinkedIn, Instagram, technical posts | Llama 3.2 3B Instruct, Unsloth LoRA → GGUF for Ollama | Colab T4 | None | Ready for real content? "Probably not"; memorization risk |
| Writekin, scouttyg / HN eggbrain (2026-07-28), MLX-Swift | Apple Mail, iMessage, documents, chat exports | On-device QLoRA; Compose screen drafts and rewrites | 16 GB min, 32 GB+ recommended | Pangram anecdotes | v0.9 "uneven," sometimes "completely off"; PolyForm Noncommercial |
| NicAI, Nicolas Deville (2026-09-20), MLX plan | 1,185 notes (~677k words; 99 AI-written) + 169 draft-and-sent email pairs; 490-line SOUL.md for labels and checks | Qwen2.5-1.5B-Instruct voice rewriter via `mlx_lm.lora` / `fuse` / `server` | Mac Studio M1 Ultra 128 GB | Planned: entity-split, frozen 30-pair blind test vs "Claude with SOUL.md" | No results. "The data work is the project, and the training is an afternoon at the end of it." |
| meyerdav, HN "Can my fine-tuned model pass Pangram?" (2026-11-01) | Own writing | Small local model, ~15 min | n/r | Pangram | "100% human" in some instances [self-reported; model and data size not given] |
| codebyandy/finetune-me (undated), MLX | iMessage `chat.db` + Slack; last 6 turns as context | mlx-community/Qwen3-4B-8bit, mlx-lm LoRA r16, LR 1e-4, 1,000 iters, seq 1024, batch 4 | M1, ~1–2 h | Planned: blind quiz, perplexity, frontier model with 20 examples | No results. "The model will sound like you while saying plausible nonsense." |
| iClone, ishan0102 (undated; likely early 2024), MLX | iMessage | Mistral-7B | Apple silicon | None | Multi-turn format still TODO |
| mlx-whatsapp, gavi (undated), MLX | WhatsApp "Export Chat → Without Media" | Mistral-7B-v0.1 base, `lora.py --iters 600 --batch-size 2` | Apple silicon | None | "Dont upload your fused models to public sites such a huggingface." |
| WeClone, xming521 (n.d.; 18.4k stars) | Chat histories; Telegram fully supported | Qwen2.5-7B-Instruct LoRA; Presidio PII filter | NVIDIA ~16 GB VRAM | n/r | Digital-twin toolkit; no MLX |
| Modal DoppelBot, modal-labs/doppel-bot (n.d.; 270 stars) | One target user's Slack messages | Llama 3.1 fine-tune (earlier OpenLLaMA per a third-party writeup [unverified]) | Modal | n/r | "Few minutes to an hour" of training; one user per workspace; Modal's "@erik-bot" from the CEO's Slack [unverified] |
| Sarah Constantin, "Fine-tuning LLMs for style transfer" (date n/r in notes) | 124 Dune-style quotes with hand-written questions | GPT-3.5 fine-tune | n/r | Informal | Style transfer "clearly happening"; more non sequiturs; argues with and belittles the user |
| OpenAI community thread (2023-01) | Tweets | Prompt-format suggestions | n/r | n/r | No successful fine-tune; the poster fell back to ~10 few-shot examples |

**Verification of commonly cited examples.** Donner and Miller are confirmed from primary write-ups; Miller's HN thread drew 751 points and 355 comments. Simon Willison did not fine-tune on his own writing. He linked Miller (2023-04-12: "one of the clearest explanations of the process of fine-tuning a model like this I've seen anywhere"), Lazerowitz (2023-11-08), and a Homer Simpson LLaMA fine-tune (2023-03-17: "Clearly my mental model around this was incorrect"). No "Sarah Chieng" clone project exists in the sources; the only hit was an unrelated Val Town Twitter-search tool credited to her and Alex Phan. No Eugene Yan fine-tune on his own writing was found. X/Twitter posts could not be searched.

**MLX projects.** Rathod, Lopes, Leary, codebyandy, iClone, mlx-whatsapp, Writekin and the NicAI plan. The official MLX "Community Projects" discussion (#654) lists only iClone and mlx-whatsapp among personal-data projects. Other MLX tools surfaced: mlx-lm-lora, MLX-LoRA-Studio, mlx-tune, Courtyard (Show HN 2026-02-25). Apple's WWDC25 session 298 says MLX LM fine-tunes locally "without sending data off the machine." No MLX project published a blind evaluation or before/after metrics apart from Lopes' word overlap. Privacy, more than speed, is why people chose MLX.

**Data formats in use** (five recurring patterns):
1. Raw text continuation on a base model (Rathod; Jeff Wang; StyleTunedLM).
2. Multi-speaker transcripts under a persona instruction (Donner; Miller; furiousteabag).
3. Context → my reply (Lazerowitz; codebyandy; Prevost; Carmo; DoppelBot per a search summary [unverified]).
4. Synthetic or back-generated prompts for standalone writing (Leary; Cselle; Prevost; Lopes; Nottingham; Constantin; Daigler).
5. Draft or translation → my version (grapeot; Lydon's deployment; NicAI's draft→sent pairs).

Standalone essays and tweets have no natural prompt. Inventing one is where most effort and many quality problems arise. No practitioner A/B-tested formats on the same data.

**Recurring lessons**
1. **Voice transfers; facts do not.** Larson: "The model learned my _style_. It did not learn the _facts_." Lopes: "Fine-tuning shapes behavior and style more than it adds information." grapeot: fine-tuning "can't give AI a new ability."
2. **Data work dominates.** NicAI (above). Prevost: "a model is only as good as its data." Pandey: "The actual training process ended up being the easiest step."
3. **Base model choice matters.** Griffiths (Qwen3 8B switch). Prevost: Gemma 3 12B was the "sweet spot" after Qwen3 and Ministral gave inconsistent results. Donner: 13B a "marked improvement" over 7B.
4. **LoRA is enough.** furiousteabag: full FT "not significantly better."
5. **Rank 16 over 8; include MLP projections** (Lopes; Lydon).
6. **Decoding matters as much as training** (Donner; Lazerowitz; Miller).
7. **Loss misleads; judge blind.** NicAI: "There is no dependable automatic metric for 'sounds like me'"; use a blind human comparison.
8. **Separate reasoning from voice** (Lydon), accepting NicAI's warning about added failure points, latency and fact wash-out.
9. **Privacy is first-class.** "Nothing leaves your machine" (Writekin). Train locally and keep data and adapters out of the repo (codebyandy). Don't publish fused models (mlx-whatsapp). PII scrubbing can cause odd hallucinations (muttled).
10. **Costs are trivial; reruns are the budget.** ~$0 (Colab, Griffiths), $0.13 (Tinker, Nottingham), $2–3 (Telegram), $83.20 (Lazerowitz), ~$100 (Donner, Miller, grapeot's GPT-4o run). NicAI: budget "5 to 10 times your first estimate, because the spend is in the reruns."
11. **Voice freezes in time.** Griffiths: the model "will always sound like 2026 Andrea." Nobody reports a retraining cadence.

Trend [inference in notes]: model sizes fell from 7B/13B/65B in 2023 to 3B/4B/8B in 2025–26 while reported quality held. Practitioners with 48–128 GB still chose small models (Phi-3-mini, Qwen2.5-1.5B), which suggests model size is not the bottleneck for style.

---

## 13. Commercial "write in my voice" products

| Product | Claimed mechanism | Per-user model training | Source |
|---|---|---|---|
| Jasper Brand Voice | "Upload up to 8 examples of text, files (.txt, .pdf, or .docx), and/or URLs"; analysis into an editable voice description; Style Guides (rules, Business tier); Memory for facts | No: Jasper "doesn't train large language models (LLMs) on your data" | Jasper help |
| Grammarly / Superhuman voice (launched 2023-10) | "Personalized voice detection and application"; automatic profile that "evolves as you write"; editable role and dialect; distinguishes short messages from long documents; Paraphraser custom voice from a few examples | Not claimed | Grammarly support; Superhuman help; TechCrunch 2023-10-25 |
| Writer.com | Personal voice profile (AI Studio → Voice & style) from analyzed samples or chosen characteristics; TechTarget reports two Palmyra models, one for voice extraction and one for generation | Not per user | Writer support; TechTarget |
| Hypotenuse AI | Studies "all of your existing content and brand guidelines"; "bespoke models learn how your brand actually speaks" | Unclear [vendor claim, no technical detail] | hypotenuse.ai |
| Personal.ai | Per-user "Personal Language Model" of ~120M parameters on a "Memory Stack," plus retrieval of 8–10 memory blocks per prompt; edits feed training | Claimed [vendor claim; internally inconsistent; no independent documentation] | personal.ai |
| Delphi (digital clones) | RAG on Pinecone, "over 100 million stored vectors across 12,000+ namespaces"; CTO: "Even if we have billion-token context windows, RAG will still be important" | No evidence | CO/AI on Pinecone case study |
| Every Spiral v4 | "Style Engine" computes a "writing fingerprint," selects relevant samples, "uses stylometry" at draft time; LLM-as-judge blind lineup on every draft; drafts indistinguishable 87% of the time; help docs advise 3–5+ samples and separate styles per context | No | Every announcement; Every help [vendor claim] |
| Claude Styles (Anthropic, 2024-11) | Upload or paste samples (pdf/doc/txt) or describe a style → reusable style instruction | No (prompting) | Anthropic support; Claude blog |
| Rephrasy.ai | Learns style "without training a model"; passes "every AI detector" | Unsupported Reddit claim | Reddit snapshot |
| Open source: DoppelBot, WeClone, Writekin | Per-user fine-tuning on Slack, chat history, or Mail/Messages on-device | Yes | GitHub |

[inference in notes] Vendors avoid per-user fine-tuning for cost, for privacy positioning ("we don't train on your data"), and because frontier APIs lack it; Anthropic's Messages API has no fine-tuning endpoint (stated on the NicAI page). The niche falls to open-source and local tools. Spiral's blind-lineup judge is the most concrete automatic voice evaluation in a product and can be copied. Typefully and Lex: no documentation found. No vendor style-match claim is independently verified.

---

## 14. Apple silicon tooling (as of 2026-11-07)

Reference hardware: the M4 Pro has 273 GB/s memory bandwidth in both 16-core and 20-core GPU configurations (llama.cpp discussion #4167). macOS reserves ~3.5 GB, leaving ~20.5 GB usable on a 24 GB Mac (willitrunai, 2026-04-20) [estimate]. Many figures below come from community blogs, not controlled benchmarks.

### 14.1 Training frameworks

| Tool | Status | Methods | Fit for this build |
|---|---|---|---|
| **mlx-lm** (ml-explore) | v0.32.2, Oct 16 (year inferred as 2026) | LoRA (default), DoRA, full; QLoRA automatic when the base is quantized | Default for SFT |
| **mlx-lm-lora** (Goekdeniz-Guelmez, Apache-2.0) | Community; `pip install -U mlx-lm-lora`; `mlx_lm_lora.train --train-mode <mode>` | SFT; DPO, CPO, ORPO, DSLA, FTPO; GRPO, GSPO, Dr. GRPO, DAPO, KLPO; Online DPO, XPO, RLHF Reinforce, PPO; LoRA/DoRA/full; QLoRA at 4/6/8-bit; QAT for SFT/DPO/ORPO/DSLA; `--judge` and `train_judge` for online methods | Preference stage |
| **mlx-tune** (ARahim3; formerly "unsloth-mlx"; not affiliated with Unsloth or Apple) | v0.6.0; macOS 13+, Python 3.9+; 8 GB min, 16 GB+ recommended | Unsloth-style API (`get_peft_model`); SFT, DPO, ORPO, GRPO, KTO, SimPO, CPT, vision, audio, embeddings; GGUF export; RL single-sample only | Only SimPO path found; OOM on 8B ORPO in one comparison |
| **mlxsmith** | Alpha (PyPI 0.1.3) | Wrapper around mlx-lm-lora for DPO, ORPO, GRPO | Not ready |
| **mlx-optiq** | Docs | Fused cut-cross-entropy (auto above `max_seq_length=4096`); opt-in `--fused-dpo` | Long-context SFT/DPO in 24 GB |
| **PyTorch MPS + PEFT/TRL** | MPS still "beta" | LoRA; no practical 4-bit QLoRA; fp16/fp32 | Only at 3–4B when the HF/TRL ecosystem is needed |
| **Unsloth** | Studio (GUI) claims "full support for training, MLX and GGUF inference" on macOS; Core's Apple/MLX support "in the works"; no dates | SFT/LoRA via MLX; DPO/GRPO on Mac not covered [secondary comment] | Unproven |
| **Axolotl / LLaMA-Factory** | A Medium write-up covers Axolotl LoRA on Apple silicon via MPS (not read) | n/r | No 2026 confirmation |
| **Apple Foundation Models adapter toolkit** | Beta 0.1.0 → Beta 0.2.0 → 26.0.0 final; "not compatible with macOS, iOS, iPadOS, or visionOS 27 and later" | LoRA on Apple's ~3B system model; rank fixed at 32 (third-party) | Not viable: needs ≥32 GB |

**mlx-lm details**
- Install `pip install "mlx-lm[train]"`; entry point `mlx_lm.lora`.
- Release history (years inferred): v0.32.2 (Oct 16), v0.32.1 and v0.32.0 (Oct 15), v0.31.3 (Apr 22), v0.31.2 (Apr 07; Gemma 4 support and tool parser; trainer memory-clearing fix), v0.31.0 (Mar 07; Qwen 3.5 tensor parallelism), v0.30.7 (Feb 12; GLM5, Qwen 3.5 without vision; validation set optional), v0.30.6 (Feb 04; Transformers v5). No release mentions GGUF. v0.32 notes mention "Muse Spark" (NVFP4) without details.
- `CONFIG_DEFAULTS` in `mlx_lm/lora.py`: `fine_tune_type: lora`; `optimizer: adam` (adamw, muon, sgd, adafactor available); `num_layers: 16` (−1 = all); `batch_size: 4`; `iters: 1000`; `val_batches: 25`; `learning_rate: 1e-5`; `steps_per_eval: 200`; `save_every: 100`; `max_seq_length: 2048`; `grad_checkpoint: False`; `grad_accumulation_steps: 1`; `lora_parameters: {rank: 8, dropout: 0.0, scale: 20.0}`; `mask_prompt: False`; `report_to: None` (wandb, swanlab); `seed: 0`.
- Rank, scale and dropout have no CLI flags; set them under `lora_parameters` in the YAML config. The example YAML returned 404, so `lora_parameters.keys` (target modules) was not confirmed.
- Data: `train.jsonl` (required), `valid.jsonl` (optional since v0.30.7), `test.jsonl`. Auto-detected formats: `text`, `chat` (`messages`), `completions` (`prompt`/`completion`, custom keys via `prompt_feature`/`completion_feature`), `tools`. HF datasets via an `hf_dataset` YAML block. Chat templates applied by default. `--mask-prompt` works only for chat and completions.
- Memory advice in LORA.md: QLoRA; batch 4 → 2 or 1 with `--grad-accumulation-steps`; `--num-layers` 16 → 8 or 4; split long examples; `--grad-checkpoint`.
- Test perplexity with `mlx_lm.lora --test`. Generate unfused with `mlx_lm.generate --adapter-path`.
- `mlx_lm.fuse` flags: `--model`, `--save-path`, `--adapter-path`, `--upload-repo`, `--dequantize`, `--export-gguf`, `--gguf-path`, `--trust-remote-code`. GGUF export accepts only `llama`, `mixtral`, `mistral` model types in fp16; other types raise `ValueError`. It does not dequantize without `--dequantize`.
- mlx-tune: GGUF export "doesn't work directly from a 4-bit base model (mlx-lm limitation)"; merging into a 4-bit model "can erase small LoRA updates," so merge at 16-bit.
- HF forum: a Gemma 4 E4B adapter worked unfused and failed fused; mlx_vlm server issue #907 dropped the adapter from cache under `--adapter-path`.
- LORA.md's model-family list is stale (Mistral, Llama, Phi2, Mixtral, Qwen2, Gemma, OLMo, MiniCPM, InternLM2). No official statement covers LoRA on Qwen 3.5's Gated DeltaNet layers end to end.
- [inference in notes] GGUF path for Qwen or Gemma: `mlx_lm.fuse --dequantize` → llama.cpp `convert_hf_to_gguf.py` → `llama-quantize`. Not verified.

**PyTorch MPS details**
- HF blog (harshitkgupta), Qwen 2.5 0.5B–3B LoRA on a 16 GB Mac, 10 runs: MPS had 2.2–5.7× higher raw throughput; MPS could not load 3B fp16 on 16 GB while MLX 4-bit fit; dequantization explains only ~1.07–1.4× of the gap, leaving a ~4.1–4.6× framework gap; eval loss tracked closely [unverified: search summary only].
- longform.social post: PyTorch documents AdamW on MPS for float32/float16 only; an open issue reports bf16 unsupported on some setups; TRL enables bf16 when fp16 isn't set (a trap on MPS) and enables gradient checkpointing by default (misbehaves, citing a Gemma 4 issue). Recommends fp16 for training, fp32 for smoke tests.
- mac-playbooks (PyTorch MPS): fp16 backward on MPS can give NaN gradients; fp32 roughly doubles memory. Possibly outdated.

**Unsloth details.** Requirements page: Studio needs Python 3.11 up to 3.14 (training 3.11–3.13); export on CPU "coming very soon." PR #14457 calls the MLX backend "a first-class path" and says `unsloth train/chat/inference/export` detect MLX. Issue #685 comment: Apple silicon takes the MLX path for SFT/LoRA; "Intel Macs and GRPO or DPO are still not covered" [secondary].

**Apple details**
- FM adapter toolkit: Apple silicon Mac with ≥32 GB (or Linux GPUs), Python 3.11+. JSONL `messages`. Apple suggests 100–1,000 samples for basic tasks, 5,000+ for complex. Example `--epochs 5 --learning-rate 1e-3 --batch-size 4`. ~160 MB per adapter, tied to one system-model version. Deployment needs the `com.apple.developer.foundation-model-adapter` entitlement; toolkit weights may only be used to train adapters.
- Axiom reference: `SystemLanguageModel.Adapter` deprecated in 26.4, obsoleted in 27.0, with no adapter replacement in the 27 SDK.
- WWDC26: Core AI deploys custom on-device models (with a Torch conversion package); Core AI models can be swapped into a Foundation Models `LanguageModelSession` (Apple's demo used Qwen). Session 339 describes public `LanguageModel` and `LanguageModelExecutor` protocols covering Apple models, Core AI, MLX and custom packages (sessions 324, 382, 326; 339 via wwdc.ai). This is serving inside Swift apps, irrelevant for a Claude Code tool.
- An iOS 27 on-device "Foundation Models Adapter Trainer" for per-user adapters (ninetwothree blog) [unverified].

### 14.2 Memory and throughput

| Source | Hardware | Model and setup | Peak memory | Speed |
|---|---|---|---|---|
| mlx-lm-lora README [self-reported] | M4 Pro 24 GB | Qwen3-8B 4-bit SFT, all LoRA layers, batch 1, ctx 4096, 100 steps | ~6–10 GB | ~4.1 it/s (implies short sequences) |
| same | M4 Pro 24 GB | Qwen3-0.6B bf16: SFT / ORPO / GRPO | ~2 / ~2–4 / ~9–20 GB | ~4.7 / ~4.5 / ~0.02 it/s |
| same, mlx-tune run | M4 Pro 24 GB | Qwen3-8B SFT; ORPO; GRPO | ~8–18 GB | ~0.07 it/s; OOM on ORPO and GRPO |
| mlx-optiq docs [self-reported] | M3 Max 36 GB | Qwen3.5-4B 4-bit OptiQ, batch 1, all layers, grad ckpt, SFT at 2k / 4k / 8k | 7.7 / 11.4 / 19.9 GB | 2.8 / 6.7 / 45 s per step |
| same | M3 Max 36 GB | DPO with `--fused-dpo` at 2k / 4k / 8k | 8.7 / 10.9 / 17.3 GB | 29 / 144 / 216 s per step |
| sciences44 [measured] | M1 64 GB | 4-bit, rank 8, 16 layers, LR 1e-5, 600 iters, short text-to-SQL: Qwen3.5-0.8B / 2B / 4B / Mistral-Nemo-12B | 3.9 / 5.9 / 11.1 / 8.2 GB | ~475 / ~180 / ~115 / ~210 tok/s; ~15 / 8 / 12 / 8 min |
| deadbydawn101 HF card | M4 Max 128 GB | Gemma 4 E4B LoRA via `mlx_vlm.lora` | 7.876 GB | ~190 tok/s |
| rainytechlab (DEV) | n/r | Qwen2.5-3B 4-bit smoke test | ~2.5 GB | ~16 s run |
| LORA.md | M1 Max 32 GB | Mistral-7B-v0.1, batch 1, 4 layers | n/r | ~250 tok/s |
| Rathod | M1 Pro 16 GB | Mistral 7B v0.3 4-bit QLoRA, 5,000 iters | ~7.2 GB | ~5 h |

- mlx-optiq on a 24 GB M4: 8k context peaks ~14.7 GB with fused cut-cross-entropy; the plain path OOMs. DPO OOMs at ~4k without `--fused-dpo`.
- sciences44 hit 97% RAM at batch 2 on the 2B; trainable params 13.6M (0.32%) for 4B, 18.0M (0.15%) for 12B.
- Estimates: InsiderLLM guide (updated 2026-11-04; no test machine named) rates a 24 GB Mac "Comfortable" for LoRA at 7–8B and QLoRA at 8–14B; Llama 3.1 8B ~14 GB LoRA / ~7 GB QLoRA; Qwen 2.5 14B ~24 / ~12 GB (contradicting its own 14–18 GB figure); 8B LoRA ~200 (M2 Pro), ~250 (M1 Max), ~320 (M3 Max), ~380 (M4 Max) tok/s; gradient checkpointing +~30% time; 200–500 examples at 300–600 iters ≈ 15–45 min. willitrunai: M4 Pro 24 GB "marginal" for larger Qwen 3.5 models; ~2 h for 600 iters of 9B LoRA on an M4 Max 64 GB; full FT of 9B needs 40+ GB. Unsloth GPU minimums: 7B 5 GB QLoRA, 19 GB LoRA (VRAM). apxml QLoRA memory chapter: activations scale with batch × sequence length.

Fit on 24 GB [inference in notes]:

| Model size | Approach | Fit |
|---|---|---|
| 3–4B | bf16 LoRA | Fits (~8 GB weights plus activations) |
| 3–4B | QLoRA | Easy; ~8k context with fused CE |
| 7–9B | QLoRA | Best balance (~5–6 GB weights; 6–10 GB peak at 4k self-reported) |
| 7–9B | bf16 LoRA | Tight / risky (~16–18 GB weights) |
| 12–14B | QLoRA | Feasible at batch 1, grad checkpointing, ≤2–4k context |
| 12–14B | bf16 LoRA | Does not fit |
| Any | Full fine-tune | Only below ~1–2B |

Throughput [estimate]: ~100–200 training tok/s for QLoRA at 8–14B; ~200–400 at 3–4B. A ~1M-token corpus takes ~1–3 h per epoch at 8B QLoRA. Sequence length is the biggest memory lever; chunk prose into 1–2k-token windows.

Gaps: no independent M4 Pro 24 GB measurement of `mlx_lm.lora` tok/s and peak memory for 4–9B models on long prose. No measurement of memory pressure or swapping at 12–14B. The `sysctl iogpu.wired_limit_mb` headroom setting was not verified.

### 14.3 Base models that train on 24 GB

| Model | Release | License | Base checkpoint | Notes |
|---|---|---|---|---|
| Qwen3.5 4B / 9B | 2026-03-01/02 (also 0.8B, 2B) | Apache 2.0 | Yes | Artificial Analysis Intelligence Index: 9B 32, 4B 27, top of their size classes. Architecture (4B): 32 layers, repeating 3× Gated DeltaNet + 1× gated attention; control tokens trained so LoRA works with the chat template. Natively multimodal: the 4B needed vision weights stripped or MLX LoRA crashed. Thinking template caused errors; text format avoided them. Larger-than-normal quantization differences (Unsloth guidance cited on HF forum). Lydon: 9B OOM in training |
| Gemma 4 E4B / 12B "Unified" | E4B 2026-03-31; 12B 2026-06-03 | Apache 2.0 [secondary sources] | Only `-it` IDs surfaced | E4B 128K context. E4B LoRA via `mlx_vlm.lora` ~7.9 GB. Fused-checkpoint failure report. mlx-lm support from v0.31.2. Unsloth: bf16 LoRA for the 26B-A4B MoE, QLoRA not recommended there. 12B Unified architecture unconfirmed |
| Ministral 3 3B / 8B / 14B (Mistral AI) | arXiv:2601.08584 (Jan 2026); eWeek | Apache 2.0 | Yes: base, instruct, reasoning | LM Studio 0.3.33 support. Notes infer a smoother export path |
| OLMo 3 7B (`allenai/Olmo-3-1025-7B`) | ID suggests Oct 2025 [inference] | Apache 2.0 | Yes | Fully open data, code, checkpoints; 5.93T tokens; 32 layers; 65,536 context; 32B sibling; Olmo-3 tool calling in LM Studio 0.3.33 |
| Fallbacks | Gemma 3 1B/4B/12B/27B (2025-03-10); Gemma 3n E2B/E4B (2025-06-26); Qwen3 4B/8B/14B; Llama 3.1 8B | Various | Various | Llama/Mistral types work with mlx-lm GGUF export. SmolLM3, Phi-4/Phi-4-mini, Mistral Small not re-verified |

- Other Gemma releases: Gemma 4 31B and 26B A4B (2026-03-31), MTP variants (2026-04-16). Nothing listed for November 2026.
- Larger Qwen 3.5 (27B dense, 35B-A3B MoE, 122B-A10B MoE): 27B and 35B-A3B at 4-bit are "tight"/"marginal" even for inference on a 24 GB M4 Pro (~17–20 GB).
- A 2026 creative-writing roundup (PromptQuorum) picks Gemma 4 31B for prose on 24 GB GPUs; it is GPU inference and low reliability (it mentions an unverifiable "Qwen3.8-27B").
- No models released in October–November 2026 beyond these were found. No rigorous benchmark of post-LoRA style imitation across these small models exists.
- Notes' picks [inference]: primary, Qwen3.5-9B or Ministral 3 8B in QLoRA; fast iteration, Qwen3.5-4B or Gemma 4 E4B in bf16 LoRA; stretch, Gemma 4 12B or Ministral 3 14B in QLoRA with short sequences.

### 14.4 Serving

| Server | Adapter handling | Notes |
|---|---|---|
| `mlx_lm.server` | Per-request `adapters` path (relative to the server's start directory); no fuse step | OpenAI-compatible on localhost:8080; `/v1/chat/completions`, `/v1/models`; `draft_model` speculative decoding (`num_draft_tokens` default 3); streaming; `--kv-bits`; "not recommended for production" (basic security checks only). `--adapter-path` startup flag unverified |
| llama.cpp `llama-server` | `--lora FNAME` (comma-separated), `--lora-scaled FNAME:SCALE`, `--lora-init-without-apply`; `GET /lora-adapters`; `POST /lora-adapters` with `[{"id": 1, "scale": 0.5}]`; per-request `lora` on `/completion` | "Requests with different LoRA configurations will not be batched together." README silent on `lora` in `/v1/chat/completions`. Older issue #10374 (global-scale hot-swap) appears addressed |
| Ollama v0.40.15 (2026-11-03) | Modelfile `ADAPTER` documented for Llama 2/3/3.1, Mistral 1/2, Mixtral, Gemma 1/2 safetensors, and GGUF adapters; `FROM` must match the adapter's base; non-QLoRA adapters recommended | Ollama 0.19 (blog 2026-03-30) runs on MLX in preview, pitched at Macs with ">32GB of unified memory"; on 24 GB it may still use llama.cpp. Claims that MLX became default in v0.40.0 (Sept 2026) with 16/24 GB fallback [unverified]. Import a fused model |
| LM Studio | No official LoRA-adapter documentation | Ships MLX and llama.cpp engines (ExLLM docs). No built-in LoRA training (PromptQuorum KO, Apr 2026). Community script `export_to_lms.py` fuses, converts to GGUF and copies into LM Studio's models folder |

- mlx-lm server changes: OpenAI-compatible `finish_reason` (v0.30.5); `chat_template_kwargs`, `top_logprobs` (v0.30.6); prompt-cache improvements (v0.31.0); `--allowed-origins`, parallel tool-call fix (v0.31.2).
- Ollama MLX blog: Qwen3.5-35B-A3B NVFP4 prefill 1810 tok/s and decode 112 tok/s vs 1154 and 58 on 0.18 (hardware not specified); promises "an easier way to import" fine-tuned models. Recent release notes: faster Gemma 4 prompt processing on Apple silicon, DFlash2 speculative decoding on MLX, faster top-k on MLX; nothing on adapters. Third-party coverage (yage.ai 2026-03-31; gingter.org 2026-04-23): GGUF runs on llama.cpp and safetensors on MLX inside Ollama.

**Speed**
- Measured, llama.cpp, LLaMA 7B, M4 Pro 20-core: Q4_0 TG128 50.74 tok/s, PP512 439.78 tok/s; Q8_0 TG 30.69; F16 TG 17.18. 16-core M4 Pro Q4_0: TG 49.64, PP 364.06. M4 Max 40-core Q4_0: TG 83.06.
- willitrunai [estimate], MLX on M4 Pro 24 GB: Qwen 3.5 9B 4-bit ~32–42 tok/s at ~6 GB; 9B 8-bit ~30–40 at ~10.4 GB; 27B 4-bit ~15–22 at ~17–18 GB; 35B-A3B 4-bit ~18–25 at ~19.5–20.5 GB.
- apple-silicon-llm-bench [measured, M4 Max]: Qwen3-4B ~145 tok/s, Gemma 3 4B ~141 tok/s decode (MLX/Core AI).
- llmcheck [estimate]: Qwen3 8B Q4_K_M on an M4 Pro via Ollama ~45 tok/s.
- 500 generated tokens on an M4 Pro [estimate]: 4B 4-bit ~7 s (~70 tok/s); 7–9B 4-bit ~10–16 s (~32–50 tok/s); 7–9B 8-bit ~16 s; 12–14B 4-bit ~18–20 s (~25–28 tok/s); plus ~1–2 s prefill for a 500–1,000-token prompt. Unfused adapters add a small overhead.
- Notes' serving path [inference]: dev loop on `mlx_lm.server` with per-request adapters for A/B tests; stable deploy via `mlx_lm.fuse --dequantize` then `mlx_lm.convert -q`, or GGUF for Ollama/LM Studio; `llama-server` when multiple adapters or a scale-based style-strength knob are wanted.

### 14.5 Exposing the model to Claude Code via MCP

- **SDK.** Official MCP Python quickstart (2026-07-28 spec revision): Python 3.10+, MCP Python SDK ≥2.0.0, `uv add "mcp[cli]"`; `from mcp.server import MCPServer`, `mcp = MCPServer("...")`, `@mcp.tool()` (type hints and docstrings generate schemas), `mcp.run(transport="stdio")`; depends on `httpx2`. "Never write to stdout" in stdio servers; log to stderr. Older tutorials use FastMCP; whether `from mcp.server.fastmcp import FastMCP` still works in 2.x is unverified.
- **Registration.** `claude mcp add [options] <name> -- <command> [args...]`, e.g. `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080`. Scopes: `local` (default, `~/.claude.json` per project), `project` (`.mcp.json`, shareable), `user`. `.mcp.json` stdio entries use `command`, `args`, `env` with `${VAR}` expansion.
- **Limits.** `MCP_TIMEOUT` sets startup timeout. Per-server `"timeout"` (ms) overrides `MCP_TOOL_TIMEOUT` (~28 h when unset). `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` defaults to 30 min for stdio. `MAX_MCP_OUTPUT_TOKENS` defaults to 25,000, warning above 10,000.
- **Community bridges** (review before running): Glama `custom-mcp` (FastMCP bridge to any OpenAI-compatible service, port 5001, `.env` config); mcpmarket `ollama-claude`; playbooks Ollama MCP server. No maintained reference server wraps `mlx_lm.server`.
- **Notes' design [inference].** One tool, e.g. `draft_in_my_voice(instructions, source_text=None, max_tokens=600, temperature=0.8)`, POSTing to `http://127.0.0.1:8080/v1/chat/completions` with an `adapters` path; optional `adapter_version` and `style_strength`. Keep the model server as a separate long-running process (launchd or terminal) so model load does not delay Claude Code startup. Set a per-server timeout around 120,000 ms. The tool description should say when to call it and that Claude should lightly edit the output, so Claude does not paraphrase the voice away.

---

## 15. Open gaps

1. **The key comparison is missing.** No blind study on one person's held-out writing compares a fine-tuned local model, a frontier model with style guide and retrieved exemplars, and frontier draft → local restyle.
2. **Newest frontier models are untested** on everyday-author imitation (GPT-5-class, Claude 4.x, Gemini 2.5/3). The latest tested are GPT-4o, Gemini-2.0-Flash, DeepSeek-V3, Llama-4-Maverick.
3. **Style guides vs demonstrations** for individual authors: no controlled study.
4. **Inversion input forms** (paraphrase, outline, generic draft): no comparison.
5. **Scaling:** no study of single-author style fidelity against data size, LoRA rank and base-model size. No per-user LoRA vs full FT comparison at frontier scale with human judges.
6. **Preference optimization on one real person's text** as chosen: no measured result.
7. **Retrieval by register vs by topic** for a fine-tuned style model: unmeasured.
8. **Self-recognition:** no study of authors picking their own writing against imitations, and no guidance on the number of blind trials.
9. **Evaluators:** no validated absolute "sounds like me" score; no study of LLM-judge agreement with the author; no study of judge self-preference in style matching; no validation of slop-score or composite stylometry against human judgments.
10. **Failure measurement:** no measurement of signature-phrase collapse, instruction-following loss after per-user tuning, or hallucination rates of LoRA restylers on long-form text.
11. **Long-form text:** transfer benchmarks use ≤60-token Reddit comments.
12. **Hardware:** no independent M4 Pro 24 GB measurements for 8–9B LoRA on long prose; 8–9B ORPO/DPO memory on 24 GB unmeasured; Ollama MLX on 24 GB and adapter import for Qwen/Gemma unconfirmed; LM Studio adapter loading undocumented.
13. **Data hygiene:** no independent benchmark of quote and signature stripping on 2024–26 mail clients; no register-tag vs per-register-adapter comparison.
14. **Longevity:** no reports on whether people keep using voice models or how often they retrain as style drifts.

---

## 16. Implications for the build

Mapped to the coordinator's five-point approach. "Flag" marks where the notes add a constraint or point the other way. The build plan is in `/Users/natuanand/quill/knowledge_base/plan.md`.

**(1) Prompting alone is insufficient; train a LoRA/QLoRA style adapter with MLX on an ~8–9B open-weight model.**
- Supported. Prompted imitation fails on informal registers (Blog AV ~17–21%) and draws expert rejection (OR 0.16). Weight updates hold the only strong human-judged wins (Panza, Chakrabarty, DITTO, StyleTunedLM). 7–9B QLoRA is the notes' best balance on 24 GB; Qwen3-8B 4-bit SFT peaks ~6–10 GB at 4k context on an M4 Pro 24 GB [self-reported].
- Flag: the case is weakest for structured email, where 5-shot prompting already passes AV 95%+, and Jemama & Kumar report 97–100% verifier pass with completion prompting on formal essays. If the user's corpus is mostly formal email, expect a narrow margin over the baseline in point (5).
- Flag: Qwen3.5-9B carries reported quantization sensitivity, vision-weight and thinking-template quirks, and one training OOM report. Ministral 3 8B or Llama 3.1 8B are lower-risk QLoRA candidates. Compare a 4-bit and an 8-bit base, and keep a 4B bf16 LoRA as the fast-iteration path. InMyStyle saw no gain from scaling 0.5B → 7B, and practitioners with large RAM still chose small models.
- Flag: mlx-lm defaults (rank 8, top 16 layers, LR 1e-5) sit below the evidence. Use all linear layers, all layers, rank 16–32, LR ~1e-4, 1–3 epochs, early stopping, and watch for training loss < ~0.2. Panza found LoRA below RoSA and full FT on MAUVE; RoSA does not appear in the MLX tooling covered. DoRA is available in mlx-lm and untested for style.
- Flag: mlx-lm GGUF export covers only llama/mistral/mixtral types. Serve unfused through `mlx_lm.server` with per-request adapters, or fuse with `--dequantize` and convert via llama.cpp (unverified path).

**(2) Training data by style inversion plus synthesized task prompts, with the user's text verbatim as the target.**
- Supported by STRAP, TinyStyler, ASTRAPOP (neutral → original), Chakrabarty (content description → text), Panza, LongForm and Humpback (reverse instructions). Back-and-Forth Translation shows the response-rewriting step to avoid.
- Flag: no study compares paraphrase, outline and generic-draft inputs. Mix all three with an input-type tag and ablate.
- Flag: each synthesized prompt must carry every fact in the target (recipient, purpose, numbers, dates, thread context), or the model learns to invent specifics (codebyandy; zwischenzugs).
- Flag: use a neutralizer from a different model family than the runtime drafter, or several, so the rewriter does not learn one drafter's quirks.
- Flag: "verbatim" applies after cleaning. Strip quoted history, signatures and code; replace PII with typed placeholders; exclude AI-written or AI-assisted texts (NicAI's "imitate an imitation"). Named-entity loss masking (StyleTunedLM) is compatible because it changes the loss and leaves the text intact.
- Flag: the best-measured small-corpus recipe is StyleTunedLM's raw-text LoRA on a base model merged with an instruction adapter. A short raw-text "voice" pass before pair SFT is a cheap variant worth testing.
- Tag register and recipient. Split held-out data by topic and entity. Target ≥50k–80k words of clean text overall and ≥~100 examples per register.

**(3) Optional light preference stage (ORPO/SimPO; chosen = real text, rejected = generic LLM version), gated on eval.**
- Supported in shape. Gutenberg-DPO, the nbeerbower ORPO models and Quill use this construction. ASTRAPOP measured a modest gain over SFT (joint 0.484 → 0.507). DITTO shows preference-style training wins at very low data. Gating fits the expected size of the gain.
- Flag: no controlled ORPO or SimPO result exists for one person's style. ASTRAPOP measured DPO and CPO; DITTO is an online method. mlx-lm-lora's Online DPO/XPO with a judge is the nearest MLX analogue to DITTO [inference].
- Flag: the notes favor self-generated rejects (the SFT adapter's own outputs, Quill-style) over a generic frontier version, because they target what the adapter still gets wrong. Build both reject types and compare.
- Flag: PO costs meaning (ASTRAPOP SBERT 0.754 → 0.726–0.733), and DPO erodes quality and diversity as pairs grow (Antislop: quality 67.80 → 54.61 at 8k pairs). Require a semantic floor between chosen and rejected; LR 5e-7 to 5e-6; ~1 epoch. FTPO (in mlx-lm-lora) is the measured alternative for suppressing tics.
- Flag: tooling. mlx-lm-lora provides ORPO and DPO. SimPO appears only in mlx-tune, which ran out of memory on 8B ORPO on an M4 Pro 24 GB in a comparison published by mlx-lm-lora's author. 8–9B ORPO memory on 24 GB is unmeasured; DPO on a 4B OOMs at ~4k context without `--fused-dpo`. Cap sequences near 1,024 tokens and run batch 1 with accumulation.

**(4) Runtime: frontier model supplies content; local style model rewrites; register-based retrieval of past writing; best-of-N reranking on style + meaning; fallback.**
- Supported. TinyStyler proposes restyling chat-model output and gains from rerank(5). Practitioners converge on draft-then-restyle (Lydon, NicAI, Writekin). Register-based retrieval follows from Wang et al.'s finding that topic-matched exemplars cut attribution sharply.
- Flag: Panza found retrieval at inference over a fine-tuned model caused over-copying of past emails; training with retrieval in context (RAFT) fixed it. If retrieved exemplars enter the rewriter's prompt at runtime, include them in training prompts too. Otherwise keep retrieval for the frontier content stage. APM found RAG helped only with the stronger base model.
- Flag: frontier fingerprints live partly in content choices (Sun et al.), and drafts anchor the result (Baumler, g=−1.43). A content outline or fact list may leave less residue than a full draft. Untested; evaluate both input forms.
- Flag: rewriters drop facts (NicAI) and break local coherence (Unslopper). Check entity, number, date and URL preservation (all kept, none added) and bidirectional NLI against the content. Rewrite long documents per paragraph at low temperature.
- Flag: the style scorer used for reranking must differ from the one used in evaluation (TinyStyler). If best-of-N uses StyleDistance, evaluate with LUAR and the held-out verifier, or the reverse.
- Flag: latency. ~10–16 s per 500 tokens at 7–9B 4-bit [estimate], multiplied by N unless batched. Size N and the MCP per-server timeout (notes suggest ~120,000 ms) together.

**(5) Local eval harness (held-out authorship verifier, StyleDistance/LUAR, meaning check, slop score, stylometry diffs, blind pairwise self-test) with a prompt-only frontier baseline the adapter must beat.**
- Supported. Every component runs locally: StyleDistance, Wegmann and LUAR (~0.1B each), MIS (~355M), a ModernBERT-base or char-n-gram verifier, slop-score, faststylometry.
- Flag: local 8B LLM judges score below chance (Llama-3.1-8B 0.279). Use a frontier judge pairwise with position swaps if privacy allows (gpt-4.1 0.815), or calibrate a local judge on known pairs first.
- Flag: LUAR is topic-leaky (STEL-or-Content 0.03). Evaluate on held-out topics with same-topic impostors. Sanity-check each embedding on the user's own data before trusting it.
- Flag: Delta-style stylometry needs ≥2,000 pooled words per condition. Use per-feature z-scores for single outputs.
- Flag: Binoculars in bf16 does not fit in 24 GB; GPTZero and Pangram are cloud APIs. Calibrate detectors and slop rates on the user's own text and report deltas from that baseline.
- Flag: self-judgment is weak (r ≈ 0.24 with LUAR; ghostwriter effect). Delay the self-test by days, run ≥20 trials (≤6 correct = indistinguishable, ≥15 = detectable at n=20), and add a reader who knows the user's writing.
- Flag: make the baseline strong. Frontier model plus style guide, register-matched (not topic-matched) exemplars, and an opening snippet where the task allows. NicAI calls this "the real baseline." No one has published this comparison, so the result is itself a contribution.
- Validation loss is not a quality signal (Donner; NicAI; sciences44).

**Other**
- Privacy: train and serve locally; keep other people's messages as masked context; never publish adapters or fused models (mlx-whatsapp; codebyandy).
- Budget for reruns, not the first run (NicAI).
- Plan for retraining as the user's style drifts (Griffiths).

---

## 17. References

All web sources were accessed 2026-11-07 by the notes' authors. Titles in quotes are as given in the notes; three titles marked "(title from reviewer's prior knowledge)" were not in the notes. Markers [unverified], [secondary], [self-reported] and [vendor claim] carry over from the notes.

### 17.1 Academic papers

- Ahmed (2026, Jan). n-gram logit-space style injection (TinyLlama-1.1B). arXiv:2601.16224. https://arxiv.org/html/2601.16224
- Alhafni, Kulkarni, Kumar, Raheja (2024). Fine-grained linguistic control benchmark for personalization. arXiv:2402.04914. https://arxiv.org/abs/2402.04914
- Babakov et al. (2022). Mutual Implication Score. ACL 2022 Student Research Workshop. https://aclanthology.org/2022.acl-srw.23.pdf ; model https://huggingface.co/s-nlp/Mutual_Implication_Score ; license listing https://www.promptlayer.com/models/mutualimplicationscore
- Bao et al. (2023, Oct). Fast-DetectGPT. arXiv:2310.05130. https://arxiv.org/pdf/2310.05130 ; repo summary https://www.sourcepulse.org/projects/1843956 [secondary]
- Baumler et al. (2026, Apr). "Can You Make It Sound Like You? Post-Editing LLM-Generated Text for Personal Style." UMD; pre-registered. arXiv:2604.24444. https://arxiv.org/html/2604.24444v1 ; https://arxiv.org/html/2604.24444
- Biderman et al. (2024, May). "LoRA Learns Less and Forgets Less." TMLR 2024. arXiv:2405.09673. https://arxiv.org/abs/2405.09673
- Chakrabarty, Ginsburg, Dhillon (2025, Oct). "Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers." Preprint under review. arXiv:2510.13939. https://arxiv.org/abs/2510.13939 ; https://arxiv.org/html/2510.13939
- Chakravorty (2026, Jul). "Small Is Enough: Per-User Style Rewriting of AI-Edited Text via LoRA Adapters" (InMyStyle). arXiv:2607.29238. https://arxiv.org/abs/2607.29238
- COPE, "Personalized LLM Decoding via Contrasting Personal Preference" (n.d.). Lacuna summary https://lacuna.tiptreesystems.com/work/personalized-llm-decoding-via-contrasting-personal-preference/wrk_e267a8ec1d52eec496d307e0912d76a4 [secondary; unverified]
- Eder (2010; 2013). "Does Size Matter? Authorship Attribution, Small Samples, Big Problem." DH 2010; Literary and Linguistic Computing 2013, doi:10.1093/llc/fqt066. https://dh2010.cch.kcl.ac.uk/academic-programme/abstracts/papers/html/ab-688.html ; methodology page https://computationalstylistics.github.io/projects/methodology ; "Short Samples in Authorship Attribution" https://dh-abstracts.library.virginia.edu/works/3978 ; Eder (2015), cited via StyleTunedLM.
- Fisher et al. (2024, Aug). StyleRemix. arXiv:2408.15666. https://arxiv.org/abs/2408.15666
- Gao et al. (2024). PRELUDE/CIPHER, "Aligning LLM Agents by Learning Latent Preference from User Edits." Microsoft; NeurIPS 2024. arXiv:2404.15269. https://doi.org/10.48550/arXiv.2404.15269 ; https://www.microsoft.com/en-us/research/publication/aligning-llm-agents-by-learning-latent-preference-from-user-edits/
- Hallinan et al. (2023, Nov). STEER. arXiv:2311.07167. https://arxiv.org/abs/2311.07167
- Hans et al. (2024, Jan). Binoculars. arXiv:2401.12070. https://arxiv.org/abs/2401.12070 ; code https://github.com/ahans30/Binoculars ; https://huggingface.co/blog/dmicz/binoculars-text-detection ; https://weaviate.io/papers/paper24
- Horvitz, Patel, Callison-Burch, Yu, McKeown (2023, Aug). ParaGuide. arXiv:2308.15459; AAAI 2024 [venue unverified]. https://arxiv.org/abs/2308.15459
- Horvitz, Patel, Singh, Callison-Burch, McKeown, Yu (2024, Jun). TinyStyler. Findings of EMNLP 2024. arXiv:2406.15586. https://arxiv.org/abs/2406.15586 ; https://arxiv.org/html/2406.15586 ; https://preview.aclanthology.org/watermark/2024.findings-emnlp.781 ; model https://huggingface.co/tinystyler/tinystyler
- Huerta-Enochian, Ko (2024). "Instruction Fine-Tuning: Does Prompt Loss Matter?" EMNLP 2024. arXiv:2401.13586. https://aclanthology.org/2024.emnlp-main.1267 ; https://arxiv.org/html/2401.13586v2
- Jangra et al. (2025, Aug; EMNLP 2026 main). "Evaluating Style-Personalized Text Generation: Challenges and Directions." arXiv:2508.06374. https://arxiv.org/html/2508.06374v4
- Jemama, Kumar (2025, Sep). "How Well Do LLMs Imitate Human Writing Style?" IEEE UEMCON 2025. arXiv:2509.24930. https://arxiv.org/abs/2509.24930 ; https://arxiv.org/html/2509.24930v1 ; code https://github.com/rajeshjnu2006/writing-style-uemcon2025
- Khan, Wang, Hager, Andrews (2023, Dec). "Learning to Generate Text in Arbitrary Writing Styles" (StyleMC). arXiv:2312.17242. https://arxiv.org/abs/2312.17242 ; https://arxiv.org/html/2312.17242
- Köksal, Schick, Korhonen, Schütze (2023, Apr). LongForm / Reverse Instructions. Findings of EMNLP 2024. arXiv:2304.08460. https://arxiv.org/pdf/2304.08460 ; ICLR 2024 listing https://www.iclr.cc/virtual/2024/22434
- Konen et al. (2024). Style Vectors. Findings of EACL 2024. arXiv:2402.01618. https://arxiv.org/abs/2402.01618 ; https://aclanthology.org/2024.findings-eacl.52
- Krishna, Wieting, Iyyer (2020, Oct). "Reformulating Unsupervised Style Transfer as Paraphrase Generation" (STRAP). EMNLP 2020. arXiv:2010.05700. https://arxiv.org/abs/2010.05700
- Kumar, Viswanathan, Yerra, Salemi, Rossi, Dernoncourt, Deilamsalehy, Chen (2024, Jul). LongLaMP. arXiv:2407.11016. https://arxiv.org/abs/2407.11016 ; https://arxiv.org/html/2407.11016
- Li et al. (2023, Aug). "Teach LLMs to Personalize." Google. arXiv:2308.07968. https://arxiv.org/abs/2308.07968
- Li et al. (2023, Aug). Humpback / Instruction Backtranslation; "Self-Alignment with Instruction Backtranslation" (title from reviewer's prior knowledge). Meta; ICLR 2024. arXiv:2308.06259. https://arxiv.org/abs/2308.06259
- Liu, Agarwal, May (2024, Mar; rev. Jul). "Authorship Style Transfer with Policy Optimization" (ASTRAPOP). USC ISI. arXiv:2403.08043. https://arxiv.org/abs/2403.08043 ; https://arxiv.org/html/2403.08043 ; https://arxiv.org/html/2403.08043v2 ; https://arxiv.org/pdf/2403.08043
- Liu, Agarwal, May (2024, Jun). STAMP. arXiv:2406.11581. https://web3.arxiv.org/pdf/2406.11581
- Liu, Bahja, Kovatchev, Lee (2025, Dec; CoNLL 2026). "Capturing Classic Authorial Style in Long-Form Story Generation with GRPO Fine-Tuning." arXiv:2512.05747. https://arxiv.org/abs/2512.05747 ; https://arxiv.org/html/2512.05747v2
- Liu, Diddee, Ippolito (2024, Sep). StyleTunedLM; "Customizing Large Language Model Generation Style using Parameter-Efficient Finetuning" (title from reviewer's prior knowledge). CMU; INLG 2024. arXiv:2409.04574. https://aclanthology.org/2024.inlg-main.34.pdf ; https://arxiv.org/html/2409.04574v1
- Liu et al. (2025, Feb). "A Survey of Personalized LLMs: Progress and Future Directions." arXiv:2502.11528. https://arxiv.org/abs/2502.11528
- Nguyen et al. (2024, Aug). "Instruction Back-and-Forth Translation." Findings of EMNLP 2024. arXiv:2408.04614. https://arxiv.org/abs/2408.04614 ; https://aclanthology.org/2024.findings-emnlp.777
- Nicolicioiu et al. (2024, Jul). Panza (fully local personalized email assistant). arXiv:2407.10994. https://arxiv.org/abs/2407.10994 ; https://arxiv.org/html/2407.10994
- Paech, Roush, Goldfeder, Shwartz-Ziv (2025, Oct). Antislop. ICLR 2026 poster. arXiv:2510.15061. https://arxiv.org/abs/2510.15061 ; https://arxiv.org/html/2510.15061 ; https://iclr.cc/virtual/2026/poster/10008156 ; code https://github.com/sam-paech/auto-antislop
- Patel, Andrews, Callison-Burch (2022, Dec). "Low-Resource Authorship Style Transfer: Can Non-Famous Authors Be Imitated?" (STYLL). arXiv:2212.08986. https://arxiv.org/abs/2212.08986
- Patel, Zhu, Qiu, Horvitz, Apidianaki, McKeown, Callison-Burch (2024, Oct). StyleDistance. NAACL 2025. arXiv:2410.12757. https://arxiv.org/abs/2410.12757 ; https://arxiv.org/html/2410.12757 ; model https://huggingface.co/StyleDistance/styledistance
- Qiu, Zhu, Patel, Apidianaki, Callison-Burch (2025, Feb). mStyleDistance. arXiv:2502.15168. https://arxiv.org/pdf/2502.15168 ; model https://huggingface.co/StyleDistance/mstyledistance
- Reinhart et al. (2025). "Do LLMs write like humans? Variation in grammatical and rhetorical styles." PNAS 122. arXiv:2410.16107. https://arxiv.org/abs/2410.16107
- Rivera-Soto et al. (2021). "Learning Universal Authorship Representations" (LUAR). EMNLP 2021. Models https://huggingface.co/rrivera1849/LUAR-MUD ; https://huggingface.co/rrivera1849/LUAR-CRUD ; https://huggingface.co/rrivera1849/LUAR-MUD-MV-Qwen ; LUSR (rrivera1849/LUSR) ; port https://huggingface.co/gabrielloiseau/LUAR-MUD-sentence-transformers ; code https://awesome.ecosyste.ms/projects/github.com%2Fllnl%2Fluar (github.com/llnl/luar)
- Salemi, Mysore, Bendersky, Zamani (2023, Apr). LaMP. arXiv:2304.11406; ACL 2024 [venue not verified in academic note]. https://arxiv.org/abs/2304.11406 ; https://preview.aclanthology.org/setup/2024.acl-long.399 ; review https://liner.com/review/lamp-when-large-language-models-meet-personalization [secondary]
- Salemi et al. (2025, Jan). REST-PG. Google. arXiv:2501.04167. https://arxiv.org/abs/2501.04167
- Salemi, Zamani (2024, Sep). "Comparing Retrieval-Augmentation and Parameter-Efficient Fine-Tuning for Privacy-Preserving Personalization of LLMs." arXiv:2409.09510. https://arxiv.org/abs/2409.09510 ; https://arxiv.org/html/2409.09510
- Shaikh et al. (2024, Jun; ICLR 2025). DITTO; "Show, Don't Tell: Aligning Language Models with Demonstrated Feedback" (title from reviewer's prior knowledge). arXiv:2406.00888. https://arxiv.org/html/2406.00888
- Shi et al. (2024, May). "Instruction Modelling." NeurIPS 2024. arXiv:2405.14394. https://arxiv.org/abs/2405.14394
- Song et al. (2026, Jan). CARD. arXiv:2601.06352. https://arxiv.org/abs/2601.06352
- Song et al. (2026, Jan). PsPLUG. arXiv:2601.06362. https://arxiv.org/abs/2601.06362
- Spohn, Girrbach, Akata (2026, May). APM. arXiv:2605.21063. https://arxiv.org/abs/2605.21063
- Sun, Yin, Xu, Kolter, Liu (2025, Feb). "Idiosyncrasies in Large Language Models." ICML 2025. arXiv:2502.12150. https://arxiv.org/abs/2502.12150
- Tan, Zeng, Tian, Liu, Yin, Jiang (2024, Feb). OPPU, "Democratizing LLMs via Personalized PEFT." EMNLP 2024. arXiv:2402.04401. https://arxiv.org/abs/2402.04401 ; https://arxiv.org/html/2402.04401 ; https://arxiv.org/pdf/2402.04401
- Tan, Liu, Jiang (2024, Jun). PER-PCS, "Personalized Pieces." EMNLP 2024. arXiv:2406.10471. https://arxiv.org/abs/2406.10471
- Wang, Tripto, Park, Li, Zhou (2025, Sep). "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors." Findings of EMNLP 2025. arXiv:2509.14543. https://arxiv.org/html/2509.14543v1 ; https://arxiv.org/abs/2509.14543v1 ; https://preview.aclanthology.org/dashboard/2025.findings-emnlp.532 ; code https://github.com/jaaack-wang/llms-implicit-writing-styles-imitation ; review https://www.themoonlight.io/en/review/catch-me-if-you-can-not-yet-llms-still-struggle-to-imitate-the-implicit-writing-styles-of-everyday-authors [secondary]
- Wegmann, Nguyen (2021). STEL framework. EMNLP 2021.
- Wegmann, Schraagen, Nguyen (2022, Apr). "Same Author or Just Same Topic? Towards Content-Independent Style Representations." RepL4NLP@ACL 2022. arXiv:2204.04907. https://arxiv.org/abs/2204.04907 ; https://www.arxiv.org/pdf/2204.04907 ; model https://huggingface.co/AnnaWegmann/Style-Embedding ; code github.com/nlpsoc/style-embeddings
- Zhang et al. (2024, Nov). "Personalization of LLMs: A Survey." TMLR. arXiv:2411.00027. https://arxiv.org/abs/2411.00027
- Zhang et al. (2025, Mar). StyleVector, "Personalized Text Generation with Contrastive Activation Steering." arXiv:2503.05213; ACL 2025 [venue unverified]. https://arxiv.org/abs/2503.05213
- ORPO (2024, Mar). arXiv:2403.07691. https://arxiv.org/abs/2403.07691 [not re-fetched]
- SimPO (2024, May). arXiv:2405.14734. https://arxiv.org/abs/2405.14734 [not re-fetched]
- KTO (2024, Feb). arXiv:2402.01306. https://arxiv.org/abs/2402.01306 [not re-fetched]
- arXiv:2601.18353 (2026, Jan). Blind pairwise expert vs lay study of LLM imitation of acclaimed authors. Title and authors unconfirmed; attributed by a search summary to Chakrabarty & Dhillon, CHI 2026 [unverified]. https://arxiv.org/html/2601.18353v1
- arXiv:2604.23178 (2026, Apr). LLM-judge stylistic bias study (markdown preference). https://arxiv.org/pdf/2604.23178
- arXiv:2308.09055 (2023, Aug). Formality-transfer evaluation; bidirectional NLI content score correlation. https://arxiv.org/pdf/2308.09055
- arXiv:2507.04889 (2025, Jul). Agent tone of voice: fine-tuning vs system prompting [unverified; search summary]. https://arxiv.org/pdf/2507.04889.pdf
- Ministral 3 technical report (2026, Jan). arXiv:2601.08584. https://arxiv.org/abs/2601.08584
- LMU Munich. "AI ghostwriter effect" (ACM TOCHI). https://www.lmu.de/en/newsroom/news-overview/news/who-wrote-it-the-ai-ghostwriter-effect-80ece661.html
- Abbasi, Chen (2008). Writeprints [not fetched]. LIWC-22 (used by Wang et al.). `stylo` R package (Eder, Rybicki, Kestemont) [not fetched].

### 17.2 Datasets, models and evaluation tools

- jondurbin (2024). gutenberg-dpo-v0.1. https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1
- nbeerbower. gutenberg2-dpo https://huggingface.co/datasets/nbeerbower/gutenberg2-dpo/blob/main/README.md ; gutenberg-moderne-dpo https://huggingface.co/datasets/nbeerbower/gutenberg-moderne-dpo/blob/main/README.md ; mistral-nemo-gutenberg3-12B https://huggingface.co/nbeerbower/mistral-nemo-gutenberg3-12B ; Qwen2.5-Gutenberg-Doppel-14B https://huggingface.co/nbeerbower/Qwen2.5-Gutenberg-Doppel-14B
- sam-paech (2024). Quill-v1. https://huggingface.co/sam-paech/Quill-v1
- ifable (2024). gemma-2-Ifable-9B. https://huggingface.co/ifable/gemma-2-Ifable-9B
- N8Programs (early 2026). Unslopper-GGUF card https://huggingface.co/N8Programs/Unslopper-GGUF/blob/main/README.md ; Reddit announcement snapshot (2026-01-15) https://reddit.sentinel-team.org/posts/1qd88v2/snapshots/2026-01-15T23%3A10%3A41.149982Z
- Oysiyl. qwen3-0.6b-unslop-good-lora-v1. https://featherless.ai/models/Oysiyl/qwen3-0.6b-unslop-good-lora-v1
- chartreuse-verte. prose-rewriter-1.7b-v2.4. https://featherless.ai/models/chartreuse-verte/prose-rewriter-1.7b-v2.4
- Fast Data Science. faststylometry. https://fastdatascience.com/fast-stylometry-python-library ; https://pypi.org/project/faststylometry
- sam-paech. slop-score. https://github.com/sam-paech/slop-score ; Go port SlopScoreTool https://pkg.go.dev/github.com/lemon07r/SlopScoreTool
- EQ-Bench Creative Writing v2. https://eqbench.com/creative_writing_v2.html
- Talon (Mailgun), AgentMail docs. https://docs.agentmail.to/talon-reply-extraction
- Unquote (NagaYu). https://github.com/NagaYu/unquote ; email-reply-extractor https://pypi.org/project/email-reply-extractor/
- Unsloth. LoRA hyperparameters guide (2025–26). https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide
- Schulman et al. (2025, Sep). "LoRA Without Regret." Thinking Machines. https://thinkingmachines.ai/blog/lora/ ; TRL replication https://huggingface.co/docs/trl/main/en/lora_without_regret
- apxml. QLoRA memory chapter. https://apxml.com/courses/designing-and-sizing-production-llm-infrastructure/chapter-5-fine-tuning-memory-mechanics/qlora-quantized-training

### 17.3 Practitioner write-ups, repos and forum threads

- Miller, Izzy (2023-04-10). "Replacing my best friends with an LLM trained on 500,000 group chat messages." https://www.izzy.co/blogs/robo-boys.html ; HN thread https://hn.algolia.com/api/v1/items/35540154
- Wang, Jeff (2023-04-19). "Automating Your Newsletters." https://jeffwang.substack.com/p/automating-your-newsletters
- Carmo, Duarte O. (2023-05-24). "Fine-tuning FLAN-T5 on my Telegram group chat." https://duarteocarmo.com/blog/fine-tune-flan-t5-telegram
- muttled (2023-07-21). Show HN: "I trained a 65B LLM on my texts to talk to myself." https://hn.algolia.com/api/v1/items/36815443
- Lazerowitz, Ross (2023-09-04). "Fine-tuning GPT3.5-turbo based on 140k slack messages." https://rosslazer.com/posts/fine-tuning
- Cselle, Gabor (2023-11-29). write-my-posts. https://github.com/gaborcselle/write-my-posts
- OpenAI Community (2023-01). "Fine tuning on someone's tweets to match their tone and writing style." https://community.openai.com/t/fine-tuning-on-someones-tweets-to-match-their-tone-and-writing-style/40213
- Stroet, Timo (2024-01-02). "Training an LLM on 150K Discord messages." https://gotimo2.github.io/posts/training-an-llm-on-150k-discord-messages
- Donner, Edward (2024-01-02). "A simulation of me: fine-tuning an LLM on 240k text messages." https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/ ; "Step by step guide: fine-tune an LLM on your texts (part 1)," snapshot 2024-04-23 https://web-clips.pages.dev/snapshots/Step%20by%20step%20guide_%20fine-tune%20an%20LLM%20on%20your%20texts%20(part%201)%20-%20Edward%20Donner%20-%20edwarddonner.com%20(2024-04-23T01_05_33.305Z).html
- Heralax_Tekran (2024-04-08). r/LocalLLaMA, "Trained an LLM on my own writings. Somewhat funny results." Mirror https://lr.us.psf.lt/r/LocalLLaMA/comments/1bzczyc/trained_an_llm_on_my_own_writings_somewhat_funny/kyp20tu/?context=3 [unverified] ; Augmentoolkit https://github.com/e-p-armstrong/augmentoolkit/
- Daigler, Michael (2024-05-04). "Making AI Write Like You." https://michaeldaigler.beehiiv.com/p/making-ai-write-like-fine-tuning-llama-3-newsletters-stepbystep-guide
- furiousteabag (Alex) (2024-06-13). "I fine-tuned an LLM with my Telegram chat history." https://hackernoon.com/i-fine-tuned-an-llm-with-my-telegram-chat-history-heres-what-i-learned ; code furiousteabag/doppelganger
- Rathod, Aditya (2024-08-18). "Training a bot on my own messages for fun and chaos." https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself
- grapeot (2024-12-23). "From Prompting to Fine-tuning: Making AI More Like 'Me'." https://yage.ai/finetuning-en.html
- BitsOfChris (2025-04-25). "I trained an AI to think like me." https://khoa-nguyen-bk18.github.io/brain/SecondBrain/I-trained-an-AI-to-think-like-me-—-here’s-what-happened
- Lopes, Didier (2025-09-02). "Fine-tuning an LLM on my blog posts." https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts
- Leary, Kevin (2025-09-18). "Creating Custom AI Models on a MacBook Pro." https://www.kevinleary.net/blog/custom-ai-models-macbook-pro/
- daehnhardt.com (2025-10-16). LoRA fine-tuning rules of thumb. https://daehnhardt.com/blog/2025/10/16/lora-fine-tuning-wins/ [unverified; search summary]
- zwischenzugs (2025-11-04). "Fine-tuning an AI, Part I." https://zwischenzugs.com/2025/11/04/fine-tuning-an-ai-part-i/
- Nottingham, Lydia (2025-11-20). "I fine-tuned Llama-3.1-70B on my blog." https://lydianottingham.substack.com/p/i-fine-tuned-llama-31-70b-on-my-blog ; https://github.com/LydNot/clone
- Reddit r/AI_Agents thread (~2025-11; snapshot 2026-05-08). https://reddit.sentinel-team.org/posts/1t6dkqw/snapshots/2026-05-08T19%3A17%3A52.632086Z
- Prevost, Jonathan (Feb 17, likely 2026). "I Built an AI Clone of Myself – Fine-Tuning with 10 Years of Data and Voice Cloning." https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60
- Courtyard, Show HN (2026-02-25). Open-source macOS app for local MLX fine-tuning. https://hn.algolia.com/api/v1/search?query=fine-tune%20MLX%20my&tags=story&hitsPerPage=30
- Larson, Shane (2026-03-13). "I Fine-Tuned a 7B Model on My Own Writing in One Evening." https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E
- Griffiths, Andrea (2026-03-17 update; dev.to 2026-03-24). "An Experiment in Voice: What Happens When AI Learns to Write Like You." https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na
- Lydon, Nic (May 9, likely 2026). "I trained an LLM on 75K of my own messages so it would stop writing like a chatbot." https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi
- Pandey, Shrestha (Jun 7, year not shown). "I fine-tuned Llama 3.2 on my own writing style using LoRA, Unsloth and a free Colab GPU." https://dev.to/shresthapandey/i-fine-tuned-llama-32-on-my-own-writing-style-using-lora-unsloth-and-a-free-colab-gpu-13l5
- scouttyg / eggbrain (2026-07-28). Writekin, Show HN https://hn.algolia.com/api/v1/items/49088436 ; https://github.com/scouttyg/writekin
- Deville, Nicolas (2026-09-20). NicAI voice-model (SLM) plan. https://notes.nicolasdeville.com/nicai/slm/
- meyerdav (2026-11-01). HN, "Can my fine-tuned model pass Pangram?" https://hn.algolia.com/api/v1/items/50324089
- codebyandy (n.d.). finetune-me. https://github.com/codebyandy/finetune-me
- ishan0102 (n.d.; likely early 2024). iClone. https://github.com/ishan0102/iClone
- gavi (n.d.). mlx-whatsapp. https://github.com/gavi/mlx-whatsapp
- xming521 (n.d.). WeClone. https://github.com/xming521/WeClone
- Modal Labs (n.d.). DoppelBot. https://github.com/modal-labs/doppel-bot ; third-party writeup https://starlog.pages.dev/articles/llm-engineering/jerryjliu-doppel-bot [unverified]
- Constantin, Sarah (date n/r). "Fine-tuning LLMs for style transfer." https://sarahconstantin.substack.com/p/fine-tuning-llms-for-style-transfer
- thatechmaestro (n.d.). "Replicate an author's writing style using prompt engineering." https://dev.to/thatechmaestro/replicate-an-authors-writing-style-using-prompt-engineering-insights-from-an-experiment-with-2hfk [unverified; search summary]
- blog-rgu (n.d.). Mistral Telegram persona. https://blog-rgu.pages.dev/blog/fine-tuning-mistral-telegram-persona [unverified; search snippet]
- Willison, Simon. Fine-tuning tag https://simonwillison.net/tags/fine-tuning/ ; Miller link (2023-04-12) https://simonwillison.net/2023/Apr/12/replacing-my-best-friends
- Sarah Chieng search result (Val Town, with Alex Phan). https://val.town/v/alexdphan/twitterSearch/references?view=list
- Eugene Yan search result. https://eugeneyan.com/speaking/writing-for-a-tech-career/
- ml-explore/mlx discussion #654, Community Projects. https://github.com/ml-explore/mlx/discussions/654
- Goekdeniz-Guelmez. MLX-LoRA-Studio. https://github.com/Goekdeniz-Guelmez/MLX-LoRA-Studio
- mac-playbooks. MLX LoRA playbook https://svah-x.github.io/mac-playbooks/playbooks/mlx-lora ; PyTorch MPS playbook https://svah-x.github.io/mac-playbooks/playbooks/pytorch-mps
- note.com. Mac fine-tune guide. https://note.com/best_ai_tools/n/n969312502825?hl=en
- passo.uno. Fine-tuning a docs LLM. https://passo.uno/fine-tuning-docs-llm/
- sciences44. mlx-lora-finetune. https://github.com/sciences44/mlx-lora-finetune

### 17.4 Commercial products

- Jasper (n.d.). Brand Voice. https://help.jasper.ai/hc/en-us/articles/18618693085339-Brand-Voice ; https://help.jasper.ai/hc/articles/18618693085339-Brand-Voice
- Grammarly / Superhuman (launched 2023-10). Voice features. https://support.grammarly.com/hc/en-us/articles/23153676821773-Introducing-voice-features ; https://help.superhuman.com/hc/en-us/articles/46242251232781-Introducing-voice-features ; TechCrunch (2023-10-25) https://techcrunch.com/2023/10/25/grammarlys-new-generative-ai-feature-learns-your-style-and-applies-it-to-any-text
- Writer (n.d.). Personal voice profile. https://support.writer.com/articles/4354376534-how-to-set-up-and-use-your-personal-voice-profile ; TechTarget https://www.techtarget.com/searchenterpriseai/news/366575533/Writer-Incs-new-AI-tool-generates-voice-of-marketers-content
- Hypotenuse AI (n.d.). Brand voice. https://hypotenuse.ai/features/brand-voice [vendor claim]
- Personal.ai (n.d.). PLM https://www.personal.ai/plm-personal-and-large-language-models ; PAI Academy https://www.personal.ai/pai-academy/chat-prompting-and-carrying-context-with-a-persona [vendor claim]
- Delphi via CO/AI (n.d.). Pinecone case study. https://getcoai.com/news/delphi-scales-ai-chatbots-to-100m-vectors-using-pinecone-database/
- Every (n.d.). Spiral 4.0 announcement (email link to every.to/on-every/spiral-4-0-goes-agent-native) https://every.to/emails/click/6c97bb0a1707598998fd8cfab915fb8cecd7c5507e895982b0a15fd991072efd/eyJzdWJqZWN0IjoiU3BpcmFsIDQuMCBHb2VzIEFnZW50LW5hdGl2ZSIsInBvc3RfaWQiOjQyODgsInBvc3RfdHlwZSI6InBvc3QiLCJ1cmwiOiJodHRwczovL2V2ZXJ5LnRvL29uLWV2ZXJ5L3NwaXJhbC00LTAtZ29lcy1hZ2VudC1uYXRpdmUiLCJwb3NpdGlvbiI6Mn0= ; help https://help.every.to/en/articles/13231409-why-don-t-the-drafts-match-my-writing-style [vendor claim]
- Anthropic (2024-11). Claude Styles. https://support.anthropic.com/en/articles/10181068-configuring-and-using-styles ; https://claude.com/blog/styles
- Rephrasy.ai: claim in the Reddit r/AI_Agents snapshot above [unsupported].

### 17.5 Apple silicon, training and serving tooling

- ml-explore. mlx-lm releases https://github.com/ml-explore/mlx-lm/releases ; LORA.md https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md ; lora.py https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/lora.py ; fuse.py https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/fuse.py ; SERVER.md https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md
- Goekdeniz-Guelmez. mlx-lm-lora. https://github.com/Goekdeniz-Guelmez/mlx-lm-lora ; https://pypi.org/project/mlx-lm-lora/ [self-reported benchmarks]
- ARahim3. mlx-tune (v0.6.0). https://github.com/ARahim3/mlx-tune
- mlxsmith 0.1.3 (alpha). https://pypi.org/project/mlxsmith/0.1.3/
- mlx-optiq. Fine-tuning docs. https://mlx-optiq.com/docs/finetune [self-reported]
- deadbydawn101. gemma-4-E4B-mlx-4bit model card. https://huggingface.co/deadbydawn101/gemma-4-E4B-mlx-4bit
- rainytechlab (DEV Community). "Fine-tune an LLM on your Mac with MLX QLoRA in 16 seconds." https://dev.to/rainytechlab/fine-tune-an-llm-on-your-mac-with-mlx-qlora-in-16-seconds-real-run-no-cloud-39ni
- HF forum. Gemma 4 E4B adapters fuse failure. https://discuss.huggingface.co/t/gemma4-e4b-adaptors-fuse-after-training-how/176429
- HF forum. Fine-tuning Qwen3.5-4B-Base on raw novel text. https://discuss.huggingface.co/t/how-should-i-fine-tune-qwen3-5-4b-base-on-raw-novel-text-without-a-chat-qa-format/179431
- InsiderLLM (updated 2026-11-04). Fine-tuning on Mac with LoRA and MLX. https://insiderllm.com/guides/fine-tuning-mac-lora-mlx/ [estimate]
- willitrunai (2026-04-20). Qwen 3.5 MLX Apple silicon guide. https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide [estimate]
- Unsloth. Requirements https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements ; Gemma 4 training guide https://unsloth.ai/docs/models/gemma-4/train ; PR #14457 https://github.com/unslothai/unsloth/pull/14457 ; issue #685 https://github.com/unslothai/unsloth/issues/685 [secondary comment]
- harshitkgupta (HF blog). PyTorch MPS vs MLX for fine-tuning on Mac. https://huggingface.co/blog/harshitkgupta/fine-tuning-coding-agents-on-mac-pytorch-mps-mlx [unverified; search summary]
- longform.social. PyTorch MPS + TRL pitfalls post. https://longform.social/post/did:plc:pgryn3ephfd2xgft23qokfzt/3mjg7wgy5dc22/source
- plawanrath (Medium). Fine-tuning Mistral-7B on Apple silicon with Axolotl LoRA. https://medium.com/@plawanrath/fine-tuning-mistral-7b-on-apple-silicon-a-mac-users-journey-with-axolotl-lora-c6ff53858e7d [not read]
- Apple. Foundation Models adapter training toolkit. https://developer.apple.com/apple-intelligence/foundation-models-adapter/
- Axiom. Foundation Models adapters reference. https://charleswiltgen.github.io/Axiom/reference/foundation-models-adapters-ref
- Apple WWDC25 session 298 (MLX). https://developer.apple.com/videos/play/wwdc2025/298/
- Apple WWDC26 sessions 324 "Meet Core AI" https://developer.apple.com/videos/play/wwdc2026/324/ ; 382 https://developer.apple.com/videos/play/wwdc2026/382/ ; 326 https://developer.apple.com/videos/play/wwdc2026/326/ ; 339 via https://wwdc.ai/2026/339
- ninetwothree. WWDC 2026 on-device AI. https://www.ninetwothree.co/blog/wwdc-2026-on-device-ai [unverified]
- Artificial Analysis. Qwen3.5 small models. https://artificialanalysis.ai/es/articles/qwen3-5-small-models ; NYU Shanghai RITS https://rits.shanghai.nyu.edu/ai/qwen-3-5-small-models-9b-parameters-that-beat-120b
- devshiva. Qwen3.5-4B-Base README mirror. https://huggingface.co/devshiva/Qwen3.5-4B-Base/blob/main/README.md
- Google. Gemma releases. https://ai.google.dev/gemma/docs/releases ; emelia.io Gemma 4 guide https://emelia.io/hub/gemma-4-open-source-guide ; Notebookcheck https://www.notebookcheck.net/Gemma-4-on-Hugging-Face-Google-s-Easter-surprise-for-download.1265198.0.html [secondary]
- eWeek. Mistral 3 launch. https://www.eweek.com/news/mistral-3-launch/
- AllenAI. Olmo-3-1025-7B. https://huggingface.co/allenai/Olmo-3-1025-7B
- LM Studio 0.3.33. https://lmstudio.ai/blog/lmstudio-v0.3.33
- PromptQuorum. Best local LLM for creative writing https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing [low reliability] ; LM Studio advanced features (KO, Apr 2026) https://www.promptquorum.com/ko/local-llms/lm-studio-advanced-features
- ggml-org. llama.cpp Apple silicon benchmark discussion #4167 https://github.com/ggml-org/llama.cpp/discussions/4167 ; server README https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md ; issue #10374 https://github.com/ggml-org/llama.cpp/issues/10374
- Ollama. MLX blog (2026-03-30) https://ollama.com/blog/mlx ; releases (v0.40.15, 2026-11-03) https://github.com/ollama/ollama/releases ; Modelfile docs https://ollama.readthedocs.io/en/modelfile ; import docs https://docs.ollama.com/import.md
- yage.ai (2026-03-31). MLX on Apple silicon. https://yage.ai/share/mlx-apple-silicon-en-20260331.html ; gingter.org (2026-04-23) https://gingter.org/2026/04/23/ollama-goes-mlx/
- Ex0bit. export_to_lms.py. https://huggingface.co/Ex0bit/jit-lora/blob/main/src/export_to_lms.py
- ExLLM. LM Studio provider docs. https://hexdocs.pm/ex_llm/ExLLM.Providers.LMStudio.html
- john-rocky. apple-silicon-llm-bench. https://github.com/john-rocky/apple-silicon-llm-bench
- llmcheck. Qwen 3 8B on M4 Pro. https://llmcheck.net/models/qwen-3-8b-on-m4-pro/ [estimate]

### 17.6 MCP and Claude Code

- Model Context Protocol. "Build a server" (2026-07-28 spec revision). https://modelcontextprotocol.io/docs/develop/build-server
- Anthropic. Claude Code MCP docs. https://code.claude.com/docs/en/mcp
- Glama. custom-mcp (Dev00355). https://glama.ai/mcp/servers/@Dev00355/custom-mcp
- mcpmarket. ollama-claude. https://mcpmarket.com/server/ollama-claude
- playbooks. Ollama MCP server. https://playbooks.com/mcp/newaiteesollama
