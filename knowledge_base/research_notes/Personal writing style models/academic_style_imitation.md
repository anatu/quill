# Academic Literature on Imitating One Individual's Writing Style (author-level style imitation, personalized generation, authorship style transfer)

Scope note: Current as of Nov 2026. Most figures below were checked against arXiv abstracts or the arXiv HTML full text during this session. Where a venue or number comes only from a search snippet or a secondary summary, the entry says so. arXiv IDs are given as `arXiv:XXXX.XXXXX`.

---

## 1. How well do frontier LLMs imitate a specific person's style via prompting alone?

### Takeaway
Prompting with a few of a person's samples gets partway there, and only in structured, formulaic genres (news, email). In informal genres (blogs, forums) it largely fails. Few-shot outputs remain detectable as AI and drift toward a generic "LLM voice" that persists across model sizes and is stronger in instruction-tuned models. Adding more in-context examples helps very little. The strongest evidence: expert readers strongly reject prompted imitations of literary authors but prefer fine-tuned ones.

### Cited Findings
**Wang, Tripto, Park, Li, Zhou: "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors"** (Findings of EMNLP 2025; arXiv:2509.14543)
- **Setup.** Over 40,000 generations per model, from more than 400 real authors, across four corpora: Enron emails (150 authors), Blog (100), CCAT50 news (50) and Reddit (100). Models tested: GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, Gemma-3-27B, DeepSeek-V3 and Llama-4-Maverick. The main setting is 5-shot with same-author demonstrations; the zero-shot baseline gets only a content summary plus genre. Evaluation is an ensemble of authorship attribution (AA), authorship verification (AV), style matching and AI detection — [arXiv HTML](https://arxiv.org/html/2509.14543v1); [ACL Anthology](https://preview.aclanthology.org/dashboard/2025.findings-emnlp.532)
- **Top-5 AA accuracy, GPT-4o, 5-shot vs 0-shot.** CCAT50 86.64 vs 83.88; Enron 59.65 vs 28.62; Reddit 27.12 vs 18.77; Blog 39.39 vs 17.22 — [arXiv HTML](https://arxiv.org/html/2509.14543v1)
- **AV pass rate, 5-shot.** News (CCAT50) 94.68–97.44% and Enron 95.65–96.64% across models. Reddit only 49.97% (DeepSeek-V3) to 65.88% (Gemini-2.0-Flash). Blog only 16.72% (Gemma-3-27B) to 21.25% (Gemini). Zero-shot Blog AV was 8.15–10.35% — [arXiv HTML](https://arxiv.org/html/2509.14543v1)
- **AI detection (share of generations GPTZero labeled "human", 5-shot).**
  - GPT-4o: Enron 16.86%, CCAT50 0.08%, Reddit 0.67%, Blog 0.47%.
  - Gemini-2.0-Flash: 18.74–54.25%.
  - Real human test texts: 99.2–100%.
  - The authors caution that GPTZero may be biased toward detecting GPT-family output — [arXiv HTML](https://arxiv.org/html/2509.14543v1)
- **More shots.** Varying demonstrations across 2/4/6/8/10 gave "limited gains" in stylistic alignment. The result is reported only as a figure — [arXiv HTML](https://arxiv.org/html/2509.14543v1)
- **Content-similar demonstrations hurt.** Choosing demonstrations that are content-similar to the target ("+Sim ctrl") lowered AA, averaged over three LLMs: Enron 69.33→36.00, Reddit 35.43→16.63, Blog 43.93→22.13. Length-matching lowered style accuracy on Reddit (71.80→56.60) — [arXiv HTML](https://arxiv.org/html/2509.14543v1)
- **Generic default.** The paper says outputs "often default to an average, generic tone." Code and data: github.com/jaaack-wang/llms-implicit-writing-styles-imitation — [arXiv HTML](https://arxiv.org/html/2509.14543v1)

**Chakrabarty, Ginsburg, Dhillon: "Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers"** (preprint under review, 2025; arXiv:2510.13939)
- **Design.** Preregistered. MFA-trained writers were compared with ChatGPT/GPT-4o, Claude 3.5 Sonnet and Gemini 1.5 Pro, writing excerpts of up to 450 words that emulate 50 award-winning authors. Judges were 28 MFA-trained readers and 516 college-educated readers — [arXiv](https://arxiv.org/abs/2510.13939)
- **In-context prompting (instructions plus few-shot examples) was strongly disfavored by MFA readers** for stylistic fidelity (OR=0.16) and quality (OR=0.13). General readers showed no fidelity preference (OR=1.06) — [arXiv](https://arxiv.org/abs/2510.13939)
- **Detection.** Pangram flagged 97% of in-context-prompted texts as AI. Among MFA readers, each unit of detector score reduced the odds of choosing an excerpt for fidelity by a factor of 6.3 — [arXiv HTML](https://arxiv.org/html/2510.13939)
- **Why prompting loses.** Experts appear to penalize "AI-ness": clichés, purple prose, too much exposition, lack of subtext, mixed metaphors. The authors conclude "models cannot emulate an author's style properly just by prompting" — [arXiv HTML](https://arxiv.org/html/2510.13939)

**Khan, Wang, Hager, Andrews: "Learning to Generate Text in Arbitrary Writing Styles" (StyleMC)** (arXiv:2312.17242, 2023)
- "Instruction-tuned language models can struggle to reproduce author-specific style demonstrated in a prompt" when the sample is a few hundred words. GPT-3.5 performed worse than its previous generations in this few-shot setting — [arXiv](https://arxiv.org/abs/2312.17242); [arXiv HTML](https://arxiv.org/html/2312.17242)
- Human writing "dips" into low-probability regions; LM samples pick likely tokens at each step — [arXiv HTML](https://arxiv.org/html/2312.17242)

**Shaikh et al.: DITTO** (ICLR 2025; arXiv:2406.00888)
- Framing: "Language models are aligned to emulate the collective voice of many, resulting in outputs that align with no one in particular." With demonstration-based alignment, DITTO beat few-shot prompting by 33.4 win-rate points on Mistral 7B and by 18 points against few-shot GPT-4. In the user study it beat user-written prompts by 27.9 points — [arXiv HTML](https://arxiv.org/html/2406.00888)

**Jemama & Kumar: "How Well Do LLMs Imitate Human Writing Style?"** (IEEE UEMCON 2025; arXiv:2509.24930)
- Five open models (Llama, Qwen, Mixtral) on academic essays. Prompting strategy mattered more than model size: few-shot gave up to 23.5× higher style-matching accuracy than zero-shot, and completion prompting reached 99.9% agreement with the author's style under the paper's own verifier.
- Matched outputs still had a mean perplexity of 15.2 vs 29.5 for human essays. Stylistic fidelity and statistical detectability are separable — [arXiv](https://arxiv.org/abs/2509.24930)
- This is a more optimistic result than Wang et al. It uses a custom TF-IDF plus embedding verifier and a single formal genre.

**"LLM voice" / homogenization evidence**
- **Reinhart et al., "Do LLMs write like humans? Variation in grammatical and rhetorical styles"** (PNAS 122, 2025; arXiv:2410.16107). Using Biber features on parallel corpora, Llama 3 variants and GPT-4o differ systematically from humans. The differences persist from small to large models and are larger for instruction-tuned models than base models — [arXiv](https://arxiv.org/abs/2410.16107)
- **Sun, Yin, Xu, Kolter, Liu, "Idiosyncrasies in Large Language Models"** (ICML 2025; arXiv:2502.12150). A fine-tuned embedding classifier identifies ChatGPT/Claude/Grok/Gemini/DeepSeek outputs with 97.1% accuracy in a five-way task. The idiosyncrasies persist even after text is rewritten, translated or summarized by another LLM, which implies they are also encoded in semantic content — [arXiv](https://arxiv.org/abs/2502.12150)
- **Spohn, Girrbach, Akata, "APM"** (arXiv:2605.21063, May 2026). "Typical LLM responses tend to follow a default style." For implicit style preferences on Llama-3.1-8B and Qwen-3.5-27B, routing was the most reliable personalization method, RAG improved only with the stronger base model, and soft-prompt optimization did not significantly beat a non-personalized baseline — [arXiv](https://arxiv.org/abs/2605.21063)

### Inferences
- Prompt-only imitation works best where the genre itself constrains style (news wires, business email). Those are exactly the settings where AV/AA tests are easiest to pass. Informal personal writing — closest to "my voice" — is where prompting fails worst (Blog AV around 17–21%).
- Collecting more in-context examples is not a reliable lever: there are flat returns beyond about 5 shots, and content-similar exemplars actively hurt. The residual "assistant voice" (Reinhart; Sun) looks like a property of instruction-tuned weights that prompting cannot override.
- The two most rigorous human-judged studies (Chakrabarty et al.; DITTO) agree that weight updates beat prompting for individual style, by large margins.

### Gaps
- No 2025–2026 study found that tests the newest frontier models (e.g., GPT-5-class, Claude 4.x, Gemini 2.5/3) on everyday-author imitation with the Wang et al. protocol. The latest models covered are GPT-4o, Gemini-2.0-Flash, DeepSeek-V3 and Llama-4-Maverick.
- Wang et al. did not test explicit style-description prompts (e.g., LLM-extracted style guides) against raw demonstrations. I found no controlled study isolating that variable for individual authors.

---

## 2. Personalization benchmarks and methods (LaMP, LongLaMP, OPPU, PER-PCS, RAG): what do they show about fine-tuning vs retrieval vs prompting?

### Takeaway
On LaMP-style benchmarks, retrieval-augmented prompting gives most of the gain cheaply. Per-user PEFT alone gives small average gains, but its gains grow with the amount of user data, and RAG+PEFT is best. These benchmarks mostly score short outputs (titles, headlines, tweets) with ROUGE, so they measure content and phrasing overlap more than voice. Studies that measure style directly (Panza; Chakrabarty) find that RAG alone "largely fail[s] to match a given user's writing style" while fine-tuning succeeds.

### Cited Findings
**Benchmarks**
- **LaMP** (Salemi, Mysore, Bendersky, Zamani; arXiv:2304.11406, 2023). Seven tasks (3 classification, 4 generation) with multiple profile entries per user. It introduced retrieval-augmented personalization (term matching, semantic and time-aware retrievers) and showed it helps — [arXiv](https://arxiv.org/abs/2304.11406). Venue: commonly cited as ACL 2024; not verified this session.
- **LongLaMP** (Kumar, Viswanathan, Yerra, Salemi, Rossi, Dernoncourt, Deilamsalehy, Chen; arXiv:2407.11016, 2024). Personalized long-form generation: emails, abstracts, reviews, topic writing. The RAG framework (BM25/Contriever over user documents) improved metrics by 5.7% to 128% over non-personalized baselines. Metrics are ROUGE-1 and ROUGE-L — [arXiv](https://arxiv.org/abs/2407.11016); [arXiv HTML](https://arxiv.org/html/2407.11016)
- **REST-PG** (Salemi et al., Google; arXiv:2501.04167, 2025). Trains LLMs to reason over the user's past preferences and writing style, then uses EM-style reinforced self-training. It gave an average 14.5% relative gain on LongLaMP — [arXiv](https://arxiv.org/abs/2501.04167)
- **Fine-grained linguistic control benchmark** (Alhafni, Kulkarni, Kumar, Raheja; arXiv:2402.04914, 2024). Personalization defined over lexical and syntactic attributes rather than coarse formality or sentiment — [arXiv](https://arxiv.org/abs/2402.04914)
- **Surveys.** Zhang et al., "Personalization of LLMs: A Survey" (TMLR; arXiv:2411.00027) — [arXiv](https://arxiv.org/abs/2411.00027). Liu et al., "A Survey of Personalized LLMs: Progress and Future Directions" (arXiv:2502.11528, 2025), with a prompting/adapter/alignment taxonomy — [arXiv](https://arxiv.org/abs/2502.11528)

**RAG vs PEFT head-to-head**
- **Salemi & Zamani, "Comparing Retrieval-Augmentation and Parameter-Efficient Fine-Tuning for Privacy-Preserving Personalization of LLMs"** (arXiv:2409.09510, 2024)
  - Across the seven LaMP datasets, RAG gave a 14.92% average improvement over non-personalized output, per-user LoRA (PEFT) gave 1.07%, and RAG+PEFT gave 15.98% — [arXiv](https://arxiv.org/abs/2409.09510)
  - PEFT helped on 5/7 datasets; RAG helped on all — [arXiv HTML](https://arxiv.org/html/2409.09510)
  - PEFT gains correlate positively with the number of profile items, while RAG gains correlate negatively, as retrieval struggles with large profiles. So RAG suits cold-start users and PEFT suits data-rich users — [arXiv HTML](https://arxiv.org/html/2409.09510)
  - PEFT gained most on LaMP-6 (personalized email subjects from the private Avocado corpus), i.e., data unlikely to be in pretraining — [arXiv HTML](https://arxiv.org/html/2409.09510)
  - Setup: FlanT5-XXL (11B), 512-token input and 128-token output, LoRA trained 50 epochs per user. They estimate about 200 MB per adapter, so about 20 PB for 100M users — [arXiv HTML](https://arxiv.org/html/2409.09510)

**Per-user PEFT methods**
- **OPPU, "Democratizing LLMs via Personalized PEFT"** (Tan, Zeng, Tian, Liu, Yin, Jiang; EMNLP 2024; arXiv:2402.04401)
  - One LoRA per user (about 0.5% of parameters) on top of a task-adapted base, combined with retrieval and profiles. It outperformed prompt-based methods on all seven LaMP tasks — [arXiv](https://arxiv.org/abs/2402.04401)
  - It was especially strong under user behavior shift, where retrieved history is less relevant, and was robust across activity levels and history formats. The main test set was the 100 most-active users — [arXiv HTML](https://arxiv.org/html/2402.04401)
- **PER-PCS, "Personalized Pieces"** (Tan, Liu, Jiang; EMNLP 2024; arXiv:2406.10471). Users share pieces of their PEFT modules, and target users assemble a personalized PEFT from a pool using their history. Performance is comparable to OPPU at significantly lower storage and compute — [arXiv](https://arxiv.org/abs/2406.10471)
- **CARD** (Song et al.; arXiv:2601.06352, Jan 2026). Clusters users by shared stylistic patterns and trains group LoRAs, then adds per-user preference vectors and low-rank logit corrections at decoding. It is motivated by per-user parameters being costly and unstable with sparse histories. Reports gains on LaMP and LongLaMP — [arXiv](https://arxiv.org/abs/2601.06352)
- **StyleVector, "Personalized Text Generation with Contrastive Activation Steering"** (Zhang et al.; arXiv:2503.05213, 2025). Training-free. It represents a user's style as an activation-space vector, explicitly to disentangle content from style. Reports an 8% relative improvement and 1700× less storage than PEFT — [arXiv](https://arxiv.org/abs/2503.05213). A search snippet suggested an ACL 2025 venue; not verified.

**Style-specific evidence that RAG alone is not enough**
- **Panza** (Nicolicioiu et al.; arXiv:2407.10994, 2024): "while base LLMs with RAG can provide coherent outputs, including personal information obtained via retrieval, they largely fail to match a given user's writing style." All fine-tuning variants beat Pretrained+RAG "by a large margin," and leading closed LLMs "yielded similarly poor results" — [arXiv HTML](https://arxiv.org/html/2407.10994)
- **Google, "Teach LLMs to Personalize"** (Li et al.; arXiv:2308.07968, 2023). A multistage retrieval → ranking → summarization → synthesis → generation pipeline improved over baselines on three datasets — [arXiv](https://arxiv.org/abs/2308.07968)

### Inferences
- The "RAG beats PEFT" headline from LaMP comes from short-output, ROUGE-scored tasks. There, retrieving topically relevant history directly raises n-gram overlap. On voice-focused tasks with style metrics (Panza's MAUVE; Chakrabarty's expert judgments), the ranking flips toward fine-tuning.
- Across studies, the most defensible design is hybrid: per-user weights for voice, retrieval for user-specific facts and phrasing.
- PEFT's benefit scales with per-user data volume (Salemi & Zamani), consistent with Panza's data ablation (Section 4).

### Gaps
- I did not obtain the per-task OPPU ROUGE numbers for the generation tasks (LaMP-4/5/7) in this session. Only the classification improvements were extracted (e.g., 17.38% MAE improvement on rating prediction).
- PersonaHub-style synthetic-persona work (e.g., "Scaling Synthetic Data Creation with 1,000,000,000 Personas") was not investigated. It targets synthetic persona diversity rather than imitating a real individual's style, so it is likely of low relevance.

---

## 3. Authorship style transfer methods (STRAP, STYLL, TinyStyler, ParaGuide, ASTRAPOP, StyleMC, steering): data requirements and results

### Takeaway
The dominant recipe is paraphrase-to-neutral, then reconstruct in the target style (STRAP, 2020). Per-author models need over 100k words. Low-resource variants (16 posts / ~500 words, or even 5 examples) condition a single universal model on authorship embeddings (TinyStyler, StyleMC) or apply policy optimization (ASTRAPOP). These beat prompted GPT-4 on automatic authorship metrics. Even so, absolute "move toward the target author" scores stay low, and every method trades style strength against meaning preservation.

### Cited Findings
**Paraphrase-and-reconstruct approaches**
- **STRAP: Krishna, Wieting, Iyyer, "Reformulating Unsupervised Style Transfer as Paraphrase Generation"** (EMNLP 2020; arXiv:2010.05700)
  - Method: paraphrase to strip style, then train an inverse paraphraser per target style.
  - It significantly outperformed prior systems on human and automatic evaluations and introduced a 15M-sentence corpus across 11 styles.
  - Surveying 23 papers, it found existing automatic style-transfer metrics "can be easily gamed" — [arXiv](https://arxiv.org/abs/2010.05700)
- **STYLL / low-resource AST: Patel, Andrews, Callison-Burch, "Low-Resource Authorship Style Transfer: Can Non-Famous Authors Be Imitated?"** (arXiv:2212.08986, 2022)
  - STRAP-like approaches need "often greater than 100,000 words" of target text, so they are mainly useful for famous authors.
  - The new task limits the target author to 16 Reddit posts (~500 words). An in-context-learning technique (STYLL) was the strongest baseline, but "current approaches do not yet achieve mastery."
  - It proposes automatic evaluation (Away/Towards/Sim/Joint) using authorship representation models — [arXiv](https://arxiv.org/abs/2212.08986)
- **TinyStyler: Horvitz, Patel, Singh, Callison-Burch, McKeown, Yu** (Findings of EMNLP 2024; arXiv:2406.15586)
  - An 800M-parameter T5 reconstructs text from a paraphrase plus a projected authorship (style) embedding. Target-author embeddings are mean-pooled over any number of examples. It was trained unsupervised on the Reddit Million User Dataset, then self-distilled on reranked synthetic pairs — [arXiv](https://arxiv.org/abs/2406.15586); [arXiv HTML](https://arxiv.org/html/2406.15586); [ACL Anthology](https://preview.aclanthology.org/watermark/2024.findings-emnlp.781)
  - Evaluation follows Patel et al.: 15 source × 15 target Reddit users with 16 samples each, i.e., 225 directions and 3,600 transformations per split (Random/Single/Diverse) — [arXiv HTML](https://arxiv.org/html/2406.15586)
  - Joint scores from Table 2 (Random / Single / Diverse) — [arXiv HTML](https://arxiv.org/html/2406.15586):

    | System | Joint (R / S / D) | Notes |
    |---|---|---|
    | GPT-4 | 0.33 / 0.31 / 0.30 | Sim 0.68–0.72 |
    | GPT-3.5 | 0.35 / 0.41 / 0.37 | |
    | Unsupervised TinyStyler | 0.32 / 0.37 / 0.28 | Strong Away/Towards; low Sim 0.31–0.44 |
    | ParaGuide variants | 0.22–0.27 | |

  - Distilled TinyStyler fixed meaning preservation. With reranking it "outperforms all methods on all evaluation sets" — [arXiv HTML](https://arxiv.org/html/2406.15586)
  - Towards scores (movement toward the target author's embedding) were at most about 0.16 for every system in Table 2, e.g., GPT-4 0.07–0.09 and TinyStyler about 0.13–0.15 — [arXiv HTML](https://arxiv.org/html/2406.15586)
  - The authors note TinyStyler can "personalize generic outputs from chat models to match a user's preferences" and flag impersonation risk — [arXiv HTML](https://arxiv.org/html/2406.15586)
- **ParaGuide: Horvitz, Patel, Callison-Burch, Yu, McKeown** (arXiv:2308.15459, 2023; venue usually cited as AAAI 2024, not verified this session). A paraphrase-conditioned diffusion model with gradient guidance from classifiers and style embedders, so the target style is specified at inference time. On the Enron email corpus it outperformed baselines on formality, sentiment and authorship transfer — [arXiv](https://arxiv.org/abs/2308.15459)
- **ASTRAPOP: Liu, Agarwal, May, "Authorship Style Transfer with Policy Optimization"** (arXiv:2403.08043, 2024)
  - Two stages: SFT, where neutral paraphrases (from GPT-3.5) are mapped back to the original, then policy optimization (PPO/DPO/CPO) directly on the Towards/Away objectives.
  - It works "with as few as five examples per author" and beats ICL and SFT alone.
  - It notes Patel et al. found SFT methods like STRAP do not outperform ICL at this data scale, and that a single exemplar-conditioned model beats one model per author in the extreme low-resource setting — [arXiv](https://arxiv.org/abs/2403.08043); [arXiv HTML](https://arxiv.org/html/2403.08043)

**Embedding-guided decoding and RL**
- **StyleMC** (Khan et al., arXiv:2312.17242). Uses contrastively trained stylometric representations (LUAR-style, trained on 1M Reddit users with ≥100 comments each) plus an author-adapted LM and MCMC sequence-level inference. Given a few hundred words of target text, it outperformed GPT-4 prompted with in-context demonstrations. Its zero-shot samples were harder to detect as machine-generated — [arXiv HTML](https://arxiv.org/html/2312.17242)
- **GRPO for classic authors: Liu, Bahja, Kovatchev, Lee, "Capturing Classic Authorial Style in Long-Form Story Generation with GRPO Fine-Tuning"** (CoNLL 2026; arXiv:2512.05747). Trains an AV-supervised style-similarity judge and uses it as the GRPO reward for an 8B generator. Average style score was 0.893 across Twain, Austen, Dickens and Hardy, above open-weight baselines — [arXiv](https://arxiv.org/abs/2512.05747)

**Steering and modular approaches (mostly coarse styles)**
- **STEER: Hallinan et al.** (arXiv:2311.07167, 2023). Expert-guided synthetic pairs plus offline-then-online RL for arbitrary-source → target-style transfer. It beat 175B GPT-3 while being 226× smaller — [arXiv](https://arxiv.org/abs/2311.07167)
- **Style vectors: Konen et al.** (Findings EACL 2024; arXiv:2402.01618). Steering vectors computed from activations for sentiment, emotion and writing style. Shown mainly on coarse styles — [arXiv](https://arxiv.org/abs/2402.01618)
- **StyleRemix: Fisher et al.** (arXiv:2408.15666, 2024). Pre-trained LoRA modules per fine-grained style axis (formality, length, etc.), used for authorship obfuscation. Released AuthorMix (30K texts, 14 authors) — [arXiv](https://arxiv.org/abs/2408.15666)

### Inferences
- Data requirements fall into three tiers: per-author inverse paraphraser at ≥100k words (STRAP); universal embedding-conditioned rewriter at 5–16 samples / ~500 words (TinyStyler, ASTRAPOP, STYLL); author-adapted fine-tuning at hundreds of samples or whole oeuvres (Sections 2 and 4).
- Low Towards scores mean that even state-of-the-art few-shot rewriters move text only a short distance toward a non-famous author in authorship-embedding space. "Beats GPT-4" is relative, not mastery.
- Many of these systems use authorship embeddings both as the training/guidance signal and as the evaluation metric. TinyStyler mitigates this by evaluating with a held-out embedding model, but metric gaming (as STRAP warned) remains a live risk.

### Gaps
- I found no human evaluation in which people who know the target author judge TinyStyler or ASTRAPOP outputs. Panza's acquaintance-based study (Section 4) is the closest analog, and it is for fine-tuning, not rewriting.
- I did not verify per-row STYLL numbers in TinyStyler's Table 2, because the parsed HTML lost the method labels for those rows.

---

## 4. How much data from one author does a LoRA or fine-tune need to capture style?

### Takeaway
Reported useful minimums range from fewer than 10 demonstrations (with preference optimization, DITTO) to about 25–100 emails (Panza: most of the gain by 25, BLEU saturating at 75–100). Whole-book oeuvres in GPT-4o fine-tuning showed no clear benefit from more tokens. A 2026 single-user case study with only 73 paragraphs and a rank-8 LoRA produced near-zero stylometric gain. The training objective (SFT vs preference/online imitation) matters as much as volume at the low end.

### Cited Findings
- **Panza** (arXiv:2407.10994)
  - Data ablation over seven users with RoSA adapters on Llama-3-8B-Instruct, normalized to full data. At 25 training emails, average BLEU was already at about 90% of maximum and MAUVE about 0.85. By about 75–100 emails, BLEU matched full-data models, while "MAUVE scores take longer to saturate" — [arXiv HTML](https://arxiv.org/html/2407.10994)
  - The paper states "as few as 50-100 emails suffice to make a convincing imitation of a person's writing style" and frames this as an attack vector. Typical full user data was "several hundred or thousand emails" — [arXiv HTML](https://arxiv.org/html/2407.10994)
  - Method comparison: RoSA (sparse plus low-rank) ≈ full fine-tuning > LoRA, especially on MAUVE, consistently across backbones and users. Fine-tuning was "highly sensitive to learning rate and the number of training epochs" — [arXiv HTML](https://arxiv.org/html/2407.10994)
  - Training data was built via a Reverse Instructions variant: an LLM writes the synthetic prompt that would yield each real email — [arXiv HTML](https://arxiv.org/html/2407.10994)
  - Human studies: acquaintances identified which of two people a Panza model imitated with about 64% precision/recall (chance 25%). Only 28–32% of Panza emails were judged suspicious by evaluators who knew the author — [arXiv HTML](https://arxiv.org/html/2407.10994)
- **DITTO** (ICLR 2025; arXiv:2406.00888)
  - Data: 7 training demonstrations per author (20 authors from the CMCC and CCAT50 authorship datasets).
  - Results: DITTO beat SFT by 11 win-rate points, SPIN by 20.2 and few-shot prompting by 33.4 on Mistral 7B. In a 16-person email user study it beat SFT by 12 and few-shot by 23.9.
  - Demonstrations were "an order of magnitude more sample-efficient" than pairwise preferences.
  - The paper notes SFT overfitting "problems that plague SFT in low-data regimes" — [arXiv HTML](https://arxiv.org/html/2406.00888)
- **Chakrabarty, Ginsburg, Dhillon** (arXiv:2510.13939)
  - GPT-4o was fine-tuned via the OpenAI API on each of 30 living authors' complete works, segmented into 250–650-word excerpts paired with GPT-4o-written content descriptions. Settings: 1 epoch for authors with large oeuvres (Atwood, Ishiguro, Rushdie, Murakami), 3 epochs otherwise, batch size 1, LR multiplier 2. One author had only two books — [arXiv HTML](https://arxiv.org/html/2510.13939)
  - Results: MFA readers favored the fine-tuned AI for fidelity (OR=8.16) and quality (OR=1.87); general readers favored it for fidelity (OR=16.65). 29 of 30 author models exceeded parity on fidelity (median win rate 0.83) — [arXiv](https://arxiv.org/abs/2510.13939); [arXiv HTML](https://arxiv.org/html/2510.13939)
  - Regressing AI preference on fine-tuning corpus size (millions of tokens) gave "near zero" slopes, i.e., "little association between corpus size (in this range) and AI preference" — [arXiv HTML](https://arxiv.org/html/2510.13939)
  - Cost: $25–$276 per author, median $81 — [arXiv HTML](https://arxiv.org/html/2510.13939)
- **Salemi & Zamani** (arXiv:2409.09510). Per-user LoRA gains correlate positively with profile size, and limited per-user data is identified as the key reason PEFT underperformed RAG on LaMP — [arXiv HTML](https://arxiv.org/html/2409.09510)
- **InMyStyle: Chakravorty, "Small Is Enough: Per-User Style Rewriting of AI-Edited Text via LoRA Adapters"** (arXiv:2607.29238, Jul 2026)
  - A single-user case study: rank-8, 3-epoch LoRAs on Qwen2.5 0.5B–7B, with 219 eval pairs from 73 paragraphs of one author's scientific writing.
  - The composite score plateaued across model sizes (Q=0.689–0.695). Authorship probabilities stayed near the decision boundary (0.51–0.53), and "stylometric improvement [was] near zero" — [arXiv](https://arxiv.org/abs/2607.29238)
- **Low-resource style transfer.** 16 posts (~500 words) is the standard benchmark budget (Patel et al.), and ASTRAPOP works with 5 examples per author. Both use a shared multi-author model conditioned on exemplars, not a per-author LoRA — [arXiv](https://arxiv.org/abs/2212.08986); [arXiv](https://arxiv.org/abs/2403.08043)

### Inferences
- For email-length personal text, about 100 samples (perhaps 10–30k words) appears to be the knee of the curve for SFT-style per-user adapters. Distribution-level style (MAUVE) keeps improving past the point where content/phrasing metrics saturate.
- At under about 10 samples, plain SFT overfits; preference-style objectives that contrast the user's text against the model's own outputs (DITTO) are the documented fix.
- Adapter type matters: RoSA and full fine-tuning beat vanilla LoRA on style metrics in Panza. Rank-8 LoRA on tiny data (InMyStyle) mostly "de-AI-ifies" text rather than personalizing it.
- Chakrabarty's flat corpus-size slope covers only book-length corpora, roughly two-book minimum. It does not show that small corpora suffice.

### Gaps
- I found no systematic scaling-law study (e.g., style fidelity vs. tokens or samples across many users, LoRA ranks and base-model sizes) for single-author style. Evidence is scattered ablations from different metrics and genres.
- Panza's figure-level per-size numbers (5/10/25/50/100 emails) were only partly recoverable from the HTML text; the exact sizes tested are in Figure 5.
- No study found compares per-user LoRA vs full fine-tuning for a frontier-scale model on the same single-author data with human judges.

---

## 5. Known failure modes: content leakage/memorization, topic overfitting, loss of instruction-following, mode collapse

### Takeaway
The documented risks are:
- **Topic and content leakage:** both the training signal and the evaluator can latch onto what an author writes about rather than how they write.
- **Verbatim regurgitation:** rare but real; papers handle it by resampling.
- **RAG-induced copying:** retrieved past texts get reused too aggressively.
- **SFT overfitting on tiny data.**
- **"Personalization collapse":** explicit style instructions override learned implicit style.

General capability loss appears small for PEFT on email (Panza). I found no direct study of "mode collapse to signature phrases."

### Cited Findings
**Topic/content confounds in style representations and evaluation**
- **Wegmann, Schraagen, Nguyen, "Same Author or Just Same Topic? Towards Content-Independent Style Representations"** (RepL4NLP@ACL 2022; arXiv:2204.04907). AV-trained style representations "might also encode content information instead of style alone." Controlling for conversation during training yields better content-independent style representations — [arXiv](https://arxiv.org/abs/2204.04907)
- **Patel et al., StyleDistance** (NAACL 2025; arXiv:2410.12757). Contrastive triplets for style embeddings risk "content leakage." The paper uses LLM-generated near-exact paraphrases varying 40 style features to train more content-independent embeddings — [arXiv](https://arxiv.org/abs/2410.12757)
- **Wang et al., "Catch Me If You Can? Not Yet"** (arXiv:2509.14543). Content-similar demonstrations reduced attribution, e.g., Enron AA 69.33→36.00 — [arXiv HTML](https://arxiv.org/html/2509.14543v1). Per a secondary search summary (not verified in full text), non-trivial zero-shot AA suggests topical overlap contributes to the authorship signal — [arXiv abs](https://arxiv.org/abs/2509.14543v1)
- **Liu et al., GRPO story generation** (CoNLL 2026; arXiv:2512.05747). According to a search-result summary of the HTML (not verified in full text), the paper notes token-level style distances are confounded by topic, and that "style imitation" can come from copying character names or setting elements from the target author's works — [arXiv HTML](https://arxiv.org/html/2512.05747v2)

**Memorization and copying**
- **Chakrabarty et al.** "In the rare occasion that a model regurgitated verbatim snippets/ngrams from original author written text we resampled it." The paper's Figure 19 reports low overall word overlap with the author's corpus. The SFT model also occasionally failed to include all requested content details, requiring resampling — [arXiv HTML](https://arxiv.org/html/2510.13939)
- **Panza.** Adding RAG at inference to a fine-tuned model lowered BLEU (content accuracy), likely from "re-using the RAG context too aggressively... emails that are very similar to past emails." Training with retrieval in the loop (RAFT) mitigated this — [arXiv HTML](https://arxiv.org/html/2407.10994)

**Overfitting and hyperparameter fragility**
- **DITTO.** SFT on few demonstrations has overfitting "problems that plague SFT in low-data regimes"; DITTO's replay and inter-checkpoint comparisons are designed to counter this — [arXiv HTML](https://arxiv.org/html/2406.00888)
- **Panza.** PEFT was "highly sensitive to learning rate and the number of training epochs" — [arXiv HTML](https://arxiv.org/html/2407.10994)

**Instruction-following and capability retention**
- **Panza.** Personalized models "retain over 98% of the performance of Llama-3-8B-Instruct" on the six-task Open LLM Leaderboard suite — [arXiv HTML](https://arxiv.org/html/2407.10994)
- **PsPLUG** (Song et al.; arXiv:2601.06362, Jan 2026). Identifies "personalization collapse": explicit style instructions (e.g., "be formal") can undermine the user-specific characteristics personalization methods preserve. It proposes a user-specific residual with tunable strength — [arXiv](https://arxiv.org/abs/2601.06362)

**Detectability as a failure mode**
- In-context outputs carry detectable AI quirks: 97% detected by Pangram. Mediation analysis shows fine-tuning removes the stylometric quirks that drive both detection and dispreference — [arXiv](https://arxiv.org/abs/2510.13939)
- High-fidelity imitations still have much lower perplexity than humans (15.2 vs 29.5) — [arXiv](https://arxiv.org/abs/2509.24930)
- LLM idiosyncrasies survive rewriting by another LLM — [arXiv](https://arxiv.org/abs/2502.12150)

**Ethics and security**
- Panza, TinyStyler and Chakrabarty et al. all flag impersonation risk. Panza: "access to a small number of writing samples can allow a bad actor to cheaply create generative models that imitate a target's writing style" — [arXiv](https://arxiv.org/abs/2407.10994); [arXiv HTML](https://arxiv.org/html/2406.15586)

### Inferences
- Single-author training sets are topically narrow (one person's job, hobbies, characters). Models and evaluators alike can satisfy "sounds like X" by reproducing X's topics, names and stock content. Held-out-topic evaluation and content-controlled style metrics (StyleDistance-type embeddings) are needed to tell style from topic.
- RAG at inference over a fine-tuned style model is a known source of copy-paste behavior unless the model is trained with retrieval in context.

### Gaps
- "Mode collapse to signature phrases" (overuse of an author's catchphrases or tics after fine-tuning) is not directly measured in any paper I found. The closest signals are low perplexity of imitations (Jemama & Kumar) and StyleMC's observation that LM sampling avoids the low-probability "dips" of human text.
- No quantified study found of instruction-following degradation (e.g., IFEval) after per-user style fine-tuning of frontier-scale models.

---

## 6. Decoupling content from style (e.g., frontier model writes content, small model restyles it)

### Takeaway
Decoupling is the core architecture of the authorship style-transfer line (neutral paraphrase → author-conditioned reconstruction). TinyStyler explicitly proposes using it to personalize chat-model outputs. It is also implicit in the best fine-tuning recipes, which train on (LLM-extracted content description → real author text) pairs (Chakrabarty; Panza's reverse instructions). The cautions: a 2026 small-LoRA restyler mostly removed "AI-ness" without recovering personal style, and LLM idiosyncrasies can survive restyling because they are partly encoded in content.

### Cited Findings
**Pipeline evidence**
- **Paraphrase → reconstruct** is the decoupling mechanism of STRAP (2020), and TinyStyler, ParaGuide and ASTRAPOP all build on neutral paraphrases. TinyStyler later distills away the separate paraphraser — [arXiv](https://arxiv.org/abs/2010.05700); [arXiv HTML](https://arxiv.org/html/2406.15586); [arXiv HTML](https://arxiv.org/html/2403.08043)
- **TinyStyler** (800M) "can empower individuals... to rewrite texts or personalize generic outputs from chat models to match a user's preferences" — [arXiv HTML](https://arxiv.org/html/2406.15586)

**Content-to-style training pairs**
- **Chakrabarty et al.** GPT-4o generated a content description for each author excerpt, and the fine-tuned model learned description → author prose. At inference it receives novel content descriptions. Separating "what happens" from "how it is written" produced the strongest author imitation in the literature found — [arXiv HTML](https://arxiv.org/html/2510.13939)
- **Panza.** Reverse Instructions use an LLM to write the instruction that would produce each real email; the model learns instruction → user's email — [arXiv HTML](https://arxiv.org/html/2407.10994)

**Restyling results and cautions**
- **InMyStyle** (arXiv:2607.29238, 2026). A small LoRA rewrites AI-edited text toward one user's style without an instruction prompt. Gains favored "content-preserving naturalization more than recovery of personal style," with near-zero stylometric improvement. LLM judges rated outputs over 20% lower in perceived AI-ness than the helper-generated inputs — [arXiv](https://arxiv.org/abs/2607.29238)
- **StyleVector** (arXiv:2503.05213). Motivated by "the entanglement of content semantics and stylistic patterns in historical texts," it extracts a style direction in activation space — [arXiv](https://arxiv.org/abs/2503.05213)
- **Sun et al.** (ICML 2025). Model-identifying idiosyncrasies "persist even when the texts are rewritten, translated, or summarized by an external LLM," i.e., some of the source model's fingerprint lives in content choices — [arXiv](https://arxiv.org/abs/2502.12150)
- **Khan et al. (StyleMC).** Proposes the approach also for style transfer and anonymization, editing a document's style while preserving meaning — [arXiv](https://arxiv.org/abs/2312.17242)

### Inferences
- A "frontier model drafts content → per-user model restyles" pipeline has direct academic precedent. The best-evidenced variant trains the restyler on (content description or neutral paraphrase → real user text) pairs, not on (AI draft → user text) pairs alone.
- If the frontier model's content choices themselves carry its fingerprint (Sun et al.), restyling surface form may not fully remove the "LLM voice."
- Passing content as a sparse description (Chakrabarty) rather than a full AI draft gives the style model more freedom and plausibly less AI residue. This is untested head-to-head.

### Gaps
- No controlled head-to-head found between (a) end-to-end per-user fine-tuning, (b) frontier draft plus small restyler, and (c) content outline plus per-user generator on the same users with human judges.

---

## 7. Cross-approach comparison (synthesis of the above)

### Takeaway
For one person's voice, weight-based adaptation that learns the mapping from content to that person's prose (fine-tuning or preference optimization on their texts) is the only family with strong human-judged evidence of success. Prompting and retrieval are cheap and good for content and facts, but they plateau at a generic voice. Few-shot style-transfer rewriters work with very little data but move text only partially toward the target.

### Cited Findings
| Approach | Typical target-author data | Best evidence for | Evidence against / limits |
|---|---|---|---|
| **Prompting / few-shot ICL** | 2–10 samples in context | Adequate for news/email (AV ~95%+) — [Wang et al.](https://arxiv.org/html/2509.14543v1); completion prompting gave high verifier agreement — [Jemama & Kumar](https://arxiv.org/abs/2509.24930) | Blog AV ~17–21%, flat returns from more shots, mostly detected — [Wang et al.](https://arxiv.org/html/2509.14543v1); expert OR=0.16 fidelity, 97% detected — [Chakrabarty et al.](https://arxiv.org/abs/2510.13939); instruction-tuned models struggle — [Khan et al.](https://arxiv.org/abs/2312.17242) |
| **Retrieval-augmented personalization** | User history of any size (best for cold start) | +14.92% avg on LaMP vs +1.07% PEFT — [Salemi & Zamani](https://arxiv.org/abs/2409.09510); LongLaMP gains of 5.7–128% — [Kumar et al.](https://arxiv.org/abs/2407.11016) | "Largely fail[s] to match a given user's writing style" — [Panza](https://arxiv.org/html/2407.10994); gains decline as profiles grow — [Salemi & Zamani](https://arxiv.org/html/2409.09510); only helps with a strong base model — [APM](https://arxiv.org/abs/2605.21063) |
| **Per-user PEFT (LoRA/RoSA), incl. OPPU, PER-PCS** | ~25–100+ emails for most of the gain | OPPU beats prompt methods on all 7 LaMP tasks — [Tan et al.](https://arxiv.org/abs/2402.04401); Panza convincing at 50–100 emails and identifiable by acquaintances — [Panza](https://arxiv.org/html/2407.10994) | Small gains with sparse data — [Salemi & Zamani](https://arxiv.org/html/2409.09510); LoRA < RoSA/FFT on style — [Panza](https://arxiv.org/html/2407.10994); ~200 MB/adapter storage; tiny-data rank-8 LoRA near-zero stylometric gain — [InMyStyle](https://arxiv.org/abs/2607.29238) |
| **Full fine-tuning / API fine-tuning** | Hundreds of emails to whole oeuvres | GPT-4o fine-tuned per author: expert fidelity OR=8.16, 3% detected, median $81 — [Chakrabarty et al.](https://arxiv.org/abs/2510.13939); FFT ≈ RoSA > LoRA — [Panza](https://arxiv.org/html/2407.10994) | Hyperparameter-sensitive; rare regurgitation needs resampling; occasional content omission — [Chakrabarty et al. HTML](https://arxiv.org/html/2510.13939) |
| **Preference / online imitation (DITTO, ASTRAPOP, GRPO)** | 5–10 demonstrations | DITTO beats SFT by 11 pts and few-shot by 33.4 pts with 7 demos — [Shaikh et al.](https://arxiv.org/html/2406.00888); ASTRAPOP beats ICL/SFT with 5 examples — [Liu et al.](https://arxiv.org/abs/2403.08043) | Evaluated by GPT-4 win rate or embedding metrics; limited human tests |
| **Style-transfer rewriting (STRAP, STYLL, TinyStyler, ParaGuide, StyleMC)** | STRAP >100k words; few-shot variants 5–16 posts (~500 words) | TinyStyler (800M) beats GPT-4 on Joint metrics — [Horvitz et al.](https://arxiv.org/html/2406.15586); StyleMC beats prompted GPT-4 — [Khan et al.](https://arxiv.org/abs/2312.17242) | Towards ≤~0.16 for all systems; style-vs-meaning trade-off; "not yet mastery" — [Patel et al.](https://arxiv.org/abs/2212.08986) |
| **Activation steering / style vectors** | Some user texts, no training | +8% relative, 1700× less storage than PEFT — [StyleVector](https://arxiv.org/abs/2503.05213) | Mostly validated on coarse styles or ROUGE benchmarks — [Konen et al.](https://arxiv.org/abs/2402.01618) |

### Inferences
- Benchmarks disagree mainly because of metrics. ROUGE-scored LaMP tasks favor retrieval; style-distribution and human-judged evaluations (MAUVE, expert readers, acquaintance tests) favor fine-tuning.
- A practical evidence-backed stack would combine several pieces:
  1. Per-user adapters (RoSA/LoRA, or API fine-tuning) trained on (LLM-written content description → user text) pairs.
  2. Retrieval inside training (RAFT) for user facts.
  3. Optionally a DITTO-style preference stage using the user's edits.
  4. Evaluation on held-out topics with content-independent style embeddings plus human judges who know the author.
  This is a synthesis, not a tested system.

### Gaps
- No single paper compares all five families on the same users, metrics and human evaluation. The table above stitches together heterogeneous studies with different genres, models and metrics, so magnitudes are not directly comparable.
