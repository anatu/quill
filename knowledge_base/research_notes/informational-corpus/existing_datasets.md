# Existing ML datasets of human-written explanatory text as candidate training corpora

Research date: 13 November 2026. Nothing was downloaded; all findings come from dataset cards, papers and licence pages. "Card" means the Hugging Face dataset card. Word totals marked "(computed)" are my multiplication of a cited count by a cited mean length, not a published figure.

Pages I could not open directly (the fetcher was blocked): `stackoverflow.com/help/licensing`, `meta.stackexchange.com`, `redditinc.com/policies/data-api-terms`, `wikihow.com/wikiHow:Terms-of-Use`, `plos.org/terms-of-use`, and the Wayback Machine. Claims about those pages rest on secondary sources and are flagged where they appear.

## 1. Licence and provenance: does the card's licence match the source's licence?

### Takeaway
Only a minority of candidates have a card licence that matches a verifiable open source licence: the eLife/PLOS lay-summary sets (CC BY 4.0), the Common Pile subsets (per-document CC BY / CC BY-SA / public domain, audited by hand), Wikimedia-derived sets (CC BY-SA), and US government text (GovReport, BillSum, CRS). Most of the rest are either unlicensed scrapes with a permissive label on top (CNN/DailyMail "Apache-2.0", Paul Graham essays "MIT", RAID "MIT", MAGE "Apache-2.0", HC3 "CC BY-SA" over Reddit text) or carry a non-commercial or unknown licence (WikiHow, Multi-News, Blog Authorship Corpus, ELI5, XSum, Newsela).

### Cited Findings

**What CC conditions mean for training (Creative Commons' own guidance, May 2025)**
- CC says the licences "apply only when copyright permission is required"; BY, SA and ND are "triggered only when works or adaptations of works are publicly shared", while NC applies to "all uses requiring permission under copyright". — [Creative Commons, Using CC-licensed works for AI training](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- On NC: copying during training "must not be for commercial gain". On SA: "following the ShareAlike condition would require AI developers to use the same CC license as the original works" if models are shared publicly. On ND: following it "would require that ND-licensed content not be used as training data". On BY: attribution "could be a simple link to the source of the dataset used to train the model". — [Creative Commons, Using CC-licensed works for AI training](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- CC also states "AI training is often permitted by copyright" and "the CC license conditions have limited application to machine reuse". — [Creative Commons legal primer, 15 May 2025](https://creativecommons.org/2025/05/15/understanding-cc-licenses-and-ai-training-a-legal-primer/)
- Common Pile's standard for "open": the Open Knowledge Foundation definition; "CC NC (non-commercial) and ND (no derivatives) licenses are not considered open under this definition". It defines licence laundering as when "a copyrighted work is redistributed (typically by a non-rights holder) with an incorrect license". — [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)

**Lay-summary sets (match)**
- `tomasg25/scientific_lay_summarisation` card licence: "cc-by-4.0". — [HF card](https://huggingface.co/datasets/tomasg25/scientific_lay_summarisation)
- eLife's terms say journal content is "licensed under a Creative Commons Attribution license", with the footer "Subject to a Creative Commons Attribution license, except where otherwise noted", linking CC BY 4.0. — [eLife terms](https://elifesciences.org/terms)
- `BioLaySumm/BioLaySumm2025-eLife` has no licence field and an empty README. — [HF card](https://huggingface.co/datasets/BioLaySumm/BioLaySumm2025-eLife)
- `GEM/cochrane-simplification` card licence: "cc-by-4.0: Creative Commons Attribution 4.0 International". — [HF card](https://huggingface.co/datasets/GEM/cochrane-simplification). A search of its revision history showed another revision with a blank licence field, and Cochrane's own reuse terms were not found. — [HF revision](https://huggingface.co/datasets/GEM/cochrane-simplification/blob/refs%2Fpr%2F1/README.md)

**Common Pile (match, with per-document metadata)**
- Common Pile v0.1 is 8 TB of text from 30 sources; the authors included data "only ... from sources where we were confident" of the licence, excluded OpenAlex, YouTube Commons and the Hacker News Kaggle set for that reason, and "frequently resort to manual review by humans". Licence data was collected in late 2024. — [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)
- `common-pile/news`: "We scrape the news sites that publish content under CC BY or CC BY-SA according to opennewswire"; "Per-document license information is available in the `license` entry of the `metadata` field". Sites include 360info, Global Voices, SciDev.Net, Meduza, Africa is a Country, Alt News, Factly, Freedom of the Press Foundation and others. The card warns licence metadata may occasionally be inaccurate. — [HF card](https://huggingface.co/datasets/common-pile/news)
- `common-pile/stackexchange`: per-document licence in metadata, samples show CC BY-SA 3.0 or 4.0. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)
- `common-pile/libretexts`: sections kept only when the licence statement is public domain, "a CC BY, CC BY-SA, or the GNU Free Documentation License". — [HF card](https://huggingface.co/datasets/common-pile/libretexts)
- `common-pile/pressbooks`: English books listed as public domain, CC BY or CC BY-SA; the card warns of possible licence laundering in the metadata. — [HF card](https://huggingface.co/datasets/common-pile/pressbooks)
- `common-pile/wikimedia` and `wikimedia_filtered`: eight English Wikimedia wikis (Wikipedia, Wikinews, Wikibooks, Wikiquote, Wikisource, Wikiversity, Wikivoyage, Wiktionary), CC BY-SA, March 2025 dumps, with a `wiki` field in metadata. — [HF card](https://huggingface.co/datasets/common-pile/wikimedia_filtered)
- Global Voices source licence: CC BY 3.0 ("Creative Commons Attribution-Only license"); republication should link the original and name the author; third-party media excluded. — [Global Voices attribution policy](https://globalvoices.org/about/global-voices-attribution-policy/)
- 360info source licence: content is "licensed under a Creative Commons Attribution 4.0 International license"; academics write, professional editors turn it into plain language. — [360info about](https://360info.org/about-us/)

**Common Corpus (PleIAs)**
- "All data in Common Corpus are either uncopyrighted or freely licensed"; per-document `license` field (635 distinct values in the preview). — [HF card](https://huggingface.co/datasets/PleIAs/common_corpus)

**Wikipedia-derived (match, version labels stale)**
- Wikipedia text is licensed under "the Creative Commons Attribution-ShareAlike 4.0 International License" and the GFDL. — [Wikipedia:Copyrights](https://en.wikipedia.org/wiki/Wikipedia:Copyrights)
- `wikimedia/wikipedia` card licence: "cc-by-sa-3.0" and "gfdl" (dump 2023-11-01). — [HF card](https://huggingface.co/datasets/wikimedia/wikipedia)
- `Salesforce/wikitext` licence field: cc-by-sa-3.0 and gfdl, while its licensing section says CC BY-SA 4.0. — [HF card](https://huggingface.co/datasets/Salesforce/wikitext)
- `chaojiang06/wiki_auto`: "The dataset is not licensed by itself, but the source Wikipedia data is under a `cc-by-sa-3.0` license." — [HF card](https://huggingface.co/datasets/chaojiang06/wiki_auto)
- Wikinews: CC BY 4.0 for material after 16 December 2024, CC BY 2.5 from 25 September 2005 to 16 December 2024, public domain before that. — [Wikinews:Copyright](https://en.wikinews.org/wiki/Wikinews:Copyright)

**US government text (match)**
- EveryCRSReport: CRS reports, as US Government works, are not subject to copyright in the United States; a report and its metadata "may be reproduced and distributed in its entirety without permission". Reports may contain third-party copyrighted images or material. — [EveryCRSReport download page](https://www.everycrsreport.com/download.html)
- `FiscalNote/billsum` card licence "cc0-1.0"; US bills collected from Govinfo. — [HF card](https://huggingface.co/datasets/FiscalNote/billsum)
- `ccdv/govreport-summarization` has no licence field. — [HF card](https://huggingface.co/datasets/ccdv/govreport-summarization)
- VOA: "All text, audio and video material produced exclusively by the Voice of America is in the public domain"; AP, AFP and Reuters material on the site is excluded and may not be copied. — [VOA terms](https://www.voanews.com/p/5338.html)

**Project Gutenberg-derived**
- `deepmind/pg19`: "The dataset is licensed under Apache License, Version 2.0"; books "published before 1919". — [HF card](https://huggingface.co/datasets/deepmind/pg19)
- Standardized Project Gutenberg Corpus Zenodo record: "Creative Commons Attribution 4.0 International". — [Zenodo](https://zenodo.org/records/2422561)

**Stack Exchange (source licence open; access terms changed)**
- Per the official licensing page as reported in search results: content before 2011-04-08 is CC BY-SA 2.5; 2011-04-08 up to 2018-05-02 is CC BY-SA 3.0; since 2 May 2018 it is CC BY-SA 4.0. I could not open the page itself. — [Stack Overflow licensing page (not fetched)](https://stackoverflow.com/help/licensing); [Wikipedia: Stack Exchange](https://en.wikipedia.org/wiki/Stack_Exchange)
- July 2024: Stack Exchange stopped uploading dumps to the Internet Archive and moved them to a profile download whose terms say a recipient who trains an LLM on the dump can be denied future access. Critics argued this contradicts CC BY-SA's ban on additional restrictions. — [DevClass, 30 July 2024](https://www.devclass.com/development/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-critics-complain-this-contradicts-license/1625192); [heise](https://heise.de/-9823083)
- Common Pile used "community uploaded dumps from December of 2024" and filled gaps from the last official July 2024 dumps. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)

**Reddit-derived (no clean licence)**
- The original ELI5 card: licence "unknown"; status "hinges on the legal status of the Pushshift.io data which is unclear". — [HF card](https://huggingface.co/datasets/defunct-datasets/eli5)
- `rexarski/eli5_category`: licence "unknown", same Pushshift statement. — [HF card](https://huggingface.co/datasets/rexarski/eli5_category)
- Secondary reports of Reddit's 2023 Data API Terms: using User Content to train a machine learning or AI model without rightsholders' express permission is prohibited. I did not retrieve the clause text. — [The Register, 18 April 2023](https://www.theregister.com/2023/04/18/reddit_charging_ai_api/); [The Decoder](https://the-decoder.com/reddit-ends-its-role-as-a-free-ai-training-data-goldmine/)
- Reddit is litigating scraping: on 31 July 2026 an S.D.N.Y. judge largely denied Perplexity's and SerpApi's motions to dismiss. — [MediaPost](https://www.mediapost.com/publications/article/416950/reddit-can-proceed-with-scraping-claims-against-pe.html); [Law360](https://www.law360.com/articles/2508228/reddit-ai-data-scraping-case-mostly-survives-dismissal)

**WikiHow (NC-SA, actively enforced)**
- `gursi26/wikihow-cleaned` card licence "cc-by-nc-sa-3.0"; access is disabled after a DMCA notice. — [HF card](https://huggingface.co/datasets/gursi26/wikihow-cleaned)
- The DMCA notice came from representatives of wikiHow, Inc., relayed by Hugging Face on 24 August (URL path indicates 2026), with a 7-day deadline before the whole repo is disabled. — [HF discussion](https://huggingface.co/datasets/gursi26/wikihow-cleaned/discussions/1)
- wikiHow sued OpenAI in New York federal court over scraping of more than 11,000 articles. — [IPWatchdog, 25 August 2026](https://ipwatchdog.com/2026/08/25/wikihow-files-lawsuit-against-openai-over-chatgpts-use-of-its-how-to-library/)
- The M4 paper lists WikiHow's licence as "CC-BY-NC-SA". — [M4 paper](https://ar5iv.labs.arxiv.org/html/2305.14902)

**News summarization (mismatch or restricted)**
- `abisee/cnn_dailymail`: "The CNN / Daily Mail dataset version 1.0.0 is released under the Apache-2.0 License." — [HF card](https://huggingface.co/datasets/abisee/cnn_dailymail)
- `EdinburghNLP/xsum`: licence "unknown"; Licensing Information "[More Information Needed]"; source is BBC articles. — [HF card](https://huggingface.co/datasets/EdinburghNLP/xsum)
- `alexfabbri/multi_news`: licence "other"; "The Dataset is intended for non-commercial research and educational purposes only"; text from newser.com. — [HF card](https://huggingface.co/datasets/alexfabbri/multi_news)
- Newsela: "Currently, we only grant access to academically-affiliated researchers whose projects are likely to lead to a publication", with an NDA. — [Newsela data page](https://newsela.com/legal/data)

**AI-detection sets (card licences cover a mixture of sources)**
- HC3: licence field "cc-by-sa-4.0", with the note that where a source "has a specific license which is stricter than CC-BY-SA, our products follow the same". Its largest split is reddit_eli5. — [HF card](https://huggingface.co/datasets/Hello-SimpleAI/HC3)
- RAID: card and repo licence MIT. — [HF card](https://huggingface.co/datasets/liamdugan/raid); [GitHub](https://github.com/liamdugan/raid). Human sources: arXiv abstracts, book summaries, BBC News articles, poemhunter.com poems, RecipeNLG, Reddit (TL;DR), IMDb reviews, Wikipedia (GPT-wiki-intro). — [RAID paper](https://arxiv.org/html/2405.07940)
- MAGE: card licence "apache-2.0"; human sources are CMV, Yelp, XSum, TLDR_news, ELI5, WritingPrompts, ROCStories, HellaSwag, SQuAD, SciXGen; the paper states no source licences. — [HF card](https://huggingface.co/datasets/yaful/MAGE); [MAGE paper](https://ar5iv.labs.arxiv.org/html/2305.13242)
- M4: the GitHub page shows no licence; the paper's table lists per-source licences (Wikipedia CC BY-SA 3.0, WikiHow CC-BY-NC-SA, arXiv abstracts CC0, PeerRead Apache, Reddit ELI5 given only as "Huggingface") and says researchers must follow the original sources' terms. — [GitHub](https://github.com/mbzuai-nlp/M4); [M4 paper](https://ar5iv.labs.arxiv.org/html/2305.14902)
- TuringBench: card licence "apache-2.0"; Source Data is "[More Information Needed]". — [HF card](https://huggingface.co/datasets/turingbench/TuringBench)
- OUTFOX: repo Apache-2.0; human text is Kaggle Feedback Prize essays by US students in grades 6 to 12; the source licence is not stated. — [GitHub](https://github.com/ryuryukke/OUTFOX)
- CHEAT: repo MIT; human inputs are in `ieee-init` files. — [GitHub](https://github.com/botianzhe/CHEAT)
- Ghostbuster: human text is IvyPanda student essays, the Reuters 50-50 set, and r/WritingPrompts. — [Ghostbuster paper](https://ar5iv.labs.arxiv.org/html/2305.15047)
- Kobak et al.: the repo (MIT) distributes a 362,442 × 15 matrix of yearly word occurrences and 900 excess words, not abstract texts; the abstracts must be fetched from NCBI's PubMed baseline. — [GitHub](https://github.com/berenslab/llm-excess-vocab)

**Other**
- The Pile: card licence "other"; "Please refer to the specific license depending on the subset you use." — [HF card](https://huggingface.co/datasets/EleutherAI/pile)
- peS2o: licence "odc-by". — [HF card](https://huggingface.co/datasets/allenai/peS2o). Common Pile notes ODC-By on a collection "does not extend to individual documents within the corpus". — [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)
- SciTLDR: sidebar licence "unknown", licensing section "Apache License 2.0". — [HF card](https://huggingface.co/datasets/allenai/scitldr)
- Blog Authorship Corpus: licence "unknown"; "The corpus may be freely used for non-commercial research purposes." — [HF card](https://huggingface.co/datasets/barilan/blog_authorship_corpus)
- `sgoel9/paul_graham_essays`: "This dataset is released under the MIT License"; the card says nothing about permission from Paul Graham and only asks users to attribute and link to paulgraham.com. — [HF card](https://huggingface.co/datasets/sgoel9/paul_graham_essays)
- `crumb/openstax-text`: card licence cc-by-4.0, "76 openstax textbooks". — [HF card](https://huggingface.co/datasets/crumb/openstax-text). OpenStax's help centre says its textbooks are under CC BY-NC-SA: "OpenStax content is free to use and adapt, but not for commercial purposes." — [OpenStax help](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks)
- Khan Academy support pages point to CC BY-NC-SA for videos and exercises. — [Khan Academy support](https://support.khanacademy.org/hc/en-us/articles/202262954-Can-I-use-Khan-Academy-s-videos-name-materials-links-)

### Inferences
- Reading CC's guidance against this project's three acts: (a) a private local fine-tune shares nothing publicly, so BY, SA and ND are not triggered; only NC bites, and a personal non-commercial project plausibly satisfies it; (b) README sample outputs are public sharing only if they reproduce or adapt source text, so short novel outputs are low risk but verbatim regurgitation is not; (c) distributing adapter weights is the act that triggers SA (CC's reading: same licence on the shared model) and makes NC a lasting constraint on anyone downstream. So CC BY and public domain are the only inputs that leave adapter release unencumbered; CC BY-SA is workable if the adapter is released under CC BY-SA with attribution; NC and ND sources should be avoided if weights might ever be published. This is CC's interpretation, not settled law.
- Licence-label mismatches I would call out: CNN/DailyMail (Apache-2.0 over CNN and Daily Mail articles), Paul Graham essays (MIT over a living author's site with no stated permission), RAID (MIT over BBC, IMDb, Reddit and poemhunter text), MAGE (Apache-2.0 over Yelp, Reddit, BBC text), HC3 (CC BY-SA over Reddit answers whose own card says licence unknown), TuringBench (Apache-2.0, sources undocumented), and `crumb/openstax-text` (CC BY 4.0 claimed while OpenStax's help centre says CC BY-NC-SA). In each case the card licence can cover at most the compilation or the annotations, not the underlying prose.
- Card licences that are stale but harmless: `wikimedia/wikipedia` and WikiText say CC BY-SA 3.0 while Wikipedia now states 4.0.
- PG-19's Apache label sits on public-domain books, so the mismatch has no practical consequence in the US.

### Gaps
- The exact text of Stack Exchange's licensing page, the July 2024 dump agreement, Reddit's Data API Terms and wikiHow's Terms of Use could not be fetched; whether wikiHow's terms now name AI training is unverified.
- PLOS's terms page returned 403; the CC BY 4.0 status of PLOS text rests on the dataset card, not the publisher page.
- OpenStax sources conflict (help centre says all CC BY-NC-SA; a second help page and a Wikipedia mirror say most books are CC BY with Calculus and American Government as NC-SA exceptions). Per-book licences were not checked.
- Cochrane's own reuse terms for plain-language summaries were not found; the CC BY 4.0 label on the GEM card is unverified against the source.
- Licence files for Ghostbuster, TuringBench sources, the Feedback Prize essays, and "Human vs GPT"-style Kaggle or HF corpora were not checked.
- Khan Academy's Terms of Service text was not retrieved; no Khan-derived dataset was verified.

## 2. Size in words, number of documents, typical document length

### Takeaway
The 300,000-word floor is easy to clear with any of the open options; the binding constraint is unit length. eLife digests (mean 348 words) and CRS/GAO summaries (mean 553 words) already sit inside the 150 to 800 word chunk window, PLOS summaries (176 words) sit at its bottom edge, and ELI5 or Stack Exchange answers average about 130 words so only the long tail qualifies.

### Cited Findings
- eLife: 4,828 articles; digests average 347.6 words (15.7 sentences). PLOS: 27,525 articles; author summaries average 175.6 words (7.8 sentences). — [Goldsack et al. 2022](https://ar5iv.labs.arxiv.org/html/2210.09932)
- BioLaySumm 2025 eLife: 4,729 rows; summaries about 1.01k to 4.15k characters. — [HF card](https://huggingface.co/datasets/BioLaySumm/BioLaySumm2025-eLife)
- Cochrane simplification: 4,459 paragraph pairs. — [HF card](https://huggingface.co/datasets/GEM/cochrane-simplification)
- GovReport: 19,466 reports (12,228 GAO, 7,238 CRS); documents average 9,409 words, summaries 553 words. — [GovReport paper](https://ar5iv.labs.arxiv.org/html/2104.02112)
- EveryCRSReport: 23,620 CRS reports with bulk download via `reports.csv`. — [EveryCRSReport about](https://www.everycrsreport.com/about.html)
- BillSum: 23,455 bills. — [HF card](https://huggingface.co/datasets/FiscalNote/billsum)
- Common Pile raw to filtered: StackExchange 33,415,400 to 30,987,814 docs (103.7 to 89.7 GB); Wikimedia 63,969,938 to 16,311,574 (90.5 to 57.4 GB); News 172,308 to 126,673 (0.4 to 0.3 GB); LibreTexts 62,269 to 40,049 (5.3 to 3.6 GB); PressBooks 106,881 to 54,455 (1.5 to 0.6 GB); OERCommons 9,339 to 5,249; Project Gutenberg 71,810 to 55,454; Public Domain Review 1,412 to 1,406. — [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)
- A Common Pile Stack Exchange document is one question with comments, all answers and their comments. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)
- Common Corpus: 2.27 trillion tokens; OpenCulture 967B, OpenGovernment 579B, OpenSource 283B, OpenScience 281B, OpenWeb 88.5B, Open Semantic 68B. — [HF card](https://huggingface.co/datasets/PleIAs/common_corpus)
- Wikipedia 20231101: English 6.41M articles, Simple English 242k. — [HF card](https://huggingface.co/datasets/wikimedia/wikipedia)
- WikiText: "over 100 million tokens" from verified Good and Featured articles. — [HF card](https://huggingface.co/datasets/Salesforce/wikitext)
- Wiki-auto: 138,095 article pairs from the 2019/09 dump, with paragraph and sentence alignments. — [HF card](https://huggingface.co/datasets/chaojiang06/wiki_auto)
- ELI5: 272K questions; answers average 130.6 words (6.6 sentences). — [ELI5 paper](https://ar5iv.labs.arxiv.org/html/1907.09190)
- ELI5-Category: 91,772 training examples. — [HF card](https://huggingface.co/datasets/rexarski/eli5_category)
- HC3 human answers: reddit_eli5 51,336 (mean 134 words); finance 3,933 (202); medicine 1,248 (93); open_qa 1,187 (35); wiki_csai 842 (229). — [HC3 paper](https://ar5iv.labs.arxiv.org/html/2301.07597)
- RAID: 14,971 human-written documents, about 2,000 per domain. — [RAID paper](https://arxiv.org/html/2405.07940)
- MAGE: 436,606 rows in total; human samples average 232 (unit unstated). — [HF card](https://huggingface.co/datasets/yaful/MAGE); [MAGE paper](https://ar5iv.labs.arxiv.org/html/2305.13242)
- M4: 35,798 parallel human texts, 3,000 per English source (Wikipedia, Reddit ELI5, WikiHow, arXiv abstracts) and 5,798 PeerRead reviews. — [M4 paper](https://ar5iv.labs.arxiv.org/html/2305.14902)
- Ghostbuster: 1,000 human documents per domain; median 529 words (essays), 498 (Reuters), 455 (WritingPrompts). — [Ghostbuster paper](https://ar5iv.labs.arxiv.org/html/2305.15047)
- OUTFOX: 15,400 human student essays. — [GitHub](https://github.com/ryuryukke/OUTFOX)
- XSum: 226,711 BBC articles, mean 431 words, summary 23 words. — [XSum paper](https://ar5iv.labs.arxiv.org/html/1808.08745)
- CNN/DailyMail: 311,971 articles, mean 781 tokens, highlights 56 tokens. — [HF card](https://huggingface.co/datasets/abisee/cnn_dailymail)
- Multi-News: 44,972 / 5,622 / 5,622 examples. — [HF card](https://huggingface.co/datasets/alexfabbri/multi_news)
- SciTLDR: 5.4K TLDRs over 3.2K papers; "The average rewritten summary is 20 words long". — [HF card](https://huggingface.co/datasets/allenai/scitldr)
- PG-19: 28,752 books. — [HF card](https://huggingface.co/datasets/deepmind/pg19). SPGC: 55,905 books. — [Zenodo](https://zenodo.org/records/2422561)
- peS2o V2: 38.97M documents, 42.01B whitespace tokens. — [HF card](https://huggingface.co/datasets/allenai/peS2o)
- Blog Authorship Corpus: 19,320 bloggers, 681,288 posts, over 140 million words. — [HF card](https://huggingface.co/datasets/barilan/blog_authorship_corpus)
- Paul Graham essays: 215 essays, 2.96 MB. — [HF card](https://huggingface.co/datasets/sgoel9/paul_graham_essays)
- `crumb/openstax-text`: 3,354,565 rows, 159 MB. — [HF card](https://huggingface.co/datasets/crumb/openstax-text)

### Inferences
- Computed totals: eLife digests about 1.68M words (4,828 × 347.6); PLOS summaries about 4.83M words (27,525 × 175.6); GovReport summaries about 10.8M words (19,466 × 553.4); HC3 wiki_csai about 193k words (842 × 229), which alone is below the 300k floor; ELI5 answers about 35.5M words; XSum articles about 97.7M words.
- eLife digests alone give roughly five times the required volume in units that need no chunking. Each digest is a complete explainer, which matters because chunks cut from the middle of 9,000-word reports or textbook pages lose their opening and close.
- SciTLDR (20 words), XSum summaries (23 words) and CNN/DM highlights are too short to train 150 to 800 word prose; only the article bodies would be usable, and those are the copyrighted parts.
- AI-detection sets are small on the human side (1,000 to 3,000 documents per domain) and are re-samples of datasets already listed here; going to the upstream source is strictly better.
- The HC3 card shows 17.1k reddit_eli5 rows while the paper counts 51,336 human answers; the likely reason is several human answers per question row.

### Gaps
- Per-wiki document counts inside `common-pile/wikimedia` (Wikinews, Wikibooks, Wikiversity) are not on the card.
- Word counts for `common-pile/news` per site (how much is 360info or SciDev.Net versus Tasnim or Meduza) are not published.
- Mean length for Cochrane plain-language summaries, BillSum summaries, Multi-News, TuringBench and CHEAT was not obtained.
- Simple English Wikipedia's total word count and Wikinews's English article count were not obtained.

## 3. Register and quality: good explanatory prose or noisy forum text?

### Takeaway
The best-matched register for "plain, concrete explanatory writing" is the eLife digest (professionally edited science explanation, reading grade about 11), followed by open-licensed explanatory journalism (360info, SciDev.Net, Global Voices) and high-voted Stack Exchange answers for maths and technical walkthroughs. Government summaries are clean but bureaucratic; ELI5 is conversational and uneven; PLOS author summaries are measurably harder to read than eLife's.

### Cited Findings
- eLife digests are written by expert editors "based on the article and on questions answered by its author"; PLOS summaries are written by the paper's authors (150 to 200 words). Lay-summary readability: FKGL 10.92 (eLife) versus 14.76 (PLOS); Coleman-Liau 12.51 versus 15.90; Dale-Chall 8.83 versus 10.91. — [Goldsack et al. 2022](https://ar5iv.labs.arxiv.org/html/2210.09932)
- 360info: academics write, professional journalists and editors commission and translate the work into plain language. — [360info about](https://360info.org/about-us/)
- `common-pile/news` mixes 20 outlets including fact-checkers (Alt News, Factly, ZimFact), state media (Tasnim News Agency), Meduza and Agenzia Fides. — [HF card](https://huggingface.co/datasets/common-pile/news)
- Common Pile's filtered sets apply "filters based on language, text quality, length, likelihood, and toxicity", plus PII and boilerplate removal. — [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)
- `common-pile/wikimedia` includes talk pages "where editors discuss changes made for a page"; wikitext was converted with wtf_wikipedia and math converted to LaTeX. — [HF card](https://huggingface.co/datasets/common-pile/wikimedia)
- Stack Exchange documents in Common Pile order answers by votes with the accepted answer first, and include comments. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)
- LibreTexts preview rows are Illustrative Mathematics Grade 7 textbook sections. — [HF card](https://huggingface.co/datasets/common-pile/libretexts)
- GovReport summaries are expert-written: GAO "highlights" and CRS summaries; boilerplate was removed and section structure kept. — [GovReport paper](https://ar5iv.labs.arxiv.org/html/2104.02112)
- ELI5 kept threads where question and at least one answer had a score of at least two, and used the highest-scored answer as reference. — [ELI5 paper](https://ar5iv.labs.arxiv.org/html/1907.09190)
- HC3 human answers are "written by domain experts or are high-voted answers from web users"; wiki_csai treats Wikipedia concept explanations as answers; finance comes from FiQA, built from Stack Exchange investment posts. — [HC3 paper](https://ar5iv.labs.arxiv.org/html/2301.07597)
- WikiText is drawn from verified Good and Featured Wikipedia articles. — [HF card](https://huggingface.co/datasets/Salesforce/wikitext)
- XSum articles and their one-sentence summaries were written by professional BBC writers. — [XSum paper](https://ar5iv.labs.arxiv.org/html/1808.08745)
- Multi-News summaries are "professionally written by editors". — [HF card](https://huggingface.co/datasets/alexfabbri/multi_news)
- OUTFOX human essays are by US students in grades 6 to 12; Ghostbuster essays are high school and university essays from IvyPanda. — [GitHub](https://github.com/ryuryukke/OUTFOX); [Ghostbuster paper](https://ar5iv.labs.arxiv.org/html/2305.15047)
- PG-19 books were published before 1919. — [HF card](https://huggingface.co/datasets/deepmind/pg19)
- More than half of Common Corpus predates the 21st century; preview rows include a 1905 patent, 1937 Hansard and court decisions. — [HF card](https://huggingface.co/datasets/PleIAs/common_corpus)

### Inferences
- Ranked by fit to the target register (my judgement from the cards and papers; I read no full samples because nothing was downloaded): (1) eLife digests; (2) 360info, SciDev.Net and Global Voices articles inside `common-pile/news`; (3) Stack Exchange accepted answers from prose-heavy sites (Mathematics, Physics, Cross Validated, Skeptics, English Language) after stripping questions and comments; (4) Wikinews; (5) CRS/GAO summaries; (6) LibreTexts and Wikibooks textbook sections; (7) Featured-article Wikipedia.
- Wikipedia prose is encyclopedic and impersonal, and it is the register an LLM already defaults to, so it is a weak teacher for "prefer this over generic AI writing". WikiText's tokenised format (`@-@`, lower-level tokenisation artefacts) makes it worse than a fresh dump.
- CRS and GAO summaries are clear and concrete but heavy with institutional phrasing ("GAO was asked to review"), so they suit a policy-explainer slice, not the whole corpus.
- Student-essay sets (OUTFOX, Ghostbuster essays) are the wrong quality bar for a model meant to write better than average. PG-19 and most of Common Corpus are the wrong century for "modern" prose.
- `common-pile/news` needs a per-source allowlist: state media and fact-check boilerplate would pull the style off target.
- Wikimedia data needs talk pages filtered out, and textbook sources need maths-markup handling.

### Gaps
- No samples were read at length, so every quality ranking above is a judgement from descriptions, not from inspection.
- The share of prose versus code or formula in Stack Exchange answers per site was not measured.
- Cochrane plain-language summaries' readability relative to eLife was not checked.

## 4. Dates: is the human text from before December 2022?

### Takeaway
Most classic datasets are safely pre-2022 (ELI5, XSum, CNN/DM, GovReport, WikiText, eLife/PLOS as retrieved March 2022, PG-19). The risk sits in recent open collections: Common Pile's news, Stack Exchange and Wikimedia data run to 2024-2025 and must be date-filtered, and even "human" halves of two detection sets contain post-2021 text.

### Cited Findings
- eLife and PLOS data were retrieved on 11 and 7 March 2022. — [Goldsack et al. 2022](https://ar5iv.labs.arxiv.org/html/2210.09932)
- BioLaySumm 2025 eLife has a `year` field with 11 values; samples cover 2015 to 2020. — [HF card](https://huggingface.co/datasets/BioLaySumm/BioLaySumm2025-eLife)
- GovReport: GAO reports before 7 July 2020, CRS before 20 May 2020. — [GovReport paper](https://ar5iv.labs.arxiv.org/html/2104.02112)
- ELI5: posts from August 2012 to August 2019 (card); threads up to July 2018 (paper). ELI5-Category: January 2017 to June 2021. — [HF card](https://huggingface.co/datasets/defunct-datasets/eli5); [ELI5 paper](https://ar5iv.labs.arxiv.org/html/1907.09190); [HF card](https://huggingface.co/datasets/rexarski/eli5_category)
- XSum: 2010 to 2017. CNN/DailyMail: April 2007 to April 2015. — [XSum paper](https://ar5iv.labs.arxiv.org/html/1808.08745); [HF card](https://huggingface.co/datasets/abisee/cnn_dailymail)
- Wiki-auto: 2019/09 dump. `wikimedia/wikipedia`: 2023-11-01 dump. — [HF card](https://huggingface.co/datasets/chaojiang06/wiki_auto); [HF card](https://huggingface.co/datasets/wikimedia/wikipedia)
- Blog Authorship Corpus: August 2004. — [HF card](https://huggingface.co/datasets/barilan/blog_authorship_corpus)
- peS2o knowledge cutoff: 2023-01-03. — [HF card](https://huggingface.co/datasets/allenai/peS2o)
- `common-pile/news`: scraped 2024-05-27; preview articles dated 2021 to 2024. — [HF card](https://huggingface.co/datasets/common-pile/news)
- `common-pile/stackexchange`: December 2024 community dumps plus July 2024 official dumps; records carry a `created` field. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)
- `common-pile/wikimedia`: March 2025 dumps, most recent revision of each page only. — [HF card](https://huggingface.co/datasets/common-pile/wikimedia)
- RAID: "To avoid contamination, most of our human-written documents are taken from publicly available pre-2022 datasets"; only Wikipedia and Abstracts include post-2021 documents. — [RAID paper](https://arxiv.org/html/2405.07940)
- M4: Wikipedia is "the March 2022 version"; no dates given for the other English sources. — [M4 paper](https://ar5iv.labs.arxiv.org/html/2305.14902)
- Ghostbuster: WritingPrompts posts taken from before ChatGPT's release on 30 November 2022. — [Ghostbuster paper](https://ar5iv.labs.arxiv.org/html/2305.15047)
- HC3 paper is dated 18 January 2023 and draws human answers from existing QA datasets (ELI5, WikiQA, Medical Dialog, FiQA) plus crawled Wikipedia. — [HF card](https://huggingface.co/datasets/Hello-SimpleAI/HC3); [HC3 paper](https://ar5iv.labs.arxiv.org/html/2301.07597)
- Kobak et al. analyse excess vocabulary in PubMed abstracts from 2013 to 2024. — [GitHub](https://github.com/berenslab/llm-excess-vocab)
- Common Pile avoided LLM-generated text as a sourcing rule. — [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)

### Inferences
- Safe without filtering: eLife/PLOS (Goldsack version), GovReport, ELI5, XSum, CNN/DM, WikiText, Wiki-auto, PG-19, Blog Authorship Corpus, Ghostbuster.
- Needs a date filter: `common-pile/stackexchange` (use `created` earlier than December 2022), `common-pile/news` (publication date is in the text, not a clean field, so filtering is harder), anything from the 2023 or 2025 Wikipedia dumps (latest-revision dumps cannot be filtered by date at all; a 2022 dump or WikiText is the only clean route), EveryCRSReport (use version dates), PLOS or PubMed abstracts after 2022 (Kobak's finding is precisely that these now contain LLM-assisted text).
- A March 2025 Wikipedia or Wikibooks snapshot is the least controllable source for AI contamination because any article may have been edited with an LLM since 2023.

### Gaps
- The HC3 wiki_csai crawl date is not stated on the card or in the passage I read; it is most likely late 2022.
- Publication-year range of the Goldsack eLife and PLOS articles is not stated beyond retrieval dates.
- Date range for MAGE's TLDR_news and SciXGen sources, TuringBench, CHEAT and OUTFOX was not established.

## 5. Voice: many anonymous authors, or a coherent style?

### Takeaway
Only a few candidates offer a consistent voice. eLife digests come from a small editorial team following one house format; CRS and GAO summaries follow institutional templates; single-outlet news (360info, Wikinews, VOA) has a house style. Everything forum- or wiki-derived is thousands of anonymous authors.

### Cited Findings
- eLife digests are written by expert editors; PLOS summaries by each paper's own authors. — [Goldsack et al. 2022](https://ar5iv.labs.arxiv.org/html/2210.09932)
- GAO highlights and CRS summaries are expert-written institutional products. — [GovReport paper](https://ar5iv.labs.arxiv.org/html/2104.02112)
- 360info pieces are written by academics and edited into plain language by professional journalists. — [360info about](https://360info.org/about-us/)
- `common-pile/news` spans 20 outlets, with 17 distinct `source` values in the preview. — [HF card](https://huggingface.co/datasets/common-pile/news)
- Blog Authorship Corpus: 19,320 bloggers. — [HF card](https://huggingface.co/datasets/barilan/blog_authorship_corpus)
- Reuters 50-50 (used in Ghostbuster): 5,000 news articles by 50 journalists. — [Ghostbuster paper](https://ar5iv.labs.arxiv.org/html/2305.15047)
- Paul Graham essays: 215 essays by one author. — [HF card](https://huggingface.co/datasets/sgoel9/paul_graham_essays)
- ELI5 uses the highest-scored answer per thread from any Reddit user. — [ELI5 paper](https://ar5iv.labs.arxiv.org/html/1907.09190)

### Inferences
- For a style model, eLife digests are the closest thing to a single-voice explanatory corpus with an open licence: one publisher, one format, one editorial team, about 1.7M words.
- PLOS summaries are 27,525 different author teams writing to a loose brief, so the voice is diffuse and closer to abstract-ese.
- Stack Exchange can be made semi-coherent by selecting a handful of prolific high-reputation answerers per site, since attribution is in the data and CC BY-SA requires it anyway.
- The single-author scrapes are the most coherent and the least licensable. The project memory records that the chosen target author was selected with consent; an unlicensed Paul Graham scrape has no equivalent consent on its card.

### Gaps
- How many editors write eLife digests, and whether the format changed over the years, was not verified.
- Author-count distributions for Stack Exchange sites were not checked.

## 6. Contamination and memorization: was it in the pretraining of Qwen or Llama?

### Takeaway
Neither Qwen3 nor Llama 3 publishes a dataset-level training list, so exposure cannot be confirmed for any candidate; assume all public web text (Wikipedia, Stack Exchange, Reddit, BBC, PubMed Central) was seen. That mostly lowers the marginal style signal from those sources and is a reason to prefer distinctive, edited prose over encyclopedic text.

### Cited Findings
- Qwen3 was pretrained on 36 trillion tokens across 119 languages in three stages; sources named only as categories ("books, multilingual texts, and synthetic data", PDF-like documents recognised with Qwen2.5-VL, synthetic textbooks and QA from Qwen2.5 models). No specific public dataset is named. — [Qwen3 technical report](https://arxiv.org/html/2505.09388)
- The Llama 3 paper reports verbatim memorization rates of about 1.13% and 3.91% for the 405B model at n = 50 and n = 1000, roughly on par with Llama 2 (from a search summary; I did not open the paper). — [The Llama 3 Herd of Models](https://arxiv.org/pdf/2407.21783)
- A survey cites the original LLaMA's reported mix as Common Crawl, C4, GitHub, Wikipedia, Books, ArXiv and StackExchange, with StackExchange at 2.0% (search summary; applies to LLaMA 1, not Llama 3). — [Survey of transparency for LLMs](https://arxiv.org/pdf/2403.16139)
- The Pile's subsets as shown on its card include Pile-CC, PubMed Central, pubmed, FreeLaw, USPTO, GitHub, HackerNews, NIH ExPorter, Enron emails, EuroParl and Ubuntu IRC. — [HF card](https://huggingface.co/datasets/EleutherAI/pile)
- Common Pile was built to train the Comma v0.1 models (7B parameters, 1T and 2T tokens); the paper has no memorization analysis in the part I read. — [Common Pile abstract](https://arxiv.org/abs/2506.05209); [Common Pile v0.1 paper](https://arxiv.org/html/2506.05209)

### Inferences
- Wikipedia, Stack Exchange and PubMed Central (which holds eLife and PLOS full texts) are standard pretraining sources, so an 8B base model has very likely seen every strong candidate here. Fine-tuning on seen text still shifts style, but the held-out evaluation should use text published after the base model's cutoff or text never on the open web.
- Memorization risk for README samples is highest for short, heavily duplicated text (Wikipedia leads, famous Stack Overflow answers) and lower for eLife digests, which appear once each. A verbatim-overlap check of sample outputs against the training set is cheap insurance, and it also matters for BY and SA compliance.

### Gaps
- No published study was found that measures memorization of ELI5, XSum, eLife or Stack Exchange text specifically in Qwen or Llama models.
- Llama 3's training sources are not disclosed at dataset level; the figures above come from a search summary, not a reading of the paper.
- Whether Qwen or Llama used The Pile or Common Corpus is unknown.

## 7. Availability in November 2026 and takedown history

### Takeaway
Reddit- and wikiHow-derived datasets are the unstable ones: canonical ELI5 has been defunct since Reddit's API change, and wikiHow began DMCA takedowns on Hugging Face in August 2026 alongside a lawsuit against OpenAI. The CC BY, CC BY-SA and public-domain sets were all reachable when checked.

### Cited Findings
- ELI5: "Dataset "eli5" is defunct and no longer accessible due to unavailability of the source data"; "Reddit recently changed the terms of access to its API, making the source data for this dataset unavailable." — [HF card](https://huggingface.co/datasets/defunct-datasets/eli5)
- `rexarski/eli5_category` page is up with 499 downloads last month, but it is a loading-script repo of 17.9 kB with the viewer disabled. — [HF card](https://huggingface.co/datasets/rexarski/eli5_category)
- `gursi26/wikihow-cleaned`: access disabled following a DMCA notice from wikiHow, Inc. — [HF card](https://huggingface.co/datasets/gursi26/wikihow-cleaned); [HF discussion](https://huggingface.co/datasets/gursi26/wikihow-cleaned/discussions/1)
- HC3 card is live with no warnings and still includes the reddit_eli5 split. — [HF card](https://huggingface.co/datasets/Hello-SimpleAI/HC3)
- The Pile's card shows no takedown notice, but the repo is 24.9 kB against a stated 825 GiB, with a loading script. — [HF card](https://huggingface.co/datasets/EleutherAI/pile)
- Blog Authorship Corpus: viewer disabled, loading-script repo, original host u.cs.biu.ac.il. — [HF card](https://huggingface.co/datasets/barilan/blog_authorship_corpus)
- Stack Exchange official dumps left the Internet Archive in July 2024; community uploads continued through December 2024, and some defunct sites are missing. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)
- Live when fetched: Common Pile org (63 datasets), Common Corpus, scientific_lay_summarisation, BioLaySumm 2025 eLife, GEM Cochrane, GovReport, BillSum, wikimedia/wikipedia, WikiText, Wiki-auto, PG-19, SciTLDR, XSum, CNN/DailyMail, Multi-News, RAID, MAGE, TuringBench, peS2o, paul_graham_essays, openstax-text. — [Common Pile org](https://huggingface.co/common-pile); [Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus); [lay summarisation](https://huggingface.co/datasets/tomasg25/scientific_lay_summarisation)
- EveryCRSReport offers a CSV index and a bulk-download script. — [EveryCRSReport download page](https://www.everycrsreport.com/download.html)
- Newsela access requires academic affiliation and an NDA. — [Newsela data page](https://newsela.com/legal/data)

### Inferences
- "Card is live" is not "files download": I did not download anything, so loading-script repos (The Pile, ELI5-Category, Blog Authorship Corpus) may well fail with current `datasets` versions, which no longer run loading scripts by default.
- HC3 and M4 still redistribute Reddit ELI5 and WikiHow text; given the August 2026 wikiHow notices and Reddit's litigation, both are plausible future takedown targets and poor foundations for a public project.
- Newsela is out of reach for an individual non-academic project.

### Gaps
- Whether the August 2026 wikiHow DMCA campaign reached other WikiHow datasets on Hugging Face (the original `wikihow` summarization set, WikiLingua, M4) was not checked.
- Status of `sentence-transformers/eli5`, `Pavithree/eli5` and Kaggle "Human vs GPT" corpora was not verified.
- Outcome of Reddit v. Anthropic (filed June 2025) was not found.
- Whether Stack Exchange changed its dump terms after July 2024 was not found.

## 8. One-line verdicts and the three strongest ready-made options

### Takeaway
The three strongest ready-made options are (1) eLife digests from the lay-summarisation corpora, (2) a date-filtered, site-selected slice of `common-pile/stackexchange`, and (3) an allowlisted slice of `common-pile/news` plus Wikinews, with CRS/GAO summaries from GovReport as the public-domain fallback. All three have verified open licences, clear the 300,000-word floor, and cover science, maths/technical and news registers respectively.

### Cited Findings
Verdict lines rest on the findings cited in sections 1 to 7; the load-bearing ones are repeated here.
- eLife digests: CC BY 4.0, 4,828 digests, mean 347.6 words, editor-written, FKGL 10.92, retrieved March 2022. — [HF card](https://huggingface.co/datasets/tomasg25/scientific_lay_summarisation); [Goldsack et al. 2022](https://ar5iv.labs.arxiv.org/html/2210.09932)
- `common-pile/stackexchange`: 33.4M question threads, per-document CC BY-SA 3.0/4.0 metadata, `created` field, answers vote-ordered. — [HF card](https://huggingface.co/datasets/common-pile/stackexchange)
- `common-pile/news`: 172,308 documents from CC BY / CC BY-SA outlets with per-document licence. — [HF card](https://huggingface.co/datasets/common-pile/news)
- GovReport: 19,466 public-domain reports with 553-word expert summaries, all before mid-2020. — [GovReport paper](https://ar5iv.labs.arxiv.org/html/2104.02112)

### Inferences

**The three strongest**
1. eLife digests (`tomasg25/scientific_lay_summarisation`, eLife config, summary field only). About 1.68M words (computed) of edited science explanation in ready-sized units, CC BY 4.0, pre-2022, coherent voice. Attribution by a link to eLife and the dataset satisfies BY. Weakness: biology and medicine only, and a recognisable digest formula ("... et al. show that ...") that may need diluting.
2. `common-pile/stackexchange`, filtered: keep accepted or top-voted answers of 150 to 800 words created before December 2022 from prose-heavy sites (Mathematics, Physics, Cross Validated, Computer Science, Skeptics), drop questions and comments. Supplies the maths and technical walkthroughs eLife lacks. CC BY-SA means a published adapter should carry CC BY-SA and attribution, per CC's reading. Weakness: many authors, variable quality, needs real filtering work.
3. `common-pile/news` allowlist (360info, SciDev.Net, Global Voices) plus Wikinews from `common-pile/wikimedia_filtered` (`wiki` metadata). Supplies news-style explanatory prose under CC BY. Weakness: articles run to 2024, so date filtering is needed and is awkward; per-site volume is unknown.

Fallback or supplement: GovReport summaries or EveryCRSReport (public domain, no licence obligations at all, about 10.8M summary words computed) for a policy-explainer slice.

**One-line verdicts**
- eLife digests: best single option; use.
- PLOS author summaries: open and large, but short and harder to read; secondary.
- Cochrane plain-language summaries: small, paragraph-pair format, source terms unverified; skip unless verified.
- SciTLDR: 20-word summaries; unusable for prose training.
- Common Pile Stack Exchange: strong for maths/technical after filtering; SA applies.
- Raw Stack Exchange dump: same text, worse access terms since July 2024; use the Common Pile copy.
- Common Pile news: good after an outlet allowlist and date filter.
- Common Pile LibreTexts / PressBooks / OERCommons: open textbook prose; useful supplement, needs maths cleanup and chunking.
- Common Pile Wikimedia (Wikibooks, Wikinews, Wikiversity): open; drop talk pages; March 2025 snapshot cannot be date-filtered.
- Common Corpus: enormous, mostly historical, legal and multilingual; poor fit for modern explanatory English.
- Wikipedia / WikiText / Simple English Wikipedia: open and clean but encyclopedic and already the model's default register; low value.
- Wiki-auto: alignment data for simplification, not a prose corpus; skip.
- Newsela: closed to non-academics; skip.
- GovReport / CRS: public domain, clean, formal; good fallback slice.
- BillSum: legislative summaries; too legalistic.
- VOA: public domain for VOA-produced text, but no verified ready-made dataset and wire copy must be excluded.
- XSum, CNN/DailyMail, Multi-News: copyrighted news under unknown, mislabelled or non-commercial terms; do not use.
- ELI5 and variants: defunct, licence unknown, Reddit terms hostile; do not use.
- WikiHow sets: CC BY-NC-SA and under active DMCA enforcement; do not use.
- HC3, M4, MAGE, RAID, TuringBench: re-samples of the above with permissive labels over mixed sources; go upstream instead. HC3 wiki_csai (193k words computed) is Wikipedia and below the floor.
- Ghostbuster, OUTFOX: student essays, fiction, Reuters copy; wrong register or licence.
- CHEAT: IEEE abstracts under an MIT label; skip.
- Kobak et al.: word-frequency data only; useful as a vocabulary blocklist for evaluation, not as a corpus.
- The Pile: mixed per-subset licences, loading-script repo; superseded by Common Pile for this purpose.
- peS2o / S2ORC / arXiv: research-paper register, not lay explanation; no verified "lay summary" subset exists.
- PG-19 / SPGC: public domain but pre-1919 prose; wrong era.
- Blog Authorship Corpus: 2004 personal blogs, non-commercial research only; skip.
- Paul Graham and similar single-author scrapes: coherent voice, no real licence; do not use without the author's consent.
- OpenStax / Khan Academy sets: licence conflict or NC; verify per book before any use.

### Gaps
- No dataset of award-winning or professionally curated science journalism with an open licence was found; I did not search for one beyond the candidates given.
- Candidate additions I did not verify: The Conversation (I believe CC BY-ND, which CC's guidance treats as barring training), Our World in Data articles, NASA/NIH/EIA explainers (US government works, but no ready-made dataset confirmed). These would need their own licence check.
- All three top options need hands-on sampling before commitment; nothing in these notes is based on reading the data itself.
