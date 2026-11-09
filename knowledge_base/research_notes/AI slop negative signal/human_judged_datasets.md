# Human-judged / human-edited AI writing datasets usable as negative signal for a nonfiction style model

Verification date for everything below: 2026-11-07. I checked licenses, sizes and file contents against the HF Hub API, HF datasets-server, the GitHub API and arXiv (abstract/HTML) on that date. Items marked **[unverified]** come from memory or a search snippet and were not re-checked against a primary source in this session. Where I computed a count from the released file myself, the bullet says "computed from released file".

Fit rating used throughout: how directly the item maps to *slop vs. good informational/instructive prose* (explainers, memos, docs, analyses). **A** = human-edited or human-labeled AI text in or near informational nonfiction, with reasons. **B** = human quality judgments, but on the wrong domain or with coarse labels. **C** = AI-vs-human labels only (useful for mass synthetic negatives or as a detector). **D** = synthetic negatives only.

---

## Q1. Which datasets give human-labeled or human-edited slop in informational nonfiction at useful scale (≥1k items), with a permissive license?

### Takeaway
No public dataset meets all four criteria at once: expert-edited, informational nonfiction (memos/docs/explainers), ≥1k items, and categorized reasons. The closest options are: **LAMP** (1,282 expert-edited AI paragraphs with 9,593 categorized span edits; BSD-3 repo; but about 75% literary fiction); **Beemo** (2,187 expert-edited assistant responses across QA/summarize/rewrite/generation; MIT for the edits; no reasons); and **HelpSteer3-Edit** (14,461 human edits of AI responses with feedback and change summaries; CC-BY-4.0; about 5.7k English general/STEM; but edits target helpfulness, not style). For nonfiction-specific expert *judgments* (not edits), **Human Detectors** (300 nonfiction articles × 5 experts with free-text explanations, MIT) is the best domain match but is small. **Measuring AI "Slop"** has exactly the right taxonomy and annotators (professional copy-editors on news and QA text), but its data is **not released**: the repo says "Coming soon!".

### Cited Findings

#### Tier A: human edits of AI text, or expert span annotations (most directly useful)

**1. LAMP corpus (Language model Authored, Manually Polished)**
- Paper: "Can AI writing be salvaged? Mitigating Idiosyncrasies and Improving Human-AI Alignment in the Writing Process through Edits", Tuhin Chakrabarty, Philippe Laban, Chien-Sheng Wu. arXiv 2409.14509, first posted 2024-09-22, ACM CHI 2025 (arXiv comment). — [arXiv](https://arxiv.org/abs/2409.14509)
- The authors hired professional writers, who "agree on undesirable idiosyncrasies in LLM generated text". They formalized these into a seven-category taxonomy. The paper describes LAMP as 1,057 LLM-generated paragraphs edited according to that taxonomy. — [arXiv](https://arxiv.org/abs/2409.14509)
- Release: GitHub `salesforce/creativity_eval`, folder `Writing_Alignment/LAMP/` (`LAMP.json`, `LAMP-train-val-test.json`, plus 50 samples re-annotated by 3 writers and 600 preference annotations). Each record has `instruction`, `preedit` (AI paragraph), `postedit` (expert edit) and `fine_grained_edits` (originalText → editedText + `categorization`). The source New Yorker paragraphs are not redistributed. — [README](https://github.com/salesforce/creativity_eval/tree/main/Writing_Alignment)
- License: the repo is **BSD-3-Clause** (GitHub API). The Salesforce model cards add a "research purposes only" ethics note. — [GitHub repo](https://github.com/salesforce/creativity_eval); [WQRM card](https://huggingface.co/Salesforce/WQRM)
- Computed from released file `LAMP-train-val-test.json`:
  - Size: **1,282 items**, 19 distinct editor IDs. The AI paragraphs come from gpt4o (463), claude3.5-sonnet (449), llama3-70B (364) and llama3.1-405B (6).
  - Domains: Literary Fiction 965, Travel Writing 111, Food Writing 84, Internet Advice Column 65, Creative NonFiction 41, Personal Experience 10, Fantasy 6. So about 24% (311) is nonfiction-ish, but it is creative or personal nonfiction, not docs or memos.
  - Edits: **9,593 categorized span edits**. Awkward Word Choice and Phrasing 2,531; Poor Sentence Structure 1,926; Cliché 1,847; Unnecessary Exposition 1,715; Lack of Specificity and Detail 1,011; Purple Prose 426; Tense Inconsistency 101; Punctuation 29; the rest fewer than 5 each.
  - Length: mean 206 words before the edit and 189 after.
  - Each item also carries a pre- and post-edit quality score.
  - Source: [data file](https://github.com/salesforce/creativity_eval/blob/main/Writing_Alignment/LAMP/LAMP-train-val-test.json)
- The WQRM paper uses the same 1,282 items, split 1,000 train / 67 val / 215 test. — [arXiv HTML](https://arxiv.org/html/2504.07532v3)
- Experts largely preferred expert-edited text over automatically edited text in a large preference annotation, but "automatic editing methods show promise". — [arXiv](https://arxiv.org/abs/2409.14509)
- Fit: **A−**. It is the best categorized "slop → fix" signal (cliché, unnecessary exposition, lack of specificity, purple prose), but the domain is mostly fiction.

**2. Beemo (Benchmark of Expert-edited Machine-generated Outputs)**
- Paper: Ekaterina Artemova, Jason Lucas, Saranya Venkatraman, Jooyoung Lee, Sergei Tilga, Adaku Uchendu, Vladislav Mikhailov. arXiv 2411.04032, 2024-11-06, NAACL 2025. — [arXiv](https://arxiv.org/abs/2411.04032)
- HF: `toloka/beemo`. The viewer shows **2,187 rows**. Each row holds a No Robots prompt, the human-written gold answer, the LLM output (from 10 open instruction-tuned LLMs), an **expert-edited** version, and 3 GPT-4o plus 3 Llama-3.1-70B "humanize" edits. Categories: Generation 585, Rewrite 525, Open QA 483, Summarize 389, Closed QA 205. — [HF card](https://huggingface.co/datasets/toloka/beemo)
- The editors were "an in-house team of annotators, who are well experienced in refining content produced by LLMs". The abstract frames the edits as refining "for natural flow, coherence, and factual correctness". **No edit categories or reasons are recorded.** — [HF card](https://huggingface.co/datasets/toloka/beemo); [arXiv](https://arxiv.org/abs/2411.04032)
- License is split:
  - Expert edits (`human_edits`): **MIT**.
  - Prompts and human outputs (from No Robots): **CC-BY-NC-4.0**.
  - Model outputs: the license of each generating LLM (Llama 2, Gemma, etc.).
  - Source: [HF card](https://huggingface.co/datasets/toloka/beemo)
- Finding: expert editing evades machine-generated-text (MGT) detectors, while LLM-edited texts are unlikely to be recognized as human-written. — [arXiv](https://arxiv.org/abs/2411.04032)
- Fit: **A−/B+**. The domain (assistant answers, summaries, rewrites) is closer to informational prose than LAMP, and the pairs come ready-made (model_output → human_edits). There are no reasons, and the generators are small or old (zephyr, tulu-2, Llama-2, Gemma-1, Mistral-7B).

**3. HelpSteer3-Edit / Edit-Quality / Feedback (NVIDIA)**
- Paper: "HelpSteer3: Human-Annotated Feedback and Edit Data to Empower Inference-Time Scaling in Open-Ended General-Domain Tasks", Zhilin Wang, Jiaqi Zeng, Olivier Delalleau, Daniel Egert, Ellie Evans, Hoo-Chang Shin, Felipe Soares, Yi Dong, Oleksii Kuchaiev. arXiv 2503.04378, 2025-03-06, ACL 2025 Main. — [arXiv](https://arxiv.org/abs/2503.04378)
- HF: `nvidia/HelpSteer3`, **CC-BY-4.0**. — [HF card](https://huggingface.co/datasets/nvidia/HelpSteer3)
  - **Edit** config: **14,461** samples. Each has the original AI response and 3 human feedbacks (2–10 sentences each, starting "The response is {not/slightly/partially/mostly/perfectly} helpful"). A separate annotator then wrote an edited response plus a **short change summary**.
  - **Edit-Quality**: 3,274 samples, each with a good and a bad human edit. "Bad" means the edit did not follow the feedback.
  - **Feedback**: 40,821 samples.
- The Edit train split in the viewer has 13,740 rows: multilingual 4,626, general 4,606, code 3,371, stem 1,137; English 5,743. — [HF dataset](https://huggingface.co/datasets/nvidia/HelpSteer3)
- Labelers: about 7,000 annotators in 80+ regions, contracted through Scale AI and Translated, with measures to prevent LLM use. The responses came from about 20 permissively licensed LLMs (none proprietary). — [HF card](https://huggingface.co/datasets/nvidia/HelpSteer3)
- Fit: **B+**. This is the largest permissive set of human edits of AI text with written rationales, and the general/STEM parts are informational. The target, however, is *helpfulness*, not prose style or slop. You would need to filter it for feedback that mentions verbosity, repetition, formatting or tone; I did not measure how much does.

**4. Human Detectors (expert AI-vs-human judgments on nonfiction articles, with explanations)**
- Paper: "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text", Jenna Russell, Marzena Karpinska, Mohit Iyyer. arXiv 2501.15654, 2025-01-26, ACL 2025. — [arXiv](https://arxiv.org/abs/2501.15654)
- Content: **300 nonfiction English articles** (150 human, 150 AI). Five "expert" annotators (frequent LLM users recruited on Upwork) gave each article a label, a confidence score and a paragraph-length explanation. The paper reports 1,740 annotations in one section and 1,790 in another. The majority vote of the 5 experts misclassified only 1 of 300 articles. — [arXiv](https://arxiv.org/abs/2501.15654); [arXiv HTML](https://arxiv.org/html/2501.15654v2)
- Human articles (under 1k words) came from AP, Discover, National Geographic, NYT, Reader's Digest, Scientific American, Smithsonian and WSJ. AI articles came from GPT-4o, Claude-3.5-Sonnet, o1-Pro, paraphrased GPT-4o, and o1-Pro "humanized" using a guidebook of expert clues. — [arXiv HTML](https://arxiv.org/html/2501.15654v2)
- Explanation categories (share of explanations mentioning each): Vocabulary 53.1%, Sentence Structure 35.9%, Grammar & Punctuation 24.8%, Originality 23.7%, Quotes 22.3%, Clarity 19.5%. Formality, tone, factuality and names are also coded (frequencies not captured). Example "AI vocabulary": vibrant, crucial, significantly, testament, delve. — [arXiv HTML](https://arxiv.org/html/2501.15654v2)
- Release: GitHub `jenna-russell/human_detectors`, **MIT**. An HF mirror with prompt-disjoint splits (100 val / 200 test) is `suraj-ranganath/tell-human-detectors` (MIT); it is used by the TELL explainable detector paper (arXiv 2605.27921). — [GitHub](https://github.com/jenna-russell/human_detectors); [HF mirror](https://huggingface.co/datasets/suraj-ranganath/tell-human-detectors); [TELL arXiv](https://arxiv.org/abs/2605.27921)
- Fit: **A for domain and labeler quality, but small**. The explanations are a strong seed for a nonfiction slop rubric. The labels are AI-vs-human, not quality.

**5. Measuring AI "Slop" in Text (taxonomy plus expert span annotation; data NOT released)**
- Paper: Chantal Shaib, Tuhin Chakrabarty, Diego Garcia-Olano, Byron C. Wallace. arXiv 2509.19163 (v3), first posted 2025-09-23. No venue is listed on arXiv. — [arXiv](https://arxiv.org/abs/2509.19163)
- Taxonomy, built from interviews with experts in NLP, writing and philosophy:
  - **Information Utility**: Density, Relevance.
  - **Information Quality**: Factuality, Bias/Subjectivity.
  - **Style Quality**: Repetition, Templatedness, Coherence, Tone (including fluency, verbosity, word complexity).
  - Source: [arXiv HTML](https://arxiv.org/html/2509.19163v3)
- Annotation: 3 professional copy-editors (15–30 years' experience) worked on news articles from Russell et al. (human, Claude, GPT-4o, o1-pro, humanized) and on MS MARCO QA answers (Llama-4 Scout, OLMo-2-13B, Mistral-7B, GPT-4o, Gemma-2-27B). In total 213 article annotations and 123 passage annotations. — [arXiv HTML](https://arxiv.org/html/2509.19163v3)
- Agreement on the binary "slop" label is near zero:
  - Cohen's κ: −0.12, 0.11, 0.01.
  - Gwet's AC1: 0.07–0.21.
  - Theme-level Krippendorff's α_MASI: 0.37–0.44.
  - Span count correlates with the slop label (ρ = 0.63 overall).
  - Relevance, Density and Tone are the strongest predictors overall. For news, Coherence, Tone, Density, Relevance and Bias are significant; for QA, Factuality and Structure are the strongest.
  - Source: [arXiv HTML](https://arxiv.org/html/2509.19163v3)
- Release status: the paper points to `github.com/cshaib/slop`. On 2026-11-07 that repo held only `.gitignore`, `LICENSE` (MIT) and a README reading "Coming soon!" (last push 2025-09-23). **No annotations are available.** — [GitHub](https://github.com/cshaib/slop)
- Fit: it would be **A** if released (informational news and QA, professional copy-editors, span-level codes). Today it is usable only as a **taxonomy**.

**6. Scarecrow (span-level error annotation of GPT-2/GPT-3 news-style text)**
- Paper: "Is GPT-3 Text Indistinguishable from Human Text? Scarecrow: A Framework for Scrutinizing Machine Text", Yao Dou, Maxwell Forbes, Rik Koncel-Kedziorski, Noah A. Smith, Yejin Choi. arXiv 2107.01294, 2021-07-02; ACL 2022 **[venue unverified]**. — [arXiv](https://arxiv.org/abs/2107.01294)
- **Crowd** annotators (laypeople) marked over **41k error spans** in human-written and machine-generated English news paragraphs, using 10 error categories. The abstract names redundancy, commonsense errors and incoherence among them; the full list is **[unverified]**. Rationales are included. — [arXiv](https://arxiv.org/abs/2107.01294)
- Release: [project page](https://yao-dou.github.io/scarecrow/). The GitHub repo `Yao-Dou/scarecrow` has no license file (GitHub API).
- Fit: **B**. Informational news domain, span-level categories, good scale. But it is pre-RLHF model output, so its error profile (incoherence, off-prompt) differs from modern "polished slop" (templatedness, puffery, hedging).

#### Tier B: human quality or preference judgments (AI vs. AI, or human vs. AI)

**7. Writing Quality (WQ) benchmark** (Chakrabarty, Laban, Wu, "AI-Slop to AI-Polish? Aligning Language Models through Edit-Based Writing Rewards and Test-time Computation", arXiv 2504.07532, 2025-04-10, "Under Submission" per arXiv comment)
- It consolidates 4,729 judgments. — [arXiv HTML](https://arxiv.org/html/2504.07532v3)

  | Subset | Judgments | Labelers | Domain | Pair type |
  |---|---|---|---|---|
  | Art or Artifice | 144 | expert | flash fiction | — |
  | LAMP-test | 1,206 | expert | fiction and non-fiction, 200–400 words | — |
  | Style Mimic | 300 | implicit (150 pairs duplicated) | fiction | human-human |
  | Synthetic Mirror | 1,120 | implicit (author text preferred over GPT-4o/Claude mirror) | flash fiction | — |
  | LM Arena | 1,959 | crowd | creative writing | AI-AI |

- Data: `creativity_eval/WritingRewards/WQ-benchmark-data/` (per-subset JSON files plus a combined `wq_benchmark.json`), BSD-3 repo. — [GitHub](https://github.com/salesforce/creativity_eval/tree/main/WritingRewards)
- Fit: **B**. Mostly fiction, and two subsets use implicit labels.

**8. HelpSteer2 (and HelpSteer2-Preference)**
- Paper: arXiv 2406.08673 (2024-06-12), Wang et al.; venue **[unverified]**. HelpSteer2-Preference: arXiv 2410.01257, ICLR 2025. — [arXiv](https://arxiv.org/abs/2406.08673); [arXiv](https://arxiv.org/abs/2410.01257)
- `nvidia/HelpSteer2`, **CC-BY-4.0**. 21,362 samples, each rated 0–4 on helpfulness, correctness, **coherence**, complexity and **verbosity** ("amount of detail ... relative to what is asked"). Built with Scale AI. Individual (pre-averaging) annotator ratings are also released. — [HF card](https://huggingface.co/datasets/nvidia/HelpSteer2)
- A community-derived set, `wassname/helpsteer2_dpo_nonverbose` (MIT), exists (contents not inspected). — [HF](https://huggingface.co/datasets/wassname/helpsteer2_dpo_nonverbose)
- Fit: **B**. Verbosity and coherence are coarse padding proxies, from crowd raters, on general assistant responses.

**9. HelpSteer3-Preference**
- arXiv 2505.11475, NeurIPS 2025 Datasets & Benchmarks. **40,476** preference pairs, each with up to 3 annotators' 1–2 sentence rationales. CC-BY-4.0. — [arXiv](https://arxiv.org/abs/2505.11475); [HF card](https://huggingface.co/datasets/nvidia/HelpSteer3)
- Fit: **B−**. The rationales are general helpfulness judgments, not style.

**10. WritingPreferenceBench**
- Paper: "Beyond Correctness: Evaluating Subjective Writing Preferences Across Cultures", Shuangshuang Ying et al. (24 authors). arXiv 2510.14616, 2025-10. — [arXiv](https://arxiv.org/abs/2510.14616)
- HF `m-a-p/Writing-Preference-Bench`, **Apache-2.0**. **1,800** pairs (1,200 EN / 600 ZH) across 8 macro domains, including **Non-Fiction, Functional Documents, Promotional & Communication**. Pairs are matched for correctness, factuality and length. Labels come from 11 expert annotators after 8 hours of rubric calibration, on a 0–3 scale; a pair is kept only if at least 2 of 3 agree and Δscore ≥ 1. — [HF card](https://huggingface.co/datasets/m-a-p/Writing-Preference-Bench)
- Results: sequence-classifier reward models average 52.7% accuracy, zero-shot LLM judges 53.9%, and generative RMs with reasoning 81.8%. — [arXiv](https://arxiv.org/abs/2510.14616)
- Caveat: chosen responses average 1,450 characters/words vs. 840 for rejected in English, so length is not perfectly controlled despite the claim. — [HF card](https://huggingface.co/datasets/m-a-p/Writing-Preference-Bench)
- Fit: **B as an eval set** (the nonfiction and functional slices). Too small to train on.

**11. LitBench** (creative only; noted for completeness)
- Daniel Fein, Sebastian Russo, Violet Xiang, Kabir Jolly, Rafael Rafailov, Nick Haber. arXiv 2507.00769, 2025-07-01. 2,480 debiased test pairs and 43,827 training pairs, labeled by Reddit r/WritingPrompts upvotes. — [arXiv](https://arxiv.org/abs/2507.00769)
- HF `SAA-Lab/LitBench-Train` has no license tag. — [HF](https://huggingface.co/datasets/SAA-Lab/LitBench-Train)
- Claude-3.7-Sonnet reached 73% agreement with the human labels; trained Bradley-Terry and generative RMs reached 78%. — [arXiv](https://arxiv.org/abs/2507.00769)
- Fit: **D for nonfiction.**

**12. LMArena human preference sets and the style-control analysis**
- `lmarena-ai/arena-human-preference-55k` (Apache-2.0), `-100k` (no license tag), `-140k` (**CC-BY-4.0**). All are crowd votes on general chat. — [HF 140k](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k); [HF 55k](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-55k)
- The LMSYS style-control blog (2024-08-29; Tianle Li, Anastasios Angelopoulos, Wei-Lin Chiang) adds style covariates to Bradley-Terry: length, markdown headers, bold, lists. Coefficients with both controlled: length 0.249, list 0.031, header 0.024, bold 0.019. "All other markdown effects are second order." — [LMSYS blog](https://lmsys.org/blog/2024-08-28-style-control/)
- Fit: **C/B−**. Crowd votes reward length. This is evidence that raw crowd preference is a *bad* target for anti-slop.

**13. Other general preference sets (not writing-specific)**
- `lmsys/mt_bench_human_judgments`: CC-BY-4.0, 1K–10K size category. — [HF](https://huggingface.co/datasets/lmsys/mt_bench_human_judgments)
- `Anthropic/hh-rlhf`: MIT, arXiv 2204.05862, crowd dialogue preferences. — [HF](https://huggingface.co/datasets/Anthropic/hh-rlhf)
- `openai/summarize_from_feedback`: arXiv 2009.01325, no license tag on HF. — [HF](https://huggingface.co/datasets/openai/summarize_from_feedback)
- `stanfordnlp/SHP`: Reddit upvote preferences over *human* comments, no license tag. — [HF](https://huggingface.co/datasets/stanfordnlp/SHP)
- `openbmb/UltraFeedback`: MIT, arXiv 2310.01377; its labels are GPT-4-generated, not human **[labeler detail not re-fetched]**. — [HF](https://huggingface.co/datasets/openbmb/UltraFeedback)
- Fit: **C/D** for the slop objective.

**14. The Slop Index** (`hgaddipati/slop-index`, **CC-BY-4.0**, GitHub `hgaddipati1118/slop-index`, MIT code)
- 58 models × 112 "everyday writing tasks", **64,636 outputs**: email 17,351; social 16,172; essay 15,562; slack 15,551. — [HF card](https://huggingface.co/datasets/hgaddipati/slop-index)
- Outputs are scored mechanically against pre-ChatGPT human corpora (Enron, pre-2022 tweets, older essays) on conciseness/padding, templating, rhythm and "tells". Separately, a blind crowd arena asks "which feels more like AI slop". — [HF card](https://huggingface.co/datasets/hgaddipati/slop-index)
- The released data carries only **per-model** crowd Elo (`crowd_elo`, `crowd_games`); per-vote, per-item labels are not in the listed files. — [HF card](https://huggingface.co/datasets/hgaddipati/slop-index)
- Fit: **C+**. A large pool of unedited AI functional prose (emails, essays) for negatives, plus a mechanical slop scorer recipe. Per-item human labels are absent.

**15. bench-labs/slop-classification** (MIT)
- **406 rows** with anonymous human votes from −1 (definitely slop) to +1 (not slop) via the "SlopFinder" interface. Samples come mainly from `allenai/preference-test-sets` (241), ultrafeedback (60), orca_dpo_pairs (40) and ultrachat (30). Contributions have ended. — [HF card](https://huggingface.co/datasets/bench-labs/slop-classification); [datasets-server stats](https://huggingface.co/datasets/bench-labs/slop-classification)
- Fit: **B− but tiny.**

**16. "That's AI Slop, You Bot!"** (Jason Miklian, John E. Katsos, arXiv 2606.12073, 2026-06)
- HF `miklia/ai-slop-accusations-reddit-hackernews`, CC-BY-4.0. It contains comment *IDs* (475,997 Reddit; 102,687 HN), **LLM** labels on 7,500 sampled accusations, and human speech-act codes on 300. Comment bodies are not distributed. — [HF card](https://huggingface.co/datasets/miklia/ai-slop-accusations-reddit-hackernews)
- Key finding: "prose features that statistically distinguish AI from human text do not predict which human text gets accused as AI". — [arXiv](https://arxiv.org/abs/2606.12073)
- Fit: **D** as training data. It is useful as a caution about crowd "slop" labels.

**17. Expert reader studies (creative; no confirmed data release)**
- "Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers", Tuhin Chakrabarty, Jane C. Ginsburg, Paramveer Dhillon. arXiv 2510.13939 (v4). Readers: 28 MFA-trained and 516 general.
  - With in-context prompting, MFA readers strongly disfavored AI text for fidelity (OR = 0.16) and quality (OR = 0.13).
  - **Fine-tuning ChatGPT on each author's complete works reversed this** (fidelity OR = 8.16, quality OR = 1.87).
  - Source: [arXiv](https://arxiv.org/abs/2510.13939)
- Data release not checked. **[unverified]**

#### Tier C: AI-vs-human detection corpora (labels by construction; no human quality judgment unless noted)

| Dataset | Paper / venue / arXiv | HF / GitHub | Size & domains | Human edits? | License | Fit |
|---|---|---|---|---|---|---|
| **APT-Eval** | Saha & Feizi, "Almost AI, Almost Human: The Challenge of Detecting AI-Polished Writing", Findings of ACL 2025, [2502.15666](https://arxiv.org/abs/2502.15666) | [smksaha/apt-eval](https://huggingface.co/datasets/smksaha/apt-eval) | 15,004 samples (abstract says 14.7K): 300 pure human texts AI-polished by GPT-4o, Llama3.1-70B, Llama3-8B, Llama2-7B and DeepSeek-V3; degree-based 4,406 + percentage-based 7,379; 6 domains | No. Human→AI *polish* is the reverse direction | MIT | C+. Polished-vs-original pairs isolate what "AI polish" adds |
| **EditLens** | Thai, Emi, Masrour, Iyyer, ICLR 2026, [2510.03154](https://arxiv.org/abs/2510.03154) | [pangram/editlens_iclr](https://huggingface.co/datasets/pangram/editlens_iclr) (gated, auto-approve); [GitHub](https://github.com/pangramlabs/EditLens) | 60k train / 2.4k val / 6k test. Pre-2022 human text from Amazon/Google reviews, WritingPrompts, FineWeb-EDU, XSum, CNN/DM (Enron held out), AI-edited by Claude Sonnet 4, GPT-4.1 and Gemini 2.5 Flash under 303 edit prompts; plus a 1,768-sample Grammarly set ([HTML](https://arxiv.org/html/2510.03154v1)) | No (AI edits of human text). 3 annotators validated the edit-magnitude metrics (Krippendorff's α ≈ 0.66–0.67) | **CC BY-NC-SA 4.0** (non-commercial) | C+. Continuous "how AI-edited" labels |
| **RAID** | Dugan et al., ACL 2024, [2405.07940](https://arxiv.org/abs/2405.07940) | [liamdugan/raid](https://huggingface.co/datasets/liamdugan/raid) | 6M+ generations (card now says 10M+ documents); 11 models, 11–12 attacks, 4 decoding strategies; train/test domains: news, books, abstracts, reviews, Reddit, recipes, Wikipedia, poetry ([card](https://huggingface.co/datasets/liamdugan/raid)) | No | MIT | C. Mass synthetic informational negatives (wiki, news, abstracts) |
| **M4** | Wang et al., [2305.14902](https://arxiv.org/abs/2305.14902); venue **[unverified]** | [mbzuai-nlp/M4](https://github.com/mbzuai-nlp/M4) | Multi-generator, multi-domain, multilingual; domain list **[unverified]** | No | No license on GitHub | C |
| **M4GT-Bench** | Wang et al., [2402.11175](https://arxiv.org/abs/2402.11175); venue **[unverified]** | [mbzuai-nlp/M4GT-Bench](https://github.com/mbzuai-nlp/M4GT-Bench) | Adds mixed human–machine boundary detection | Boundary labels, not edits | No license on GitHub | C |
| **MAGE** | Li et al., ACL 2024, [2305.13242](https://arxiv.org/abs/2305.13242) | [yaful/MAGE](https://huggingface.co/datasets/yaful/MAGE) | 100K–1M rows; diverse domains and LLMs (exact counts **[unverified]**) | No | Apache-2.0 | C |
| **HC3** | Guo et al., [2301.07597](https://arxiv.org/abs/2301.07597) | [Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3) | 10K–100K; human-expert vs ChatGPT answers in open-domain, finance, medical, legal, psychology | No | CC-BY-SA-4.0 | C. Q&A explainers, but ChatGPT-3.5 era |
| **Ghostbuster** | Verma, Fleisig, Tomlin, Klein, NAACL 2024, [2305.15047](https://arxiv.org/abs/2305.15047) | [vivek3141/ghostbuster](https://github.com/vivek3141/ghostbuster); HF mirror [polsci/ghostbuster-essay-cleaned](https://huggingface.co/datasets/polsci/ghostbuster-essay-cleaned) | Student essays, creative writing, news | No | GitHub: NOASSERTION; mirror tagged CC-BY-3.0 | C |
| **CHEAT** | Yu et al., [2304.12008](https://arxiv.org/abs/2304.12008) | [botianzhe/CHEAT](https://github.com/botianzhe/CHEAT) | 35,304 ChatGPT abstracts (Generation, Polish, Mix) | No | MIT | C |
| **MGTBench** | He et al., [2303.14822](https://arxiv.org/abs/2303.14822); venue **[unverified]** | [xinleihe/MGTBench](https://github.com/xinleihe/MGTBench) | Benchmark framework over public datasets (ChatGPT-turbo, Claude, etc.) | No | MIT | C |
| **DetectRL** | Wu et al., NeurIPS 2024 D&B, [2410.23746](https://arxiv.org/abs/2410.23746) | [NLP2CT/DetectRL](https://github.com/NLP2CT/DetectRL); successor DetectRL-X (ACL 2026, [2605.15518](https://arxiv.org/abs/2605.15518), [HF](https://huggingface.co/datasets/WUJUNCHAO/DetectRL-X), MIT) | Domains prone to misuse | Heuristic *simulated* human revisions (word substitution, spelling noise), not real edits | GitHub: none listed | C |
| **TSM-Bench** | Quaremba, Black, Vrandečić, Simperl, [2605.31113](https://arxiv.org/abs/2605.31113) (2026-05) | not checked | Task-specific MGT from real Wikipedia editing tasks (e.g., summarization); multilingual | No | **[unverified]** | C+. Encyclopedic domain |
| **wikipedia-human-ai** | community | [gouwsxander/wikipedia-human-ai](https://huggingface.co/datasets/gouwsxander/wikipedia-human-ai) | 9,970 Wikipedia paragraphs paired with GPT-5-nano rewrites (first-rows check) | No | MIT | D/C. Clean aligned informational pairs |

#### Tier D: human revision corpora (no AI; useful for the *direction* of good edits)

- **IteraTeR**: Du, Raheja, Kumar, Kim, Lopez, Kang, ACL 2022, arXiv 2203.03802. A multi-domain, edit-intention-annotated corpus of iteratively revised formal writing. HF `wanyu/IteraTeR_human_sent` (1K–10K), `_human_doc`, `_full_sent` (100K–1M), `_full_doc`, `_v2`, and `zaemyung/IteraTeR_plus`; **Apache-2.0**. The specific domains (ArXiv, Wikipedia, Wikinews) and intent labels (fluency, coherence, clarity, style, meaning-changed) are **[unverified this session]**. — [arXiv](https://arxiv.org/abs/2203.03802); [GitHub](https://github.com/vipulraheja/iterater); [HF](https://huggingface.co/datasets/wanyu/IteraTeR_full_sent)
- **CoEdIT**: Raheja, Kumar, Koo, Kang, EMNLP 2023 Findings, arXiv 2305.09857. HF `grammarly/coedit`, Apache-2.0, 10K–100K. Built by re-purposing existing human-edit corpora as instructions; the exact composition (~82k pairs, including WNC and IteraTeR) is **[unverified]**. — [arXiv](https://arxiv.org/abs/2305.09857); [HF](https://huggingface.co/datasets/grammarly/coedit)
- **Wiki Neutrality Corpus (WNC)**: Pryzant, Diehl Martinez, Dass, Kurohashi, Jurafsky, Yang, "Automatically Neutralizing Subjective Bias in Text", AAAI 2020, arXiv 1911.09709. Harvested from Wikipedia NPOV edits; code repo `rpryzant/neutralizing-bias` (MIT); data via a bit.ly/Dropbox link. The commonly cited size of ~180k biased→neutral sentence pairs is **[unverified this session]**. — [arXiv](https://arxiv.org/abs/1911.09709); [GitHub](https://github.com/rpryzant/neutralizing-bias)
- **arXivEdits**: Chao Jiang, Wei Xu, Samuel Stevens, EMNLP 2022, arXiv 2210.15067. Community HF copies at `miwytt/arXivEdits_edits` (no license tag). — [arXiv](https://arxiv.org/abs/2210.15067); [HF](https://huggingface.co/datasets/miwytt/arXivEdits_edits)
- **ScholaWrite**: Le et al., arXiv 2502.02904. About 62K LaTeX text changes from 5 CS preprints over 4 months, with writing-intention annotations. HF `minnesotanlp/scholawrite` (Apache-2.0, gated). — [arXiv](https://arxiv.org/abs/2502.02904); [HF](https://huggingface.co/datasets/minnesotanlp/scholawrite)
- **WikiAtomicEdits**: `google-research-datasets/wiki_atomic_edits`, CC-BY-SA-4.0, 100K–1M. — [HF](https://huggingface.co/datasets/google-research-datasets/wiki_atomic_edits)
- **ArgRewrite (V.2)**: not found on HF Hub; **[unverified]**.

#### Tier E: community slop/unslop sets (negatives are synthetic unless noted)

- **jondurbin/gutenberg-dpo-v0.1** (CC-BY-4.0, under 1K rows): chosen = the original Gutenberg chapter (human); rejected = an LLM-written chapter (llama-2-13b-chat, bagel-7b, dolphin-2.2-34b) generated from a synthetic prompt plus the previous chapter's summary. Fiction. — [HF card](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1)
- **nbeerbower** sets (all Apache-2.0):
  - `gutenberg2-dpo`: 293 rows; chosen = human chapter, rejected = LLM chapter. — [HF](https://huggingface.co/datasets/nbeerbower/gutenberg2-dpo)
  - `gutenberg-moderne-dpo`. — [HF](https://huggingface.co/datasets/nbeerbower/gutenberg-moderne-dpo)
  - `human-writing-dpo`: 2,620 rows; chosen = r/WritingPrompts stories with ≥15 upvotes; rejected = output of `Dumpling-Qwen2.5-7B`; filtered by a GPT-4.1-mini judge; NSFW. The author reports that Reddit score correlates only r = 0.092 with the judge's quality score. — [HF](https://huggingface.co/datasets/nbeerbower/human-writing-dpo)
- **sam-paech antislop sets** (no license tag on HF):
  - `gutenbergs_1_2_3_antislop-dpo`: 4,620 rows. — [HF](https://huggingface.co/datasets/sam-paech/gutenbergs_1_2_3_antislop-dpo)
  - `gemma-3-27b-it-antislop-ftpo-preference-dataset`: 12,000 *token-level* chosen/rejected records with a validator class and rule; a 12B variant also exists. — [HF](https://huggingface.co/datasets/sam-paech/gemma-3-27b-it-antislop-ftpo-preference-dataset)
  - Both are generated automatically by the Antislop sampler, which bans over-represented n-grams relative to a human profile. Paper: Paech, Roush, Goldfeder, Shwartz-Ziv, "Antislop", arXiv 2510.15061, which says the code is MIT. The GitHub API shows no license file on `auto-antislop`; `antislop-sampler` is Apache-2.0. — [arXiv](https://arxiv.org/abs/2510.15061); [auto-antislop](https://github.com/sam-paech/auto-antislop); [antislop-sampler](https://github.com/sam-paech/antislop-sampler)
- **cowWhySo/unslop-pairs** (license "other"): 6,569 pairs. Human passages from public corpora (6 registers) are rewritten by LLMs into 7 "slop styles" (hedging, bullet-itis, corporate throat-clearing, inflated vocabulary), fact-checked by a judge model, and shipped as SFT, DPO and classifier formats. — [HF card](https://huggingface.co/datasets/cowWhySo/unslop-pairs)
- **stindardlogic/writing-quality-dpo-100k** (Apache-2.0): 100k pairs. Each rejected text contains exactly one of 19 defects, for example verbose (~10.8k), vague_language, weak_opening, logical_gaps, buried_lede, cliche_heavy, passive_voice_overuse, unclear_antecedents. Synthetic; the generator is undocumented in the part I read. — [HF card](https://huggingface.co/datasets/stindardlogic/writing-quality-dpo-100k)
- **arjun10g/deslop-v3-dpo** (no license tag): 1,340 pairs. Fields include `pair_type` (e.g., `rewrite_hard_negative`), source (e.g., `stackexchange/parenting`) and `register_hint`. — [HF](https://huggingface.co/datasets/arjun10g/deslop-v3-dpo)
- **N8Programs/unslop-good** (CC0-1.0): 1,000 chat rows of the form "Polish this AI passage to feel more human". Provenance is undocumented. — [HF](https://huggingface.co/datasets/N8Programs/unslop-good)
- **alac/deslop-sentence** (Apache-2.0): 14,032 sentence pairs. — [HF](https://huggingface.co/datasets/alac/deslop-sentence)
- **alexreversegpt/ai-writing-tells** (CC-BY-4.0): 100 rows with domain, tell category (e.g., `hedge_and_filler`), AI text, human rewrite and edit tags (e.g., `cut_hedge`, `add_specific`). — [HF](https://huggingface.co/datasets/alexreversegpt/ai-writing-tells)
- **HumanizerBench** (CC-BY-4.0): outputs of humanizer tools scored by 6 commercial detectors. Its card discloses that it is operated by WriteHuman, one of the tools ranked. — [HF](https://huggingface.co/datasets/HumanizerBench/humanizerbench)

### Inferences
- For *informational* nonfiction specifically, the usable human-edit pool comes from three sources:
  - Beemo: about 2.2k items, but no reasons.
  - LAMP: the ~311 nonfiction-ish items, plus all 9.6k categorized edits if you accept transfer from fiction.
  - HelpSteer3-Edit: about 5.7k English general/STEM items, but helpfulness-oriented.
  - This is enough for an eval set or a small DPO/KTO mixing component. It is not enough to be the sole negative signal.
- LAMP's categories (Unnecessary Exposition, Lack of Specificity, Cliché, Awkward Phrasing, Poor Sentence Structure, Purple Prose) overlap well with the Measuring-Slop "Style Quality" and "Information Utility" codes. Together with the Human-Detectors explanation categories (vocabulary, sentence structure, originality, clarity), they give a defensible label schema for annotating the user's own nonfiction negatives.
- WNC (puffery and subjective-intensifier removal on Wikipedia) and IteraTeR (clarity and coherence edits on formal writing) are the best *human* edit-direction data for encyclopedic and instructive registers, even though they contain no AI text.
- Licensing for private, non-commercial use:
  - Everything above is usable.
  - Non-commercial: EditLens (CC BY-NC-SA) and Beemo's No-Robots fields (CC-BY-NC).
  - Unlicensed (no license tag or file): LitBench, the sam-paech sets, M4/M4GT, DetectRL, scarecrow.
  - Most permissive: LAMP (BSD-3), Beemo expert edits (MIT), HelpSteer2/3 (CC-BY-4.0), Human Detectors (MIT), APT-Eval (MIT), RAID (MIT).

### Gaps
- I found no released dataset of expert edits on AI-written *memos, docs, explainers or analyses* with categorized reasons. The Measuring-Slop annotations would be the closest, but they remain unreleased as of 2026-11-07.
- I did not measure how many HelpSteer3-Edit change summaries or feedbacks mention style (verbosity, repetition, tone). That requires downloading the data.
- Not re-verified this session: Scarecrow's full category list and venue, M4/M4GT/MAGE domain lists, WNC size, IteraTeR domains and intents, CoEdIT composition, and the release status of the Chakrabarty et al. 2025 reader-study data.
- APT-Eval's 6 domain names were not captured (the card section was truncated).
- EQ-Bench Longform/Creative judge data: I did not verify where it is released or who the judge is. The HF copy `Disya/eq-bench-creative-writing-v3` has no license tag. It is creative-only and almost certainly LLM-judged.
- I could not confirm whether the post-editing-for-personal-style study (Baumler et al., ACL 2026, arXiv 2604.24444; 81 participants) releases its post-edits. — [arXiv](https://arxiv.org/abs/2604.24444)

---

## Q2. Is there any validated reward model or classifier for "AI slop / writing quality" we could run locally (size, license, reported agreement with experts)?

### Takeaway
Yes, but only for adjacent targets, and validation is thin. **WQRM** (ModernBERT-large, MIT) is the only small, openly licensed writing-quality reward model validated against professional writers. It reaches 74.3% on the WQ benchmark, and in a test-time selection study experts preferred its picks 66% of the time (72.2% when the reward gap is over 1). It was trained almost entirely on fiction-heavy LAMP, so it needs re-validation on nonfiction. **EditLens** (RoBERTa-large / Llama-3.2-3B, CC BY-NC-SA) is a validated *AI-ness / AI-editing-extent* scorer. The **WritingBench critic** (Qwen2.5-7B, Apache-2.0) is a rubric scorer whose human-agreement numbers I did not verify. Community "slop detectors" on HF are unvalidated.

### Cited Findings
- **Salesforce/WQRM**:
  - Model: **MIT** license, base `answerdotai/ModernBERT-large`, trained on LAMP-PR (pairwise plus regression).
  - **Salesforce/WQRM-PRE** adds 100 expert-written and 83 MFA-written paragraphs.
  - The card says the models "are trained on shorter text" and recommends scoring at paragraph level and averaging.
  - Source: [HF WQRM](https://huggingface.co/Salesforce/WQRM); [HF WQRM-PRE](https://huggingface.co/Salesforce/WQRM-PRE); [GitHub README](https://github.com/salesforce/creativity_eval/tree/main/WritingRewards)
- WQ accuracy (overall, then Synthetic Mirror / Art or Artifice / LAMP / Style Mimic / LM Arena):
  - MBERT-WQRM-PR: **74.3%** (99.8 / 80.6 / 72.6 / 67.3 / 51.0).
  - MBERT-WQRM-R: 73.4%.
  - MBERT-WQRM-P: 67.7%.
  - Best Llama-3.1-70B generative WQRM: 70.2%.
  - Source: [arXiv HTML](https://arxiv.org/html/2504.07532v3)
- Baselines on WQ (overall): GPT-4o zero-shot 40.9, 5-shot 54.3; o1 51.7; o3 64.3; DeepSeek-R1 46.0; Skywork-8B-v0.2 RM 60.5; Pangram AI detector 65.0. — [arXiv HTML](https://arxiv.org/html/2504.07532v3)
- Expert validation:
  - 9 professional writers (from top US MFA programs) produced 300 triplet rankings over 100 drafts covering fiction, **non-fiction and marketing**.
  - Average rank: best-WQRM edit 1.58, random edit 2.09, first draft 2.26.
  - The abstract reports experts preferring WQRM-selected outputs 66% overall and 72.2% when the reward gap is over 1 point.
  - Agreement with experts was 55% for gaps ≤0.5 and 80% for gaps >3.0.
  - Source: [arXiv](https://arxiv.org/abs/2504.07532); [arXiv HTML](https://arxiv.org/html/2504.07532v3)
- **ConicCat/Lamp-P-Writing-Quality-RM**: a community Llama-3.2-3B Bradley-Terry RM trained on Lamp-P, licensed llama3.2. It claims "100%" accuracy on its own validation split, with no external validation. **ConicCat/Litbench-Creative-Writing-RM-3B** is creative-only. — [HF](https://huggingface.co/ConicCat/Lamp-P-Writing-Quality-RM); [HF](https://huggingface.co/ConicCat/Litbench-Creative-Writing-RM-3B)
- **EditLens**:
  - Models: `pangram/editlens_roberta-large` and `pangram/editlens_Llama-3.2-3B`, **CC BY-NC-SA 4.0**. The model cards returned 401 when fetched (gated).
  - Inference outputs a bucket and a continuous score in [0, 1].
  - Reported binary F1 94.7% and ternary F1 90.4% (human / AI / mixed). Its edit-magnitude metrics were validated by 3 annotators (α ≈ 0.66–0.67).
  - Community quantized ports exist, e.g., `benreeve/editlens-roberta-large-onnx-int8`.
  - Source: [GitHub](https://github.com/pangramlabs/EditLens); [arXiv](https://arxiv.org/abs/2510.03154); [arXiv HTML](https://arxiv.org/html/2510.03154v1); [HF ONNX](https://huggingface.co/benreeve/editlens-roberta-large-onnx-int8)
- **WritingBench-Critic-Model-Qwen-7B** (Apache-2.0): fine-tuned from Qwen2.5-7B-Instruct on a 50K SFT set. It scores each criterion 1–10 with a justification; GGUF quantizations are available (mradermacher). — [HF](https://huggingface.co/AQuarterMile/WritingBench-Critic-Model-Qwen-7B); [arXiv](https://arxiv.org/abs/2503.05244); [GitHub](https://github.com/X-PLUG/WritingBench)
- Generative RMs with reasoning reach 81.8% on WritingPreferenceBench, versus 52.7% for sequence-classifier RMs. This suggests small classifier heads miss subjective quality. — [arXiv](https://arxiv.org/abs/2510.14616)
- Measuring-Slop: zero-shot LLM slop judgments had near-zero agreement with copy-editors (κ = 0.01 for GPT-5). A fine-tuned Qwen-7B span extractor reached 0.32 precision / 0.30 recall, but it is not released. — [arXiv HTML](https://arxiv.org/html/2509.19163v3)
- Community "slop detectors", none with independent validation:
  - `distil-labs/distil-ai-slop-detector-gemma`: Gemma-3-270M, Gemma license, distilled from GPT-OSS-120B labels; it claims 100% on its own test set. — [HF](https://huggingface.co/distil-labs/distil-ai-slop-detector-gemma)
  - `gouwsxander/slop-detector-bert`: Apache-2.0 LoRA on bert-base-cased, trained only on Wikipedia paragraphs vs. GPT-5-nano rewrites. — [HF](https://huggingface.co/gouwsxander/slop-detector-bert)
  - `underscore2/modernbert_*_slop_classifier` (Apache-2.0) and `trentmkelly/slop-detector-mini-2` (HF search listing).
- An LLM-judge reward needs explicit length control. The `rawmodels/unslop-harbor` authors report that their Claude Opus 5.5 rubric judge followed length compliance "in 18 of 23 decided tasks" until they added a length-ignore clause. — [HF card](https://huggingface.co/datasets/rawmodels/unslop-harbor)

### Inferences
- On an M4 Pro with 24 GB, WQRM (ModernBERT-large; about 395M parameters **[size from general knowledge, unverified]**) and EditLens-RoBERTa-large run trivially, and the 3B and 7B scorers fit at 4–8-bit.
- A practical stack:
  - EditLens or a Human-Detectors-style detector for "AI-ness".
  - WQRM at paragraph level for craft-level quality.
  - A slop-lexicon and template scorer for surface tells (Antislop, Slop Index mechanical axes).
- None of these is validated on memo, doc or explainer prose. A small in-house expert-labeled eval set of 100–300 pairs in the target domain is needed before trusting any of them as a reward.
- WQRM's 51% on LM Arena pairs and 99.8% on Synthetic Mirror pairs suggest it is strong at "human vs. AI-ish" and weak at ranking two AI outputs. That matches a negative-signal use (penalizing slop) better than fine-grained ranking.

### Gaps
- I did not verify the WritingBench paper's reported critic–human agreement, or its domain list (I recall 6 domains, including academic/engineering and finance/business, and about 1,239 queries **[unverified]**).
- No published head-to-head of WQRM, EditLens and the WritingBench critic on nonfiction exists that I found.
- The exact parameter counts and MLX conversion status of WQRM and EditLens were not checked.

---

## Q3. How much do human-labeled sets add over cheap synthetic negatives (LLM text as "rejected")? Any ablations?

### Takeaway
I found **no direct ablation**, in any paper, that trains the same writing model on human-edited/labeled negatives vs. synthetic LLM negatives and compares the results. The WQRM paper, the obvious candidate, does not report one. The indirect evidence consistently points one way: synthetic human-vs-AI pairs are easy and teach superficial tells, while human edits and expert labels carry the harder AI-vs-AI quality signal. But human labels of "slop" are themselves noisy, so they work best as span- or category-level edits, not binary verdicts.

### Cited Findings
- The WQRM paper reports no ablation of expert edits vs. synthetic/LLM negatives. Its training uses AI paragraphs paired with expert edits (LAMP). — [arXiv HTML](https://arxiv.org/html/2504.07532v3)
- Synthetic human-vs-AI pairs are nearly trivially separable, while AI-vs-AI quality is not. WQRM scores 99.8% on Synthetic Mirror (author vs. AI mirror) but 51.0% on crowd LM Arena pairs and 67.3% on Style Mimic. An off-the-shelf AI detector (Pangram) scores 65.0% overall on WQ, beating GPT-4o and o1. — [arXiv HTML](https://arxiv.org/html/2504.07532v3)
- Human vs. LLM editing differs measurably. In Beemo, expert-edited AI text evades MGT detectors, while LLM-"humanized" text is unlikely to be recognized as human-written. LLM edits therefore keep the AI signature that human edits remove. — [arXiv](https://arxiv.org/abs/2411.04032)
- Experts largely prefer expert-edited text over automatically edited text (LAMP preference study). — [arXiv](https://arxiv.org/abs/2409.14509)
- Training only on generic synthetic MGT overfits to superficial artefacts. TSM-Bench reports that fine-tuning on task-specific data generalizes to generic data, "but not vice versa", and that detection accuracy drops 10–40% on realistic Wikipedia editing tasks. — [arXiv](https://arxiv.org/abs/2605.31113)
- Antislop: on its automatically generated slop preference data, FTPO achieved 90% slop reduction while maintaining or improving benchmarks. **DPO "suffers significant degradation in writing quality and lexical diversity despite achieving weaker suppression."** Some slop patterns appear over 1,000× more often in LLM output than in human text. — [arXiv](https://arxiv.org/abs/2510.15061)
- Standard RMs mostly learn objective errors. On WritingPreferenceBench (correctness and length matched), sequence-classifier RMs average 52.7%; generative RMs with reasoning reach 81.8%. — [arXiv](https://arxiv.org/abs/2510.14616)
- Human "slop" labels are noisy at the binary level:
  - Copy-editors' binary slop κ ranged from −0.12 to 0.11, while span counts correlated with the slop label (ρ = 0.63). — [arXiv HTML](https://arxiv.org/html/2509.19163v3)
  - Crowd "AI slop" accusations online are not predicted by the prose features that distinguish AI text. — [arXiv](https://arxiv.org/abs/2606.12073)
  - Reddit upvotes correlate only r = 0.092 with an LLM judge's quality score (community dataset note). — [HF](https://huggingface.co/datasets/nbeerbower/human-writing-dpo)
  - Crowd chat preferences are strongly length-driven (style-control length coefficient 0.249, against ≤0.031 for markdown features). — [LMSYS blog](https://lmsys.org/blog/2024-08-28-style-control/)
- Human post-edits of AI drafts do not equal the author's own voice. In a pre-registered study (n = 81), post-edited text moved toward participants' unassisted writing but "still remains stylistically closer in style to LLM text", with less stylistic diversity than unassisted human text. — [arXiv](https://arxiv.org/abs/2604.24444)
- Even when prompted with expert feedback and told to make only grammar edits, LLM revisions significantly alter semantic meaning. This argues against LLM-generated "fixed" versions as the *chosen* side. — [arXiv](https://arxiv.org/abs/2603.18161)
- Fine-tuning on an author's complete works, not in-context imitation, was what made AI excerpts preferred by MFA readers (fidelity OR 0.16 → 8.16). That supports the project's QLoRA-on-author-corpus approach as the primary lever. — [arXiv](https://arxiv.org/abs/2510.13939)
- Scale comparison for AI-ness in the wild: Pangram labels 27.5% of tokens in June 2026 FineWeb-filtered web data as AI-generated (31.1% by August). The authors recommend filtering AI text when the target is human text. — [arXiv](https://arxiv.org/abs/2609.40295)
- Tangential (QA, not writing; search-snippet level **[unverified]**): a 2026 "Style-Debiased DPO" paper reports that when rejected responses are mostly correct and differ only in style, vanilla DPO/IPO/KTO fail to beat baseline. — [arXiv](https://arxiv.org/abs/2609.16532)

### Inferences
- Cheap synthetic negatives are good for *suppressing surface tells*: author text as chosen and an LLM rewrite of the same content as rejected, in the style of gutenberg-dpo, cowWhySo/unslop-pairs or RAID/Wikipedia pairs. But they risk teaching only those surface tells (TSM-Bench), and plain DPO on them can hurt quality and diversity (Antislop). Token- or span-level objectives (FTPO-like) or small DPO β with SFT anchoring look safer.
- Human edits (LAMP, Beemo, HelpSteer3-Edit) add value mainly as follows:
  - Hard negatives where both sides are fluent: the AI draft vs. the expert fix.
  - Categorized spans that let you target exposition, cliché and vagueness instead of vocabulary only.
  - An eval set that does not share the generator's artefacts.
- Because post-edited text stays closer to LLM style than to the author's own writing, the *chosen* side should be the target author's real prose wherever possible. Human edits of AI text work best as an intermediate rung (AI draft < expert edit < author original), not as the ceiling.
- Binary human slop labels are too noisy to train on directly. Span-level, category-coded edits or pairwise judgments with a minimum score gap (as in WritingPreferenceBench's Δ ≥ 1 rule) are the more reliable formats.

### Gaps
- No controlled study compares human-edited vs. LLM-generated negatives for writing-quality or style DPO, nor reports how many human pairs equal N synthetic pairs. This is an open question; the project would have to run the ablation itself, for example on the LAMP nonfiction slice plus Beemo vs. matched synthetic rewrites.
- The full text of the Antislop DPO-vs-FTPO comparison (numbers, model sizes) was not read beyond the abstract.
- The Style-Debiased DPO result (arXiv 2609.16532) is known only from a search snippet.
