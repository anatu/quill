# De-slop evidence and corpus design for informational prose

Research date: 2026-11-13. Evidence labels used below: [PR] = peer-reviewed venue; [PP] = preprint; [BLOG] = practitioner, vendor or press; [WIKI] = Wikipedia project page. "Snippet-level" means I saw the claim only in a search summary and did not open the paper. Numbers from papers I opened were extracted by a fetch tool summarizing the page, so check the primary source before quoting any figure in a publication.

## 1. What measurably distinguishes LLM-written from human-written expository text?

### Takeaway
The best-measured differences are grammatical and lexical, and they come from instruction tuning: GPT-4o uses present-participial clauses about 5x and nominalizations about 2x the human rate, and a classifier on 66 Biber features separates one LLM from humans at 93-98%. Individual marker words ("delve") decay within a year or two of becoming famous, so word lists are a moving target, while structural habits (noun-heavy dense style, contrast frames, trailing "-ing" clauses, low variation) are the more durable signal. Effect sizes for sentence-length variance, tricolons and summary closers are poorly quantified.

### Cited Findings

Vocabulary
- [PR] Kobak et al. (Science Advances 11(27), 2025) apply excess-mortality logic to 14-15 million PubMed abstracts, 2010-2024. They estimate that at least 10% of 2024 abstracts were LLM-processed (13.5% in a later version), reaching 30% in some sub-corpora. The numbers differ by arXiv version. Snippet-level. — [arXiv 2406.07016](https://arxiv.org/abs/2406.07016v5)
- The Kobak repository lists all 900 excess words found for 2013-2024, annotated, and has an update with six more months of data. — [berenslab/llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab)
- [PR] Juzek & Ward (COLING 2025) identify 21 focal words whose rise in scientific abstracts is likely due to LLM use, and report that study participants react differently to "delve" than to the other focal words. Snippet-level. — [arXiv 2412.11385](https://arxiv.org/pdf/2412.11385)
- [PR] Reinhart et al. (PNAS, Feb 2025): word rates in GPT-4o output relative to humans were camaraderie 162x, tapestry 155x, intricate 119x, underscore 107x, amidst 100x, palpable 95x. "Tapestry" appeared in 23% of GPT-4o outputs and "amidst" in 27%. Llama 3 Instruct had its own set (unease 63-101x, palpable about 47x). Obscenities were more than 100x rarer in LLM text. — [arXiv 2410.16107](https://arxiv.org/html/2410.16107v2)
- [PR] Paech et al. (ICLR 2026): some slop patterns appear "over 1,000x more frequently" in LLM output than in human text. — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061)
- [WIKI] Wikipedia's "Signs of AI writing" groups marker words by model era. 2023 to mid-2024: additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant. Mid-2024 to mid-2025: align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant. Mid-2025 to mid-2026: emphasizing, enhance, highlighting, showcasing. Mid-2026 onward: challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally. The page says a single word is weak evidence and many in one edit is "one of the strongest tells". — [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Marker words fade. Wikipedia says "delve" was heavily overused in 2023 and early 2024 and dropped sharply in 2025. A 2026 preprint on 44 years of CHI papers calls "delve" the clearest case of a 2024 spike followed by decline by 2026. A Korean-abstract preprint finds several words peaked in 2024-2025 and fell toward trend in 2026 while others kept rising. Geng & Trotta (2025) are cited as showing "delve" fell once famous while other favored words kept rising. The last three are snippet-level. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing); [arXiv 2609.23090](https://arxiv.org/pdf/2609.23090); [arXiv 2609.07447](https://arxiv.org/pdf/2609.07447)
- [PP] A 2026 preprint argues the excess-vocabulary method cannot separate "more papers use models" from "models became harder to detect". Snippet-level; the search did not make clear which of two 2026 preprints said this. — [arXiv 2609.07447](https://arxiv.org/pdf/2609.07447); [arXiv 2609.10664](https://arxiv.org/pdf/2609.10664)

Syntax and register (Biber features)
- [PR] Reinhart et al. built parallel corpora by having models continue human texts (HAP-E: 8,290 texts, 66,320 chunks; CAP: 9,615 texts) with GPT-4o, GPT-4o Mini and Llama 3 8B/70B base and instruct. GPT-4o versus humans: present participial clauses 5.3x (d = 1.38); nominalizations 2.1x (d = 1.23); "that" clauses as subject 2.6x (d = 0.77); phrasal coordination 1.9x (d = 0.81); agentless passives at about half the human rate. — [arXiv 2410.16107](https://arxiv.org/html/2410.16107v2)
- Same paper: a random forest on Biber features got 66% on a seven-way task (chance 14%); 4.2% of LLM texts were classed as human and 9.8% of human texts as LLM. Pairwise one-LLM-versus-human accuracy was 93-98% across corpora. — [arXiv 2410.16107](https://arxiv.org/html/2410.16107v2)
- Same paper: base Llama 3 models use features and words at near-human rates; instruction-tuned ones diverge. Larger models were not closer to humans than smaller ones. The authors conclude instruction tuning trains "a particular informationally dense, noun-heavy style". — [arXiv 2410.16107](https://arxiv.org/html/2410.16107v2)
- Limits of that paper: no per-genre breakdown, English only, classifiers dropped sharply on an external abstracts set, and the newest model tested is GPT-4o. — [arXiv 2410.16107](https://arxiv.org/html/2410.16107v2)
- [PP] "Base Models Look Human To AI Detectors" (2026): Llama-3-8B base continuations of human prefixes scored 96.7% (GPTZero) and 98.8% (Pangram) human probability; the instruct model scored 30.3% and 17.1%. Qwen3-8B showed similar gaps. — [arXiv 2605.19516](https://arxiv.org/html/2605.19516v1)
- [PR] Zanotto & Aroyehun (EMNLP 2025), eight domains and 11 LLMs: human texts have simpler syntax and more diverse semantic content; newer models produce text that is similarly variable to each other (homogenization). Snippet-level. — [ACL Anthology 2025.emnlp-main.1163](https://preview.aclanthology.org/setup/2025.emnlp-main.1163)
- [PP] "More Aligned, Less Diverse?" (2026) compares two LLM generations and reports newer models' sentences are 15-30% longer than human authors'. Snippet-level. — [arXiv 2605.06030](https://arxiv.org/pdf/2605.06030)
- [PP] Stylometry on 10-sentence samples with tree models finds LLM text more grammatically standardized, with overuse of certain words and punctuation. Snippet-level. — [arXiv 2507.00838](https://arxiv.org/html/2507.00838v2)
- [PP] One 2025 study reports human essay perplexity of 29.5 versus about 15 for LLM outputs. Snippet-level. — [arXiv 2509.24930](https://arxiv.org/pdf/2509.24930v1)

Sentence-length variance ("burstiness")
- [PP] A 2023 comparison of six LLMs on news found LLM sentence lengths vary less than human ones. Snippet-level, no effect size seen. — [arXiv 2308.09067](https://arxiv.org/pdf/2308.09067)
- [PP] Tarım & Onan (2025): LLaMA reduces burstiness relative to humans, but a diffusion LM came close to human values; perplexity and burstiness alone do not separate reliably. Snippet-level. — [arXiv 2507.10475](https://arxiv.org/pdf/2507.10475)
- [WIKI] Wikipedia says mid-2026-onward output uses more periods and commas and sentences of roughly 8-20 words. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

Rhetorical and discourse tells
- [WIKI] Negative parallelism in three forms: "Not just X, but also Y", "Not X, but Y", and the reversed "Y rather than X", the last called particularly common in recent output. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [BLOG] A Decrypt article citing a Washington Post analysis of 328,744 ChatGPT messages says variants of "not just X, but Y" appeared in roughly 6% of July messages. Secondary press; I did not see the original. — [Decrypt](https://decrypt.co/348923/5-biggest-tells-something-written-ai)
- [BLOG] Paech's slop score weights contrast frames heavily: 60% slop words, 25% "not X, but Y" patterns, 15% slop trigrams, per a paper's description of the EQ-Bench implementation. — [arXiv 2601.21169](https://arxiv.org/pdf/2601.21169); [sam-paech/slop-score](https://github.com/sam-paech/slop-score)
- [WIKI] Other catalogued tells: trailing "-ing" clauses that attach vague significance; copula avoidance ("serves as", "features" for "is"); vague connections ("associated with", listed among the most common signs as of October 2026); the "despite its... faces challenges" formula ending on a positive note; hedging disclaimers; rule of three; em dashes. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WIKI] The page marks several tells as outdated or historical: significance/legacy puffery examples, vague attributions, promotional language (2023-2025), section summaries, and em dash overuse (2022 to September 2026). It cites a study of an over-10% drop in "is"/"are" in academic writing in 2023. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WIKI] Caveats on that page: "Not all text featuring these indicators is AI-generated", and the list is not a ban on words or punctuation. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing); [FlowingData](https://flowingdata.com/2025/10/20/signs-of-ai-writing-on-wikipedia/)
- [PR] Russell, Karpinska & Iyyer (ACL 2025): expert annotators explaining their calls on 300 non-fiction articles relied on "AI vocabulary" and also on formality, originality and clarity. — [ACL Anthology 2025.acl-long.267](https://aclanthology.org/2025.acl-long.267)

### Inferences
- The participial-clause and nominalization excess are the same thing Wikipedia editors describe informally as "superficial analysis with -ing clauses" and puffed-up abstraction. These are the strongest quantified targets for an informational restyler, and they are measurable with an off-the-shelf Biber tagger.
- Since base models sit near human rates and instruct models do not, the "AI style" is a learned assistant register, which is why fine-tuning on human text can plausibly move it.
- A fixed banned-word list will go stale within a model generation. A metric built on rates relative to a human reference corpus (as in Reinhart or Paech) ages better.
- Wikipedia's tells come from encyclopedia drafts, so the content-level ones (notability claims, awards sections) do not carry over to explainers; the language-level ones do.

### Gaps
- I found no study giving an effect size for sentence-length standard deviation for GPT-4o-, Claude- or GPT-5-class models. Popular "burstiness score" ranges trace to an unsourced humanizer tool.
- I found no peer-reviewed frequency measurements for tricolons, signposting or summary closers in expository text. The Wikipedia fetch covered only the first 100,000 of about 248,000 characters, so its rule-of-three, signposting and em-dash sections were not read in full.
- No Biber-style replication on 2025-2026 frontier models was found. Whether the 5.3x participial figure holds for them is unknown.
- The Wikipedia page's era labels (including a "GPT-6" era) were reported by the fetch tool and I could not independently confirm them.

## 2. Do readers prefer human expository writing to LLM writing, and when?

### Takeaway
On blind tests of informational text, lay readers mostly do not prefer human writing: they rate LLM summaries as clearer or indistinguishable, and rate news equally. Preference for human text shows up with expert readers, with labels attached, and on comprehension. "Clearly preferred over generic LLM writing" is therefore a hard bar with ordinary readers and a more reachable one with heavy LLM users, who are the readers that notice slop.

### Cited Findings
- [PR] Markowitz (PNAS Nexus, 2024): with authorship hidden, GPT-4 lay summaries of PNAS papers were rated simpler, clearer and easier to understand than the researchers' own; readers also did better on comprehension checks. Effects were statistically significant but small. Snippet-level. — [arXiv 2405.00706](https://arxiv.org/pdf/2405.00706); [PsyPost](https://www.psypost.org/generative-ai-simplifies-science-communication-boosts-public-trust-in-scientists/)
- [PP] Guo et al. (2025), 150 Mechanical Turk participants: LLM plain-language summaries were indistinguishable from human ones on subjective ratings (simplicity, informativeness, coherence, faithfulness), but human-written ones produced "significantly better comprehension". Ten automated metrics did not track human judgment. — [arXiv 2505.10409](https://arxiv.org/abs/2505.10409v1)
- [PP] A 2026 survey experiment found ML-expert readers could not reliably tell human from LLM-generated or LLM-edited research summaries despite high confidence. Snippet-level. — [alphaXiv 2601.15556](https://www.alphaxiv.org/abs/2601.15556.md)
- [PP] Gilardi et al., preregistered, 599 Swiss participants: no significant difference in perceived quality between journalist-written, AI-rewritten and fully AI-generated news. Disclosure raised immediate engagement but not openness to AI news later. — [arXiv 2409.03500](https://arxiv.org/html/2409.03500v2)
- [PP] Zhu et al. (2024): raters could not tell the two kinds apart blind, and favored whatever was labelled human; a label swap showed preference followed the label. Snippet-level. — [arXiv 2410.03723](https://arxiv.org/pdf/2410.03723v2.pdf)
- [PP] Chakrabarty, Ginsburg & Dhillon (literary, not expository): for prompted frontier models, 28 MFA readers strongly preferred human text (odds ratio 0.16 for style, 0.13 for quality), while 131 lay readers were neutral on style (0.86, n.s.) and preferred the AI on quality (1.55, p = 0.014). — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- Same study: for prompted outputs, a higher Pangram AI score predicted lower expert preference, and cliché density mediated 16.4% of that effect. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- [PR] Companion paper (CHI 2026): experts preferred human writing in 82.7% of cases against prompted AI; lay judges preferred AI in both conditions. — [arXiv 2601.18353](https://arxiv.org/abs/2601.18353)
- [PR] Russell et al.: the majority vote of five frequent-LLM-user annotators misclassified 1 of 300 non-fiction articles (GPT-4o, Claude, o1), beating most detectors even after paraphrasing and humanization. — [ACL Anthology 2025.acl-long.267](https://aclanthology.org/2025.acl-long.267)
- [WIKI] Wikipedia cites a 2025 study finding general human detection "no better than random chance", a German-theses study with 57% recognition for AI texts and 64% for human, and a preprint where experts caught 90% of AI text with 3.3% false positives. — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

### Inferences
- The reader population decides the outcome. Naive crowd readers reward fluency and simplicity, which generic LLM text already has. Frequent LLM users and trained writers penalize recognizable AI style. The project's claim should name its reader pool.
- Because blind lay ratings of informational text are near parity, a restyler can lose by removing clarity. Comprehension should be tracked alongside preference (Guo et al. show the two diverge).
- Label effects are large, so every comparison must be blind.

### Gaps
- I found no blind pairwise study of human versus LLM technical explainers or mathematics walkthroughs.
- I found no systematic survey of what readers say they dislike about AI informational writing. The nearest evidence is the annotator explanations in Russell et al. (vocabulary, formality, lack of originality) and the cliché mediation result, which is literary.
- Markowitz and Guo figures are from abstracts and summaries; exact effect sizes were not retrieved.

## 3. What works for removing "AI style" by fine-tuning?

### Takeaway
Three approaches have measurements behind them: fine-tuning on human text with back-translated instructions (flips expert preference and drops detector flags from 97% to 3%), training a paraphraser to invert LLM paraphrases back to human originals (about 12,000 pairs and one LoRA epoch suffice to move detectors), and targeted logit-level suppression of overused patterns (FTPO, about 90% slop reduction without quality loss). Plain DPO against slop degraded writing quality in the one direct comparison.

### Cited Findings

Fine-tuning on human text
- [PP] Chakrabarty et al. fine-tuned GPT-4o separately on each of 30 living authors' complete works, split into 250-650 word excerpts. Each training pair was an instruction plus a GPT-4o-generated content description as input and the original excerpt as output (instruction back-translation). One epoch for the four largest corpora, three for the rest. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- Same study, 3,840 pairwise judgments: after fine-tuning, experts favored AI for style (odds ratio 8.16) and quality (1.87); lay readers 8.29 and 2.42. Pangram flagged 97% of prompted outputs and 3% of fine-tuned ones; GPTZero 91% and 0%. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- Same study: preference showed no systematic relation to corpus size (Pearson r < 0.1); corpora ranged from 2 books to 22. Cost was $25-$276 per author, median $81. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- Limits: only GPT-4o was fine-tuned; excerpts were 450 words or fewer; fine-tuned outputs were post-edited by GPT-4o for grammar and consistency; lay agreement was low (Fleiss' kappa 0.07-0.22). Literary fiction, not exposition. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- [PR] The CHI 2026 companion reports expert preference moving from 82.7% human (prompted) to 62% AI (fine-tuned). — [arXiv 2601.18353](https://arxiv.org/abs/2601.18353)

Paraphrase-then-invert
- [PP] "Base Models Look Human" (HIP): 11,757 pairs mapping a GPT-5-nano paraphrase back to the original human passage (sources include RAID and MAGE); LoRA rank 128, one epoch, loss only on the human completion; tested on Qwen3 0.6B-14B and Llama 3 8B/70B. Applied iteratively for 10 rounds, it beat DIPPER, SilverSpeak, StealthRL and simple paraphrase on GPTZero and Pangram, but semantic preservation fell with each round. — [arXiv 2605.19516](https://arxiv.org/html/2605.19516v1)
- Same paper, appendix: fine-tuning an instruct model on FineWeb-Edu (generic human educational web text) also recovered much of the lost human-likeness. The same method on GPT-4.1-nano through the OpenAI API did not give a useful trade-off. — [arXiv 2605.19516](https://arxiv.org/html/2605.19516v1)
- [PP] "Language Models Optimized to Fool Detectors Still Have a Distinct Style": Mistral-7B with LoRA (r = 32) trained to recover human originals from machine paraphrases, conditioned on same-author exemplars, on about 1M Reddit comments from 63,184 authors with 5 paraphrases each, one epoch; then DPO preferring the most human-like of 20 generations. Style similarity rose from 0.71 to 0.83 and semantic similarity from 0.74 to 0.83 against TinyStyler. — [arXiv 2505.14608](https://arxiv.org/html/2505.14608v2)
- Same paper: models DPO-tuned only to beat FastDetectGPT drove that detector below chance (AUROC 0.72 to 0.18) yet a style-embedding detector still scored about 0.95-0.96. Beating a token-statistics detector does not remove the style. — [arXiv 2505.14608](https://arxiv.org/html/2505.14608v2)

Anti-slop methods
- [PR] Antislop (Paech et al., ICLR 2026): a backtracking sampler suppresses 8,000+ patterns where token banning becomes unusable at about 2,000; FTPO fine-tuning gives about 90% slop reduction while holding or improving GSM8K, MMLU and creative-writing scores; DPO gave weaker suppression with significant loss of writing quality and lexical diversity. The sampler costs throughput, so the authors prefer FTPO for deployment. Code is MIT-licensed. — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061); [liner summary](https://liner.com/review/antislop-a-comprehensive-framework-for-identifying-and-eliminating-repetitive-patterns)
- [BLOG] The slop-score repo ships a human writing profile and a benchmarking script over creative-writing and essay prompts. — [sam-paech/slop-score](https://github.com/sam-paech/slop-score)

Authorship style transfer
- [PR] TinyStyler (Findings of EMNLP 2024): an 800M-parameter model conditioned on pretrained authorship embeddings, reported to outperform GPT-4 on few-shot authorship style transfer; baselines include STYLL and PARAGUIDE. Snippet-level. — [arXiv 2406.15586](https://arxiv.org/pdf/2406.15586)
- [PR] StyleDistance (NAACL 2025) trains content-independent style embeddings on synthetic parallel text because earlier style embeddings leak content. — [ACL Anthology 2025.naacl-long.436](https://aclanthology.org/2025.naacl-long.436.pdf)
- [PP] AuthorMist uses reinforcement learning on Qwen2.5-3B to evade detectors, with reported success of 78.6-96.2% per detector. Secondary write-up only. — [alphaXiv 2503.08716](https://www.alphaxiv.org/abs/2503.08716)

### Inferences
- The "content description to human passage" and "LLM paraphrase to human original" formats are the same idea: the model sees AI-register or neutral input and must emit the human text. The second matches a draft restyler directly and has been shown at 8B scale with LoRA.
- Data sizes that worked: about 12,000 pairs (HIP), one author's books (Chakrabarty), 1M short comments (style-aware paraphraser). The project's 320,000-word single-author run is inside this range, so data volume is unlikely to be the constraint.
- The FineWeb-Edu result is the one direct data point that broad, unauthored human explanatory text moves an instruct model toward human-likeness as detectors measure it. It says nothing about reader preference.
- FTPO can be layered on any corpus choice to clean residual tells; the Antislop result argues against DPO with LLM drafts as negatives as the main method.
- Iterating a paraphraser trades meaning for style. For informational text a single pass plus a fidelity check is the safer default.

### Gaps
- I found no well-documented practitioner report with measurements of fine-tuning a small open model on human expository prose to reduce tells. Hugging Face and forum write-ups were not surfaced.
- STYLL and LUAR details were not retrieved; nothing was found on ORPO for this purpose.
- The Antislop models, training-set sizes and limitations were not on the abstract page.
- No study tests reader preference (as opposed to detector scores) for inverse-paraphrase models on expository text.

## 4. Single author versus multi-author training data; register transfer

### Takeaway
Direct evidence is thin. Per-author fine-tuning yields a distinct voice with as little as two books, and pooling many authors is reported to blend opposing style directions, but no study compares one author, a house style and a broad mix on reader preference. Broad human text does remove detector-visible AI style, so the open question is distinctness and appeal, and the project will have to test it.

### Cited Findings
- [PP] Chakrabarty et al.: per-author models were preferred regardless of corpus size (r < 0.1), from 2 books to 22. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- [PP] FAVoR (2026, federated personalization) states that naively pooling author data or averaging adapter updates mixes author-specific directions with unrelated or opposing ones, and names the result "author-style homogenization". Snippet-level. — [arXiv 2609.30968](https://arxiv.org/html/2609.30968)
- [PR] StyleTunedLM (INLG 2024) fine-tunes LoRA modules on Llama 2 for ten individual authors and also merges modules. Snippet-level. — [arXiv 2409.04574](https://arxiv.org/pdf/2409.04574)
- [PP] A 2025 study of novelists' styles found full fine-tuning gives greater stylistic fidelity than LoRA, with weak replication of Twain and Melville. Snippet-level. — [arXiv 2511.20459](https://arxiv.org/html/2511.20459)
- [PP] A 2026 few-shot author-style paper reports that direct fine-tuning maximizes style at the cost of quality. Snippet-level. — [arXiv 2610.03163](https://arxiv.org/html/2610.03163v1)
- [PP] The Mistral-7B style-aware paraphraser trained on 63,184 authors conditions on same-author exemplars at inference, so the many-author model is steered toward one target style, and it generalized to Amazon reviews and blogs not seen in training. — [arXiv 2505.14608](https://arxiv.org/html/2505.14608v2)
- [PP] Fine-tuning an instruct model on FineWeb-Edu recovered much of the human-likeness detectors measure. — [arXiv 2605.19516](https://arxiv.org/html/2605.19516v1)
- [PP] Optimizing against a style detector failed, which the authors attribute to the variety of human styles creating conflicting objectives. — [arXiv 2505.14608](https://arxiv.org/html/2505.14608v2)
- [PP] AVShift (2026): fine-tuned LLMs for authorship verification generalize best across genres and benefit substantially from stylistically diverse training data. This is verification, not generation. Snippet-level. — [arXiv 2608.17979](https://arxiv.org/html/2608.17979)
- [PR] Reinhart et al. argue LLM style misaligns with genre conventions: words common in fiction are conspicuous in academic or news writing. — [arXiv 2410.16107](https://arxiv.org/html/2410.16107v2)
- [PP] Co-writing with an instruction-tuned model reduced lexical and conceptual diversity across users. Snippet-level. — [arXiv 2508.01491](https://arxiv.org/pdf/2508.01491)

### Inferences
- The project's own result (an essayist's voice that does not suit explainers) fits the general point in Reinhart et al. that a style appropriate to one register is conspicuous in another. Register match of the corpus to the target task probably matters more than author count.
- A reasonable reading of the evidence for the three options:
  - (a) One explanatory author: best-supported route to a distinct voice; 320,000 words is ample. Risks are one author's tics becoming the new tells and narrow topical coverage.
  - (b) House-style multi-author corpus: untested in the literature. It is the middle case, with editorial constraints keeping style directions aligned, which is the condition FAVoR says naive pooling lacks.
  - (c) Broad mix: supported for removing detector-visible AI style (FineWeb-Edu, Reddit paraphraser). Expect a neutral human register, not a voice. Exemplar or author-tag conditioning is the published way to keep steerability.
- Since generic LLM text already ties with human text among lay readers, "neutral human" from option (c) may not be enough to be clearly preferred; (a) or (b) give readers something positive to prefer. This is a hypothesis to test.

### Gaps
- No study found that measures blandness or preference for a model trained on many authors versus one, and none on house-style corpora.
- No evidence found on minimum words per author beyond the Chakrabarty range, and none specific to QLoRA on 8B models.
- No study found on whether an author voice learned on narrative essays carries into technical explanation.
- No evidence found on factual fidelity as a function of single- versus multi-author training.

## 5. Does famous or heavily memorized text raise verbatim-copying risk after fine-tuning?

### Takeaway
Yes, for text the base model already memorized in pretraining: fine-tuning can reactivate it, and the fine-tuning corpus need not contain the text that gets regurgitated. The demonstrations are on large hosted models with a summary-to-text task; LoRA on small models showed near-zero memorization of the fine-tuning data in one preprint. An output-overlap check is cheap and should be run regardless of corpus choice.

### Cited Findings
- [PR per arXiv page: COLM oral; a search result also listed ICML 2026] "Alignment Whack-a-Mole" (Liu, Mireshghallah, Ginsburg, Chakrabarty; arXiv March 2026, revised Nov 2026): GPT-4o, Gemini-2.5-Pro and DeepSeek-V3.1 fine-tuned to expand plot summaries into text reproduced up to 85-90% of held-out copyrighted books, with single verbatim spans over 460 words; 81 books, 47 authors. — [arXiv 2603.20957](https://arxiv.org/abs/2603.20957); [ICML listing](https://icml.cc/virtual/2026/78905)
- Same paper: fine-tuning only on Murakami unlocked verbatim recall of books by more than 30 unrelated authors; fine-tuning on public-domain text or random authors gave comparable extraction; synthetic text gave far less. The three models memorized the same books in the same regions (r >= 0.90). The authors read this as reactivation of pretraining memorization. — [arXiv 2603.20957](https://arxiv.org/abs/2603.20957)
- Same paper offers no new mitigation; its authors argue the result undercuts a premise of fair-use rulings. That is advocacy by the authors. — [arXiv 2603.20957](https://arxiv.org/abs/2603.20957)
- [PP] Wang & Li (2025), GPT-2 and Llama 3: LoRA gave near-zero plagiarism-style memorization of fine-tuning data versus full fine-tuning, and duplication and model size did not raise it the way they do under full fine-tuning. — [arXiv 2506.20856](https://arxiv.org/html/2506.20856v1)
- [PP] Chakrabarty et al. held evaluation excerpts out of training, measured ROUGE-L of 0.16-0.23 between outputs and originals, and resampled outputs that regurgitated verbatim text. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- Creative Commons: "The only way to know whether a model has memorized content is by identifying model outputs" substantially similar to the original; mitigation "can mitigate, but may not eliminate" risk. — [Creative Commons](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)

### Inferences
- Risk tracks what the base model saw often in pretraining. Canonical public-domain classics and very famous essays are the likeliest to be latent in an 8B model, so choosing them for a restyler adds recall risk without adding legal exposure for the public-domain ones; the practical cost is outputs that quote instead of restyle.
- A restyler has a built-in safeguard: the content comes from the user's draft. The dangerous setup in the Whack-a-Mole paper is prompting with a description of the training text itself.
- Cheap mitigations consistent with the sources: hold out evaluation passages, keep epochs low, deduplicate, use LoRA, and run an n-gram or ROUGE-L overlap check of outputs against the corpus with resampling on hits.

### Gaps
- The Whack-a-Mole paper did not report open-weight 8B models, so the size of the reactivation effect at that scale is unknown.
- No study found on epochs versus memorization for QLoRA specifically. The LoRA result is one unreviewed preprint.
- The venue for the Whack-a-Mole paper is inconsistent across sources (COLM versus ICML).

## 6. Legal and norms context for training corpora, as of November 2026

### Takeaway
Creative Commons' position is that its licenses bind training only where copyright permission is needed; where an exception such as fair use applies, the license terms do not. If the license is relied on, CC reads NonCommercial as covering every stage through sharing the model, NoDerivatives as excluding use as training data, and ShareAlike and Attribution as conditional on public sharing. US law is unsettled: two 2025 district rulings found generative training fair use, and the first appellate ruling (September 2026) rejected fair use for a non-generative tool. This is not legal advice.

### Cited Findings

Creative Commons
- "CC licenses apply only when copyright permission is required." "If exceptions or limitations apply, then the CC license terms don't apply." — [CC: Using CC-licensed works for AI training](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- CC's 2023 post: there are "strong arguments that, in most cases, using copyrighted works to train generative AI models would be" fair use in the US, and training "can be protected by the text and data mining exception in the EU"; also "the answers may be complex or still unknown". — [CC, Aug 2023](https://creativecommons.org/2023/08/18/understanding-cc-licenses-and-generative-ai/)
- Attribution: required by all CC licenses; for datasets it "could be a simple link to the source of the dataset used to train the model"; for outputs produced with retrieval, attribution to the specific work is "ideal". Triggered when works or adaptations are shared publicly. — [CC](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- ShareAlike: phrased conditionally, "If AI models or outputs are based on ShareAlike content and they will be shared publicly...", the same license would be required. CC does not state a firm conclusion on whether models or outputs are adaptations. — [CC](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- NonCommercial: "all stages, from copying the data during training to sharing the trained model, must not be for commercial gain." — [CC](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- NoDerivatives: following it "would require that ND-licensed content not be used as training data." — [CC](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- CC says its guidance "is likely to lead to overcompliance with both copyright law and CC license terms", and that choosing a more restrictive license to block training is not effective. — [CC](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/); [CC legal primer, May 2025](https://creativecommons.org/2025/05/15/understanding-cc-licenses-and-ai-training-a-legal-primer/)
- CC signals, announced 25 June 2025: four signals (Credit, Direct Contribution, Ecosystem Contribution, Open) layered on top of licenses, not replacing them. Press describes them as social and ethical markers that are not currently enforceable. A repository synced December 2025 still called it a draft proposal. — [heise](https://heise.de/-10461593); [Maginative](https://www.maginative.com/article/creative-commons-unveils-framework-to-signal-ai-use-permissions/); [cc-signals repo listing](https://awesome.ecosyste.ms/projects/github.com%2Fcreativecommons%2Fcc-signals)

United States
- Bartz v. Anthropic (N.D. Cal., June 2025): training on books held fair use; liability for pirated library copies left open; settled for up to $1.5 billion. One October 2026 guide says the settlement was approved 20 July 2026 and is on appeal to the Ninth Circuit. — [Davis Wright Tremaine](https://www.dwt.com/blogs/artificial-intelligence-law-advisor/2025/06/courts-find-fair-use-in-gen-ai-training); [IPWatchdog](https://ipwatchdog.com/2025/12/23/copyright-ai-collide-three-key-decisions-ai-training-copyrighted-content-2025/); [AI Vortex guide](https://www.aivortex.io/legal/guides/ai-copyright-training-data-2026-landscape/)
- Kadrey v. Meta (N.D. Cal., June 2025): fair use on that record, with the judge indicating a better market-harm record could change the result. — [Davis Wright Tremaine](https://www.dwt.com/blogs/artificial-intelligence-law-advisor/2025/06/courts-find-fair-use-in-gen-ai-training); [White & Case](https://www.whitecase.com/insight-alert/two-california-district-judges-rule-using-books-train-ai-fair-use)
- Thomson Reuters v. ROSS: the Third Circuit ruled on 29 September 2026, the first federal appellate decision on fair use in AI training, finding factors one, three and four against ROSS. The tool was a non-generative legal search product, the court distinguished generative-AI arguments, and commentators say the generative question stays open. ROSS's counsel said it will seek further review. — [Ballard Spahr](https://www.ballardspahr.com/insights/alerts-and-articles/2026/10/third-circuit-addresses-fair-use-in-ai-training-but-leaves-generative-ai-questions-unresolved); [Courthouse News](https://www.courthousenews.com/ai-training-of-copyrighted-material-not-fair-use-third-circuit/)
- Commentators note that even where training is transformative, tainted sourcing can create liability. — [IPWatchdog](https://ipwatchdog.com/2025/12/23/copyright-ai-collide-three-key-decisions-ai-training-copyrighted-content-2025/)

European Union
- Under Article 4 of the DSM Directive, commercial text and data mining is allowed unless rights are reserved, and for online content the reservation must be machine-readable. The GPAI Code of Practice requires providers to identify and comply with machine-readable reservations. — [Reed Smith](https://www.reedsmith.com/articles/entertainment-media-guide-to-ai-three-years-on/text-data-mining-in-the-eu/); [SCL](https://www.scl.org/european-commission-consults-on-protocols-for-reserving-rights-from-text-and-data-mining-under-the-ai-act-and-the-gpai-code-of-practice/)
- Kneschke v. LAION: the Hamburg Regional Court (September 2024) held dataset creation fell under the research mining exception; an appellate ruling dated December 2025 found natural-language opt-outs were not shown to be machine-readable at the 2021 download date. Commentators say it tells little about what counts today. — [Kluwer Copyright Blog](https://legalblogs.wolterskluwer.com/copyright-blog/laion-round-2-machine-readable-but-still-not-actionable-the-lack-of-progress-on-tdm-opt-outs-part-2/); [Open Future](https://openfuture.eu/blog/laion-round-2-machine-readable-but-still-not-actionable/)
- The Commission consulted in late 2025 and early 2026 on a list of accepted machine-readable opt-out protocols, to be reviewed at least every two years. — [SCL](https://www.scl.org/european-commission-consults-on-protocols-for-reserving-rights-from-text-and-data-mining-under-the-ai-act-and-the-gpai-code-of-practice/); [CEPIC](https://www.cepic.org/post/european-commission-launches-stakeholder-consultation-on-ai-act-opt-out-protocols-for-text-and-data-mining)

Where the law is unsettled
- Whether generative training is fair use at the appellate level; how market harm is weighed (Bartz and Kadrey differ); whether a model or its outputs are adaptations of training works, which decides whether ShareAlike reaches weights; what counts as a machine-readable opt-out in the EU. — [Global Legal Post](https://www.globallegalpost.com/news/anthropic-meta-fair-use-rulings-in-ai-training-expose-judicial-split-on-market-harms-1365503569); [CC](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/); [Kluwer Copyright Blog](https://legalblogs.wolterskluwer.com/copyright-blog/laion-round-2-machine-readable-but-still-not-actionable-the-lack-of-progress-on-tdm-opt-outs-part-2/)

### Inferences
- The conservative ("overcompliance") reading for a released adapter: public domain, CC0 and CC BY sources with a source list are clean; CC BY-SA would suggest releasing weights under the same license; NC sources fit only a non-commercial project; ND sources should be left out.
- Consent from the rights holder (as the project has for its current author) sidesteps most of this and is the strongest basis for a single-author or single-publisher corpus.
- Honoring opt-out signals and listing sources is a norms matter even where not legally required.

### Gaps
- I did not read the CC primer PDF, the court opinions or the current CC signals page; the status of CC signals after December 2025 is unconfirmed.
- No 2026 result was found for New York Times v. OpenAI or Getty v. Stability.
- Whether the Commission published its final opt-out protocol list is unconfirmed.
- Dates in the Third Circuit and Bartz summaries vary across secondary sources; check dockets.

## 7. How to evaluate "preferred over generic AI writing" cheaply and honestly

### Takeaway
Use blind, randomized pairwise human judgments on the same content as the primary metric, with a named reader pool and a pre-set sample size. LLM judges favor low-perplexity, familiar text even without knowing whose it is, so they are biased toward the baseline the project wants to beat. Detector and slop scores are useful diagnostics for style shift and are not evidence of reader preference.

### Cited Findings

Human designs
- [PP] Chakrabarty et al. used blind pairwise comparisons on matched content (3,840 judgments from 28 experts and 131 lay readers) and analyzed odds ratios. Expert agreement was moderate (Fleiss' kappa 0.41-0.67) and lay agreement low (0.07-0.22). — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- [PP] Labels drive preference: in a label-swap design, raters favored whichever text was tagged human. — [arXiv 2410.03723](https://arxiv.org/pdf/2410.03723v2.pdf)
- [PP] Subjective ratings and comprehension diverge for plain-language summaries (n = 150), and automated metrics did not track human judgment. — [arXiv 2505.10409](https://arxiv.org/abs/2505.10409v1)
- [PR] Frequent LLM users are far more sensitive to AI style than detectors or naive readers (1 error in 300 by majority of five). — [ACL Anthology 2025.acl-long.267](https://aclanthology.org/2025.acl-long.267)

LLM judges
- [PP] Wataoka et al.: GPT-4 shows significant self-preference in pairwise judging; judges rate lower-perplexity text higher, and the bias appears without the judge being told which text is its own. The authors attribute it to familiarity. — [arXiv 2410.21819](https://arxiv.org/html/2410.21819v1)
- [PP] "Beyond the Surface": larger models show less self-preference, and gold judgments are needed to measure it properly. Snippet-level. — [arXiv 2506.02592](https://arxiv.org/pdf/2506.02592)
- [PP] Pairwise LLM judging also has position bias; rubric-based judging has its own self-preference. Snippet-level. — [arXiv 2508.09724](https://arxiv.org/pdf/2508.09724); [arXiv 2604.06996](https://arxiv.org/pdf/2604.06996.pdf)

Detectors and slop metrics
- [PP] Pangram and GPTZero flagged 97% and 91% of prompted outputs and 3% and 0% of fine-tuned outputs; the Pangram score predicted expert preference only for prompted text, and that link vanished after fine-tuning. — [arXiv 2510.13939](https://arxiv.org/html/2510.13939v3)
- [PP] Detectors rate base-model continuations as human (97-99%), so they track post-training artifacts and context, not machine origin. — [arXiv 2605.19516](https://arxiv.org/html/2605.19516v1)
- [PP] A model can push a token-statistics detector below chance while a style-embedding detector still scores about 0.95 AUROC; the authors recommend judging over multiple samples per source (their detector-tuned model became detectable at 5 samples). — [arXiv 2505.14608](https://arxiv.org/html/2505.14608v2)
- Liang et al. (Patterns, 2023), via a secondary summary: detectors flagged 61.3% of non-native English essays as AI. Pangram's own report claims near-zero false positives on similar sets; that is first-party. — [The Batch](https://www.deeplearning.ai/the-batch/ai-detectors-find-the-devils-work/); [arXiv 2402.14873](https://arxiv.org/pdf/2402.14873)
- [WIKI] "Do not solely rely on artificial intelligence content detection tools." — [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [BLOG] Slop score is a fixed-list composite (60% words, 25% contrast frames, 15% trigrams), so it measures presence of known tells only. — [arXiv 2601.21169](https://arxiv.org/pdf/2601.21169); [sam-paech/slop-score](https://github.com/sam-paech/slop-score)

### Inferences
- Sample sizes (my calculation, normal approximation to a two-sided binomial test against 50%, alpha 0.05, power 80%, independent judgments): a true preference rate of 55% needs about 780 judgments; 60% about 195; 65% about 85; 70% about 47. "Clearly prefer" is best pre-registered as a threshold, for example the lower confidence bound above 50% with a point estimate of at least 60-65%. With 200 judgments, an observed 60% has a 95% interval of roughly 53-67%.
- Judgments from the same rater or same item are correlated, so the figures above are lower bounds. Spread judgments over at least 30-40 distinct source items and several raters, and analyze with a mixed-effects logistic model or a bootstrap over items, as the odds-ratio analysis in Chakrabarty et al. does.
- Minimum honest design: same content in both arms (quill restyle versus the base or a frontier model's draft of the same material), randomized left/right order, no labels, length-matched, raters drawn from the intended audience, a "which would you rather read" question plus a short reason, and a separate fidelity check (facts preserved) and comprehension probe on a subset.
- Report results separately for frequent LLM users and for general readers; the literature predicts different answers.
- If an LLM judge is used for cheap iteration, use a judge from a different model family than both arms, randomize position, run both orders, and calibrate against a few dozen human judgments. Expect it to favor the generic arm.
- Use detector score, slop score and Biber-feature rates against a human expository reference as development diagnostics only. Evaluate in aggregate over many outputs, since style differences that are invisible per document show up over 5-50 samples.
- Field free-text reasons from raters; they fill the evidence gap on what readers dislike.

### Gaps
- No validated LLM-judge protocol for expository style preference was found, and no measurement of how well any judge agrees with humans on this task.
- No independent 2025-2026 benchmark of detector false-positive rates was read directly; a 2026 preprint on non-native academic writing (arXiv 2608.26710) and a Chicago Booth evaluation were seen only by title or vendor citation.
- No source was found for typical inter-rater agreement on pairwise preference for informational text; the kappa values above are for literary excerpts.
