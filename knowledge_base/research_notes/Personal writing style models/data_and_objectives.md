# Data-Construction Recipes and Training Objectives for Personal-Style Small LLMs (50k-1M word personal corpus, LoRA on 4B-14B, Apple M4 Pro 24 GB)

Research date: 2026-11-07. Each source is dated by its arXiv, publication or page date. "Inference" bullets are my reasoning from the cited findings, not claims made by the sources.

## 1. Style inversion / back-translation data (neutral or outline input mapped to the person's original text)

### Takeaway
"Paraphrase inversion" is the main recipe in the authorship-style-transfer literature. You neutralize real target-style text with a paraphraser, then train a model to reconstruct the original. STRAP (2020), TinyStyler (2024) and ASTRAPOP (2024) all use it, and the same idea powers Gutenberg-DPO prompts and the 2026 "Unslopper" reverse-AI-ification rewriter. Measured results show small specialized models (800M-7B) trained this way can match or beat GPT-4 prompting on authorship-transfer joint scores, though they preserve meaning less well. I found no study that directly compares input forms (neutral paraphrase vs bullet outline vs generic LLM draft).

### Cited Findings
- **STRAP (Krishna, Wieting, Iyyer; EMNLP 2020, arXiv Oct 2020).** Recasts unsupervised style transfer as paraphrase generation. Pretrained LMs are fine-tuned on automatically generated paraphrase data, so the "inverse paraphraser" learns neutral text -> style. Introduces a ~15M-sentence, 11-style dataset (CDS). Reports it "significantly outperforms" prior systems on human and automatic evals, and argues existing automatic style-transfer metrics are easily gamed. — [arXiv 2010.05700](https://arxiv.org/abs/2010.05700)
- **TinyStyler (Horvitz et al., Columbia/Penn; arXiv Jun 2024, EMNLP 2024 Findings) recipe:**
  - Pegasus paraphraser (`tuner007/pegasus_paraphrase`, top-p 0.80, temperature 1.5) neutralizes Reddit comments; ~88M comments from the Million User Dataset, <=60 tokens each.
  - A T5-Large v1.1 (~800M) reconstructs the original, conditioned on a 768-d Wegmann et al. style embedding prepended to the input. Training: LR 1e-5, batch 16 x grad-accum 4, 230k steps.
  - Few-shot conditioning mean-pools the target author's embeddings; evaluation uses 16 target samples per author.
  - Synthetic pairs then go through a filter: drop outputs identical to the input or with hallucinated links, keep MIS and SimCSE >= 0.7, Away < 0.9, Towards < 0.30, and pick the best by geometric mean. This leaves ~40k high-quality pairs, which are used for self-distillation so no paraphraser is needed at inference. — [arXiv 2406.15586](https://arxiv.org/html/2406.15586)
- **TinyStyler results.**
  - Authorship-transfer joint score (Random / Single / Diverse): GPT-4 0.33/0.31/0.30; GPT-3.5 0.35/0.41/0.37; TinyStyler 0.40/0.45/0.36; TinyStyler + rerank(5) 0.43/0.48/0.39.
  - GPT-4 keeps meaning better: Sim 0.71 vs 0.59 on the Random split.
  - Speed: 0.47 s per example vs 1.56 s for GPT-4.
  - Model is public at huggingface.co/tinystyler/tinystyler. — [arXiv 2406.15586](https://arxiv.org/html/2406.15586)
- **ASTRAPOP (Liu, Agarwal, May, USC ISI; arXiv Mar 2024, rev. Jul 2024).**
  - Neutral inputs come from a LLaMA paraphraser fine-tuned on GPT-3.5-turbo paraphrases. It scored 0.764 SBERT vs 0.738 for GPT-3.5-turbo itself.
  - SFT on pseudo-parallel neutral -> target pairs ("following STRAP") uses LLaMA-2-7B base with LoRA r=16, alpha=32, dropout 0.05 on q_proj/v_proj.
  - Low-resource individual-author task: Reddit MUD, 2 texts per author for training, 16 per author for evaluation, 5 exemplars at inference.
  - Plain SFT joint 0.484 vs STRAP 0.414 vs STYLL-GPT-3.5 0.370. — [arXiv 2403.08043](https://arxiv.org/html/2403.08043v2)
- **N8Programs "Unslopper-30B-A3B" (early 2026).**
  - A Qwen3-VL-30B-A3B-Instruct fine-tune trained on ~1,000 `unslop-good` examples to "reverse the AI-ification process". Training pairs are human Project Gutenberg passages and AI-rewritten versions of them.
  - On 100 GPT-5.2 short stories, rewrites were rated 30% AI / 45% mixed / 25% human vs 99% AI for the untuned control. Quality score dropped slightly.
  - The author warns of local coherence problems and recommends using it inside a larger pipeline. Commenters doubted ~1k examples was enough. — [Unslopper GGUF model card](https://huggingface.co/N8Programs/Unslopper-GGUF/blob/main/README.md); [Reddit announcement snapshot, Jan 2026](https://reddit.sentinel-team.org/posts/1qd88v2/snapshots/2026-01-15T23%3A10%3A41.149982Z)
- **Smaller derivatives exist.** A Qwen3-0.6B LoRA trained on the same `unslop-good` data (a "pilot project"), and chartreuse-verte prose-rewriter 1.7B models (fiction-focused, not instruction-tuned). — [Featherless: qwen3-0.6b-unslop-good-lora-v1](https://featherless.ai/models/Oysiyl/qwen3-0.6b-unslop-good-lora-v1); [Featherless: prose-rewriter-1.7b](https://featherless.ai/models/chartreuse-verte/prose-rewriter-1.7b-v2.4)
- **Gutenberg-DPO (jondurbin, 2024) uses "summary/prompt" input rather than paraphrase.** Books were split into chapters with `chapterize`. An LLM wrote a synthetic prompt plus a summary for each chapter, and later chapters' prompts include the previous chapter's summary. 918 rows, 16 books, cc-by-4.0. — [HF dataset card](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1)
- **Content-summary + exemplars is a standard prompting baseline in recent style-imitation evaluation.** It works well on email (GPT-4o 5-shot top-5 attribution 59.65% vs 28.62% zero-shot on Enron) and poorly on blogs/Reddit (verification ~17-21%). — [Wang et al., arXiv 2509.14543, Sep 2025; EMNLP 2025 Findings](https://arxiv.org/html/2509.14543)

### Inferences
- For a personal corpus, the reproducible recipe is: for each cleaned unit (one email body, one doc section, one post), have a strong LLM produce a style-neutral version, then train `neutral -> original` with a LoRA on a 4B-14B instruct model. TinyStyler's similarity/novelty filter and best-of-N reranking carry over directly.
- Input form trade-off (reasoning, not measured head-to-head):
  - *Neutral paraphrase*: highest content alignment, so it best teaches surface style (lexical, punctuation, rhythm). Risks teaching "copy and lightly edit".
  - *Bullet outline*: teaches structure and expansion choices too, but the model must invent connective content, which raises hallucination risk.
  - *Generic LLM draft of the same content*: matches the deployment input in the "frontier drafts, local model restyles" pipeline (Q7), and Unslopper shows it works for de-AI-ification.
  - Training on a mix of all three (with a tag saying which) is low-cost. It likely makes the model robust to whichever input arrives at inference.
- The neutralizer should be a different model family from the one that will draft at deployment, or the training inputs should be diversified. Otherwise the rewriter may learn quirks of one drafter.

### Gaps
- No paper found that compares paraphrase vs outline vs generic-draft inputs for reconstructing one person's style. This is worth an internal ablation.
- TinyStyler/ASTRAPOP evaluate on short Reddit comments (<=60 tokens). Results on long emails/docs are not established.
- The Unslopper model card itself (HF, 30B) returned HTTP 401. Exact data construction (which model "AI-ified" the passages) was not verified beyond the GGUF card and Reddit post.

## 2. Synthetic instruction pairs ("plausible request -> my real text")

### Takeaway
Reverse instructions / instruction backtranslation, where an LLM writes the instruction that would have produced a human-written text, is a well-validated way to turn unlabeled human text into SFT data: LongForm, Humpback and Back-and-Forth Translation. The main pitfalls are poor-quality or misaligned pairs (hence self-curation), prompts that under-specify content (the model learns to hallucinate specifics in your voice), and the wrong lesson from Back-and-Forth. That paper improves generic assistant quality by rewriting the human response, which would destroy the personal style you want to keep.

### Cited Findings
- **Humpback / Instruction Backtranslation (Li et al., Meta; arXiv Aug 2023, ICLR 2024).** A seed-finetuned model generates instructions for web documents (self-augmentation), then scores and keeps only high-quality pairs (self-curation). Two iterations on LLaMa "outperform all other LLaMa-based models on the Alpaca leaderboard" without distillation data. — [arXiv 2308.06259](https://arxiv.org/abs/2308.06259)
- **LongForm / Reverse Instructions (Köksal, Schick, Korhonen, Schütze; arXiv Apr 2023, EMNLP 2024 Findings).** LLM-generated instructions for human-written C4/Wikipedia passages. LongForm-OPT-2.7B beat OPT-30B on long text generation, and Reverse Instructions beat prior models by >35% across text-generation tasks. Human-written outputs are credited with beating noisy Self-Instruct-style synthetic data. — [arXiv 2304.08460](https://arxiv.org/pdf/2304.08460); [ICLR 2024 listing](https://www.iclr.cc/virtual/2024/22434)
- **Instruction Back-and-Forth Translation (Nguyen et al.; arXiv Aug 2024, EMNLP 2024 Findings).** After backtranslating instructions for Dolma documents, Llama-2-70B-chat rewrites each response to look like an AI-assistant answer. This gives +3.6% AlpacaEval win rate over prior backtranslation data at equal volume, and rewriting beats distillation. — [arXiv 2408.04614](https://arxiv.org/abs/2408.04614); [ACL Anthology](https://aclanthology.org/2024.findings-emnlp.777)
- **StyleTunedLM eval prompts (Liu, Diddee, Ippolito, CMU; INLG 2024).** 50 prompts were GPT-4-generated and 50 were built from the first 6-8 words of held-out sentences. This is a practical template for building a held-out style test set. — [ACL Anthology PDF](https://aclanthology.org/2024.inlg-main.34.pdf)
- **Practitioner failure mode (codebyandy/finetune-me, Qwen3-4B on iMessage + Slack).** "The model will sound like you while saying plausible nonsense." Style transfers well; knowledge and beliefs do not. — [GitHub README](https://github.com/codebyandy/finetune-me)
- **Practitioner email fine-tune (zwischenzugs, Nov 2025).** Qwen2.5-3B-Instruct trained on own Gmail Sent folder via LLaMA-Factory. The fine-tuned model wrote "Hey, how are you? I was thinking of going out for a drink..." and signed with the author's name, while the base model produced "Subject: Exciting Plans for Our Drink Date! Dear [Friend's Name]". It also hallucinated a spurious date. — [zwischenzugs blog](https://zwischenzugs.com/2025/11/04/fine-tuning-an-ai-part-i/)
- **Gutenberg-DPO prompts include the previous chapter's summary** as context, so each target is reachable from the prompt rather than invented. — [HF dataset card](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1)

### Inferences
- For each personal text, generate an instruction that contains the facts the text contains: recipient, purpose, key points, any numbers or dates. For replies, include the thread context. If the instruction lacks the facts, the model learns to invent names, dates and commitments in your voice. That is the "plausible nonsense" and "spurious date" failure.
- Do Humpback-style curation. Have an LLM judge score whether the instruction plausibly elicits the text, and drop low-scoring pairs, near-duplicates and boilerplate.
- Vary instruction phrasing (terse and detailed, imperative and conversational) so the model doesn't overfit to one prompt template. Generating 2-3 instructions per text is a cheap form of data augmentation on a small corpus. This is my reasoning, not measured.
- Never rewrite the response side, which is the Back-and-Forth step. The person's text must be the target verbatim, after cleaning.

### Gaps
- No quantitative study found of instruction-quality effects specifically for single-person style SFT (vs generic assistant quality).
- Humpback's seed size, corpus details and curation ablations were not verified from the full paper in this session.

## 3. Continued pretraining on raw text vs instruction-format SFT; mixing general data; prompt masking

### Takeaway
The best measured evidence for small personal corpora is StyleTunedLM. It did raw next-token LoRA on a base model, then merged in an instruction adapter to restore instruction following. Style fidelity improved sharply with corpus size, and ~80k tokens per author was needed for strong results. LoRA itself is a forgetting regularizer ("learns less, forgets less"). Prompt-loss masking matters mainly for short completions. For long personal texts it is nearly irrelevant, while low-data/short-output regimes can benefit from some loss on prompts.

### Cited Findings
- **StyleTunedLM (INLG 2024, Sep 2024).**
  - LoRA on Llama-2-7B base, unstructured author text, next-token objective; books chunked into 256 tokens. LR 5e-5, 3 epochs, batch 4 per GPU, max length 256, 2x A6000.
  - Beat 5-shot, 10-shot and Llama-2-chat "instruct" prompting: classifier accuracy 0.879 vs 0.693 / 0.680 / 0.263; lexical MSE 1.39 vs 3.80 / 3.31 / 2.67.
  - Average held-out perplexity reduction was 7.0%. — [ACL Anthology PDF](https://aclanthology.org/2024.inlg-main.34.pdf)
- **StyleTunedLM data-size ablation (of ~80k tokens; 3 epochs).**

  | Share of 80k tokens | Cosine | Classifier acc | Lexical MSE |
  |---|---|---|---|
  | 5% | 0.57 | 0.11 | 6.04 |
  | 35% | 0.74 | 0.44 | 3.49 |
  | 70% | 0.92 | 0.81 | 1.44 |
  | 100% | 0.95 | 0.88 | 1.39 |

  The paper cites Eder (2015): 5,000-10,000 words are needed for stable authorship attribution. The authors target writers with "1k-50k tokens of prior work". — [ACL Anthology PDF](https://aclanthology.org/2024.inlg-main.34.pdf)
- **StyleTunedLM restored instruction following by merging** the style LoRA with a LIMA-trained LoRA (concatenating A vertically and B horizontally).
  - Style vs general-ability trade-off (Virginia Woolf : LIMA mixing ratio): cosine 0.57 (0:1), 0.59 (0.8:1), 0.64 (0.9:1), 0.70 (1:1).
  - The merge is reported to maintain benchmark performance. — [ACL Anthology PDF](https://aclanthology.org/2024.inlg-main.34.pdf)
- **StyleTunedLM named-entity loss masking.** Name tokens (spaCy) get label -100, so the model learns style rather than content names. For Wodehouse, masking cut names copied from training from 50% to 23%, with minimal style loss (cosine 1.0 -> 0.98). — [ACL Anthology PDF](https://aclanthology.org/2024.inlg-main.34.pdf)
- **"LoRA Learns Less and Forgets Less" (Biderman et al.; arXiv May 2024, TMLR 2024).** LoRA underperforms full fine-tuning on target-domain code/math but better preserves out-of-domain performance. It regularizes more than weight decay or dropout and keeps generations more diverse. — [arXiv 2405.09673](https://arxiv.org/abs/2405.09673)
- **Instruction Modelling (Shi et al., NeurIPS 2024).** Applying loss to instruction and prompt tokens improves results, most when instructions are long and outputs short, or in low-data settings. Best case: over 100% relative gain on AlpacaEval 1.0, attributed to reduced overfitting. — [arXiv 2405.14394](https://arxiv.org/abs/2405.14394)
- **"Instruction Fine-Tuning: Does Prompt Loss Matter?" (Huerta-Enochian & Ko, EMNLP 2024).** Prompt-loss weight matters for short-completion data, where a small PLW of 0.01-0.5 is best. Prompt masking "can be safely ignored" for medium and long completions. — [ACL Anthology](https://aclanthology.org/2024.emnlp-main.1267); [arXiv 2401.13586](https://arxiv.org/html/2401.13586v2)
- **Unsloth guide (2025-26).** "Train on completions only" can improve accuracy "by a few points", especially for multi-turn chat (`train_on_responses_only`). — [Unsloth LoRA hyperparameters guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- **mlx-lm prompt masking.** `--mask-prompt` computes loss only on the completion, for `chat` and `completions` formats; the last chat message is the completion. — [mlx-lm LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

### Inferences
- Recommended two-stage pattern on a Mac:
  - **(a)** Optional short raw-text "voice" pass on the cleaned corpus: completions or text format, 256-1024-token chunks, 1-2 epochs.
  - **(b)** Instruction-format SFT on synthetic-instruction and inversion pairs (Q1/Q2), on an instruct base so it stays useful.
  - This mirrors StyleTunedLM's "style adapter + instruction adapter" result without needing a separate LIMA LoRA. Alternatively, follow StyleTunedLM literally: train a style LoRA on base text and merge it with a general instruct adapter.
- To guard against capability loss, mix ~10-30% general instruction data (e.g., a small open instruct set or self-distilled responses from the same base model). Also run a quick held-out instruction-following/MMLU spot check before and after. The ratio is my heuristic; StyleTunedLM's merge-ratio table shows the style vs instruction trade-off is real and tunable.
- Prompt masking: for long emails/docs, mask or don't, since per Huerta-Enochian it barely matters. For short Slack replies with long thread context, mask the context (or use a small PLW). Otherwise the model spends capacity modeling other people's messages.

### Gaps
- No controlled study found comparing raw-text CPT vs instruction SFT vs both for one person's style at 50k-1M words on modern 4B-14B instruct models.
- No measured "optimal general-data mixing ratio" for personal-style SFT was found.

## 4. Preference optimization for style (chosen = person's real text, rejected = generic LLM version)

### Takeaway
"Human original = chosen, LLM-generated version of the same content = rejected" is the established construction of the Gutenberg DPO family, used by hundreds of community creative-writing models (ORPO/SimPO). The only controlled measurement of PO for individual-author style is ASTRAPOP: DPO/CPO on top of SFT raised the authorship joint score (0.484 -> ~0.505) and toward-target style, but cost some meaning preservation. The Antislop paper adds a warning that DPO can degrade writing quality and diversity when pushed. Use PO as a light second stage after SFT, prefer reference-free ORPO/SimPO on 24 GB, and keep learning rates very low.

### Cited Findings
- **Gutenberg-DPO v0.1 (jondurbin, 2024).** Chosen = original human chapter. Rejected = chapter written by an LLM (llama-2-13b-chat, bagel-7b, dolphin-2.2-34b) from the same synthetic prompt plus the previous-chapter summary. 918 rows; HF lists 462 models using it. — [HF dataset card](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1)
- **nbeerbower derivatives** (gutenberg2-dpo, gutenberg-moderne-dpo; rejected text from Mahou-1.5-mistral-nemo) and models trained on them. Mostly ORPO, e.g., mistral-nemo-gutenberg3-12B "ORPO tuned with 8x A100 for 2 epochs" and Qwen2.5-Gutenberg-Doppel-14B "ORPO tuned with 4x A40 for 3 epochs". — [gutenberg2-dpo card](https://huggingface.co/datasets/nbeerbower/gutenberg2-dpo/blob/main/README.md); [gutenberg-moderne-dpo card](https://huggingface.co/datasets/nbeerbower/gutenberg-moderne-dpo/blob/main/README.md); [mistral-nemo-gutenberg3-12B](https://huggingface.co/nbeerbower/mistral-nemo-gutenberg3-12B); [Qwen2.5-Gutenberg-Doppel-14B](https://huggingface.co/nbeerbower/Qwen2.5-Gutenberg-Doppel-14B)
- **sam-paech Quill-v1 (gemma-2-9b-it; 2024).**
  - Trained with ORPO ("gently") then SimPO ("less gently") on Gutenberg3: 629 public-domain novels. Chosen = Gutenberg passage. Rejected = gemma-2-9b-it's own generation from a description of the passage, explicitly to "steer the model away from its default style".
  - EQ-Bench creative writing 79.75. No base-model comparison on the card. — [HF model card](https://huggingface.co/sam-paech/Quill-v1)
- **Self-generated rejects.** Using the base model's own output as "rejected" (Quill) targets that model's default style specifically. That is the closest analogue to "my real email vs what this model would write". — [HF model card](https://huggingface.co/sam-paech/Quill-v1)
- **ifable/gemma-2-Ifable-9B.** SimPO on jondurbin/gutenberg-dpo-v0.1 plus a proprietary creative set; the card reports #1 on EQ-Bench Creative Writing on 2024-09-10. This is a self-reported ranking, not a controlled ablation. — [HF model card](https://huggingface.co/ifable/gemma-2-Ifable-9B)
- **ASTRAPOP (2024), controlled SFT vs PO for individual authors, LLaMA-2-7B LoRA.**

  | Method | Toward | Away | SBERT | Joint |
  |---|---|---|---|---|
  | SFT | 0.137 | 0.707 | 0.754 | 0.484 |
  | +PPO | 0.147 | 0.773 | 0.729 | 0.495 |
  | +DPO | 0.164 | 0.748 | 0.733 | 0.507 |
  | +CPO | 0.165 | 0.752 | 0.726 | 0.505 |

  DPO and CPO ~= each other and beat PPO. Meaning similarity fell because "our reward function does not take semantic similarity into account". The reward for individual authors is LUAR authorship similarity. ASTRAPOP-CPO uniquely reproduced idiosyncrasies (the typo "alot", all-lowercase, space before commas). — [arXiv 2403.08043](https://arxiv.org/html/2403.08043v2); [ASTRAPOP search summary of results](https://arxiv.org/pdf/2403.08043)
- **STAMP (same authors, arXiv Jun 2024)** extends this with multi-iteration preference optimization. — [arXiv 2406.11581](https://web3.arxiv.org/pdf/2406.11581)
- **Antislop (Paech et al.; arXiv Oct 2025, ICLR 2026 poster).** On identical preference pairs (gemma-3-12b, banned-pattern suppression):

  | Method | Writing quality | Lexical diversity | MMLU |
  |---|---|---|---|
  | Baseline | 67.80 | 100 | 0.590 |
  | DPO 2k | 62.98 | 91.03 | 0.541 |
  | DPO 8k | 54.61 | 73.92 | 0.571 |
  | FTPO 2k | 68.93 | 101.05 | 0.559 |
  | FTPO 8k | 67.49 | 95.09 | 0.592 |

  DPO "logits diverge unconstrained as training continues". FTPO (token-level preference with MSE tethers to reference logits) suppressed up to 92% of patterns with minimal quality loss. — [arXiv 2510.15061](https://arxiv.org/html/2510.15061)
- **Learning rates.** Unsloth recommends ~5e-6 for DPO/GRPO-type methods vs ~2e-4 for SFT LoRA. — [Unsloth guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- **COPE ("Personalized LLM Decoding via Contrasting Personal Preference").** Reportedly uses DPO with synthetic generic negatives chosen by distance from the user's historical style, plus contrastive decoding. Only a secondary summary was seen. — [Lacuna summary](https://lacuna.tiptreesystems.com/work/personalized-llm-decoding-via-contrasting-personal-preference/wrk_e267a8ec1d52eec496d307e0912d76a4)
- **Algorithm references (not re-fetched this session).** ORPO is reference-model-free and folds an odds-ratio penalty into SFT; SimPO is reference-free with a length-normalized reward; KTO uses unpaired good/bad labels. — [ORPO arXiv 2403.07691](https://arxiv.org/abs/2403.07691); [SimPO arXiv 2405.14734](https://arxiv.org/abs/2405.14734); [KTO arXiv 2402.01306](https://arxiv.org/abs/2402.01306)

### Inferences
- Personal-corpus recipe:
  - **(1)** SFT first (Q1-Q3).
  - **(2)** For a held-out slice, build pairs: prompt = the synthetic instruction or neutral input; chosen = the person's real text; rejected = the SFT'd model's own output, or the base instruct model's output, or a frontier model's output for the same prompt.
  - **(3)** Run ORPO/SimPO/DPO at LR ~5e-7 to 5e-6 for ~1 epoch.
  - Self-generated rejects (Quill-style) are most targeted, because they penalize exactly what this model still does wrong.
- Because chosen and rejected share content but differ in style, the preference signal is mostly stylistic. That is the point, but it can also reward content drift if rejected texts omit facts. Add a meaning-preservation term or filter (semantic-similarity floor between chosen and rejected) to avoid ASTRAPOP's SBERT drop.
- Memory on 24 GB: DPO needs a reference policy. With LoRA the reference can be the adapter-disabled base, but it still does extra forward passes on 2 sequences per example. ORPO/SimPO are reference-free and lighter. Paired sequences double activation memory, so cap sequence length (e.g., 1024) and use batch 1 + grad accumulation. On a 14B model, PO is likely only feasible with QLoRA (4-bit). This is reasoning based on algorithm structure.
- Expect a modest gain over SFT: ASTRAPOP saw ~+5% relative joint and +20% relative "toward" score. It is not a step change, and over-training risks the quality/diversity collapse Antislop measured for DPO.

### Gaps
- No public controlled before/after numbers found for nbeerbower Gutenberg ORPO models vs their bases on EQ-Bench. Quill and Ifable report absolute scores or rankings only.
- No paper found that does DPO with "one specific person's real emails/docs as chosen vs LLM rewrite as rejected" and measures it. ASTRAPOP is the closest (Reddit authors, LUAR reward).
- No verified source on MLX-native DPO/ORPO support. mlx-lm core docs list only lora/dora/full SFT. Third-party MLX preference-training packages exist, but none were verified here.

## 5. Inference-time techniques that complement fine-tuning

### Takeaway
The best-documented complements are retrieval of the person's own past writing as in-context examples, and phrase/regex banning with the Antislop sampler or FTPO. Evidence suggests per-user LoRA and retrieval are complementary (OPPU). One counterintuitive finding: choosing few-shot examples by topic similarity hurt style attribution relative to random examples. Logit-space n-gram injection and activation steering give weaker, less reliable style control than LoRA or prompting.

### Cited Findings
- **OPPU (Tan et al., EMNLP 2024).** One PEFT module per user plus retrieval and profile: "integrating non-parametric and parametric knowledge performs the best". Reported gains include 17.38% relative MAE improvement on LaMP-3 and +3.42% ROUGE-1 on scholarly title generation. OPPU outperforms retrieval-only under user behavior shift. — [arXiv 2402.04401](https://arxiv.org/pdf/2402.04401)
- **LaMP benchmark (Salemi et al.; arXiv Apr 2023, ACL 2024).** Retrieval-augmented personalization from user profiles (BM25, Contriever, time-aware). A secondary summary reports ~23.5% improvement for fine-tuned and 12.2% for zero-shot models; this was not verified against the paper. — [LaMP (ACL 2024)](https://preview.aclanthology.org/setup/2024.acl-long.399); [Liner review](https://liner.com/review/lamp-when-large-language-models-meet-personalization)
- **Wang et al. 2025 ("Catch Me If You Can? Not Yet").**
  - Going from 2 to 10 examples changes imitation metrics only slightly.
  - Selecting examples by topic similarity "generally hurt attribution, sharply on Blog and Enron".
  - Adding an opening snippet of the target text most increased "human" classification rates (roughly doubled on Reddit/Blog).
  - Most prompted outputs stayed detectable as AI: GPTZero human rates below 55%, often under 20%. — [arXiv 2509.14543](https://arxiv.org/html/2509.14543)
- **Antislop sampler (sam-paech; arXiv Oct 2025).**
  - Finds over-represented patterns by frequency ratio vs human baselines (wordfreq; Reddit creative writing + Gutenberg n-grams), e.g., "elara" 85,513x.
  - On a banned match, it backtracks to the pattern's first token, multiplies its probability by 10^(-10s) and resamples. It handles 8,000 patterns; plain token banning "becomes unusable at just 2,000". Regex bans fully suppressed "It's not X, it's Y".
  - Cost: throughput falls 69% at a 1,000-pattern list and up to 96% at 8,000 (worst case), so the authors prefer FTPO fine-tuning for production.
  - Code: github.com/sam-paech/auto-antislop (MIT). — [arXiv 2510.15061](https://arxiv.org/html/2510.15061)
- **n-gram logit-space style injection (Ahmed; arXiv Jan 2026; TinyLlama-1.1B).**
  - Works only in a narrow low-lambda window (lambda=0.1 on a single-author corpus: style perplexity -24.7%) and collapses fluency at higher lambda.
  - "Consistently outperformed by prompting and LoRA". LoRA (r=8, alpha=16, LR 2e-4, 800 steps) was "the most reliable and effective method overall". Caveat: not like-for-like comparisons. — [arXiv 2601.16224](https://arxiv.org/html/2601.16224)
- **Style Vectors (Konen et al., DLR; EACL 2024 Findings).** Steering vectors computed from activations of target-style texts are added to hidden layers (e.g., LLaMA layers 18-20) at generation time, giving "nuanced, parameterisable" style control without training. Quantitative writing-style results were not retrieved. — [ACL Anthology 2024.findings-eacl.52](https://aclanthology.org/2024.findings-eacl.52); [arXiv 2402.01618](https://arxiv.org/abs/2402.01618)
- **PRELUDE/CIPHER (Gao et al., Microsoft; NeurIPS 2024).** Learns a textual preference description from the user's edits to agent drafts and retrieves preferences from the k closest past contexts. Lowest edit-distance cost in simulated email-writing/summarization tasks, with no fine-tuning. — [arXiv 2404.15269](https://doi.org/10.48550/arXiv.2404.15269); [MSR page](https://www.microsoft.com/en-us/research/publication/aligning-llm-agents-by-learning-latent-preference-from-user-edits/)

### Inferences
- Retrieval: retrieve by register/genre and recipient (same channel, same recipient type, similar length) rather than pure topic similarity. Wang et al. found topic-matched exemplars hurt style matching, plausibly because they invite content copying. Use topic retrieval only for facts/content grounding (OPPU/LaMP-style), kept separate from the style exemplars.
- Build a personal antislop list. Compute n-gram frequency ratios of the model's outputs vs the person's own corpus, not generic human text, and ban the top over-represented phrases (e.g., "I hope this email finds you well", "delve"). Use the Antislop sampler for a few hundred patterns, or llama.cpp logit bias for single tokens. The 69%+ throughput cost at 1k patterns suggests keeping lists short on a laptop.
- Activation steering is a research option on a Mac (needs hooking MLX/PyTorch layers). Evidence that it beats a LoRA for a single person's idiolect is lacking.

### Gaps
- No measured comparison of retrieval-by-register vs retrieval-by-topic for a fine-tuned personal-style model.
- No head-to-head of style vectors vs LoRA for individual (non-celebrity) authors.
- LaMP headline numbers are second-hand.

## 6. Hyperparameter guidance for small-data style LoRA (and 24 GB M4 Pro feasibility)

### Takeaway
Consensus defaults:
- LoRA on all linear layers (attention + MLP), rank 16-32, alpha = rank to 2x rank.
- LR ~1e-4 to 2e-4 for SFT LoRA (~5e-6 or lower for preference stages), 1-3 epochs.
- Small effective batch (8-16); early stopping on held-out loss. Training loss below ~0.2 signals memorization.
- 256-1024-token chunks.

On 24 GB unified memory, LoRA on 4B-8B fits comfortably and 14B needs QLoRA (4-bit) with short sequences. Full-precision LoRA on 14B is likely over budget.

### Cited Findings
- **"LoRA Without Regret" (Schulman et al., Thinking Machines, Sep 2025).**
  - "Even in small data settings, LoRA performs better when applied to all weight matrices, especially MLP and MoE layers". Attention-only LoRA underperforms even at matched parameter count.
  - Optimal LoRA LR is ~10x the full-FT LR and approximately rank-independent (due to 1/r scaling). Low ranks fall off the full-FT curve after a step count that correlates with rank (capacity).
  - LoRA is less tolerant of large batch sizes. — [Thinking Machines blog](https://thinkingmachines.ai/blog/lora/); [HF TRL replication docs](https://huggingface.co/docs/trl/main/en/lora_without_regret)
- **Unsloth guide.**
  - r 16 or 32; alpha = r or 2r; dropout 0 (up to 0.1 if overfitting).
  - Targets q/k/v/o/gate/up/down; LR 2e-4 (SFT), ~5e-6 (DPO/GRPO); 1-3 epochs ("beyond 3 ... overfitting risk").
  - Batch 2 x grad-accum 8; weight decay 0.01-0.1; warmup 5-10%; linear or cosine schedule.
  - Overfitting if training loss < ~0.2. Fixes: lower LR/epochs, more decay/dropout, early stop on eval loss, or halve alpha at inference. — [Unsloth guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- **Published personal/author configs.**
  - StyleTunedLM: LR 5e-5, 3 epochs, 256-token chunks, Llama-2-7B. — [INLG 2024](https://aclanthology.org/2024.inlg-main.34.pdf)
  - ASTRAPOP: r=16, alpha=32, dropout 0.05, q/v only. — [arXiv 2403.08043](https://arxiv.org/html/2403.08043v2)
  - codebyandy/finetune-me (Apple Silicon, mlx-lm): Qwen3-4B-8bit, rank 16, LR 1e-4, 1000 iters, max_seq_length 1024, batch 4 "safe for 16 GB", roughly 1-2 h on an M1. — [GitHub](https://github.com/codebyandy/finetune-me)
- **mlx-lm.** QLoRA is used automatically when `--model` is a quantized model. Default `--num-layers 16` (number of top layers adapted), batch 4. Memory levers: `--grad-checkpoint`, smaller batch + `--grad-accumulation-steps`, fewer layers, shorter sequences. Fuse with `mlx_lm.fuse`; `--export-gguf` only for Llama/Mistral-style models. — [mlx-lm LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- **Memory estimates (third-party guides, not measured on M4 Pro).** Llama-3.1-8B ~14 GB LoRA / ~7 GB QLoRA. Qwen2.5-14B ~24 GB LoRA / ~12 GB QLoRA (the same guide elsewhere says 14-18 GB for 14B LoRA, an internal inconsistency). The guide advises QLoRA for 14B on a 32 GB Mac. Activations scale with batch x sequence length. — [insiderllm MLX guide](https://insiderllm.com/guides/fine-tuning-mac-lora-mlx/); [apxml QLoRA memory chapter](https://apxml.com/courses/designing-and-sizing-production-llm-infrastructure/chapter-5-fine-tuning-memory-mechanics/qlora-quantized-training)
- **Data quantity.** StyleTunedLM found 4k tokens (5%) and 28k tokens (35%) inadequate and 56k-80k tokens strong (see Q3 table). — [INLG 2024](https://aclanthology.org/2024.inlg-main.34.pdf)
- **Few-shot alternative.** Prompting with exemplars saturates quickly (2 -> 10 examples changes little). — [arXiv 2509.14543](https://arxiv.org/html/2509.14543)

### Inferences
- Starting config for 50k-1M words (~65k-1.3M tokens) on an M4 Pro 24 GB with mlx-lm:
  - Qwen3-8B or similar at 4-bit (QLoRA), or bf16 for <=4B models.
  - LoRA on all linear layers and all (or the top 16-24) layers; rank 16 (32 for >500k words); alpha/scale ~2x rank.
  - LR 1e-4; 1-2 epochs for >300k words, 2-3 for <100k words; batch 1-2 with grad accumulation to 8-16.
  - max_seq_length 1024-2048 with `--grad-checkpoint`; hold out 5-10% for validation loss and a style classifier eval.
  - 14B at 4-bit is feasible but slower and tighter; keep sequences <=1024.
- Chunking long docs: split on paragraph or section boundaries into 256-1024-token chunks, keep the doc title or section header as context, and avoid splitting mid-sentence. For emails, one email body = one example (most are under 1k tokens).
- Dedup aggressively. Exact and near-duplicates (MinHash/Jaccard), template emails, repeated signatures and repeated Slack bot messages over-weight boilerplate and drive memorization (training loss < 0.2). Tooling was not separately verified this session.
- Without loss masking, the model will learn to emit names and other PII. StyleTunedLM's NER loss masking (label -100) is a cheap mitigation for names. Combine with regex/NER scrubbing of emails, phones and addresses before training (see Q8).

### Gaps
- No measured peak-memory numbers found specifically for M4 Pro 24 GB with Qwen3-8B/14B QLoRA. A short probe run is needed.
- No study found optimizing rank/epochs specifically for 50k-1M word single-author corpora on modern instruct models.

## 7. Architecture "frontier model drafts content, small local model rewrites in the person's voice"

### Takeaway
There is indirect but consistent evidence for splitting content and voice. A small specialized restyler (TinyStyler 800M; ASTRAPOP 7B) beats GPT-4/3.5 prompting on authorship-style transfer, while GPT-4 keeps meaning better. Combining the two plays to each one's strength, but no paper directly measures "Claude draft + local style rewriter" against either alone. Known risks are meaning drift (lower similarity scores for style-optimized rewriters), hallucinated specifics, residual AI traces surviving rewriting, and local coherence breaks. Mitigations come from the same literature: best-of-N reranking with semantic-similarity and style scores, similarity thresholds, and fact/entity preservation checks.

### Cited Findings
- **Small restyler vs frontier prompting.** TinyStyler + rerank(5) joint 0.43-0.48 vs GPT-4 0.30-0.33, but GPT-4 Sim 0.71 vs TinyStyler 0.59 on the Random split. On formality transfer, GPT-4 still leads overall (joint 0.85 vs 0.76-0.78). — [arXiv 2406.15586](https://arxiv.org/html/2406.15586)
- **Preference optimization trades meaning for style.** ASTRAPOP PO raises style scores while SBERT falls from 0.754 (SFT) to 0.726-0.733, because the reward ignores semantics. — [arXiv 2403.08043](https://arxiv.org/html/2403.08043v2)
- **Human post-editing of LLM drafts (Baumler et al., UMD; arXiv Apr 2026, pre-registered, n=81).**
  - Post-editing moved text toward the author's own style (g=0.55) and away from LLM text (g=-0.41), but post-edited text stayed much closer to LLM text than to the author's unassisted writing (g=-1.43). It was more homogeneous across people than unassisted writing (g=1.42).
  - Perceived self-similarity correlated only weakly with embedding similarity (r=0.244).
  - Participants corrected factual content in ~31% of drafts.
  - 58/81 preferred post-editing to writing alone. — [arXiv 2604.24444](https://arxiv.org/html/2604.24444v1)
- **Unslopper (rewriting AI drafts toward human prose).** AI-detection rating went from 99% AI to 30% AI, quality dropped slightly, and there were "local coherence problems". The author advises using it in a larger pipeline. — [Unslopper GGUF card](https://huggingface.co/N8Programs/Unslopper-GGUF/blob/main/README.md); [Reddit snapshot](https://reddit.sentinel-team.org/posts/1qd88v2/snapshots/2026-01-15T23%3A10%3A41.149982Z)
- **Content quality from small style models.** "The model will sound like you while saying plausible nonsense". The README recommends tuning for voice and supplying facts via prompts/retrieval. — [codebyandy/finetune-me](https://github.com/codebyandy/finetune-me)
- **Generic drafts are the top objection.** Generic or unoriginal drafts were the most cited reason to avoid an LLM-draft workflow, so draft quality matters as much as restyling. — [arXiv 2604.24444](https://arxiv.org/html/2604.24444v1)
- **Mitigations from the literature.**
  - TinyStyler's filter (drop outputs with hallucinated links; require SimCSE and MIS meaning similarity >= 0.7) plus best-of-5 reranking by geometric mean of style and similarity scores. — [arXiv 2406.15586](https://arxiv.org/html/2406.15586)
  - CIPHER-style learning from the user's edits to the final output. — [arXiv 2404.15269](https://doi.org/10.48550/arXiv.2404.15269)

### Inferences
- Pipeline sketch:
  1. The frontier model produces a content-complete draft or a structured outline (facts, asks, dates, recipients).
  2. The local LoRA restyler, trained on Q1 inversion data with generic-LLM-draft inputs, rewrites it.
  3. Sample N=3-5 candidates.
  4. Score each for meaning (embedding similarity or NLI entailment both ways vs the draft), entity/number preservation (every named entity, number, date and URL in the draft must appear in the output, and no new ones), and style (a classifier or LUAR-style embedding trained on the person's corpus).
  5. Return the best, or fall back to the draft and flag it if none pass.
  6. Optionally the frontier model acts as a verifier ("does B say anything not in A?").
- Train the restyler on generic-draft inputs so training matches deployment. Because the "neutral" side is an LLM draft, residual-AI-trace removal is learned explicitly, which addresses the post-editing study's finding that traces persist.
- Keep the restyler's freedom bounded. Use a low temperature for rewriting; consider rewriting paragraph by paragraph for long docs to limit coherence breaks (Unslopper warning). Expose a "style strength" knob: TinyStyler's embedding interpolation, alpha scaling of the LoRA, or blending draft and rewrite.

### Gaps
- No controlled study found comparing (a) frontier-only with style prompt + exemplars, (b) local fine-tuned model alone, and (c) frontier draft -> local restyle, on one person's real email/doc corpus. This needs an internal eval (blind pairwise "which is mine?" judgments plus fact-preservation checks).
- No measured hallucination-introduction rates for LoRA restylers on long-form text were found.

## 8. Data hygiene: quoted replies, signatures, forwards, code, register separation and control tags

### Takeaway
Email cleaning is the dominant data-quality risk. Off-the-shelf reply/quote strippers (Talon, email-reply-parser) are imperfect, with measured recall below 50% on one third-party benchmark, so combine them with heuristics and spot checks. Practitioners use only Sent mail, condition on channel and recipient via a system-prompt tag, and keep prior turns as (masked) context. Name masking in the loss reduces content and PII memorization.

### Cited Findings
- **Use only your own sent mail.** Practitioners export Gmail via Google Takeout (.mbox) and use the "Sent" mail, since it contains your own writing. — [note.com Mac fine-tune guide](https://note.com/best_ai_tools/n/n969312502825?hl=en); [zwischenzugs blog, Nov 2025](https://zwischenzugs.com/2025/11/04/fine-tuning-an-ai-part-i/)
- **Talon (Mailgun)** provides `quotations.extract_from_plain` / HTML quote removal and `extract_signature`. It sometimes keeps reply headers and quoted lines, and gets confused by signatures placed before quotes; it does detect Outlook separators and From/Sent headers. — [AgentMail Talon docs](https://docs.agentmail.to/talon-reply-extraction)
- **email-reply-parser** (Zapier port of GitHub's parser) is plain-text only and faster (~0.03 ms). The Unquote project's benchmark on 4,000 real reply pairs reports Talon P 0.592 / R 0.455 and email-reply-parser P 0.719 / R 0.367. Unquote is a competing model-based tool, so it is an interested party. Rules that assume quoted lines start with ">" fail often, especially outside English. — [Unquote GitHub](https://github.com/NagaYu/unquote); [email-reply-extractor PyPI](https://pypi.org/project/email-reply-extractor/)
- **Register/recipient conditioning in practice.**
  - System prompt "You are Andy. You are messaging {contact} in {channel}", with the last 6 turns as context and your reply as the assistant target; the same tag is used at inference.
  - Data from iMessage `chat.db` and the Slack API; `build_dataset.py` "filters noise".
  - The README warns that the data contains other people's messages: train locally and don't publish adapters. — [codebyandy/finetune-me](https://github.com/codebyandy/finetune-me)
- **Entity loss masking.** StyleTunedLM sets labels to -100 on spaCy-detected names, which halves name copying from training (Wodehouse 50% -> 23%) with minimal style cost. The authors note effectiveness depends on NER accuracy. — [INLG 2024](https://aclanthology.org/2024.inlg-main.34.pdf)
- **Thread context as masked prompt.** With `--mask-prompt`, the final chat message is the completion, so earlier turns (other people's messages, quoted thread) are context only. — [mlx-lm LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- **Register effects on imitation difficulty.** Imitation is much easier for structured registers (email, news: ~95-97% verification) than informal ones (blogs/forums: ~17-21% with 5 shots). This is a reason to separate and tag registers. — [arXiv 2509.14543](https://arxiv.org/html/2509.14543)

### Inferences
- Cleaning pipeline (order matters):
  1. Parse MIME; prefer text/plain, else HTML -> text.
  2. Drop auto-replies, calendar invites, newsletters and pure forwards ("---------- Forwarded message").
  3. Strip quoted history: Talon/email-reply-parser, then regex for "On <date>, <name> wrote:", "From: ... Sent: ...", ">"-prefixed lines and Outlook "-----Original Message-----".
  4. Strip signatures and legal disclaimers. Learn your own signature block(s) by frequency and remove exact matches.
  5. Remove or replace code blocks, stack traces, tables and pasted logs with a placeholder token, since they are not your prose.
  6. Drop very short texts (< ~5 words, e.g., "thanks!") or down-sample them heavily.
  7. Near-dedup.
  8. Scrub PII: emails, phones, addresses, account numbers via regex/NER. Replace with typed placeholders like `<PERSON_1>` or `<EMAIL>` rather than deleting, so sentence rhythm survives.
  9. Keep other people's turns only as masked context.
- Register control: tag every example with `register={email_formal, email_casual, slack, doc, post}` and, if useful, `recipient_type={manager, peer, external, friend}` in the system prompt, as codebyandy does. Either train one adapter with tags (better data sharing when the corpus is small) or separate adapters per register when one register dominates and others get swamped. Balance or up-sample minority registers. At inference, the tag selects register; reuse the same tags in the retrieval filter (Q5).
- Time-weighting: if the corpus spans many years, consider down-weighting old writing, since style drifts. OPPU notes retrieval-only methods suffer under user behavior shift. This is reasoning, not tested.

### Gaps
- No peer-reviewed benchmark of email quote/signature stripping quality on modern (2024-26) mail clients was found. The only numbers come from an interested third party (Unquote).
- No study found that measures the effect of register control tags vs per-register adapters for one person's style.
- Specific PII-scrubbing tools (e.g., Microsoft Presidio) and dedup tools (MinHash/datasketch) were not researched in this session. Evaluate them separately.
