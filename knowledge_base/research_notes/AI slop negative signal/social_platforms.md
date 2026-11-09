# Social and community platforms as sources of human-labeled "AI slop" (negative signal for a nonfiction style model)

Research date: 2026-11-07. All counts marked "measured" were run by this researcher on 2026-11-07 against live public APIs: HN Algolia, HN Firebase, the Arctic Shift Reddit API, and the MediaWiki API. The raw outputs and scripts are in `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/negsignal/` and `.../scratchpad/scripts/`. Claims taken only from search-engine summaries, not from a fetched primary page, are marked **(unverified: snippet)**.

## Q1. Which platform sources yield retrievable text plus a human slop label, at meaningful volume (≥1k examples), in informational nonfiction?

### Takeaway
Three sources clear the ≥1k bar with text you can retrieve and informational content:
1. **Wikipedia's AI Cleanup tags.** 7,764 articles are tagged right now. The text is nonfiction, CC BY-SA, comes with stated reasons, and the human cleanup edits give before/after pairs.
2. **Hacker News callout replies.** Thousands of phrase matches per year, with the parent comment or linked article retrievable, though most matches are not targeted callouts.
3. **Reddit callout comments via Arctic Shift dumps.** Very large volume, but the labels have to be mined from replies, and ToS risk is highest here.

LinkedIn, the platform most associated with slop, is a poor source. The labeled examples mostly circulate as screenshots (86% of recent r/LinkedInLunatics posts are images), and there is no API. X is expensive, and its terms bar training. Bluesky labelers target images, not text. Medium's AI labels are private curation decisions.

### Cited Findings

#### Catalog summary (one row per source)

| Source | Where labels live | Label form | Text retrievable? | Approx. volume | Nonfiction fit | Access (Nov 2026) |
|---|---|---|---|---|---|---|
| Wikipedia WikiProject AI Cleanup | `{{AI-generated}}`-style maintenance tags; monthly categories; G15 speedy deletions; talk pages | Editor tag (often with reason), deletion, cleanup diff | Yes, full revision history via MediaWiki API/dumps | 7,764 articles currently tagged (May 2025–Nov 2026), measured | Excellent (encyclopedic exposition) | Free API/dumps; CC BY-SA |
| Hacker News comments | Replies such as "clearly written by an LLM"; flags; mod notices from dang/tomhow; software auto-kill | Reply callout; flag/kill; mod notice | Parent comment yes (Firebase/Algolia), except flagged/killed items, which read "[flagged]"; linked articles need a separate fetch | "AI slop" 6,866 comments in 2026 YTD; "written by AI" 1,245; "LLM-generated" 3,154; only an estimated 10–35% are targeted callouts | Good (technical blogs, docs, essays, comments) | Free Algolia + Firebase APIs |
| Reddit (r/ChatGPT, r/antiai, r/aiwars, r/isthisAI, r/LinkedInLunatics, r/Professors, r/freelanceWriters, r/copywriting, etc.) | Reply callouts; mod removals ("Rule X: no AI content"); flair | Reply; removal; flair | Comment/self-post text yes via dumps; LinkedInLunatics mostly images | Millions of comments in AI-focused subs; callout subset unmeasured (API full-text search timed out) | Mixed: mostly casual comments; some posts/copy | Arctic Shift API/dumps (unofficial); Reddit API requires approval since Nov 2025 |
| LinkedIn | Comments on posts; r/LinkedInLunatics reposts | Comment; screenshot repost | Rarely (screenshots; no API) | Prevalence studies only (41–54% of long posts flagged AI by detectors) | Excellent genre match (business explainers/memos) | No usable API; ToS bars scraping |
| X/Twitter | Quote-tweet dunks; replies; Community Notes | QT/reply; note | Yes via paid API | Unmeasured | Mixed | Pay-per-use (~$0.005/read, unverified); dev terms bar training |
| Bluesky | Replies; labelers (aimod.social); moderation lists | Label on post/account; reply | Yes (open firehose/Jetstream) | Unmeasured; labelers focus on images | Mixed | Free, open protocol; advisory AI-consent signals |
| Medium | Internal curation ("Network Only" distribution, paywall removal) | Private platform decision | No (labels not public) | Unknown | Good | N/A |
| Stack Overflow / Stack Exchange | Mod deletions of ChatGPT answers (ban Dec 2022) | Deletion | Deleted posts generally not in public dumps (inference) | Unknown | Excellent (technical answers) | Dumps lack deleted content |
| Curated "AI tells" lists (Wikipedia guide, GitHub humanizer/unsloppify/slopbuster, tropes.fyi) | Pattern catalogs with some before/after examples | Pattern + explanation | Yes | Tens to hundreds of patterns, not thousands of examples | Good (patterns are genre-general) | Mostly open licenses |

#### Hacker News (measured, HN Algolia API `https://hn.algolia.com/api/v1/search`, phrase queries, `tags=comment`, by calendar year; 2026 = Jan 1–Nov 7)
- Comment counts by phrase, 2022 / 2023 / 2024 / 2025 / 2026 YTD — measured via [HN Algolia API](https://hn.algolia.com/api/v1/search?query=%22AI%20slop%22&tags=comment):
  - "AI slop": 0 / 0 / 385 / 3,215 / 6,866. Stories with the phrase: 0 / 0 / 21 / 241 / 588.
  - "LLM-generated" (Algolia treats it the same as "LLM generated"): 6 / 312 / 612 / 1,590 / 3,154.
  - "written by AI": 39 / 206 / 223 / 604 / 1,245. "AI written": 39 / 191 / 145 / 471 / 1,749.
  - "written by an LLM": 0 / 43 / 73 / 258 / 492.
  - "written by ChatGPT": 51 / 288 / 102 / 99 / 43. The vocabulary moved from naming ChatGPT to "LLM" and "slop".
  - "reads like AI": 4 / 7 / 8 / 44 / 100. "smells like AI": 1 / 0 / 3 / 15 / 26. "sounds like ChatGPT": 1 / 19 / 8 / 14 / 9.
  - "em dash": about 30/yr in 2020–2022 (32, 27, 30), then 127 (2023), 54 (2024), 980 (2025), 1,055 (2026 YTD). This is a proxy for the em-dash-as-AI-tell discourse.
  - "slop" (any use): 128 (2022) → 1,562 (2024) → 8,473 (2025) → 22,695 (2026 YTD).
- Precision of phrase matches (measured on a small sample: 12 random 2026 comments per phrase, read by hand; [Algolia search_by_date](https://hn.algolia.com/api/v1/search_by_date?query=%22written%20by%20an%20LLM%22&tags=comment)):
  - "written by an LLM": about 4 of 12 were targeted callouts. Examples: "it's clearly written by an LLM instead of a person"; "It was definitely written by an LLM, the entire article is full of 'it's not X, it's Y' overconfident truisms"; a callout aimed at a project's docs. The rest were about code, hypotheticals, or denials. One was a non-native speaker joking that their grammar error "proves it was not written by an LLM".
  - "AI slop": about 1–2 of 12 targeted a specific item, such as a one-word "AI slop" reply to a story. Most were general discourse.
  - "LLM-generated": about 2 of 12, mostly about code.
  - Rough yield of targeted callouts from phrase matches: 10–35%. A classifier pass is needed. This is a small-sample estimate by this researcher, not a published figure.
- HN rule and moderation timeline. Quotes are from dang's comments, retrieved via the [Algolia items API](https://hn.algolia.com/api/v1/items/47340079) and [comment search tagged author_dang](https://hn.algolia.com/api/v1/search?query=generated%20comments&tags=comment,author_dang):
  - 2022-12-12 (item 33950747): "They're already banned—HN has never allowed bots or generated comments… We don't want canned responses from humans either!"
  - 2023-03-18 (35206303): "If people see AI-generated comments on HN they should flag them and let us know at hn@ycombinator.com. HN is a place for humans to converse, and bots have never been allowed."
  - 2023-05-15 (35954113): "HN users are allergic to LLM generated comments, including summaries."
  - 2023-06-09 (36252547): "Threads here need to be between humans."
  - 2025-02-18 (43085967): "We don't want LLM-generated comments… Downvoting or flagging comments that you think are generated is fine. 'Calling out' is more of a grey area".
  - 2026-03-06 (47270436): "(informal to date, probably soon to be formalized) rules… we don't allow either generated comments or AI-e[dited]…"
  - 2026-03-11: an HN thread titled "Don't post generated/AI-edited comments. HN is for conversation between humans" (item 47340079, 265 top-level replies). Since then, mod notices link both it and `newsguidelines.html#generated`. Same day (47342045): "We aren't asking people to not use AI… What we're asking is not to post AI-generated comments to Hacker News."
  - 2026-04-28 (47940483): "it looks like you've done it over 30 times already… there's no way to be certain of this, but it's what our software thinks".
  - 2026-05-24 (48257965): "Attacking another user like this is not acceptable, regardless of how/whether they used an LLM."
  - Oct–Nov 2026 (50156084, 50197564, 50397579): "Some of your recent comments have been killed by our software because they've been classified as genai text, which is not allowed on HN". HN now runs an automated genai classifier, so some "labels" are machine-made, not human.
- Current guidelines text (fetched from [HN guidelines](https://news.ycombinator.com/newsguidelines.html)): "Please don't put generated text in HN posts. Write your text yourself—HN is for sharing between humans. For the same reason, please don't automate posting."
- Moderator notice volume is small. Comments by dang containing the exact phrase "generated comments": 1 / 11 / 8 / 12 / 25 (2022–2026). tomhow: 0 / 0 / 0 / 9 / 13. dang's "genai text": 6 in 2026. These are exact-phrase counts and therefore lower bounds; the related non-phrase query matches 254 dang comments overall — measured via [Algolia](https://hn.algolia.com/api/v1/search?query=%22generated%20comments%22&tags=comment,author_dang).
- Moderator-labeled text is often gone. The parents of two dang removal notices (items 49949362 and 48222790) return the literal text "[flagged]" in both the [official Firebase API](https://hacker-news.firebaseio.com/v0/item/49949362.json) and the [Algolia items API](https://hn.algolia.com/api/v1/items/49949362). A third parent (50395314) still had its full text — measured.

#### Reddit (measured via the [Arctic Shift API](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md))
- Subreddit sizes from Arctic Shift `_meta` (comment counts updated about 2026-10-12) — [Arctic Shift subreddits endpoint](https://arctic-shift.photon-reddit.com/api/subreddits/search?subreddit=antiai):

  | Subreddit | Posts | Comments |
  |---|---|---|
  | r/ChatGPT | 550,222 | 7,615,646 |
  | r/OpenAI | 139,770 | 1,825,081 |
  | r/antiai | 72,252 | 2,118,915 |
  | r/aiwars | 69,298 | 3,483,531 |
  | r/isthisAI | 34,059 | 935,326 |
  | r/LinkedInLunatics | 88,873 | 3,050,448 |
  | r/Professors | 85,281 | 2,506,139 |
  | r/Teachers | 473,396 | 9,534,895 |
  | r/writing | 586,023 | 6,439,935 |
  | r/freelanceWriters | 38,360 | 311,220 |
  | r/copywriting | 40,733 | 288,304 |
  | r/ArtificialInteligence | 190,227 | 1,270,290 |
  | r/ChatGPTPro | 27,485 | 287,699 |

  r/RoastMyPost was not found. The subscriber fields in Arctic Shift's metadata are stale; r/antiai shows 471, so do not use them.
- Posts matching keywords, by year, 2022 / 2023 / 2024 / 2025 / 2026 YTD — measured via [posts/search/aggregate](https://arctic-shift.photon-reddit.com/api/posts/search/aggregate?subreddit=Professors&query=ChatGPT&aggregate=created_utc&frequency=year&after=2022-01-01):
  - r/Professors, "ChatGPT": 55 / 440 / 364 / 432 / 182.
  - r/freelanceWriters, "AI": 81 / 391 / 281 / 288 / 118.
  - r/LinkedInLunatics, "ChatGPT": 11 / 97 / 94 / 140 / 83.
  - The same queries for r/copywriting "AI" and r/Teachers "ChatGPT" timed out.
- r/LinkedInLunatics is a screenshot venue. Of its 100 most recent posts since 2026-09-01: 86 were image posts (85 on i.redd.it, 1 imgur), 13 were galleries, and only 5 had more than 200 characters of self-text. Only 2 titles mentioned AI or ChatGPT. 90 posts had no flair. Measured via [Arctic Shift posts/search](https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LinkedInLunatics&after=2026-09-01&limit=100).
- API limits, measured. Comment full-text (`body`) search returned "Timeout. Maybe slow down a bit" (HTTP 422) for r/freelanceWriters, r/copywriting, r/Professors and r/LinkedInLunatics. Callout counts are unmeasurable through the API, and the dumps are the practical path. The README says `body` search requires `author`, `subreddit`, `link_id` or `parent_id`; that "Keyword search isn't supported for very active users or subreddits"; and it recommends the monthly `.zst` dumps for large-scale work. It states no terms of use — [Arctic Shift API README](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md).
- Moderation research: Lloyd, Reagle and Naaman (CSCW 2025) interviewed 15 moderators of subreddits that restrict AI content. They found enforcement relies on "time-intensive and inaccurate detection heuristics". A companion study found AI rules "relatively uncommon", but the number of subreddits with them "more than doubled over the course of a year" — [arXiv 2311.12702](https://arxiv.org/abs/2311.12702); [Cornell Chronicle](https://news.cornell.edu/node/331751). These are search summaries; the rule-prevalence percentage was not fetched.

#### Wikipedia (an added venue, and the strongest nonfiction source)
- Currently tagged articles: 7,764 across 18 monthly subcategories of "Category:Articles containing suspected AI-generated texts" (May 2025 → Nov 2026). Examples: Oct 2026 = 847, Jul 2026 = 841, Sep 2026 = 736, Jun 2026 = 569, Dec 2025 = 565, Nov 2025 = 534. Measured via the [MediaWiki API categoryinfo](https://en.wikipedia.org/w/api.php?action=query&prop=categoryinfo&titles=Category:Articles_containing_suspected_AI-generated_texts&format=json).
- "Wikipedia:Signs of AI writing" is an advice page from WikiProject AI Cleanup, not policy, and has no community review — [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). It lists:
  - Content signs: inflated significance and "legacy" framing, promotional claims, superficial analysis, vague attributions, formulaic "challenges"/outlook sections.
  - Language signs: "AI vocabulary", avoidance of plain "is/are", negative parallelisms, rule of three.
  - Formatting and markdown, citation errors, chatbot-style messages.
  - "Historical indicators", including "overused em dashes (2022–September 2026)" and knowledge-cutoff disclaimers (2022–2023).
  - It links speedy-deletion criterion G15 (unambiguously LLM-generated pages) and limits it to "the most objective" signs.
- The project dates to late 2023, and the guide is its most thorough resource — [IEEE Spectrum](https://spectrum.ieee.org/wikipedia-wikiproject-ai-writing-cleanup); [404 Media](https://404media.co/the-editors-protecting-wikipedia-from-ai-hoaxes) **(unverified: snippet)**.

#### LinkedIn
- Originality.ai (Nov 2024) studied 8,795 posts of 100+ words, Jan 2018–Oct 2024. It found 54% "likely AI-generated", counting heavily AI-edited posts as AI. Its other figures: about a 189% jump after ChatGPT launched and +107% in average length. LinkedIn called the content "AI-assisted" — [The Register](https://www.theregister.com/2024/11/28/linkedin_ai_posts); [Website Planet](https://www.websiteplanet.com/news/linkedin-long-posts-ai); [Originality.ai](https://originality.ai/pt/blog/ai-content-published-linkedin) **(partly unverified: snippet)**.
- Pangram Labs (July 2026) analyzed 1,002,627 posts from LinkedIn, X, Reddit, Medium and Substack, collected April–June 2026 through a Chrome extension (what users scrolled past, not a random sample). Posts over 250 words flagged as fully AI: LinkedIn >40%, Medium 31%, Substack about 10% (21.9% fully or partly), and 25% across all platforms — [Fast Company](https://www.fastcompany.com/91571983/linkedin-is-the-most-ai-saturated-platform); [ThePrint](https://theprint.in/feature/ai-content-linkedin-x-pangram-report-substack-reddit-human/2983225/); [TechRadar](https://www.techradar.com/pro/ai-writing-is-now-a-problem-everywhere-on-social-media-study-finds-nearly-half-of-all-linkedin-long-posts-are-ai-generated-and-thats-only-the-start) **(unverified: snippet; original report not fetched)**. These are detector labels, not human labels.
- No public labeled dataset of LinkedIn posts (human vs AI) was found on Kaggle or Hugging Face. The only LinkedIn datasets found concern fake profiles — [search result: weaklinksinlinkedin](https://sites.google.com/view/weaklinksinlinkedin/datasets) **(unverified: snippet)**.

#### X / Twitter
- X is piloting LLM-written Community Notes ("AI note writers", July 2025) and tested "collaborative notes" in Feb 2026 — [Engadget](https://www.engadget.com/social-media/xs-latest-community-notes-experiment-allows-ai-to-write-the-first-draft-210605597.html) **(unverified: snippet)**. In a field study, LLM notes beat human notes on helpfulness, but the advantage was smallest for posts about AI-generated content — [Li & Bakker, arXiv 2604.02592](https://arxiv.org/abs/2604.02592) **(unverified: snippet)**. No source counted Community Notes that label text (as opposed to images) as AI-generated.
- The viral February 2025 X post calling the em dash an AI tell reportedly had 3.7M views — [Daily Dot](https://dailydot.com/culture/em-dash-ai/) **(unverified: snippet; attribution unclear)**.

#### Bluesky
- The main AI labeler, aimod.social ("AI Imagery Labeler"), is volunteer-run and covers images. Its handbook says it does not use detection software — [handbook](https://trail-buckthorn-014.notion.site/Bluesky-AI-Imagery-Labeler-Moderator-Handbook-65ef75d92a0e4faab0ad2925fc35c85c) **(unverified: snippet)**. A user can subscribe to at most 10 labelers, including Bluesky's own. Labelers are built with Ozone — [Bluesky moderation docs](https://www.docs.bsky.app/docs/advanced-guides/moderation) **(unverified: snippet)**. No text-slop labeler was found.

#### Medium and Substack
- Medium (from May 1, 2024): AI-generated writing, disclosed or not, cannot be paywalled. Undisclosed AI writing gets "Network Only" distribution. Enforcement combines detection tools with human review — [Medium help: AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy); [Plagiarism Today](https://www.plagiarismtoday.com/?p=42690) **(unverified: snippet)**. These are internal decisions; no public per-story label exists.
- Substack has the lowest AI share in Pangram's 2026 data. No platform-level slop label was found; callouts are writer-to-writer posts and Notes — [ThePrint](https://theprint.in/feature/ai-content-linkedin-x-pangram-report-substack-reddit-human/2983225/) **(unverified: snippet)**.

#### Stack Overflow
- Stack Overflow banned ChatGPT answers in December 2022. In June 2023, moderators struck after being told not to remove answers merely for being AI-generated and to stop using detectors. The company said the detectors had "an alarmingly high rate of false positives" — [DevClass](https://devclass.com/2023/06/05/stack-overflow-volunteer-moderators-down-tools-over-secret-new-policy-that-obstructs-removal-of-ai-generated-content/); [IT Brew](https://www.itbrew.com/stories/2023/06/21/stack-overflow-moderators-strike-after-being-told-to-let-the-chatgpt-flow) **(unverified: snippet)**.

#### Curated collections of tells (patterns rather than labeled examples)
- [blader/humanizer](https://github.com/ntuee10/humanizer) and its forks are numbered pattern lists built from Wikipedia's Signs of AI writing, with before/after examples. [woerndl/unsloppify](https://github.com/woerndl/unsloppify) has a trope catalog citing tropes.fyi by ossama.is. [gabelul/slopbuster](https://github.com/gabelul/slopbuster) claims 100+ patterns from 1,000+ samples. [haidrrrry/humanize-ai-writing](https://github.com/haidrrrry/humanize-ai-writing) also exists. **(unverified: snippet; contents not inspected)**. No "awesome-ai-slop" repo turned up.
- Academic human-labeled sets on nonfiction:
  - [Russell, Karpinska & Iyyer, ACL 2025](https://aclanthology.org/2025.acl-long.267): 300 nonfiction articles labeled by expert annotators, released with code.
  - [Shaib et al. 2025, "Measuring AI 'Slop' in Text"](https://arxiv.org/abs/2509.19163v1): binary slop judgments plus span-level "slop codes" on news and retrieval-augmented QA passages.

### Inferences
- The best negative-signal source for nonfiction is Wikipedia AI Cleanup. Each tagged revision is an informational text that a human judged LLM-like. The tag's reason, the talk-page discussion and the cleanup diff supply a "why". The cleanup rewrite gives a matched human-preferred version for contrastive or DPO-style pairs. Volume: about 7.8k currently tagged. Cumulative tagged revisions are likely higher, because removed tags leave the category, but that is unmeasured. The genre is encyclopedic, not memo or explainer, so use it for vocabulary and structural tells rather than voice.
- HN is the best source for informal-technical nonfiction. Taking about 10–35% targeted callouts out of several thousand 2025–2026 phrase hits gives roughly 1–3k labeled items per year from a few phrases. More phrasings ("LLM-written", "ChatGPT-ese", "GPT-isms", "AI-generated article") would raise that. The parent text comes back through the API unless the comment was flagged. For story-level callouts, the labeled object is an external blog post, which has to be fetched separately.
- Reddit has the largest raw volume but the lowest signal density for nonfiction. Callouts in r/ChatGPT, r/antiai and r/aiwars mostly concern comments, images or meta-discussion. r/freelanceWriters and r/copywriting talk about clients rejecting AI-sounding copy, but only a few hundred posts a year, and the rejected copy is rarely pasted. r/Professors carries about 400 ChatGPT posts a year, mostly anecdotes; student essays are rarely posted verbatim, probably for privacy.
- On LinkedIn, the "labeled examples" are screenshots. Mining r/LinkedInLunatics would need OCR on images, and most posts there are mocked for reasons other than AI.

### Gaps
- No measured count of targeted callout comments on Reddit: Arctic Shift's comment full-text search timed out. Counting needs the monthly dumps (comment bodies plus `parent_id` joins), which this pass did not download.
- r/RoastMyPost was not found. No data was gathered on per-subreddit removal reasons, which are not in public dumps, or on flair-based AI labels.
- Not measured: cumulative (not just current) Wikipedia AI tags, the share of tags carrying a reason, and G15 deletion counts. The "Candidates for speedy deletion as LLM-generated" category name guessed here does not exist.
- No source counted Community Notes about AI text, X quote-tweet dunks, or Bluesky reply callouts.
- YouTube and TikTok comment callouts were not researched beyond noting they exist. The YouTube Data API exposes comments, but quota and terms were not verified this session.
- Not inspected: the Pangram 2026 original report, and whether Originality.ai or Pangram release their labeled data.

## Q2. How noisy are the labels? Measurements of false accusations, disagreement and bias

### Takeaway
Community callouts are noisy, and they are biased in ways a style model should not learn:
- Callouts track perceived authenticity rather than actual AI features: prose features that tell AI from human text do not predict which human writing gets accused (Miklian & Katsos 2026).
- Detectors and naive heuristics over-flag non-native writers: an average 61% false-positive rate on TOEFL essays (Liang et al. 2023).
- Em-dash "witch hunts" are well documented.
- Recall is also poor: 1,783 AI comments on r/changemyview went undetected.

Only screened expert annotators are reliably accurate. The best five, majority-voting, misclassified 1 of 300 nonfiction articles.

### Cited Findings
- Miklian & Katsos, "'That's AI Slop, You Bot!' Studying Accusations, Evidence, and Credibility in Online Discourse Towards LLM-Generated Comments" (arXiv 2606.12073, 10 June 2026) — [arXiv abstract](https://arxiv.org/abs/2606.12073):
  - Corpus: 25M HN and Reddit comments, 2023–2026. Method: LLM judgment of 7,500 sampled accusations, speech-act coding of 300 confirmed ones, and a matched-control comparison of accused vs non-accused parent comments.
  - The pejorative share of accusations rose more than tenfold on both platforms, while the placebo terms "shill" and "astroturf" did not rise. "AI slop" accounts for 94% of pejorative mentions.
  - Prose features that distinguish AI from human text do not predict which human writing gets accused. The authors conclude accusations work as "social gatekeeping of perceived authenticity rather than AI detection".
  - The abstract gives no false-positive rate and no data-release statement. The license is CC BY-NC-ND 4.0.
  - Secondary summaries add that the sample covered 18 subreddits and that only formal-register adverbs were marginally predictive (p = 0.083) — [Unite.AI](https://www.unite.ai/the-rise-of-ai-slop-accusations-is-becoming-a-new-form-of-gatekeeping/) **(unverified: snippet; full text 404'd)**.
- Liang et al. 2023 ("GPT detectors are biased against non-native English writers", *Patterns*) — [arXiv 2304.02819](https://arxiv.org/pdf/2304.02819); [Times Higher Education](https://www.timeshighereducation.com/node/727071); data on [HF: WxWx/ChatGPT-Detector-Bias](https://huggingface.co/datasets/WxWx/ChatGPT-Detector-Bias/blob/main/README.md?code=true) **(figures via snippets; consistent across sources)**:
  - 7 detectors were tested on 91 TOEFL essays and 88 US 8th-grade essays. The average false-positive rate on TOEFL essays was about 61% (61.22%), and 89 of 91 (97.8%) were flagged by at least one detector.
  - The authors attribute the bias to low perplexity from limited lexical variety.
- Russell, Karpinska & Iyyer (ACL 2025) — [ACL Anthology](https://aclanthology.org/2025.acl-long.267); [arXiv 2501.15654](https://arxiv.org/abs/2501.15654) **(via snippets)**:
  - Frequent LLM users are accurate detectors on 300 nonfiction articles; a majority vote of 5 experts misclassified 1 of 300.
  - The experts were the top performers (>90% accuracy) out of 70+ screened annotators, so this does not describe the typical commenter.
  - Experts relied on "AI vocabulary" plus formality, originality and clarity.
- Shaib et al. 2025: binary "slop" judgments are "(somewhat) subjective" but correlate with coherence and relevance. Off-the-shelf LLMs agree poorly with human slop annotators — [arXiv 2509.19163](https://arxiv.org/abs/2509.19163v1) **(aggregator detail unverified)**.
- Recall: University of Zurich researchers posted 1,783 AI comments on r/changemyview over about 4 months. By their own account, no one in the subreddit discovered the bots — [Engadget](https://engadget.com/ai/researchers-secretly-experimented-on-reddit-users-with-ai-generated-comments-194328026.html?src=rss); [SAN](https://san.com/cc/university-of-zurichs-unauthorized-ai-experiment-on-reddit-sparks-controversy/) **(unverified: snippet)**.
- Moderators' self-assessment: detection relies on "time-intensive and inaccurate detection heuristics" — [Lloyd et al., arXiv 2311.12702](https://arxiv.org/abs/2311.12702).
- Platform admissions of uncertainty:
  - dang on HN: "there's no way to be certain of this, but it's what our software thinks" (2026-04-28); and "Attacking another user like this is not acceptable, regardless of how/whether they used an LLM" (2026-05-24) — [HN Algolia](https://hn.algolia.com/api/v1/search?query=generated%20comments&tags=comment,author_dang).
  - Stack Overflow said detectors had "an alarmingly high rate of false positives" — [DevClass](https://devclass.com/2023/06/05/stack-overflow-volunteer-moderators-down-tools-over-secret-new-policy-that-obstructs-removal-of-ai-generated-content/).
  - Wikipedia's guide: "Not all text featuring these indicators is AI-generated"; "Do not solely rely on artificial intelligence content detection tools"; humans are "notoriously bad" at telling the two apart — [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
- Em-dash false positives:
  - Writers and outlets pushed back throughout 2025. In one viral episode, Nike was accused of a "GPT AI-ism" over a single em dash — [Daily Dot](https://dailydot.com/culture/em-dash-ai/); [Salon](https://www.salon.com/2025/06/11/ai-cant-have-my-em-dash); [McSweeney's](https://www.mcsweeneys.net/articles/the-em-dash-responds-to-the-ai-allegations); [Boston Globe](https://www.bostonglobe.com/2025/05/02/opinion/ai-chatgpt-em-dash-punctuation-literature) **(unverified: snippet)**.
  - HN mentions of "em dash" ran 18–35× above the 2020–2022 baseline in 2025–2026 (measured; see Q1).
  - Wikipedia now treats overused em dashes as a historical indicator valid for 2022–September 2026, which suggests the tell has decayed — [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
- Bias against non-native writers in the wild: in the HN sample, a commenter wrote, "This kind of makes it obvious that I am not a native speaker, but kind of also proves its was not written by an LLM" (2026-10-17). That is anecdotal (measured sample).

### Inferences
- For a style model, "perceived slop" is arguably the right negative target even when a human wrote the text. But the false-positive classes must be filtered out, or the model will learn to avoid legitimate human features: plain non-native English, formal register, em dashes, tidy structure.
- Recommended label hygiene:
  1. Require the callout to name a specific tell (for example "it's not X, it's Y", "delve", grandiose significance, recap paragraphs) or carry a moderator or Wikipedia tag reason.
  2. Drop callouts based only on punctuation.
  3. Optionally cross-check with a strong detector and a manual spot-check.
  4. Down-weight replies from threads where the author disputes the accusation.
- Label precision ranks, from highest to lowest:
  1. Wikipedia AI Cleanup tags: editors follow a written guide; reasons are often explicit; G15 is limited to objective signs.
  2. HN moderator kills: high-precision human/software review, but the text is mostly unretrievable.
  3. Targeted HN or Reddit reply callouts naming a specific tell.
  4. Bare "AI slop" replies.
  5. Platform detectors (Medium, Pangram/Originality prevalence numbers), which are machine, not human, labels.

### Gaps
- No published false-accusation rate for community callouts. Miklian & Katsos establish that accusations don't track AI features, but the fetched abstract gives no precision figure.
- No measured inter-annotator agreement for social-platform callouts, as opposed to curated expert annotation.
- No direct study of callout bias against non-native writers on Reddit or HN; only detector studies (Liang) and anecdotes.

## Q3. What is legally and ToS-feasible to collect in Nov 2026 for private, local, non-commercial use?

### Takeaway
The cleanest options are Wikipedia (CC BY-SA, open API and dumps) and Hacker News (free official Firebase API and Algolia, no auth). Bluesky is technically open, but its AI-use consent signals are advisory. Reddit data is reachable through Arctic Shift dumps, but Reddit's terms require approval for API use since Nov 2025, and Reddit is suing AI scrapers. X requires paid pay-per-use access, and its developer terms explicitly bar using X content to "fine-tune or train" foundation models. That clause arguably covers QLoRA of an open base model even for private use. LinkedIn bars scraping contractually and wins its enforcement cases. Not legal advice; the user should judge contractual risk.

### Cited Findings
- **Hacker News.**
  - Free, unauthenticated Firebase item API and Algolia search, both used successfully here — [HN Firebase API](https://hacker-news.firebaseio.com/v0/item/50395314.json); [HN Algolia](https://hn.algolia.com/api/v1/search?query=%22AI%20slop%22&tags=comment) (measured).
  - BigQuery `bigquery-public-data.hacker_news.full` freshness is unconfirmed. A MotherDuck copy says it is "refreshed daily" from that table and covers 2016–2025; older forum posts report stalls — [MotherDuck docs](https://motherduck.com/docs/getting-started/sample-data-queries/hacker-news/) **(unverified: snippet)**. Hugging Face mirrors exist, e.g. [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) **(unverified)**.
- **Reddit.**
  - Since November 2025, the "Responsible Builder Policy" requires explicit approval before accessing Reddit data through the API. Researchers apply via ticket or r/reddit4researchers, and users report denials — [r/redditdev announcement thread mirror](https://r.datuan.dev/r/redditdev/comments/1oug31u/introducing_the_responsible_builder_policy_new/nocca6t) **(unverified: snippet via mirror)**.
  - Commercial use reportedly needs a separate licence — [third-party README](https://glama.ai/mcp/servers/gavinmcfall/read-it) **(unverified)**.
  - Reddit sued Anthropic (June 2025) and Perplexity, SerpApi, Oxylabs and AWMProxy (Oct 2025) over scraping for AI, while licensing to OpenAI and Google — [Engadget](https://www.engadget.com/social-media/reddit-sues-perplexity-and-three-other-companies-for-allegedly-using-its-content-without-paying-205136436.html?src=rss).
  - Arctic Shift is free and has no stated terms; it asks users to be considerate and points to monthly dumps — [Arctic Shift README](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md).
  - Reddit's Public Content Policy page returned HTTP 403 to fetch, so its exact AI-training language is unverified here — [Reddit Public Content Policy](https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy).
- **X.**
  - In June 2025, X added a clause under "Reverse Engineering and other Restrictions" barring use of the X API or X content to "fine-tune or train a foundation or frontier model" — [TechCrunch](https://techcrunch.com/2025/06/05/x-changes-its-terms-to-bar-training-of-ai-models-using-its-content) **(via snippet; clause text not fetched)**.
  - Pricing per third-party sources: pay-per-use became the default on 2026-02-06 and the free tier closed to new signups; about $0.005 per post read with a 2M–3M monthly read cap (sources disagree); Basic subscribers auto-migrated from 2026-06-01; legacy Pro deprecated around Aug–Sep 2026 — [Open Terms Archive](https://opentermsarchive.org/en/memos/x-replaces-its-dollar200-entry-level-api-plan-with-a-pay-per-use-model/); [Postproxy](https://www.postproxy.dev/blog/x-api-pricing-2026/) **(unverified: snippet; official pricing page not fetched)**.
- **LinkedIn.**
  - In hiQ v. LinkedIn, the court found the User Agreement "unambiguously prohibits scraping", ending in a $500k stipulated judgment on the contract claim. Separately, the Ninth Circuit held that CFAA doesn't bar scraping public profiles — [Wikipedia: hiQ v. LinkedIn](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn); [National Law Review](https://www.natlawreview.com/article/linkedin-s-data-scraping-battle-hiq-labs-ends-proposed-judgment) **(via snippet)**.
  - LinkedIn sued Proxycurl in Jan 2025; Proxycurl shut down on 2025-07-04 — [LinkedIn News](https://news.linkedin.com/2025/LinkedInWinsLegalBattleToProtectMemberData) **(via snippet)**.
- **Bluesky.**
  - The firehose is an open stream of all public events. A 1M-post dataset scraped from it was pulled from Hugging Face after backlash in Nov 2024 — [TechCrunch](https://techcrunch.com/2025/03/15/bluesky-users-debate-plans-around-user-data-and-ai-training/); [ccstartup summary](https://ccstartup.com/blog/2024/11/27/one-million-public-bluesky-posts-scraped-for-ai-training) **(via snippet)**.
  - Proposal 0008 (2025) adds per-user consent settings for generative AI, bulk datasets and similar uses. Bluesky says "Bluesky won't be able to enforce this consent outside of our systems" — [TechCrunch](https://techcrunch.com/2025/03/15/bluesky-users-debate-plans-around-user-data-and-ai-training/) **(via snippet)**.
- **Medium.** Labels are internal, so there is nothing to collect. Medium enforces with detectors plus human review — [Medium help](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy) **(via snippet)**.
- **Wikipedia.** The free MediaWiki API worked, but it rate-limits bursts. This researcher got "You are making too many requests to the API" after about 3 rapid calls, then succeeded with pacing and a descriptive User-Agent (measured) — [MediaWiki API](https://en.wikipedia.org/w/api.php).
- **Academic datasets.** The Liang et al. data is on Hugging Face ([WxWx/ChatGPT-Detector-Bias](https://huggingface.co/datasets/WxWx/ChatGPT-Detector-Bias/blob/main/README.md?code=true)). Russell et al. released their annotated data and code ([ACL 2025](https://aclanthology.org/2025.acl-long.267)) **(license not checked)**.

### Inferences
- Lowest risk for a private local model:
  - Wikipedia revisions, where CC BY-SA attribution and share-alike matter only if outputs are redistributed.
  - HN via the official APIs.
  - Released academic datasets, subject to each license.
  - Pattern catalogs from GitHub, per repo license.
- Moderate risk: Reddit via Arctic Shift dumps. Using third-party dumps sidesteps Reddit's API-approval regime technically, not contractually: Reddit's terms still govern the content. Enforcement has targeted commercial AI firms, not private hobby use. That is an inference, not a legal assurance.
- Avoid:
  - X: the anti-training clause applies regardless of commerciality, plus per-read cost.
  - LinkedIn: contract terms and active litigation.
  - Bulk Bluesky collection where users have set "disallow" consent records. The records are advisory but ethically salient, and the community reacts strongly.
- Practical collection plan: about 7.8k Wikipedia tagged articles with diffs, plus about 1–3k HN targeted callouts per year (2024–2026), plus optional mining of Reddit dumps from r/ChatGPT, r/antiai, r/aiwars, r/freelanceWriters and r/copywriting. Together these could plausibly reach 10k+ labeled negatives. Most would not be in a "memo/explainer" register, so plan to filter them for genre.

### Gaps
- Not fetched or verified: Reddit's exact Public Content Policy and Data API Terms text (403), YC/HN's terms of use on bulk reuse, X's official pricing page and full developer-agreement clause, and Bluesky's current developer guidelines and Jetstream docs.
- No legal analysis of contract or ToS exposure for private, non-commercial fine-tuning was found. The user should judge this; it is not resolvable from public sources.
- Whether the HN BigQuery dataset is current in Nov 2026 is unverified. Checking it requires a `SELECT MAX(timestamp)` query on the table.
