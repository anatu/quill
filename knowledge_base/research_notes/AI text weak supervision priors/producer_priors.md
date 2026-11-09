# Producer-level priors: classifying authors and domains (not single texts) as AI-content producers, to harvest weakly labeled negatives at scale

Compiled 2026-11-07. Scope: signals about the producer (velocity, breadth, account and domain age, identity fakery, templating, network structure, artifact leaks) that raise P(AI) for everything a producer publishes.

How claims are labeled:
- **[MEASURED-HERE]**: I ran a read-only query on 2026-11-07. Scripts are in `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/priors/scripts/` and outputs in `.../scratchpad/priors/data/`.
- **[MEASURED]**: an independent or academic measurement.
- **[VENDOR]**: a measurement by a company that sells AI detection (Pangram, Originality.ai, Copyleaks, Surfer).
- **[SELF-REPORTED]**: the producer's own claim.
- **[SNIPPET]**: from a search summary or secondary rewrite, not checked against a fetched primary page.

Related notes in this KB:
- `AI slop negative signal/moderated_communities.md`: NewsGuard inclusion criteria, KDP disclosure, Wikipedia tags, Problematic Paper Screener.
- `AI slop negative signal/lexicons_and_detectors.md`: detector accuracy, including Binoculars and Pangram.
- `AI slop negative signal/social_platforms.md`: X/Reddit/HN terms of service and hiQ.
- `Nonfiction author style corpora/legal_and_acquisition.md`: Bartz, Kadrey and fair use.

This note does not repeat them.

---

## Q1. Which producer-level signals have measured precision (or strong case evidence) for identifying AI-content producers?

### Takeaway
The strongest measured result is **aggregating a text detector over many pages from one producer**. He, Govindan and Madhyastha (IMC 2025) reached 100% site-level accuracy on 120 out-of-distribution sites, where per-page accuracy was at most 93%. Their site-level false-positive rate on sites crawled entirely before ChatGPT was 1.22%.

Metadata-only signals have case evidence but almost no measured precision:
- velocity
- domain age or "zombie" status
- fake bylines and AI headshots
- topical breadth
- shared IDs

They work best as **priors that pick which producers to score**, not as labels on their own.

A single chatbot leak predicts very different things on different platforms:
- On X in 2022-23, only about 24% of accounts that posted "as an AI language model" were likely LLM bots. The other 76% were humans quoting ChatGPT.
- On websites without human bylines, NewsGuard's analysts found that every leak site they reviewed (49 of 49 in 2023) was mostly AI. That figure is analyst-verified, not a measured precision.

### Cited Findings

#### A. Signal catalog (summary table; details and sources in the sub-sections below)

| Signal (producer-level) | How to compute from public data | Best evidence of precision | Strength |
|---|---|---|---|
| **Detector aggregated over a producer's pages** | Sample 15-20 prose pages per site, score each with Binoculars, use the 9 score deciles as features, train a linear SVM | 100% OOD site accuracy on 120 sites; 1.22% site FPR on pre-ChatGPT sites (He et al., IMC 2025) [MEASURED] | **High** |
| **Chatbot error leak + no human byline** | Search for refusal/meta phrases, then check bylines and the About page | All 49 NewsGuard 2023 sites; later grown to 3,749 domains under 4 criteria [MEASURED by analysts] | High, but analyst-confirmed |
| **Visible prompt leak** (instructions left in the text) | Search for imperative prompt text ("rewrite this article…", "[Your Name]") | CopyCop: more than 90 French articles kept an English rewrite instruction [MEASURED, SNIPPET] | High for that producer |
| **Leak phrase on a social account** | Phrase search plus manual review | Only 24% of 100 sampled accounts were likely LLM bots (Yang & Menczer) [MEASURED] | **Low alone** |
| **Fake author identity** (AI or stock headshot, unverifiable byline, vanishing bios) | Reverse image search; GAN-face detectors | SI/AdVon case; LinkedIn GAN detector 99.6% TPR at 1% FPR (GAN only) [MEASURED] | High when found; detection misses diffusion faces |
| **Domain first seen after Nov 2022** | Common Crawl / Wayback first capture; crt.sh first cert; RDAP registration | 10.08% of sites first crawled 2024-25 are LLM-dominant, vs 4.30% of all sampled sites and 1.22% (FPR) of pre-ChatGPT sites [MEASURED] | Moderate (about 2.3× lift over base) |
| **Zombie / expired-domain repurposing** | Wayback capture gap of 12 months or more, then new content; RDAP registration later than first Wayback capture; sitemap holds no pre-gap URLs | Case evidence (Hairpin, Southwest Journal, Apple Daily); Domain-Z measured ≥27,758 residual-trust abuses (malware, pre-LLM) [MEASURED] | Moderate-high in combination |
| **Velocity** (items per producer per day) | Sitemap lastmod, RSS, WP REST, Wayback, KDP release dates, podcast RSS pubDates | Inception Point: 325 shows in one day; KDP: all 29 repeat authors in one sample judged AI [VENDOR]; "hundreds of articles a day" (NewsGuard) | Moderate; prolific humans exist |
| **Topical breadth** | Entropy of URL sections or categories per byline or site | Case evidence only (my Southwest Journal measurement below; NewsGuard generic names) | Low-moderate, unmeasured |
| **Network coordination** (shared GA/AdSense IDs, reply/retweet clusters, shared link targets) | Page source IDs; follow/reply graphs | fox8: reply-pair rate 0.2% vs 0.016% baseline; shared IDs can be misleading (5,700+ US gov sites share one GA ID) [MEASURED] | Moderate for expanding from seeds |
| **Org age and size** | Founding year, headcount | Small firms founded after 2015: 14.1% LLM-modified job posts, vs 4.0% for those founded before 1980 [MEASURED, distributional] | Weak (population-level) |
| **Author's preprint frequency** | arXiv submission counts per author | Positive association with LLM modification, no effect size in the abstract (Liang et al. 2024) [MEASURED] | Weak |
| **Platform base rate** | — | Medium about 47%; LinkedIn long posts 41-54%; Amazon front-page reviews 3% [VENDOR] | Sets the prior |

#### B. Aggregation over a producer's output (the best-measured lever)
- He, Govindan and Madhyastha (USC), "Did I Just Browse A Website Written by LLMs?", IMC 2025 poster, arXiv 2507.13933 (v1 Jul 2025, v2 Oct 2025). The pipeline extracts prose-like text with Trafilatura, scores each page with Binoculars, samples **15-20 pages per site**, and uses the **9 deciles of the site's Binoculars scores** as features for a **linear SVM** — [arXiv 2507.13933v2 PDF](https://arxiv.org/abs/2507.13933v2) [MEASURED-HERE: text extracted from PDF]
- Ground truth was two sets totaling 120 sites (2,630 pages). "Company": 30 Russell-2000 company sites, plus 30 LLM sites generated with Wix's AI builder (20 blogs each). "Personal": 30 IndieWeb blogs, plus 30 LLM sites built with B12.io. The model reached **100% OOD accuracy** in both directions (train on one set, test on the other). "Since Binoculars classifies with a threshold, its per-page accuracy is at best 93%". The SVM still separated the sites completely — [arXiv 2507.13933v2](https://arxiv.org/abs/2507.13933v2)
- In the wild, **search results (how-to):** the authors searched Bing for 2,000 **WikiHow article titles** and got 17,036 sites in the top 20. Of the 10,232 sites that yielded at least 15 pages (264,918 pages), **1,019 (9.96%) were LLM-dominant**, "often … generic blogs with many ads, written by made-up authors". They found no significant ranking penalty for LLM sites ("equal medians"). The paper also reports a "blurry boundary", with "many in-between sites" — [arXiv 2507.13933v2](https://arxiv.org/abs/2507.13933v2)
- In the wild, **Common Crawl:** of 10,479 random sites from 2020-2025 (284,523 pages), 451 (4.30%) were LLM-dominant. Of 4,938 sites crawled entirely after ChatGPT launched, 358 (7.25%). Of 764 sites first crawled in 2024-2025, 77 (**10.08%**). Of 1,315 sites crawled entirely before ChatGPT, **16 (1.22%) were misclassified as LLM**, the authors say mostly because of pages that slipped past their filters — [arXiv 2507.13933v2](https://arxiv.org/abs/2507.13933v2)
- Reddit: La Cava, Aiello and Tagarelli (arXiv 2510.07226, 8 Oct 2025) studied 51 subreddits over 2022-2024. Machine-generated text is "marginally present", with peaks "up to 9%" in some communities and months. It is "often concentrated in the activity of a small fraction of users" and most common in technical-knowledge and social-support subreddits. This is direct evidence that **AI text clusters by producer** — [arXiv 2510.07226](https://arxiv.org/abs/2510.07226v1)
- Hanley and Durumeric, "Machine-Made Media" (ICWSM 2024; arXiv v1 16 May 2023, v5 20 Mar 2024). They ran a DeBERTa synthetic-news detector over **15.46M articles from 3,074 news sites**, Jan 2022 to May 2023. Synthetic articles rose **57.3% on mainstream and 474% on misinformation sites** (v5 figures; earlier versions give 55.4/457 and 61.1/426). The rise was "largely driven by smaller less popular websites", and an interrupted time series shows a jump after ChatGPT on small and misinformation sites but not on large mainstream ones. No per-site shares or detector FPR appear in the abstract — [arXiv 2305.09820](https://arxiv.org/abs/2305.09820). The GitHub repo (Apache-2.0, last push 2024-10-09) ships `reliable_domains.txt` (30 KB) and `unreliable_domains.txt` (19 KB) plus classifier code — [github.com/hanshanley/machine-made-media](https://github.com/hanshanley/machine-made-media) [MEASURED-HERE via GitHub API]

#### C. Artifact seeding and propagation: how much does one leak predict the rest of a producer's output?
- **Social accounts (low precision).** Yang and Menczer, "Anatomy of an AI-powered malicious social botnet" (arXiv 2307.16336, 30 Jul 2023; JQD:DM 2024). Searching Twitter for "as an AI language model" from 1 Oct 2022 to 23 Apr 2023 returned **12,226 tweets from 9,112 accounts**. In a manual sample of 100 accounts, **76% "appear to be humans posting or retweeting ChatGPT output" and 24% were likely LLM bots** — [arXiv HTML](https://arxiv.org/html/2307.16336v1)
- In the same paper, the fox8 botnet (1,140 accounts) was found by expanding from **link targets** (fox8.news, cryptnomics.org, globaleconomics.news), not from the phrase. About 3% of bot tweets linked to those sites. The bots posted 1,205 self-revealing tweets, but the total tweet count is not reported, so the leak rate per account cannot be computed. The authors treat only self-revealing tweets as confidently attributable, and note that malicious prompts are more likely to trigger refusals, which biases the sample — [arXiv HTML](https://arxiv.org/html/2307.16336v1)
- Detectors failed at the account level in that paper. The OpenAI classifier peaked at F1 0.84 (threshold 52.7) on the labeled set, but **815 of 1,986 random accounts (41%) crossed that threshold**. GPTZero scored fox8 content near zero, and Botometer recall was close to zero. The coordination signals worked: a **reply-pair rate of 0.2% vs 0.016% at baseline**, and dense follow, reply and retweet components (1,036-1,058 accounts) — [arXiv HTML](https://arxiv.org/html/2307.16336v1)
- **Websites (high precision after analyst confirmation).** NewsGuard, "Rise of the Newsbots" (1 May 2023) found **49 sites in 7 languages**. Analysts searched Google, Bing, DuckDuckGo and a media-monitoring tool for chatbot error phrases (e.g., "as an AI language model", "I cannot complete this prompt"). They then checked other content on each site for AI phrases and with GPTZero. All 49 had at least one error-message article, and NewsGuard calls them "almost entirely written by" AI — [NewsGuard 2023](https://www.newsguardtech.com/special-reports/newsbots-ai-generated-news-websites-proliferating/)
- NewsGuard's tracker stood at **3,749 "AI Content Farm" sites in 16 languages** as of 2026-06-23. Inclusion requires all four of: a substantial AI share; little human oversight (e.g., error messages); a layout implying human writers; and no disclosure. The page cites output of "dozens of articles a day" — [NewsGuard AI Tracking Center](https://www.newsguardtech.com/special-reports/ai-tracking-center/). Real-time Pangram-assisted detection began in Mar 2026 (see moderated_communities.md).
- **Prompt leaks.** Recorded Future (Insikt Group, 9 May 2024) reported on CopyCop, a Russia-linked network. It published **more than 19,000 articles across 11 sites by end of March 2024**. More than 90 French articles still carried an English instruction to take a conservative stance against Macron's policies. The rewrites were attributed to uncensored Llama-3-8B variants — [secondary: bestofai summary of the Recorded Future/Wired coverage](https://bestofai.com/article/a-russia-linked-network-uses-ai-to-rewrite-real-news-stories) [SNIPPET; primary report not fetched]
- **Product listings.** In Jan 2024, Amazon listings were found titled with ChatGPT refusals ("I'm sorry but I cannot fulfill this request it goes against OpenAI use policy"), for items such as a dresser and a hose. Amazon reportedly removed them — [ChannelX, Jan 2024](https://channelx.world/2024/01/sorry-i-cannot-fulfill-this-request-as-it-goes-against-openais-use-case-policy/); [PYMNTS](https://www.pymnts.com/?p=1660684). The rest of those sellers' catalogs has not been studied.
- **Podcasts.** Podnews (2026-04-15) says one Inception Point Spanish-language biography episode "contained English AI-tool output asking for clarification", and that none of the shows disclose AI — [Podnews](https://podnews.net/update/ai-slop-overtakes-humans)
- **Common Crawl leak prevalence.** I found **no study** that counts chatbot-leak phrases across Common Crawl, or that measures what share of a leaking domain's other pages are AI. He et al.'s site-level pipeline is the obvious tool for measuring it. See Gaps.

#### D. Identity fakery (bylines, headshots, bios)
- Sports Illustrated / Arena Group: Futurism, 27 Nov 2023. Articles ran under bylines that could not be verified elsewhere online, and the author headshots were **for sale on a site selling AI-generated headshots**. The bios vanished after Futurism contacted the publisher. Arena said the content came from AdVon Commerce and that AdVon used pen names; it denied AI authorship — [Deseret News summary](https://www.deseret.com/2023/11/28/23980127/sports-illustrated-denies-it-published-stories-under-fake-bylines-with-ai-generated-pics-futurism)
- AdVon: Futurism, 8 May 2024. AdVon had its own AI text generator, "**MEL**". CMS screenshots suggested **more than 90,000 articles for hundreds of publications**. Gannett's Reviewed pulled fake-byline content, and the LA Times and McClatchy cut ties. AdVon says it uses AI alongside humans [SELF-REPORTED] — [Futurism](https://futurism.com/advon-ai-content); [NPR, 16 May 2024](https://www.npr.org/transcripts/1251917136)
- NewsGuard 2023 sites listed bylines as "Admin" or "Editor" or none. HarmonyHustle's "Alex" and "Tom" photos failed a reverse image search. HistoryFact.in's About page still read "[Your Name]". Of the 29 sites that listed contacts, 8 email addresses were invalid and 17 sites did not reply — [NewsGuard 2023](https://www.newsguardtech.com/special-reports/newsbots-ai-generated-news-websites-proliferating/)
- KDP self-help, Originality.ai, 28 Jan 2026 [VENDOR]: of 844 "Success" books, **29% of author bios** were likely AI, 8% likely human, and 63% missing or too short to grade. Book descriptions were 79% likely AI — [Originality.ai](https://originality.ai/blog/likely-ai-success-self-help-book-study)
- **Face detection precision.**
  - LinkedIn and UC Berkeley (2023): **99.6% TPR at 1% FPR** on StyleGAN 1-3 faces, using 100,000 real LinkedIn photos and 41,500 synthetic faces. It generalizes "somewhat" to Generated.photos but **not to Stable Diffusion** faces — [LinkedIn Engineering](https://engineering.linkedin.com/blog/2023/new-approaches-for-detecting-ai-generated-profile-photos); follow-up covering diffusion: [arXiv 2311.08577](https://www.emergentmind.com/papers/2311.08577)
  - Yang, Singh and Menczer (JOTS, Sept 2024) used eye-placement cues on 1,420 GAN-face accounts and estimated a prevalence of **0.021-0.044%** of active Twitter accounts (a lower bound, about 10K daily actives) — [arXiv 2401.02627](https://arxiv.org/pdf/2401.02627)
  - Ricker et al. found 0.052% prevalence among about 15M Twitter profile images, mostly from thispersondoesnotexist — [arXiv 2404.14244](https://arxiv.org/html/2404.14244v3)

#### E. Velocity
- **Podcasts.**
  - The Hollywood Reporter (Sept 2025) says Inception Point AI / Quiet Please has **more than 5,000 shows and more than 3,000 episodes a week at about $1 per episode**, each taking about an hour from idea to release [SELF-REPORTED] — [THR](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/). Indicator counted 4,749 Quiet Please shows on Spreaker [SNIPPET] — [Indicator](https://indicator.media/p/this-podcast-company-went-all-in-on-ai-it-shows)
  - Podnews (2026-04-15) reports **325 new shows in a single day** (almost 1 in 5 new shows) and **20 wellness shows in under 75 minutes**. In one 24-hour window, Podcast Index flagged 45.7% of new feeds as possibly AI and judged 44.6% likely legitimate — [Podnews](https://podnews.net/update/ai-slop-overtakes-humans)
  - Gizmodo (2026-05-03): 35.4% of new feeds in the past day, 485 AI feeds that day, and Inception Point alone accounting for **23.6% of all new podcast output** — [Gizmodo](https://gizmodo.com/more-than-a-third-of-all-new-podcasts-are-ai-generated-2000753786). Bloomberg reported 4,243 of 10,871 new feeds (39%) over 9 days — [Bloomberg Soundbite](https://bloomberg.com/news/newsletters/2026-04-30/-podslop-proliferation-is-challenging-the-audio-industry). The classifier is itself AI and has no published accuracy.
- **KDP.**
  - Amazon caps uploads at 3 titles per day (Sept 2023) and requires AI disclosure, which is not public — [The Register](https://www.theregister.com/2023/09/22/amazon_ai_book_publishing_limit/); confirmed still in place by [Fortune, 2026-09-14](https://fortune.com/2026/09/14/ai-slop-books-amazon-marketplace-publishing-human-authors/)
  - Originality.ai [VENDOR]: 773 authors wrote the 844 books. The **29 repeat authors (under 4%) wrote 101 books (12%)**, and "all of these repeat authors likely used AI". One pen-name author released 5 books from 29 Sep to 1 Oct 2025 and 74 books from May to Oct 2025. A real, named author had 14 books in the window and 397 in total — [Originality.ai](https://originality.ai/blog/likely-ai-success-self-help-book-study)
  - Dhillon (Michigan) and Chakrabarty (Stony Brook), not peer-reviewed, using Pangram: of **14,419 self-published genre-fiction books (2023-2026), 2,880 (about 20%) were more than 25% AI**, 2,168 more than 50%, and about 1,000 more than 90%. Books with sales per quarter grew 19.2× while revenue grew 8.9×. Fortune gives no author-level velocity analysis — [Fortune](https://fortune.com/2026/09/14/ai-slop-books-amazon-marketplace-publishing-human-authors/)
- **News sites:** "Some publish hundreds of articles a day" — [NewsGuard 2023](https://www.newsguardtech.com/special-reports/newsbots-ai-generated-news-websites-proliferating/)
- **Academia (pre-LLM velocity baseline).** Ioannidis, Klavans and Boyack (Nature 2018) found **more than 9,000 authors averaging at least one paper every five days**, 265 after exclusions. Of 27 who responded, 70% admitted failing at least one authorship criterion more than 25% of the time. The authors stress there is "no evidence" of wrongdoing — [Retraction Watch](https://retractionwatch.com/2018/09/12/when-it-comes-to-authorship-how-prolific-is-too-prolific/?nb=1); [The Publication Plan](https://thepublicationplan.com/2018/11/19/the-prolific-authors-publishing-an-equivalent-of-one-paper-every-five-days/). Liang et al. (arXiv 2404.01268, Apr 2024) studied 950,965 papers from Jan 2020 to Feb 2024. LLM modification reached 17.5% in CS and 6.3% in math and Nature journals, and was **higher for first authors who post preprints more often**, for crowded fields and for shorter papers — [arXiv 2404.01268](https://arxiv.org/abs/2404.01268)
- **Tortured phrases (pre-LLM producer fingerprint).** Cabanac, Labbé and Magazinov (arXiv 2107.06751, 12 Jul 2021) documented phrases such as "counterfeit consciousness" for "artificial intelligence". They found them concentrated in one reputable journal, with more abstracts flagged as synthetic there and abrupt shifts in editorial timelines. The abstract gives no precision figure — [arXiv 2107.06751](https://arxiv.org/abs/2107.06751)

#### F. Domain age, zombie domains, parasite SEO (Google policy definitions)
- Google spam policies:
  - **Scaled content abuse**: "many pages are generated for the primary purpose of manipulating search rankings", e.g., "using generative AI tools … to generate many pages without adding value".
  - **Expired domain abuse**: "an expired domain name is purchased and repurposed primarily to manipulate search rankings".
  - **Site reputation abuse**: "third-party content is published on a host site mainly because of that host's already-established ranking signals".
  — [Google Search Central](https://developers.google.com/search/docs/essentials/spam-policies)
- Site reputation abuse was announced 5 Mar 2024 and enforced from 5 May 2024. In Nov 2024 Google ruled that "no amount of first-party involvement" exempts such content. Enforcement is by **manual action only** — [Search Engine Land](https://searchengineland.com/google-site-reputation-abuse-policy-now-includes-first-party-involvement-or-oversight-of-content-448432). Sistrix reported Forbes Advisor's removal from the index under this policy [SNIPPET] — [Sistrix](https://www.sistrix.com/?p=169359)
- **Zombie cases.**
  - The Hairpin's domain lapsed and was bought by Nebojša Vujinović Vujo, who filled it with AI articles (Wired, Jan 2024). He claims more than 2,000 sites, and NewsGuard documented more than 700 in his network [SELF-REPORTED / SNIPPET] — [Futurism](https://futurism.com/the-byte/hairpin-domain-ai-content)
  - The same network includes the Southwest Journal (Minneapolis) — [Racket](https://racketmn.com/southwest-journal-minneapolis-mn-vujo-ai) — and Hong Kong's Apple Daily domain — [VOA](https://www.voanews.com/a/domain-takeover-ends-apple-daily-tenure-as-pro-democracy-news-site/7513132.html)
- **Pre-LLM baseline for residual-trust abuse.** Lever et al., "Domain-Z" (IEEE S&P 2016), studied about 179M expired domains (Nov 2008 to Jul 2015). They found **at least 27,758 domains abusing residual trust** and 238,279 re-registered domains that malware later contacted — [PDF](https://patrickmcdaniel.org/pubs/ieeesp16b.pdf). So et al., "Domains Do Change Their Spots" (IEEE S&P 2022), extends this — [NSF PAR](https://par.nsf.gov/servlets/purl/10338034)

#### G. Network structure
- Bellingcat (2017) linked fake-news sites through shared Google Analytics IDs plus WHOIS — [Bellingcat](https://www.bellingcat.com/news/africa/2017/08/04/guptaleaks-google-analytics/). Papadogiannakis et al. (WWW 2022) built bipartite graphs and a metagraph from publisher-specific ad IDs to detect co-ownership [SNIPPET] — [review summary](https://liner.com/review/leveraging-googles-publisherspecific-ids-to-detect-website-administration)
- One caveat: **more than 5,700 websites share GA ID UA-33523145-1**, the US federal analytics program, so a single shared ID is not proof of common ownership — [Adalytics](https://adalytics.io/blog/network-graph-analysis-to-identify-related-websites)

#### H. Population-level priors by producer type (distributional estimates, not per-document)
- Liang et al., *Patterns* 2025 (arXiv 2502.09747v2, 17 Feb 2025), word-frequency mixture estimates:
  - **Corporate press releases:** Newswire peaked at **24.3%** in Dec 2023; PRNewswire about 16.4%.
  - **UN country-team releases:** 3.1% (Q1 2023) rising to 13.7% (Q3 2024).
  - **CFPB complaints:** 17.7% by Aug 2024.
  - **Small-firm LinkedIn job posts by founding year:** post-2015 firms 14.1%, 2000/2010-2015 firms 10.2%, 1980-2000 firms 7.2%, pre-1980 firms 4.0%. Firms with ≤10 employees 11.1% vs 6.2%.
  - **Pre-ChatGPT false-positive baselines:** 2-3% for press releases, 1.5% for CFPB.
  - **Adoption lag:** about 3-5 months after ChatGPT.
  — [arXiv 2502.09747v2](https://arxiv.org/html/2502.09747v2)
- **Platform base rates** [VENDOR]:
  - **Medium:** Pangram estimated **more than 47% of 274,466 posts** over 6 weeks (Wired, Oct 2024). The same report puts news sites at 7% in a one-day sample. Originality found just over 40% of 473 Medium articles from 2024, vs 3.4% in 2018 — [Wired via mirror](https://pipedot.org/6RV0W); original at [wired.com](https://www.wired.com/story/ai-generated-medium-posts-content-moderation/), which blocked my fetch.
  - **LinkedIn long posts:** Originality found 54% of posts from Oct 2024 likely AI (8,795 posts of 100+ words, 2018-2024) — [The Register, 2024-11-28](https://www.theregister.com/2024/11/28/linkedin_ai_posts). Pangram reports 41% fully AI [SNIPPET] — [PPC Land](https://ppc.land/over-half-of-linkedin-posts-are-now-likely-ai-but-authenticity-still-wins/)
- **Whole web** [VENDOR]. Graphite's first study (65,000 Common Crawl pages, Jan 2020 to May 2025, Surfer detector) put the crossover to majority-AI around Nov 2024. Its newer study (55,400 articles to Mar 2026, averaging Pangram, Copyleaks and GPTZero) found **about 49.9% "mostly AI" in Q1 2026**, with growth slowing — [Graphite](https://graphite.io/five-percent/more-articles-are-now-created-by-ai-than-humans)

#### I. Measured examples run on 2026-11-07 [MEASURED-HERE]
Domain-age, CT and Wayback profile of producers named in 2023-24 reports, from `domain_age.py`: RDAP via rdap.org, crt.sh JSON, and the Wayback CDX API (status-200 captures collapsed by month). Output is in `data/domain_age.jsonl`.

| Domain (named by) | RDAP registration today | Wayback first capture; largest gap | crt.sh first cert (n certs) | Reading |
|---|---|---|---|---|
| bestbudgetusa.com (NewsGuard 2023: "anonymously registered May 2022") | **404, no longer registered** | 2009-10; **136-month gap 2011-02 → 2022-06** | 2009-04-21 (197) | Old domain revived in 2022, now dropped |
| tnewsnetwork.com (NewsGuard: reg. Feb 2023) | **2026-07-13** (re-registered) | 2014-12; 28-month gap 2019-07 → 2021-11 | 2018-07-17 (109) | Churned twice |
| harmonyhustle.com (NewsGuard: reg. Apr 2023) | 2023-04-01 | 2021-12; 16-month gap to 2023-04 | **2023-04-02** (34) | First cert 1 day after registration |
| wavefunction.info (NewsGuard: reg. Mar 2023) | **2025-02-22** (re-registered) | 2013-04; **120-month gap 2013-04 → 2023-04** | 2025-02-22 (72) | Zombie, then churned |
| historyfact.in (NewsGuard) | **404** | only 2023-03 → 2023-05 | 2022-08-13 (16) | Short-lived |
| fox8.news (Yang & Menczer) | **404** | 2023-03 → 2025-02 | 2021-02-15 (280) | Dropped |
| cryptnomics.org (Yang & Menczer) | **404** | 2023-03 → 2025-09 | none (0) | Dropped |
| globaleconomics.news (Yang & Menczer) | **404** | 2023-03 → 2023-12 | 2023-02-08 (8) | Dropped |
| thehairpin.com (Wired, Jan 2024) | **2023-12-29** | **2010-10**; 165 capture-months | 2016-06-03 (265) | **Zombie signature: registration date 13 years after first capture** |
| southwestjournal.com (Racket: Vujo network) | 1997-12-22 (never dropped) | 1998-12; 186 capture-months | 2019-06-07 (254) | Aftermarket transfer, so registration age misses it |
| theatlantic.com (control) | 1995-08-15 | 1996-11; 324 capture-months | 2008-09-03 (3,106) | Stable human publisher |

- What the table shows:
  - **5 of the 8 farm and botnet domains named in 2023 are no longer registered.**
  - 2 more were re-registered with new creation dates (2025, 2026).
  - Only harmonyhustle.com keeps its 2023 date.
  - The Hairpin's RDAP date (2023-12-29), set against Wayback captures back to 2010, is the clean zombie signature.
  - Southwest Journal shows that aftermarket purchases keep the old registration date, so RDAP alone misses them.
- **Sitemap velocity and breadth, southwestjournal.com** (`sitemap_velocity.py`, then a section count). It has 6 child sitemaps. The 3 post sitemaps hold **2,023 URLs, every lastmod in 2023-2026** (2023: 269; 2024: 1,202; 2025: 377; 2026: 175), with none earlier, although Wayback captures go back to 1998. **745 URLs share one lastmod day (2024-01-27).** Top sections: us 429, news 193, cars 188, other 185, sport 125, world 116, celebrities 92, gambling 75, animals 74, finance 56, canada 54, net-worth 45, education 39. Subsections include us/florida 60, us/california 39 and sport/nba 36. Recent slugs: "health-insurance-cover-medical-treatment-but-exclude-dental-care", "am-i-registered-to-vote", "nfl-thanksgiving-2026-games". These are generic national SEO topics on a former Minneapolis neighborhood-paper domain. Caveat: lastmod records modification, not first publication.
- **Access failures** (useful operational finding): the WordPress REST `/wp-json/wp/v2/posts` endpoint returned 404 for thehairpin.com and 403 for marginalrevolution.com and tnewsnetwork.com, and timed out for harmonyhustle.com. Sitemaps returned 404 or 403 for thehairpin.com, tnewsnetwork.com and marginalrevolution.com. Live velocity endpoints are often blocked, so **Wayback and Common Crawl captures are the dependable velocity source**.
- **Podcast Index API check.** Podnews says Podcast Index added a `/recent/problematic` endpoint (spam, phishing, "low-effort AI"). No such path exists in the public spec repo `Podcastindex-org/docs-api` (`api_src/paths/recent/` has data, episodes, feeds, newfeeds, newvaluefeeds and soundbites; last commit 2026-07-08) — [docs-api](https://github.com/Podcastindex-org/docs-api) [MEASURED-HERE via GitHub API]. Status: reported but undocumented.

### Inferences
- The best way to harvest negatives is **seed, expand, then confirm by aggregation**:
  1. Seed producers from high-precision artifacts: NewsGuard-style error leaks on byline-less sites, prompt leaks, fake headshots, Podcast Index or Inception Point feeds, and Hanley's domain lists.
  2. Expand through network edges (shared ad/analytics IDs, link targets, co-ownership) and metadata priors (first seen after Nov 2022, zombie signature, bursty velocity, broad topics).
  3. Confirm each candidate producer with a He et al.-style aggregate over 15-20 pages.

  Under this scheme the metadata priors decide **where to look**. The aggregate detector decides **the label**.
- A rough lift from domain age: P(LLM-dominant) is 10.08% for sites first crawled 2024-25, against a 4.30% Common Crawl base. That makes "new domain" about a **2.3× likelihood-ratio prior** (my calculation from He et al.). It is useful for ranking candidates but far from a label.
- A social-platform leak is only a **seed for manual or coordination review** (24% bot precision). A leak on a byline-less website, followed by aggregate confirmation, can label the whole domain. A leak on a site with real, verifiable human bylines (newsrooms, Medium writers) should label **only that document**.
- Domain churn is severe: 5 of 8 named domains were gone within about 3 years. Harvesting from published lists therefore depends on Wayback or Common Crawl snapshots from the producer's active window, not on live crawling.
- Zombie detection is best done as the conjunction: (Wayback gap ≥12 months) AND (post-gap content has no URLs from before the gap, or registration date > first capture) AND (broad generic topics). RDAP registration age alone fails for aftermarket transfers such as southwestjournal.com.
- Velocity thresholds should be set per platform. On KDP, more than 3 titles in a week from one pen name is already unusual given the 3-per-day cap and the Originality data. For podcasts, dozens of new shows per day from one publisher is decisive. For news sites, "hundreds per day" from a site with no wire subscription is strong evidence.

### Gaps
- No published study measures **P(rest of producer's output is AI | one leak)** for websites, KDP authors, or Amazon sellers. fox8 is the only measured precision, and it covers social accounts. This can be measured by running He et al.'s pipeline over leak-seeded domains.
- No measured precision exists for velocity, topical-breadth, or bio-templating signals in isolation. All evidence is case-based or vendor-based.
- I did not find a study that counts chatbot-leak phrases across Common Crawl. The Common Crawl index has no full-text search, so it would need a WARC/WET scan, which I did not run.
- NewsGuard's discovery method beyond 2023 and its per-site evidence are not public. The list is available only on request.
- Shoaib et al. and Stanford Internet Observatory / DFRLab work on AI content-farm networks: I did not locate specific papers with measured network-detection precision in this session.
- I could not fetch the primary Recorded Future CopyCop report, the primary Wired Medium article, or Futurism's original SI article (paywalled or blocked). Their figures here come from secondary coverage.
- The date of Pangram's Amazon-review study conflicts: a search summary said mid-2025, but the fetched page is dated 2026-05-04.

---

## Q2. Which signals unlock large, retrievable, informational corpora (how-to, explainers, news rewrites, product copy, reviews, comments)?

### Takeaway
The best fit for quill's informational-nonfiction negatives is **how-to and explainer websites**. He et al. found that 9.96% of Bing top-20 sites for WikiHow queries are LLM-dominant, so replicating their query, crawl and aggregate pipeline yields thousands of labeled how-to sites. Next come **AI content-farm news and explainer domains**, seeded from NewsGuard-style leaks, Hanley's domain lists and zombie domains, and retrieved from Wayback or Common Crawl. Then **KDP nonfiction metadata** (descriptions 79% likely AI in the self-help sample), **Medium** posts and **podcast feeds** from known AI publishers. Reviews (Amazon Reviews'23) and civic comments (Mirrulations) are large and retrievable, but either the AI rate is low (about 3% of front-page Amazon reviews) or the prevalence is unmeasured (regulations.gov).

### Cited Findings
- **How-to sites (best genre match).**
  - He et al. built the set by querying Bing for 2,000 WikiHow titles: 17,036 sites, of which 10,232 had at least 15 prose pages, 264,918 pages in total. **1,019 sites (9.96%) were LLM-dominant**, described as "generic blogs with many ads, written by made-up authors" — [arXiv 2507.13933v2](https://arxiv.org/abs/2507.13933v2)
  - Search results surface more LLM sites than random sampling does (9.84% vs 4.30%) — [arXiv 2507.13933v2](https://arxiv.org/abs/2507.13933v2). The paper gives 9.84% in the Common Crawl paragraph and 9.96% (1,019/10,232) in the search-results paragraph, an internal inconsistency.
- **Common Crawl new domains.** Of 764 sites first crawled in 2024-25, 10.08% were LLM-dominant — [arXiv 2507.13933v2](https://arxiv.org/abs/2507.13933v2). Common Crawl's terms (last updated 2024-03-07) require users to "respect the copyrights and other applicable rights of third parties" — [Common Crawl ToU](https://commoncrawl.org/terms-of-use) [MEASURED-HERE, page text]
- **News rewrites and content farms.**
  - NewsGuard: 3,749 domains in 16 languages as of 2026-06-23, list available on request — [NewsGuard](https://www.newsguardtech.com/special-reports/ai-tracking-center/)
  - Hanley and Durumeric's repo ships the reliable and unreliable domain lists (Apache-2.0) and classifier code — [GitHub](https://github.com/hanshanley/machine-made-media)
  - CopyCop: more than 19,000 articles on 11 sites by Mar 2024 [SNIPPET] — [bestofai](https://bestofai.com/article/a-russia-linked-network-uses-ai-to-rewrite-real-news-stories)
  - AdVon: more than 90,000 articles for hundreds of publications, including product reviews and roundups on Reviewed, the LA Times and McClatchy sites — [Futurism](https://futurism.com/advon-ai-content)
  - Vujo network: more than 2,000 sites claimed, more than 700 documented by NewsGuard — [Futurism](https://futurism.com/the-byte/hairpin-domain-ai-content)
  - In my measurement, southwestjournal.com alone exposes 2,023 post URLs of generic explainers (health insurance, voter registration, net worth, cars) through a public sitemap [MEASURED-HERE].
- **KDP nonfiction (self-help, herbal remedies)** [VENDOR]. "Success" self-help: 77% of 844 books likely AI, descriptions 79%, bios 29% — [Originality.ai](https://originality.ai/blog/likely-ai-success-self-help-book-study). Herbal remedies: 82% at least partly AI (Jan-Sep 2025) [SNIPPET] — [The Week](https://www.theweek.in/news/health/2025/10/28/beware-that-herbal-remedy-book-in-amazon-wishlist-is-likely-written-by-ai.html). Genre fiction: about 20% substantially AI (Dhillon and Chakrabarty) — [Fortune](https://fortune.com/2026/09/14/ai-slop-books-amazon-marketplace-publishing-human-authors/)
- **Medium:** more than 47% of 274,466 posts likely AI [VENDOR] — [Wired via mirror](https://pipedot.org/6RV0W)
- **LinkedIn long posts:** 41-54% likely AI [VENDOR] — [The Register](https://www.theregister.com/2024/11/28/linkedin_ai_posts). There is no public API; see social_platforms.md.
- **Podcasts (informational audio: biographies, wellness, weather/pollen-type shows).** Inception Point accounts for 23.6% of new podcast output, with more than 5,000 shows — [Gizmodo](https://gizmodo.com/more-than-a-third-of-all-new-podcasts-are-ai-generated-2000753786); [THR](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/). Podnews counted more than 8,000 Inception Point shows still in the index, with 20 wellness shows (codependency, mental health, vaccinations) released in 75 minutes — [Podnews](https://podnews.net/update/ai-slop-overtakes-humans)
- **YouTube (narration scripts, mostly visual).** Kapwing (Nov 2025) found 278 channels that are entirely AI slop among about 15,000 top-trending channels, with more than 63B views and 221M subscribers. 104 of a fresh account's first 500 Shorts recommendations (21%) were AI slop [SNIPPET] — [Newsbytes](https://www.newsbytesapp.com/news/science/20-of-youtube-recommendations-for-new-users-are-low-quality-ai-videos/story); [RTTNews](https://www.rttnews.com/amp/3606751/study-finds-over-20-of-videos-shown-to-new-youtube-users-are-low-quality-ai-content.aspx)
- **Reviews.**
  - Pangram [VENDOR]: 3% of 30,000 front-page reviews on 500 bestsellers were AI. **93% of AI reviews carried Verified Purchase**, so the badge does not separate them. AI reviews were 74% five-star vs 59% for human reviews, and 10% one-star vs 22%. No reviewer-level analysis — [Pangram](https://www.pangram.com/blog/ai-amazon-reviews)
  - Originality [VENDOR]: about a 400% rise after ChatGPT, and extreme ratings 1.3× more likely to be AI [SNIPPET] — [Originality](https://originality.ai/pt/blog/amazon-ai-generated-reviews)
  - The Transparency Company (Dec 2024) analyzed 73M reviews in home, legal and medical services: about 14% likely fake and **2.3M partly or entirely AI**, with large volumes from mid-2023. The FTC sued Rytr (Sept 2024) because some subscribers generated "hundreds and perhaps thousands" of reviews. The FTC fake-review rule took effect Oct 2024 — [AP via KSL, 2024-12-26](https://www.ksl.com/article/51216679/the-internet-is-rife-with-fake-reviews-will-ai-make-it-worse)
  - **Amazon Reviews'23 (McAuley Lab):** 571.54M reviews, 54.51M users, 48.19M items, May 1996 to Sep 2023. Fields include `user_id`, `timestamp` (ms), `helpful_vote` and `verified_purchase`, so reviewer velocity is computable — [HF README](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) [MEASURED-HERE: README fetched; it has no license field]
- **Civic comments.**
  - Mirrulations has 22M public comments (Oct 2024; later "nearly 30 million" files) in the AWS Open Data bucket `s3://mirrulations`, readable with `--no-sign-request`, with text extracted from PDFs. A full download is estimated at about 3 years — [Moravian](https://news.moravian.edu/2024/10/22/moravian-universitys-mirrulations-dataset-now-openly-accessible-on-the-amazon-web-services-cloud/); [AWS registry](https://registry.opendata.aws/mirrulations/)
  - **I found no measured prevalence of LLM-written comments on regulations.gov.** Commentary says reCAPTCHA and API limits curb automated floods — [GWU Regulatory Studies](https://regulatorystudies.columbian.gwu.edu/node/4321). DOJ's Docketscope detects "duplicate and computer-generated submissions" — [arXiv 2604.17247](https://arxiv.org/html/2604.17247)
  - **Pre-LLM templated baseline (FCC 2017):** about 18M of more than 22M comments were fake. Broadband for America spent $4.2M on more than 8.5M fake comments plus about 0.5M fake letters to Congress. One 19-year-old generated more than 7.7M comments with automated software — [Law Street Media](https://lawstreetmedia.com/news/tech/new-york-ag-investigation-report-finding-18-million-fake-comments-on-fcc-net-neutrality-rulemaking/); [Inquirer, 2021-05-07](https://www.inquirer.com/business/fcc-comments-net-neutrality-comcast-attorney-general-ny-20210507.html)
- **Reddit:** machine-generated text is concentrated in a small fraction of users, and most common in technical-knowledge subreddits — [arXiv 2510.07226](https://arxiv.org/abs/2510.07226v1). The 2025 University of Zurich r/changemyview experiment used LLM personas, and Reddit banned the accounts — [Engadget](https://engadget.com/ai/researchers-secretly-experimented-on-reddit-users-with-ai-generated-comments-194328026.html)

### Inferences
- Ranked by fit to quill (informational nonfiction):
  1. how-to and explainer blogs (He et al. replication)
  2. content-farm explainers and news rewrites (NewsGuard, Hanley lists, zombie domains, Vujo-style networks)
  3. KDP nonfiction descriptions and "Look Inside" samples, though samples are hard to retrieve
  4. Medium technical and self-help posts
  5. podcast transcripts from AI publishers, if transcripts exist in feeds
  6. product copy and roundups (AdVon-style)
  7. reviews
  8. civic comments
- A cheap, high-yield recipe for how-to negatives:
  1. Take queries from WikiHow titles or quill's own topic list.
  2. Pull the top 20 results.
  3. Crawl 15-20 pages per domain from Common Crawl.
  4. Score locally with Binoculars and aggregate by domain.
  5. Keep domains above a strict site-level threshold.

  Using those domains' pre-2023 human controls (or the bottom-scoring sites) gives matched human positives on the same topics.
- Amazon Reviews'23 ends Sep 2023, before most AI-review growth, so it is weak for AI negatives. It is useful as a pre-LLM human baseline and for learning reviewer-velocity distributions.
- Civic comments suit learning mass-template patterns (FCC 2017), not LLM style. Without a prevalence study, treat regulations.gov as unlabeled.

### Gaps
- No public, downloadable label list exists for NewsGuard, Podcast Index flags (the endpoint is undocumented), or Pangram's site datastream.
- He et al. did not release their site lists or labels in the 2-page poster (not stated). Contacting the authors may be required.
- Whether Inception Point feeds carry `podcast:transcript` tags was not checked.
- KDP "Look Inside" text is not bulk-retrievable. Only descriptions and bios are on product pages.

---

## Q3. What are the false-positive modes (prolific human writers, newsrooms with wire copy, templated but human SEO shops pre-2023, non-native writers)?

### Takeaway
Every producer signal has a human look-alike:
- **Velocity:** hyperprolific scientists, real authors who use AI only partly, newsrooms running wire copy.
- **Leak phrases:** humans quoting ChatGPT (76% of X phrase-posters).
- **Domain age:** every legitimate new site launched after 2022.
- **Shared IDs:** agency or government analytics.
- **Templating:** pre-LLM mail-merge and SEO shops.
- **Detectors:** non-native writers (61% FPR on TOEFL essays; see social_platforms.md).

Measured pre-ChatGPT false-positive floors are roughly 1.2% for site-level aggregation, 1.5-3% for distributional estimates and 3.4% for Originality on Medium in 2018. Many producers are also **hybrids** (AI plus human editors), so a producer-level label should be "AI-dominant", not "all AI".

### Cited Findings
- **Quoting humans.** In a 100-account sample, 76% of accounts posting "as an AI language model" were humans posting or retweeting ChatGPT output — [Yang & Menczer](https://arxiv.org/html/2307.16336v1)
- **Detector over-flagging at account level.** 41% of random accounts crossed the OpenAI-classifier threshold tuned for fox8 — [Yang & Menczer](https://arxiv.org/html/2307.16336v1)
- **Site-level FPR floor.** 16 of 1,315 sites crawled entirely before ChatGPT (1.22%) were misclassified as LLM, mostly because pages evaded the filters — [He et al.](https://arxiv.org/abs/2507.13933v2)
- **Distributional baselines** before ChatGPT: about 2-3% for press releases, 1.5% for CFPB complaints — [Liang et al. 2025](https://arxiv.org/html/2502.09747v2). Originality flagged 3.4% of Medium posts from 2018 — [Wired via mirror](https://pipedot.org/6RV0W)
- **Demographic confounds.** LLM use in CFPB complaints is higher in areas with lower bachelor's attainment (19.9% vs 17.4%) and in highly urbanized areas (18.2% vs 10.9%). By state it ranges from 2.6% (WV) to 29.2% (AR) — [Liang et al. 2025](https://arxiv.org/html/2502.09747v2). Detectors flag non-native writing: an average 61.22% FPR on TOEFL essays (Liang et al. 2023), covered in `AI slop negative signal/social_platforms.md` — [arXiv 2304.02819](https://arxiv.org/pdf/2304.02819)
- **Prolific humans.**
  - More than 9,000 authors averaged at least one paper every five days before LLMs — [Retraction Watch](https://retractionwatch.com/2018/09/12/when-it-comes-to-authorship-how-prolific-is-too-prolific/?nb=1)
  - A 2024 Scientometrics paper (160,108 computer scientists) argues that "hyperprolific" should be judged on citations as well as counts [SNIPPET] — [THE](https://www.timeshighereducation.com/node/742062)
  - The KDP author with 397 books "appears to be a real person" using his real name and face [VENDOR] — [Originality.ai](https://originality.ai/blog/likely-ai-success-self-help-book-study)
- **Hybrid producers.**
  - AdVon writers polished MEL drafts, and AdVon claims AI is used alongside humans — [Futurism](https://futurism.com/advon-ai-content)
  - Vujo describes a mix of AI and human writers using Copymatic, Jasper and ChatGPT [SELF-REPORTED] — [Futurism](https://futurism.com/the-byte/hairpin-domain-ai-content)
  - Inception Point's CEO says wellness content gets human review [SELF-REPORTED] — [Podnews](https://podnews.net/update/ai-slop-overtakes-humans)
  - Medium's CEO argues detectors cannot separate fully AI posts from lightly assisted ones — [Wired via mirror](https://pipedot.org/6RV0W)
  - LinkedIn says flagged posts were "AI-assisted" — [The Register](https://www.theregister.com/2024/11/28/linkedin_ai_posts)
  - He et al. report "many in-between sites" — [He et al.](https://arxiv.org/abs/2507.13933v2)
- **Shared infrastructure.** More than 5,700 sites share the US government's GA ID — [Adalytics](https://adalytics.io/blog/network-graph-analysis-to-identify-related-websites). Shared IDs need corroboration ("multiple corroborating signals") — [same](https://adalytics.io/blog/network-graph-analysis-to-identify-related-websites)
- **Pre-LLM templating (human or rule-based).**
  - FCC 2017: millions of templated or fabricated comments came from lead generators and automated software, not LLMs — [Law Street Media](https://lawstreetmedia.com/news/tech/new-york-ag-investigation-report-finding-18-million-fake-comments-on-fcc-net-neutrality-rulemaking/)
  - Tortured phrases came from paraphrasing tools before ChatGPT — [arXiv 2107.06751](https://arxiv.org/abs/2107.06751)
  - Expired-domain abuse predates LLMs: at least 27,758 residual-trust abuses by 2015 — [Domain-Z](https://patrickmcdaniel.org/pubs/ieeesp16b.pdf)
- **Domain-age pitfalls** [MEASURED-HERE]:
  - RDAP returns the **latest** registration (tnewsnetwork.com shows 2026, though NewsGuard said Feb 2023).
  - Aftermarket transfers keep the original date (southwestjournal.com, 1997).
  - CT logs only show TLS issuance. cryptnomics.org had no crt.sh certificates at all.
- **Ranking and quality are not proxies.** LLM sites did not rank lower on Bing — [He et al.](https://arxiv.org/abs/2507.13933v2). Some flagged Medium posts drew hundreds of claps — [Wired via mirror](https://pipedot.org/6RV0W). Human pages still make up about 86% of Google top results [VENDOR] — [Graphite](https://graphite.io/five-percent/more-articles-are-now-created-by-ai-than-humans)

### Inferences
- Mitigations, in priority order:
  1. Require **two independent signals**, e.g., (leak OR fake identity OR zombie OR publisher flag) AND (aggregate detector over 15 or more pages), before labeling a producer.
  2. **Restrict content to after Nov 2022** for the negatives, and use the same producer's pre-2023 content (when it exists and differs, as with zombie domains) as a check, not as a human positive.
  3. Exclude wire-syndicated text by near-duplicate matching against AP or Reuters before labeling a newsroom.
  4. Exclude producers whose text is mainly non-native English unless a strong artifact exists. Otherwise quill learns to avoid plain non-native phrasing, not slop.
  5. Treat hybrids as "AI-dominant producer", and label at the document level within them where the detector is confident.
- For quill specifically, a false positive (a human-written page labeled AI) matters less if the negatives feed feature mining (slop n-grams, structure), as recommended in `training_methods.md`, rather than a sequence-level rejected-text loss. Hybrid pages are still "slop-styled" text.

### Gaps
- No measured false-positive rate exists for velocity or topical-breadth heuristics on prolific human bloggers or newsrooms.
- Wire copy: I found no study measuring how syndicated AP/Reuters text and pre-LLM automated journalism (e.g., template-generated earnings stories) score under site-level aggregation. It is plausible this text inflates newsroom scores, but that is unverified.
- No study measures how much aggregation reduces the non-native false-positive rate (per-producer averaging may compound it, not cancel it).

---

## Q4. What's legally and ToS-feasible for private, local use?

### Takeaway
The producer-metadata queries are all public, read-only and low-risk at a polite rate: RDAP, crt.sh, the Wayback CDX API, Common Crawl indexes and WARCs, sitemaps and RSS. Common Crawl's terms leave copyright compliance to the user. For a private, non-commercial local fine-tune, the copyright analysis in `Nonfiction author style corpora/legal_and_acquisition.md` applies (Bartz and Kadrey, June 2025). The real constraints are:
- **proprietary label lists:** NewsGuard is by request only; Podcast Index needs an API key and its flags are undocumented
- **platform terms that ban scraping:** X, LinkedIn and Amazon (see `social_platforms.md`)
- **personal data in reviews and comments:** keep it local and never publish producer "AI" labels about identifiable people

### Cited Findings
- Common Crawl ToU (last updated 2024-03-07): "BY USING THE CRAWLED CONTENT, YOU AGREE TO RESPECT THE COPYRIGHTS AND OTHER APPLICABLE RIGHTS OF THIRD PARTIES". Common Crawl disclaims responsibility for the content and recommends legal counsel before commercial use — [Common Crawl ToU](https://commoncrawl.org/terms-of-use) [MEASURED-HERE]
- NewsGuard's domain list is available to researchers, platforms and advertisers on request through a contact form. No public license — [NewsGuard](https://www.newsguardtech.com/special-reports/ai-tracking-center/)
- Hanley and Durumeric's domain lists and code are Apache-2.0 — [GitHub](https://github.com/hanshanley/machine-made-media) [MEASURED-HERE]
- The Amazon Reviews'23 HF README declares no license (it gives a citation and a research-contact email) — [HF README](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) [MEASURED-HERE]
- Mirrulations is in the AWS Open Data Sponsorship Program, with anonymous S3 access. Comments are public records submitted to agencies. I found no license statement — [AWS registry](https://registry.opendata.aws/mirrulations/)
- The FTC's fake-review rule (effective Oct 2024) targets businesses and individuals who create or buy fake reviews. Platforms are shielded — [AP via KSL](https://www.ksl.com/article/51216679/the-internet-is-rife-with-fake-reviews-will-ai-make-it-worse)
- Fair use for training (Bartz v. Anthropic, 23 Jun 2025; Kadrey v. Meta, 25 Jun 2025) and how copies were acquired: see `Nonfiction author style corpora/legal_and_acquisition.md`. Platform terms (hiQ v. LinkedIn contract claim; X terms) are in `AI slop negative signal/social_platforms.md`.

### Inferences
- **Feasible now, low risk:**
  - RDAP, crt.sh and Wayback CDX metadata at about 1 request per 1.5-2 seconds (as I ran them)
  - Common Crawl CDX lookups and WARC range reads for candidate domains
  - public sitemaps and RSS
  - the Hanley lists
  - Amazon Reviews'23 and Mirrulations for local analysis
- **Feasible with permission or keys:** the NewsGuard list (request it), the Podcast Index API (free key; ask the maintainers about the "problematic" flags), and He et al.'s site lists (ask the authors).
- **Avoid:** live scraping of Amazon, LinkedIn or X; publishing producer-level "AI" labels (defamation risk, especially for real people like the 397-book author); and redistributing harvested text. Keep everything in a private, local negatives store with source URLs and capture dates for provenance.

### Gaps
- I did not verify Amazon's current Conditions of Use wording on robots and data mining in this session.
- No license is stated for Mirrulations or Amazon Reviews'23.
- Whether Wayback "Save Page Now" or CDX rate limits allow bulk WARC retrieval at the scale needed (thousands of domains × 20 pages) was not tested. Common Crawl WARC range requests are the safer path.
