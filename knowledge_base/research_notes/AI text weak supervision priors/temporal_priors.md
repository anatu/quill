# Time as a label: temporal priors, same-URL before/after pairs, and within-author changepoints for weakly labeling human vs AI text (as of 2026-11-07)

Scope: using the ChatGPT launch (2022-11-30) as a natural experiment for the quill project (a QLoRA style model, 7-9B, MLX on an M4 Pro 24 GB, writing informational nonfiction in one human author's voice). The aim is to harvest large, weakly labeled human anchors and AI-contaminated contrasts with *known* noise rates.

Conventions used throughout:
- **[PUB-EST]**: a population-level estimate published in a peer-reviewed paper or preprint. The method is named each time.
- **[VENDOR]**: a claim by a company that sells detectors or SEO services.
- **[LOCAL]**: a number I measured myself on 2026-11-07 with read-only queries. The scripts and raw outputs are in `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/priors/` (`scripts/` and `dl/`).
- **[SNIPPET]**: taken only from a search-engine summary or a secondary article, and not checked against a fetched primary page.
- **[PRIOR-KNOWLEDGE]**: from my background knowledge and not re-verified in this session.

---

## Q1. Published AI-share priors by source and month: what is measured, how, and with what error

### Takeaway
Two families of measurement now exist.
- **Distributional MLE.** This is the Liang/Zou word-frequency mixture estimator. It gives corpus-level fractions with errors below about 2-3 points, and it is a lower bound. The domain priors it gives are:
  - consumer complaints 17.7% (Aug 2024)
  - press releases 16-24% (2024)
  - UN press releases 13.7% (Q3 2024)
  - small-firm job postings up to 14% (Oct 2023)
  - CS paper sentences up to 22% (Sep 2024)
  - peer reviews 6.5-16.9% (2023-24)
  - PubMed abstracts at least 13.5% (2024)
- **Detector-based web studies.** For crawlable pages, the best-corrected number is about 24% in Aug 2026 (Bayesian error-corrected over 71 Common Crawl snapshots). It is about 29.5% on .com, 6% on .edu/.gov, 11.6% in the top PageRank tier and 27.5% in the tail. Vendor studies put "new articles" at about 50% from 2025 onward.

Before 2022-12 the measured AI share is about zero: 0.2 pp/yr growth through Feb 2023. The rise lags launch by 3-5 months.

### Cited Findings

**A. Distributional (MLE / word-frequency) estimates. These are corpus-level, not per-document.**

- **Liang et al. 2025, "The widespread adoption of large language model-assisted writing across society"** (arXiv 2502.09747, v1 2025-02-13). It covers Jan 2022-Sep 2024 with 687,241 consumer complaints, 537,413 corporate press releases, 304.3M job postings and 15,919 UN press releases. — [arXiv abs](https://arxiv.org/abs/2502.09747)
  - Venue: listed as *Patterns* 6(12), DOI 10.1016/j.patter.2025.101366 **[SNIPPET]**. — [researchr](https://researchr.org/publication/LiangZCWCZ25/bibtex)
  - **CFPB complaints [PUB-EST]:**
    - The pre-ChatGPT baseline is 1.5% (treated as false positives). The share rose to 15.3% by Aug 2023 and 17.7% by Aug 2024, and growth began about 3-4 months after launch.
    - By state (Jan-Aug 2024): Arkansas 29.2%, Missouri 26.9%, North Dakota 24.8% at the top; West Virginia 2.6%, Idaho 3.8%, Vermont 4.8% at the bottom; California 17.4%, New York 16.6%.
    - Highly urbanized areas reached 18.2% versus 10.9% for the rest.
    - Lower-bachelor's-attainment areas reached 19.9% versus 17.4% (2024Q3).
    - Source data is the public CFPB Consumer Complaint Database. — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - **Corporate press releases [PUB-EST]:**
    - Source: NewsAPI (newsapi.ai, a commercial API).
    - By distributor: Newswire peaked at 24.3% (Dec 2023) and was 23.8% through Sep 2024. PRNewswire was about 16.4-16.5%. PRWeb plateaued around 15% (data end Jan 2024).
    - Pre-ChatGPT baseline: about 2-3%.
    - By category, Q4 2023: Science & Tech 16.8% on both PRNewswire and PRWeb.
    - The paper contradicts itself in one place: one passage says Newswire exceeded 25%. — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - **Job postings [PUB-EST]:**
    - Source: Revelio Labs data sourced from LinkedIn. It is licensed via Stanford GSB and **not public**. The sample is 304,270,122 postings, Jan 2021-Oct 2023.
    - The full sample sits at about 3-4%. Small firms leveled at about 5-10% by Oct 2023, after a lag of about 5 months.
    - Firms founded after 2015 reached 14.1%, versus 4.0% for firms founded before 1980. — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - **UN press releases [PUB-EST]:**
    - Scraped from 97 UN country-team websites.
    - The share went 3.1% (Q1 2023) → 10.1% (Q3 2023) → 13.7% (Q3 2024). Latin America and the Caribbean reached about 20-21%. — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - **Method and error:**
    - Calibrated on pre-ChatGPT data (2021; 2019 for UN). The LLM reference corpus is built with a two-stage prompt: summarize to bullet points, then expand.
    - Validation on mixtures at 0-25%: population-level error stays below 3.3%. For example, a true 0% mixture of complaints is estimated at 1.8% and a true 25% at 26.5%; for UN releases, 0% → 2.5%.
    - 95% bootstrap CIs: about ±0.2-0.3 pp for press releases and about ±0.5-1.0 pp for job-posting categories.
    - The authors call the estimates a **lower bound** because heavily edited or human-imitating text is missed.
    - Using GPT-4 references gives marginally higher estimates. — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
- **Liang et al. 2024, peer reviews, "Monitoring AI-Modified Content at Scale"** (ICML 2024; arXiv 2403.07183) **[PUB-EST]:**
  - ICLR 2024: 10.6% (pre-ChatGPT 1.6%). NeurIPS 2023: 9.1% (1.9%). CoRL 2023: 6.5% (2.4%). EMNLP 2023: about 16.9%. Nature-portfolio reviews: no significant increase.
  - Validation error: below 1.8% in-distribution (ICLR 2023) and out-of-distribution (NeurIPS 2022), and below 2.4% on CoRL 2022.
  - Against instance-level classifiers, the best baseline's error was 6.2% in-distribution and 11.2% OOD. — [arXiv HTML v2](https://arxiv.org/html/2403.07183v2); [abs](https://arxiv.org/abs/2403.07183)
- **Liang et al. 2025, scientific papers** (*Nature Human Behaviour*, 2025-08-04, DOI 10.1038/s41562-025-02273-8) **[PUB-EST]:**
  - 1,121,912 arXiv/bioRxiv/Nature-portfolio papers, Jan 2020-Sep 2024.
  - Computer science reached up to 22%; mathematics and Nature portfolio up to 9%. Press coverage gives 22.5% of CS abstract sentences, 9.8% physics, 7.8% math.
  - Higher rates go with first authors who post preprints more often, crowded fields and shorter papers. — [Stanford PDF](https://nlp.stanford.edu/~manning/papers/Liang_et_al-2025-Nature_Human_Behaviour.pdf); [search summary of NHB](https://www.nature.com/nature-index/article/10.1038/s41562-025-02273-8)
  - The earlier preprint covered 950,965 papers to Feb 2024: CS 17.5%, math and Nature 6.3%. — [arXiv 2404.01268](https://arxiv.org/abs/2404.01268)
- **Kobak et al. 2025, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary"** (*Science Advances*, 2025-07-02) **[PUB-EST]:**
  - 15,103,888 PubMed abstracts. Excess frequency is measured against a linear extrapolation from 2021-2022; 2023 is excluded as possibly contaminated.
  - "At least 13.5% of 2024 abstracts were processed with LLMs" (rare-word set Δ=0.136, 10 common words Δ=0.134).
  - Subgroups range from below 5% to more than 40%: computational fields ≈0.20, Chinese computational papers 0.41, *Sensors* 0.25, *Nature/Science/Cell* 0.07.
  - For comparison, COVID-related words gave Δ=0.069. Excess words numbered 190 in 2021 and 454 in 2024; no word had δ>0.01 in 2013-2019.
  - The lower bound holds because abstracts without marker words do not contribute.
  - Data (a 362,442×15 yearly word-count matrix) is on Zenodo and code is at `berenslab/llm-excess-vocab`. — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/)
- **Geng & Trotta 2024** analyze about 1M arXiv abstracts (May 2018-Jan 2024) with GPT-3.5 rewrites of pre-2023 abstracts as the reference. ChatGPT's influence is growing, strongest in CS. — [arXiv 2404.08627](https://arxiv.org/abs/2404.08627). A secondary summary gives "≈35% of CS abstracts by early 2024" **[SNIPPET, unverified]**. — [Moonlight review](https://themoonlight.io/review/is-chatgpt-transforming-academics-writing-style)

**B. Detector-based prevalence on the web and platforms.**

- **Visokay, McCormick et al., "The uneven rise of AI-generated web content"** (arXiv 2610.36631, 2026-10-27; the newest and most careful CC study) **[PUB-EST]:**
  - Data: 5,118,347 pages from 505,974 domains across 71 Common Crawl snapshots (Jan 2019-Aug 2026). Per crawl, 20,000 domains are drawn across six PageRank strata and pages are reservoir-sampled from the index, about 72k pages per crawl. Only pages with at least 500 characters of trafilatura text count. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
  - **Overall share:** about 24% in Aug 2026 (95% CrI 22.9-24.4), up 21.7 pp since Dec 2021. Average growth was 0.2 pp/yr (Jan 2019-Feb 2023), 4.6 pp/yr (Feb 2023-Jan 2025) and 8.1 pp/yr (Jan 2025-Aug 2026). — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
  - **By TLD (Aug 2026):**
    - .com 29.5%, .net 20.4%, .org 14.6%, .edu 6.1%, .gov 5.8%.
    - Feb-Mar 2024 values: .com 7.0%, .edu 2.1%, .gov 2.5%.
    - By PageRank tier: the top tier is 11.6% (11.2-11.9) and the tail 27.5% (26.5-28.4). Bottom and tail tiers account for 78.8% of the net increase.
    - By language: English-only pages 32.8%, non-English 17.0%, bilingual 20.2%. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
  - **Detectors:** open Pangram (a QLoRA adapter on Llama-3.2-3B, from the EditLens release) and Binoculars-Falcon (English only).
    - Open-Pangram control-period FPR is 4.5% on English-only pages, 28.5% on bilingual pages, and 9.0-12.9% by tier on English pages.
    - Sensitivity on fully-AI English RAID text: open Pangram 0.720, Binoculars-Falcon 0.727.
    - Commercial Pangram 4 flagged **2 of 20,100** control (2019-2021) pages.
    - A Bayesian measurement-error model takes specificity from 30 pre-2022 control crawls and sensitivity from benchmarks, then poststratifies by language, length, tier and TLD. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
  - Pew's comparison figure is 10%. On all English captures without extraction, the same detector flags "roughly 13 to 19 percent" **[SNIPPET via secondary article]**. — [FourWeekMBA summary](https://fourweekmba.com/ai-written-text-reaches-24-of-web-pages-up-from-near-zero/)
- **Dolezal, Alam, Graham (Internet Archive) & Bohacek, "The Impact of AI-Generated Text on the Internet"** (arXiv 2604.26965, 2026-04-14) **[PUB-EST]:**
  - Data: Wayback Machine URLs first archived on or after 2022-01-01, using longitudinal sampling with a target of 10,000 URLs/month and one URL per host. The oldest snapshot is used, English only, Aug 2022-May 2025.
  - Result: about **35% of newly published websites** were AI-generated or AI-assisted by mid-2025 (Pangram v3), up from about 0 before launch.
  - Pangram failed to detect davinci-002/babbage-002 text. Pangram provided a research grant.
  - The study does **not** compare the same URL over time. — [arXiv HTML](https://arxiv.org/html/2604.26965v1)
- **He et al., DeGenTWeb** (arXiv 2605.00087, v2 2026-10-26) **[PUB-EST]:**
  - 20.9% of Common Crawl sites (Jan-Jul 2026) and 13.6% of sites linked from Bing results (2025) are "MGT-dominant", defined as sites whose informational prose is mostly machine-generated. These are lower bounds.
  - 0.12% of human sites are mislabeled. Data is promised after publication. — [arXiv abs](https://arxiv.org/abs/2605.00087)
- **Graphite (SEO agency) "More articles are now created by AI than humans"** **[VENDOR]:**
  - 2025 version: Common Crawl articles with article schema, at least 100 words, publish dates Jan 2020-May 2025, Surfer detector on 500-word chunks.
  - Error rates: FPR 4.2% on 15,894 articles dated Jan 2020-Nov 2022 (assumed human); FNR 0.6% on 6,009 GPT-4o articles.
  - Results: about 39% AI 12 months after launch; AI passed human in Nov 2024; plateau thereafter. URLs are withheld.
  - Sample size is reported inconsistently: 43k on the page, about 65k in Axios. — [Graphite](https://graphite.io/five-percent/more-articles-are-now-created-by-ai-than-humans); [Axios 2025-10-14](https://www.axios.com/2025/10/14/ai-generated-writing-humans)
  - 2026 update ("AI Now Writes as Many Online Articles as Humans", with GPTZero): averages Pangram, GPTZero and Copyleaks. Results: 36% at 12 months, 48% at 24 months, about 50% since Q1 2025. FPR and FNR are reported "below 2%". The figure is 3.3 pp lower than the single-detector estimate.
  - Sample is about 55,400 articles through Mar 2026 per Copyleaks coverage **[SNIPPET]**. — [GPTZero post 2026-05-19](https://gptzero.me/news/ai-written-web/); [Axios 2026-05-15](https://axios.com/2026/05/15/human-vs-ai-written-articles)
- **Ahrefs (2025-05-19)** **[VENDOR]:** 900,000 new English pages from April 2025, one per domain, scored with the in-house `bot_or_not` detector. 74.2% "contain AI content", but only 2.5% are pure AI; 25.8% are pure human and 71.7% mixed. — [Ahrefs](https://ahrefs.com/blog/what-percentage-of-new-content-is-ai-generated)
- **Hanley & Durumeric, "Machine-Made Media"** (ICWSM 2024; arXiv v5 2024-03-20) **[PUB-EST, relative only]:**
  - 15.46M articles from 3,074 news and misinformation sites, scored with a DeBERTa detector.
  - Between 2022-01-01 and 2023-05-01, synthetic articles grew **+57.3% on mainstream** and **+474% on misinformation sites**. The abstract gives no absolute share. Model weights and URLs are released on GitHub. — [arXiv](https://arxiv.org/abs/2305.09820); [project page](https://hanshanley.github.io/publication/machine-made)
- **Russell, Karpinska, …, Iyyer, "AI use in American newspapers is widespread, uneven, and rarely disclosed"** (arXiv 2510.18774; ACL 2026) **[PUB-EST, Pangram co-authors]:**
  - 186K articles from 1.5K US newspapers, summer 2025. About 9% are partially or fully AI.
  - NYT/WaPo/WSJ opinion pieces are flagged at 4.5%, versus 0.7% for news.
  - Only 5 of 100 flagged articles disclosed AI use. — [arXiv](https://arxiv.org/abs/2510.18774v1); [ACL Anthology](https://aclanthology.org/2026.acl-long.663/)
- **Brooks, Eggert, Peskoff, "The Rise of AI-Generated Content in Wikipedia"** (arXiv 2410.08044; WikiNLP 2024) **[PUB-EST]:** up to 5% of 2,909 new English articles from Aug 2024 contain significant AI text (GPTZero flagged 156, Binoculars 96). Thresholds are calibrated to about 1% FPR on pre-GPT-3.5 articles, so this is a lower bound. — [arXiv HTML](https://arxiv.org/html/2410.08044v1)
- **Sun et al., "Are We in the AI-Generated Text World Already?"** (ACL 2025) **[PUB-EST]:** the AI attribution rate went from Jan 2022 to Oct 2024 as follows: Medium 1.77% → 37.03%, Quora 2.06% → 38.95%, Reddit 1.31% → 2.45%. About 2.4M posts were scored with OSM-Det. — [arXiv](https://arxiv.org/abs/2412.18148)
- **Platform vendor claims [VENDOR]:**
  - Pangram: over 47% of 274,466 Medium posts over six weeks (WIRED, Oct 2024).
  - Originality.ai on Medium: 3.4% in 2018 versus over 40% in 2024 (n=473). — [NewsBytes summary](https://www.newsbytesapp.com/news/science/medium-faces-significant-surge-of-ai-content-robot-bloggers/story)
  - Originality.ai on LinkedIn: 54% of 8,795 long-form posts (Nov 2024). — [Originality.ai](https://originality.ai/blog/ai-content-published-linkedin); [The Register](https://www.theregister.com/2024/11/28/linkedin_ai_posts)

**C. Corpus availability (who can replicate the priors).**
- **CFPB complaints** are public through an API that needs no key. **[LOCAL]** Counts of complaints with public narratives by year received:
  - 2019: 277,554; 2020: 444,836; 2021: 496,475; 2022: 801,453
  - 2023: 1,293,801; 2024: 2,739,721; 2025: 5,452,074; 2026 to date: 6,313,908
  - All complaints, all years: 18,996,256 — [CFPB search API](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/)
- **[LOCAL]** Credit reporting was 62.0% of 2021 narratives and **88.4% of 2025 narratives**. — [CFPB search API](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/)
- **CFPB license:** public narratives are opt-in. A third-party HF mirror lists CC0 **[SNIPPET; no CFPB license statement found]**. — [PIRG guide](https://pirg.org/edfund/articles/how-to-explore-consumer-problems-in-the-financial-marketplace-using-the-cfpbs-consumer-complaint-database/); [HF mirror](https://huggingface.co/datasets/emperor-mew/cfpb-complaints)
- **Other corpora:**
  - Not public: press releases (NewsAPI, commercial) and job postings (licensed Revelio/LinkedIn). — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - Public: PubMed (bulk download) — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/) — and arXiv/bioRxiv.
  - Withheld: Graphite URLs. — [Graphite](https://graphite.io/five-percent/more-articles-are-now-created-by-ai-than-humans)
  - Released: Hanley & Durumeric URLs. — [arXiv](https://arxiv.org/abs/2305.09820)

### Inferences
- **Priors for quill-relevant informational nonfiction (approximate, as of 2025-26):**

  | Source | AI share | Basis |
  |---|---|---|
  | Top-tier/central sites (curated corporate and brand blogs) | ~11-15% | Visokay top tier 11.6%, .org 14.6% |
  | Long-tail .com | ~27-30% | Visokay tail tier and .com |
  | New "articles" | ~50% | Vendor figure; includes SEO farms |
  | US newspaper articles | ~9% | Russell et al. |
  | New Wikipedia articles | at least 5% in 2024 | Brooks et al. |
  | PubMed abstracts | at least 13.5% in 2024 | Kobak et al. |
  | CS paper sentences | ~22% | Liang et al. 2025 |

  These are different estimands: share of sentences modified, share of documents flagged, and "contains any AI" (Ahrefs) are not comparable. Ahrefs' 74% versus 2.5% shows how much the definition matters.
- **Safe cutoffs.** Capture or crawl date before 2022-12-01 is near-certainly free of ChatGPT-era text. Dec 2022-Feb 2023 is low-contamination, since growth stays at 0.2 pp/yr until Feb 2023 and the rise lags launch by 3-5 months. Use crawl or capture timestamps, not page-claimed publish dates.
- **Publish-date calibration can fail.** Graphite calibrated on pages *dated* 2020-2022, so pages refreshed later could inflate its 4.2% "FPR". My zapier and HubSpot tests found 37-42% of pre-ChatGPT blog URLs heavily rewritten by 2026 (Q2).
- **Detector-based shares rise faster than distributional ones** (2026 web 24-50% versus 2024 domain-text 14-24%). This reflects later dates, document-level flags rather than token share, and different populations. For priors, prefer the error-corrected Visokay numbers for crawlable pages and the Liang-family numbers for specific institutional genres.

### Gaps
- No month-by-month table was retrievable for Visokay et al. (only anchor dates), for Dolezal et al. (figure only), or for Graphite (chart and spreadsheet only).
- I found no per-genre estimate for "how-to/explainer blogs" specifically, or for Substack or company blogs, with published error bars.
- I could not fetch the original WIRED/Pangram Medium analysis.
- The Liang 2025 *Patterns* publication details are snippet-only.
- The CFPB license and consumer copyright status of narratives are unverified.

---

## Q2. Same-URL temporal pairs from Common Crawl and the Wayback Machine: feasibility, yield and precision

### Takeaway
Same-URL pairs are feasible and cheap, but **not** through the public CC CDX server. It returned 504s on every query I made on 2026-11-07. The CC **columnar (parquet) index**, read over HTTPS with row-group pruning, returned a whole domain prefix in 20-220 s per crawl.

On two refresh-heavy marketing/how-to blogs, about 12-13% of pre-ChatGPT (May 2022) URLs reappeared in one 2026 crawl. Of the matched pairs, **39% (21/54; Wilson 95% CI about 27-52%) were heavily rewritten** (5-gram Jaccard below 0.3), and heavily rewritten pages grew a median 1.4×.

Major publishers (Healthline, Investopedia, AP) now block CCBot, so post-2023 CC pairs under-represent exactly the high-quality sources. No published study measures LLM "content refresh" at page level. A rewrite by itself carries only the population prior (roughly 12-30% AI for this tier), so rewritten pages must be detector-filtered before they can serve as AI labels.

### Cited Findings

**Infrastructure (measured and documented)**
- **[LOCAL]** `collinfo.json` lists 129 crawls, CC-MAIN-2021-49 through CC-MAIN-2026-43 (Oct 2026). — [CC index](https://index.commoncrawl.org/collinfo.json)
- **[LOCAL]** CC CDX lookups on 2026-11-07 (around 19:45-20:30 local) almost all failed:
  - One 5-row prefix query returned HTTP 200 in 9.1 s.
  - Every later prefix query (limits 500-3000, with or without filters) and every exact-URL lookup (CC-MAIN-2022-21, CC-MAIN-2026-39) returned **504 Gateway Time-out** after about 10 s. — [CC index server](https://index.commoncrawl.org/)
- CC's FAQ says 503s from index.commoncrawl.org mean "slow down", and blocked IPs should wait 24 h. CC recommends the columnar index (Athena, Spark, or local DuckDB over parquet) for large filtering. A mailing-list post says the columnar index "rarely has traffic problems". — [CC FAQ](https://commoncrawl.org/faq); [CC status page](https://status.commoncrawl.org); [CC Google group](https://groups.google.com/g/common-crawl/c/BvMGYUY-dro)
- **[LOCAL]** Columnar index layout and performance:
  - Each crawl's `cc-index-table.paths.gz` lists 300 `subset=warc` parquet files. They are SURT-sorted, with 4-9 row groups per file and min/max statistics on `url_surtkey`, so a domain prefix maps to one or two row groups.
  - Scanning the footers of all 300 files took about 14 s. Extracting one prefix took 22-23 s (zapier), 83 s (HubSpot 2022) and 218-226 s (Investopedia).
  - data.commoncrawl.org returned **503** at 6 parallel threads. Two threads with backoff worked, but one footer read failed in each of two runs.
  - Script: `scripts/cc_columnar.py`. — [CC-MAIN-2022-21 cc-index-table.paths.gz](https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-21/cc-index-table.paths.gz)
- **Scale context.** Visokay et al. counted 194.9B captures over 71 crawls (about 2.7B per crawl), of which 58% had at least 500 characters of text. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
- **[LOCAL]** The Wayback CDX API works but was slow on 2026-11-07:
  - 8.6 s for a prefix listing, about 20 s for a per-URL `limit=-25` query.
  - Some digest-collapse and `id_` fetches timed out at 75 s.
  - I stopped two of three parallel jobs to stay polite. Only one prefix (zapier, n=20) completed. Script: `scripts/wb_pairs.py`. — [Wayback CDX API](https://web.archive.org/cdx/search/cdx)

**Measured pair statistics [LOCAL] (CC-MAIN-2022-21 = May 2022 versus CC-MAIN-2026-39 = Sep 2026, via the columnar index plus WARC range fetches)**

| Prefix | 2022 captures / 200-HTML URLs | 2026 captures / 200-HTML URLs | Same URL in both | Pairs diffed (≥150 words both sides) | Heavy rewrite (J5<0.3) | Moderate (0.3-0.6) | Light/boilerplate (0.6-0.98) |
|---|---|---|---|---|---|---|---|
| zapier.com/blog/ | 1,371 / 1,148 | 1,155 / 973 | 152 (13.2% of 2022) | 24 | 10 (42%) | 3 (12%) | 11 (46%) |
| blog.hubspot.com/marketing/ | 4,029 / 2,243 | 2,126 / 908 | 268 (11.9%) | 30 | 11 (37%) | 3 (10%) | 16 (53%) |
| **Pooled** | | | | **54** | **21 (39%)** | 6 (11%) | 27 (50%) |

Source for all rows: [CC columnar index](https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-39/cc-index-table.paths.gz); WARC records from [data.commoncrawl.org](https://data.commoncrawl.org/). Text is main-content `<p>/<li>/<h2>/<h3>` from the largest `<article>`/`<main>`, with a fallback to body. J5 is 5-gram shingle Jaccard.

- **[LOCAL]** WARC digests were identical for **0%** of matched URLs. Whole-HTML digests always change (templates, scripts), so digest equality is useless as a "content unchanged" test. — [same source]
- **[LOCAL]** The 0.6-0.98 band mixes real light edits with boilerplate change. The first extractor version (first `<article>` only) gave 38% exactly identical (J=1.0) for zapier. The body-fallback version moved those to 0.83-0.95, so treat that band as "article mostly unchanged". — [same source]
- **[LOCAL]** Heavy rewrites are longer: median new/old word ratio is 1.42 pooled and 1.99 for HubSpot. Spot checks show they are often **re-titled and re-scoped** ("B2C marketing trends 2022" became "What is B2C Marketing? [+ New Data & Trends … 2025]"), with new first-person anecdotal openings, CTAs and affiliate disclosures. — [same source]
- **[LOCAL]** A crude LLM-marker rate (about 35 words and 9 phrases per 1k words) barely moved: heavy rewrites 1.34 → 1.57, light/unchanged pages 1.21 → 1.31. With n this small the shift is not meaningful. — [same source]
- **[LOCAL] Wayback, zapier.com/blog/ (20 random URLs captured 200 between Jun 2021 and Oct 2022):**
  - 18 were still HTTP 200 at their last 2025-26 capture; 2 were not captured since 2025; none redirected or 404'd.
  - Median number of distinct content digests since 2022-12: 6 (range 2-53).
  - Of 17 pairs diffed: heavy 3 (18%), moderate 3 (18%), light 8 (47%), identical 3 (18%).
  - — [Wayback CDX API](https://web.archive.org/cdx/search/cdx)
- **[LOCAL]** About 87% of 2022 URLs were "absent" from the 2026 crawl, but in Wayback 18/20 were still live. So that absence mostly reflects CC re-sampling each crawl, not deletion. — [same sources]
- **[LOCAL] robots.txt fetched 2026-11-07:** Healthline, Investopedia and AP News have `User-agent: CCBot / Disallow: /`. CNET lists CCBot in a blocked user-agent group (the rule body was not captured). HubSpot and Zapier do not block CCBot.
  - Matching columnar counts: Healthline `/health/` had 973 rows in 2022-21 and 0 in 2026-39. Investopedia `/terms/` had 6,453 rows in 2022-21 and 0 in 2026-39 (one footer read failed in the 2026 run). — [healthline robots.txt](https://www.healthline.com/robots.txt); [investopedia robots.txt](https://www.investopedia.com/robots.txt); [apnews robots.txt](https://apnews.com/robots.txt)
- Longpre et al., "Consent in Crisis" (arXiv 2407.14933, 2024): from 2023 to 2024, "~5%+ of all tokens in C4, or 28%+ of the most actively maintained, critical sources in C4" became fully restricted by robots.txt, and ToS restrictions cover 45% of C4. — [arXiv](https://arxiv.org/abs/2407.14933)
- Pew (2024-05-17): 38% of pages in 2013 CC samples were inaccessible by Oct 2023, about 1 in 5 of 2021 pages, and 8% of 2023 pages. About 90k pages were sampled per year, and only definitive error codes were counted. — [Pew Research](https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/)
- Garg et al. 2025, "Longitudinal Sampling of URLs From the Wayback Machine": TimeMaps of 27.3M URLs and 3.8B captures (1996-2021). It is a sampling framework that Dolezal et al. adapted (first-archival time, not same-URL diffs). — [arXiv 2507.14752](https://arxiv.org/abs/2507.14752)
- **Prior published work on LLM content refresh:** none found. Searching for page-level LLM rewrite detection over time (Wayback or CC) surfaced only adjacent work: recency bias in LLM rerankers, and a vendor study (Seer) finding 89% of LLM-cited pages were updated in 2023-2025. — [arXiv 2509.11353](https://arxiv.org/html/2509.11353v1); [Seer Interactive](https://www.seerinteractive.com/insights/study-ai-brand-visibility-and-content-recency) **[VENDOR]**
- **Refreshes predate LLMs.** HubSpot's "historical optimization" program found 76% of monthly blog views and 92% of monthly leads came from posts published before that month. Optimized posts gained an average 106% in organic views (self-reported). — [HubSpot blog](https://blog.hubspot.com/marketing/historical-blog-seo-conversion-optimization)
- **FineWeb as a zero-crawl route:**
  - FineWeb has per-dump configs with `url`, `date` (crawl time) and `dump` columns.
  - MinHash dedup is applied **within each dump individually**, so the same URL can recur across dumps with extracted text. That allows joining dumps on URL without WARC fetches.
  - It covers 110 dump configs, CC-MAIN-2013-20 to CC-MAIN-2025-26. — [FineWeb card](https://huggingface.co/datasets/HuggingFaceFW/fineweb); [datasets-server first-rows](https://datasets-server.huggingface.co/first-rows?dataset=HuggingFaceFW/fineweb&config=CC-MAIN-2022-21&split=train)

### Inferences
- **Yield per site.** A refresh-heavy corporate blog with about 1-2k crawled URLs per crawl gives about 150-270 same-URL pairs per (old crawl, new crawl) combination, of which about 40% are heavy rewrites (about 60-105 per blog). Taking the union over several 2021-22 crawls and several 2025-26 crawls should raise URL overlap well above 12%. That is unmeasured; Wayback suggests about 90% of these URLs are still live.
- **Yield at web scale.** If the 12% one-crawl-pair overlap generalized to the roughly 2.7B captures per crawl, there would be about 10^8 raw pairs per crawl pair. This is an **unverified extrapolation**. Expect lower overlap in the tail, many non-English pages, and robots.txt attrition. The practical route is FineWeb (dumps 2021-04…2022-49 joined with 2024-xx…2025-26) or the columnar index restricted to a curated domain list (how-to, SaaS blogs, explainers).
- **Expected precision that a rewritten page is AI-written, with no detector.** P(AI | rewritten) ≈ the prior for new text on that tier: about 12% (top tier) to 27-30% (.com tail), with vendor estimates up to about 50%.
  - Rewriting may raise this above the prior. LLM-assisted refreshes are cheap, and heavy rewrites were 1.4-2× longer. No source measures it.
  - The HubSpot evidence shows human-driven refreshes were already standard practice, so rewrites are not themselves an AI signal.
- **Pair labels.** The old side is a high-precision human anchor (see Q6 for ε_h). The new side is an *unlabeled, content-matched* text. Its best use for quill is (a) as a topic-matched contrast, scored by a detector before use as a negative, or (b) as a source of human→refresh edit pairs whose direction of change can be studied in aggregate.
- **Blocking bias.** Because major health, finance and news publishers block CCBot after 2023, CC-based post-period samples are skewed toward sites that permit crawling, and those sites lean toward the long tail. Use Wayback for blocked domains; it archived Healthline and Investopedia URLs independently of CC, though that is not re-tested here.

### Gaps
- Global URL-overlap and rewrite rates across many domains were not measured: only 2 domains in CC and 1 in Wayback. n=54+17 pairs gives wide CIs.
- No detector was run on the new-side texts, so the AI share among rewrites is unmeasured. Running open Pangram (EditLens) locally on about 100 pairs would close this.
- Wayback throughput for a larger test is unknown, because the service was slow during testing.
- No published page-level "LLM content refresh" study exists, as far as these searches show.

---

## Q3. Within-author changepoints: methods and evidence that individual authors shift toward LLM style after 2023

### Takeaway
Author-level adoption has been measured at scale only for scientists. Kusumegi et al. (*Science*, 2025) tracked 168,553 preprint authors and dated each author's "adoption" as the first manuscript whose abstract exceeds a distributional LLM-signal threshold. Lin & Zhu and Xu et al. use adopter-versus-non-adopter difference-in-differences.

PAN's style-change task detects authorship switches *within* a document and is now at F1 0.83 on topic-controlled hard data. It does not handle dating a change in one author's output across time. That needs standard changepoint methods (PELT, BOCPD) on per-document stylometric distance series.

I found no published per-author changepoint study for bloggers, Medium, Substack, LinkedIn or company blogs. Two diffusion effects make marker-word changepoints noisy: humans imitate LLM vocabulary (Yakura et al.) and authors deliberately drop flagged words (Geng & Trotta).

### Cited Findings
- **Kusumegi, Yang, Ginsparg, de Vaan, Stuart, Yin, "Scientific production in the era of large language models"** (*Science* 390(6779):1240-1243, 2025; arXiv 2601.13187):
  - Detection: "a text-based AI detection algorithm" applied to all abstracts. Human token distributions come from pre-2023 abstracts and LLM distributions from GPT-3.5-turbo-0125 rewrites of those abstracts.
  - Adoption: an author's "initial adoption … marked by the first manuscript … such that α(mj) > τ". Adoption status is 0→1 for all later months. Core-AI subfields are excluded to avoid topic confounds.
  - Sample: 168,553 authors, Jan 2022-Jul 2024 (arXiv 109,965; bioRxiv 43,218; SSRN 15,370), drawn from 2.1M preprints. Authors are compared against matched non-adopters in author-fixed-effects stacked DiD event studies.
  - Effects: productivity +36.2% (arXiv), +52.9% (bioRxiv), +59.8% (SSRN). For authors with East Asian names: +43.0% / 70.9% / 70.1%.
  - Stated limits: abstracts only; cannot say which co-author used the LLM; "almost certainly fails to detect use by authors who heavily edit"; adoption time may be endogenous. — [arXiv PDF text, local copy](https://arxiv.org/abs/2601.13187); [ScienceDaily](https://sciencedaily.com/releases/2025/12/251224032347.htm)
- **Lin & Zhu 2025, "Divergent LLM Adoption and Heterogeneous Convergence Paths in Research Writing"** (arXiv 2504.13629): 627k+ arXiv papers with a fine-tuned discipline-specific classifier for ChatGPT-revised style. Adoption differs by discipline, gender, native language and career stage. Non-native and junior authors show the largest stylistic shifts, and DiD shows convergence. — [arXiv](https://arxiv.org/abs/2504.13629)
- **Xu, Ye, Zhang, Wang 2024** (arXiv 2408.17325, cond-mat abstracts, DiD): non-native English authors show significant improvement in English quality, with more "unique words" and fewer rare words. The effect is significant for Latin and Ural-Altaic language groups but not Germanic. — [arXiv](https://arxiv.org/abs/2408.17325)
- **Liang et al. 2025 (NHB)** finds higher LLM share for first authors who post preprints more often, an author-level correlate. — [Stanford PDF](https://nlp.stanford.edu/~manning/papers/Liang_et_al-2025-Nature_Human_Behaviour.pdf)
- **Geng & Trotta 2025, "Human-LLM Coevolution: Evidence from Academic Writing"** (Findings of ACL 2025; arXiv 2502.09606): "delve" and other flagged words dropped soon after they were publicly flagged in early 2024, while "significant" kept rising. The authors attribute this to author behavior, not model updates, and say it complicates detection. — [arXiv](https://arxiv.org/abs/2502.09606v1)
- **Yakura et al.** (arXiv 2409.01754): transcripts of about 280k academic YouTube talks (later versions cover 740,249 hours of talks and podcasts) show "a measurable and abrupt increase" in ChatGPT-preferred words ("delve", "comprehend", "boast", "swift", "meticulous") in *spoken* language after release. This is evidence of human imitation. — [arXiv](https://arxiv.org/abs/2409.01754v2)
- **PAN Multi-Author Writing Style Analysis 2025:**
  - Task: sentence-level change detection between consecutive sentences in Reddit-derived documents. There are three difficulty sets (easy = multi-topic, medium, hard = single topic with similar sentences), each of 6,000 documents split 70/15/15. Data is on Zenodo record 14891299.
  - Best macro-F1: easy 0.959, medium 0.825, hard 0.830. The naive baseline scores 0.44.
  - 2024 bests were 0.991 / 0.887 / 0.863.
  - Task history: style breach 2017 → paragraph-level 2020-22 → sentence-level 2022 → topic-controlled 2023-25. — [PAN 2025 task page](https://pan.webis.de/clef25/pan25-web/style-change-detection.html); [Zangerle et al. overview, CEUR Vol-4038](https://ceur-ws.org/Vol-4038/paper_279.pdf)
- PAN 2026 runs "Voight-Kampff Generative AI Detection" alongside Multi-Author Writing Style Analysis. — [PAN 2026 overview, arXiv 2602.09147](https://arxiv.org/pdf/2602.09147)
- **Generic changepoint algorithms** suitable for per-author time series: Bayesian Online Changepoint Detection (Adams & MacKay 2007) — [arXiv 0710.3742](https://arxiv.org/abs/0710.3742); PELT exact linear-time penalized changepoints (Killick, Fearnhead, Eckley 2012) — [arXiv 1101.1438](https://arxiv.org/abs/1101.1438) **[PRIOR-KNOWLEDGE for IDs and attribution]**.

### Inferences
- **A workable recipe for quill.**
  1. For each candidate author with dated work (Substack/Medium via RSS or archive pages, company-blog bylines, arXiv with ORCID-disambiguated IDs), build a pre-2022 stylometric centroid. Use function-word frequencies, punctuation rates, sentence-length distribution and POS n-grams, which are mostly topic-independent.
  2. Score each later document on three signals: distance to that centroid, a detector score, and an LLM-marker rate.
  3. Run PELT or BOCPD on the series and accept only changepoints after 2023-03 that show a sustained shift.
  4. Subtract the platform-wide drift estimated from matched non-adopter authors, as in Kusumegi/Lin-Zhu DiD. Yakura and Geng-Trotta show that vocabulary drifts even without LLM use.
- **Labels from this.** Pre-changepoint (and especially pre-2022-12) documents are high-precision human. Post-changepoint documents are "AI-assisted" with precision equal to the detector's PPV at the author's estimated adoption share. These per-author before/after pairs fix voice and roughly fix topic. That makes them better contrasts for a *style* model than population-level negatives.
- **For quill's target author.** Treat their own post-2023 output as suspect. Train only on pre-2022-12 text, or screen later text with the changepoint test.
- **Marker words decay.** Do not rely on single words such as "delve", which authors adapt away from (Geng & Trotta). Function-word and syntactic features are more robust, and distributional detectors should be recalibrated per period.

### Gaps
- I found no published per-author LLM-adoption or changepoint study for bloggers, Medium/Substack writers, LinkedIn posters or company blogs. The only author-level evidence is for scientists.
- The adopter fraction by date and the detector threshold and validation in Kusumegi et al. are in the SM, which was not read.
- Lin & Zhu's adopter fraction and threshold are not given on the abstract page.
- I found no benchmark for cross-time, within-author LLM-adoption changepoints. PAN covers within-document change only.

---

## Q4. Confounds in before/after contrasts and how to control them

### Takeaway
Every temporal contrast is confounded by things that changed alongside LLM adoption. The ones measured or documented here:
- **Topic drift**, including AI as a subject.
- **Template and boilerplate changes.** Whole-HTML digests matched 0% of the time in my test.
- **Human-driven SEO refreshes** that predate LLMs.
- **Corpus composition shifts.** CFPB narratives grew about 11× from 2021 to 2025, and credit reporting went from 62% to 88% of them.
- **Crawl selection.** robots.txt now blocks CCBot on Healthline, Investopedia and AP.
- **Non-native writers adopting tools.**
- **Humans imitating LLM vocabulary.**

Controls: hold URL, author or domain fixed; use topic-independent features; use difference-in-differences against matched non-adopters; calibrate per domain on that domain's own pre-2022 text.

### Cited Findings
- **Topic.** Kusumegi et al. exclude core AI subfields "to isolate the general productivity effects of LLMs from rapid growth in research on AI". — [arXiv 2601.13187](https://arxiv.org/abs/2601.13187)
- Kobak et al. separate *style* excess words from *content* words. COVID content words produced Δ=0.069, about half the 2024 style-word Δ. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/)
- **[LOCAL]** A related-post card on a 2026 HubSpot page was "Generative engine optimization KPIs that actually matter for marketing teams", showing AI-related topics entering marketing blogs. — [CC-MAIN-2026-39 WARC via columnar index](https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-39/cc-index-table.paths.gz)
- **Templates and boilerplate [LOCAL].**
  - 0% identical digests across 420 matched URLs.
  - A naive extractor's choice of the first `<article>` captured a related-post card (13 words) instead of a 6,165-word page.
  - Zapier's 2026 pages add an affiliate disclosure, and HubSpot's add CTA blocks.
  - — [CC columnar index + WARC](https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-21/cc-index-table.paths.gz)
- **Human refresh practice predating LLMs.** HubSpot historical optimization: 76% of views and 92% of leads come from older posts. — [HubSpot](https://blog.hubspot.com/marketing/historical-blog-seo-conversion-optimization)
- **Composition shift [LOCAL].** CFPB narratives went from 496,475 (2021) to 5,452,074 (2025), with credit reporting rising from 62.0% to 88.4%. — [CFPB API](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/)
- **Crawl selection.**
  - Consent in Crisis: 28%+ of critical C4 sources restricted in 2023-24. — [arXiv 2407.14933](https://arxiv.org/abs/2407.14933)
  - **[LOCAL]** CCBot is blocked by Healthline, Investopedia and AP. — [healthline robots.txt](https://www.healthline.com/robots.txt)
  - Visokay et al.: about 4/5 of the AI increase comes from peripheral domains. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
- **Non-native writers.**
  - Liang et al. note that detectors misclassify non-native writing and that shifts in user demographics can bias estimates. — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - The largest adoption effects are for authors with East Asian names. — [arXiv 2601.13187](https://arxiv.org/abs/2601.13187)
  - Non-native cond-mat authors' English improved. — [arXiv 2408.17325](https://arxiv.org/abs/2408.17325)
  - Non-native and junior scholars shift most. — [arXiv 2504.13629](https://arxiv.org/abs/2504.13629)
- **Language-level contamination of the human baseline.** Humans imitate LLM words in speech (Yakura) — [arXiv 2409.01754](https://arxiv.org/abs/2409.01754v2) — and deliberately avoid flagged words (Geng & Trotta) — [arXiv 2502.09606](https://arxiv.org/abs/2502.09606v1).
- **Machine text before 2022 (machine translation).** In ccMatrix, 57.1% of sentences belong to translation tuples spanning 3+ languages, and 9.4% of unique English sentences have at least one translation. — [Thompson et al., ACL Findings 2024](https://arxiv.org/html/2401.05749v1)
- **Older generators go undetected.** Pangram did not detect davinci-002 or babbage-002 output. — [arXiv 2604.26965](https://arxiv.org/html/2604.26965v1)
- **Detector false positives vary by group** (language, PageRank tier). Visokay et al. let sensitivity and specificity vary by group and poststratify. Open-Pangram FPR is 4.5% on English-only pages and 28.5% on bilingual pages. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)

### Inferences
- **Controls ranked by strength for quill.**
  1. Same author before/after, with author-specific pre-2022 calibration.
  2. Same URL with an unchanged H1/title. Re-titled pages are often topic changes, as seen in the HubSpot examples.
  3. Same domain and section with topic matching, for example by embedding nearest neighbors across periods.
  4. Population-level contrast only with a domain-specific pre-period baseline, as in Liang's 2021 calibration.
- **Features.** Use function words, punctuation and syntactic templates, and drop topical nouns and AI-topic terms. Always compare against a matched non-adopter drift series (DiD), because the language itself moved post-2023.
- **Extraction.** Use one extractor (e.g., trafilatura, as in Visokay and Dolezal) on both sides of a pair, and drop pairs whose boilerplate share changed. My extractor showed how easily boilerplate shifts J5 by 0.05-0.15.
- **Platform and editor turnover.** Bylines change (company blogs reassign posts), and platform migrations change templates. For company blogs, require the same byline on both sides before calling a change "the author's".

### Gaps
- No quantitative estimate exists of how much of the post-2023 marker-word rise in *web* text is human imitation versus LLM use. Yakura's result is for spoken academic language.
- Editor turnover on company blogs has no published measurement.

---

## Q5. Pre-2022 human anchor corpora available at scale, with licenses

### Takeaway
The cleanest large anchors are:
- **FineWeb** dumps CC-MAIN-2021-04 through CC-MAIN-2022-49 (ODC-By; per-dump configs with URL and crawl date; 15 dumps in 2021-22).
- **C4** (ODC-By; 2019 crawl).
- **Pre-Dec-2022 Wikipedia dumps or revision text** (CC BY-SA).
- **PG-19** (Apache-2.0; old books, zero AI but archaic style).

Watch the cutoffs. Dolma's CC slice runs to Mar 2023, RedPajama-v1 includes a 2023 dump, and the HF `wikimedia/wikipedia` snapshot is 20231101. All must be filtered by crawl or revision date. Since mid-2024 the Stack Exchange dump has sat behind a login with a no-LLM-training clause, so only older archive.org dumps are clean to use.

### Cited Findings
- **FineWeb** (HuggingFaceFW/fineweb):
  - License ODC-By; ungated; card last modified 2025-07-11.
  - 110 per-dump configs from CC-MAIN-2013-20 to CC-MAIN-2025-26. The 2021-22 dumps are 2021-04, -10, -17, -21, -25, -31, -39, -43, -49 and 2022-05, -21, -27, -33, -40, -49.
  - More than 18.5T tokens (originally 15T). Each crawl is deduplicated individually.
  - v1.1.0 (2024-05-31) reprocessed dumps CC-MAIN-2021-49 to 2023-40 for a deduplication bug.
  - Columns: `text, id, dump, url, date, file_path, language, language_score, token_count`. — [HF API](https://huggingface.co/api/datasets/HuggingFaceFW/fineweb); [FineWeb card](https://huggingface.co/datasets/HuggingFaceFW/fineweb); [datasets-server](https://datasets-server.huggingface.co/first-rows?dataset=HuggingFaceFW/fineweb&config=CC-MAIN-2022-21&split=train)
- **C4** (allenai/c4): ODC-By, ungated, configs en / en.noblocklist / en.noclean / realnewslike / multilingual. — [HF API](https://huggingface.co/api/datasets/allenai/c4). Built from an April 2019 CC snapshot **[PRIOR-KNOWLEDGE]**.
- **Dolma** (allenai/dolma): license changed to ODC-By on 2024-04-15. The CC portion (Dolma v1.6 CC and CC News) has a knowledge cutoff of **Mar 2023**, so it contains early-2023 crawl data. — [Dolma card](https://huggingface.co/datasets/allenai/dolma)
- **RedPajama-v1:** "five dumps from Commoncrawl" processed with cc_net. Licensing is "refer to the licenses of the data subsets". StackExchange comes from the Internet Archive. — [RedPajama-1T card](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T). The five dumps are 2019-30, 2020-05, 2021-04, 2022-05 and **2023-06** (the last is Jan/Feb 2023) **[PRIOR-KNOWLEDGE]**.
- **PG-19** (deepmind/pg19): Apache-2.0. — [HF API](https://huggingface.co/api/datasets/deepmind/pg19). Books published before 1919 **[PRIOR-KNOWLEDGE]**.
- **Wikipedia** (wikimedia/wikipedia on HF): CC BY-SA 3.0 / GFDL, with a single snapshot date of **20231101** across 323 configs. That is post-ChatGPT, so use older dumps or timestamp-filter revisions. — [HF API](https://huggingface.co/api/datasets/wikimedia/wikipedia)
- Brooks et al. found up to 5% of *new* Aug 2024 articles AI-flagged, and their pre-GPT-3.5 calibration set sat at about 1% FPR. — [arXiv 2410.08044](https://arxiv.org/html/2410.08044v1)
- **Stack Exchange:** in mid-2024 the dump moved to a logged-in profile download with an agreement excluding LLM training, and is no longer uploaded to archive.org. Critics and Archive Team say this conflicts with CC BY-SA. — [DevClass 2024-07-30](https://devclass.com/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-as-critics-complain-license-permits-reuse-for-any-purpose); [Archive Team wiki](https://wiki.archiveteam.org/index.php/Stack_Exchange)
- **CFPB complaint narratives before 2022-12 [LOCAL]:** 2019 277,554; 2020 444,836; 2021 496,475; 2022 801,453 (includes Dec 2022). This is a genre-specific human anchor with a published monthly AI curve after launch. — [CFPB API](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/)
- **FineWeb-2** (multilingual): ODC-By, 1,870 language configs. — [HF API](https://huggingface.co/api/datasets/HuggingFaceFW/fineweb-2)
- **Common Pile** comma_v0.1 training set: present on the Hub, but the card exposes no license field. — [HF API](https://huggingface.co/api/datasets/common-pile/comma_v0.1_training_dataset). It is an openly licensed corpus from EleutherAI and collaborators (2025) **[PRIOR-KNOWLEDGE]**.

### Inferences
- **Recommended anchor for quill (informational nonfiction).** Use FineWeb CC-MAIN-2021-xx to CC-MAIN-2022-40, filtered to explainer and how-to domains, plus pre-2022-12 Wikipedia revisions. Treat CC-MAIN-2022-49 (Nov/Dec 2022) as acceptable given the 3-5-month adoption lag, but tag it.
- **The same FineWeb config family gives the post-period too** (2024-xx to 2025-26). Pre- and post-period text then share one extraction and filter pipeline, which removes an extraction confound from temporal contrasts.
- **Licensing.** ODC-By (FineWeb, C4, Dolma) requires attribution and respect for the underlying content's terms. Per-page copyright still applies to web text, so for a locally trained style adapter this is the same exposure as any web-pretrained model. Wikipedia text is CC BY-SA.

### Gaps
- Per-dump token counts for FineWeb 2021-22 were not retrieved.
- C4's snapshot month and the RedPajama-v1 dump list were not re-verified in this session.
- Common Pile's license metadata and the current Stack Exchange archive.org dump history were not checked.

---

## Q6. Turning temporal priors into labels with known noise rates

### Takeaway
A timestamp is a high-precision *human* label and a low-precision *AI* label.
- **Human side.** Text captured before 2022-12 has a measured AI-flag rate as low as 2/20,100 (≈0.01%) with a strong commercial detector on 2019-2021 crawlable pages. Weaker detectors flag 1.5-4.5%, which is mostly false positives. Pre-LLM machine text (MT, spinners, GPT-3-era tools) adds unknown contamination that detectors under-detect.
- **AI side.** Text dated after 2023 is AI with probability equal to the source and month prior, about 10-50% (Q1). So "post-2023 = AI" is wrong for most documents.

The fix is to treat post-period text as an unlabeled mixture with a known class prior (PU or mixture-proportion learning). Alternatively, detector-filter it and compute the PPV from the prior and the detector's TPR/FPR. Same-URL and same-author pairs add matched controls but do not change this arithmetic.

### Cited Findings
- Distributional MLE gives corpus-level fractions with validated error below 1.8-3.3 pp and bootstrap CIs, but it explicitly cannot flag individual documents. — [Liang et al. 2025 HTML](https://arxiv.org/html/2502.09747v2); [Liang et al. 2024 peer reviews](https://arxiv.org/html/2403.07183v2); [NHB summary](https://www.nature.com/nature-index/article/10.1038/s41562-025-02273-8)
- Visokay et al. show how to get error-corrected prevalence. Treat flags as noisy indicators. Estimate specificity on pre-2022 control crawls, which are assumed to have almost no AI text, and sensitivity on benchmarks. Propagate the uncertainty. Detector errors were moderately correlated on AI text, which violates naive independence. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
- **Measured false-positive and pre-period flag rates:**
  - Pangram 4: 2/20,100 control pages (≈0.01%).
  - Open Pangram: 4.5% (English-only).
  - Surfer: 4.2% on articles dated 2020-2022. — [Graphite](https://graphite.io/five-percent/more-articles-are-now-created-by-ai-than-humans)
  - Liang MLE baselines: 1.5% (complaints), 2-3% (press releases). — [arXiv HTML v2](https://arxiv.org/html/2502.09747v2)
  - DeGenTWeb site-level: 0.12%. — [arXiv](https://arxiv.org/abs/2605.00087)
- **Measured sensitivities:**
  - Open Pangram 0.720 and Binoculars-Falcon 0.727 on fully-AI English (RAID). Open Pangram catches 94.2% of co-written texts, Binoculars-Falcon 34.1%. — [arXiv HTML](https://arxiv.org/html/2610.36631v1)
  - Graphite/Surfer FNR 0.6% on GPT-4o articles. — [Graphite](https://graphite.io/five-percent/more-articles-are-now-created-by-ai-than-humans)
  - Detectors miss older completion models. — [arXiv 2604.26965](https://arxiv.org/html/2604.26965v1)

### Inferences
- **Human-anchor noise ε_h for text captured before 2022-12.** About 0.01-0.1% for LLM-style text, using the Pangram 4 control rate as an upper bound on detectable AI. Add unmeasured pre-LLM machine text (MT, spun, templated) of perhaps a few percent in low-quality web tiers, and much less in Wikipedia, books or curated blogs. Reduce it with quality and domain filters and by dropping pages that are non-English or multi-way-parallel.
- **AI-side noise with time alone.** For a post-2023 document from source s in month t, P(AI)=π_{s,t}, so the label-flip rate is 1−π: about 70-90% for curated sites and about 50% for vendor "new articles". **Do not** use these as negatives directly. Use them in:
  - **PU learning** with known class prior π (for example, the Elkan-Noto correction **[PRIOR-KNOWLEDGE]**), or
  - **mixture-proportion estimation** against the pre-period anchor (the Liang MLE itself does this), or
  - **ranking**: score post-period text with a detector and keep the top tail.
- **PPV of detector-filtered post-period labels** (illustrative, using the measured rates above), where PPV = π·TPR / (π·TPR + (1−π)·FPR):

  | Detector | Prior π | PPV |
  |---|---|---|
  | Open Pangram (TPR 0.72, FPR 0.045), runs locally | 0.12 (top tier) | ≈ 0.69 |
  | Open Pangram | 0.25 | ≈ 0.84 |
  | Open Pangram | 0.50 | ≈ 0.94 |
  | Pangram 4 (FPR ≈ 0.0001, TPR assumed about 0.9) | 0.12 | ≈ 0.999 |

  Calibrate FPR on the *same domain's* pre-2022 pages. FPR varies 4.5-12.9% by tier, so a domain-specific FPR can move PPV by 10+ points.
- **Pairs and noise.**
  - In a same-URL or same-author pair, the old side carries ε_h noise.
  - The new side carries noise of 1−PPV, given the pair's prior. That prior is π for the tier, possibly higher for heavy rewrites, but unmeasured.
  - Pairs where the detector fires on the new side and not the old side are the cleanest contrastive examples. For a style model they come content-matched, the setting the earlier training-methods note favored for paired negatives.
- **Budget check for quill.** With FineWeb-scale anchors (billions of pre-2022 documents) the human side is unlimited. The binding constraint is a high-PPV AI side in informational nonfiction. Detector-filtered same-URL rewrites of explainer and how-to pages (about 40% of matched pairs are heavy rewrites; Q2) are a promising, measurable source. Run a local detector on a pilot of about 500 pairs to estimate the AI share among rewrites before scaling.

### Gaps
- There is no published estimate of pre-2022 contamination by pre-LLM machine text (MT, spinners, GPT-2/GPT-3 tools) for English informational web text specifically.
- No study reports detector TPR on *refreshed* (human→AI partial rewrite) pages. EditLens-style mixed-authorship detection is the closest.
- The PPV figures are illustrative. They rest on out-of-domain sensitivity (RAID) and an assumed Pangram 4 TPR on web text.
