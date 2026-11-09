# Same-content human vs AI informational text pairs: natural and cheaply constructible sources (as of 2026-11-07)

Scope: pair sources where the topic or content is held fixed and only the writer (human vs AI) differs, for use as content-controlled negatives when training "quill" (QLoRA, 7-9B, MLX). Wikipedia AI-cleanup diffs and social media are out of scope; they are covered elsewhere.

Labels used throughout:
- **measured**: I counted or computed it on 2026-11-07, with scripts and downloads under `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/priors/`.
- **published**: reported in a paper or dataset card.
- **self-reported**: an operator's or company's own claim.
- **estimated**: my inference.

## Which sources yield ≥10k aligned pairs in informational registers, retrievable with workable terms, ideally from 2025-2026 models?

### Takeaway
Three things clear the ≥10k bar for informational text with a recent production or frontier model as the writer:
- **Grokipedia v0.1 paired with Wikipedia.** There are about 884k article pairs, written by Grok in Oct 2025. The text is public, but the terms are mixed (CC BY-SA plus xAI terms).
- **DetectRL-X.** Paired human/LLM fields, MIT license, written by GPT-4o, Gemini-2.5-Flash, DeepSeek-V3 and Qwen-Max.
- **EditLens.** 60k training rows, edits by GPT-4.1, Claude Sonnet 4 and Gemini 2.5 Flash on human text from before 2022. It is gated and non-commercial.

HAP-E-2 adds continuation pairs from GPT-5-mini and Claude Haiku 4.5, at 8,290 texts per model across 6 registers, of which only part is informational.

The "natural" non-encyclopedia sources each fail one test:
- News content-farm rewrites, AI Overviews, Amazon review highlights, Quora/Poe answers and AI recipe clones have no published paired dataset.
- Building those pairs means scraping copyrighted or terms-restricted pages on both sides.
- Stack Exchange's deleted AI answers did not turn up in any public dataset.

Legacy pair sets (HC3, RAID, GPT-wiki-intro, M4/MAGE) are large but come from 2022-2023 models.

### Cited Findings

**A. Grokipedia (xAI) vs Wikipedia**
- **Launch size.** Grokipedia v0.1 launched on 27 Oct 2025 with 885,279 articles. This is the sitemap count captured by a third party (self-reported/measured by the uploader). — [stefan-it/grokipedia-urls](https://huggingface.co/datasets/stefan-it/grokipedia-urls)
- **Triedman & Mantzarlis corpus (published, Nov 2025).**
  - They scraped 883,858 articles (99.8%) on 28-30 Oct 2025.
  - They matched each one by exact title to the Wikimedia Enterprise English Wikipedia dump of 28 Oct 2025.
  - 496,058 articles (56%) carry the footer "The content is adapted from Wikipedia, licensed under Creative Commons Attribution-ShareAlike 4.0 License". 385,139 (44%) do not.
  — [arXiv:2511.09685 (HTML)](https://arxiv.org/html/2511.09685)
- **Similarity and length (published).**
  - Similarity was measured as mean chunk-level embedding cosine (EmbeddingGemma, 250-token chunks with 100-token overlap). It is 0.90 for CC-licensed articles and 0.77 for non-CC articles, and the non-CC distribution is bimodal.
  - Controversial topics average 0.73 against 0.82 for other topics.
  - About 96% of Grokipedia articles have at least as many chunks as their Wikipedia counterpart.
  - The median non-CC article is about 4.6× longer, measured by outline length.
  — [arXiv:2511.09685](https://arxiv.org/html/2511.09685)
- **Public v0.1 dump.**
  - The paper's scrape is public as `htriedman/grokipedia-v0.1-dump`.
  - The file listing shows `grokipedia_scrape.ndjson` at 68.8 GB, plus 16 chunk-text parquet shards of about 0.97 GB each with matching embedding .npy files of about 8.76 GB each (measured).
  - The schema has sections, paragraphs, tables, references and a `fact_check_timestamp` field.
  - Mirrors exist at REXX-NEW and Whalemini.
  — [HF card](https://huggingface.co/datasets/htriedman/grokipedia-v0.1-dump)
- **Dump license (self-reported by the uploader).**
  - Content is governed by the xAI Terms of Service.
  - Wikipedia-adapted pages may fall under CC BY-SA 4.0.
  - The other pages fall under the xAI Community License, "all rights reserved. Copyright © xAI 2025", and the dataset must state "Powered by xAI".
  — [HF card](https://huggingface.co/datasets/htriedman/grokipedia-v0.1-dump)
- **Title mapping (published).** A ready-made Grokipedia-to-Wikipedia title map covers 881,743 Grokipedia v0.1 URLs (measured row count). It maps to Wikipedia titles in 16 languages, using Wikipedia and Wikidata dumps of 1 Nov 2025 with redirects resolved. 3,536 Grokipedia URLs had no Wikipedia match. License: Apache-2.0. — [lewoniewski/grokipedia-wikipedia-16-languages](https://huggingface.co/datasets/lewoniewski/grokipedia-wikipedia-16-languages)
- **Current size (measured, 2026-11-07).**
  - The live sitemap index (`assets.grokipedia.com/sitemap/sitemap-index.xml`) lists 235 child sitemaps, all with lastmod 2026-01-26. The last child holds 7,612 URLs.
  - A weekly HF snapshot of that sitemap (`fetched_at` 2026-03-16) has 5,857,612 rows (5,857,573 unique URLs), with page lastmod values ranging from 2025-10-27 to 2026-01-26. 509,152 are dated Dec 2025 and 5,348,457 Jan 2026.
  - So the index is about 5.86M URLs and has not grown since late Jan 2026.
  — [caentzminger/grokipedia-urls](https://huggingface.co/datasets/caentzminger/grokipedia-urls)
- **Earlier reported counts.** Press put v0.2 at about 5.6M articles (Teslarati) and "over 6 million" after the Nov 2025 v0.2 release (SmartWorld). — [Teslarati](https://www.teslarati.com/elon-musks-grokipedia-surges-to-5-6-million-articles-almost-79-of-wikipedia/); [SmartWorld](https://www.smartworld.it/news/grokipedia-abbandonata-nessun-aggiornamento-aprile-2026.html)
- **Project status: conflicting evidence.**
  - SmartWorld (6 Aug 2026), citing a Lawfare investigation, says Grokipedia had no updates since April 2026. It also says 225,496 user-proposed corrections on 34,519 pages had gone unprocessed for three months. — [SmartWorld](https://www.smartworld.it/news/grokipedia-abbandonata-nessun-aggiornamento-aprile-2026.html)
  - But in my 12-page sample (measured, 2026-11-07), the JSON-LD `dateModified` ranged from 2026-01-14 to 2026-11-02. 6 of 12 were dated Sep-Nov 2026 (for example Photosynthesis 2026-11-02, Plate tectonics 2026-11-01, Great Barrier Reef 2026-10-20), and the page shows "Fact-checked by Grok · 5 days ago".
  - So some pages, or at least their fact-check timestamps, are still being touched even though the sitemap is frozen.
  - I did not fetch the Lawfare piece itself.
- **Retrieval (measured).**
  - robots.txt disallows only `/api/`.
  - Article pages are server-rendered. The HTML comment reads "Article body — pre-rendered HTML, zero client JS", and paragraphs are `<span data-tts-block="true" class="mb-4 block …">` elements.
  - So plain HTML fetching works, about 0.5 MB per page.
  - The ToS link on the page points to x.ai/legal/terms-of-service. `grokipedia.com/terms-of-service` returned 404 to WebFetch, so I could not read Grokipedia-specific terms.
- **Yasseri & Mohammadi (published).**
  - v2 compared 1,811 pairs from the 2,000 most-edited Wikipedia articles (Oct 2025).
  - Results, Grokipedia vs Wikipedia: TF-IDF cosine 0.505, embedding cosine 0.825, BERTScore F1 0.193, stylistic similarity 0.835, Flesch-Kincaid grade 19.3 vs 12.8, words 14,200 vs 9,360, references per 1k words 21.4 vs 90.2.
  — [arXiv:2510.26899v2](https://arxiv.org/html/2510.26899v2)
  - v5 (10 Apr 2026) scales to 17,790 pairs from the 20,000 most-edited pages. It reports that Grokipedia content "divides into two distinct groups", one aligned with Wikipedia and one that "diverges sharply". — [arXiv:2510.26899](https://arxiv.org/abs/2510.26899)
- **Hadad et al. (published, Feb 2026).** Inclusion in Grokipedia is non-uniform. Rewriting is more frequent for pages with higher reference density and recent controversy, and very popular pages are more often reproduced without modification. — [arXiv:2602.05519](https://arxiv.org/abs/2602.05519)
- **Other Grokipedia comparison studies.** A citation study covers 1,000 pairs and about 600k citations; political-framing studies cover 1,394 pairs (2607.15146) and controversial topics (2601.15484); there is also a search-recommendation audit. — [2512.03337](https://arxiv.org/html/2512.03337); [2607.15146](https://arxiv.org/pdf/2607.15146); [2601.15484](https://arxiv.org/html/2601.15484); [2512.17027](https://arxiv.org/html/2512.17027v1)

**B. News rewrites (content farms)**
- **NewsGuard, Aug 2023.** 37 sites used chatbots to rewrite NYT, CNN and Reuters articles without credit. Some left chatbot error or refusal text in the published pages. NewsGuard said the true number was likely higher. — [NewsGuard Misinformation Monitor Aug 2023](https://www.newsguardtech.com/misinformation-monitor/august-2023); [Gizmodo](https://gizmodo.com/content-farms-ai-chatbots-plagiarize-news-nyt-1850770474)
- **NewsGuard tracker (self-reported).** It lists 3,749 "AI Content Farm" sites in 16 languages, last updated 23 Jun 2026. The full domain list is available to researchers on request. — [NewsGuard AI Tracking Center](https://www.newsguardtech.com/special-reports/ai-tracking-center/)
- **Hanley & Durumeric (ICWSM 2024).**
  - They classified 12.91M articles from 3,074 sites. — [arXiv:2305.09820](https://arxiv.org/abs/2305.09820)
  - Their repo releases code (Apache-2.0) and domain lists: 1,059 unreliable and 2,015 reliable sites.
  - Article URLs and the DeBERTa detector are available by Google-form request only, and the URL data is research-only.
  - The repo has paraphrase and perturbation notebooks but no released synthetic-to-source article pairs.
  — [GitHub hanshanley/machine-made-media](https://github.com/hanshanley/machine-made-media)
- I found no published dataset that aligns content-farm AI rewrites with their source wire, NYT or Reuters articles.

**C. Q&A with human and AI answers to the same question**
- **HC3 (measured row counts).**
  - 24,322 questions: reddit_eli5 17,112, finance 3,933, medicine 1,248, open_qa 1,187, wiki_csai 842.
  - Each question carries both human and ChatGPT (2022-23) answers.
  - License: CC BY-SA 4.0, or the stricter license of the source dataset.
  — [Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3)
- **HC3 with Gemini 2.0 Flash (published).** 23,463 answers to HC3 questions, MIT license. The released columns are only `Text` and `Is_AI`, with no question ID, so they cannot be aligned directly to HC3 human answers. — [SES-Lab-OTH/HC3-Gemini-Flash-Responses](https://huggingface.co/datasets/SES-Lab-OTH/HC3-Gemini-Flash-Responses)
- **Stack Overflow human-vs-ChatGPT studies are small (published).**
  - 130 threads ([2310.02104](https://arxiv.org/abs/2310.02104)).
  - 517 questions ([Kabir et al. 2308.02312](https://arxiv.org/pdf/2308.02312v2)).
  - 442 Python and 182 Java questions ([2307.09765](https://arxiv.org/pdf/2307.09765)).
  - 2,564 questions ([2409.17473](https://arxiv.org/abs/2409.17473v1)).
- **Stack Exchange terms.** Since Jul 2024 the data dump sits behind a login and an agreement that restricts LLM training. Critics say this conflicts with CC BY-SA. — [devclass](https://devclass.com/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-as-critics-complain-license-permits-reuse-for-any-purpose); [heise](https://heise.de/-9823083)
- **No Robots (measured).** 10,000 human-written prompt/response pairs (9,500 train, 500 test), CC BY-NC 4.0. — [HuggingFaceH4/no_robots](https://huggingface.co/datasets/HuggingFaceH4/no_robots)
- **Beemo (NAACL 2025).**
  - Built on No Robots prompts and human outputs in five categories: Generation, Rewrite, Summarize, Open QA, Closed QA.
  - Outputs come from 10 open instruction-tuned LLMs of the 2023-24 era (Zephyr, Tulu-2, Gemma, Llama-2, Mistral, and others).
  - Expert edits plus GPT-4o and Llama-3.1-70B edits. The HF train split has 2,187 rows. The paper reports 6.5k human texts and 13.1k machine-generated and LLM-edited texts. License: MIT.
  — [toloka/beemo](https://huggingface.co/datasets/toloka/beemo); [arXiv:2411.04032](https://arxiv.org/abs/2411.04032)
- **Search Arena (measured row count).** 24,069 in-the-wild conversations with search-augmented LLMs, 18 Mar to 8 May 2025, 13 models. It includes "LLM + web search trace", so the AI answer can in principle be paired with the human pages it cited. Prompts are CC-BY-4.0; model outputs fall under each provider's terms. — [lmarena-ai/search-arena-24k](https://huggingface.co/datasets/lmarena-ai/search-arena-24k)

**D. Search and aggregator summaries**
- **Google AI Overviews: no paired release found.**
  - The closest published work decomposes AI search responses into 98,020 atomic claims and finds 11.0% unsupported by the cited pages (Mar-Apr 2026). — [arXiv:2605.14021](https://arxiv.org/html/2605.14021v1)
  - Another study covers 11,000 queries across GPT, SearchGPT and AI Overviews. — [arXiv:2603.16138](https://arxiv.org/pdf/2603.16138v1)
  - A 2026 HF panel on AI Overviews and Wikipedia traffic contains derived counts only, no text. — [audiofreak7/wikipedia-ai-overviews-panels-2026-09](https://huggingface.co/datasets/audiofreak7/wikipedia-ai-overviews-panels-2026-09)
- **Amazon review highlights.** No public corpus of live highlights paired with their source reviews. Academic work builds its own approximations (AMCIS 2025; INFORMS ISR appendix). The only Amazon-released summaries are PASS summaries for 32 FewSum products (CDLA-Sharing). — [AMCIS 2025](https://aisel.aisnet.org/amcis2025/data_science/sig_dsa/8); [ISR appendix](https://pubsonline.informs.org/doi/suppl/10.1287/isre.2024.1282/suppl_file/isre.2024.1282.sm1.pdf); [AWS Open Data FewSum](https://registry.opendata.aws/pass-summaries-fewsum)
- **AI recipe sites.**
  - Futurism reports Decrypt Ads found about 2,100 AI-slop recipe domains. — [Futurism](https://futurism.com/?p=405537)
  - Bloggers report AI-cloned recipe catalogs with lightly rephrased instructions. These are secondary, opinion-style reports. — [implicator.ai](https://www.implicator.ai/the-algorithm-ate-your-grandmothers-recipe)
  - Fortune-sourced reporting says AI Overviews merge recipes from several bloggers. — [Search Engine Land](https://searchengineland.com/google-ai-slop-thanksgiving-food-bloggers-465200)
  - No dataset found.

**E. Paraphrase and humanizer corpora (human→AI or AI→humanized)**
- **Wahle et al. (EMNLP 2022).** 200,000 GPT-3 and T5 paraphrases of text from 20,966 arXiv preprints, 39,241 Wikipedia articles and student theses. — [arXiv:2210.03568](https://arxiv.org/pdf/2210.03568.pdf)
- **Older spinner data (iConference 2022).** SpinBot and SpinnerChief paraphrases: 200,767 paragraphs from 8,024 Wikipedia articles. — [Zenodo](https://zenodo.org/records/3608000)
- **ltg/en-wiki-paraphrased.** Mistral-7B-Instruct-v0.1 paraphrases of the top 10% most-visited Wikipedia articles, about 400M words, Apache-2.0. — [HF card](https://huggingface.co/datasets/ltg/en-wiki-paraphrased)
- **APT-Eval (ACL Findings 2025).**
  - 14,650 rows (measured) of human text polished by GPT-4o, Llama3.1-70B, Llama3-8B, Llama2-7B and DeepSeek-V3.
  - Domains: blog, email, game review, news, paper abstract, speech.
  - Polish levels run from extreme_minor to major, plus percentage-based polishing. License: MIT.
  — [smksaha/apt-eval](https://huggingface.co/datasets/smksaha/apt-eval)
- **EditLens (ICLR 2026).**
  - All human sources predate 2022: Amazon and Google reviews, WritingPrompts, FineWeb-EDU, XSum, CNN/DM, and Enron as the out-of-distribution set.
  - Edits and generations are by GPT-4.1, Claude Sonnet 4 and Gemini 2.5 Flash, with Llama-3.3-70B held out. There are 303 edit prompts.
  - Size: 60k train, 2.4k validation, 6k test, from 22,690 unique training source texts.
  — [arXiv:2510.03154](https://arxiv.org/html/2510.03154v1)
  - The HF dataset is gated. The license is reported as CC BY-NC-SA 4.0 (secondary source). — [pangram/editlens_iclr](https://huggingface.co/datasets/pangram/editlens_iclr); [papernotes summary](https://en.papernotes.org/ICLR2026/aigc_detection/editlens_quantifying_the_extent_of_ai_editing_in_text/)
- **DetectRL-X (ACL 2026).**
  - Paired `human_written_text` / `llm_generated_text` fields.
  - 8 languages × 4 LLMs (DeepSeek-V3, Gemini-2.5-Flash, GPT-4o, Qwen-Max) × 6 domains, including News.
  - 124,800 samples per strategy file. Strategies include polishing, expanding, condensing and paraphrasing.
  - About 31 GB binary plus 18 GB ternary data. License: MIT.
  — [WUJUNCHAO/DetectRL-X](https://huggingface.co/datasets/WUJUNCHAO/DetectRL-X)
- **MIRAGE / DetectAnyLLM (Sep 2025).** Over 93K human/machine pairs from 10 corpora in 5 domains, using 17 LLMs for generate, polish and rewrite. One table lists 13 commercial LLMs, so the model count is inconsistent. — [arXiv:2509.14268](https://arxiv.org/html/2509.14268v1)
- **DAMAGE (Jan 2025).** Audits 19 humanizer and paraphrasing tools. The pair-dataset size is not in the abstract. — [arXiv:2501.03437](https://arxiv.org/abs/2501.03437)
- **"Humanized but Still True?" (30 Oct 2026).**
  - Covers 11 commercial humanizers plus one open 12B humanizer, applied to fact-dense U.S. federal agency text, which is a public-domain human side.
  - Code and data are on GitHub (`zwang-devv/humanizer-fact-audit`).
  — [arXiv:2611.00359](https://arxiv.org/abs/2611.00359)

**F. Constructed pair corpora (synthetic AI side, human side real)**
- **HAP-E / HAP-E-2 (published; file list measured).**
  - 12,000 human texts (2,000 in each of academic, news, fiction, spoken, blogs, TV/movie).
  - The LLM continues a 500-word human chunk; the real next 500 words are the human side. That gives 8,290 texts per LLM.
  - HAP-E-2 files cover Llama-3 8B/70B base and instruct, Gemma-2 9B/27B base and it, gpt-4o, gpt-4o-mini, gpt-5-mini-2025-08-07 and claude-haiku-4-5-20251001. License: MIT.
  — [HAP-E](https://huggingface.co/datasets/browndw/human-ai-parallel-corpus); [HAP-E-2](https://huggingface.co/datasets/browndw/human-ai-parallel-corpus-2)
- **GPT-wiki-intro (measured).** 150,000 pairs of Wikipedia intros and text-curie-001 intros, prompted with the title plus the first 7 words. — [aadityaubhat/GPT-wiki-intro](https://huggingface.co/datasets/aadityaubhat/GPT-wiki-intro)
- **RAID.**
  - 11 generators (GPT-2/3/4, ChatGPT, Llama-2-chat, Mistral, MPT, Cohere, with base and chat variants).
  - Genres include news, wiki, abstracts, recipes and reviews. 4 decoding settings, 12 attacks.
  - `source_id` links each generation to its human text, and titles drive the prompts. License: MIT.
  — [liamdugan/raid](https://huggingface.co/datasets/liamdugan/raid)
- **MAGE.** 436,606 rows (measured). — [yaful/MAGE](https://huggingface.co/datasets/yaful/MAGE)
- **STORM FreshWiki.** Under 1k Wikipedia articles (most-edited Feb 2022 to Sep 2023) for STORM-generated vs human comparison, CC BY-SA. — [EchoShao8899/FreshWiki](https://huggingface.co/datasets/EchoShao8899/FreshWiki)

### Inferences
- **Grokipedia (best natural, large, recent pair source, but noisy).**
  - Ranking by scale × recency × informational register × retrievability, Grokipedia v0.1 paired with Wikipedia is the best natural source: about 880k topic-aligned pairs, all encyclopedic and written by Grok in Oct 2025.
  - The CC-labelled ~56% are mostly light rewrites that contain human text. Use them as "AI-edited" pairs, not clean AI text.
  - The non-CC ~44% (~385k) are full AI write-ups. Those are the cleanest AI side.
  - It is one model family (Grok) with one production pipeline. That makes it a strong but narrow negative.
- **Grokipedia terms (estimated).** Terms are the weak point. For local, non-distributed research use, the risk is lower. Redistributing the non-CC text or a model trained on it is governed by xAI's terms. Treat that as a legal question, not settled.
- **Pre-2022 human side.** Swapping the 2025 Wikipedia side for each article's last revision before 2022 removes post-ChatGPT contamination. In my pilot the 2021 and 2025 revisions share 65-92% of content words (see the next question), so topic alignment barely changes. At scale, use the Wikimedia history dumps (dumps.wikimedia.org) rather than the API: the REST and parse endpoints returned HTTP 429 to my pilot after about 6 articles at a rate of one request every 3 s.
- **DetectRL-X and EditLens (best constructed-but-recent options).**
  - DetectRL-X (MIT, paired fields, 2025 models, news among its 6 domains) and EditLens (2025 frontier models, human sources before 2022, edit magnitude labelled) are the best ready-made constructed sets.
  - EditLens's non-commercial license and gating matter only if quill is ever distributed.
- **News-farm and aggregator pairs.** These would be the most "natural slop", but there is no released pair set. Building one means crawling farm domains (NewsGuard list on request, Common Crawl) and near-duplicate matching to wire copy. Both sides are copyrighted. Expect weeks of work for maybe low thousands of clean pairs (estimated).
- **Q&A.** HC3 is the only ≥10k same-question human/AI QA set with IDs, and its AI side is 2022 ChatGPT. Regenerating HC3 questions with current models is cheap, since the human answers are CC BY-SA.

### Gaps
- Grokipedia-specific terms of service could not be read (404). The share of CC-notice articles in the v0.2 (~5.86M) corpus is unknown. All 12 popular pages I sampled lacked the notice, which may mean high-traffic pages were rewritten, but the sample is far too small to generalize.
- No public full-text dump of Grokipedia v0.2 was found; the HF mirrors are all v0.1. Scraping 5.86M pages at about 0.5 MB each is roughly 3 TB of HTML (estimated).
- I did not read the Lawfare investigation directly, and there is no official xAI statement on update status.
- No public dataset of Stack Exchange AI answers that were deleted after the Dec 2022 ban was found, and I could not confirm from primary docs whether dumps include deleted posts.
- No public Quora/Poe paired data, Fandom AI-page data, AI Stack Overflow-clone data, Yelp highlight data, or press-release vs AI-rewrite corpus was found.
- MIRAGE's license and exact model list were not verified. Neither were RAID's per-domain human-document counts or MAGE's model list.

## How good is the alignment (same facts?) and how would we verify it cheaply?

### Takeaway
Alignment ranges from near-verbatim to topic-only:
- **CC-labelled Grokipedia pages and EditLens/APT-Eval edits** are fact-aligned by construction, but they are partly human text.
- **Non-CC Grokipedia pages** are topic-aligned only. My pilot found almost no shared 4-grams and 14-38% entity overlap with the 2021 Wikipedia article, at 1.0-1.5× the length. They are the same subject with different content selection, not the same facts.

A cheap verification stack is:
1. Chunk-level embedding cosine.
2. Entity and number recall in both directions.
3. n-gram containment, to flag copying.
4. A length ratio.

The published thresholds below give starting cut-offs.

### Cited Findings
- **Grokipedia similarity (published).** Mean chunk embedding cosine is 0.90 for CC-licensed and 0.77 for non-CC articles (bimodal). The median non-CC article is about 4.6× longer than Wikipedia. — [arXiv:2511.09685](https://arxiv.org/html/2511.09685)
- **Lexical vs semantic gap (published).** Lexical overlap is far lower than semantic overlap: TF-IDF cosine 0.505, unigram Jaccard 0.362, trigram overlap 0.250, against embedding cosine 0.825. BERTScore F1 is 0.193 (unreconciled in the paper). — [arXiv:2510.26899v2](https://arxiv.org/html/2510.26899v2)
- **Pilot (measured, 2026-11-07).**
  - 6 informational topics. The Grokipedia page as served on 2026-11-07 was compared with the last English Wikipedia revision before 2022-01-01 (revisions dated 2021-12-07 to 2021-12-30).
  - None of the 6 pages carried the CC notice.
  - Entities were approximated as capitalized multi-word phrases plus 3-4 digit numbers.

  | Topic | Grok words | Wiki-2021 words | Length ratio | Content-word Jaccard | Grok 4-grams found in Wiki-2021 | Grok sentences ≥50% 8-gram-copied | Wiki-2021 entities found in Grok | Grok entities found in Wiki-2021 |
  |---|---|---|---|---|---|---|---|---|
  | Bicycle | 10,828 | 7,028 | 1.54 | 0.210 | 0.2% | 0/358 | 13.8% | 13.8% |
  | Coffee | 13,514 | 10,385 | 1.30 | 0.243 | 0.4% | 0/425 | 21.3% | 28.4% |
  | Great Barrier Reef | 6,261 | 6,308 | 0.99 | 0.216 | 1.1% | 0/192 | 35.8% | 39.6% |
  | Penicillin | 8,327 | 5,431 | 1.53 | 0.266 | 0.7% | 1/288 | 37.7% | 33.7% |
  | Photosynthesis | 7,967 | 6,510 | 1.22 | 0.274 | 0.9% | 0/280 | 26.4% | 20.9% |
  | Plate tectonics | 7,827 | 7,572 | 1.03 | 0.262 | 0.7% | 0/269 | 29.6% | 23.9% |

  - For reference, Wikipedia's own 2021 vs 2025 revisions of these pages share 0.65-0.92 content-word Jaccard.
  - Scripts and outputs are in `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/priors/scripts/` and `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/priors/dl_pilot/`.
- **EditLens edit magnitude (published).**
  - Measured as cosine distance between Linq-Embed-Mistral embeddings of source and edit, plus "soft n-gram" overlap.
  - Human validation: Krippendorff's α of 0.67 (cosine) and 0.66 (soft n-grams).
  - Thresholds: at least 0.03 cosine distance (0.06 soft n-gram) to count as AI-edited, and 0.15 cosine distance (0.72 soft n-gram) to count as fully AI-generated.
  — [arXiv:2510.03154](https://arxiv.org/html/2510.03154v1)
- **Humanizer fact audit (published).**
  - "Checkable units" are numbers, names and quoted spans.
  - Commercial humanizers changed or dropped at least one checkable unit in 35-65% of documents that contained one. 10 of 11 tools altered at least one number or name in 20% or more of documents.
  - Unit retention did not track detector evasion (Spearman ρ = -0.46, CI -0.65 to 0.08).
  — [arXiv:2611.00359](https://arxiv.org/abs/2611.00359)
- **Atomic-claim support (published).** AI search answers checked against their cited pages at the claim level: 11.0% of 98,020 claims were unsupported, with omission the dominant failure. — [arXiv:2605.14021](https://arxiv.org/html/2605.14021v1)
- **Two-stage generation (published).** Liang et al. found that prompting from titles or keywords alone produces "unrealistic text with fabricated results". They instead summarize each human paragraph into an outline and then expand it, which keeps facts aligned by construction. — [arXiv:2404.01268](https://arxiv.org/html/2404.01268)
- **GPT-wiki-intro anchoring.** It conditions only on the title plus the first 7 words, so its AI side shares the topic but not the facts. — [GPT-wiki-intro card](https://huggingface.co/datasets/aadityaubhat/GPT-wiki-intro)

### Inferences
- **Recommended cheap verification per pair (estimated, local on an M4 Pro).**
  - (a) Chunk both texts into about 250 tokens and keep pairs whose best-match chunk cosine averages ≥0.80 (a small local embedding model is enough).
  - (b) Require ≥50% recall in both directions of numbers and named entities (spaCy NER or the regex above). This is what separates "same facts" from "same topic".
  - (c) Reject pairs where more than 10% of AI-side sentences are 8-gram copies of the human side, or treat those as edit pairs.
  - (d) Keep the length ratio within 0.7-1.5, or truncate both sides to matched spans.
- **Grokipedia non-CC pages.** Whole-article pairs would mostly fail (b) at 14-38% entity overlap. Align at paragraph or section level with embedding search and keep only mutually-best-matching paragraph pairs with high entity overlap. That should yield many paragraph pairs per article (estimated) where the facts genuinely match.
- **Constructed pairs.** Outline→expand pairs pass (b) almost by construction. Pass the outline the human text's numbers and names explicitly, then check recall.

### Gaps
- The pilot is n=6 popular science/culture pages, with a regex entity proxy. It is not representative of the 5.86M-page corpus, and paragraph-level alignment yield was not measured.
- No study was found that reports paragraph-level fact alignment between Grokipedia and pre-2022 Wikipedia.

## Is a natural pair source materially better than constructed pairs from our own pre-2022 human corpus? Any evidence?

### Takeaway
No study compares natural and constructed pairs head-to-head as training negatives for style models. Indirect evidence says:
- Constructed pairs from current instruction-tuned models reproduce the systematic stylistic gap robustly and transfer to real-world data at the population level.
- They under-represent real-world mixing: human-edited AI text, humanizer output, and pipeline-specific quirks such as Grokipedia's length inflation, FK grade 19 and citation style.

Constructed pairs from quill's own pre-2022 corpus should therefore be the backbone, because they give exact content control. Add natural pairs, mainly Grokipedia non-CC paragraphs, as a small out-of-distribution slice and an evaluation set, not as the main signal.

### Cited Findings
- **Reinhart et al., PNAS 2025 (HAP-E).**
  - Same preceding human context, LLM vs human continuation.
  - A random forest separates human text from any single LLM with roughly 93-98% accuracy.
  - GPT-4o uses present participial clauses at 5.3× the human rate (d = 1.38) and nominalizations at 2.1× (d = 1.23). It uses agentless passives at about half the human rate.
  - Instruction-tuned models diverge more than base models; Llama-3 base is close to human.
  - Classifiers trained on instruction-tuned output transfer above chance to M4 arXiv abstracts; base-model-trained ones reach about 50%.
  — [arXiv:2410.16107v2](https://arxiv.org/html/2410.16107v2); [PNAS DOI listed](https://arxiv.org/abs/2410.16107)
- **Liang et al. 2024.** Their constructed outline→expand references (gpt-3.5-turbo-0125) gave less than 3.5% population-level error on validation mixtures built from pre-ChatGPT papers. That is a controlled test, not labelled real-world AI text. They were then used to estimate real LLM use across 950,965 papers. — [arXiv:2404.01268](https://arxiv.org/html/2404.01268)
- **Liang et al. peer reviews.** GPT-4-generated reviews served as the reference distribution. From them the authors estimated that 6.5-16.9% of ICLR, NeurIPS, CoRL and EMNLP 2023-24 reviews were substantially AI-modified. — [arXiv:2403.07183](https://arxiv.org/abs/2403.07183)
- **Beemo.** "Expert-based editing evades MGT detection", whereas "LLM-edited texts are unlikely to be recognized as human-written". So synthetic LLM edits do not mimic how humans post-edit AI text. — [arXiv:2411.04032](https://arxiv.org/abs/2411.04032)
- **Humanizer audit (Oct 2026).** On AI-styled rewrites by 2026 models, two perplexity-based detectors scored below chance (AUROC 0.37 and 0.39). The audit model Jev reached AUROC 0.864 but flagged 24% of human originals. — [arXiv:2611.00359](https://arxiv.org/abs/2611.00359)
- **Detector generalization.** Detectors are near ceiling on QA-style benchmark data but drop on meaning-preserving rewrites. In-distribution performance is "a weak proxy" under shifts in domain, style and generator. — [arXiv:2605.03969](https://arxiv.org/html/2605.03969)
- **Generator and setting diversity in published constructed sets.**
  - RAID: 11 generators × 4 decoding settings × 12 attacks. — [RAID card](https://huggingface.co/datasets/liamdugan/raid)
  - DetectRL-X: 4 vendors and 11+ rewriting strategies. — [card](https://huggingface.co/datasets/WUJUNCHAO/DetectRL-X)
  - EditLens: 3 in-distribution LLMs, 1 held-out LLM, 303 prompts. — [arXiv:2510.03154](https://arxiv.org/html/2510.03154v1)
  - HAP-E-2: 14 model files across 4 families. — [HAP-E-2](https://huggingface.co/datasets/browndw/human-ai-parallel-corpus-2)
- **Grokipedia's production style differs from generic chat-model style.** Flesch-Kincaid grade is 19.3 vs 12.8, references per 1k words 21.4 vs 90.2, and headings per 1k words 2.87 vs 5.58. — [arXiv:2510.26899v2](https://arxiv.org/html/2510.26899v2)

### Inferences
- **Constructed pairs win on control, natural pairs win on realism (estimated).**
  - For quill's purpose (push away from AI style without pushing away from topics), constructed pairs from its own pre-2022 corpus are materially better on content control. Outline→expand keeps the facts.
  - They also come in exactly the target authors' registers.
  - Natural sources add realism (a real production pipeline, real post-editing), but they bring topic drift (Grokipedia non-CC pages share only 14-38% of entities) and single-family bias (Grok).
- **Suggested construction recipe (estimated).**
  - ≥4 generator families. For example, two frontier APIs plus Qwen/Llama/Gemma-class open models, including whatever 7-9B base quill fine-tunes, so the negatives cover the model's own priors.
  - ≥3 tasks: outline→expand, "rewrite/polish this", and "explain this topic" from the outline alone.
  - 2 temperatures, and a few dozen prompt templates in the style of EditLens's 303.
  - Instruction-tuned generators matter most, because they carry the largest stylistic gap. Base models add little negative signal.
- **Natural pairs as a check (estimated).** Use Grokipedia paragraph pairs (filtered as in the previous question) and a regenerated-HC3 set as a held-out "real-world slop" check. If the style model trained on constructed negatives also moves away from Grokipedia paragraphs relative to their human counterparts, the constructed negatives are generalizing.

### Gaps
- No study was found that trains a generator or style model with natural vs constructed AI negatives and compares the outcomes.
- No study was found that quantifies how many generator models or prompts are needed for constructed negatives to cover real-world slop. The model counts above describe what benchmarks used, not measured requirements.
- Whether Grok-written Grokipedia text is stylistically representative of the 2025-26 "slop" quill wants to avoid (compared with ChatGPT, Claude or Gemini output) has not been measured.
