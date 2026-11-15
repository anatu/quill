# Harness-level optimisation versus model-level training for writing quality (state of evidence, November 2026)

Notes on reading these findings:
- "Peer-reviewed" is marked where a venue was confirmed on the source page. Everything else is a preprint, vendor post or blog and is labelled.
- Several numbers were read from arXiv abstract pages or from the paper HTML through an automated reader; where a number came only from a third-party summary it is flagged "secondary".
- Roughly 40 searches and page reads were made. This is a targeted sweep, not a systematic review. Counts in the census section are estimates.

## 1. Head-to-head evidence: fine-tuning versus prompting, exemplar retrieval and pipeline design for writing

### Takeaway
For author-level style judged by blind human readers, fine-tuning wins clearly and prompting with exemplars loses, in every direct comparison found (literary authors, personal email). For personalisation benchmarks scored on content overlap (LaMP), retrieval wins by an order of magnitude over per-user adapters, and the two are additive. The split is consistent: fine-tuning buys style and "not sounding like AI"; retrieval and pipelines buy content, coverage and organisation.

### Cited Findings

Fine-tuning beats prompted frontier models on author style
- Chakrabarty, Ginsburg and Dhillon (preprint, "under review", v4 March 2026): MFA-trained writers and three frontier models (ChatGPT, Claude, Gemini) wrote excerpts of up to 450 words emulating 50 award-winning authors; 28 MFA-trained readers and 516 general readers judged blind pairs. With in-context prompting, expert readers disfavoured AI (odds ratio 0.16 for stylistic fidelity, 0.13 for quality); general readers were about neutral on fidelity (OR 1.06) and favoured AI on quality (OR 1.82). After fine-tuning ChatGPT on each author's complete works the result reversed: experts OR 8.16 for fidelity and 1.87 for quality; general readers OR 16.65 and 5.42. — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939)
- Same study: AI detectors flagged 97% of in-context-prompted outputs and 3% of fine-tuned outputs; median fine-tuning plus inference cost was $81 per author. Only GPT-4o was fine-tuned, so the comparison is fine-tuned GPT-4o against prompted frontier models and human experts, not fine-tuned small model against prompted large model. — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939)
- Companion paper by Chakrabarty and Dhillon (CHI 2026 per search summary; peer-reviewed): expert writers preferred human excerpts under in-context prompting; the preference reversed to 62% for AI after fine-tuning on each author's complete works. Figure read from a search summary, not the paper body. — [arXiv 2601.18353](https://arxiv.org/pdf/2601.18353)
- Panza (preprint, v4 February 2025; Mistral-7B and Llama-3-8B class models, fully local): for personal email, all fine-tuning regimes beat pretrained-plus-RAG "by a large margin" on BLEU/ROUGE/MAUVE (exact values in figures only). Against GPT-4o given the user's full email history in context: BLEU 0.24 (GPT-4o) versus 0.31 (Panza) and MAUVE 0.009 versus 0.96 for one user; BLEU 0.19 versus 0.22 and MAUVE 0.004 versus 0.93 for another. — [arXiv 2407.10994v4](https://arxiv.org/html/2407.10994v4)
- Panza human study: share of emails judged "suspicious" was 24% for genuine emails, 64% for un-tuned Llama-3-8B, 28% and 32% for the two Panza variants. Usefulness on a 1-3 scale (six subjects): Llama+RAG 2.10, full fine-tune+RAG 2.56, RoSA+RAG 2.65. — [arXiv 2407.10994v4](https://arxiv.org/html/2407.10994v4)
- Panza data efficiency: 25 training emails reach about 90% of full-data BLEU; 75-100 emails essentially match it; MAUVE (the style-distribution metric) saturates more slowly. — [arXiv 2407.10994v4](https://arxiv.org/html/2407.10994v4)
- Panza on adding RAG to a fine-tuned model: retrieval at inference lowered average BLEU for adapter-tuned models and may slightly raise MAUVE; the authors hypothesise the model reuses retrieved context "too aggressively" (not verified by them). — [arXiv 2407.10994v4](https://arxiv.org/html/2407.10994v4)
- A personal-chat impersonation study reports fine-tuning works better than prompting but "sometimes develops flow problems, e.g. jumping between topics" (search-summary level only). — [arXiv 2510.13898](https://www.arxiv.org/pdf/2510.13898)

Retrieval beats per-user adapters on LaMP-style benchmarks
- Salemi and Zamani (preprint v2 June 2025; seven LaMP datasets): retrieval-augmented personalisation improved over a non-personalised LLM by 14.92% on average; per-user PEFT by 1.07%; combining both gave 15.98%. PEFT effectiveness correlated positively with the amount of user data; RAG helped most for cold-start users. — [arXiv 2409.09510](https://arxiv.org/abs/2409.09510)
- Counter-claim: the One-PEFT-Per-User (OPPU) paper reports per-user adapters beating retrieval and profile prompting across all seven LaMP tasks, particularly under user behaviour shift where retrieved history is less relevant (search-summary level). — [arXiv 2402.04401](https://arxiv.org/pdf/2402.04401.pdf)
- LongLaMP (preprint, v3 October 2024; personalised email completion, abstract generation, review writing, topic writing): retrieval of user history gave an average improvement of about 30.21% in ROUGE-1 and 47.5% in ROUGE-L across tasks, in both zero-shot and fine-tuned settings (figures from search summary of the paper's conclusion; per-setting split not retrieved). — [arXiv 2407.11016](https://arxiv.org/abs/2407.11016v3)

Fine-tuning that does not recover style
- InMyStyle (single-author preprint, v2 September 2026): LoRA rank-8 adapters on Qwen2.5 0.5B-7B trained to rewrite AI-edited text into one user's scientific style. Composite score plateaued at 0.689-0.695 across all model sizes; authorship probability stayed at the classifier's decision boundary (0.51-0.53); stylometric improvement was near zero. Five LLM judges rated outputs more than 20% lower on "AI-ness" than inputs. The author concludes the gain is "content-preserving naturalization" and not recovery of personal style. — [arXiv 2607.29238](https://arxiv.org/abs/2607.29238)

Curated training data can outrank model size on general writing
- WritingBench (preprint; NeurIPS-template): Qwen-2.5-7B and Llama-3.1-8B fine-tuned on 12K examples filtered by the benchmark's critic model scored 7.44 and 7.39 on its 1-10 scale, above GPT-4o at 6.81 and above the 70B-class base models; the top model (Claude-3.7-thinking) scored 7.91. The scorer is an LLM critic, and the training data were selected by the same critic. — [arXiv 2503.05244v4](https://arxiv.org/html/2503.05244v4)

### Inferences
- The two bodies of evidence measure different things. LaMP/LongLaMP score ROUGE against a user's real output, which rewards getting the user's content and topics right; retrieval supplies exactly that. Blind-read and MAUVE/authorship measures reward distributional style; fine-tuning supplies that. Neither literature shows one approach winning both.
- The strongest fine-tuning results fine-tune a strong base (GPT-4o on complete works) or score on a narrow genre (email). The one small-model style-rewriter study with authorship metrics (InMyStyle) found near-zero stylometric movement. So "fine-tuning wins on style" is established for large bases and for short formulaic genres, and is not established for a small local model on essay-length prose.
- No study found holds a strong base model fixed and compares (a) a fine-tuned small model, (b) a prompted frontier model inside a multi-pass writing pipeline, and (c) both combined, with blind human reads. That is the comparison the requester's question turns on.

### Gaps
- No head-to-head of fine-tuning versus a multi-stage pipeline (plan, draft, critique, revise) for author style. The Chakrabarty prompting condition is single-shot in-context prompting, not an optimised harness.
- No study found comparing approaches on coherence or factuality for style-conditioned long-form writing; factuality comparisons exist only in grounded article generation (section 2).
- Exact Panza BLEU/MAUVE values for pretrained+RAG versus fine-tuned are in figures and were not extracted.
- OPPU and LongLaMP numbers were read at summary level only.

## 2. Prompt and pipeline optimisation frameworks applied to writing

### Takeaway
Hand-designed pipelines for long-form writing have peer-reviewed human-judged gains of roughly 10 to 28 percentage points on organisation, coherence and coverage. Automatic prompt optimisers (DSPy/MIPRO, GEPA, TextGrad) have almost no published results on writing quality; the only writing numbers found are a paywalled vendor claim and a hobbyist blog. No work was found that optimises a multi-stage writing pipeline end to end against human preference or an expert rubric.

### Cited Findings

Hand-designed writing pipelines with human evaluation (peer-reviewed)
- STORM (NAACL 2024): a pipeline of perspective discovery, simulated question-asking, outline building and writing. Articles were judged more organised (25% absolute increase) and broader in coverage (by 10%) than an outline-driven retrieval-augmented baseline; experienced Wikipedia editors gave feedback and flagged "source bias transfer" and "over-association of unrelated facts". — [arXiv 2402.14207](https://arxiv.org/abs/2402.14207)
- STORM's prompts were written zero-shot inside DSPy; no DSPy optimiser was applied (search summary of the paper). — [arXiv 2402.14207](https://arxiv.org/pdf/2402.14207)
- DOC, detailed outline control for long stories (ACL 2023): human evaluation gains over the Re3 pipeline baseline of 22.5% absolute in plot coherence, 28.2% in outline relevance and 20.7% in interestingness. — [arXiv 2212.10077](https://arxiv.org/abs/2212.10077)
- Agents' Room (ICLR 2025): narrative writing decomposed into specialised planning and writing agents; human participants consistently preferred its stories over end-to-end baselines. A secondary review notes the stories were about twice as long as the baselines', which may confound preference. — [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0fbc8a83d93dd8021a4dd8d2d34138eb-Abstract-Conference.html); length caveat from [secondary review](https://www.themoonlight.io/review/agents-room-narrative-generation-through-multi-step-collaboration)
- OmniThink (preprint; later versions): iterative expand-and-reflect retrieval before outlining. A secondary review reports human evaluation above Co-STORM including an 11% improvement in breadth, and 120.63 unique URLs retrieved on average versus 10.49 for Co-STORM. Secondary source; not verified against the paper. — [arXiv 2501.09751](https://arxiv.org/html/2501.09751v5); figures from [secondary review](https://liner.com/review/omnithink-expanding-knowledge-boundaries-in-machine-writing-through-thinking)

Automatic prompt optimisers
- GEPA (ICLR 2026 oral): beats GRPO reinforcement learning by 6% on average and up to 20% with up to 35x fewer rollouts, and beats MIPROv2 by over 10% (+12% on AIME-2025), across six tasks. The abstract names no writing or long-form task. — [arXiv 2507.19457](https://arxiv.org/abs/2507.19457)
- Vendor claim (Every, December 2025, paywalled): prompts behind the Spiral writing assistant "got a 44 percent quality improvement through GEPA optimization". The readable portion gives no metric, judge or dataset. — [Every](https://every.to/also-true-for-humans/this-prompt-optimizer-learns-from-its-mistakes-like-dna)
- Blog (single author): GEPA improved a small model's fiction and length adherence; the author notes the result depends heavily on the quality of the LLM judge. — [Substack](https://meandnotes.substack.com/p/i-taught-a-small-llm-to-write-fiction?open=false)
- A targeted search for end-to-end optimisation of a multi-stage writing pipeline against human preference or a rubric returned general framework descriptions only; nothing specific to essay or article generation. The nearest items are preference-based prompt optimisers not specific to writing: PrefPO, a pairwise-preference prompt optimiser (title-level only), and Prompt Optimization with Human Feedback (2024). — [arXiv 2603.19311](https://arxiv.org/pdf/2603.19311); [arXiv 2405.17346](https://arxiv.org/pdf/2405.17346)
- A blog comparison states TextGrad has had no commits since July 2025 (blog-level, unverified). — [futureagi blog](https://futureagi.com/blog/top-10-prompt-optimization-tools-2025/)

Model-level preference optimisation for writing is more active than prompt-level
- A January 2026 preprint trains a generative reward model on human preference data for story RL and reports a 72.4% win rate over an SFT baseline (search-summary level). — [arXiv 2601.07149](https://arxiv.org/html/2601.07149)
- POLARIS (EMNLP 2026 main, peer-reviewed): GRPO on Qwen3.5-9B with a frontier LLM judge scoring a story rubric plus a human-written story injected into each group; about 1.4K prompt-story pairs. In blinded human evaluation the result was preferred over the base 9B model and on par with Qwen3.5-27B, and held quality at three times the training length. — [arXiv 2606.04095](https://arxiv.org/abs/2606.04095)
- Related preprints on creative-writing reward models and preference optimisation exist (RLMR, Creative Preference Optimization); titles only. — [arXiv 2508.18642](https://arxiv.org/html/2508.18642); [arXiv 2505.14442](https://arxiv.org/pdf/2505.14442)

### Inferences
- Where a rubric or preference signal for writing exists, the field has mostly spent it on weights (GRPO, DPO, reward models), not on prompts or pipeline structure. The same signal could drive GEPA-style optimisation of a pipeline, and that experiment appears unpublished.
- Pipeline gains are documented on structure-level properties (organisation, coverage, plot coherence, outline relevance). None of the pipeline papers found reports a gain on sentence-level prose quality or voice.
- The pipeline papers used 2022-2024 base models. Whether a 25-point organisation gain survives on a 2026 frontier model is untested in what was found; the Anthropic harness post (section 6) reports components becoming unnecessary as models improved.

### Gaps
- No peer-reviewed result found for DSPy/MIPRO, GEPA, TextGrad, OPRO or PromptBreeder on a writing-quality or long-form benchmark with human evaluation.
- OPRO, PromptBreeder and the Berkeley "compound AI systems" framing were not retrieved in this pass; no writing-specific results from them surfaced in any search.
- Re3 (the 2022 predecessor to DOC) was not fetched; its own gains over a non-pipeline baseline are not recorded here.
- The Every "44 percent" claim cannot be assessed.

## 3. The harness idea: fixed-model scaffold effects, and whether it has reached writing

### Takeaway
For coding and general agent benchmarks there is now direct evidence, mostly 2026 preprints, that changing only the harness moves scores by 7 to 34 points, often more than the gap between adjacent models. No study was found that runs this design for writing: nobody has held the model fixed and varied a writing harness with human-judged prose quality as the outcome.

### Cited Findings
- Position paper with a controlled grid (preprint, May 2026): on a SWE-bench Verified subset, changing harness moved pass@1 by 8.5-13.0 points (GLM-5.1 52.5% to 65.5%; GPT-5.4 55.0% to 63.5%; Kimi K2.6 52.0% to 60.5%) while changing model moved it 2.5-5.0 points; aggregate harness-to-model variance ratio 7.80x; six ranking reversals in nine comparisons. — [arXiv 2605.23950](https://arxiv.org/html/2605.23950)
- Examples that paper collects from other sources: Claude Opus 4.5 on SWE-bench Pro 45.9% under the SEAL scaffold versus 55.4% under Claude Code (9.5 points, about twice the 4.9-point model range under SEAL); Claude Sonnet 4.5 68% versus 34% and GPT-5 Medium 46% versus 12% across two scaffolds on SWE-bench Verified Mini (HAL); Grok 4 58.6% versus 72-75%; Terminal-Bench 2 with GPT-5.4 69.7% to 77.0% via automated harness evolution; scaffold-only variation up to 11 points for GPT-5 and 15 for Kimi K2 Thinking (Epoch AI). The authors say harness shifts routinely exceed the 2-4 point gains reported as model advances. — [arXiv 2605.23950](https://arxiv.org/html/2605.23950)
- That paper mentions one non-coding domain (APEX-Agents: banking, consulting, law tasks) and no writing tasks. — [arXiv 2605.23950](https://arxiv.org/html/2605.23950)
- Pre-registered GAIA study (preprint, June 2026; ReAct, planner-actor-rater, planner-then-executor; Claude Opus 4.7, Sonnet 4.6, Haiku 4.5, Gemini 3.1 Pro Preview, GPT-5.5): scaffold alone shifted accuracy by up to 28 points (Opus, Level 2). The hypothesis that stronger models are less scaffold-sensitive was rejected in direction: Opus gained the most. The author concludes the scaffold gap "is not guaranteed to shrink as models improve". — [arXiv 2606.08529](https://arxiv.org/abs/2606.08529)
- Audit of benchmark papers (preprint): two reports of the same model on SWE-bench Verified differed by about ten points, attributed mainly to under-specified harnesses; sampling noise alone is about 1-3 points (search-summary level). — [arXiv 2605.21404](https://arxiv.org/html/2605.21404)
- Vendor analysis (Braintrust, June 2026): claims harness choice explains about 7x more success variance than model choice, with one configuration going from 12% to 92%. Not independently verified. — [Braintrust](https://www.braintrust.dev/evals/hf-agent-traces)
- Anthropic engineering post (vendor, March 2026): a planner-generator-evaluator harness for app building. Solo Opus 4.5 run: 20 minutes, $9, core feature broken. Full harness: 6 hours, $200, playable result. Updated harness on Opus 4.6: 3 h 50 min, $124.70. One example each, no repeated trials. Writing is not discussed. — [Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Same post on harness decay: context resets were needed for Sonnet 4.5 and dropped for Opus 4.5; the sprint decomposition was removed with Opus 4.6; the planner stayed because the generator under-scoped without it; the evaluator became "unnecessary overhead" for tasks the model already does reliably. — [Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Nearest writing-adjacent agent benchmark found: WeaveBench (preprint, June 2026) includes a document-repagination task; best pass rate 41.2%. It tests document manipulation, not prose quality (search-summary level). — [arXiv 2606.09426](https://arxiv.org/pdf/2606.09426)
- A targeted search for a writing agent with a fixed-model scaffold ablation and revision passes returned no matching paper. — [search result set, e.g. arXiv 2606.08529](https://arxiv.org/pdf/2606.08529)

### Inferences
- In coding and GAIA-type tasks, harness effects (roughly 8-28 points in controlled studies) are comparable to or larger than one model-generation step (2-5 points between adjacent models in the same grid). This is the best available prior for writing, but it is a transfer assumption: those tasks have verifiable success criteria, which is what lets a harness add checking and recovery. Prose quality has no such oracle.
- The two harness accounts disagree on trajectory. The GAIA study finds the strongest model gained most from scaffolding; the Anthropic post finds components dropping away with each model release. Both can be true if harness value concentrates at the edge of what the model can do alone.
- The pipeline literature in section 2 (STORM, DOC, Agents' Room) is the writing equivalent of fixed-model scaffold studies, though it does not use the word harness: each holds the model fixed and varies the structure around it.

### Gaps
- No fixed-model, varied-harness study for writing quality was found. No paper found uses "harness" for writing as its object of study.
- No evidence found on writing-workspace design (file-based drafting, structured editors, revision passes, style-guide retrieval, memory of author preferences) with measured outcome differences holding the model fixed.
- The HAL, Epoch AI and Vals figures are reported through the position paper and were not checked at source.

## 4. Exemplar retrieval and in-context style

### Takeaway
In-context exemplars move style measurably but shallowly: large gains on easy, formulaic registers; small ones on informal personal prose; almost no gain from adding more than a few examples; and outputs remain detectable as AI. Content-similar exemplar retrieval, the default RAG choice, made style imitation worse in the one study that tested it.

### Cited Findings
- "Catch Me If You Can? Not Yet" (Findings of EMNLP 2025, peer-reviewed): 400+ real authors, 40,000+ generations per model, six models (GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, Gemma-3-27B, DeepSeek-V3, Llama-4-Maverick), news, email, forum and blog text. — [arXiv 2509.14543](https://arxiv.org/abs/2509.14543); [ACL Anthology](https://preview.aclanthology.org/dashboard/2025.findings-emnlp.532)
- Same paper, 5-shot versus zero-shot authorship verification accuracy for GPT-4o: news 95.28 versus 93.14; email 96.15 versus 85.02; Reddit 63.65 versus 56.66; blogs 19.37 versus 8.15. Blog verification stayed between 16.7% and 21.3% at 5-shot across the four models with baselines. — [arXiv 2509.14543v1 HTML](https://arxiv.org/html/2509.14543v1)
- Same paper, share of outputs GPTZero classed as human at 5-shot for GPT-4o: news 0.08%, email 16.86%, Reddit 0.67%, blogs 0.47%. Gemini-2.0-Flash and Gemma-3-27B were higher (for example 54.25% and 43.63% on email; 18.74% and 7.58% on blogs). — [arXiv 2509.14543v1 HTML](https://arxiv.org/html/2509.14543v1)
- Same paper, number of demonstrations: 2, 4, 6, 8 and 10 examples "affect the four metrics very little" (values in figures only). — [arXiv 2509.14543v1 HTML](https://arxiv.org/html/2509.14543v1)
- Same paper, exemplar selection: choosing exemplars by content similarity to the target lowered top-5 authorship attribution on every dataset (email 69.33 to 36.00; Reddit 35.43 to 16.63; blogs 43.93 to 22.13) and lowered email verification from 95.44 to 81.28. Including a snippet of the author's actual opening raised the "human" rate on all four datasets (for example blogs 9.00% to 21.70%). — [arXiv 2509.14543v1 HTML](https://arxiv.org/html/2509.14543v1)
- The paper ran no fine-tuning comparison, by design. — [arXiv 2509.14543v1 HTML](https://arxiv.org/html/2509.14543v1)
- Blind-read evidence that exemplars do not transfer literary style: expert readers' odds of preferring in-context-prompted AI over human experts were 0.16 for stylistic fidelity. — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939)
- Copying from demonstrations: a persona-dialogue study found that as demonstrations sharing the query's context were added, outputs converged on the demonstration responses until they reproduced them; an EACL 2026 Findings paper describes a general "copying bias" in few-shot prompting (both at search-summary level; neither is about prose style). — [arXiv 2402.09954](https://arxiv.org/pdf/2402.09954); [EACL 2026 Findings](https://preview.aclanthology.org/ingest-eacl/2026.findings-eacl.13.pdf)
- Recitation risk sits on the fine-tuning side as well: "Alignment Whack-a-Mole" (ICML 2026, peer-reviewed) fine-tuned GPT-4o, Gemini-2.5-Pro and DeepSeek-V3.1 on "write an N-word excerpt in the style of X" tasks and extracted up to 85-90% of held-out books, with single verbatim spans over 460 words; fine-tuning on one author unlocked recall of 30+ unrelated authors; fine-tuning on synthetic text gave near-zero extraction; models produced almost no verbatim text before fine-tuning. — [ICML 2026](https://icml.cc/virtual/2026/78906); [arXiv 2603.20957](https://arxiv.org/pdf/2603.20957v3)

### Inferences
- The plateau is early: most of the in-context style gain arrives by about 2-5 exemplars. Adding more exemplars is not a path to deep style.
- Retrieval keyed on topic similarity is the wrong retrieval for style. It likely pulls the model toward the exemplar's content and away from the author's register. A style harness would need exemplars chosen for register, not topic.
- Informal, idiosyncratic prose is where in-context imitation fails worst (blog verification about 20%). Essay-style personal non-fiction is closer to blogs than to newswire, so this is the relevant row for an essayist target.
- Verbatim recitation is documented more strongly as a fine-tuning hazard (on large API models whose pre-training already contains the books) than as an exemplar-retrieval hazard.

### Gaps
- No study found measuring verbatim or n-gram copying from in-context style exemplars in prose generation.
- No study found testing whether in-context exemplars transfer rhetorical structure (argument shape, paragraph moves) as distinct from surface style.
- No dose-response study beyond 10 exemplars, and none using long-context "whole corpus in the prompt" on 2026 models for style, was found.
- The few-shot study used 2024-2025 models; whether 2026 frontier models close the gap is not established here.

## 5. Writing-quality evaluation used in this literature

### Takeaway
Automatic judging of prose is the weak link. The best reported LLM judges agree with human preferences 73-87% of the time, and only with task-specific criteria or training; fixed-rubric LLM judges fall to 40-69%. Blind pairwise reads by experts are the only evaluation that has overturned a headline result, and experts and lay readers disagree with each other.

### Cited Findings
- WritingBench (preprint): 1,000 queries, 6 domains, 100 subdomains. A fine-tuned critic model with query-dependent criteria reached 84% human agreement; Claude-3.7 with query-dependent criteria reached 87%; static criteria gave 67% and 58% (Claude-3.7 as judge) and 69% and 40% (GPT-4o as judge). — [arXiv 2503.05244v4](https://arxiv.org/html/2503.05244v4)
- HelloBench (preprint): its GPT-4o judge was validated by three humans rating whether 200 judge outputs were "reasonable" (92.83 reasonable rate), not by agreement with independent human scores (search-summary level). — [arXiv 2409.16191](https://arxiv.org/pdf/2409.16191)
- LitBench (EACL 2026, peer-reviewed): best zero-shot LLM judge (Claude-3.7-Sonnet) reached 73% agreement with human story preferences; trained Bradley-Terry and generative reward models reached 78%. Human labels are Reddit story preferences, not expert editors (search-summary level). — [ACL Anthology](https://aclanthology.org/2026.eacl-long.362); [arXiv 2507.00769](https://arxiv.org/abs/2507.00769v1)
- LitBench cites Feuer et al. (2025) as finding that stylistic choices shape LLM-judge decisions more than substance (reported via LitBench; not checked at source). — [arXiv 2507.00769](https://arxiv.org/abs/2507.00769v1)
- ExpertLongBench (ICLR 2026 per a secondary listing): 11 expert tasks in 9 domains with checklist-based scoring (CLEAR). Best average F1 was 26.8% (Gemini-2.0-Flash) in an early version and 33.4 (Gemini-2.5-Pro) in a later one; the legal task was below 8% for all models; two LLM checklist judges correlated at Pearson 0.88 with each other (search-summary level). — [arXiv 2506.01241](https://arxiv.org/html/2506.01241v3)
- LongGenBench: all ten evaluated models degraded as required length increased (abstract-level, via search). — [search summary citing the LongGenBench abstract; ExpertLongBench result page](https://arxiv.org/pdf/2506.01241)
- Expert versus lay divergence: under in-context prompting, experts' odds ratio for AI on writing quality was 0.13 while general readers' was 1.82; the reader-type interaction was significant (p < 10^-4 for quality). — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939)
- LLM judges are lenient toward LLM output: the Anthropic harness post reports its evaluator "identified real issues, then talked itself into approving the work" until calibrated with few-shot scored examples; scores then improved over iterations and plateaued, and the author sometimes preferred a middle iteration to the last. — [Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Agents' Room built an LLM evaluator that correlates significantly with human raters, alongside human preference judgements (summary-level). — [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0fbc8a83d93dd8021a4dd8d2d34138eb-Abstract-Conference.html)
- Automatic style metrics in use: authorship attribution and verification accuracy, MAUVE, AI-detector pass rate. Panza suggests rough thresholds of above 0.2 BLEU and 0.75 MAUVE for plausible emails. — [arXiv 2407.10994v4](https://arxiv.org/html/2407.10994v4); [arXiv 2509.14543v1](https://arxiv.org/html/2509.14543v1)

### Inferences
- What has counted as a meaningful gain in this literature: 10-28 absolute points on a human-judged dimension for pipelines (STORM, DOC); a reversal of pairwise preference (odds ratio from below 1 to above 1) for fine-tuning; 5 or more points on a 100-point LLM-judged scale is commonly reported but sits inside the 13-27% judge-human disagreement band.
- A judge that agrees with humans 73-87% of the time cannot reliably rank two systems whose true preference split is close to 55/45. Harness-versus-model comparisons for prose need blind human reads, and expert readers specifically when the claim is about style.
- Any loop that optimises a writing harness against an LLM judge inherits the judge's documented preference for style over substance and its leniency toward LLM text.

### Gaps
- No study found measuring disagreement among expert editors on prose quality, which would set the noise floor for human evaluation.
- CoAuthor and the CHI co-writing evaluation methods were not examined in this pass beyond confirming the design-space survey exists (section 8).
- WritingBench's peer-review venue is not confirmed. HelloBench, LongGenBench and ExpertLongBench details are summary-level.
- No source found stating a field-agreed minimum meaningful difference for writing-quality metrics.

## 6. Industry and practitioner practice

### Takeaway
Provider and practitioner material on writing workflows is advice, with almost no measurement. The one detailed provider account of a generator-evaluator harness is about app building, uses single examples, and reports that harness parts became unnecessary with each model release.

### Cited Findings
- Anthropic engineering post (vendor, March 2026, not peer-reviewed): planner, generator and evaluator agents; subjective quality made gradable through four named criteria with weights; evaluator calibrated with few-shot scored examples; 5-15 iterations per run. Reported measurements are one-off cost and duration comparisons ($9 and 20 minutes solo versus $200 and 6 hours with the harness). — [Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Same post: wording in the grading criteria (the example given is "museum quality") visibly steered outputs toward a particular convergence; separating the critic from the generator was "more tractable" than making a generator self-critical. — [Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Same post: a "radical simplification" of the harness failed; removing one component at a time identified which pieces were load-bearing. — [Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Every (vendor, paywalled): 44% "quality improvement" for a writing product's prompts via GEPA, no method visible. — [Every](https://every.to/also-true-for-humans/this-prompt-optimizer-learns-from-its-mistakes-like-dna)
- Blog-level claim that DSPy-style optimisation adds roughly 5-15% over manual prompt iteration on the same base model; described in the search summary as anecdotal. — [comparison blog](https://learn.engineering.vips.edu/compare/dspy-vs-textgrad)

### Inferences
- Measured industry evidence for writing harnesses is effectively absent from what was retrievable. Outline-first drafting, critique passes and style guides in context are supported by the academic pipeline results in section 2, not by vendor measurements.
- The transferable practitioner lessons are procedural: separate the critic from the writer, calibrate the critic against the owner's own judgements with scored examples, expect scores to plateau and intermediate drafts sometimes to be better, and ablate one component at a time.

### Gaps
- Provider documentation on writing-specific workflows (context-engineering posts, reusable "skills" for writing, editor agents) was not retrieved; searches did not surface any with measurements. This is unverified absence, not confirmed absence.
- No measured comparison found of "style guide in context" versus none, or of reusable writing instructions, on human-judged prose.
- No practitioner account found reporting blind human evaluation of a multi-pass writing workflow.

## 7. Small-model-plus-large-model systems for writing

### Takeaway
The planner-realiser split exists in the literature (large model writes neutral content, small tuned model applies style) and small models trained with a large model as judge can match models three times their size on stories. Evidence that a small style adapter adds measurable author style on top of a large model's draft is thin, and the one study with authorship metrics is negative.

### Cited Findings
- SAG, style-aligned article generation (2024 preprint): a large model produces a neutral base text and a small model handles style, trained by style supervised fine-tuning then content DPO; the large model is frozen. Described at search-summary level; no numbers retrieved. — [arXiv 2410.03137](https://export.arxiv.org/pdf/2410.03137)
- InMyStyle (preprint, 2026): local helper LLMs build paired data, then a 0.5B-7B LoRA model rewrites AI-edited text toward the user's style. Quality plateaued across model sizes (0.689-0.695); stylometric improvement near zero; authorship probability 0.51-0.53; LLM-judged "AI-ness" fell more than 20%. Single user, 219 evaluation pairs. — [arXiv 2607.29238](https://arxiv.org/abs/2607.29238)
- POLARIS (EMNLP 2026): a frontier LLM used as an online rubric judge during RL training of a 9B model; blinded humans rated the result on par with the 27B model in the same family. The large model is a training-time component here, not an inference-time one. — [arXiv 2606.04095](https://arxiv.org/abs/2606.04095)
- WritingBench: 7-8B models fine-tuned on 12K critic-filtered examples outscored GPT-4o (7.44 and 7.39 versus 6.81) on the benchmark's own LLM critic. — [arXiv 2503.05244v4](https://arxiv.org/html/2503.05244v4)
- Panza cost profile: adapter fine-tuning under 24 GB GPU memory (4-bit variant on a free Colab T4), inference about 16 tokens per second on an M3 Pro laptop; quantising to 4-bit moved BLEU from 0.265 to 0.207 while MAUVE stayed at 0.97-1.00. — [arXiv 2407.10994v4](https://arxiv.org/html/2407.10994v4)
- Fine-tuned GPT-4o per author: median $81 fine-tuning plus inference. — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939)
- "Customizing LLM generation style using PEFT" (2024 preprint) exists as a style-adapter reference; not read. — [arXiv 2409.04574](https://arxiv.org/pdf/2409.04574)

### Inferences
- Two results point the same way for a small local style model: InMyStyle's rewriter removed AI tells without adding author signal, and Panza's style metric (MAUVE) survived quantisation while its content metric (BLEU) dropped. Small tuned models appear able to carry register cheaply; content and structure are where they fall short. That argues for the split in which a large model supplies content and structure and the small model is confined to surface realisation, but no study found tests that split with blind reads.
- Using a frontier model as judge during small-model training (POLARIS) is a harness-into-weights route: the harness's critic is spent at training time. It has peer-reviewed human validation for stories, not for expository prose or author style.

### Gaps
- No study found that distils a multi-stage writing pipeline into a small model and reports quality retained.
- No study found with a fine-tuned small model used as reranker or verifier of style inside a large-model writing loop, with human evaluation.
- No cost-versus-quality curve found for planner-realiser writing systems. SAG's numbers were not retrieved.

## 8. Census and judgement

### Takeaway
The writing harness is not a recognised research area. Relevant work is scattered across four communities that do not share a name for it, and none has a survey that treats the pipeline around the model as the object of study for prose quality. Fine-tuning and personalisation for style is the larger and better-surveyed literature; fixed-model harness studies exist almost entirely for coding and task agents.

### Cited Findings
- Human-computer interaction: "A Design Space for Intelligent and Interactive Writing Assistants" (CHI 2024, 36 authors) was built from a systematic review of 115 papers, organised by task, user, technology, interaction and ecosystem. It maps writing-assistant design; it is not an evaluation of pipeline effects on output quality. — [arXiv 2403.14117](https://arxiv.org/abs/2403.14117)
- Personalisation: at least three surveys in 2024-2025 organise methods into retrieval or prompting, fine-tuned adapters, and preference alignment: "Personalization of Large Language Models: A Survey", "A Survey of Personalized Large Language Models", and "Personalized Generation in Large Model Era". — [arXiv 2411.00027](https://arxiv.org/pdf/2411.00027); [arXiv 2502.11528](https://arxiv.org/html/2502.11528v2); [arXiv 2503.02614](https://arxiv.org/pdf/2503.02614v2)
- Agent harness: fixed-model scaffold comparisons found were all 2026 preprints or vendor posts on coding, terminal and GAIA tasks, and the main position paper mentions no writing task. — [arXiv 2605.23950](https://arxiv.org/html/2605.23950); [arXiv 2606.08529](https://arxiv.org/abs/2606.08529)
- Venues where the located writing-pipeline papers appeared: NAACL 2024 (STORM), ACL 2023 (DOC), ICLR 2025 (Agents' Room), Findings of EMNLP 2025 (in-context style limits), EACL 2026 (LitBench), EMNLP 2026 (POLARIS), ICML 2026 (fine-tuning and verbatim recall), CHI 2024 and CHI 2026 (design space; fine-tuned versus prompted style). — [arXiv 2402.14207](https://arxiv.org/abs/2402.14207); [arXiv 2212.10077](https://arxiv.org/abs/2212.10077); [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0fbc8a83d93dd8021a4dd8d2d34138eb-Abstract-Conference.html); [ACL Anthology](https://preview.aclanthology.org/dashboard/2025.findings-emnlp.532); [ACL Anthology](https://aclanthology.org/2026.eacl-long.362); [arXiv 2606.04095](https://arxiv.org/abs/2606.04095); [ICML 2026](https://icml.cc/virtual/2026/78906); [arXiv 2601.18353](https://arxiv.org/pdf/2601.18353)
- Targeted searches for (a) prompt-optimiser results on long-form writing, (b) end-to-end optimisation of a writing pipeline against human preference, and (c) fixed-model writing-scaffold ablations each returned no matching paper. — [GEPA abstract, no writing task named](https://arxiv.org/abs/2507.19457); [harness position paper, no writing task](https://arxiv.org/html/2605.23950)

### Inferences
- Rough census from this sweep (an estimate from what surfaced in about 40 queries, not a count): papers that hold the model fixed and vary the structure around it for writing, with human evaluation, number in the low tens for 2022-2026 and are concentrated in grounded article generation (STORM lineage) and story generation (Re3, DOC, Agents' Room lineage). Papers that fine-tune, adapt or preference-optimise for style, personalisation or creative writing are several times more numerous and have three or more dedicated surveys. Papers that use the word harness or scaffold with writing quality as the outcome: none found.
- The four communities and what each holds: NLP generation (pipelines, measured on organisation and coverage); personalisation and information retrieval (retrieval versus adapters, measured on ROUGE); HCI (co-writing interfaces, measured on user experience); agent evaluation (harness effects, measured on task success). The requester's question, harness versus training for prose quality and voice, falls between all four.
- Division of credit as the evidence stands. Model-level training is credited, with blind expert reads, for author-level style and for removing AI-typical surface. Harness-level structure is credited, with human evaluation on older models, for organisation, coverage and long-range coherence. In-context exemplars are credited with a modest, early-plateauing style shift that fails on informal personal prose. Nothing found credits either side for expository clarity or explanation quality specifically.
- For a two-week small-model style fine-tune that has stalled: the literature does not show that a harness would have delivered the style that fine-tuning targets (the direct evidence says prompting with exemplars does not). It does suggest that properties a small model lacks, namely content, structure and coherence over length, are the ones pipelines have improved, and that the combination of large-model content with small-model realisation is plausible and untested.

### Gaps
- No systematic count was made; database queries with inclusion criteria would be needed for defensible numbers.
- No survey of writing pipelines or writing agents as systems was found. Surveys of compound AI systems and agent scaffolding were not retrieved, so whether any has a writing section is unknown.
- Where the literature is thin or empty: fixed-model harness ablations for prose; prompt or pipeline optimisation against human writing preference; harness versus fine-tune versus both in one study; expository and explanatory writing quality (most work is fiction, Wikipedia-style articles, email or reviews); expert-reader evaluation on 2026 frontier models inside a pipeline; verbatim copying from in-context style exemplars.
