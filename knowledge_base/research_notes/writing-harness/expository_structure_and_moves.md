# Expository structure and typed moves: theory, corpora, and prior generation systems

Reading note on evidence status. Each bullet under "Cited Findings" was seen in a search result or fetched page this session; where the number came from a secondary summary and not the paper itself, the bullet says so. Things I know from background reading but did not re-verify are kept out of "Cited Findings" and listed under "Gaps" as "recalled, unverified", so the report writer can decide whether to check them.

## 1. Discourse theories usable as a plan representation

### Takeaway
RST is the only theory here with a long record as a *generation plan* (classical planners, then RSTGen in 2022), but its measured benefit in neural generation is "competitive", not a clear win, and one follow-up reports that RST-conditioning degrades n-gram quality against plain BART. The more robust lesson from the classical work (Moore and Paris) is that a plan needs to record the *intended effect on the reader* for each part, not only the rhetorical relation between parts, which is exactly what a typed "move" does.

### Cited Findings
- Moore and Paris (1993), Computational Linguistics 19(4):651-694, argue that a discourse model "must include information about the intended effect of individual parts of the text on the hearer, as well as how the parts relate to one another rhetorically", and present a text planner that records both and uses the recorded structure to answer follow-up questions. — [ACL Anthology J93-4004](https://aclanthology.org/J93-4004/)
- The 1989 precursor to that paper characterises earlier generators (McKeown 1985, McCoy 1985, Paris 1988) as using only rhetorical and attentional information and omitting intentional information; its rhetorical relations are taken from RST (Mann and Thompson 1987). — [ACL Anthology P89-1025](https://preview.aclanthology.org/fix_video/P89-1025.pdf)
- RSTGen (Adewoyin, Dutta and He, NAACL 2022) conditions a pretrained LM on an RST tree (nuclearity, relation labels, node positions) plus keyphrases; nuclearity and node position control structure, relations and keyphrases control semantics; a neural RST predictor can sample trees. Evaluated on argument generation and story generation, the authors report "competitive" performance, not a consistent gain. — [arXiv 2205.12590](https://arxiv.org/abs/2205.12590)
- An INLG 2024 follow-up that controls rhetorical structure at decode time (PPLM-style) notes that in existing RST-conditioned methods output quality "tends to deteriorate when compared to the baseline, the vanilla BART, as measured by n-gram overlap metrics such as BLEU". — [INLG 2024 main.40](https://aclanthology.org/2024.inlg-main.40.pdf)
- Xu, Li and Choi (ACL 2022) deliberately chose sentence-level *functional roles* over RST for long-form answers: RST relations relate adjacent units, whereas functional roles describe how information is organised with respect to the question. — [arXiv 2203.11048](https://arxiv.org/pdf/2203.11048.pdf)
- Meyer's framework identifies five top-level expository structures tied to content: description, sequence, compare/contrast, cause/effect, problem/solution; Meyer (1975) argued the top-level organisation shapes what readers remember. — [Shanahan on Literacy summary](https://shanahanonliteracy.com/blog/does-text-structure-instruction-improve-reading-comprehension)
- Teaching readers to use those structures has meta-analytic support: Hebert et al. (2016, J. Educational Psychology 108(5):609-629) and Pyle et al. (2017, Reading Research Quarterly 52(4):469-501). One evidence-map summary gives ES = 0.96 for students with or at risk of disabilities; I could not confirm which paper/subgroup that number belongs to. — [ASHA evidence map](https://apps.asha.org/EvidenceMaps/Articles/ArticleSummary/61fb58ef-54ff-4a0f-a6f3-ae318f6ea0d5)
- Kintsch-tradition evidence that coherence is reader-relative: McNamara, Kintsch, Songer and Kintsch (1996, Cognition and Instruction 14(1):1-43) wrote four versions of a text crossing local and global coherence; low-knowledge readers did better with the coherent version, high-knowledge readers did better with the minimally coherent one on bridging-inference, problem-solving and sorting measures. — [scilit record](https://scilit.com/publications/301a1d52e5db2c321b87abb1d565f76f); [BYU Editing Research summary](https://editingresearch.byu.edu/2022/11/23/how-less-clarity-could-improve-active-processing)
- Plan-then-write evidence that is not discourse-theoretic: Goldfarb-Tarrant et al. (2019) plan-write-revise is reported (via a later paper's related-work section) to give 10-50% quality gains in user studies; EIPE-text (2023) reports human-judged coherence +5.0% and relevance +13.3% from a refined tree-structured plan. Both are narrative, not expository. — [arXiv 2310.08185](https://arxiv.org/html/2310.08185)
- 2025 work comparing one-shot with plan-based long-form writing finds LLMs "often struggle to maintain consistency and provide deep insights" one-shot relative to plan-based writing. — [arXiv 2502.19103](https://arxiv.org/pdf/2502.19103v2)

### Inferences
- For a planner-realiser split, the well-supported representation is a flat or shallowly nested *sequence of typed moves with bound content* (functional roles), not a full RST tree. RST trees are expensive to produce, parsers are noisy, and the only direct neural test did not show a quality gain. RST/PDTB relation labels are more useful as an *evaluation* lens (see section 6) than as the plan.
- Meyer's five structures are best used one level up: as the "type" of a section (is this section a comparison, a causal account, a procedure?), which then constrains which moves appear.
- McNamara et al. (1996) implies the plan needs an explicit reader-knowledge parameter; the amount of restating and bridging should fall as assumed knowledge rises.

### Gaps
- Not searched or not found this session: Segmented Discourse Representation Theory in generation; Daneš' thematic progression and Halliday and Hasan's cohesion used as generation controls; given-new ordering as a controllable feature. I found no evidence either way that any of these has been used successfully to control neural generation.
- Recalled, unverified: McKeown's (1985) TEXT system used four schemas (identification, constituency, attributive, compare-and-contrast) built from rhetorical predicates; Hovy (1988-93) operationalised RST relations as plan operators; PDTB 3.0 has four top-level sense classes (Temporal, Contingency, Comparison, Expansion); Barzilay and Lapata's entity grid (2008) is the standard given-new style coherence model. None of these were checked against sources today.
- RSTGen's actual numeric deltas were not retrieved.

## 2. What makes instructional text effective (cognitive and educational research)

### Takeaway
Five text-level devices have meta-analytic support with moderate effects (roughly g = 0.4 to 0.55): worked examples, self-explanation prompts, signalling, refutation of misconceptions, and removing interesting-but-irrelevant material. All interact with prior knowledge, so "more scaffolding" is not monotonically better.

### Cited Findings
Established (meta-analyses):
- Worked examples: Barbieri et al. (2023, Educational Psychology Review), 43 articles, 55 studies, 181 effect sizes, mathematics only: average g = 0.48. Correct-only examples beat incorrect-only or mixed; adding self-explanation prompts to worked examples *reduced* the effect. Most studies are middle/high-school algebra and geometry. — [Springer, doi 10.1007/s10648-023-09745-1](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf); [Learning Scientists summary](https://www.learningscientists.org/blog/2024/1/25-1)
- Self-explanation prompts: Bisra et al. (2018), 64 reports, 69 effect sizes, g = 0.55; interrogative prompts g = 0.56 (36 studies), imperative prompts g = 0.40 (12 studies); most participants undergraduates. — [Bisra et al. PDF](https://www.Gwern.net/doc/psychology/spaced-repetition/2018-bisra.pdf); [TUM Clearing House table](https://www.clearinghouse.edu.tum.de/wp-content/uploads/2023/09/KR_25_ENG_Table.pdf)
- Signalling (headings, previews, emphasis, pointer phrases): Schneider, Beege, Nebel and Rey (2018, Educational Research Review 23:1-24), 103 studies, 12,201 participants; retention g+ = 0.53, transfer g+ = 0.33 (numbers from a secondary summary, not checked against the paper). Low-prior-knowledge learners benefit more. — [ACU summary](https://inspire.acu.edu.au/articles/signalling); [QIC umbrella summary](https://www.qic-wd.org/sites/default/files/Umbrella%20Summary%20-%20Signaling%20in%20Training%20111021.pdf)
- Refutation text (state the misconception, say it is wrong, explain why): Schroeder and Kucera (2022, Educational Psychology Review 34:957-987), 44 between-subjects comparisons, n = 3,869, g = 0.41. A 2025 meta-analysis (Danielson et al., Educational Psychologist; 71 articles, 294 effect sizes) also finds a consistent advantage with no moderator changing it. — [Springer, doi 10.1007/s10648-021-09656-z](https://link.springer.com/content/pdf/10.1007/s10648-021-09656-z.pdf); [NSF PAR copy](https://par.nsf.gov/servlets/purl/10629626)
- Seductive details: Sundararajan and Adesope (2020, Educational Psychology Review 32(3):707-734) find learners given interesting-but-irrelevant material score lower; worse when the detail sits next to relevant diagrams or is static. Coverage conflicts on scope: the university press release says 58 studies and 7,500+ students, a blog says 68 experiments. One summary says the harm is considerable in short lessons (under 5 minutes) and not significant in longer ones (over 10 minutes). — [WSU news](https://news.wsu.edu/2020/03/19/seductive-details-inhibit-learning/); [Learning and the Brain](https://www.learningandthebrain.com/blog/seductive-details-when-do-cool-stories-and-videos-interfere-with-learning/)
- Expertise reversal: Tetzlaff, Simonsmeier, Peters and Brod (2025, Learning and Instruction 98:102142) meta-analyse about 60 studies, 176 effect sizes, nearly 6,000 participants; techniques that help novices can hurt experts, and the effect grows with learner age (figures from a secondary summary). — [Learning and the Brain summary](https://www.learningandthebrain.com/blog/one-size-doesnt-fit-all-teaching-experts-and-novices/)
- Text-structure awareness: see Hebert et al. (2016) and Pyle et al. (2017) in section 1; instruction was reported as stronger when it attended to clue words (secondary source). — [Shanahan on Literacy](https://shanahanonliteracy.com/blog/does-text-structure-instruction-improve-reading-comprehension)

Single studies:
- Cohesion by knowledge interaction: McNamara et al. (1996), described in section 1; a later McNamara study with fourth graders reports the same "reverse cohesion effect" for knowledgeable children. — [IEJEE](https://iejee.com/index.php/IEJEE/article/view/222)
- LLM explanations: a pre-registered experiment with 1,200 participants found LLM-generated explanations improved learning over seeing only the correct answer, most for people who attempted the problem first. — [Stanford SCALE repository entry](https://scale.stanford.edu/ai/repository/math-education-large-language-models-peril-or-promise)

### Inferences
Which features are countable in a text (my classification; the counting methods are proposals, not validated instruments):

| Device | Countable as | Evidence strength |
|---|---|---|
| Worked example present, fully worked, correct | count of example blocks; steps per example | meta-analysis, maths only |
| Self-explanation / "why" prompt | count of reader-directed questions | meta-analysis; but negative moderator when stacked on worked examples |
| Signalling | headings, previews, summaries, enumerators, pointer phrases per 1,000 words | meta-analysis (multimedia; text-only subset not isolated here) |
| Refutation | misconception statement + explicit negation + explanation triple | two meta-analyses |
| Seductive detail | sentences not bound to any plan item | meta-analysis; needs a plan to count against |
| Define before use | term's first use precedes its definition (order violation count) | no effect size found |
| Cohesion level | argument/noun overlap between adjacent sentences, causal connectives | single studies; reader-dependent |

- The seductive-details result gives a direct operational rule for a planner-realiser system: every realised sentence should trace to a plan item, and anecdote/colour that carries no plan content should be treated as a cost, particularly in short pieces.
- The Barbieri moderator (self-explanation prompts reduce the worked-example effect) is a caution against piling devices on top of one another.

### Gaps
- No meta-analytic effect size was found this session for: defining terms before use; examples-before versus examples-after definitions; concreteness fading; analogy in text; advance organisers.
- The overall g for seductive details was not confirmed from the paper.
- Recalled, unverified: advance organisers have a small average effect (Luiten et al. 1980, about 0.2); case comparison/analogy has d about 0.5 (Alfieri et al. 2013); instructional explanations added to worked examples have a very small overall effect (Wittwer and Renkl 2010, d about 0.16); the seductive-details overall effect is about g = -0.33; Mayer's coherence and signalling principles; Lorch's signalling reviews. Check all before citing.
- Almost all of this evidence is from short lessons, multimedia, or maths; evidence for long-form prose textbooks specifically is thin.

## 3. Annotation schemes and corpora for moves in explanatory or instructional text

### Takeaway
Labelled data exists for dialogue explanation moves (5 Levels), sentence roles in explanatory answers (LFQA discourse), definitions in textbooks (DEFT) and concept prerequisites (LectureBank), but I found no corpus of sentence-level pedagogical moves annotated on textbooks. Agreement on move labels is only moderate (kappa about 0.4 to 0.5), which bounds how reliable any move classifier or judge will be.

### Cited Findings
- "5 Levels" corpus (Wachsmuth and Alshomary, COLING 2022): 65 transcribed dialogues from the Wired series, 13 topics x 5 explainee levels (child to colleague), 1,550 turns, each labelled by five professionals for topic, dialogue act and explanation move. Ten moves: test understanding, test prior knowledge, provide explanation, request explanation, signal understanding, signal non-understanding, provide feedback, provide assessment, provide extra info, other. Fleiss kappa: moves 0.43, dialogue acts 0.49, topic 0.35. — [arXiv 2209.02508](https://arxiv.org/abs/2209.02508); [ACL Anthology](https://aclanthology.org/2022.coling-1.27/)
- Move frequencies in 5 Levels: provide explanation 43.8% of turns (51.8% of explainer turns); provide feedback 18.4%; request explanation 9.2%; signal understanding 9.1%; test prior knowledge 7.2% overall but 14.1% of explainer turns; test understanding 7.1% of explainer turns; provide extra info 3.1%. Across levels, feedback falls from 25.6% (child) to 9.5% (colleague), and turns on related topics rise from 8.4% to 30.9%. BERT with sequence context reaches macro-F1 0.43 on moves (0.84 on "provide explanation", 0.08 on "extra info"). — [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2209.02508)
- LFQA discourse (Xu, Li and Choi, ACL 2022): six sentence-level roles (Answer-Summary, Answer, Example, Auxiliary Information, Organizational sentence, Miscellaneous); about 3.9k sentences in 640 answer paragraphs from ELI5 (411 paragraphs, 2,670 sentences), WebGPT (98, 551) and Natural Questions (131, 695). Public on Hugging Face (`fangyuan/lfqa_discourse`). — [arXiv 2203.11048](https://arxiv.org/pdf/2203.11048.pdf); [project page](https://cs.utexas.edu/~fxu/lfqa_discourse)
- LFQA role distribution (Table 3): ELI5 has 13% Example sentences, 18% Auxiliary, 1% Organizational, 10% Miscellaneous, and the two Answer roles at 30% and 28%; NQ (Wikipedia-derived) has 39% Auxiliary and 5% Example; WebGPT 26% Auxiliary, 8% Example, 3% Organizational. Role agreement among student annotators was "modest to high" and rose to Fleiss kappa 0.70 after collapsing the commonly confused Answer/Summary/Auxiliary distinctions. (I read the table from extracted PDF text; which of 30%/28% is Answer versus Summary was not confirmed.) — [arXiv 2203.11048](https://arxiv.org/pdf/2203.11048.pdf)
- DEFT (Spala et al., LAW 2019): definition annotation over open textbooks (biology, history, physics, psychology, economics, sociology, government; CC BY 4.0) and SEC contracts; about 28% of the textbook sentences in the corpus contain definitions versus 22% of contract sentences. Used for SemEval-2020 Task 6 (DeftEval), which used textbook sentences only, with sentence classification, sequence labelling and relation extraction subtasks. — [ACL Anthology W19-4015](https://aclanthology.org/W19-4015/); [SemEval task paper, arXiv 2008.13694](https://arxiv.org/pdf/2008.13694)
- LectureBank (Li et al., AAAI 2019): 1,352 English lecture files plus prerequisite relations over 208 manually labelled NLP concepts (a separate 305-topic taxonomy organises the files); each relation was labelled by a single annotator. LectureBankCD extends to computer vision and bioinformatics, with 1,717 NLP resources and 322 concepts. — [arXiv 1811.12181](https://arxiv.org/pdf/1811.12181); [arXiv 2105.03505](https://ar5iv.labs.arxiv.org/html/2105.03505)
- Document-level pedagogical roles (Sheng et al., BEA 2017): first corpus labelling whole documents (ACL Anthology papers, not textbooks) with roles such as Tutorial. — [ACL Anthology W17-5012](https://preview.aclanthology.org/menus/W17-5012/)
- Student dialogue discourse (Mim et al., 2025): turn-level annotation of knowledge-construction versus task-production talk; GPT-3.5 and Llama-3.1 perform "suboptimally" at predicting the labels. — [arXiv 2511.20547](https://arxiv.org/abs/2511.20547)
- A targeted search for sentence-level pedagogical role annotation of science textbooks, with frequency counts, returned no such corpus. — [search result set, nearest hit: TIB Pedagogical Role Annotation Dataset](https://service.tib.eu/ldmservice/dataset/pedagogical-role-annotation-dataset)

### Inferences
- A textbook-move evaluation set will probably have to be built in-house. The cheapest starting point is the LFQA six-role scheme extended with Definition (DEFT gives a detector and training data) and Worked Example.
- Expect human agreement near kappa 0.4 to 0.5 on fine move labels and about 0.7 on coarse ones; design the move inventory so that the distinctions the system depends on are the coarse, high-agreement ones (core statement versus example versus background versus organisation).
- Define-before-use can be checked mechanically by combining a definition detector with first-mention order; LectureBank-style prerequisite graphs supply ordering constraints across concepts but only for NLP/CV/bioinformatics.

### Gaps
- The DEFT sentence total for textbooks was truncated in the result ("2,443 sen..."); the 28% rate describes the annotated sample, which may have been selected for definition density, so it should not be read as a base rate for textbooks.
- Not found or not searched: Swales-style move analyses of textbooks and lectures; science-communication move studies; AL-CPL and other textbook prerequisite datasets; the "InstruX" nine teaching acts (a search snippet mentioned them but the page I fetched was a different paper, so nothing is cited).
- Recalled, unverified: WCL definition corpus (Navigli and Velardi 2010); a later ELI5-based explanation-dialogue corpus by Alshomary et al. (2024).

## 4. Readability and explanation-quality measures beyond formulas

### Takeaway
Coh-Metrix's five "easability" components are the standard multi-level alternative to readability formulas, but I found no explanation-quality metric validated against learning outcomes; the only outcome-linked text property with experimental support is cohesion, and its benefit reverses for knowledgeable readers.

### Cited Findings
- Graesser, McNamara and Kulikowich (2011) present five Coh-Metrix factors that account for most variance across grade levels and text categories: narrativity, syntactic simplicity, word concreteness, referential cohesion, and causal ("deep") cohesion. — [Penn State record](https://pure.psu.edu/en/publications/coh-metrix-providing-multilevel-analyses-of-text-characteristics/)
- Referential cohesion is content-word/co-reference overlap between sentences; deep cohesion is the density of causal, intentional and other connectives that support the situation model. — [GSU Coh-Metrix overview](https://sites.gsu.edu/csal/readibillity/coh-metrix-advanced-overview)
- A secondary source reports the underlying PCA gave eight components (the five above plus verb, logical and temporal cohesion). — [Dergipark article](https://dergipark.org.tr/tr/download/article-file/375100)
- Applied to explanations (weak evidence, N = 24 texts, high-school journal): ChatGPT (GPT-5 free tier) maths explanations had the lowest syntactic simplicity (means 8.75 to 19.25 on a 0-100 scale) versus Khan Academy transcripts (78.0); the standard textbook had the highest word concreteness (81.5); Khan Academy the highest narrativity (87.5). Authors note length confounds and that the tool was not built for maths prose. — [NHSJS 2026](https://nhsjs.com/2026/comparing-text-only-linguistic-profiles-of-math-explanations-across-khan-academy-chatgpt-and-textbooks-a-descriptive-case-study-of-four-high-school-topics/)
- Human raters outperform LLM raters for instructional quality: in the Instructional Agents study (2025), outputs scored against the Quality Matters rubric got "more sensitive and discriminative" judgments from human experts, while LLM reviewers gave mostly moderate scores. — [review of arXiv 2508.19611](https://www.themoonlight.io/review/instructional-agents-llm-agents-on-automated-course-material-generation-for-teaching-faculties)
- Agreement on the discourse roles of model-generated answers is lower than on human answers (Fleiss kappa 0.31 for machine text in Xu et al.), i.e. the structure of machine text is harder for people to label. — [arXiv 2203.11048](https://arxiv.org/pdf/2203.11048.pdf)

### Inferences
- Coh-Metrix components are usable as descriptive checks (is the output's cohesion and syntactic simplicity in the band of the target textbooks?) but not as an objective to maximise, given the reverse-cohesion effect.
- A plan gives a cheaper quality measure than any of these: plan coverage (each move realised), plan fidelity (no unplanned content) and order violations are directly countable.

### Gaps
- No source found for an automatic explanation-quality measure validated against learner outcomes. Neural coherence models (entity grid and successors) were not searched.
- The Coh-Metrix behavioural validation studies themselves were not retrieved.

## 5. Prior generation systems built on such structure

### Takeaway
Classical systems established the plan-of-typed-acts architecture; LLM-era educational systems mostly impose coarse pipeline stages (plan, outline, draft) and report teacher ratings or time savings, not learning outcomes. I found no study that manipulates pedagogical move structure in generated text and measures learning.

### Cited Findings
- Classical: Moore and Paris's planner (1993) built explanations top-down from communicative goals, recording intention and rhetorical relation at each node so the system could answer follow-ups and re-explain. — [ACL Anthology J93-4004](https://aclanthology.org/J93-4004/)
- RSTGen (2022): explicit RST tree as control input; competitive on argument and story generation. — [arXiv 2205.12590](https://arxiv.org/abs/2205.12590)
- Instructional Agents (arXiv 2508.19611, 2025): multi-agent pipeline producing syllabi, lecture scripts, slides and assessments; evaluated against the Quality Matters rubric by experts and LLMs. — [review](https://www.themoonlight.io/review/instructional-agents-llm-agents-on-automated-course-material-generation-for-teaching-faculties)
- POSED (ASEE paper): Plan, Outline, Sources, Evaluation, Draft with human approval gates; reports instructor preparation falling from about 10-20 hours per lecture to about 2 hours of review, under $1.50 AI cost per lecture. Self-reported, no learning measure. — [ASEE PDF](https://nemo.asee.org/public/conferences/374/papers/50304/download)
- Lesson plans for high-school physics (arXiv 2510.19866, 2025): five LLMs crossed with prompt frameworks; the prompt framework had the strongest effect on factual accuracy and pedagogical completeness. — [arXiv 2510.19866](https://www.arxiv.org/pdf/2510.19866)
- LLM-drafted line-by-line explanations of Java worked examples for instructor editing, compared with expert and student explanations in a feasibility study. — [NSF PAR 10613692](https://par.nsf.gov/biblio/10613692-engaging-llm-explain-worked-examples-java-programming-prompt-engineering-feasibility-study)
- Personalised LLM worked examples by skill level (Utrecht master's thesis): educators rated them highly, but the controlled comparison against generic examples showed no conclusive learning gain (small sample). — [Utrecht thesis](https://studenttheses.uu.nl/handle/20.500.12932/49888)
- LLM-generated retrieval-practice questions in two data-science courses (about 60 students): 89% versus 73% quiz accuracy; authors caution about variable question quality. — [arXiv 2507.05629](https://arxiv.org/html/2507.05629v1)
- LLM explanations versus answer-only feedback, 1,200 participants, pre-registered: explanations improved learning. — [Stanford SCALE](https://scale.stanford.edu/ai/repository/math-education-large-language-models-peril-or-promise)

### Inferences
- The proposed backbone (strong model emits ordered typed moves with bound details, second model realises) is closer to Moore and Paris than to anything in the recent LLM education literature I found; the recent work plans at section/outline granularity, not move granularity.
- What structure has demonstrably bought so far: follow-up/repair ability (classical), instructor time (POSED), and prompt-framework effects on completeness. Gains in learner outcomes from structure are unproven.

### Gaps
- No evidence located for: Reiter's instructional-text work; ITS explanation generators with measured results; LLM textbook-generation papers with teacher ratings of move-level structure; any randomised test of move planning.
- Recalled, unverified: STORM (Shao et al. 2024, arXiv 2402.14207), outline-driven Wikipedia-style writing judged more organised by experienced editors; Wang et al. (NAACL 2024, "Bridging the novice-expert gap"), where conditioning tutor responses on expert-annotated strategy and intention labels made them markedly more preferred. Both are the closest LLM-era analogues to move-conditioned realisation and worth checking.

## 6. Structural differences between human expert and LLM expository prose

### Takeaway
Across several studies LLM text shows flatter, more paratactic discourse structure with heavy reliance on Elaboration-type relations, less structural variability, and fewer hedges; evidence on connectives is mixed and none of the studies I found is on textbook exposition specifically.

### Cited Findings
- A 2026 preprint reports human writers build deeper rhetorical hierarchies while LLMs produce flatter structures relying on surface relations such as Elaboration and Cause; a human-written structure persists after LLM polishing. — [arXiv 2604.04932](https://arxiv.org/pdf/2604.04932)
- Fomsgaard, Pastor and Dias (ACL 2026): LLM argumentative essays are more generic than student essays, and higher genericity correlates with less structured, paratactic discourse. — [ACL 2026 long.1521](https://aclanthology.org/2026.acl-long.1521.pdf)
- Kim et al. (ACL 2024, "Threads of Subtlety"): RST-derived discourse motifs show human texts have more structural variability; detectors built on such signatures drop sharply out of domain. — [arXiv 2402.10586](https://arxiv.org/abs/2402.10586)
- GPT-2-era baseline (Wey et al.): 445 human and machine documents, about 27,000 clauses annotated; machine text matched human clause types but had shorter, lower-quality coherence relations. — [eScholarship](https://escholarship.org/uc/item/2276k59j)
- Hedging: in a persuasion study, humans used hedging terms roughly 40% more often than LLMs, and LLMs used more maximisers. — [arXiv 2505.09662](https://arxiv.org/pdf/2505.09662)
- Discourse markers: Herbold et al. found GPT-4 essays use significantly fewer discourse markers than human essays (GPT-3.5 did not differ). A metadiscourse study instead finds ChatGPT leans on transitions and endophoric markers for structure while students use more stance and engagement markers. These partly conflict. — [arXiv 2304.14276](https://arxiv.org/pdf/2304.14276); [UEA repository](https://ueaeprints.uea.ac.uk/id/eprint/99123)
- In explanatory answers, human ELI5 writers spend 13% of sentences on examples and use devices such as hypophora (posing then answering a question) as organisational sentences; role structure of machine-generated answers was harder for annotators to agree on (kappa 0.31). — [arXiv 2203.11048](https://arxiv.org/pdf/2203.11048.pdf)
- Maths explanations (N = 24, descriptive only): ChatGPT prose was far less syntactically simple than textbook or Khan Academy prose and clustered separately from both. — [NHSJS 2026](https://nhsjs.com/2026/comparing-text-only-linguistic-profiles-of-math-explanations-across-khan-academy-chatgpt-and-textbooks-a-descriptive-case-study-of-four-high-school-topics/)

### Inferences
- The consistent finding (flat, Elaboration-heavy, low variability) is the kind of defect an explicit move plan could address, since a plan forces non-elaborative moves (contrast, consequence, example, refutation) and can vary their order between sections. This is a hypothesis; none of the cited studies tested it.
- Useful structural diagnostics for comparing output with target textbooks: relation-type distribution from a discourse parser, tree depth, share of example sentences, hedge rate, question rate.

### Gaps
- No study found comparing human and LLM text on textbook or instructional explanations at the level of examples, signposting, reader address, question use, sentence-length variation or information ordering. The essay and persuasion studies may not transfer.
- The two 2026 papers were seen only as search snippets; details unverified.

## 7. Practical guidance: a small move set and its frequencies

### Takeaway
No published source gives a validated 6-to-12 move inventory for textbook prose with frequencies in real textbooks. The nearest empirical anchors are the LFQA six roles, the 5 Levels explainer moves and DEFT's definition rate; a move set has to be assembled from these and then counted on the target textbooks.

### Cited Findings
- In explanatory answers, six roles covered over 90% of sentences (Miscellaneous under 10%); examples were 5 to 13% of sentences, background/auxiliary 18 to 39%, organisational sentences 0.4 to 3%. — [arXiv 2203.11048](https://arxiv.org/pdf/2203.11048.pdf)
- Expert explainers in dialogue spend about half their turns providing explanation, about 14% testing prior knowledge and about 7% testing understanding. — [ar5iv 2209.02508](https://ar5iv.labs.arxiv.org/html/2209.02508)
- About 28% of sentences in DEFT's textbook sample contain a definition. — [W19-4015 PDF](https://preview.aclanthology.org/author-url/W19-4015.pdf)
- Devices with meta-analytic support that map onto moves: worked example (g = 0.48), self-explanation prompt (g = 0.55), signalling (g+ = 0.53 retention), refutation (g = 0.41). — [Barbieri 2023](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf); [Bisra 2018](https://www.Gwern.net/doc/psychology/spaced-repetition/2018-bisra.pdf); [signalling summary](https://inspire.acu.edu.au/articles/signalling); [Schroeder and Kucera 2022](https://link.springer.com/content/pdf/10.1007/s10648-021-09656-z.pdf)

### Inferences
A candidate ten-move inventory, with the source that motivates each (my synthesis, not a published scheme):

| Move | Bound details | Anchor |
|---|---|---|
| Motivate / pose the question | the problem or puzzle | LFQA organisational sentence (hypophora); 5 Levels "test prior knowledge" |
| Preview / signpost | what follows, in order | signalling meta-analysis |
| State the core claim or definition | term, definiens | LFQA Answer-Summary; DEFT |
| Restate / elaborate | the same claim in other words | LFQA Answer |
| Give background / prerequisite | prior concept needed | LFQA Auxiliary; prerequisite graphs |
| Give an example or worked example | case, steps, result | LFQA Example; worked-example effect |
| Contrast with a near neighbour | two terms, the distinguishing feature | Meyer comparison structure |
| Refute a misconception | the wrong belief, why it is wrong | refutation-text meta-analyses |
| State a consequence / cause | what follows and why | Meyer causation; deep cohesion |
| Prompt or check the reader / summarise | a question or recap | self-explanation prompts; 5 Levels "test understanding" |

- Rough expected shares, extrapolated from explanatory answers and therefore weak: core statements plus restatement about half of sentences; background a fifth to a third; examples around a tenth; organisational and reader-directed sentences a few percent. Real textbooks likely have more definitions and worked examples than ELI5 answers.
- Because fine move labels reach only moderate human agreement, keep the inventory near ten and make each move carry bound content, so that realisation can be checked by content coverage even where the label is debatable.

### Gaps
- Move frequencies in actual textbooks: no source found. This has to be measured on the target corpus.
- Whether a ten-move inventory "covers most" textbook exposition is untested; the over-90% coverage figure is for six roles on short answers, not chapters.
