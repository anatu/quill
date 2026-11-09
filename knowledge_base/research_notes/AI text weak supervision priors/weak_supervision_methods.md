# Methods for combining noisy priors into calibrated AI-text / slop labels, training a local classifier, and using it in quill

Compiled 2026-11-07. Scope: methodology only (weak supervision, PU learning, distributional estimation, style-embedding propagation, shortcut risks, local classifier training/calibration, and pipeline uses). Prior catalogs (self-disclosure, time, producer behavior, paired corpora) are covered by other researchers. Labels used throughout: **(measured)** = number from an experiment in the cited paper; **(self-reported)** = vendor or model-card claim, or authors' claim about their own product; **(estimated)** = my arithmetic or extrapolation; **[unverified]** = not confirmed from a primary source this session.

---

## 1. Weak supervision / data programming: can a generative label model combine our priors without ground truth?

### Takeaway
Snorkel-style label models (2016-2020) estimate labeling-function (LF) accuracies from agreement and disagreement, but only when several LFs overlap on the same documents. Our strongest priors are one-sided and fire on non-overlapping populations: "pre-Dec-2022 → human" never co-fires with "Co-Authored-By: Claude → AI". So a label model cannot learn their accuracies from the data. It is useful only over the post-2023 pool, where several two-sided signals overlap (detector scores, lexicon scores, producer behavior). No published work applies Snorkel/FlyingSquid to AI-text detection. The nearest precedents are LLM-labels→small-classifier pipelines for web text quality (FineWeb-Edu, DCLM).

### Cited Findings
- **Snorkel results (VLDB 2018; arXiv Nov 2017), self-reported by the authors on their own tasks:** in a user study, subject-matter experts built models 2.8× faster and improved predictive performance by an average of 45.5% versus seven hours of hand labeling. Average F1 was 30.4 for Snorkel users vs 20.9 for hand supervision, and 8 of 15 participants matched or beat the hand-labeled models. Across benchmarks, Snorkel averaged a 132% improvement over prior heuristic approaches and came within an average 3.60% of models trained on large hand-curated sets (measured) — [Ratner et al., Snorkel (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5951191); [Morning Paper summary, 2018-08-22](https://blog.acolyer.org/2018/08/22/snorkel-rapid-training-data-creation-with-weak-supervision/)
- **Snorkel `LabelModel` mechanics (docs v0.9.7):**
  - Learns P(lf | Y) for each LF and reweights the votes. The input is an n×m matrix with abstain encoded as −1.
  - Uses "a matrix completion-style approach" from the AAAI'19 paper (arXiv 1810.02840), which handles dependency graphs via the junction tree. The shipped class, however, assumes "the LFs are conditionally independent given Y" and does not model LF dependencies.
  - `fit()` accepts `class_balance` (class fractions) or `Y_dev` (gold labels to estimate class balance). `prec_init` defaults to 0.7.
  - The docs give no guidance on LF count or minimum accuracy.
  - — [Snorkel LabelModel docs](https://snorkel.readthedocs.io/en/v0.9.7/packages/_autosummary/labeling/snorkel.labeling.model.label_model.LabelModel.html)
- **FlyingSquid (Fu et al., ICML 2020):** splits label-model parameter estimation into closed-form subproblems over triplets of label sources, with no SGD. It runs about 170× faster on average on simple graph structures and up to 4,000× faster on video tasks with temporal dependencies. Estimation time is linear in data size, with provable bounds (measured/self-reported) — [Fu et al., arXiv 2002.11955](https://arxiv.org/pdf/2002.11955); [PMLR v119](https://proceedings.mlr.press/v119/fu20a.html); [Hazy Research blog, 2020-02-28](https://hazyresearch.stanford.edu/blog/2020-02-28-flyingsquid)
- **WRENCH (NeurIPS 2021 Datasets & Benchmarks):** 22 real-world datasets and more than 120 method variants. The authors report large "hidden" evaluation variance from datasets that share a name but differ in labels and weak sources — [WRENCH](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/1c9ac0159c94d8d0cbedc973445af2da-Abstract-round2.html). I did not retrieve its numeric label-model-vs-gold gap.
- **Weak supervision often loses to a little clean data (Zhu et al., ACL 2023, outstanding paper):**
  - Without clean validation samples, the WSL methods tested perform about as well as, or worse than, the raw weak labels.
  - When the clean validation data is used for training instead, most WSL advantages vanish, even with as few as 5 clean samples per class.
  - Training directly on clean samples beats WSL methods once there are more than 10 per class on most datasets (measured).
  - — [Zhu et al., arXiv 2305.17442](https://arxiv.org/pdf/2305.17442)
- **Prompts as LFs:** "Language Models in the Loop" treats LLM prompts as labeling functions that map completions to labels or abstains — [ACM 10.1145/3617130](https://dl.acm.org/doi/10.1145/3617130). Details not read.
- **AutoWS** generates LFs from a small labeled seed set per class, then aggregates them into probabilistic labels — [arXiv 2302.03297](https://arxiv.org/abs/2302.03297)
- **No AI-text-detection application found.** A targeted search (2026-11) for programmatic weak supervision or labeling functions applied to machine-generated text detection returned only general WS and adjacent applications — [search results incl. TEXTRON, AutoWS](https://arxiv.org/pdf/2402.09811)
- **Nearest at-scale analogues (text quality, not AI detection):**
  - **FineWeb-Edu (2024):** Llama-3-70B-Instruct scored about 450-460k web pages (sources differ) on a 0-5 educational scale. A frozen Snowflake-Arctic-Embed encoder plus a linear regression head was trained on those labels and reached 82% F1 at threshold 3 on held-out Llama labels (measured against teacher labels, not humans). The card warns that it may overfit to academic-looking content at high scores — [FineWeb paper, arXiv 2406.17557](https://arxiv.org/pdf/2406.17557); [fineweb-edu-classifier card](https://huggingface.co/HuggingFaceFW/fineweb-edu-classifier)
  - **DCLM (2024)** built a de facto PU setup: a fastText classifier with OpenHermes-2.5 + ELI5 as "hq" positives and random Common Crawl/RefinedWeb as negatives, thresholded at the top 10%. It was the best filter in their ablation (CORE 41.0) — [DCLM review](https://liner.com/review/datacomplm-in-search-next-generation-training-sets-for-language-models); [fasttext-oh-eli5](https://huggingface.co/mlfoundations/fasttext-oh-eli5). A later analysis reports that well-formed news-style text gets near-0 "hq" probability because the QA-heavy positives contain no news, a domain shortcut — [arXiv 2510.00866](https://arxiv.org/html/2510.00866v1)

### Inferences
- **Identifiability problem specific to our priors.** A label model learns LF accuracy from co-firing. Our "certain" priors split into two disjoint coverage regions:
  - The time LF (pre-2022 → human) covers only old documents.
  - Self-disclosure and artifact-leak LFs (→ AI) fire only on new ones.
  - These LFs never vote on the same documents, so their accuracies are unidentifiable from L alone. Snorkel's conditional-independence assumption is also violated: every AI LF is structurally conditioned on date > 2022.
  - FlyingSquid's triplet method needs ≥3 conditionally independent sources voting on the same items (inferred from its triplet construction).
- **Where a label model does fit:** the post-2023 unlabeled pool, with LFs that vote on most documents:
  - two-sided detector LFs: Binoculars and Fast-DetectGPT score bands with abstain in the middle, and a Pangram score on a subsample;
  - a Liang-style word-likelihood-ratio LF;
  - a slop-lexicon density LF;
  - producer-behavior LFs (velocity, domain age, fake byline), which are author-level and correlated with each other;
  - a LUAR/StyleDistance kNN LF (section 4).
  
  Supply `class_balance` from the Liang α estimate (section 3) instead of letting the model guess it.
- **Treat the one-sided certain LFs as anchors, not votes.** Pre-2022 = negatives, artifact leaks and self-disclosure = positives. This turns the problem into PNU learning (section 2) and makes the label model optional.
- **Zhu et al. implies a cheap baseline is mandatory.** We have about 9.5k gold-ish labels (300 Human Detectors + ~7.6k Wikipedia {{AI-generated}} + ~1.6k Beemo). A classifier trained only on that gold, with no weak labels, is the bar the weak-supervision pipeline must beat on held-out sources. If it doesn't, drop the label model.
- **LF count (estimate):** 8-20 LFs is the practical range for one person to write and audit. Correlated producer LFs should be merged into one "producer score" LF so the conditional-independence assumption is less badly violated.

### Gaps
- No published accuracy figures for Snorkel/FlyingSquid on AI-text or writing-quality labels.
- WRENCH's label-model-vs-gold gap numbers were not retrieved.
- No source gives an empirical rule for the minimum LF count or coverage for reliable accuracy estimation, beyond the triplet requirement.

---

## 2. Positive-unlabeled (PU) learning with certain-AI positives, an unlabeled post-2023 pool and certain-human negatives

### Takeaway
nnPU (Kiryo et al., NIPS 2017) is the standard deep-net-safe PU objective, and it takes the class prior π as an input. The one AI-text PU paper (Tian et al., MPU, ICLR 2024 spotlight; verified) uses the opposite framing: **human = positive**, and short AI texts are treated as "partially unlabeled". Its PU loss adds only +0.4 to +2.6 F1 points on top of data augmentation. The bigger risk for us is that our certain-AI positives violate SCAR, the assumption most PU methods need, because artifact leaks and self-disclosures are the least-edited, sloppiest AI text.

### Cited Findings
- **nnPU (Kiryo, Niu, du Plessis, Sugiyama; NIPS 2017 oral; arXiv 1703.00593):** with flexible models, the unbiased PU (uPU) empirical risk can go negative, which causes severe overfitting. The non-negative estimator clamps that term, so deep nets can be used even with limited positives. The authors give bias, consistency, MSE and estimation-error bounds — [arXiv 1703.00593](https://arxiv.org/abs/1703.00593). As written in MPU, the nnPU risk is π̃·R_P(+1) + max{0, R_U(−1) − π̃·R_P(−1)}, so the class prior π̃ is an explicit input — [MPU, arXiv 2305.18149v4](https://arxiv.org/html/2305.18149v4)
- **SCAR/SAR (Bekker & Davis, Machine Learning 109:719-760, 2020):**
  - SCAR, the basis of most PU methods, assumes labeled positives are a random sample of all positives: Pr(s=1|x) = c·Pr(y=1|x), with label frequency c independent of features.
  - SAR lets labeling depend on features.
  - Bekker, Robberechts and Davis show that wrongly assuming SCAR hurts classifier performance.
  - Under SCAR, the class prior and c convert into each other via the label prior. Class-prior estimators include du Plessis & Sugiyama (2014) and TIcE (decision-tree induction, AAAI 2018).
  - — [Bekker & Davis survey, arXiv 1811.04820](https://arxiv.org/pdf/1811.04820)
- **MPU (Tian et al., ICLR 2024 spotlight) — verified:**
  - Framing: human texts are the labeled positive class, and short machine texts get an extra "unlabeled" mark because very simple AI sentences can look human.
  - Prior: a length-dependent prior π̃(l) from an "abstract recurrent" model (best token-level p = 0.2). Loss = R_PN + γ·R_MPU with γ = 0.4.
  - "Text Multiscaling" randomly drops sentences (p_sent = 0.25). Backbones are BERT and RoBERTa.
  - — [arXiv 2305.18149v4](https://arxiv.org/html/2305.18149v4); [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/95ab5c3e26fd82c7de3230bbad087d2d-Abstract-Conference.html)
  - Results (measured, F1):

    | Benchmark | RoBERTa-finetuned | RoBERTa-MPU |
    |---|---|---|
    | HC3-En Full | 97.42 | 98.40 |
    | HC3-En Sent | 58.60 | 85.31 |
    | HC3-Zh Full | 96.28 | 97.42 |
    | HC3-Zh Sent | 83.07 | 89.37 |
    | TweepFake (accuracy) | 89.6 | 91.4 |

  - Ablation: Text Multiscaling alone gives most of the short-text gain (Sent 58.60 → 82.76). Adding the MPU loss on top adds +2.55 (Sent) and +1.98 (Full) in English. The MPU loss alone *hurt* English Sent (−13.30). nnPU vs uPU adds only +0.50 and +0.44 (measured) — [arXiv 2305.18149v4](https://arxiv.org/html/2305.18149v4)
  - MPU's Appendix C reports a **spacing artifact in HC3**: a simple token-presence rule reaches 82.12% F1 on sentence-level data — [arXiv 2305.18149v4](https://arxiv.org/html/2305.18149v4)
- **Precedent for PU-like quality filtering at scale:** DCLM's positives (OH-2.5/ELI5) against an unlabeled web pool, and the domain bias that resulted (see section 1) — [arXiv 2510.00866](https://arxiv.org/html/2510.00866v1)

### Inferences
- **Our setting is PNU, not pure PU.** Use a supervised term on (certain-AI P, certain-human N), plus an nnPU term on the unlabeled post-2023 pool U, with π taken from the Liang α of that slice (section 3).
- **SCAR is badly violated by our positives.**
  - Artifact leaks ("As an AI language model…", "Certainly! Here is…") select raw, unedited chatbot output.
  - Self-disclosure selects coding and academic contexts.
  - A classifier trained on these positives learns "unedited chatbot register". It will under-detect edited, humanized or style-imitated AI, which is exactly what quill's adapter produces (section 6).
  - Mitigation: add synthetic positives that cover the SAR gap (paraphrased, humanized, style-imitated, own-adapter outputs). Strip the leak string itself from leak-positives before training so the model can't key on it. Weight positives by inverse estimated propensity.
- **Choice of positive class.** MPU's human-positive framing matters only for very short text. For informational nonfiction at paragraph or document level, the standard AI = positive framing is fine.
- **Expected gain is small.** The best AI-text PU evidence shows PU-loss gains of about 0.4-2.6 F1 over strong supervised baselines. PU is therefore a way to *use* the unlabeled pool and correct π, not a way to reach Pangram-level accuracy.

### Gaps
- I found no AI-text detection work that uses PU learning with self-disclosed or artifact positives, or with web-scale unlabeled pools.
- I found no class-prior-estimation results (TIcE, KM2) on text-detection data.

---

## 3. Distributional estimation: Liang et al.'s MLE for the fraction of LLM-modified text, and corpus-level priors as soft labels or PU class priors

### Takeaway
The Liang et al. framework (ICML 2024, then COLM 2024 and a 2025 society-wide study) estimates the corpus-level fraction α of "substantially LLM-modified" text. It fits a two-component mixture over document-level word-occurrence likelihoods (mainly adjectives), with reference human and AI corpora. On synthetic mixtures it is accurate to within about 2.4 percentage points, 3-5× better than instance-level detectors. It is the right tool to supply π per (source × time-slice) for PU or label-model class balance, and to check calibration-in-the-large. It cannot label individual documents.

### Cited Findings
- **Method (Liang et al., "Monitoring AI-Modified Content at Scale", ICML 2024; arXiv 2403.07183, Mar 2024):**
  - Each document comes from (1−α)P + αQ. A document is a *set* of token occurrences, so length penalties are limited.
  - p̂(t) and q̂(t) are the fractions of human and AI reference documents containing t.
  - α is fit by MLE: maximize Σ log((1−α)P(x) + αQ(x)).
  - Main features are **adjectives**, with technical terms removed; the authors found them more stable than adverbs, verbs, nouns or all tokens. Sentence units performed slightly better than documents.
  - Cost is about 68 FLOPs per sentence vs about 2.7×10⁹ for a compared detector.
  - The AI reference corpus is built by prompting the LLM with the same instructions humans got. A two-stage variant condenses human reviews into outlines, then has the LLM expand them.
  - — [arXiv 2403.07183v2](https://arxiv.org/html/2403.07183v2)
- **Validation (measured):**
  - On held-out synthetic mixtures, error was below 1.8% in-distribution (ICLR 2023), below 1.8% under topic shift to NeurIPS 2022, and below 2.4% for CoRL 2022.
  - Against the best instance-level baseline (a fine-tuned BERT plus two published detectors), error fell 6.2% → 1.8% in-distribution and 11.2% → 2.4% out-of-distribution.
  - Typo-only ChatGPT proofreading produced only a slight, non-significant α increase.
  - A model trained on GPT-3.5 references still detected GPT-4 text.
  - Estimates rose from pre-ChatGPT to 2024: ICLR 1.6% → 10.6%, NeurIPS 1.9% → 9.1%, CoRL 2.4% → 6.5%. EMNLP 2023 was about 16.9%, and Nature portfolio reviews showed no significant rise.
  - Example rising adjectives: "commendable," "meticulous," "intricate".
  - — [arXiv 2403.07183v2](https://arxiv.org/html/2403.07183v2)
- **Stated limitations:**
  - Results are tied to the reference LLM, and the authors recommend matching it to the LLM likely used.
  - The token-independence assumption is an approximation.
  - Temporal shifts in topics, vocabulary or writer populations can bias α.
  - α measures "substantial modification", not from-scratch generation.
  - — [arXiv 2403.07183v2](https://arxiv.org/html/2403.07183v2)
- **Scientific papers (Liang et al., "Mapping the Increasing Use of LLMs in Scientific Papers", COLM 2024; arXiv 2404.01268):** 950,965 papers from Jan 2020 to Feb 2024 (773k arXiv, 161k bioRxiv, 16.5k Nature portfolio). Higher α was associated with frequent preprint posters, crowded fields and shorter papers — [arXiv 2404.01268](https://arxiv.org/html/2404.01268v1)
- **Society-wide (Liang et al., arXiv 2502.09747, Feb 2025):** data from Jan 2022 to Sep 2024. Estimates: about 18% of US financial consumer-complaint text by late 2024, up to 24% of corporate press releases, just under 10% of job postings at small firms, and nearly 14% of UN press releases. Growth plateaued in 2024, which the authors attribute to saturation or to newer models being harder to detect — [arXiv 2502.09747](https://arxiv.org/abs/2502.09747). The abstract describes the method only as a "robust population-level statistical framework" [method identity with the ICML paper not confirmed from the abstract].
- **Time-prior calibration precedent (Brooks, Eggert, Peskoff; WikiNLP 2024; arXiv 2410.08044, Oct 2024):** GPTZero and Binoculars thresholds were set to a 1% FPR on pre-GPT-3.5 Wikipedia articles. At those thresholds they flag more than 5% of 2,909 new English Wikipedia articles from Aug 2024. The authors call this a lower bound. Flagged articles skewed lower quality and self-promotional — [arXiv 2410.08044](https://arxiv.org/html/2410.08044v1)

### Inferences
- **Use 1: class priors.** Compute α per (source family × quarter), e.g. Wikipedia new articles, Medium tech posts, news sites, Substack. Use that α as π in nnPU and as `class_balance` in the Snorkel `LabelModel`. Validate the α estimator on synthetic mixtures of our own human pool and our mirrors first, as Liang did.
- **Use 2: label proportions.** Instead of per-document soft labels, constrain the classifier so its mean predicted probability on each slice matches that slice's α. This is "learning from label proportions" (the method name is general knowledge; I found no AI-text source for it). It also gives a calibration-in-the-large check that needs no per-document gold.
- **Use 3: a quill eval metric.** Run α on a batch of N adapter generations against reference corpora (P = the author's human text or matched pre-2022 informational prose; Q = generic LLM output on the same briefs). This gives a population-level "AI-modified share" that is cheap and hard to game per sample. Caveat: Q must be rebuilt for each new model family.
- **Do not use α as a per-document soft label.** It is a mixture weight, not a posterior. The per-document posterior αQ(x) / ((1−α)P(x) + αQ(x)) is a naive-Bayes-style score and inherits the token-independence approximation. It is acceptable as *one LF*, not as the target.
- **The time prior is softer than "pre-Dec-2022 = human".** Brooks et al. used pre-GPT-3.5 (before March 2022) as the clean cutoff, and GPT-3-era content farms existed before ChatGPT (general knowledge [unverified]). The safest cutoff for "certain human" is about 2021 or earlier, with α checked on 2022 slices.

### Gaps
- I did not confirm from primary text whether the 2025 society study used exactly the adjective-MLE framework.
- I found no published use of Liang-α as a PU class prior or as label-proportion supervision for detector training.

---

## 4. Label propagation via style embeddings (LUAR / StyleDistance / Wegmann) and author-level vs document-level labels

### Takeaway
Style embeddings trained only on human authorship data separate human from LLM text and support few-shot detection (Soto et al., ICLR 2024). A style-based detector also survived DPO evasion that broke a likelihood detector (AUROC 0.95 vs 0.18). That makes kNN propagation in LUAR or StyleDistance space a good *LF* and a second, independent eval detector. I found no work on multiple-instance learning (MIL) for author-level AI-text labels. Producer priors should enter as noisy document LFs with author-level correlation handled explicitly.

### Cited Findings
- **Soto et al., "Few-Shot Detection of Machine-Generated Text using Style Representations" (ICLR 2024; arXiv 2401.06712, Jan 2024):** style representations learned from human-authored text (LUAR family) separate human text from Llama-2, ChatGPT and GPT-4 output. The method is cosine similarity to a few known LLM samples, with no target-model training data needed. It also attributes text to generators from a few examples. Code is in LLNL/LUAR `fewshot_iclr2024` — [arXiv 2401.06712](https://arxiv.org/pdf/2401.06712)
- **Style-based detection under DPO:** DPO against Fast-DetectGPT drove that detector's AUROC to 0.18, while a style-based detector stayed at 0.95 (measured) — [Soto et al., arXiv 2505.14608](https://arxiv.org/html/2505.14608v1) (from prior project notes, `AI slop negative signal/training_methods.md`)
- **StyleDistance (Patel et al., NAACL 2025; arXiv 2410.12757, Oct 2024):** standard contrastive style triplets "do not explicitly control for content", which weakens content-independence. StyleDistance trains on SynthSTEL, LLM-generated near-exact paraphrases varying 40 style features. It reports strong STEL and STEL-or-Content results and generalization to unseen features (self-reported) — [arXiv 2410.12757](https://arxiv.org/html/2410.12757v2); [ACL Anthology](https://preview.aclanthology.org/setup/2025.naacl-long.436)
- **Contrastive multi-author detection:**
  - FAID (EACL 2026) treats each LLM as an "author" and learns author-specific hidden-space features over about 84k human, AI and collaborative texts — [arXiv 2505.14271](https://arxiv.org/html/2505.14271v2)
  - WhosAI (ECAI 2024) learns a similarity space that new generators can be added to — [arXiv 2407.09364](https://www.arxiv.org/abs/2407.09364)
- **Author attributes confound detection:** writer traits such as language proficiency and native vs learner status systematically shift detector behavior — [Li & Wan, arXiv 2502.12611](https://arxiv.org/pdf/2502.12611v2)
- **No MIL work found.** A 2026-11 search found no author-level or account-level AI-text detection framed as multiple-instance learning — [search incl. FAID, WhosAI](https://arxiv.org/html/2505.14271v2)

### Inferences
- **Author level vs document level.** Producer priors (high velocity, new domain, fake byline) are bag-level: they say a site or author *probably* publishes AI text.
  - Standard MIL ("a bag is positive if ≥1 instance is positive") is the wrong assumption for content farms that mix scraped human text with AI rewrites. Even "most instances positive" is unreliable.
  - Recommended handling:
    1. Enter producer priors as a *document LF* with a learned (lower) accuracy.
    2. Cap each author's contribution to training (e.g., ≤20 documents per author) so one prolific farm can't dominate.
    3. **Split train and test by author or domain, never by document.** This avoids author-identity leakage, where the classifier memorizes a site's template.
- **Propagation recipe.** Embed all documents with StyleDistance (content-controlled) and LUAR (author-level, stronger on longer text). For each unlabeled document, the LF votes AI if its k nearest *labeled* neighbors are predominantly certain-AI and the margin over human neighbors exceeds a threshold, and abstains otherwise. For authors, aggregate document embeddings (mean) and propagate to stylistically near authors only at very high similarity.
  - Risk: LUAR-type embeddings carry topic and genre, as StyleDistance's own motivation notes. Propagation can then spread "2024 tech-blog topic" rather than "AI style". Prefer StyleDistance for propagation and audit neighbors manually on 50 cases.
- **Why bother:** a style-embedding detector is architecturally different from a fine-tuned ModernBERT classifier. That makes it a good *held-out eval detector* when the ModernBERT one is used for reranking (section 7b), because the two are less likely to share the same Goodhart blind spots.

### Gaps
- No quantitative evidence on how accurately label propagation in style-embedding space spreads AI/human labels to new authors.
- No measured LUAR or StyleDistance detector accuracy on informational nonfiction was found.

---

## 5. Shortcut and confound risks (temporal, domain, length, formatting) and mitigations

### Takeaway
2024-2026 work repeatedly shows that detector benchmark accuracy is inflated by surface shortcuts:
- formatting and lexical surface features alone separate human from AI (EMNLP 2026, two papers);
- a whitespace artifact gives 82% F1 on HC3;
- generic-trained detectors lose 10-40% on realistic Wikipedia editing (TSM-Bench, ICLR 2026);
- fine-tuned classifiers fall from 95%+ to about 60% on unseen generators (RAID, ACL 2024).

Our design (human = pre-2022, AI = post-2023) adds a temporal shortcut that no paper I found measures directly. The only mitigation with strong reported evidence is Pangram's: AI "mirrors" matched to each human document's topic and length, plus hard-negative mining.

### Cited Findings
- **TSM-Bench (Quaremba, Black, Vrandečić, Simperl; ICLR 2026; arXiv 2605.31113):** detectors trained on generic machine text overfit to "superficial artefacts". Their accuracy drops 10-40% on real Wikipedia editing tasks (summarization, paraphrasing, etc.). Task-specific fine-tuning transfers to generic data but not the reverse. About 152,910 machine texts [count from secondary summary] — [ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10006430); [alphaXiv](https://www.alphaxiv.org/abs/2605.31113)
- **Clever Hans formatting confounds (Dutta Chowdhury, España-Bonet, van Genabith; Findings of EMNLP 2026):** surface form alone "strongly separates" human from machine text on three benchmarks, and the learned surface patterns differ by benchmark. Detector scores are largely predictable from surface form, though detectors still carry some signal beyond it. Controlled reformatting shows partial, detector-specific causal effects — [ACL Anthology 2026.findings-emnlp.1051](https://aclanthology.org/2026.findings-emnlp.1051/). The abstract gives no numbers.
- **Shortcut-controlled evaluation (Jung, Ahn, Park, Kim; EMNLP 2026):** a logistic regression on surface features (formatting style, lexical usage) "performs strongly without any semantic signals". Existing detectors degrade consistently once shortcuts are removed. The authors release AIGT-SignalBench — [ACL Anthology 2026.emnlp-main.2177](https://aclanthology.org/2026.emnlp-main.2177/). The abstract gives no numbers.
- **HC3 spacing artifact:** a token-presence rule reaches 82.12% F1 at sentence level (measured) — [MPU appendix C, arXiv 2305.18149v4](https://arxiv.org/html/2305.18149v4)
- **Prompt-specific shortcuts:** detectors learn cues tied to particular generation prompts (HC3) — [arXiv 2406.16275](https://arxiv.org/html/2406.16275v1)
- **RAID (Dugan et al., ACL 2024; over 6M generations, 11 models, 8 domains, 11 attacks, 4 decoding strategies), measured:**
  - RoBERTa-Large (GPT-2) gets 95%+ accuracy on five domains with GPT-2 text but "rarely exceeds 60%" on the same domains from other models.
  - A repetition penalty cuts accuracy by up to 32 points for every detector.
  - Homoglyphs drop Originality from 85.0 to 9.3 and Binoculars from 79.6 to 37.7 (at 5% FPR).
  - At naive τ = 0.5 thresholds, FPRs include GLTR 99.3%, F-DetectGPT 23.2%, RoBERTa-Base (GPT-2) 6.59%, RADAR 3.48% and Binoculars 0.00%.
  - A single global threshold gives domain FPRs far from target, e.g. RADAR 20.4% on reviews and GLTR 33.4% on recipes. RAID therefore sets per-domain thresholds at a fixed 5% FPR.
  - — [arXiv 2405.07940](https://arxiv.org/html/2405.07940)
- **M4 (Wang et al., EACL 2024 resource award):** detectors generalize poorly to unseen domains and LLMs and "tend to misclassify machine-generated text as human-written" in those cases — [ACL Anthology 2024.eacl-long.83](https://aclanthology.org/2024.eacl-long.83). Exact cross-domain numbers not retrieved.
- **DetectRL (NeurIPS 2024 D&B):** zero-shot detectors struggle under realistic attacks (prompt variation, word substitution, writing errors). Detectors trained on diverse lengths generalize better, and performance degrades when test lengths differ from training lengths. The authors say supervised detectors were comparatively robust — [arXiv 2410.23746](https://arxiv.org/html/2410.23746v3). Aggregator scores (about 91 OOD) [unverified].
- **Domain shortcut in quality filtering:** DCLM's classifier assigns near-0 "hq" probability to well-formed news because its positives contain no news — [arXiv 2510.00866](https://arxiv.org/html/2510.00866v1)
- **Matched-mirror mitigation (Pangram):** for each human document, an AI mirror is generated to match "as many axes as possible", including topic and length, sometimes seeded with the human document's opening excerpt. Boilerplate is stripped, and examples under 50 words are rejected. The stated aim is to make the model learn "features of LLM writing rather than topic or style" — [Emi & Spero, arXiv 2402.14873v3](https://arxiv.org/html/2402.14873v3); [Pangram "How it works"](https://www.pangram.com/research/how-it-works)
- **Era-matched human corpus for FPR:** Epoch AI (2026-07-15) used 495 pre-2022 human passages from 99 authors. Pangram and GPTZero had 0 false positives on it (90% CI 0-0.54%) and Originality.ai had 19 (3.84%) — [Epoch AI data insight](https://epoch.ai/data-insights/ai-detectors-false-negatives); [data repo](https://github.com/jaeholee-brown/ai-text-detectors)
- **No direct temporal-shortcut study found.** A search for date or era shortcuts in AI-text detection turned up only prompt and surface shortcuts — [search incl. arXiv 2406.16275](https://arxiv.org/html/2406.16275v1)

### Inferences
- **Temporal shortcut risk in our design is high.** With human = pre-2022 and AI = 2023+ web, the classifier can learn:
  - post-2022 entities and topics (LLMs, COVID aftermath, 2024 elections);
  - 2023+ CMS formatting (markdown headers, emoji bullets, "Key Takeaways" boxes, FAQ schema);
  - SEO conventions;
  - Unicode quote and dash habits of newer editors.
- **Mitigations, ranked by evidence:**
  1. **Topic- and length-matched mirrors:** for every pre-2022 human document, generate AI versions from the same title, outline or opening, with several current LLMs. This is Pangram's approach and has the strongest reported evidence. Grokipedia/Wikipedia pairs are naturally topic-matched, but measure verbatim overlap first: pairs that share text teach nothing, and partial copying makes labels ambiguous.
  2. **Format normalization:** render everything to plain text and strip markdown, headers, lists, emoji and URLs. Test format-only models (e.g., a logistic regression on surface features, as in Jung et al.) and require the main classifier to beat them by a wide margin.
  3. **Post-2023 human negatives** to break the date-label link: verified-human 2023+ text (the author's own recent writing, Human Detectors human items, human-edited Beemo items, Wikipedia pages whose content predates 2022 but were edited later).
  4. **Leave-one-source-out and leave-one-generator-out evaluation** (RAID, M4).
  5. **Probe audits:** train linear probes on the classifier's embeddings to predict year and topic. Only if the probes do well, try adversarial debiasing (gradient reversal on a year head). I found no AI-text paper evaluating adversarial debiasing, so treat it as experimental.
  6. **Length bucketing and multiscale augmentation**, i.e., sentence dropping (DetectRL, MPU).
- **Per-domain thresholds are required.** One global threshold produces wildly different domain FPRs (RAID), so calibrate thresholds per source family.

### Gaps
- No paper quantifies a date shortcut, i.e., accuracy explained by publication-year cues.
- No numbers were retrieved from the two EMNLP 2026 shortcut papers (abstracts only).
- No evaluation of adversarial debiasing for AI-text detectors was found.

---

## 6. Training a local classifier: backbone, data scale, reported accuracies, robustness to quill's own outputs, calibration, active learning

### Takeaway
The only detector with independently validated ≥95% TPR at ≤2% FPR on nonfiction (Pangram) was built from about 28M confirmed-human documents, about 360k-1M mirrored examples, and hard-negative mining that cut FPR 100-1000×. It was not built from weak labels on wild data. Open fine-tuned encoders (ModernBERT, DeBERTa, RoBERTa) reach 99%+ in-distribution but fall to AUROC ≈0.86 on Beemo-style OOD data and to about 60% on unseen generators. Most importantly for quill: **fine-tuning a model on an author's work dropped Pangram's detection of its outputs from 97% to 3%**. A local classifier trained on generic or wild AI text should be assumed blind to quill's adapter until shown otherwise on adapter outputs.

### Cited Findings
- **Pangram recipe and numbers (Emi & Spero, arXiv 2402.14873v3, Jul 2024; self-reported):**
  - About 28M confirmed-human documents across 10 domains, with about 4M held out for FPR. Wikipedia had about 1M and news about 500k.
  - Initial training set: 40k per domain (360k). Performance saturates around 40k per domain, and at 100k per domain (1M) the model could not exceed 98% accuracy before hard-negative mining.
  - Hard-negative mining: each round takes up to 10k false positives per domain (80k total), generates mirrors for them, and retrains. The number of rounds is not stated.
  - Holdout FPR, before → after mining: domain-weighted 2.29% → 0.02%, Wikipedia 5.34% → 0.05%, news 0.55% → 0.001%, scientific papers 1.54% → 0.04%, and held-out email 6.60% → 0.00%.
  - On a 1,976-document benchmark (10 domains, 8 LLMs): 99% accuracy, and >97% recall at 1% FPR on every LLM. GPTZero and Originality fall below 95%.
  - Architecture: "a slightly modified transformer-style architecture" (no size given).
  - — [arXiv 2402.14873v3](https://arxiv.org/html/2402.14873v3)
- **Independent nonfiction validation (Russell, Karpinska, Iyyer; ACL 2025), measured:**
  - On 300 nonfiction articles: Pangram 98.0% TPR at 2.0% FPR; GPTZero 85.3% (0.7%); Fast-DetectGPT 80.0% (7.2%); Binoculars 66.7% (1.3%); RADAR 15.3% (2.0%).
  - On humanized o1-Pro articles: Pangram 90.0%, GPTZero 46.7%, Fast-DetectGPT 23.3%, Binoculars 6.67%.
  - — [arXiv 2501.15654](https://arxiv.org/html/2501.15654) (from prior notes, `AI slop negative signal/lexicons_and_detectors.md`)
- **Fine-tuned author-style outputs evade detectors (Chakrabarty, Ginsburg, Dhillon; arXiv 2510.13939v3, Nov 2025), measured:**
  - Pangram flagged 97% of in-context-prompted outputs but **3% of outputs from GPT-4o fine-tuned on each author's complete works**. GPTZero flagged 91% and 0%. Human text was never misclassified (threshold 0.9).
  - Cliché density mediated 16.4% of the detector-score effect on reader preference for in-context outputs, and only 1.3% (n.s.) after fine-tuning. The authors conclude fine-tuning "eliminates rather than masks" stylistic AI signatures.
  - Fine-tuning cost a median of $81 per author.
  - Scale: 30 fine-tuned authors and 90 fine-tuned pairs. The authors are literary fiction writers, not nonfiction.
  - — [arXiv 2510.13939v3](https://arxiv.org/html/2510.13939v3)
- **Style imitation also evades (Epoch AI, 2026-07-15), measured:**
  - Five-sample style imitation by Claude Opus 4.8, GPT-5.5 and Gemini 3.1 Pro produced miss rates of 10.10% for Pangram, 10.77% for GPTZero and 17.85% for Originality, vs 0-0.67% with basic prompts.
  - Scientific writing was hardest (Pangram missed 25%), and the Gemini scientific cell evaded Pangram 48% of the time.
  - Counting "Mixed" verdicts as detections lowers the Pangram miss rate to 6.1%.
  - — [Epoch AI](https://epoch.ai/data-insights/ai-detectors-false-negatives)
- **Open fine-tuned encoders:**
  - ModernBERT binary detection: about 99.45% accuracy and 99.02% AI recall in-distribution; about 94.23% on adversarial inputs (self-reported) — [Mixture of Detectors, arXiv 2509.22147](https://arxiv.org/pdf/2509.22147)
  - Vanguard (ModernBERT-large, 2nd in PAN-CLEF 2026 Voight-Kampff): in-distribution AUROC above 0.99, but on Beemo AUROC 0.856 and macro-F1 0.697 (self-reported model card) — [Vanguard card](https://huggingface.co/ShantanuT01/vanguard-ai-text-detector)
  - PAN 2026 approaches included fine-tuned RoBERTa, DeBERTa and Qwen, Longformer with adversarial training, and contrastive kNN. One team reports a 0.975 mean, and another reports ROC-AUC 0.918 on the adversarial ELOQUENT set — [PAN 2026 overview, arXiv 2602.09147](https://arxiv.org/pdf/2602.09147); [CEUR Vol-4283](https://ceur-ws.org/Vol-4283/paper391.pdf)
  - RoBERTa-Large trained on GPT-2 text "rarely exceeds 60%" on unseen generators — [RAID](https://arxiv.org/html/2405.07940)
  - Community DeBERTa-v3-large detector (desklib) claims to lead RAID (self-reported, unverified) — [desklib card](https://huggingface.co/desklib/ai-text-detector-v1.01) (from prior notes)
- **Small-data precedents:** WQRM (ModernBERT-large) was trained on about 1,000 expert edit pairs and reached 74.3% on the 4,729-judgment WQ benchmark — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3) (from prior notes). FineWeb-Edu used a frozen encoder plus a linear head on about 450k teacher labels for 82% F1 — [card](https://huggingface.co/HuggingFaceFW/fineweb-edu-classifier)
- **Thresholding practice:** RAID and Pangram both report at a fixed FPR (5% and 1%), with per-domain thresholds in RAID — [RAID](https://arxiv.org/html/2405.07940); [Pangram](https://arxiv.org/html/2402.14873v3)
- **Hardware notes (prior project notes, partly unverified):**
  - PyTorch MPS is workable for encoder fine-tuning. fp16 backward on MPS has produced NaNs in the past, and fp32 doubles memory (possibly outdated) — [mac-playbooks](https://svah-x.github.io/mac-playbooks/playbooks/pytorch-mps) (from `Personal writing style models/apple_silicon_stack.md`)
  - The project plan estimates a ModernBERT-base fine-tune at about 30-60 min on MPS (estimated, `plan.md`).

### Inferences
- **Backbone choice (estimated; specs from general knowledge [unverified]).**
  - ModernBERT-base (~149M params, 8k context) is the default: long context fits whole articles, and it fits easily in 24 GB at fp32 with batch 16 × 512 tokens.
  - DeBERTa-v3-large (~435M) is the accuracy alternative at 512 tokens.
  - A frozen-encoder + logistic-regression variant (FineWeb-Edu style) trains in minutes and is the fast-iteration baseline.
  - MLX has no mature encoder fine-tuning path in prior notes, so use PyTorch MPS for the classifier and keep MLX for the 7-9B adapter.
- **Throughput (estimated, not measured).** ModernBERT-base at 512 tokens on an M4 Pro might reach on the order of 15-40 training samples/s.
  - That puts 200k documents × 2 epochs at roughly 3-7 hours, and 40k documents under an hour.
  - Inference at about 100-300 docs/s means a 1M-document pool can be scored overnight.
  - Measure throughput on day 1; no published M4 Pro encoder benchmark was found.
- **Data needed (inferred from Pangram).** Gains saturate around 40k examples per domain. For one domain (informational nonfiction, a few sub-genres), about 40-100k balanced examples plus 2-3 hard-negative-mining rounds over a ≥200k held-out human pool is the right order. Generating 50k mirrors with a local 7-9B model is slow (≈35 tok/s single stream in prior notes, so about 7 days for 50k × 500 tokens, estimated). Use batched local generation or a cheap API, and include several generator families plus quill's own adapter.
- **Robustness to quill's own outputs is the central risk.** The Chakrabarty result implies any detector trained without fine-tuned-style-model outputs will score the adapter as human. Two consequences:
  1. Include adapter generations, from several checkpoints, as positives in training. This is trivial because their provenance is known.
  2. **Separate two targets.** *Provenance* (is this AI?) is uninformative for quill, since every output is AI. *AI-tell or slop salience* (does this read as AI or sloppy to a reader?) is what quill needs. The second requires human judgments, not provenance labels.
- **Calibration.** Fit temperature scaling (one parameter; Guo et al. 2017, standard reference [not re-fetched this session]) per source family on gold. Then set per-family thresholds at a target FPR, with Clopper-Pearson upper bounds (section 9). Calibrate on a split of gold that was never used for model selection.
- **Active learning (inferred).** Pangram's hard-negative mining is uncertainty and error sampling over a known-human pool. For a few hundred user labels, the analogue is: each round, have the user label about 100 items from (a) top-scored post-2023 documents in sources with low α, (b) quill outputs near the decision threshold, and (c) disagreements between ModernBERT and the style-embedding detector. Fold the labels into both the gold calibration set and the training set, following Zhu et al.: clean labels are worth more as training data than as validation-only data, so keep a fixed untouched test slice.

### Gaps
- No published comparison of a weakly supervised local detector against Pangram on informational nonfiction.
- No measured ModernBERT or DeBERTa training or inference throughput on M-series GPUs.
- No study of active learning for AI-text detection with a few hundred labels.
- No published detection rates for small (7-9B) open models fine-tuned on a single nonfiction author.
- No primary source confirming ModernBERT parameter counts this session.

---

## 7. Uses in the quill pipeline: evidence for each, and the accuracy level each one needs

### Takeaway
Ordered from safest to riskiest:
1. Corpus-level eval (α-style metric, held-out detectors)
2. Source of contrastive tell lexicons for FTPO and banlists
3. A soft rerank feature in best-of-N, using a *different* model than the eval
4. FTPO pair mining
5. Detector reward in rejection sampling or a preference stage, which has the strongest evidence of Goodhart failure

Detector scores also correlate poorly with quality differences inside one model's outputs (Pangram is near random on non-AI-vs-human quality pairs). So no detector should be the sole objective.

### Cited Findings
- **Reward hacking:**
  - DPO for under a day against a detector's "human" score on Llama-2-7B cut OpenAI's RoBERTa-large detector AUROC from 0.84 to 0.62/0.63, and the evasion transferred to other detectors — [Nicks et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1f9f07df0992ce21698d800eaa891bd8-Abstract-Conference.html)
  - DPO against Fast-DetectGPT drove that detector's AUROC to 0.18, while a style-based detector held at 0.95 — [arXiv 2505.14608](https://arxiv.org/html/2505.14608v1)
  - (both from prior notes)
- **Detectors are weak quality rankers:** Pangram scored 65.0% on the WQ benchmark and was "near random on pairs that don't involve AI-vs-human distinctions". WQRM best-of-20 picks were preferred by experts 66% of the time (72.2% at reward gap >1) — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3) (from prior notes)
- **Lexical tells exist at corpus level but fade after fine-tuning:**
  - Liang et al.'s adjective shifts ("commendable," "meticulous," "intricate") are strong at population level — [arXiv 2403.07183](https://arxiv.org/html/2403.07183v2)
  - Cliché density's mediating role fell from 16.4% to an insignificant 1.3% after fine-tuning on an author — [arXiv 2510.13939v3](https://arxiv.org/html/2510.13939v3)
- **FTPO** gets about 90% suppression of targeted patterns with under 1% quality loss on creative writing, vs DPO at about 80% suppression with about 15% degradation (self-reported). Its data comes from backtracking-sampler events — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061); [auto-antislop](https://github.com/sam-paech/auto-antislop) (from prior notes)
- **Population metrics resist per-sample gaming:** Liang-α is about 3-5× more accurate than instance-level detectors at estimating corpus fractions (measured, 1.8-2.4% vs 6.2-11.2% error) — [arXiv 2403.07183v2](https://arxiv.org/html/2403.07183v2)

### Inferences
Accuracy needed for each use (my judgment, based on the findings above):

| Use | What it needs from the classifier | Minimum validated accuracy (proposed) | Main risk | Guardrail |
|---|---|---|---|---|
| (a) Eval metric | Good ranking at population level; calibration-in-the-large | AUROC ≥0.85 on held-out sources *and* on adapter-vs-author samples; α estimator within ±3 pts on synthetic mixtures | Blind to the adapter's style (Chakrabarty 97% → 3%) | Report three independent signals: Liang-α, a style-embedding detector, and Pangram on a sample. Never optimize against the eval models. |
| (b) Best-of-N soft rank feature or gate | Ranking *within* one model's outputs | Within-model pairwise agreement ≥65% against user judgments on ≥100 pairs (WQRM-level); as a gate, FPR on the author's own held-out text ≤2% | Goodhart: selects evasive rather than better text; detectors are near random on within-AI quality | Use the classifier as one feature next to style-verifier and meaning scores. Eval uses a different detector family. Watch for divergence between the rerank score and the held-out detector. |
| (c) Tell-lexicon mining | Only high-confidence pools (top or bottom 5%) | Precision ≥95% at the chosen cutoffs (pool purity); recall irrelevant | Mining topic or era words instead of tells (temporal shortcut) | Mine contrastively on *topic-matched* pools (mirrors, Grokipedia/Wikipedia pairs). Keep tokens over-represented in AI across ≥3 sources. Confirm the adapter actually emits them before banning. |
| (d) Reward for rejection sampling or preference training | Robust to optimization pressure | No accuracy level is sufficient alone; detectors break within a day of DPO | Evasion without quality gain; transfers to other detectors | Prefer rejection sampling with a hard cap (top-k of N, small N) over gradient-based optimization against the detector. Always re-measure with held-out detectors and human reads. |
| (e) FTPO pair mining | Token-level candidates, not document labels | Lexicon precision as in (c); the document classifier is not needed | Suppressing legitimate domain vocabulary | Every rejected token gets on-domain alternatives (FTPO design). Re-check the author-style verifier after training. |

- Uses (a), (c) and (e) are justified at the accuracy a weakly supervised local classifier can realistically reach (AUROC about 0.85-0.95 OOD). Use (b) is justified only after the within-model ranking test. Use (d) should not use the local classifier as a gradient signal at any accuracy.

### Gaps
- No study measures whether best-of-N on a detector score improves human-judged quality in informational nonfiction.
- No FTPO evaluation on nonfiction or on 7-9B models other than those in the paper.

---

## 8. Key question: can weak supervision over these priors produce a local classifier approaching Pangram (≥95% TPR at ≤2% FPR on nonfiction)?

### Takeaway
There is no published evidence that weak supervision over wild-data priors reaches Pangram-level accuracy, and the strongest evidence points the other way. Pangram reached its numbers with millions of confirmed-human documents, topic-matched synthetic mirrors and hard-negative mining, not weak labels. Open supervised encoders that score 99% in-distribution fall to AUROC ≈0.86 OOD. A solo builder can plausibly reach ≥95% TPR at ≤2% FPR **in-distribution** (raw chatbot informational text vs pre-2022 human prose). On humanized, style-imitated or fine-tuned text, including quill's adapter, expect far less. That OOD figure is an estimate, with no direct measurement.

### Cited Findings
- **Pangram reached its accuracy without weak supervision.** Its route was confirmed human data, mirrors and hard-negative mining. FPR before mining was already 2.29% domain-weighted (5.34% on Wikipedia) at 360k-1M examples, and it took mining to reach 0.02% — [arXiv 2402.14873v3](https://arxiv.org/html/2402.14873v3)
- **Independent measurement:** Pangram 98.0% TPR at 2.0% FPR on 300 nonfiction articles, 90.0% on humanized — [arXiv 2501.15654](https://arxiv.org/html/2501.15654)
- **Even Pangram misses author-tuned and style-imitated text:** 3% detection on author-fine-tuned GPT-4o outputs; 10% miss on style imitation, 25% on scientific — [arXiv 2510.13939v3](https://arxiv.org/html/2510.13939v3); [Epoch AI](https://epoch.ai/data-insights/ai-detectors-false-negatives)
- **Open supervised detectors collapse OOD:** RoBERTa-L about 60% on unseen generators — [RAID](https://arxiv.org/html/2405.07940). ModernBERT-large at Beemo AUROC 0.856 — [Vanguard card](https://huggingface.co/ShantanuT01/vanguard-ai-text-detector). Generic-trained detectors lose 10-40% on realistic Wikipedia edits — [TSM-Bench](https://iclr.cc/virtual/2026/poster/10006430)
- **The weak-supervision ceiling, where measured, sits just below hand labels:** Snorkel came within an average 3.6% of large hand-labeled sets on IE tasks — [Snorkel](https://pmc.ncbi.nlm.nih.gov/articles/PMC5951191). WSL methods lose to training on more than 10 clean examples per class — [Zhu et al.](https://arxiv.org/pdf/2305.17442)
- **PU gains for AI-text detection are small:** about +0.4 to +2.6 F1 — [MPU](https://arxiv.org/html/2305.18149v4)

### Inferences
- **Most of the value of weak supervision here is in evaluation, not training.** The priors (self-disclosed and artifact-leak AI, producer-flagged sites, Wikipedia-tagged articles) give *wild*, real-distribution positives that synthetic mirrors lack. They are most valuable as a realistic test set and as hard positives for later training rounds.
- **The bulk of training signal should come from a Pangram-style recipe:**
  - pre-2022 human informational prose;
  - topic- and length-matched mirrors from many current LLMs, including paraphrased, humanized and style-imitated variants and quill adapter outputs;
  - 2-3 rounds of hard-negative mining over a large held-out human pool.
- **A realistic target (estimated):** ≥95% TPR at ≤2% FPR on held-out in-distribution generators. AUROC 0.85-0.95 on leave-one-source-out wild data. Low, unknown detection on adapter outputs until they are included in training.
- **Pangram as a teacher.** An option is to score a few thousand unlabeled documents with the Pangram API and distill. This is likely the single strongest LF, but check Pangram's terms of service on training with its outputs [unverified].

### Gaps
- No direct head-to-head between any weakly supervised or PU-trained local detector and Pangram on nonfiction.
- Pangram's ToS on distillation not checked.

---

## 9. Key question: what is the minimum gold set to calibrate and validate?

### Takeaway
Validating an FPR claim of ≤2% at 95% confidence needs at least 150 human documents with zero false positives per reported domain. With a realistic observed FPR of about 1%, it needs 500-1,000 per domain. Estimating TPR to ±3 points needs about 300-400 AI documents per condition. Temperature scaling needs only a few hundred mixed examples. Quill-specific gold is the bottleneck: AI provenance labels for adapter outputs are free, but "reads as AI or sloppy" labels need human judgment. Plan for about 200-400 user-judged adapter outputs plus 100-200 held-out author passages.

### Cited Findings
- RAID and Pangram both report accuracy at a fixed FPR and set thresholds per domain. A global threshold can give domain FPRs of 20-33% — [RAID](https://arxiv.org/html/2405.07940); [Pangram](https://arxiv.org/html/2402.14873v3)
- Epoch's 495-passage human set gives a 90% CI of 0-0.54% on 0 false positives — [Epoch AI](https://epoch.ai/data-insights/ai-detectors-false-negatives)
- Existing gold available to the project:
  - Human Detectors (300 nonfiction) — [arXiv 2501.15654](https://arxiv.org/html/2501.15654)
  - the Epoch set (495 pre-2022 human passages plus 297 AI per condition, public CSV) — [repo](https://github.com/jaeholee-brown/ai-text-detectors)
  - Wikipedia {{AI-generated}} (~7.6k) and Beemo (~1.6k), from the project brief
- Zhu et al.: once there are more than 10 clean examples per class, use them in training as well as validation — [arXiv 2305.17442](https://arxiv.org/pdf/2305.17442)

### Inferences
- **One-sided 95% Clopper-Pearson upper bounds on FPR** (computed this session, exact binomial):

  | Human docs (n) | 0 FP | ~0.5% observed FP | ~1% observed FP |
  |---|---|---|---|
  | 150 | ≤1.98% | – | ≤3.12% |
  | 300 | ≤0.99% | ≤1.57% | ≤2.56% |
  | 500 | ≤0.60% | ≤1.25% | ≤2.09% |
  | 1,000 | ≤0.30% | ≤1.05% | ≤1.69% |
  | 2,000 | ≤0.15% | ≤0.85% | ≤1.45% |

- **TPR precision** (95% normal-approximation half-width, computed):
  - n = 200: ±4.2 pts at TPR 0.90, ±3.0 at 0.95
  - n = 400: ±2.9 / ±2.1
  - n = 1,000: ±1.9 / ±1.4
- **Minimum recommended gold set (estimate):**
  - **Human side:** about 1,000 verified-human informational documents across the 3-4 target sub-genres, ideally 2023+ human text to break the date shortcut. The author's own held-out passages (≥150) give an author-specific FPR, since a gate must not reject the target author.
  - **AI side:** about 400 per stress condition (raw, paraphrased or humanized, style-imitated, quill adapter). Human Detectors, Beemo and Wikipedia-tagged articles supply the wild conditions.
  - **Calibration split:** about 300-500 mixed items, disjoint from test.
  - **Quill quality target:** 200-400 user-judged adapter outputs in about 100-item active-learning rounds (section 6), plus a frozen 100-item test slice.

### Gaps
- No source sets an accepted minimum gold size for AI-text detector validation. The numbers above are my binomial arithmetic.
- Label noise in Wikipedia {{AI-generated}} tags is unknown, so measure it on a 100-item audit.

---

## 10. Key question: what concrete pipeline would a solo builder run, at what compute, on a 24 GB M4 Pro?

### Takeaway
LFs → (optional) label model → PNU-trained ModernBERT-base on PyTorch MPS → hard-negative mining → per-family temperature scaling and FPR thresholds → leave-one-source-out and adapter-output validation. Roughly 2-3 weeks of part-time work. Compute is dominated by mirror generation (days locally, or hours via API). Classifier training is hours, and scoring a 1M-document pool is roughly one night (all estimated).

### Cited Findings
- **Component precedents:**
  - mirror generation and hard-negative mining — [Pangram](https://arxiv.org/html/2402.14873v3)
  - `LabelModel` with `class_balance` and abstains — [Snorkel docs](https://snorkel.readthedocs.io/en/v0.9.7/packages/_autosummary/labeling/snorkel.labeling.model.label_model.LabelModel.html)
  - nnPU — [Kiryo et al.](https://arxiv.org/abs/1703.00593)
  - corpus α as a prior — [Liang et al.](https://arxiv.org/html/2403.07183v2)
  - time-prior threshold calibration at 1% FPR — [Brooks et al.](https://arxiv.org/html/2410.08044v1)
  - style-embedding detector — [Soto et al.](https://arxiv.org/pdf/2401.06712)
  - fixed-FPR, per-domain evaluation — [RAID](https://arxiv.org/html/2405.07940)
  - shortcut baselines — [Jung et al. EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2177/)
- **Local generation speed** is about 35 tok/s single stream for a 7-9B 4-bit model on this machine (estimate in `plan.md`; not independently measured).

### Inferences
The concrete pipeline (all compute figures estimated):
1. **Pools (1-2 days).**
   - H = certain human: Wikipedia revision snapshots before 2022, news and blog archives from 2021 or earlier, author corpora, about 200-500k documents. Hold out 50% for mining and FPR.
   - A_wild = certain AI from self-disclosure and artifact leaks. Strip the leak strings.
   - A_pair = Grokipedia articles paired with Wikipedia, deduplicated for overlap.
   - U = unlabeled post-2023 informational web, about 0.5-1M documents.
   - Normalize all text to plain text.
2. **Mirrors (≈1-7 days).** 40-100k AI mirrors of sampled H documents (same title, outline or opening; matched length), from ≥4 model families, plus about 20% paraphrased or humanized and about 10% style-imitated variants. Add about 2-5k quill-adapter generations per checkpoint. Batched local generation or a low-cost API cuts this from about a week to under a day.
3. **LFs (2-3 days).** About 10-15 LFs on U:
   - Binoculars band and Fast-DetectGPT band (both run locally on the 7-9B base and fit in 24 GB at 4-bit);
   - Liang-α word likelihood ratio;
   - slop-lexicon density;
   - a StyleDistance kNN vote;
   - a merged producer score;
   - Pangram on a ≤5k sample (subject to ToS).
   
   Inspect overlaps and conflicts, and fit `LabelModel` with `class_balance` from per-slice α. The fit takes seconds to minutes on CPU, and FlyingSquid is faster still.
4. **Baselines first (hours).**
   - a format-only logistic regression (shortcut ceiling);
   - year and topic probes;
   - a gold-only classifier (Zhu et al. bar);
   - a frozen-encoder + logistic-regression model.
5. **Main classifier (hours per run).** ModernBERT-base on PyTorch MPS (fp32 or bf16 if stable), 512-1,024 tokens, 2 epochs. Loss = cross-entropy on (H vs mirrors + A_wild + adapter) + γ·nnPU on U with per-slice π = α. Split by author or domain.
6. **Hard-negative mining (2-3 rounds, each about a day including regeneration).** Score the held-out H half, take the top false positives (≤10k), generate mirrors for them, and retrain.
7. **Calibration (minutes).** Temperature-scale per source family on the calibration split. Set thresholds at 1% and 2% FPR per family and report Clopper-Pearson bounds.
8. **Validation (1-2 days).**
   - Human Detectors 300 and the Epoch set; Beemo; Wikipedia-tagged vs time-matched untagged.
   - Leave-one-generator-out and leave-one-source-out.
   - Adapter outputs vs the author's held-out text.
   - Agreement with the Liang-α of each slice.
   - Compare on a 300-500 document overlap with Pangram scores as an external anchor.
9. **Deploy into quill per section 7.** Use ModernBERT as a rerank feature only. Hold out the StyleDistance detector, Liang-α and Pangram-sample for eval. Mine lexicons from topic-matched top and bottom pools for the banlist and FTPO. Do not use any detector as a DPO or GRPO reward.
10. **Active-learning loop (ongoing).** About 100 user labels per round from the disagreement and threshold regions. Retrain weekly, and keep a frozen test slice.

### Gaps
- No measured end-to-end timings for this pipeline on M4 Pro.
- No primary benchmark of ModernBERT on MPS.
- Local Binoculars and Fast-DetectGPT throughput at 7-9B on 24 GB not measured.
