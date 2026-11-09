# Moderated communities and institutions that label AI-generated / AI-sloppy text: a catalog of harvestable negative signal (as of 2026-11-07)

Scope note: this covers Wikipedia, Stack Exchange, academic publishing, news/content farms, publishing platforms, open-source and bug-bounty slop, and education. Live Wikipedia numbers come from read-only MediaWiki API queries I ran on 2026-11-07 (UTC). Claims marked "(snippet only)" come from search-result summaries and were not checked against a fetched primary page. Claims marked "(prior knowledge, not re-verified)" are from my background knowledge and are listed so the writer can decide whether to use them.

## Q1. Which sources give high-precision human labels on informational nonfiction, at 1k+ examples, retrievable as text?

### Takeaway
English Wikipedia is the only source that clears all three bars: human labels, more than 1k items, and full text you can retrieve under an open license. The {{AI-generated}} tag sits on 7,648 articles as of 2026-11-07, there are 950 user-level AI noticeboard cases, public abuse-filter logs store the added text, and full revision history is available. Every other high-precision labeler is either small (Retraction Watch 95 entries, curl 49, Academ-AI about 500) or keeps its text or list private (Stack Overflow deletions, NewsGuard's 3,749 domains, G15-deleted pages).

### Cited Findings

#### Wikipedia: tracking category and the {{AI-generated}} template (highest volume, human-applied)
- On 2026-11-07, 7,648 mainspace articles transclude {{AI-generated}}. — [MediaWiki API embeddedin, Template:AI-generated](https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=Template:AI-generated&einamespace=0&eilimit=500)
- The parent "Articles containing suspected AI-generated texts" category holds no pages directly. It has 18 dated monthly subcategories (May 2025 to Nov 2026) containing 7,764 pages in total. — [API categoryinfo](https://en.wikipedia.org/w/api.php?action=query&prop=categoryinfo&titles=Category:Articles_containing_suspected_AI-generated_texts); [Category page](https://en.wikipedia.org/wiki/Category:Articles_containing_suspected_AI-generated_texts)
- Pages still tagged, by month the tag was added: May 2025: 1, Jul 2025: 27, Aug 2025: 349, Sep 2025: 361, Oct 2025: 500, Nov 2025: 534, Dec 2025: 565, Jan 2026: 380, Feb 2026: 462, Mar 2026: 361, Apr 2026: 331, May 2026: 217, Jun 2026: 569, Jul 2026: 841, Aug 2026: 437, Sep 2026: 736, Oct 2026: 847, Nov 1–7 2026: 246. These count only tags that remain; older months shrink as articles are cleaned. — [API categoryinfo over monthly subcats](https://en.wikipedia.org/wiki/Category:Articles_containing_suspected_AI-generated_texts)
- Template:AI-generated was created 2023-01-27 by Barkeep49. It renders: "This article {appears to incorporate | incorporates} text from a large language model, which is prohibited in Wikipedia articles." Its parameters are `partial`, `section`, `certain=yes/no` (which switches "appears to incorporate" to "incorporates"), `reason=` (free-text justification) and `date=`. — [Template:AI-generated source](https://en.wikipedia.org/wiki/Template:AI-generated)
- At least 21 redirects to the template exist, including {{LLM}}, {{ChatGPT}}, {{Slop}}, {{AI-cleanup}} and {{Completely AI-generated}}. — [API backlinks redirects](https://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle=Template:AI-generated&blfilterredir=redirects&blnamespace=10)

#### Wikipedia: policy context that sets the label's meaning
- WP:LLM, an information page, says "using LLMs to generate or rewrite article content is prohibited, except for translation and for basic copyediting of one's own work". It also says obviously generated talk-page comments may be hidden. — [Wikipedia:Large language models](https://en.wikipedia.org/wiki/Wikipedia:Large_language_models)
- WikiProject AI Cleanup: "Since March 2026, the Wikipedia guideline WP:LLM has prohibited the use of LLMs to generate or rewrite article content … However, a lot of LLM-generated text inserted from 2022 to 2026 remains on Wikipedia." — [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- The content guideline page "Wikipedia:Writing articles with large language models" was created 2025-10-24 by Cremastra as a proposal ("Large language models should not be used to generate Wikipedia articles"). — [API first revision](https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models)
- "In August 2025, English Wikipedia adopted a policy that allowed editors to nominate suspected LLM-generated articles for speedy deletion. This was followed by a March 2026 decision to prohibit the use of LLMs to generate or rewrite article content." — [Artificial intelligence in Wikimedia projects (article)](https://en.wikipedia.org/wiki/Artificial_intelligence_in_Wikimedia_projects); August 2025 date also given by [Ground News](https://ground.news/article/wikipedias-g15-policy-targets-low-quality-ai-content-for-speedy-deletion) and [WebProNews](https://www.webpronews.com/wikipedias-g15-policy-targets-low-quality-ai-content-for-speedy-deletion)
- WikiProject AI Cleanup's page was created 2023-12-04 (Chaotic Enby). "Signs of AI writing" was created the same day (Ca) and is now 180,925 bytes. — [API first revisions](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)

#### Wikipedia: G15 speedy deletion (highest precision; deleted text not public)
- The current heading is "G15. Unambiguously LLM-generated pages" (formerly "LLM-generated pages without human review"; updated by a 2026 RfC). It applies to pages that show any of three signs: (1) communication intended for the user ("Here is your Wikipedia article on…", knowledge-cutoff disclaimers, "as a large language model", unfilled placeholders like "[Birth Date]"); (2) non-existent or nonsensical references (dead-on-arrival links, invalid-checksum ISBNs, unrelated DOIs, citations dated before the event); (3) technical indicators (`oaicite`, `attributionIndex` JSON, `turn0search0`, ```` ```wikitext ```` code fences). Other stylistic signs, and even an author admitting LLM use, "are not sufficient". — [WP:Speedy deletion §G15](https://en.wikipedia.org/wiki/Wikipedia:Criteria_for_speedy_deletion#G15)
- Signs of AI writing: a high detector score (GPTZero, Pangram) "is not a valid criterion for speedy deletion under G15". — [Signs of AI writing §AI detection tools](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Volume sample: 3,000 deletions in the log between 2026-11-07T11:26Z and 2026-11-08T00:05Z (about 12.6 h) included 6 citing G15 (2 articles, 1 draft, 3 user pages), often combined with G11 (promotion). One summary read "G15: Unambiguously LLM-generated page (communication intended for the user and chatbot block (see filter logs…)". — [Deletion log via API](https://en.wikipedia.org/wiki/Special:Log/delete)
- An LLM-specific proposed-deletion process, "LLMPROD", also exists. Abuse filter 1408 "Removal of LLM PROD tags" has 1,440 hits. — [Special:AbuseFilter/1408](https://en.wikipedia.org/wiki/Special:AbuseFilter/1408); [WP:G15 text referencing WP:LLMPROD](https://en.wikipedia.org/wiki/Wikipedia:Criteria_for_speedy_deletion#G15)

#### Wikipedia: AI noticeboard and project subpages (user-level labels)
- "Wikipedia:AI noticeboard" has 950 case subpages as of 2026-11-07. They are named by date and user (e.g. "2025-09-16 Bookleo" … "2026-07-30 Bondwagon") and run from Sep 2025 onward. — [Special:PrefixIndex/Wikipedia:AI noticeboard/](https://en.wikipedia.org/wiki/Special:PrefixIndex/Wikipedia:AI_noticeboard/)
- The project says: "Content added by users who have been blocked for AI use, consented to cleanup of their edits, or had a consensus reached…" can be mass-cleaned. Its goals include "keep track of AI-using editors". — [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- "WikiProject AI Cleanup/AI diffs" calls itself a "data dump of diffs which have been confirmed beyond reasonable doubt to have been AI-written", but it holds only 5 diffs and is stale. — [AI diffs](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/AI_diffs)
- An "AI or not" quiz has 12 article-specific subpages (e.g. Prevagen, Walter Potter, Senchal Lake). These are curated human-vs-AI examples with answers, so precise but tiny. — [AI or not](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/AI_or_not)

#### Wikipedia: automated but human-authored detectors (public logs contain the text)
- Abuse filter 1325 "Possible AI-generated text": 13,890 hits, action = tag, last edited 2026-10-27. — [Special:AbuseFilter/1325](https://en.wikipedia.org/wiki/Special:AbuseFilter/1325)
- Abuse filter 1346 "Possible AI-sourced citations": 14,661 hits. The matching change tag "possible AI-generated citations" has 10,296 hits. — [Special:AbuseFilter/1346](https://en.wikipedia.org/wiki/Special:AbuseFilter/1346); [Special:Tags](https://en.wikipedia.org/wiki/Special:Tags)
- Filter 1407 "Removal of AI-generated tag": 4,063 hits. Filter 1418 "Possible self-disclosure of AI agent or AI use": 572. Filter 893 "AI-generated sources": 3. Filter 1387 "Disallow using Grokipedia on articles". — [Special:AbuseFilter](https://en.wikipedia.org/wiki/Special:AbuseFilter)
- VisualEditor EditCheck tags: "editcheck-llm-paste" ("content pasted from a source that looked AI-generated") has 2,277 hits, and "editcheck-llm-paste-shown" has 2,998. — [Special:Tags](https://en.wikipedia.org/wiki/Special:Tags)
- The abuse log is public through the API and includes `details.added_lines`. A 1325 hit from 2026-11-07 contains pasted chatbot/AI-search UI text such as "Would you like to know more about his career statistics…", "Ask anything" and "People also ask". — [API list=abuselog aflfilter=1325](https://en.wikipedia.org/w/api.php?action=query&list=abuselog&aflfilter=1325&aflprop=ids|user|title|timestamp|revid|details)

#### Stack Overflow / Stack Exchange (genre fits, data is not harvestable)
- "Policy: Generative AI (e.g., ChatGPT) is banned" was posted 2022-12-05 on Meta Stack Overflow (score 5,591; last edited 2026-10-25). It says: "All use of generative AI (e.g., ChatGPT and other LLMs) is banned when posting content on Stack Overflow. This includes 'asking' the question to an AI generator then copy-pasting its output as well as using an AI generator to 'reword' your answers." Rationale: "because the average rate of getting correct answers from ChatGPT … is too low." Discussion uses the [ai-generated-content] tag. — [Stack Exchange API, meta.SO q/421831](https://api.stackexchange.com/2.3/questions/421831?site=meta.stackoverflow&filter=withbody); [Meta post](https://meta.stackoverflow.com/questions/421831)
- In June 2023 moderators struck because a new policy barred them from removing AI answers "on the basis of being AI-generated, outside of exceedingly narrow circumstances". The company cited detector false positives. — [devclass, 2023-06-05](https://devclass.com/2023/06/05/stack-overflow-volunteer-moderators-down-tools-over-secret-new-policy-that-obstructs-removal-of-ai-generated-content/); [i-programmer](https://i-programmer.info/news/99-professional/16359-stack-overflow-moderators-take-strike-action.html)
- A Meta analysis found detectors falsely flagged about 1 in 5.5 posts at a 0.50 threshold (snippet only, from a Meta mirror). — [backiee mirror of meta.SE 389960](https://backiee.wasmer.app/https_meta_stackexchange_com/revisions/389960/3)
- I found no official count of deleted AI answers or AI-related suspensions. — [search result summary](https://devclass.com/2023/08/24/stack-overflow-how-much-is-traffic-dropping-and-how-the-moderator-strike-was-resolved/)

#### Academic publishing (very precise, small)
- Retraction Watch's "Papers and peer reviews with evidence of ChatGPT writing" lists 95 entries (92 papers, 2 peer reviews, 1 author response). Entries give title, venue and DOI, plus a PubPeer link. They do not include the offending excerpt. The list is built on Guillaume Cabanac's search strategy. — [Retraction Watch list](https://retractionwatch.com/papers-and-peer-reviews-with-evidence-of-chatgpt-writing/)
- Problematic Paper Screener (as of 2026-11-06) runs these detectors: Annulled, Concerning, Feet of Clay, Tortured, Suspect, SCIgen, Mathgen, Citejacked, Seek&Blastn and Problematic Cell Lines. None of them is an LLM-fingerprint detector. "Tortured phrases" targets paraphrasing-tool output (pre-LLM spinning), which is a different kind of slop. — [PPS home](https://dbrech.irit.fr/pls/apex/f?p=9999:1)
- As of Jan 2025, PPS / Cabanac had flagged more than 70 papers with ChatGPT fingerprints ("Regenerate Response", "As an AI language model, I cannot…") and contributed to over 1,000 retractions in total (snippet only, via a Conversation syndication). — [Brewminate repost of The Conversation](https://brewminate.com/problematic-paper-screener-trawling-for-fraud-in-scientific-literature/)
- Academ-AI (Alex Glynn, Univ. of Louisville) analysed 500 suspected undeclared-AI instances found by searching Google Scholar for chatbot phrases. It is ongoing, and a data snapshot was published. Very few cases were corrected after publication. — [arXiv 2411.15218](https://arxiv.org/abs/2411.15218v1); academ-ai.info returned HTTP 403 to my fetch, so the current count is unverified.
- Population-level studies give no per-document labels. Liang et al. (ICML 2024) estimate 6.5–16.9% of peer-review text at ICLR 2024, NeurIPS 2023, CoRL 2023 and EMNLP 2023 "may have been substantially modified by LLMs". arXiv v1 gives ICLR about 10.6% and EMNLP 16.9%. — [ICML 2024 oral](https://icml.cc/virtual/2024/oral/35507); [arXiv 2403.07183](https://arxiv.org/html/2403.07183v1)
- Liang et al. 2024 estimate LLM-modified content reached 17.5% in CS abstracts and 15.3% in introductions by Feb 2024 (950,965 papers). — [arXiv 2404.01268](https://arxiv.org/abs/2404.01268v1)
- Kobak et al., Science Advances (July 2025), found at least 13.5% of 2024 PubMed abstracts were LLM-processed (15M+ abstracts). Excess words were mostly *style* words. Code and word lists are on GitHub. — [arXiv 2406.07016](https://arxiv.org/abs/2406.07016v5); [berenslab/llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab)
- ICLR 2026 reviews: Pangram's EditLens classified about 21% of ~75,800 reviews as fully AI-generated (posted 2025-11-18; reviews pulled from the public OpenReview API). That is a detector label, not a human one. A critique found Pangram flagged 3.1% of human-written, AI-polished reviews as "AI". — [Pangram blog](https://pangram.com/blog/pangram-predicts-21-of-iclr-reviews-are-ai-generated); [arXiv 2603.20450](https://arxiv.org/html/2603.20450v1)

#### News / content farms
- NewsGuard lists 3,749 "AI Content Farm" sites in 16 languages (page "Last Updated June 23, 2026"). Inclusion requires all four of: (1) a substantial share of content is AI-produced; (2) little or no human oversight, e.g. chatbot error messages left in; (3) a generic name or layout that implies human journalists; (4) no disclosure. The full domain list is not public and is available on request; only 2 example names are shown. — [NewsGuard AI Tracking Center](https://www.newsguardtech.com/special-reports/ai-tracking-center/)
- In March 2026 NewsGuard launched a real-time detection datastream with Pangram, reporting 3,006 sites as of 2026-03-17 and 300–500 new sites per month. Analysts reportedly review Pangram flags by hand (snippet only). — [NewsGuard press release](https://newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news); [mediacopilot](https://mediacopilot.ai/newsguard-pangram-ai-content-farm-detector/)
- Google's "scaled content abuse" policy: "many pages are generated for the primary purpose of manipulating search rankings and not helping users … no matter how it's created". Its examples include "Using generative AI tools … to generate many pages without adding value for users". No list of penalized sites is published; sites are notified privately through Search Console manual actions. — [Google Search spam policies](https://developers.google.com/search/docs/essentials/spam-policies)

#### Open source / bug bounties
- curl's maintainer keeps a public gist, "AI slop security reports submitted to curl", with 49 entries (last active 2026-10-28). Each links to a disclosed HackerOne report (#2199174 to #3516202). The gist states its policy is to "instantly" ban AI-slop reporters, and adds that "several other issues not included here are highly suspicious as well". — [bagder gist](https://gist.github.com/bagder/07f7581f6e3d78ef37dfbfc81fd1d1cd)
- curl ended its HackerOne bug bounty, accepting reports until 2026-01-31, citing low-effort AI reports. Stenberg said he had not seen "a single valid security report produced with AI help". — [BleepingComputer](https://bleepingcomputer.com/news/security/curl-ending-bug-bounty-program-after-flood-of-ai-slop-reports/); [Hackaday 2026-01-26](https://hackaday.com/2026/01/26/the-curl-project-drops-bug-bounties-due-to-ai-slop)
- GitHub search on 2026-11-07, issues and PRs by label: `label:"ai slop"` 2,362; `label:ai-slop` 718; `label:slop` 1,729; `label:"llm-generated"` 1,989; `label:ai-generated` 56,411. Among the first 100 results, one repo dominates each label: flathub/flathub has 60 of 100 "ai slop" hits, all PRs, and leanprover-community/mathlib4 has 64 of 100 "llm-generated" hits. "ai-generated" is mostly self-labeled AI-authored work, not slop judgments. — [GitHub Search API](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests) (queried via `gh api search/issues`)
- OSS policies: Gentoo (Apr 2024) and NetBSD banned LLM-generated code. Ghostty (Jan 2026) restricts AI contributions to pre-approved issues. tldraw (Jan 2026) auto-closes external PRs. Godot tightened its rules on 2026-06-30. COSMIC requires certifying there is no LLM-generated code, comments or descriptions. All of these are from secondary sources. — [devgenius](https://blog.devgenius.io/open-source-projects-are-now-banning-ai-generated-pull-requests-8e1dd3e8d41c); [codenote](https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/); [letsdatascience on COSMIC](https://letsdatascience.com/news/cosmic-bans-ai-generated-pull-request-content-df1a405a)

#### Publishing platforms (policies only, no public item labels)
- Medium: "Medium is for human storytelling, not AI-generated writing." Since 2024-05-01, AI-generated writing (disclosed or not) is not eligible for the Partner Program paywall. AI outlining and grammar tools are exempt (snippet only). — [Medium AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)
- Amazon KDP capped self-publishing at 3 titles per day (Sept 2023) and asks authors to disclose AI-generated text, images and translations per title. Disclosures are not public (snippet only). — [The Register 2023-09-22](https://www.theregister.com/2023/09/22/amazon_ai_book_publishing_limit/); [Authors Guild](https://authorsguild.org/news/amazon-adds-to-kdp-generative-ai-policy-caps-daily-self-publishing-uploads/)

#### Education
- I found no public dataset of real student essays labeled AI-written by instructors. The nearest material is case analyses, such as 149 AI-plagiarism cases across 35 course sections (Apr 2023 – Oct 2025, not released), and incident logs of false accusations. — [AI Incident Database, Turnitin entity](https://incidentdatabase.ai/es/entities/turnitin); [OJDLA 2026 via academia.edu](https://independent.academia.edu/HaroldAbrams)
- Detectors flagged 61.22% of TOEFL essays by non-native writers as AI, which is evidence against using detector labels for this genre. — [search summary of Stanford study, incidentdatabase](https://incidentdatabase.ai/es/entities/turnitin)

#### Catalog summary (precision tier, volume, text retrievable?)

| Source | What's labeled | Label form | Volume (date) | Text retrievable | Precision |
|---|---|---|---|---|---|
| WP G15 deletions | Whole pages | CSD tag plus deletion-log summary | about 6 per 12.6 h sample (2026-11-07) | **No** (deleted; admins only). Log summary and title only | Very high (artifact-based) |
| WP {{AI-generated}} | Articles or sections | Template, `reason=`, `certain=`, date | 7,648 current (2026-11-07) | Yes (history, dumps, API) | Moderate-high (editor judgment, mostly style tells) |
| WP AI noticeboard | Users and their edits | Case page per user | 950 cases (Sep 2025 – Nov 2026) | Yes (contribs plus diffs) | High at user level, mixed at edit level |
| WP "Signs of AI writing" examples | Diffs and excerpts with highlighted tells | Curated, with tell category | about 115 diff/oldid links | Yes | Very high, tiny |
| WP abuse filter 1325 / 1346 / 1418 | Individual edits | Filter tag and log | 13,890 / 14,661 / 572 hits | Yes (log `added_lines`) | Low-moderate (regex, not reviewed) |
| WP filter 1407 (tag removal) | Cleanup edits | Log | 4,063 hits | Yes (diffs) | Noisy as "fixed" signal |
| SO generative-AI ban | Answers/questions | Mod deletion, canned comments | Unknown | Mostly no (deleted) | Moderate-high |
| Retraction Watch ChatGPT list | Papers and reviews | List plus PubPeer link | 95 | Via DOI (often paywalled); no excerpts | Very high (fingerprint phrases) |
| Academ-AI | Papers | Excerpt-level catalog | 500+ (Nov 2024) | Partly (snapshot) | Very high (phrase-based) |
| NewsGuard content farms | Domains | Proprietary label | 3,749 (2026-06-23) | Crawlable *if* you have the list; list is private | High (4 criteria, analyst-reviewed) |
| curl slop gist | Security reports | Maintainer list | 49 (2026-10-28) | Yes (disclosed H1 reports) | Very high |
| GitHub "ai slop" labels | PRs and issues (mostly code) | Repo label | about 2.4k + 0.7k + 1.7k | Yes (API) | Varies by repo; text is mostly PR descriptions |
| Pangram on ICLR 2026 | Reviews | Detector score | ~16k of 75.8k "fully AI" | Yes (OpenReview) | Detector-only (FP 3.1% on polished human text) |

### Inferences
- Ever-tagged Wikipedia articles: about 11.7k or more is a lower bound. That is 7,648 still tagged plus at least 4,063 tag-removal events logged by filter 1407. The two overlap only if an article is retagged, and the filter misses removals from before it existed and removals by page deletion. My working estimate for Nov 2026 is 12k–15k articles ever tagged, plus a few thousand G15/LLMPROD-deleted pages. The deletion figure is a rough extrapolation from about 11 G15 deletions per day in my single 12.6-hour sample, applied from Aug 2025; it is not a measured count.
- Revision-level count: each tagged article has at least one AI-insertion revision. Filter 1325 alone logged 13,890 suspected-AI edits. So the "suspected AI edit" population with retrievable text is in the tens of thousands, of which a human-tagged subset of roughly 8k–15k is the high-precision core.
- Genre fit for an explainer/memo/docs style model: Wikipedia (encyclopedic, informational) beats academic prose and Stack Overflow (instructive, but inaccessible). Content farms are news-rewrite slop. curl/HackerOne is technical-report slop, useful for a "docs" voice but small. The Signs page itself says it is most useful for *informational* writing.
- Only Wikipedia, GitHub labels and curl reach "retrievable text" with no partnership or legal hurdle. Of those, only Wikipedia reaches 1k+ with high precision on prose.

### Gaps
- I could not get the cumulative count of articles ever tagged {{AI-generated}}, or the exact total of G15 deletions. That needs a full-history dump scan or a Toolforge/Quarry query on `logging` and `templatelinks` history; the public API rate-limited me (HTTP 429) at about 1 request per 2.5 s.
- Filter 1407's creation date, needed to bound its 4,063 hits in time, was not retrieved.
- I did not verify whether abuse-log `added_lines` stay visible after the underlying page is deleted.
- Stack Overflow: I found no source counting deleted AI answers. I believe (prior knowledge, not re-verified; meta.stackoverflow.com and stackoverflow.com blocked my fetch tool) that deleted posts are excluded from both the data dump and SEDE.
- I could not fetch Academ-AI's current count (HTTP 403).
- No current 2026 count of PPS/PubPeer LLM-fingerprint flags was found.
- I did not research Quora, Reddit moderator removals, Google/Mozilla bug-bounty slop, or non-English Wikipedias (e.g. German "KI" templates).
- Clarkesworld (fiction, note only): I recall it closed submissions on 2023-02-20 after a surge of AI spam, from Neil Clarke's "A Concerning Trend" post (prior knowledge, not re-verified).

## Q2. Which sources provide before/after human fixes (preference pairs)?

### Takeaway
Only Wikipedia gives before/after human fixes at scale, and even there the "fix" is usually a revert, removal or stubify, not a sentence-level human rewrite. Usable pairs come from three revision types: pre-insertion human text vs. AI insertion, AI text vs. cleanup revision, and the curated Signs-page diffs. Everything else gives a label with no fix, except Wikipedia's edit summaries, which give the reason.

### Cited Findings
- Every tag, insertion and cleanup is a revision with a diff. The {{AI-generated}} `reason=` parameter records why the editor tagged the page. — [Template:AI-generated](https://en.wikipedia.org/wiki/Template:AI-generated)
- Filter 1407 logs 4,063 removals of the AI-generated tag. These events point at the cleanup revision, whose parent revision is the tagged AI text. — [Special:AbuseFilter/1407](https://en.wikipedia.org/wiki/Special:AbuseFilter/1407)
- Sample 1407 event (2026-11-07, "Galaja resistance (1992)"): rev 1384290000 (9,273 bytes) became rev 1384371846 (9,162 bytes), with the summary "I removed the content that COULD be AI. There is nothing AI-ish here anymore, if this is the future of wikipedia where everything is going to be tagged AI then it's truly over". This shows cleanup diffs can be small, contested and done by the original author. — [diff 1384371846](https://en.wikipedia.org/w/index.php?diff=1384371846)
- The project's recommended remedy is removal: "Any such material should be removed" (template fix text). When a topic is worth keeping, editors are advised to "rewrite it or stubify it" (snippet only, via a mirror of the Guide). — [Template:AI-generated](https://en.wikipedia.org/wiki/Template:AI-generated); [WikiProject AI Cleanup/Guide (mirror)](https://cavac.at/cavacopedia/Wikipedia%3AWikiProject%20AI%20Cleanup%2FGuide)
- "Signs of AI writing" holds about 115 diff/oldid links. Examples are dated ("From this September 2024 revision to Statistical Institute of Catalonia") and the tell spans are highlighted, so each example gives (AI revision, tell category, highlighted span). The pre-AI revision is one hop away in history. — [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- The Signs page also catalogs tells in *edit summaries* written by LLMs, such as "Canned assurance of adherence to Wikipedia policies" ("ensured that… adheres to, refined, enhanced, streamlined… neutral tone, encyclopedic tone, clarity, flow") and "preserved/retained… avoided". These are AI copyedits that "improve" prose, and they make natural AI-rewrite vs. original-human pairs. — [Signs §Edit summaries](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- WP:LLM asks that LLM use "be mentioned in the edit summary", so disclosed AI edits are findable by summary text. — [Wikipedia:Large language models](https://en.wikipedia.org/wiki/Wikipedia:Large_language_models)
- Medium, KDP, NewsGuard, Stack Overflow, Retraction Watch and the GitHub labels give no fix. Papers that are corrected rarely fix the problem properly: "corrections are often insufficient to rectify the problem". — [arXiv 2411.15218](https://arxiv.org/abs/2411.15218v1)

### Inferences
- Wikipedia pair types, best first:
  - (a) **AI-copyedit pairs**: original human paragraph vs. the LLM "improved" version. Find them through edit summaries matching the canned-assurance tells, or through revisions later reverted for LLM use. This is closest to the project's need, because the same content gets restyled into slop.
  - (b) **Insertion pairs**: the revision before the AI insertion (human) vs. the AI insertion, at section level. Get these by locating the tagged section and bisecting history.
  - (c) **Cleanup pairs**: the AI-tagged revision vs. the removal or rewrite revision, from filter 1407 and summaries containing "LLM", "AI-generated", "WP:LLM", "AIC", "chatbot". Many are deletions, not rewrites, so filter for diffs where text was replaced rather than only removed.
  - (d) **Noticeboard mass cleanups**: the 950 cases' contribution lists, followed by reverts carrying the `mw-reverted` tag.
- Expect true rewrite-style (AI paragraph, human-rewritten paragraph) pairs to be a minority of cleanup diffs, plausibly under 20–30%. This is a judgment, not measured; sample 200 diffs to calibrate.
- For DPO/ORPO on a 7–9B QLoRA run, a few hundred to a few thousand clean section-level pairs from (a) and (b) are likely enough to be useful. The 7.6k tagged articles should yield that after filtering.

### Gaps
- No existing public dataset (Hugging Face or otherwise) of WikiProject AI Cleanup before/after pairs was found. — [search, no hit](https://huggingface.co/datasets/OVHaiLLM/Clean-Wikipedia-English-Articles)
- I did not measure the share of cleanup diffs that are rewrites vs. removals.
- I did not check whether German, French or other Wikipedias have similar tagged sets.

## Q3. What are the licenses and access mechanics (Nov 2026)?

### Takeaway
Wikipedia is open (CC BY-SA 4.0 text; public API, dumps and abuse log). Stack Exchange content is CC BY-SA, but the official dump's download terms forbid LLM training, so using it for a style model breaks those terms even though the license itself allows it. NewsGuard is proprietary. Academic, HackerOne and GitHub text carries per-item copyright with no blanket license.

### Cited Findings
- Wikipedia: all the label and text artifacts above can be fetched read-only through the MediaWiki Action API (categoryinfo, embeddedin, revisions, compare, abuselog with `details`, logevents). I did this on 2026-11-07 and hit HTTP 429 rate limits at about 1 request per 2.5 s. — [MediaWiki API](https://en.wikipedia.org/w/api.php)
- Deleted pages (G15/LLMPROD outcomes) are visible only as deletion-log entries (title, summary). Their content is not public. — [Special:Log/delete](https://en.wikipedia.org/wiki/Special:Log/delete)
- Wikipedia text license: CC BY-SA 4.0 (plus GFDL for older contributions). — [Wikipedia:Copyrights](https://en.wikipedia.org/wiki/Wikipedia:Copyrights) (prior knowledge, not re-fetched)
- Stack Exchange, since July 2024: the dump sits behind a login. Users go to profile, Data dump access, and tick a box confirming they won't use it for LLM training; non-compliers may lose access. Critics argue this conflicts with CC BY-SA 4.0. — [devclass 2024-07-30](https://devclass.com/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-as-critics-complain-license-permits-reuse-for-any-purpose); [StackApps help mirror](https://backiee.wasmer.app/https_stackapps_com/help/data-dumps)
- The 2025-12-31 dump is 98.34 GB in 364 files, licensed CC BY-SA by version and date. The 2025-06-30 dump contained watermarks and bogus entries; none were known in 2025-12-31 at upload. — [Academic Torrents 2025-12-31](https://academictorrents.com/details/0d1d597fa7809f0e85f127b5eb3088219ddbad39)
- A community archive.org mirror calls itself an "unofficial replacement for the now-killed official archive.org release". — [archive.org stackexchange_20251231](https://archive.org/details/stackexchange_20251231)
- NewsGuard: the list is available by request only. No license is stated publicly. — [NewsGuard AI Tracking Center](https://www.newsguardtech.com/special-reports/ai-tracking-center/)
- Retraction Watch ChatGPT list: no license or downloadable format is stated. — [Retraction Watch list](https://retractionwatch.com/papers-and-peer-reviews-with-evidence-of-chatgpt-writing/)
- PPS: no export or license terms on its homepage. — [PPS](https://dbrech.irit.fr/pls/apex/f?p=9999:1)
- ICLR 2026 reviews are publicly retrievable via the OpenReview API (which is how Pangram got them). — [Pangram blog](https://pangram.com/blog/pangram-predicts-21-of-iclr-reviews-are-ai-generated)
- The curl reports are public HackerOne disclosures linked from the gist. — [bagder gist](https://gist.github.com/bagder/07f7581f6e3d78ef37dfbfc81fd1d1cd)

### Inferences
- For a private, local style model, Wikipedia-derived negatives are the cleanest legally. CC BY-SA share-alike would bite only if the derived *dataset* is redistributed; keep attribution metadata (page, revid, editor) anyway.
- Avoid the official Stack Exchange dump for training, because of the click-through LLM-training prohibition. Community torrents carry the same CC BY-SA content without the click-through, but that is a legal grey area. Get counsel before using them.
- HackerOne, GitHub issue text and journal articles need fair-use/research reasoning or per-item license checks. Treat them as eval-only unless cleared.

### Gaps
- I did not verify a license for abuse-log content specifically, or HackerOne's terms for disclosed reports.
- OpenReview review license and Crossref/Retraction Watch database terms were not verified.
- No primary page was fetched for the current stackoverflow.com dump terms (the fetch tool was blocked).

## Q4. What does each label really mean (AI-generated vs. low quality), and how much is stylistic slop vs. merely undisclosed AI?

### Takeaway
Almost every label here certifies *provenance* or *policy violation*, not bad style. Even so, the labelers, especially Wikipedia's, detect provenance mostly through stylistic tells, so the tagged sets are rich in style slop. The highest-precision labels (G15, chatbot-phrase fingerprints, curl) key on copy-paste artifacts and fabrication, which means "unedited", not necessarily "stylistically bad".

### Cited Findings
- G15 deliberately excludes stylistic signs ("not sufficient") and relies on user-directed communication, fake references and markup artifacts. — [WP:G15](https://en.wikipedia.org/wiki/Wikipedia:Criteria_for_speedy_deletion#G15)
- {{AI-generated}} labels a *policy* breach ("text from a large language model, which is prohibited"). It is "suspected" unless `certain=yes`. — [Template:AI-generated](https://en.wikipedia.org/wiki/Template:AI-generated)
- The Signs page warns that humans detect AI poorly: one 2025 study found human ability was "no better than random chance", while "expert" annotators who use LLMs heavily reached 90% detection with 3.3% false positives. It lists *ineffective* indicators: perfect grammar, mixed registers, "bland/robotic" prose, "fancy/academic" prose and isolated transition words. — [Signs §Your detection ability, §Ineffective indicators](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- The Signs page is "less useful for texts which are not informational writing". — [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Stack Overflow's ban rationale is correctness ("rate of getting correct answers … is too low") and plausibility ("they typically look like the answers might be good"), not style. — [SE API meta.SO 421831](https://api.stackexchange.com/2.3/questions/421831?site=meta.stackoverflow&filter=withbody)
- NewsGuard's label requires little human oversight *and* non-disclosure *and* a deceptive presentation, so it combines deception with low oversight. — [NewsGuard](https://www.newsguardtech.com/special-reports/ai-tracking-center/)
- Google's policy targets value and intent ("no matter how it's created"), not AI provenance. — [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- curl's "slop" means fabricated or invalid vulnerability claims. — [BleepingComputer](https://bleepingcomputer.com/news/security/curl-ending-bug-bounty-program-after-flood-of-ai-slop-reports/)
- Kobak et al.: 2024's excess vocabulary was mainly *style* words, unlike COVID-era content words. This supports AI provenance showing up as lexical style. — [arXiv 2406.07016 summary](https://arxiv.org/abs/2406.07016v5)
- False-positive risk: the tag-removal sample shows an editor disputing the tag. Detectors flag 3.1% of human AI-polished reviews and 61% of non-native TOEFL essays. — [diff 1384371846](https://en.wikipedia.org/w/index.php?diff=1384371846); [arXiv 2603.20450](https://arxiv.org/html/2603.20450v1); [incidentdatabase](https://incidentdatabase.ai/es/entities/turnitin)

### Inferences
These style-slop shares are my judgment estimates; none was measured.
- **WP {{AI-generated}}**: about 70–90% of tagged passages likely show the Signs-page style tells (puffery, "-ing" superficial analysis, AI vocabulary, rule of three, "Challenges and Future Outlook" sections). The rest were tagged for citation or markup artifacts or editor history. Best match to "AI slop in informational prose".
- **G15 pages**: close to 100% unedited chatbot output. Usually stylistically sloppy as well, but the label's evidence is artifacts. Text is unavailable anyway.
- **Filter 1325 edits**: a mix. Many are pasted chatbot or AI-search UI fragments ("Ask anything", "Would you like to know more…"). These are good negatives for "never output this", but weak as *style* negatives.
- **SO AI answers**: perhaps 50–70% stylistically sloppy (preambles, "Certainly!", over-structured bullets); the label is mostly about correctness.
- **Academic fingerprint papers**: the artifact is a leftover phrase. Surrounding prose is often generic LLM academic style, but the label does not certify that.
- **NewsGuard content farms**: high style slop plus plagiarized rewrites. Good negatives for "generic news explainer" voice.
- **curl / HackerOne**: high style slop (markdown headers, CVSS boilerplate, confident fabricated detail). An excellent small eval set for technical-report slop.
- **Pangram / detector-only sets**: unknown mix. Use only as weak labels.
- The negative set should therefore be split into three classes, because they teach different things: artifact-negatives (never emit), style-negatives (Signs tells), and content-negatives (fabrication). A style model mainly needs the second class.

### Gaps
- No source measures the stylistic-sloppiness share within any labeled set. A small hand audit is needed: about 200 Wikipedia-tagged passages scored against the Signs taxonomy.

## Q5. What taxonomy of tells do Wikipedia's labelers use? (Extracted from "Wikipedia:Signs of AI writing", live revision 2026-11-07)

### Takeaway
The guide is the most detailed public, human-curated taxonomy of informational-prose AI tells. It is organised into content, language, style, communication, markup, citations, edit summaries and miscellaneous signs, each with dated real examples and diffs. It also marks tells as era-specific (vocabulary by model generation) and lists ineffective and historical indicators. It can be lifted directly into eval rubrics and feature-based reward checks.

### Cited Findings
All items below are from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), live as of 2026-11-07.
- **Content**:
  - Undue emphasis on significance, legacy and broader trends: "stands/serves as, is a testament/reminder, a crucial/pivotal/vital/significant/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted". Example: "officially established in 1989, marking a pivotal moment in the evolution of regional statistics".
  - Canned emphasis on notability and media coverage: "independent coverage, local/regional/national media outlets, cited/featured/profiled in, active social media presence".
  - Undue emphasis on identification by primary or tertiary sources.
  - Superficial analyses, often a trailing "-ing" clause: "highlighting/underscoring/emphasizing…, ensuring…, reflecting/symbolizing…, contributing to…, fostering…, valuable insights, align/resonate with". Example: "…approximately 56,998 inhabitants, creating a lively community within its borders".
  - Vague connection: "in connection with, associated with".
  - Vague attributions: "Industry reports, Observers have cited, Experts argue, several sources".
  - Outline-like "Despite its… faces several challenges / Future Outlook" conclusions.
  - "Awards and recognition" and "X and Y" section headers.
- **Language and grammar**:
  - AI vocabulary by era:
    - 2023 to mid-2024 (GPT-4): Additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant.
    - Mid-2024 to mid-2025 (GPT-4o): align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
    - Mid-2025 to mid-2026 (GPT-5): emphasizing, enhance, highlighting, showcasing.
    - Mid-2026 on, as the page labels it: challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally, "with much more period and comma usage and shorter sentences around a strict 8–20 word limit".
    - Grok overuses "causal, empirical, correlate".
    - Editors may only add words "corroborated by at least one reliable, non-pop-science external source".
  - Avoiding the basic copula ("serves as/stands as/marks/represents", "boasts/features/offers" instead of "has").
  - Negative parallelisms ("Not just X, but also Y", "Not X, but Y", "Y rather than X").
  - Leads treating list titles as proper nouns.
  - Rule of three.
- **Style**: title case headings, overuse of boldface, inline-header vertical lists, wrong heading levels, emoji in headings, curly quotes.
- **Communication intended for the user**:
  - Collaborative phrases: "I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like…, let me know, here is a…".
  - Hedging about sources: "While specific details are limited/scarce…, not widely documented, in the provided/available sources…, based on available information".
  - Placeholders (dates, URLs).
- **Markup and citations**:
  - Markdown in wikitext; `oaicite`, `turn0search0`.
  - Broken links, invalid DOIs and ISBNs, DOIs pointing to unrelated papers, book citations without pages.
  - `utm_source=openai` / `utm_source=chatgpt.com` / `utm_source=copilot.com` / `referrer=grok.com`.
  - Named references declared but unused.
- **Edit summaries**: canned assurances of policy adherence; "preserved/retained/avoided/ensured"; overemphasis on citations ("added verified information…, improved attribution"); references to AfC review.
- **Miscellaneous**: a pronounced shift in a user's style, AfC "submission statements", pre-placed maintenance templates, canned user pages, permissions gaming, differences between LLMs, pro-authoritarian bias.
- **Ineffective indicators**: perfect grammar, mixed registers, "bland/robotic" prose, "fancy/academic" prose, isolated transitions.
- **Historical (dated) indicators**:
  - Promotional language (2023–2025: "boasts a, vibrant, rich, nestled, in the heart of, groundbreaking, renowned, diverse array").
  - Knowledge-cutoff statements (2022–2023).
  - Section summaries ("In summary, In conclusion, Overall").
  - Prompt refusal ("as an AI language model").
  - Em-dash overuse (2022–Sept 2026). The page notes newer models are "hard coded to not use em dashes at all" and that low punctuation variety "has become its own sign", though that claim is tagged citation-needed. It also cites a July 2026 study finding that of contemporary models only Claude used em dashes more than professional writers.
  - Abrupt cut-offs, outdated access-dates, elegant variation (from repetition penalties).
- **Signs of human writing**: age of text relative to ChatGPT's launch, ability to explain one's own editorial choices, syntax.

### Inferences
- The era-tagged vocabulary and the "historical indicators" section mean static slop lexicons go stale. An eval for a 2026 style model should include both older (GPT-4-era) and current (shorter-sentence, no-em-dash, "quietly/steady/matters") tells, or the model may learn to avoid only the old ones.
- The content-level tells (significance inflation, superficial "-ing" analysis, vague attribution, challenges/outlook conclusions) are genre-specific to explainers and analyses. They match the project's target nonfiction genres better than lexical lists do.

### Gaps
- I did not extract the Style subpage ("Wikipedia:Signs of AI writing/Style") or the separate "Signs of AI use in comments" page.
- I did not verify the external studies behind specific claims, such as the July 2026 em-dash study or the "GPT-6" era label; they are relayed as the page states them.
