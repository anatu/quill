# AI-writing tells (lexicons, pattern taxonomies) and automatic weak labelers (detectors, slop scorers): catalog, accuracy evidence, failure modes

Compiled 2026-11-07. Every item is dated where a date was available. **[VENDOR]** marks claims by the company selling the tool. **[UNVERIFIED]** marks claims taken from search snippets or secondary blogs that I could not check against a primary source. **[LOCAL]** marks numbers I computed myself from public data files (scratch files in `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/negsignal/`).

Project lens: a QLoRA style model (7-9B, MLX, M4 Pro 24 GB) writing informational/instructive nonfiction in one human author's voice. "Negative labels" here means marking outputs (or spans/tokens) as slop for rejected examples, token penalties, or reranking.

---

## Q1. Which weak labelers are accurate enough (precision/recall) to label negatives automatically for informational prose?

### Takeaway
Only one detector, Pangram (commercial, cloud), has independent evidence of high precision *and* recall on nonfiction/informational text, including humanized text: 98.0% TPR at 2% FPR on 300 nonfiction articles, and FPR ≤0.1% on a 1,992-passage multi-genre audit. Every open-source, locally runnable detector is far weaker, especially after paraphrase/humanization: Binoculars falls to 6.7% TPR and Fast-DetectGPT to 23.3% on humanized nonfiction. Slop-lexicon scores and LLM judges have **no published document-level precision/recall**, and in the one study that checked, they barely track human "slop" judgments (LLM-judge κ≈0.01; metric-based AUPRC 0.52-0.55 against a 0.25-0.27 base rate). All of these detectors were validated on whether text is AI-written at all. None was validated on ranking outputs *within* one fine-tuned small model, which is what negative mining for this project needs.

### Cited Findings

**Independent evaluations on nonfiction / informational text (most relevant)**
- Russell, Karpinska and Iyyer (ACL 2025; arXiv Jan 2025) had annotators and detectors classify 300 nonfiction English articles. The AI articles came from GPT-4o, Claude, o1-Pro, paraphrased GPT-4o, and o1-Pro "humanized" by prompting it to avoid AI vocabulary. Overall TPR (FPR) by detector: Pangram 98.0 (2.0); "Pangram Humanizers" 99.3 (2.7); GPTZero 85.3 (0.7); Fast-DetectGPT (threshold at FPR=0.05) 80.0 (7.2); Binoculars at its accuracy threshold 66.7 (1.3); Binoculars at its low-FPR threshold 40.0 (0); RADAR 15.3 (2.0). Majority vote of 5 expert human annotators: 99.3 (0). — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- In the same study, on **humanized o1-Pro articles only**, TPR (FPR) was: Pangram 90.0 (6.7); Pangram Humanizers 96.7 (10); GPTZero 46.7 (3.3); Fast-DetectGPT 23.3 (3.3); Binoculars 6.67 (0) at the accuracy threshold and 0 at low-FPR; RADAR 0 (3.3). From base o1-Pro to humanized, TPR fell for every detector: Pangram 100→90.0; GPTZero 76.7→46.7; Fast-DetectGPT 86.7→23.3; Binoculars 73.3→6.67. — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- Same study, prompted LLMs as detectors: the best GPT-4o configuration (zero-shot + CoT + guide) reached 78.0 TPR at 10.7 FPR, and the best o1 configuration 54 TPR at 4 FPR. — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- Same study, humans: individual expert TPR (FPR) ranged from 59.3 (2) to 97.3 (6), and one expert scored 88.0 TPR at 12 FPR. Nonexperts averaged 56.7% TPR at 51.7% FPR, which is near chance. (The paper's body text and Table 1 give slightly different FPRs.) — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- Jabarian and Imas (NBER WP 34223, Sept 2025) audited 1,992 passages across six genres: news, blogs, consumer reviews, novels, restaurant reviews and résumés. Verified human text was matched to AI text from GPT-4.1, Claude Opus 4, Claude Sonnet 4 and Gemini 2.0 Flash, with GPT-3.5 in the appendix. Passages were length-matched (e.g., news: 459.9 words human, 458.4 AI). — [Jabarian & Imas 2025](https://www.nber.org/papers/w34223)
- Same audit, FPR on human text across detector thresholds 0.1-0.9: Pangram 0.0010→0.0000; Originality 0.0027→0.0011; GPTZero 0.0071 (flat); the open-source `roberta-base` detector 0.977→0.899. That means RoBERTa-base flagged about 90-98% of human passages as AI. — [Jabarian & Imas 2025](https://www.nber.org/papers/w34223)
- Same audit, FNR: Pangram 0.0045-0.038, depending on threshold and generator; GPTZero 0.002-0.030; Originality up to 0.300 at threshold 0.1 and 0.424 at 0.9 for some generators. AUROC for Pangram was ≈1.0 in nearly all genre×model cells; the lowest was 0.9998 for GPT-4.1 news. Accuracy drops on "stubs" under 50 words. — [Jabarian & Imas 2025](https://www.nber.org/papers/w34223)
- Same audit, after every AI passage was run through the StealthGPT humanizer (Table B.4), FNR on news passages was: GPTZero 0.35-0.57; Originality 0.04-0.07; Pangram 0.013-0.037; RoBERTa 0.57-0.95. Across all genres, GPTZero "largely loses its capacity to detect" humanized text (FNR around 0.50 and above). — [Jabarian & Imas 2025](https://www.nber.org/papers/w34223)
- Same audit, API cost per passage: Pangram $0.0038 (Amazon review) to $0.0099 (blog); OriginalityAI $0.0070-$0.0179; GPTZero $0.0096-$0.0246. — [Jabarian & Imas 2025](https://www.nber.org/papers/w34223)
- Caveat on the above: Pangram-hosted pages amplify the Jabarian & Imas results **[VENDOR]**. A secondary review reports that GPTZero disputed the study's ranking in Jan 2026 **[UNVERIFIED]**. — [Pangram blog](https://pangram.com/blog/ai-detection-actually-works); [gradpilot summary](https://gradpilot.com/news/ai-detector-false-positive-rates-compared)

**Graded / continuous labelers**
- EditLens (Thai, Emi, Masrour, Iyyer; arXiv Oct 2025; ICLR 2026) is a regression head on a fine-tuned open LLM. It predicts the *extent* of AI editing as a continuous score. Reported binary (human vs. any AI) F1 is 94.7%, and three-way (human / AI-edited / AI-generated) macro-F1 is 90.4%, 16% better than the prior best. It reportedly generalizes to Enron emails, Llama-3.3-70B, and multi-edited text. Two of the four authors are at Pangram Labs, so this is academic work with vendor involvement. — [EditLens arXiv](https://arxiv.org/html/2510.03154v1); [ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10008153)

**Benchmarks of robustness (RAID, ACL 2024)**
- RAID contains 6M+ generations from 11 generators across 8 domains (News, Wiki, Reddit, Books, Abstracts, Reviews, Poetry, Recipes), with 11 adversarial attacks and 4 decoding strategies, and tested 12 detectors. — [Dugan et al. RAID](https://arxiv.org/html/2405.07940)
- RAID, TPR at FPR=5%, unattacked → under attack: Binoculars 79.6 → 80.3 paraphrase, 43.5 synonym swap, 37.7 homoglyph. Originality 85.0 → 96.7 paraphrase, 9.3 homoglyph. GPTZero 66.5 → 64.0 paraphrase, 66.2 homoglyph. RADAR 70.9 → 67.3 paraphrase. — [RAID](https://arxiv.org/html/2405.07940)
- RAID: adding a repetition penalty cut accuracy "by up to 32 points regardless of decoding strategy." Changing generator, decoding or penalty produced "up to 95+% error rate." — [RAID](https://arxiv.org/html/2405.07940)
- RAID: with one global threshold, per-domain FPR varies widely, e.g., ZeroGPT 48% on Wiki and 29% on News; Originality 13% on Wiki; RADAR 20.4% on Reviews. The authors therefore calibrate thresholds per domain. A RoBERTa detector trained on GPT-2 reaches 95%+ on GPT-2 text but "rarely achieves beyond 60%" on other generators. — [RAID](https://arxiv.org/html/2405.07940)
- A RAID shared task reported over 99% accuracy at 5% FPR, but only for generators and domains seen in training. — [RAID search summary](https://arxiv.org/abs/2405.07940)

**Zero-shot open detectors (local options)**
- Binoculars (Hans et al., Jan 2024) claims over 90% detection of ChatGPT text at 0.01% FPR with no ChatGPT training data, measured on 2023-era generators. The reference implementation uses Falcon-7B plus Falcon-7B-Instruct with one fixed global threshold. The README says it is "for academic purposes only," that it is better at English than other languages, and that it should not be used "without human supervision." — [Binoculars paper](https://arxiv.org/abs/2401.12070); [Binoculars GitHub](https://github.com/ahans30/Binoculars)
- Fast-DetectGPT reports AUROC 0.9338 on ChatGPT/GPT-4 text in the black-box setting (DetectGPT: 0.7225), with a 340× speedup. The demo defaults to gpt-neo-2.7B for both sampling and scoring. A 2026-01-31 repo update ranks scoring-model pairs as "Llama3-8B/Llama3-8B-Instruct > falcon-7b/falcon-7b-instruct >> gpt-j-6B/gpt-neo-2.7B," especially on text from reasoning models. Experiments ran on an A100 80 GB. — [Fast-DetectGPT GitHub](https://github.com/baoguangsheng/fast-detect-gpt)
- A separate evaluation (arXiv 2412.05139) argues high AUROC "does not necessarily translate into real-world performance," with TPR at 1% FPR as low as 0% in some settings. — [arXiv 2412.05139](https://arxiv.org/pdf/2412.05139v4)
- Supervised open classifiers on Hugging Face: `desklib/ai-text-detector-v1.01` (DeBERTa-v3-large) says on its model card that it "leads the RAID Benchmark" **[self-reported; current rank not verified]**. Community models such as `Lindarixon/Linda-RAID` report about 99.7 on local RAID validation, with no official score. — [desklib model card](https://huggingface.co/desklib/ai-text-detector-v1.01); [Linda-RAID](https://huggingface.co/Lindarixon/Linda-RAID)

**False positives on human text and non-native writers**
- Liang et al. (arXiv Apr 2023; *Patterns* 2023) tested 7 detectors on 91 human TOEFL essays and 88 US 8th-grade essays. Average FPR on TOEFL essays was about 61% (reported as 61.22% and 61.3%). All 7 detectors flagged 18/91 (19.8%), and at least one detector flagged 89/91 (97.8%). Native essays were classified accurately. The authors attribute this to the low perplexity of constrained non-native prose. — [Liang et al. 2023](https://arxiv.org/abs/2304.02819)
- Pangram claims 0.032% FPR on four held-out ESL datasets, versus a 0.01% general FPR, and zero false positives on Liang's 91 TOEFL essays. It concedes that n=91 limits precision **[VENDOR]**. I found no independent ESL test of Pangram. — [Pangram ESL blog](https://www.pangram.com/blog/how-accurate-is-pangram-ai-detection-on-esl)
- Graphite's 2025 study of AI share on the web used Surfer's detector. It reports a 4.2% FPR on human articles, with FNR (0.6%) measured only on GPT-4o articles **[UNVERIFIED, from snippet]**. — [Axios on Graphite](https://www.axios.com/2025/10/14/ai-generated-writing-humans)
- Wikipedia's AI Cleanup guide (live, Nov 2026) says detectors "have non-trivial error rates," can be fooled by paraphrasing, markup, or newer models, and that a high detector score is not grounds for speedy deletion (G15). — [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

**Slop scorers and LLM judges as labelers**
- slop-score computes 60% slop-word rate + 25% "not-X-but-Y" contrast patterns + 15% slop-trigram rate. Contrast detection uses 10 surface regexes plus 35 regexes over POS-tagged text. The README reports **no validation against human judgments** and no accuracy figures. — [slop-score GitHub](https://github.com/sam-paech/slop-score)
- Shaib, Chakrabarty, Garcia-Olano and Wallace ("Measuring AI 'Slop' in Text," arXiv Sept 2025) had experts label 213 news articles and 123 MS MARCO QA passages. On the binary "slop" label, the LLM judges scored: GPT-5 κ=0.01 (precision 0.38, recall 0.12); o3-mini κ=0.03 (0.42/0.08); DeepSeek-V3 κ=−0.01. — [Shaib et al. 2025](https://arxiv.org/html/2509.19163v2)
- Same paper, comparison points: a linear model over all available automatic text metrics reached only AUPRC 0.52 on news (base rate 0.25) and 0.55 on MS MARCO (base rate 0.27). A writing-quality reward model correlated 0.25 (news) and 0.15 (MS MARCO) with the binary label. A fine-tuned Qwen-7B span tagger reached span precision 0.33, recall 0.22, F1 0.26. — [Shaib et al. 2025](https://arxiv.org/html/2509.19163v2)
- Same paper: human agreement on the binary slop label was itself low, with Cohen's κ from −0.15 to 0.29 across annotator pairs and Gwet's AC1 from 0.12 to 0.42. Annotators agreed more on spans (paragraph-level span precision 0.65-0.80). The number of annotated problem spans correlated with the slop label (ρ=0.63 overall). — [Shaib et al. 2025](https://arxiv.org/html/2509.19163v2)

### Inferences
- **The detector label is mostly redundant for this project.** Every candidate negative is the model's own output, so it is AI-written by construction, and a binary "is this AI?" label adds nothing. What negative mining needs is a *graded, within-model* ranking of how AI-like or sloppy each output is. Only EditLens-style continuous scores, span taggers, or lexicon/pattern rates do that, and none has published validation as a ranker within a single model.
- **Distribution shift is the main reliability risk.** Every strong result above (Pangram, GPTZero) comes from frontier commercial generators (GPT-4o/4.1, Claude 4, o1-Pro, Gemini 2.0). The project's outputs will come from a QLoRA'd 7-9B open model, sampled with whatever decoding settings are used and steered toward one human's voice. RAID shows that detectors lose up to 95+ points under exactly these shifts (unseen generator, sampling, repetition penalty). Precision/recall for this setting must be measured on a project-specific held-out set and cannot be borrowed.
- **Using a detector as a training signal is adversarial.** Humanizers already show that optimizing text against a detector moves the score without necessarily improving the text (Fast-DetectGPT 86.7→23.3 TPR after a simple "avoid AI vocab" rewrite). Using any detector score as a reward, DPO-rejection criterion, or reranker invites the same Goodharting. Pangram looks the most robust, but it is a cloud API, which conflicts with a local-only pipeline and would need about $0.004-0.01 per passage at scale.
- **Local feasibility on 24 GB unified memory (my estimate from parameter counts, not from measurements):**
  - Fast-DetectGPT with gpt-neo-2.7B (roughly 5-6 GB in fp16) fits easily.
  - The recommended Llama3-8B/8B-Instruct pair is about 32 GB in fp16 and would need 8-bit or 4-bit quantization. How quantization affects the detection curves is unvalidated.
  - Binoculars' Falcon-7B pair is about 28 GB in bf16, which also does not fit without quantization or smaller substitute models, and those are uncalibrated.
  - DeBERTa-large classifiers (about 435M parameters) and slop-score (regex plus word list) are trivial to run.
  - All the reference code is PyTorch, so running on MLX means porting the code or using MPS.
- **Precision is achievable; recall on subtle slop is not.** For flagging blatant negatives (dense AI vocabulary, contrast templates, markdown scaffolding), pattern counts have high precision on raw small-model output. For subtle problems (density, relevance, tone: the strongest predictors of human slop judgments in Shaib et al.), no automatic labeler has demonstrated useful recall.

### Gaps
- No independent study reports Pangram, GPTZero or Originality accuracy on **small open-weight models (7-9B)**, on **LoRA fine-tuned** models, or on text written in a specific human's imitated voice.
- I did not retrieve GPTZero's or Originality.ai's own technical claims, so their vendor-stated FPRs are not catalogued here.
- I could not access the live RAID leaderboard (raid-bench.xyz/leaderboard returned 404), so current top TPR at 1% FPR and Pangram/Desklib placement there are unverified.
- I found no evidence that EditLens weights are publicly released, so local use is unconfirmed.
- No paper reports document-level precision/recall of slop-score, the antislop lists, or Kobak-style lexicons as per-document labelers. Kobak and Liang explicitly say their methods are corpus-level only.

---

## Q2. Which lexicons and pattern catalogs are current as of 2026, and how were they derived and validated?

### Takeaway
The data-driven lexicons fall into two groups. One group comes from **corpus-level excess-frequency studies of scientific abstracts (2024 data)**: Kobak's 900 words, Juzek & Ward's 21 focal words, Liang's distributional estimator. These are validated only as population estimators. The other group is **Sam Paech's antislop / slop-forensics / slop-score lists**. These are derived from frequency ratios (LLM vs. wordfreq + Reddit/Gutenberg) on **creative-writing** prompts, were last updated in Nov 2025, and have no human-judgment validation. They are dominated by fiction vocabulary: fantasy names, "voice barely whisper." Most of them do not transfer to informational prose. The most current catalog is Wikipedia's "Signs of AI writing," which as of Oct-Nov 2026 is organized by model era and marks em-dashes, section summaries and promotional tone as *historical*. It is expert-curated, not quantitatively validated. Tells drift quickly: "delve" collapsed after April 2024, OpenAI suppressed em-dashes in GPT-5.1 (Nov 2025), and new mid-2026 tells such as "rather than" parallelisms and "does not establish" disclaimers have appeared. Any lexicon used for training should therefore be regenerated from this project's own base model against this project's own human corpus.

### Cited Findings

**A. Corpus-level excess-vocabulary studies (scientific writing)**
- Kobak et al. (*Science Advances* 11(27) eadt3813, 2025; arXiv v5) studied 15.1M PubMed abstracts from 2010-2024. Method: for each word, frequency p in 2024 versus a counterfactual q projected linearly from 2021-2022, with 2023 deliberately excluded; excess gap δ=p−q and ratio r=p/q. A word counts as excess if δ>0.01 or log₁₀r > (log₁₀2/4)·log₁₀p. — [Kobak et al. v5](https://arxiv.org/html/2406.07016v5)
- Kobak findings: 454 excess words in 2024, versus a maximum of 190 in Covid-era 2021. 379 were style words (66% verbs, 14% adjectives). Top rare words: delves r=28.0, underscores r=13.8, showcasing r=10.7. Top common words: potential δ=0.052, findings δ=0.041, crucial δ=0.037. Lower bound of LLM-processed 2024 abstracts: 13.5%, ranging from under 5% to over 40% by subcorpus (e.g., UK/Australia about 0.05; China/S. Korea/Taiwan about 0.20; Chinese computational papers 0.41). All 900 excess words for 2013-2024 are released. — [Kobak et al. v5](https://arxiv.org/html/2406.07016v5); [berenslab/llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab)
- Kobak limitations, as stated by the authors: the result is a lower bound, works at corpus level only, cannot identify individual abstracts, and cannot separate LLM use from humans adopting LLM words. Differences between subcorpora may reflect detectability, for example native speakers removing unnatural words. — [Kobak et al. v5](https://arxiv.org/html/2406.07016v5)
- Liang et al., "Mapping the Increasing Use of LLMs in Scientific Papers" (COLM 2024): a distributional estimator over 950,965 papers (Jan 2020-Feb 2024) found that the estimated LLM-modified fraction α reached 17.5% of CS abstracts and 15.3% of CS introductions. — [Liang et al. 2024](https://arxiv.org/abs/2404.01268)
- Liang et al., "Monitoring AI-Modified Content at Scale" (ICML 2024): an estimated 6.5%-16.9% of peer-review text at ICLR 2024, NeurIPS 2023, CoRL 2023 and EMNLP 2023 was substantially LLM-modified. The share was higher in low-confidence and near-deadline reviews. (I did not verify the specific adjectives often quoted from this paper.) — [Liang et al. ICML 2024](https://proceedings.mlr.press/v235/liang24b.html)
- Juzek & Ward (COLING 2025, pp. 6397-6411) identified 21 "focal words" that spiked in scientific English and are overused by ChatGPT-3.5 in scientific writing. They found no evidence that architecture, algorithm choice or training data cause the overuse; RLHF evidence was inconclusive. — [Juzek & Ward COLING 2025](https://aclanthology.org/2025.coling-main.426)
- Juzek & Ward follow-up (arXiv 2508.01930, Aug 2025; BIAS@ECML-PKDD 2025): using Llama, they propose a procedure for detecting lexical preferences likely induced by learning from human feedback (RLHF/DPO). An emulated LHF experiment found that participants "systematically prefer text variants that include certain words." — [Juzek & Ward 2025b](https://arxiv.org/abs/2508.01930)
- Geng & Trotta, "Human-LLM Coevolution" (ACL Findings 2025; 1.29M arXiv abstracts 2018-2024): "delve," "intricate," "realm" and "showcasing" dropped sharply from about April 2024, after public call-outs, while less conspicuous words such as "significant" kept rising. A prompt telling GPT-4o-mini to avoid flagged words reduced them but did not eliminate them. — [Geng & Trotta 2025](https://aclanthology.org/2025.findings-acl.657); [arXiv](https://arxiv.org/abs/2502.09606)

**B. Model-output frequency-ratio lists (Paech antislop family)**
- Antislop (Paech, Roush, Goldfeder, Shwartz-Ziv; arXiv 2510.15061, Oct 2025; ICLR 2026 poster). Derivation:
  - Ratio ρ(p) = f_LLM(p)/f_human(p).
  - 2,000 outputs per model from Reddit creative-writing prompts (Nitral-AI dataset).
  - Human baselines: **wordfreq** for single words; a curated **Reddit creative writing + Project Gutenberg** corpus for n-grams, with stop-words removed.
  - Filters: minimum word length 3; a pattern must appear in at least 3 independent prompts; top 5,000 bigrams and trigrams considered.
  - Fingerprint: top 120 words and top 40 bigrams/trigrams.
  - Iteration-0 quotas: 920 dictionary + 80 non-dictionary words, plus 300/200 bigrams and 300/200 trigrams.
  - "Not X, but Y" detected by regex (Appendix L), reported at up to 6.3× human frequency in some models.
  - Source: [Antislop arXiv](https://arxiv.org/html/2510.15061); [ICLR 2026](https://iclr.cc/virtual/2026/poster/10008156); [auto-antislop code](https://github.com/sam-paech/auto-antislop)
- Antislop scale examples, all fiction (Gemma-3-12B): "elara" 85,513×; "unsettlingly" 3,833×; trigram "heart hammered ribs" 1,192×. Across 67 profiled models, "flickered" appears in 98.5% of models' top lists and "voice barely whisper" in 68.7%. Fingerprints cluster within model families and differ between families. — [Antislop](https://arxiv.org/html/2510.15061)
- slop-forensics merges per-model analyses into `slop_list.json`, bigram, trigram and phrase lists, and builds a "phylogeny" of models from presence/absence of top terms (PHYLIP parsimony). The README does not document the human corpora or thresholds; the antislop paper does. — [slop-forensics](https://github.com/sam-paech/slop-forensics)
- **[LOCAL] Contents of the current slop-score lists** (`sam-paech/slop-score/data`, last commits 2025-11-22, "fix slop list normalisation bug"):
  - Sizes: 1,648 words, 200 bigrams, 430 trigrams.
  - The first 60 alphabetical words are mostly fantasy names and fiction words (absently, ached, aelara, aethelgard, alaric, archmage…). The trigrams are narrative clichés ("voice barely whisper," "sun dipped horizon," "smile playing lips"); the bigrams include "said voice," "deep breath," "brow furrowed."
  - Informational-register words that **are** on the list: delve, delves, crucial, robust, navigate, nuanced, multifaceted, pivotal, intricate, underscore, tapestry, ensuring.
  - Words that are **not** on the list: significant, however, ensure, testament, leverage, comprehensive, essential, realm, landscape, quietly, foster, highlight, vital, key.
  - Source: [slop_list.json](https://raw.githubusercontent.com/sam-paech/slop-score/main/data/slop_list.json); [slop_list_trigrams.json](https://raw.githubusercontent.com/sam-paech/slop-score/main/data/slop_list_trigrams.json); [slop-score repo](https://github.com/sam-paech/slop-score)
- **[LOCAL] slop-score leaderboard data** (`leaderboard_results.json`, generated 2025-11-07, 23 entries; 150 creative + 150 essay outputs per model; human baseline n=83). Slop-list matches per 1k words:
  - human-baseline 6.90
  - antislop-tuned gemma-3-27b 5.61
  - claude-sonnet-4-5 9.72
  - kimi-k2-0905 10.12
  - gpt-5-mini 15.44
  - o3 19.89
  - chatgpt-4o-latest 23.26
  - gemini-2.5-flash 40.16
  - gemma-3-4b 40.44
  - "Not-x-but-y" per 1k chars: human 0.044 versus 0.086 (o3) up to 0.811 (gemma-3-4b).
  - Trigram matches per 1k words: human 0.094, kimi-k2-0905 0.078 (below the human baseline), llama-4-maverick 1.125.
  - The file has no GPT-5.1+, Gemini 3, or Claude 4.5 Opus+ entries.
  - Source: [leaderboard_results.json](https://raw.githubusercontent.com/sam-paech/slop-score/main/data/leaderboard_results.json)
- EQ-Bench publishes the slop score next to Creative Writing v3 and Longform Elo without folding it into Elo. Longform is judged by a Claude Sonnet 4.6 rubric. The slop metric is calibrated on creative writing. — [EQ-Bench longform](https://eqbench.com/creative_writing_longform.html); [creative-writing-bench](https://github.com/EQ-bench/creative-writing-bench); [benchmarklist summary](https://benchmarklist.com/benchmarks/creative_writing_v3/)

**C. Curated pattern catalogs (community)**
- Wikipedia "Signs of AI writing" (WikiProject AI Cleanup; widely covered Nov 2025; the live page says its list reflects the most common signs "as of October 2026"):
  - **Content:**
    - undue emphasis on significance or legacy ("stands/serves as," "is a testament," "pivotal/crucial," "underscores," "reflects broader")
    - canned notability and media-coverage claims
    - superficial "-ing" analyses ("highlighting," "ensuring," "fostering")
    - vague attributions ("Experts argue")
    - formulaic "despite its… faces challenges… future outlook" conclusions
    - "Awards and recognition" sections
  - **Language:**
    - AI-vocabulary density
    - avoidance of copulas ("serves as," "boasts")
    - negative parallelisms ("not only…but," "not X, but Y," and the newer "Y rather than X")
    - rule of three
  - **Style:** title-case headings, excessive bold, inline-header vertical lists, emoji in headings, curly quotes, markdown artifacts.
  - The guide is explicitly "not policy" and "not thoroughly vetted," and says "not all text featuring these indicators is AI-generated."
  - Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing); [TechCrunch 2025-11-20](https://techcrunch.com/2025/11/20/the-best-guide-to-spotting-ai-writing-comes-from-wikipedia/)
- Wikipedia **era-tagged vocabulary**, approximate per the page:
  - 2023 to mid-2024 (GPT-4): "delve," "intricate," "testament"
  - mid-2024 to mid-2025 (GPT-4o): "align with," "fostering," "showcasing"
  - mid-2025 to mid-2026 (GPT-5): "highlighting," "showcasing," notability vocabulary
  - mid-2026 onward ("GPT-6" per the page): "leverage," "multifaceted," "quietly," plus more periods and commas and 8-20-word sentences
  - "Delve" fell off sharply in 2025. Grok overuses "causal," "empirical," "correlate."
  - Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Wikipedia **historical (no longer reliable) indicators**:
  - promotional language (2023-2025)
  - knowledge-cutoff statements (2022-2023)
  - "In conclusion" / "In summary" section summaries
  - refusals
  - abrupt cut-offs
  - elegant variation from repetition penalties
  - **em-dash overuse (2022 to September 2026)**
  - **New mid-2026 tells:** "rather than" negative parallelism, "does not establish" cautions, and "should not be confused" disambiguations. The page calls these "extremely uncommon, verging on unheard-of, in AI output prior to mid-2026."
  - Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Wikipedia "Differences between LLMs": "Gemini and Claude responses tend to be more concise than responses from ChatGPT and Grok"; broader-context padding is "more characteristic of ChatGPT and Grok"; "what is typical for GPT-5 is not necessarily characteristic of GPT-4 or Gemini." — [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- tropes.fyi "AI Writing Tropes to Avoid" (by ossama.is; undated; many GitHub gist forks, e.g., Mar 2026) lists 49 tropes in six types, each tagged consistent/rising/fading/new:
  - **Sentence structure:** negative parallelism; "Not X. Not Y. Just Z."; rule of three; comma-clipped trailing phrases; "The X? A Y."; anaphora; false ranges; "It's worth noting"
  - **Paragraph structure:** short punchy fragments; excessive enumeration
  - **Composition:** preamble; tie-back; fractal summaries; never-ending conclusion; signposted conclusion
  - **Formatting:** em-dash addiction; "Where/What/Why" headers; title case; bold-first bullets
  - **Word choice:** "quietly" and other magic adverbs; synonym cycling; "tapestry/landscape"; "serves as"; "delve and friends"
  - **Tone:** stakes inflation; invented concept labels; quotable one-liners; "Let's break this down"; "Think of it as…"
  - The list is hand-curated with **no validation data**.
  - Source: [tropes.fyi](https://tropes.fyi/tropes-md); [ossa-ma gist](https://gist.github.com/ossa-ma/f3baa9d25154c33095e22272c631f5a1)
- Other community skill-style lists: "avoid-ai-writing" (21 pattern categories, 43-entry replacement table) and the "detrope" catalog (44 tropes in 8 categories). Neither is validated. — [avoid-ai-writing](https://tessl.io/registry/skills/github/administrakt0r/AI-Agents-Safe-Coding-Skills/avoid-ai-writing); [detrope](https://openskillindex.com/skills/matthewsinclair-intent-in-detrope)

**D. Structural / stylistic fingerprints (beyond words)**
- Reinhart et al. (*PNAS* 122(8), Feb 2025; DOI 10.1073/pnas.2422455122) compared LLM and human text on Biber's lexical, grammatical and rhetorical features. Instruction-tuned models write in an "informationally dense, noun-heavy style" even when asked to imitate informal registers. Per the preprint: present participial clauses at 2-5× the human rate, nominalizations at 1.5-2×, and GPT-4o agentless passives at about half the human rate. Llama 3 base models track human usage more closely than instruct models, implicating instruction tuning. A secondary summary reports a random-forest classifier at 66% accuracy **[UNVERIFIED]**. — [Reinhart et al. preprint](https://arxiv.org/html/2410.16107v2)
- Sun et al., "Idiosyncrasies in LLMs" (ICML 2025, PMLR 267): a fine-tuned text-embedding classifier separates ChatGPT, Claude, Grok, Gemini and DeepSeek outputs with 97.1% held-out accuracy. Accuracy drops only slightly when words are randomly shuffled, which suggests word choice carries much of the signal. It stays above chance after an external LLM rewrites the text, or even after summarization, which suggests semantic content and organization carry signal too. — [Sun et al. arXiv](https://arxiv.org/abs/2502.12150); [project page](https://eric-mingjie.github.io/llm-idiosyncrasies)
- "Artificial Hivemind" (Jiang, Choi et al.; NeurIPS 2025 D&B oral, Best Paper) built Infinity-Chat: 26K open-ended queries and 31,250 human annotations. It finds strong intra-model repetition and, more so, inter-model homogeneity. Reward models and LM judges are less calibrated to humans where annotators' preferences diverge. — [Jiang et al.](https://arxiv.org/abs/2510.22954); [NeurIPS best paper post](https://blog.neurips.cc/2025/11/26/announcing-the-neurips-2025-best-paper-awards/)
- Expert annotators' cues in Russell et al., as a share of explanations: vocabulary 53.1%, sentence structure 35.9%, grammar/punctuation 24.8%, originality 23.7%, quotes 22.3%, clarity 19.5%. Named AI vocabulary includes "vibrant," "crucial," "significantly," "testament," "delve." Generic names also leak: 63.3% of GPT-4o and 70% of Claude articles used "Emily" or "Sarah." After humanization, AI text still overused "Dr." / "Prof." titles. — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- An Economist analysis (2026, via secondary coverage dated 2026-08-04) compared 55,940 sentences and 1.2M words of ChatGPT/Claude/Gemini/Grok rewrites with human journalism and novels. LLMs use fewer commas, semicolons and parentheses, and overuse "and" as a connector, nominalizations, polysyllabic words, "it's not X, it's Y," and rule-of-three. They write blocky paragraphs with uniform sentence lengths. **[secondary report; original not read]** — [The Outpost summary](https://theoutpost.ai/news-story/ai-writing-s-biggest-giveaway-has-changed-the-economist-report-reveals-new-detection-patterns-29372/)

**E. Em-dash evidence over model versions**
- Small informal tests (2025): GPT-3.5 produced 0 em-dashes in 10 stories; GPT-4.1 produced 14 and GPT-4o 16. GPT-4o/4.1 used them in every story. **[small-n blog]** — [Sukhareva part 1](https://msukhareva.substack.com/p/lets-talk-about-em-dashes-in-ai); [part 2](https://msukhareva.substack.com/p/the-mystery-of-emdashes-part-two?)
- Freeburg, "The Last Fingerprint" (arXiv 2603.27006, 2026-03-27) tested 12 models from 5 providers. Em-dash rates range from 0.0 per 1k words (Llama) to 9.1 (GPT-4.1 with markdown suppressed). A "no markdown" instruction removed headers, bullets and bold but **not** em-dashes, except in Llama. Explicitly banning em-dashes did not eliminate them in some models. The tendency appears in base models, i.e., before RLHF. — [Freeburg 2026](https://arxiv.org/abs/2603.27006)
- Wikipedia now lists em-dash overuse as a *historical* indicator (2022-Sept 2026):
  - GPT-5.1 (Nov 2025) suppressed em-dashes, per Ars Technica 2025-11-14.
  - A July 2026 study found "only Claude used em dashes more than professional writers, and ChatGPT used them less."
  - From Sept 2026, newer models are "hard coded to not use em dashes at all."
  - AI em-dashes are "usually surrounded by spaces."
  - Side effect: "commas and periods are more likely now than even human text" [citation needed on Wikipedia].
  - Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- **Conflicting numbers:** a 2026 blog citing a Graphite "AI Tells" study reports Claude Opus 5.5 at about 0.015 em-dashes per 1k words and Gemini 3.1 Pro at about 0.014, versus a human baseline of 3.14, and GPT-4.1 at about 7.1 and GPT-5 at about 6.9 **[UNVERIFIED; primary Graphite study not found]**. This contradicts the Economist's finding that Claude is the only model above the human rate. The two likely cover different model versions and corpora. — [Pebblous blog](https://blog.pebblous.ai/report/opus-5-5-em-dash-ai-tells-drift/en/); [The Outpost / Economist](https://theoutpost.ai/news-story/ai-writing-s-biggest-giveaway-has-changed-the-economist-report-reveals-new-detection-patterns-29372/)

### Inferences
- **No public lexicon is validated for informational prose in 2026.**
  - Kobak/Liang/Juzek are 2024-vintage, scientific-abstract, corpus-level lists.
  - The Paech lists are creative-writing lists from late 2025.
  - Wikipedia is current (Oct-Nov 2026) and covers encyclopedic/informational register, but it is qualitative.
  - For this project, Wikipedia's content and language categories (significance inflation, "-ing" superficial analysis, copula avoidance, negative parallelisms, formulaic challenge/outlook endings, vague attributions) are the best-matched catalog for informational nonfiction. Paech's regex "not-X-but-Y" detector is the best-validated *structural* counter, because it shows the clearest human-versus-model gap in the [LOCAL] data (human 0.044 versus models 0.086-0.81 per 1k chars).
- **Word lists are a weak signal against frontier models.** In the [LOCAL] data, the best 2025 frontier models sit only about 1.4× above the human baseline on slop-list words (Claude Sonnet 4.5 9.72 versus 6.90), and kimi-k2-0905 is *below* human on trigrams. The fine-tuning base for this project (a 7-9B open instruct model, e.g., Gemma/Qwen/Llama class) likely sits far higher: gemma-3-4b is at 5.9× and gemma-3-12b at 5.3×. So lexicon signals will be strong at the start of training and weaken as the style model approaches the author's voice.
- **Regenerate the lexicon; do not adopt one.** Antislop's profiling recipe (ρ = f_model/f_human, appearance in at least 3 prompts, a dictionary filter, top-k n-grams) and Kobak's counterfactual-excess method both transfer directly. Run them on (a) the base model's outputs for this project's informational prompts versus (b) the target author's corpus plus a pre-Nov-2022 human informational baseline. Wikipedia says text before 2022-11-30 can be treated as AI-free, and humans have adopted LLM words in speech since 2023. Re-profile after each training round, because suppressed patterns are replaced by new ones.
- Sun et al.'s 97.1% source attribution and the antislop per-family clustering mean tells are **model-specific**. A GPT-4o-era list will miss Qwen/Gemma-specific habits and penalize words this base model never overuses.

### Gaps
- I could not locate the primary Graphite "AI Tells" 2026 study or the July 2026 em-dash study Wikipedia cites. The Economist original was read only through secondary coverage.
- No peer-reviewed lexicon derived from **2026 frontier models** (GPT-5.x/6, Claude 4.5-5.x, Gemini 3.x) on informational prose was found.
- The human corpus behind the slop-score "human-baseline" row (n=83, 76.8 MB `human_writing_profile.json`) is not documented in the README.
- Geng & Trotta's earlier arXiv word-frequency paper ("Is ChatGPT transforming academics' writing style?") was not retrieved, so its estimates are not included.
- I did not verify the full seven-category taxonomy of Chakrabarty et al.'s LAMP corpus (see Q3) or the specific adjectives in Liang's peer-review paper.

---

## Q3. What is the risk of over-correction (the model avoids natural human words and punctuation and becomes stilted), and does "AI-like" equal "bad writing"?

### Takeaway
The risk is real and documented.
- **Humans use the tells.** Detectors flag about 61% of non-native essays. Experts' wrong calls cite "delve" and "crucial" found in human text. Humans now say "delve" in podcasts. The slop-score human baseline scores 6.9 list words per 1k, which is not zero.
- **Naive suppression damages quality.** In the Antislop paper, DPO on banned patterns cut writing quality by 6-15 points and lexical diversity to 74-92% of baseline. Hard token-banning dropped quality to 28/100 at 8k bans.
- **Suppressed tells are replaced.** "Significant" kept rising after "delve" fell. Em-dash suppression produced over-regular commas and periods, now itself a tell.
- **Slop is not the same as bad writing.** Expert "slop" judgments track density, relevance and tone more than vocabulary. Annotators barely agree on the binary label. No study shows that slop-lexicon density correlates with human quality ratings of informational prose.
- **The least damaging option the evidence supports:** soft, targeted, model-specific suppression (FTPO-style final-token preference, or reranking), checked against the target author's own frequency of each pattern.

### Cited Findings

**Human writing contains the tells (false-positive risk)**
- Detectors misclassify non-native English: about 61% average FPR on TOEFL essays, and 97.8% of essays flagged by at least one of 7 detectors (2023). — [Liang et al. 2023](https://arxiv.org/abs/2304.02819)
- In Russell et al., 31% of experts' *incorrect* explanations mention vocabulary, typically when human-written text contained words like "delve" and "crucial." — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- Yakura et al. (arXiv Sept 2024; v3 July 2025) analyzed 740,249 hours of speech: 360,445 YouTube academic talks and 771,591 podcast episodes. They report a causal post-ChatGPT rise in ChatGPT-favored words such as "delve," "comprehend" and "meticulous" in *human* speech, including unscripted podcasts. — [Yakura et al.](https://arxiv.org/abs/2409.01754)
- "Delve" is common in Nigerian business English, per Guardian reporting from Apr 2024 **[from snippet]**. The claim that Nigerian RLHF annotators *caused* ChatGPT's "delve" habit is unsubstantiated speculation. A 2026 paper (Ugwuanyi, arXiv 2607.28528, 2026-07-30) frames the "AI-sounding delve" discourse as Global-North policing of World Englishes; its abstract gives no quantitative results. A search summary attributes to it the finding that the highest "delve" frequencies occur in Asian Englishes, not Nigerian ones **[UNVERIFIED]**. — [Guardian via PressReader](https://www.pressreader.com/usa/the-guardian-usa/20240417/282050512110374); [Ugwuanyi 2026](https://arxiv.org/abs/2607.28528)
- Wikipedia's guide cautions:
  - human writers "often use em dashes"
  - negative parallelisms are common in human "myths busted" listicles
  - "perfect grammar," "fancy" prose and isolated transition words are **ineffective** indicators
  - non-native editors may avoid repeated words, mimicking AI "elegant variation"
  - "Detecting LLM texts on the basis of style alone is not as easy as it seems."
  - Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Kobak et al. note that native speakers may strip unnatural style words more often, so lexicon-based estimates and labels depend on the writer population. — [Kobak et al. v5](https://arxiv.org/html/2406.07016v5)
- **[LOCAL]** In slop-score's own data, the human baseline scores 6.90 slop-list hits per 1k words and 0.094 slop trigrams per 1k words. That is more trigrams than kimi-k2-0905 (0.078), so a strict trigram penalty would rank this human baseline as sloppier than a 2025 frontier model. — [leaderboard_results.json](https://raw.githubusercontent.com/sam-paech/slop-score/main/data/leaderboard_results.json)

**"Slop" versus quality: what humans actually object to**
- Shaib et al. (2025) built a taxonomy from 19 expert interviews: Information Utility (density, relevance), Information Quality (factuality, bias), and Style Quality (repetition, templatedness, coherence, fluency, verbosity, word complexity, tone). All codes predicted binary slop judgments. The strongest were relevance (β̂=0.06), density (0.05) and tone (0.05); factuality and structure dominated for QA passages. The authors state that "text can be perceived as 'slop' even when not generated by AI," e.g., generic, verbose or hastily written human text. About 34-35% of samples were judged slop. — [Shaib et al. 2025](https://arxiv.org/html/2509.19163v2)
- Chakrabarty, Laban and Wu ("Can AI writing be salvaged?", CHI 2025; arXiv Sept 2024) had 18 professional writers edit LLM paragraphs using a 7-category idiosyncrasy taxonomy that includes clichés and unnecessary exposition. The resulting LAMP corpus holds 1,057 paragraphs and 8,035 edits. GPT-4o, Claude-3.5-Sonnet and Llama-3.1-70B did not differ in writing quality. Preference order: writer-edited > LLM-edited > raw LLM output. — [Chakrabarty et al.](https://arxiv.org/abs/2409.14509)
- Surge AI's Hemingway-bench (blog; page shows Feb 4 and Oct 21, 2026) ran over 5,000 blind pairwise comparisons by professional writers. Surge says EQ-Bench's grader "agreed with expert writers as little as 43% of the time" and claims "many frontier labs" find EQ-Bench scores "often negatively correlated with good creative writing." Top models were Gemini 3 Flash, Gemini 3 Pro and Claude Opus 4.5. **[VENDOR: Surge sells human evaluation; no sample sizes or agreement statistics published]** — [Surge Hemingway-bench](https://surgehq.ai/blog/hemingway-bench-ai-writing-leaderboard)
- "Artificial Hivemind" shows that reward models and LM judges are least calibrated to humans exactly where human preferences are idiosyncratic. A single-author voice is such a case. — [Jiang et al. 2025](https://arxiv.org/abs/2510.22954)

**Evidence of collateral damage from suppression**
- Antislop (ICLR 2026), Gemma-3-12B, FTPO versus DPO at 2k/4k/8k banned patterns:
  - FTPO: writing quality 68.93 / 67.31 / 67.49 (baseline 67.80); diversity 101.05 / 97.68 / 95.09; ban suppression 92.4% / 90.2% / 83.4%; MMLU and GSM8K roughly preserved (8k: 0.592 / 0.889 versus 0.590 / 0.888).
  - DPO: writing quality 62.98 / 58.24 / 54.61; diversity 91.03 / 81.92 / 73.92; long-form score falling from 51.3 to 26.9 at 8k.
  - Source: [Antislop](https://arxiv.org/html/2510.15061)
- Antislop, other models with FTPO at 1k bans: Mistral-Small writing quality 74.60 versus 72.93 baseline, ban 89.5%. Llama-3.3-70B (lm_head-only LoRA) 63.16 versus 64.34, ban 66.4%. The paper reports Llama-3.3-70B as "prone to repetition and degradation artifacts" under preference training. — [Antislop](https://arxiv.org/html/2510.15061)
- Antislop, inference-time methods:
  - Hard token banning drops writing quality to 28/100 at 8k bans.
  - Collateral damage: banning "catatonic" (tokenized "cat"+"atonic") hits every word starting with "cat."
  - The backtracking sampler suppresses 8,000+ patterns, but throughput falls 69% at 1k bans and 96% at 8k (H100/vLLM).
  - Soft banning is designed so a banned word stays available when the prompt requires it (e.g., "tapestries").
  - The ethics section flags possible suppression of legitimate dialects and minority styles.
  - The paper does **not** measure stiltedness or whether replacement words become new slop.
  - Source: [Antislop](https://arxiv.org/html/2510.15061)
- **[LOCAL]** The released antislop-tuned gemma-3-27b cut slop-list words from 32.27 to 5.61 per 1k (−83%, below the 6.90 human baseline) and trigrams from 0.78 to 0.18 (−77%). Not-x-but-y fell only from 0.577 to 0.459 per 1k chars (−20%), still about 10× the human rate. Lexical bans leave structural tells mostly intact. — [leaderboard_results.json](https://raw.githubusercontent.com/sam-paech/slop-score/main/data/leaderboard_results.json)
- Replacement and drift after suppression:
  - "Significant" kept rising after "delve" fell, and avoidance prompts reduced but did not remove flagged words ([Geng & Trotta 2025](https://aclanthology.org/2025.findings-acl.657)).
  - After em-dash suppression, "overall variety has dropped significantly," and comma/period over-regularity "has become its own sign" ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).
  - The Economist analysis reports that sparse punctuation and uniform sentence lengths are now better AI signals than em-dashes ([The Outpost / Economist](https://theoutpost.ai/news-story/ai-writing-s-biggest-giveaway-has-changed-the-economist-report-reveals-new-detection-patterns-29372/)).
- Humanizing by avoiding AI vocabulary moved detectors a lot but not expert humans. The expert majority stayed at 100% on humanized articles. Experts then relied less on vocabulary (42.3% versus 57.1% of explanations) and more on formality, originality and quotes. Removing the vocabulary removes the cheap signal but not what makes the text read as AI. — [Russell et al. 2025](https://arxiv.org/html/2501.15654)
- tropes.fyi itself acknowledges a "cat and mouse" dynamic, and that a single instance of most tropes is fine. — [tropes.fyi](https://tropes.fyi/tropes-md)

### Inferences
- **Calibrate penalties against the target author.**
  - Tells that the author uses at or above the base model's rate should never be penalized; em-dashes, "crucial," and rule-of-three in instructional lists are likely candidates.
  - The right negative signal is the *excess* of the model over the author: ρ = f_model / f_author, with a floor from a pre-2022 informational corpus. It is not a generic list.
  - This also guards against non-native or dialect bias if the chosen author's English differs from US/UK norms.
- **Prefer graded, soft mechanisms over hard bans.** The evidence favors FTPO-like final-token preference pairs (≤1% quality change at about 90% suppression) or n-best reranking with a small penalty. Hard logit bans, large banlists, and sequence-level DPO on "slop vs clean" pairs measurably degrade quality and diversity. DPO on whole rejected examples labeled by lexicon density risks teaching "avoid these words" rather than "write like the author," because the lexicon is only a weak proxy for what humans call slop.
- **Lexicons do not capture structure.** Structural tells (contrast templates, tricolons, summary endings, formulaic challenge/outlook closers, bold-header listicles, uniform sentence length) need separate counters. Word-level suppression leaves them in place, as the [LOCAL] antislop result shows.
- **Do not equate low slop score with good writing.** No study correlates slop-lexicon density with human quality ratings for informational prose. The closest study (Shaib et al.) finds that metrics poorly predict slop judgments, and that relevance, density and factuality matter more. Keep slop score as one eval metric, alongside human or pairwise preference against the author's real text, and watch for a drop in diversity (MATTR, distinct-n) as the over-correction alarm.
- **Expect drift within the project.** Each round of suppression will surface new over-represented patterns, as with "significant" after "delve" and commas after em-dashes. Re-profiling the model against the author corpus after each training round is necessary if slop signal is used in training.

### Gaps
- No study found that directly measures human-rated *stiltedness* or naturalness after lexicon-based suppression in nonfiction. The Antislop quality metric is an LLM-judged rubric (GPT-5 / Sonnet 4) on creative and long-form writing, not human-rated informational prose.
- No quantitative study found correlating slop-lexicon density with human quality judgments for informational or instructional text. Shaib et al. report that standard metrics do not capture preferences but give no per-lexicon correlations.
- No verified per-variety (Nigerian, Indian, etc.) frequency data for "delve"-class words was retrieved; the Ugwuanyi figures are unverified.
- No independent data on whether removing tells raises or lowers *expert-perceived quality*, as opposed to detectability, of nonfiction.
- No local experiment was run on informational text. A useful next experiment: score the target author's corpus and a pre-2022 informational corpus with slop-score and a regenerated lexicon, to measure the human false-positive floor before using any threshold for negatives.
