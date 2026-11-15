# Multi-stage and agentic LLM systems for long-form expository writing: what the harness contributed

Scope: 2022 to mid-November 2026. Status labels: **[PR]** = peer-reviewed venue confirmed in this session (arXiv comment field or proceedings page); **[PP]** = preprint or venue not confirmed in this session; **[BLOG]** = company post or press. "LLM judge only" is stated wherever no human evaluation of output quality was reported. Numbers were extracted from the arXiv HTML or PDF of each paper; where a paper's text and tables disagree, that is noted.

Venue confirmations come from the arXiv API comment field ([query used](https://export.arxiv.org/api/query?id_list=2402.14207,2408.15232,2501.09751,2409.02076,2411.00816,2406.19371,2504.08725,2510.24428,2508.19611,2210.06774,2212.10077)): STORM = NAACL 2024 main; Co-STORM = EMNLP 2024 main; OmniThink = EMNLP 2025; LongGenBench = ICLR 2025; CycleResearcher = ICLR 2025; Suri = EMNLP 2024 Findings; DocAgent = ACL 2025 (demo track per Anthology ID 2025.acl-demo.44); CodeWiki = ACL 2026; Instructional Agents = "ECAL'26 main conference"; Re3 = EMNLP 2022; DOC = ACL 2023; AutoSurvey2 = TKDD 2025. WebWeaver is listed as an [ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10009906). All others below carry no venue in the arXiv record and are marked [PP] even where I believe a venue exists (see Gaps in the census section).

---

## 1. Encyclopedic and report writing (STORM, Co-STORM, WikiCrow/PaperQA2, OmniThink, deep-research report generators and benchmarks)

### Takeaway
In this family the measured harness gain is in coverage, organisation and citation grounding, and the largest single lever is the pre-writing stage (question asking that feeds an outline): removing STORM's outline stage drops it almost to plain RAG, and in TTD-DR the agent workflow moves win rate against OpenAI Deep Research from 35% (same model with a search tool) to 69%. No system in this family measures prose style or "AI-sounding" quality; the one benchmark with a style dimension (DEER) finds deep-research harnesses score no better, and slightly worse, on Format & Style than the bare reasoning model.

### Cited Findings

**STORM [PR, NAACL 2024]**
- Pipeline: (1) perspective discovery from tables of contents of related Wikipedia articles, N=5 perspectives plus a "basic fact writer"; (2) simulated conversations, M=5 rounds, between a question-asking writer LLM and a search-grounded expert LLM; (3) outline drafted from the topic alone, then refined with the conversations; (4) section-by-section writing from retrieved sources, concatenation, de-duplication, lead writing. Models: gpt-3.5-turbo for question asking, gpt-3.5-turbo-instruct for other steps, gpt-4 for outline and final article; You.com search; zero-shot DSPy prompts. — [STORM](https://arxiv.org/abs/2402.14207)
- Dataset: FreshWiki, 100 recent high-quality Wikipedia articles (B-class or better, under 3,000 words; mean 2,159 words, 90 references). — [STORM](https://arxiv.org/abs/2402.14207)
- Automatic article results (rubric scores 1-5 by Prometheus-13B, an LLM judge): Direct Gen ROUGE-1 25.62, entity recall 5.08, interest 2.87, organization 4.60, relevance 3.10, coverage 4.16; RAG 28.52 / 7.57 / 3.14 / 4.22 / 3.05 / 4.08; outline-driven RAG (oRAG) 44.26 / 12.57 / 3.90 / 4.79 / 4.09 / 4.70; STORM 45.82 / 14.10 / 3.99 / 4.82 / 4.45 / 4.88. — [STORM](https://arxiv.org/abs/2402.14207)
- Ablation, article level: STORM without the outline stage falls to ROUGE-1 26.77, entity recall 7.39, interest 3.33, relevance 3.35, coverage 4.37, which is roughly the plain-RAG level. The jump from RAG to oRAG (adding any outline) is far larger than the jump from oRAG to STORM (adding perspectives and conversations). — [STORM](https://arxiv.org/abs/2402.14207)
- Ablation, outline level (heading soft recall / heading entity recall vs the human article, GPT-4): Direct Gen 87.66 / 34.78; RAG 89.55 / 42.38; STORM 92.73 / 45.91; without perspectives 92.39 / 42.70; without conversation 88.75 / 39.30. Unique references collected fall from 99.83 (full) to 54.36 without perspectives and 39.56 without conversation. Simulated conversation matters more than perspective assignment. — [STORM](https://arxiv.org/abs/2402.14207)
- Citation quality (Mistral-7B judge): citation recall 84.83%, precision 85.18%; the most common error was improper inferential linking. — [STORM](https://arxiv.org/abs/2402.14207)
- Human evaluation: 10 experienced Wikipedia editors (500+ edits), 20 topic pairs, each pair rated by two editors, 1-7 scale, STORM vs oRAG (not vs direct generation). Organization 4.00 vs 3.25 (p=0.005) is the only significant gain; interest 4.03 vs 3.63 (p=0.077), coverage 4.00 vs 3.58 (p=0.084), relevance 4.15 vs 3.93 (p=0.347), verifiability 3.80 vs 3.85 (p=0.843). Pairwise preference 26 vs 14 for STORM. — [STORM](https://arxiv.org/abs/2402.14207)
- Weaknesses editors reported: 7 of 10 said the articles sounded "emotional" or "unneutral" (tone and bias transferred from web sources); over-association of unrelated facts, with lower verifiability in over half of the 14 cases where oRAG was preferred; articles less informative than real Wikipedia pages. All 10 agreed STORM helps the pre-writing stage. — [STORM](https://arxiv.org/abs/2402.14207)

**Co-STORM [PR, EMNLP 2024]**
- Pipeline: a roundtable of N=3 simulated experts plus a moderator that asks questions drawn from retrieved-but-unused sources; a tree-structured mind map organises collected information; the final cited report is generated from the mind map. Model gpt-4o-2024-05-13 for all roles; You.com search. Dataset WildSeek, 100 topic-goal pairs from real STORM web-app users. — [Co-STORM](https://arxiv.org/abs/2408.15232)
- Automatic report scores (Prometheus-2 7B judge, 1-5): RAG chatbot relevance 3.57, breadth 3.50, depth 3.26, novelty 2.44; STORM + QA 3.61 / 3.61 / 3.43 / 2.50; Co-STORM 3.78 / 3.79 / 3.77 / 3.05. Unique URLs 2.94, 2.89 and 6.04. Largest gains are depth and novelty. — [Co-STORM](https://arxiv.org/abs/2408.15232)
- Ablation: without the moderator depth falls to 3.41 and novelty to 2.89; with one expert instead of several, depth stays 3.77 and novelty 2.93. The moderator (steering toward unused sources) matters more than the number of expert personas. — [Co-STORM](https://arxiv.org/abs/2408.15232)
- Human evaluation: 20 volunteers (19 analysed). 70% preferred Co-STORM over a search engine (n=10); 78% preferred it over a RAG chatbot (n=9). Significant gains were on breadth vs RAG (p=0.013) and serendipity (p=0.030 and p=0.009). The automatic judge's correlation with human rubric scores on 50 utterances was Pearson 0.32-0.55. — [Co-STORM](https://arxiv.org/abs/2408.15232)

**OmniThink [PR, EMNLP 2025]**
- Pipeline: iterative expansion and reflection that grows an "information tree" and a "conceptual pool"; concept-guided outline; parallel section writing with per-section retrieval, concatenation, de-duplication and polish. Built on STORM and DSPy; GPT-4o default; Bing search. — [OmniThink](https://arxiv.org/abs/2501.09751)
- New metric, knowledge density (unique atomic facts per unit length). GPT-4o backbone on WildSeek: RAG relevance 4.65, breadth 4.55, depth 4.59, novelty 4.22, KD 22.11; STORM 4.34 / 4.21 / 4.21 / 3.80 / 19.33; Co-STORM (no human) 4.37 / 4.66 / 4.65 / 3.89 / 19.53; OmniThink 4.77 / 4.71 / 4.66 / 4.31 / 22.31. Note that plain RAG beats STORM and Co-STORM on every rubric score and on knowledge density in this table. — [OmniThink](https://arxiv.org/abs/2501.09751)
- Ablation (figure only, no numbers in text): removing expansion and reflection hurts all metrics, most on information diversity and novelty; expansion drives density, breadth and depth; reflection drives novelty. — [OmniThink](https://arxiv.org/abs/2501.09751)
- Human evaluation: 15 volunteers with at least an undergraduate degree, 20 topics, OmniThink vs Co-STORM; about 11% higher breadth, a marginal novelty gap, and about 30% of pairs judged equal. Rubric scores are otherwise an LLM judge (Prometheus-2). — [OmniThink](https://arxiv.org/abs/2501.09751)

**PaperQA2 and WikiCrow [PP; arXiv 2409.13740, FutureHouse]**
- WikiCrow writes Wikipedia-style articles on human protein-coding genes by combining four PaperQA2 queries (one per section) with one GPT-4-Turbo overview call. 240 articles, mean 1,219 words (Wikipedia 890), about $4.48 and 490 seconds each. — [PaperQA2](https://arxiv.org/abs/2409.13740)
- Human expert evaluation: 375 statements sampled from the 240 paired articles, graded by four experts blinded to source. Cited-and-unsupported statements 13.5% (WikiCrow) vs 24.9% (Wikipedia), p=0.0075; uncited 3.5% vs 13.6%; citation precision 86.1% vs 71.2%, p=0.0013; reasoning errors 12 vs 26. Evaluator agreement on 40 overlapping statements was 77.5%. — [PaperQA2](https://arxiv.org/abs/2409.13740)
- Ablations (on the LitQA2 QA benchmark, not on writing): removing rerank-and-contextual-summarisation (RCS) significantly lowered accuracy (p<0.001); replacing the agent with a hard-coded pipeline lowered accuracy (p=0.015); removing citation traversal lowered DOI recall (p=0.022). — [PaperQA2](https://arxiv.org/abs/2409.13740)
- The paper does not evaluate prose quality; the metrics are citation support and factual accuracy. — [PaperQA2](https://arxiv.org/abs/2409.13740)

**Deep-research report generators**
- TTD-DR (Google, [PP]) treats report writing as iterative "denoising" of a draft with retrieval, plus component-wise self-evolution (multi-variant sampling, LLM-judge scoring, critique-based revision, merging). Its ablation is the cleanest harness-vs-model decomposition found. Win rate against OpenAI Deep Research on LongForm Research (205 queries) and DeepConsult: Gemini-2.5-pro alone 31.0 / 17.6; Gemini-2.5-pro with search tool 35.0 / 19.6; backbone DR agent 39.4 / 24.5; plus self-evolution 60.9 / 59.8; plus diffusion with retrieval (full) 69.1 / 74.5. — [TTD-DR](https://arxiv.org/abs/2507.16075)
- TTD-DR's judge is an LLM (Gemini-1.5-pro) calibrated on 200 human side-by-side comparisons; its agreement with humans was 60.8% accuracy and 0.22 correlation, against 69.0% human-human accuracy. — [TTD-DR](https://arxiv.org/abs/2507.16075)
- TTD-DR also reports other harnesses run against OpenAI Deep Research: Perplexity DR 21.8 / 32.0, Grok DeeperSearch 16.1 / 16.0, GPT-Researcher 18.3 / 9.4, Open Deep Search 2.6 / 2.2. — [TTD-DR](https://arxiv.org/abs/2507.16075)
- WebWeaver (Alibaba, [PR, ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10009906)): a planner interleaves search with outline revisions whose sections cite evidence IDs in an external memory bank; a writer composes section by section, retrieving only the cited evidence and pruning it afterwards. With Claude Sonnet 4 it scores 50.58 on DeepResearch Bench RACE (Gemini-2.5-pro Deep Research 49.71) with 93.37% citation accuracy. — [WebWeaver](https://arxiv.org/abs/2509.13312)
- WebWeaver ablations (LLM judge only): outline optimisation rounds raise comprehensiveness 48.85 to 50.82 and insight 46.33 to 48.35; LLM-judged outline quality rises 81.9 to 92.3. Section-wise hierarchical writing vs brute-force single-pass writing with all evidence in context: insight 42.72 to 50.02, readability 43.82 to 49.79, citation accuracy 86.73% to 93.37%. This is one of the few results where a writing-stage scaffold improves a readability score. No same-model no-harness baseline and no human evaluation. — [WebWeaver](https://arxiv.org/abs/2509.13312)

**Deep-research benchmarks**
- DeepResearch Bench [PP]: 100 PhD-level tasks (50 Chinese, 50 English), 22 fields. RACE scores comprehensiveness, insight, instruction following and readability relative to a reference report, judged by Gemini-2.5-Pro; FACT checks citations. RACE pairwise agreement with human experts 71.33% (human-human 68.44%), from 70+ annotators on 50 Chinese tasks. — [DeepResearch Bench](https://arxiv.org/abs/2506.11763)
- DeepResearch Bench scores: Gemini-2.5-Pro Deep Research 48.88 overall (readability 49.44), OpenAI Deep Research 46.98 (47.14), Perplexity DR 42.25, Grok Deeper Search 40.24. Search-enabled LLMs without the product harness: Claude-3.7-Sonnet w/ search 40.67, Gemini-2.5-Pro-Grounding 35.12, GPT-4.1 w/ search 33.46. The Gemini pair (48.88 vs 35.12 for a same-family model with grounding) is the nearest thing to a same-model harness delta, though the product's underlying configuration is not disclosed. — [DeepResearch Bench](https://arxiv.org/abs/2506.11763)
- ResearchRubrics (Scale AI, [PP]): 101 prompts, 2,593 expert-written rubric criteria, 2,800+ human hours. Compliance: Gemini DR 67.7%, OpenAI DR 66.4%, Perplexity DR 56.6%. Implicit reasoning and synthesis account for roughly 45-50% of failures; explicit requirements and communication quality fail under 20% of the time. Longer reports score higher (r about 0.20-0.28). Judge-human macro F1 0.72-0.76 (binary). — [ResearchRubrics](https://arxiv.org/abs/2511.07685)
- DEER [PP]: 50 expert report tasks, 13 domains, 7 dimensions including Format & Style. Format & Style is highest for reasoning-only models (about 7.2-8.1 of 10) and lower for deep-research systems (about 7.0-7.5); Information Integrity rises from about 1.1-2.3 without search to 5.1-7.0 with search or deep research; Request Fulfillment and Analytical Soundness stay low for all (about 4.2-6.2). GPT-5.2 with thinking and search (mean 6.62) outscored every deep-research product (5.98-6.50). Judge validated against two experts on 45 reports (Pearson 0.73 with expert guidance; inter-human 0.81). — [DEER](https://arxiv.org/abs/2512.17776)

### Inferences
- The attribution the literature supports is: the harness buys what the model cannot see or hold (retrieved evidence, breadth of sub-questions, a global plan), and the organisation that follows from an outline. STORM's only statistically significant human-rated gain over an outline-RAG baseline is organisation.
- Where the baseline already has an outline, the marginal gain from elaborate pre-writing (personas, roundtables) is modest and partly unreplicated: OmniThink's table has plain RAG beating STORM and Co-STORM on the same rubric.
- The harness share shrinks as base models improve: by late 2025 DEER shows a frontier model with search and reasoning outscoring dedicated deep-research products, whereas in mid-2025 TTD-DR shows a 2x win-rate gain from workflow over the same model with search.
- Prose quality is treated as solved or ignored. Readability dimensions exist (RACE, DEER) but are LLM-judged and move with content scores; DEER's result suggests retrieval-heavy harnesses can slightly degrade style.

### Gaps
- No STORM-family paper compares against a single-pass baseline with human raters; human studies use oRAG, a RAG chatbot or Co-STORM as the comparator.
- OmniThink's ablation and human-study numbers are in figures only.
- I did not retrieve published evaluations of open implementations such as GPT-Researcher or LangChain Open Deep Research beyond their appearance as baselines in TTD-DR.
- I found no study that measures stylistic distance between STORM or deep-research output and human-written reference text.

---

## 2. Survey and scientific writing (AutoSurvey, SurveyX, SurveyForge, LLMxMapReduce-V2, AI Scientist, CycleResearcher, Agents4Science)

### Takeaway
Survey harnesses reliably lift citation recall and precision and structure scores over naive RAG, but content-quality gains on LLM-judged rubrics are small (a few tenths of a point on a 5-point scale), and an independent benchmark puts every system about 21% below human surveys on content with fluency already near ceiling. For AI-written research papers, human reviewers' complaints are about hallucinated references, overclaiming, shallow analysis and lack of creativity, and not about sentence-level prose.

### Cited Findings

**AutoSurvey [PP in arXiv record; arXiv 2406.10252]**
- Pipeline: retrieval and outline generation (outlines from paper chunks, merged); parallel subsection drafting with per-section retrieval; integration and refinement (each section polished against neighbours, citations checked); multi-LLM-judge evaluation selecting the best of N candidates. Writer Claude-3-Haiku; judges GPT-4, Claude-3-Haiku, Gemini-1.5-Pro. — [AutoSurvey](https://arxiv.org/abs/2406.10252)
- At 64k tokens: naive RAG citation recall 68.79, precision 61.97, content average 4.19 (coverage 4.40, structure 3.66, relevance 4.66); AutoSurvey 82.25 / 77.41 / 4.62 (4.73 / 4.33 / 4.86); human-written 86.33 / 77.78 / 4.88. The naive-RAG gap grows with length: at 8k it is 78.14 / 71.92 / 4.33 vs 82.48 / 77.42 / 4.61. Structure is the content dimension that moves most. — [AutoSurvey](https://arxiv.org/abs/2406.10252)
- Ablation: without retrieval, citation recall 60.11 and precision 51.65 but content average only falls 4.57 to 4.44; without the reflection/refinement stage, 83.23 / 76.36 / 4.56, i.e. almost no change. Base writer swap moves content average 4.58 (Claude-haiku) to 4.70 (GPT-4), which is larger than the refinement stage's effect. — [AutoSurvey](https://arxiv.org/abs/2406.10252)
- Evaluation is LLM judges; human validation was three PhD students ranking 20 surveys, Spearman 0.54 with the judge mixture. — [AutoSurvey](https://arxiv.org/abs/2406.10252)

**SurveyX [PP; KDD 2025 header on the preprint, not confirmed]**
- Pipeline: keyword-expansion retrieval to 1,000 references with two-step filtering; "AttributeTree" pre-processing of each reference into a structured tree; hint-based outline generation with "separate-then-reorganize" de-duplication; sequential subsection drafting; RAG-based rewriting for citations and polish; figure and table generation. GPT-4o throughout. — [SurveyX](https://arxiv.org/abs/2502.14776)
- Results (LLM judge, 20 topics): naive RAG content average 3.872, citation F1 65.20; AutoSurvey 4.331 / 79.76; SurveyX 4.590 / 81.52; human 4.754 / 81.83. — [SurveyX](https://arxiv.org/abs/2502.14776)
- Ablation, the most informative in this family. Content average: full 4.590; without retrieval algorithm 4.48; without RAG rewriting 4.55; without AttributeTree 4.32; without outline optimisation 4.32 (structure 4.91 to 3.80). Citation F1: full 81.52; without retrieval 76.01; without outline optimisation 80.92; without AttributeTree 58.23; without RAG rewriting 55.16. So the post-hoc rewriting stage matters almost entirely for citation correctness, and outline plus source pre-digestion matter for content. — [SurveyX](https://arxiv.org/abs/2502.14776)
- Human evaluation: six PhD students scored content quality; SurveyX beat AutoSurvey on all metrics; human scores were lower than LLM-judge scores, especially for structure (exact values only in a figure). — [SurveyX](https://arxiv.org/abs/2502.14776)

**SurveyForge [PP in arXiv record; arXiv 2503.04629]**
- Pipeline: outline generation by "heuristic learning" from a database of about 20,000 human survey outlines plus 600,000 papers; a memory-driven Scholar Navigation Agent retrieves per subsection with temporal-aware reranking; parallel drafting, merge, refinement. Writers Claude-3-Haiku and GPT-4o-mini; judges GPT-4o and Claude-3.5-Sonnet. — [SurveyForge](https://arxiv.org/abs/2503.04629)
- Results on SurveyBench (10 topics): reference coverage 0.2341 (AutoSurvey) vs 0.3960 (SurveyForge) vs 0.6294 (human); outline score 82.18 vs 86.85 vs 87.62 (human); content average 73.87 vs 76.34. — [SurveyForge](https://arxiv.org/abs/2503.04629)
- Ablation: outline score 81.78 with no heuristic learning, 84.58 with random human outlines as exemplars, 86.67 with domain-related human outlines. Retrieval components (memory, sub-query, temporal reranking) raise reference coverage from 0.2340 to 0.3971. — [SurveyForge](https://arxiv.org/abs/2503.04629)
- Human evaluation: 20 PhD-level experts, 100 outputs, double-blind pairwise vs AutoSurvey; SurveyForge won 74% on outline and 70% on content; Cohen's kappa LLM-vs-human 0.72 (outline) and 0.65 (content). — [SurveyForge](https://arxiv.org/abs/2503.04629)

**LLMxMapReduce-V2 [PP]**
- Pipeline: cluster references, build local skeletons and merge; improve the skeleton by entropy-driven sampling over "convolution" layers of feedback with best-of-N self-refinement; write sections bottom-up over the skeleton tree. Gemini-2.0-flash-thinking for all roles. — [LLMxMapReduce-V2](https://arxiv.org/abs/2504.05732)
- Results on SurveyEval (20 test surveys, LLM judge): Vanilla (single pass over the references) structure 94.44, faithfulness 96.43, language 96.50, criticalness 37.11, claims 78.75, claim density 74.64, reference precision 25.48, recall 26.46. Vanilla + skeleton 98.95 / 97.03 / 95.95 / 41.01 / 135.15 / 72.96 / 62.60 / 65.11. AutoSurvey 86.00 / 93.10 / 92.90 / 68.39 / 423.35 / 31.97 / 50.12 / 51.73. LLMxMapReduce-V2 95.00 / 97.22 / 94.34 / 71.99 / 474.90 / 52.23 / 95.50 / 95.80. — [LLMxMapReduce-V2](https://arxiv.org/abs/2504.05732)
- Reading of that table: the single-pass baseline scores highest on the Language dimension and on claim density; the harness's gain is volume of claims (6x), critical analysis and reference utilisation, not prose. — [LLMxMapReduce-V2](https://arxiv.org/abs/2504.05732)
- Human evaluation: 17 volunteers, 20 topics, 217 valid pairwise judgments vs AutoSurvey; win rates are in a figure only. — [LLMxMapReduce-V2](https://arxiv.org/abs/2504.05732)

**SurveyBench (independent benchmark, [PP])**
- 20 topics, one high-quality human survey each; evaluates AutoSurvey, SurveyForge, LLMxMapReduce-V2 and OpenAI Deep Research on outline, content (coverage, depth, focus, coherence, fluency), richness of non-text elements, and quiz-answerability. Content averages with human set to 5: OpenAI DR 4.42, LLMxMR-V2 4.20, AutoSurvey 4.03, SurveyForge 4.03. Outline averages: OpenAI DR 3.57, AutoSurvey 3.88, SurveyForge 4.01, LLMxMR-V2 4.37. — [SurveyBench](https://arxiv.org/abs/2510.03120)
- The abstract states LLM4Survey methods score on average 21% below human surveys in content-based evaluation. On topic-specific quizzes (human survey = 10) systems score 1.48-3.19. Fluency is about 4.2-4.3 for all systems, so the deficit is depth, synthesis, cross-concept association and figures and tables, with content "often rewritten directly from cited sources". The general-purpose product (OpenAI DR) has the best content and worst outline; the purpose-built survey harnesses have the reverse. LLM judge; no human validation of judge scores described. — [SurveyBench](https://arxiv.org/abs/2510.03120)

**Other survey harnesses (abstract-level only)**
- SurveyGen-I notes that most prior systems generate subsections in parallel as isolated units and adds evolving plans plus a memory of written content and terminology for cross-section coherence. — [SurveyGen-I](https://arxiv.org/abs/2508.14317)
- Agentic AutoSurvey reports 8.18/10 vs AutoSurvey 4.77/10 on six topics with its own evaluator agent. — [Agentic AutoSurvey](https://arxiv.org/abs/2509.18661)
- AutoSurvey2 [PR, TKDD 2025 per arXiv comment] adds parallel section generation, iterative refinement and real-time retrieval, judged by a multi-LLM framework. — [AutoSurvey2](https://arxiv.org/abs/2510.26012)

**The AI Scientist [PP in arXiv record] and v2**
- Write-up stage: Aider fills a LaTeX conference template section by section (introduction, background, method, setup, results, conclusion) with one self-reflection round per section; 20 rounds of Semantic Scholar queries fill related work and citations; a final per-section refinement pass removes duplication; LaTeX compile errors are fed back. Roughly $10-15 per paper. — [The AI Scientist](https://arxiv.org/abs/2408.06292)
- Reviewer loop: GPT-4o reviewer with 5 self-reflection rounds, 5 ensembled reviews, a meta-review and 1 few-shot example reached balanced accuracy 0.65 on 500 ICLR 2022 papers vs 0.66 for humans; reflection and one-shot each added about 2%; ensembling reduced variance without improving accuracy. Generated papers averaged 3.82 (Sonnet 3.5), 3.70 (GPT-4o), 3.32 (DeepSeek Coder) and 2.30 (Llama-3.1 405B) on the diffusion template, on the automated reviewer's NeurIPS scale. The spread across base models with the harness held fixed is about 1.5 points. — [The AI Scientist](https://arxiv.org/abs/2408.06292)
- Authors' listed writing failures: hallucinated ablation tables and hardware details, intermediate "Run 2"-style artefacts left in the text, positive spin on negative results, miscompared numbers, sparse references (9 in the case-study paper), broken figure references. — [The AI Scientist](https://arxiv.org/abs/2408.06292)
- AI Scientist-v2 removes human-authored code templates, uses agentic tree search, and adds a vision-language-model feedback loop for figures and layout. — [AI Scientist-v2](https://arxiv.org/abs/2504.08066)
- [BLOG] Sakana submitted three v2 papers to an ICLR 2025 workshop (ICBINB; 3 of 43 submissions); one received reviewer scores 6, 7, 6 (average 6.33) and was withdrawn before meta-review. Sakana's own review concluded none of the three met the ICLR main-track bar and noted "embarrassing citation errors" such as attributing LSTMs to the wrong paper. — [Sakana AI](https://sakana.ai/ai-scientist-first-publication/); critical press coverage in [TechCrunch](https://techcrunch.com/2025/03/12/sakana-claims-its-ai-paper-passed-peer-review-but-its-a-bit-more-nuanced-than-that)

**CycleResearcher [PR, ICLR 2025]**
- A fine-tuned open-model writer (Mistral-Nemo-12B, Qwen2.5-72B, Mistral-Large-2) trained with iterative preference optimisation against a fine-tuned reviewer model (CycleReviewer). The paper states that the experimental results in generated papers are fabricated. — [CycleResearcher](https://arxiv.org/abs/2411.00816)
- Simulated review score 5.36 (12B) vs 5.24 for arXiv preprints, 5.69 for accepted papers and 4.31 for AI Scientist. Human evaluation: three NLP experts, 10 papers per system, overall 4.8 vs 3.6 for AI Scientist (presentation 2.8), against 5.5 for ICLR 2024 submissions and 6.4 for accepted papers. The paper has internal inconsistencies (claimed 26.89% MAE reduction vs about 20.7% from its own table; acceptance rate 31.07% in text vs 35.13% in table). — [CycleResearcher](https://arxiv.org/abs/2411.00816)

**Agents4Science 2025 (organisers' report, [PP])**
- 315 submissions, 253 complete, reviewed by three LLM reviewers (GPT-5, Gemini 2.5 Pro, Claude Sonnet 4); the top 79 also by a human expert; 48 accepted. Fully AI-driven work (95%+ AI at all four stages) was 23.3% of submissions but 14.9% of accepted papers. Human involvement was higher in hypothesis and design; manuscript writing and data analysis had the most AI autonomy. Only 16.7% of accepted papers used a specialised research agent; most used general-purpose LLMs. — [Agents4Science report](https://arxiv.org/abs/2511.15534)
- Weaknesses: only about 44% of submissions (111 papers) had no flagged hallucinated reference; authors reported that "a high proportion of references were hallucinated or only loosely related", that models overclaimed, and that ideas lacked creativity and domain depth. LLM reviewers showed sycophancy (Gemini 2.5 Pro mean 4.23 of 6 vs GPT-5 2.30; mean absolute difference from human scores 2.73, 0.91 and 1.09 for Gemini, GPT-5 and Claude). — [Agents4Science report](https://arxiv.org/abs/2511.15534)

### Inferences
- Across four survey systems the stage ranking is consistent: retrieval and source pre-digestion determine citation metrics; the outline determines structure scores; a final critique or polish pass contributes little to content scores (AutoSurvey: 4.57 to 4.56) and is useful mainly for fixing citations (SurveyX).
- LLM-judged content scores are compressed near ceiling (naive RAG 3.9-4.3, systems 4.3-4.6, human 4.75-4.9 on a 5-point scale), so reported "near-human" results depend on a judge with little headroom. SurveyX's own human raters scored lower than the judge.
- The single-pass baseline is not weak on language: in LLMxMapReduce-V2's table it has the best Language score. Harness gains are in how much is said and how well it is sourced.
- Changing the base model with the harness fixed moves quality by as much as or more than adding harness stages (AutoSurvey writer swap; AI Scientist per-model scores).

### Gaps
- None of these papers measures prose style, voice, or resemblance to human academic writing; "fluency" and "language" are single LLM-judged scalars.
- SurveyBench's 21% figure is stated in the abstract and not derived in the body text I could read.
- I could not confirm from primary sources the peer-reviewed venue of AutoSurvey, SurveyForge, SurveyX, LLMxMapReduce-V2 or The AI Scientist; treat them as preprints unless checked.
- I found no systematic study of human reviewers' prose-level comments on AI-written papers; the Agents4Science report covers content-level weaknesses only.

---

## 3. Long-form generation scaffolds and length-degradation benchmarks

### Takeaway
Benchmarks agree that unscaffolded models under-produce (typically 1,000-2,000 words, rarely above about 4,000-5,500) and lose instruction adherence as output grows; plan-then-write scaffolds fix length and constraint-following cheaply, while their effect on quality is mixed: AgentWrite raised breadth and depth about 5 points and lowered coherence and clarity about 2. The pre-2023 story scaffolds (Re3, DOC) remain the only ones with solid human evaluations, and they show the outline stage carrying most of the coherence gain.

### Cited Findings
- Re3 [PR, EMNLP 2022]: plan, draft, rewrite (rerank continuations for coherence and relevance), edit (factual consistency) for stories over 2,000 words. Against same-length stories generated directly from the same base model, human evaluators judged 14% (absolute) more Re3 stories to have a coherent overarching plot and 20% more to be relevant to the premise. — [Re3](https://arxiv.org/abs/2210.06774)
- DOC [PR, ACL 2023]: adds a detailed hierarchical outliner and a controller that keeps passages aligned with the outline, "shifting creative burden from the main drafting procedure to the planning stage". Human pairwise gains over Re3: plot coherence +22.5% absolute, outline relevance +28.2%, interestingness +20.7%. — [DOC](https://arxiv.org/abs/2212.10077)
- Dramatron [PP on arXiv; DeepMind]: hierarchical prompt chaining (title, characters, beats, locations, dialogue) for scripts; evaluated qualitatively through a user study with 15 theatre and film professionals, with no numeric comparison to a single-pass baseline. — [Dramatron](https://arxiv.org/abs/2209.14958)
- RecurrentGPT [PP, "under review"]: paragraph-at-a-time generation with natural-language long- and short-term memory stored outside the prompt, aimed at arbitrary length and interactive fiction. — [RecurrentGPT](https://arxiv.org/abs/2305.13304)
- LongWriter / AgentWrite [PP in arXiv record]: the output-length cap is traced to fine-tuning data: filtering SFT outputs to 500, 1,000 and 2,000 words gave maximum generations of about 600, 900 and 1,800 words. AgentWrite is a two-step harness (plan with per-paragraph main point and word count, then write paragraphs serially with the plan and prior text) that took GPT-4o from about 2k to about 20k words. Serial writing beat a parallel variant on coherence by about 6%. — [LongWriter](https://arxiv.org/abs/2408.07055)
- AgentWrite's quality effect on GPT-4o (LongBench-Write, 120 prompts, GPT-4o as judge): overall 85.3 to 87.5, mostly from the length score; Breadth and Depth 78.1 to 83.1; Coherence and Clarity each about 2% lower. In the fine-tuning ablation, adding plan-augmented training data scored 75.0 vs 77.3 without it, which the authors read as planning not significantly helping the trained model. — [LongWriter](https://arxiv.org/abs/2408.07055)
- Suri [PR, EMNLP 2024 Findings]: 20K human-written long texts (2,048-5,024 words; fiction, books, web text including blogs) with back-translated multi-constraint instructions; fine-tuning (I-ORPO) rather than a harness. Fine-tuned Mistral-7B generates about 5,100 tokens vs about 1,100 for the base model, without rising 5-gram repetition. Human evaluation by two annotators on 30 generations: about 67-68% of constraints fully satisfied. The authors found GPT-4o, Claude-3.5-Sonnet and Gemini-1.5-Pro agree poorly with humans on constraint satisfaction in long text. Mostly narrative, not expository. — [Suri](https://arxiv.org/abs/2406.19371)
- HelloBench [PP in arXiv record]: 647 samples over five Bloom-level task types, about 30 LLMs. "Most LLMs cannot generate text that is longer than 4000 words"; unconstrained outputs are about 1,000-2,000 words; best observed was Claude-3.5-Sonnet at 5,471 words under an 8K request. Quality scores fall as the requested length rises (GPT-4o from 47.87 unconstrained to -136.51 at 16K). Length-enhanced models (LongWriter-GLM4-9B, Suri-I-ORPO) write longer at lower quality, with severe repetition in some. The benchmark's own judge reaches only Spearman 0.32 with human annotators, and still beats other automatic metrics. No scaffold experiments. — [HelloBench](https://arxiv.org/abs/2409.16191)
- LongGenBench [PR, ICLR 2025]: synthetic 16K and 32K-token tasks with checkable single, range and periodic instructions. Adherence drops noticeably past about 4,000 tokens; about 45% of long outputs show significant repetition. Example: Llama3.1-8B completion 93.5% to 77.6% and weighted score 20.6% to 14.6% from 16K to 32K; GPT-4o completion 67.2% and weighted score 12.5% at 16K. No scaffold experiments. — [LongGenBench](https://arxiv.org/abs/2409.02076)
- CogWriter [PP]: a training-free planning agent (hierarchical plan with revise steps) plus parallel generation agents with local plan adjustment and length revision, tested on LongGenBench-16K. Same-model gains over single pass: GPT-4o completion 0.63 to 0.91, average accuracy 0.47 to 0.74; Qwen-2.5-14B completion 0.29 to 0.79, accuracy 0.44 to 0.61, words 1,817 to 10,091; Llama-3.3-70B accuracy 0.48 to 0.70. Ablation on GPT-4o-mini: full 0.55; without per-unit plan adjustment 0.45 (largest drop); without global plan revision 0.50; without length review 0.54. Automated metrics only. — [CogWriter](https://arxiv.org/abs/2502.12568)
- WebWeaver's hierarchical-vs-brute-force writing ablation (section 1) is the corresponding evidence for expository reports. — [WebWeaver](https://arxiv.org/abs/2509.13312)

### Inferences
- "Scaffolds fix length" is well supported; "scaffolds fix quality" is supported for coherence and constraint adherence at long lengths (Re3, DOC, CogWriter, WebWeaver) and contradicted for local fluency (AgentWrite's coherence and clarity dip; parallel section writing costing coherence).
- Planning matters most at the level closest to the text: DOC's detailed outline, CogWriter's per-unit plan adjustment and SurveyGen-I's memory of written content all address the same failure, sections written without knowledge of each other.
- Automatic judges for long text are weak (HelloEval 0.32 with humans; Suri's finding on LLM judges), which limits how much any LLM-judged harness gain at 10k+ words can be trusted.

### Gaps
- No human-evaluated study of a plan-and-write scaffold for expository text at 10k+ words was found; the human-evaluated scaffolds are for fiction.
- HelloBench and LongGenBench include no scaffold conditions; the only scaffold result on either is CogWriter's, and it is on synthetic constraint tasks.
- I did not retrieve RecurrentGPT's or Dramatron's quantitative results beyond their abstracts.

---

## 4. Educational and textbook content

### Takeaway
This is the thinnest family: I found no peer-reviewed system that generates textbook chapters end to end with a staged writing harness and an expert evaluation of the prose. The closest work transforms existing textbooks (Learn Your Way), generates course packs of slides and scripts (Instructional Agents), or generates short explanations and worked examples; the strongest evidence is a 60-student randomised trial of a transformation system and a single-agent vs multi-agent ablation rated by instructors.

### Cited Findings
- Learn Your Way / "Towards an AI-Augmented Textbook" (Google, [PP]): a two-step pipeline, personalisation of a source textbook (grade-level re-levelling and interest-based rewriting of suitable passages) followed by content transformations (immersive text with embedded questions, timelines and mnemonics; narrated slides; teacher-student audio lesson; mind maps; quizzes). Gemini 2.5 Pro for most steps, a fine-tuned image model for illustrations. The paper describes no critique or revision loop. It rewrites existing OpenStax-type material and does not author chapters from scratch. — [Towards an AI-Augmented Textbook](https://arxiv.org/abs/2509.13348)
- Expert evaluation: ten source PDFs across seven subjects, three grade levels and three interests; three pedagogical-expert raters per component on ten criteria (accuracy, coverage, emphasis, engagement, cognitive load, active learning, metacognition, motivation, personalisation, clarity of learning intentions) with agree / partial / disagree scoring; the overall experience averaged above 0.90 on all axes, illustrations lowest. — [Towards an AI-Augmented Textbook](https://arxiv.org/abs/2509.13348)
- Randomised controlled trial: 60 students aged 15-18, Learn Your Way vs a plain digital reader on one chapter (adolescent brain development), 20-40 minutes study. Higher scores on the immediate test (p=0.03) and on the three-day retention test (p=0.03; 58 of 60 completed). The authors state the study did not isolate which components drove the gain. — [Towards an AI-Augmented Textbook](https://arxiv.org/abs/2509.13348)
- Instructional Agents [PR per arXiv comment, "ECAL'26 main conference"]: six role agents (teaching faculty, instructional designer, teaching assistant, course coordinator, program chair, test student) follow the Analyze, Design, Develop phases of ADDIE to produce learning objectives, syllabus, LaTeX slides, slide scripts and assessments. Five CS courses, five expert raters per course (faculty and senior PhD students), adapted Quality Matters rubric, 1-5. — [Instructional Agents](https://arxiv.org/abs/2508.19611)
- Its ablation: single-agent GPT-4o-mini baseline 2.33; full multi-agent autonomous mode 3.01; human-in-the-loop co-pilot mode 3.74. Model choice (gpt-4o, gpt-4o-mini, o1-preview) made no significant difference (Friedman p=0.789). LLM reviewers' scores clustered at 2.9-3.1 and could not separate conditions, so the authors relied on human ratings. Cost about $0.22-0.36 per course. — [Instructional Agents](https://arxiv.org/abs/2508.19611)
- Slide2Text [PP]: converts PowerPoint decks into "customized textbooks" via OCR, structuring and LLM-generated explanations, exercises and references; the abstract reports no quantitative evaluation. — [Slide2Text](https://arxiv.org/abs/2503.17710)
- FACET [PP]: learner agents, a teacher agent and an evaluator agent generate personalised grade-8 maths worksheets; evaluated by automated agent assessment plus exploratory in-service teacher feedback. — [FACET](https://arxiv.org/abs/2508.11401)
- Worked examples: a human-AI authoring system drafts line-by-line explanations of Java examples for instructors to edit, with a study assessing explanation quality (details not retrieved). — [Human-AI Co-Creation of Worked Examples](https://arxiv.org/abs/2402.16235)
- Science communication (adjacent genre): LLM-CLBR [PP], a journalist LLM, a smaller "reader" LLM that takes notes on what it could not follow, and an editor LLM that turns the notes into revision suggestions, iterated. Readability index average (lower is easier): 10.69 vs GPT-4 direct 11.98 and the same base model direct 12.73; ablation: without reader notes 11.26, without editor suggestions 11.32, without collaboration 11.59. Human evaluation by four master's-level raters on 20 items: readability 3.95 vs 3.80 for GPT-4 direct (in field), but information conveyance 3.60 vs 3.75 and authenticity 3.70 vs 3.80. A 7B model in a harness matched GPT-4 on readability and lost on content. — [LLM-Collaboration on Automatic Science Journalism](https://arxiv.org/abs/2407.09756)

### Inferences
- For a textbook-exposition builder there is essentially no direct prior art with a staged writing harness evaluated on explanation quality by teachers; the nearest evidence comes from adjacent genres.
- Two adjacent results are relevant to design: a simulated-reader critique loop improves measured readability (LLM-CLBR), and role decomposition improves instructor-rated course materials over a single agent while a human in the loop adds as much again (Instructional Agents).
- The educational evaluations that exist measure learning outcomes or rubric compliance, not prose. Learn Your Way's gain cannot be separated from quizzes and multimodal formats.

### Gaps
- No LearnLM-related publication on a text-authoring pipeline was retrieved; the LearnLM work I am aware of concerns tutoring dialogue, and I did not verify it in this session.
- No papers from the intelligent-textbooks workshop series on LLM chapter generation surfaced in three targeted searches; this may be a search limitation.
- I found no evaluation of Bloom-level or pedagogical-move planning as a stage in a writing pipeline for explanations.
- WorkedGen (ACM ACE 2024) and the large-course student-rated comparison of LLM vs student code explanations surfaced only as search snippets; not verified.

---

## 5. Technical and code documentation writers

### Takeaway
Documentation agents show the clearest same-model harness gains outside deep research, and the stage that matters is context acquisition ordered by the dependency graph: DocAgent with GPT-4o-mini beats single-pass chat with the same model on completeness, helpfulness and factual grounding, and randomising the processing order removes a large part of the helpfulness gain. Human evaluation is sparse and small.

### Cited Findings
- RepoAgent [PP in arXiv record; arXiv 2402.16667]: (1) global structure analysis by AST plus Jedi caller/callee references into a DAG; (2) bottom-up documentation generation in topological order with project tree, code and references in the prompt; (3) incremental update via a Git pre-commit hook. Models gpt-3.5-turbo, gpt-4-0125, Llama-2. — [RepoAgent](https://arxiv.org/abs/2402.16667)
- RepoAgent human evaluation: three evaluators, blind pairwise against existing human-written documentation, 150 samples per repository; model output preferred 105 to 45 on Transformers (0.70) and 137 to 13 on LlamaIndex (0.91). Parameter-identification accuracy 0.95-1.00 for gpt-4-0125. No formal ablation and no quantitative comparison against a single-pass summariser. — [RepoAgent](https://arxiv.org/abs/2402.16667)
- DocAgent (Meta, [PR, ACL 2025 demo]): Navigator (dependency graph, topological order, "dependencies first"), Reader (decides what context is missing), Searcher (internal code analysis and external retrieval), Writer, Verifier (sends drafts back to Writer or Reader), Orchestrator. — [DocAgent](https://arxiv.org/abs/2504.08725)
- DocAgent vs same-model single-pass chat (GPT-4o-mini), 366 components from 9 repositories: completeness 0.934 vs 0.815; helpfulness (GPT-4o judge, 1-5) 3.88 vs 2.95; existence ratio of mentioned entities 95.74% vs 61.10% as reported. Ablation with random instead of topological order: helpfulness 3.88 to 3.44 (summary sub-score 4.32 to 3.62); truthfulness 94.64% to 86.75%. LLM judge only, with no human validation; the paper's truthfulness tables contain counts that do not match the reported ratios, and the text gives 3.69 where tables give 3.88. — [DocAgent](https://arxiv.org/abs/2504.08725)
- CodeWiki [PR, ACL 2026]: repository-level documentation by dependency-graph analysis, a feature-oriented module tree, recursive agents that delegate sub-modules (depth up to 3), and bottom-up assembly of parent overviews with diagrams. Claude Sonnet 4 writer. CodeWikiBench: 7 repositories in 7 languages, hierarchical rubrics derived from official docs, three LLM judges. Scores 68.79 vs DeepWiki 64.06 and open-source whole-repository baselines 47.13 and 50.05; wins 5 of 7 repositories, loses on C and C++. No ablation and no single-pass version of itself; human pilot of 3 participants preferred CodeWiki in 7 of 9 judgments. — [CodeWiki](https://arxiv.org/abs/2510.24428)

### Inferences
- In documentation the harness's contribution is factual grounding and completeness (the model cannot document what it has not been shown), and ordering work so that dependencies are documented first is a cheap, measurable lever.
- Readers preferring RepoAgent output to existing human docs says more about the low baseline of real-world docstrings than about prose quality; DocAgent reports that only 27.28% of documentable nodes in 164 repositories had any documentation.

### Gaps
- No README-specific generation benchmark with quality evaluation was found.
- No documentation paper evaluates explanatory quality for learners (tutorial-style docs) or prose style.
- Human evaluations are small (3 raters in RepoAgent and CodeWiki) and absent in DocAgent.

---

## 6. Cross-family: which stage matters, what kind of gain, and is prose style ever measured?

### Takeaway
Ablations across families point the same way: the evidence-gathering and planning stages (retrieval, question asking, outline) account for most of the measured gain, and the gain is in coverage, organisation, citation accuracy and length control; critique and revision passes contribute least to content scores, with exceptions where revision is evaluated at each component (TTD-DR) or driven by a simulated reader (LLM-CLBR). No system in this census measures how "AI-sounding" its prose is or compares its style to human writing; where a language or style scalar exists it is flat or slightly worse under the harness.

### Cited Findings

Stage ablations, most to least consequential within each paper:
- STORM: outline stage (removal returns article metrics to RAG level) > simulated conversation > perspective personas. — [STORM](https://arxiv.org/abs/2402.14207)
- Co-STORM: moderator steering toward unused sources > multiple expert personas. — [Co-STORM](https://arxiv.org/abs/2408.15232)
- AutoSurvey: retrieval (citation recall 83.48 to 60.11) >> reflection/refinement (content 4.57 to 4.56). — [AutoSurvey](https://arxiv.org/abs/2406.10252)
- SurveyX: source pre-digestion and outline optimisation for content (4.59 to 4.32 each); RAG rewriting for citation F1 (81.52 to 55.16) but not content (4.59 to 4.55). — [SurveyX](https://arxiv.org/abs/2502.14776)
- SurveyForge: human-outline exemplars for outline quality (81.78 to 86.67); retrieval memory for reference coverage (0.234 to 0.397). — [SurveyForge](https://arxiv.org/abs/2503.04629)
- TTD-DR: agent workflow over model with search +4 to +5 win-rate points; component-wise self-evolution (sample, judge, critique, revise, merge) +21 to +35 points; draft-guided retrieval +8 to +15 points. Here critique-and-revise is the largest contributor, applied to plans, queries and answers as well as the report. — [TTD-DR](https://arxiv.org/abs/2507.16075)
- WebWeaver: section-wise writing with per-section evidence over single-pass writing (insight +7.3, readability +6.0 on RACE); outline rounds (comprehensiveness +2.0). — [WebWeaver](https://arxiv.org/abs/2509.13312)
- CogWriter: per-unit plan adjustment > global plan revision > length review. — [CogWriter](https://arxiv.org/abs/2502.12568)
- DocAgent: dependency-ordered processing (helpfulness 3.44 to 3.88). — [DocAgent](https://arxiv.org/abs/2504.08725)
- LLM-CLBR: reader notes and editor suggestions each worth about 0.6 readability-index points. — [LLM-CLBR](https://arxiv.org/abs/2407.09756)
- AI Scientist reviewer: reflection and one-shot example about +2% balanced accuracy each; ensembling no accuracy gain. — [The AI Scientist](https://arxiv.org/abs/2408.06292)

Prose and style evidence:
- LLMxMapReduce-V2's single-pass baseline has the highest Language score (96.50 vs 94.34 for the full system). — [LLMxMapReduce-V2](https://arxiv.org/abs/2504.05732)
- AgentWrite lowers coherence and clarity about 2% while raising breadth and depth about 5%. — [LongWriter](https://arxiv.org/abs/2408.07055)
- DEER: Format & Style is best for reasoning-only models and lower for deep-research systems; presentation is called "relatively mature" while reasoning completeness and intent alignment "remain limited". — [DEER](https://arxiv.org/abs/2512.17776)
- SurveyBench: fluency about 4.2-4.3 of 5 for all systems; the gap to human surveys is depth and synthesis. — [SurveyBench](https://arxiv.org/abs/2510.03120)
- ResearchRubrics: communication-quality criteria fail under 20% of the time; implicit reasoning and synthesis make up 45-50% of failures. — [ResearchRubrics](https://arxiv.org/abs/2511.07685)
- STORM: 7 of 10 Wikipedia editors found the tone "emotional" or "unneutral", inherited from web sources; this is the only expert comment on register in the encyclopedic family. — [STORM](https://arxiv.org/abs/2402.14207)
- Adjacent, not about harness output: a linguistic-profiling study of human vs machine text across 8 domains and 11 LLMs finds human text more variable in style features and newer models converging toward similar outputs ("homogenization"). — [Linguistic and Embedding-Based Profiling](https://arxiv.org/abs/2507.13614)

Judge reliability, which bounds all of the above:
- TTD-DR judge 60.8% agreement with humans (human-human 69.0%). — [TTD-DR](https://arxiv.org/abs/2507.16075)
- HelloEval Spearman 0.32 with humans. — [HelloBench](https://arxiv.org/abs/2409.16191)
- AutoSurvey judge Spearman 0.54 with three PhD students. — [AutoSurvey](https://arxiv.org/abs/2406.10252)
- Instructional Agents: LLM reviewers could not separate conditions that human instructors separated by 1.4 points. — [Instructional Agents](https://arxiv.org/abs/2508.19611)
- Suri: frontier LLM judges agree poorly with humans on long-text constraint satisfaction. — [Suri](https://arxiv.org/abs/2406.19371)

### Inferences
- How much of machine-writing quality the literature attributes to the harness: on what the systems measure (coverage, citation accuracy, structure, length), a large share, often the difference between unusable and usable (citation recall +20 points, reference recall 26% to 96%, win rate 35% to 69%). On prose quality and style, effectively none: no paper claims a prose gain supported by human judgment, and the available scalars are flat or negative.
- Three stated reasons the question of prose is not addressed: evaluation is dominated by LLM judges with rubrics about content; baselines are other harnesses rather than the bare model; and the genres targeted (surveys, reports, wiki articles) reward completeness and attribution.
- The harness share is model-dependent and appears to be shrinking at the frontier (DEER; Instructional Agents' null model effect is the counter-example at the low-cost end, where the harness dominated).
- Parallel section drafting recurs as a source of incoherence and repetition (AgentWrite's parallel variant, SurveyGen-I's motivation, AutoSurvey2's stated limitation of stylistic inconsistency from parallel generation, per its [abstract-level summary](https://arxiv.org/abs/2510.26012)); serial writing with memory of prior text, or a later de-duplication pass, is the standard remedy.
- A system that measured stylistic fidelity of harness output against a target human author or register, with human raters, would be filling a gap rather than repeating prior work.

### Gaps
- No ablation anywhere isolates a "style" or "voice" stage, because no system has one.
- No study compares the same harness's output to human-written text with detector scores, stylometric distance or blind human "which is AI" judgments. Two targeted searches returned only general LLM-vs-human stylometry.
- Few papers report the bare model, single-pass, as a baseline with human raters; Re3 (fiction) and LLM-CLBR (science news) are the exceptions found.

---

## 7. Rough census: counts by year, venues, trend, and surveys of the area

### Takeaway
The systems examined here cluster in 2024-2025, with a sharp shift in 2025-2026 from genre-specific pipelines (wiki articles, surveys) to general "deep research" agents and to benchmarks; arXiv title counts for "deep research" go from 0 in 2024 to 67 in 2025 and 171 in 2026 to date. Venues are mainly ACL-family conferences and ICLR, with a large preprint-only share, and most post-2024 papers are evaluated only or mainly by LLM judges.

### Cited Findings
- arXiv title-phrase counts by submission year (arXiv API, queried 2026-11-15; 2026 is a partial year; titles only, so these undercount and include some off-topic matches): "deep research" 2022: 0, 2023: 0, 2024: 0, 2025: 67, 2026: 171. "survey generation" 0, 2, 0, 7, 6. "long-form generation" or "long-form text generation" 2, 2, 20, 18, 18. "AI Scientist" 0, 0, 3, 19, 54. "documentation generation" 2, 4, 4, 9, 15. — [arXiv API, example query](https://export.arxiv.org/api/query?search_query=%28ti:%22deep+research%22%29+AND+submittedDate:%5B202501010000+TO+202512312359%5D&max_results=1)
- Systems and benchmarks covered in these notes, by first arXiv year. 2022: Re3, Dramatron, DOC. 2023: RecurrentGPT. 2024: STORM, RepoAgent, AutoSurvey, Suri, LLM-CLBR, LongWriter/AgentWrite, The AI Scientist, Co-STORM, PaperQA2/WikiCrow, LongGenBench, HelloBench, CycleResearcher, worked-example co-authoring. 2025: OmniThink, SurveyX, CogWriter, SurveyForge, Slide2Text, LLMxMapReduce-V2, AI Scientist-v2, DocAgent, DeepResearch Bench, TTD-DR, FACET, SurveyGen-I, Instructional Agents, Learn Your Way, WebWeaver, Agentic AutoSurvey, SurveyBench, CodeWiki, AutoSurvey2, ResearchRubrics, Agents4Science report, DEER. (Dates from the [arXiv API](https://export.arxiv.org/api/query?id_list=2402.14207,2406.10252,2408.07055,2501.09751,2503.04629,2507.16075,2509.13312,2510.03120,2511.07685,2512.17776).)
- 2026 items that surfaced but were not read in full: ScaffoldAgent, "utility-guided dynamic outline optimization" for deep research, which uses WebWeaver as a baseline ([arXiv 2606.20122](https://arxiv.org/pdf/2606.20122)); LessonBench-V1, a benchmark for AI lesson-generation agents ([arXiv 2607.13041](https://arxiv.org/html/2607.13041v1)); a deep-research agent with progressive confidence estimation ([arXiv 2604.05952](https://arxiv.org/pdf/2604.05952)).
- Venues confirmed: NAACL 2024 (STORM), EMNLP 2022 / 2024 / 2025 (Re3, Co-STORM, Suri Findings, OmniThink), ACL 2023 / 2025 / 2026 (DOC, DocAgent demo, CodeWiki), ICLR 2025 / 2026 (LongGenBench, CycleResearcher, WebWeaver), TKDD (AutoSurvey2). — [arXiv API record](https://export.arxiv.org/api/query?id_list=2402.14207,2408.15232,2501.09751,2409.02076,2411.00816,2406.19371,2504.08725,2510.24428,2210.06774,2212.10077,2510.26012); [ICLR 2026 poster page](https://iclr.cc/virtual/2026/poster/10009906)
- Surveys of the area: "Deep Research Agents: A Systematic Examination and Roadmap" (June 2025) classifies static vs dynamic workflows and single- vs multi-agent designs and reviews benchmarks. — [Huang et al.](https://arxiv.org/abs/2506.18096)
- "Deep Research: A Systematic Survey" (late 2025) organises the field into query planning, information acquisition, memory management and answer generation (the last covering evidence synthesis, narrative structuring and presentation), and has a section on the bias and efficiency of LLM-as-judge evaluation. — [Shi et al.](https://arxiv.org/abs/2512.02038)
- Broader surveys that include a writing stage: "Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents" ([arXiv 2503.24047](https://arxiv.org/abs/2503.24047)) and an AI4Research survey with a section on semi-automatic vs fully automatic academic writing ([arXiv 2507.01903](https://arxiv.org/pdf/2507.01903v2.pdf)); both seen at search-snippet level only.
- Evaluation practice in this census: human evaluation of output quality with domain experts appears in STORM (10 editors), WikiCrow (4 experts, 375 statements), SurveyForge (20 PhDs), SurveyX (6 PhD students), CycleResearcher (3 experts), Instructional Agents (5 raters per course), Learn Your Way (expert raters plus 60-student RCT), Re3 and DOC (crowd/human pairwise). LLM judge only or nearly only: WebWeaver, DocAgent, CogWriter, LLMxMapReduce-V2 main table, SurveyBench, AutoSurvey main table, HelloBench, LongWriter. — sources as cited per system above.

### Inferences
- Trend, three phases: 2022-2023 hierarchical story scaffolds with human evaluation; 2024 genre-specific expository pipelines (wiki article, survey, paper) with LLM-judge rubrics plus a small human study; 2025-2026 general deep-research agents, test-time-scaling framings of revision, and benchmark papers that often outnumber new systems.
- The methodological centre moved from "does a pipeline beat direct prompting" (2022-2024) to "which product or agent ranks higher on an LLM-judged benchmark" (2025-2026), which makes harness-vs-model attribution harder to read from recent work.
- Educational and textbook generation is under-represented relative to surveys and reports: one transformation system with an RCT, one course-material system with expert ratings, and otherwise small or unevaluated tools.

### Gaps
- The arXiv counts are a title-keyword proxy and not a census; I found no survey paper that tabulates writing-harness systems by year, and no survey dedicated to LLM writing agents or automated scientific writing as its sole subject.
- Venues not confirmed in this session, which from memory are likely peer-reviewed but should be checked before citing as such: AutoSurvey (NeurIPS 2024), SurveyForge (ACL 2025), LongWriter and HelloBench (ICLR 2025), RepoAgent (EMNLP 2024 demo), The AI Scientist (a 2026 journal version was mentioned in a secondary news item only).
- Several fetched pages were read only for their first 100,000 characters (STORM, Co-STORM, OmniThink, PaperQA2, AI Scientist, HelloBench, DEER appendices), so appendix-only results may be missing.
- Product deep-research systems (OpenAI, Gemini, Perplexity) disclose no pipeline details; their stage contributions cannot be assessed from published sources.
