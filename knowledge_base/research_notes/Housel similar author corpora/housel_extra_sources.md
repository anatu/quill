# Morgan Housel's own writing beyond the Collaborative Fund blog: candidate training sources

Research date: 2026-11-08. Baseline: Collab Fund blog crawl (351 posts, Sep 2016 to 2026, about 342k words). Fetching was limited to robots.txt files, terms pages, three fool.com author-page requests, five fool.com articles (word counts and style read), a few Wayback and Common Crawl index lookups, one podcast RSS feed and Hugging Face API searches. Nothing was bulk-downloaded. Generic user agent: "research-client/1.0".

## Overall inventory: what extra Housel text exists and what is usable?

### Takeaway
The only large pool of extra Housel-authored prose is the Motley Fool archive, 2007/08 to Aug 2016: roughly 3,250 articles and an estimated 1.5 to 2.5M words, of which perhaps 0.3M is essay-like. It is still live on fool.com. The Fool's robots.txt blocks ClaudeBot and CCBot and signals `ai-train=no`. Its Terms of Use ban automated harvesting and commercial copying. Every other source is small, spoken, paywalled, or covered by restrictive terms or copyright: WSJ, syndicated reprints, podcasts, X and books.

### Cited Findings
- Housel said in Oct 2014 that he applied to the Fool in October 2007 and that the column was "article number 3,059" — [Fool, "How I Got Started in Finance", 2014-10-31](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)
- His last Fool article is dated Aug 30, 2016 ("Investing Is a Fascinating Business"), the same day Fortune reported his move to Collaborative Fund — [fool.com author page](https://www.fool.com/author/1611/); [Fortune, 2016-08-30](https://fortune.com/2016/08/30/motley-fool-collaborative-fund/)
- In 2025 Housel described his lifetime output as "I wrote 4,000 blog posts" across publications including the Fool — [How I Write (David Perell), 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- He also wrote "the Saturday investing column at the Wall Street Journal" while full-time at the Fool — [Bogleheads on Investing ep. 26 transcript, 2020-09-30](https://boglecenter.net/bogleheads-on-investing-episode-026-transcript/)
- Hugging Face dataset searches returned no Housel, Collab Fund, Motley Fool or Psychology of Money datasets — [HF API search "housel"](https://huggingface.co/api/datasets?search=housel)

### Inferences
Inventory (estimates are mine unless cited below):

| Source | Volume (est.) | Access | Rights / AI opt-out | Register / style distance | Usable for quill? |
|---|---|---|---|---|---|
| Motley Fool articles, 2007/08 to 2016 | ~3,250 articles; ~1.5 to 2.5M words total; ~0.3M words of 2012-2016 essay columns | Live on fool.com; JS-paginated author index; Wayback captures of the author page from 2019 on | Fool owns copyright (likely work for hire); robots.txt blocks ClaudeBot/GPTBot/CCBot; `Content-Signal: ai-train=no`; ToU bans robots/scripts and copying beyond one personal non-commercial copy | Essay columns from 2014 to 2016 are close to the Collab voice; 2010 columns are op-ed with Fool boilerplate; early high-volume pieces are unknown and probably further away | Legally blocked without Fool permission. Highest-value item to request a licence for |
| WSJ Saturday investing column (~2014-2015) | Unknown; likely tens of columns (~50-100k words if weekly for 1-2 years) | Hard paywall; author page returns 401 to automated clients | robots.txt `User-agent: * Disallow: /` with a search-engine allowlist; Dow Jones notice prohibits automated collection | Heavily edited "capital J journalism" (Housel's words) | No |
| Syndicated Fool reprints (Fox Business, Yahoo Finance) | Duplicates of Fool text | Live | Same Fool copyright | Same as the Fool text | No new text; dedupe risk only |
| Podcasts: "The Morgan Housel Podcast" (now "The Psychology of Money with Morgan Housel") | 103 episodes, ~29.8 h, ~270k spoken words at an assumed 150 wpm | RSS audio only; no transcript tags | Housel/Collab copyright; no licence | Spoken. Early episodes appear to be readings of existing essays | Only via ASR; mostly duplicates the written corpus. Low priority |
| Guest interview transcripts (Tim Ferriss, Masters in Business, Knowledge Project, How I Write, Bogleheads, Motley Fool Money, Acquired) | Perhaps 10-20 long transcripts, ~5-15k words each, half of it Housel | Several hosted as text | Owned by each show; terms vary | Spoken, conversational | Poor fit for a written-style adapter |
| X/Twitter @morganhousel | Count unknown; short aphorisms, often essay lines | Logged-in only | X ToS bans crawling or scraping "in any form, for any purpose" without written consent | Aphoristic fragments | No |
| Books (Psychology of Money 2020, Same as Ever 2023, The Art of Spending Money 2025) | ~150-200k words | Commercial | Copyrighted | Close (many chapters grew out of blog posts) | Not usable |

### Gaps
- No exact Fool article count or word count is available without crawling the full author index, which is JS-paginated and blocked to AI crawlers.
- Guest essays in other outlets: I found no reliable evidence of a substantial body (see the dedicated section).

## The Motley Fool (fool.com), 2007/08 to 2016

### Takeaway
The author page is https://www.fool.com/author/1611/. The archive is still live, with full text served as static HTML. My estimate is about 3,250 Housel articles and 1.5 to 2.5M words. The current robots.txt blocks GPTBot, ClaudeBot and CCBot outright and sets `ai-train=no` for all agents. The Terms of Use (last updated 29 Jan 2026) prohibit automated harvesting, scraping and any copying beyond one personal non-commercial copy. The archive is not usable for training without written permission from the Fool.

### Cited Findings
**Author page and availability**
- The author page lives at fool.com/author/1611. JSON-LD on article pages gives his jobTitle as "Contributing Analyst". The current bio reads: "A former economics and finance columnist for Fool.com and analyst for Motley Fool One" — [fool.com author page](https://www.fool.com/author/1611/); [sample article JSON-LD](https://www.fool.com/investing/general/2010/03/03/the-7-words-that-will-save-america.aspx)
- The server-rendered author page always returns the 20 newest articles (Aug 2016 back to Jun 14, 2016), whatever the `?page=` value (tested with 1, 81 and 200). Deeper listing pages load client-side, yet search engines have indexed `?page=` URLs up to at least 81 — [fool.com/author/1611?page=81](https://www.fool.com/author/1611?page=81)
- A Wayback capture from Oct 2019 shows 34 items per listing page with a "Load more" control and page links up to 10. It also lists 2017-2019 bylined items such as "ETFs or Mutual Funds: Which Is the Better Investment" (2019-02-13), "How to Build a Dividend Portfolio" (2018-07-26) and "A Step-by-Step Guide to Asset Allocation in Retirement" (2017-07-11), all after he left — [Wayback 2019-10-18](https://web.archive.org/web/20191018111105/https://www.fool.com/author/1611/)
- Wayback holds author-page captures from 2019-10-18 onward, many in 2020 to 2023 — [Wayback CDX for fool.com/author/1611/](https://web.archive.org/cdx/search/cdx?url=fool.com/author/1611/&fl=timestamp,statuscode&limit=40)
- Old 2010 articles still return HTTP 200 with full text. Their JSON-LD shows `datePublished` 2010 and `dateModified` 2017-04-06, the signature of a site migration — [2010 "The 7 Words That Will Save America"](https://www.fool.com/investing/general/2010/03/03/the-7-words-that-will-save-america.aspx); [2010 "The Biggest Threat From Greece..."](https://www.fool.com/investing/general/2010/05/25/the-biggest-threat-from-greece-that-no-one-talks-a.aspx)

**Article count**
- Primary anchor: "This is article number 3,059." (2014-10-31). The same footer reads "Check back every Tuesday and Friday for Morgan Housel's columns", a two-columns-a-week cadence by late 2014 — [Fool, 2014-10-31](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)
- Fortune (Aug 2016): "the past nine years as an investment columnist with The Motley Fool" — [Fortune](https://fortune.com/2016/08/30/motley-fool-collaborative-fund/). Housel himself later said "ten years" — [Bogleheads transcript](https://boglecenter.net/bogleheads-on-investing-episode-026-transcript/)
- Secondary and conflicting totals: a Knowledge Project episode summary says "about 3,600 articles on finance over nine years" — [Knowledge Project #14 summary](https://podcasts-distilled-hugo-content.pages.dev/the-knowledge-project/14-morgan-housel-reading-writing-and-lifelong-learning/) (official page: [fs.blog](https://fs.blog/knowledge-project-podcast/morgan-housel/)). A What Got You There episode-notes summary says he wrote "three articles per day" early on as a per-article contract writer and later pitched writing "75% less for the same pay". I saw that claim only as a search summary; the transcript page returned 403 to my fetch — [What Got You There #210 notes](https://whatgotyouthere.com/210-morgan-housel-episode-notes/)

**Sample word counts** (body text only; measured from the pages fetched 2026-11-08)
- "The 7 Words That Will Save America" (2010-03-03): 790 words — [link](https://www.fool.com/investing/general/2010/03/03/the-7-words-that-will-save-america.aspx)
- "The Biggest Threat From Greece That No One Talks About" (2010-05-25): 967 words — [link](https://www.fool.com/investing/general/2010/05/25/the-biggest-threat-from-greece-that-no-one-talks-a.aspx)
- "How I Got Started in Finance" (2014-10-31): 1,463 words — [link](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)
- "1945-2016: Here's Basically What Happened" (2016-07-14): 851 words — [link](https://www.fool.com/investing/2016/07/14/1945-2016-heres-basically-what-happened.aspx)
- "Expectations vs. Forecasts" (2016-08-22): 441 words — [link](https://www.fool.com/investing/2016/08/22/expectations-vs-forecasts.aspx)

**robots.txt** (fetched 2026-11-08)
- The current file names GPTBot, ClaudeBot (commented "Anthropic (Model Training)"), CCBot (commented "Common Crawl (AI Training Dataset)"), MauiBot and Bytespider, each with `Disallow: /`. For `User-agent: *` it sets `Content-Signal: ai-train=no, search=yes, ai-input=yes` — [fool.com/robots.txt](https://www.fool.com/robots.txt)
- The file does not name `anthropic-ai` or `Google-Extended`. Both fall under `*`, whose rules disallow only specific paths, but the `ai-train=no` content signal applies to every agent — [fool.com/robots.txt](https://www.fool.com/robots.txt)
- History from Wayback: the 2021-01-01, 2022-01-01 and 2023-01-01 captures name no AI bots. The 2024-01-01 capture adds GPTBot, and 2025-01-01 adds GPTBot and ClaudeBot — [Wayback robots 2023-01-01](https://web.archive.org/web/20230101001222/https://www.fool.com/robots.txt); [2024-01-01](https://web.archive.org/web/20240101000134/https://www.fool.com/robots.txt); [2025-01-01](https://web.archive.org/web/20250101032542/https://www.fool.com/robots.txt). The 2026-01-01 capture returned no matching lines when I fetched it. I did not resolve this anomaly.

**Terms of Use** ("The Motley Fool's Rules", Last Updated January 29, 2026)
- Users may not "Use any automated means, including, without limitation, agents, robots, scripts, or spiders, to access, monitor, copy or harvest data from any part of our sites" — [Fool Terms of Use](https://www.fool.com/legal/terms-and-conditions/fool-rules/)
- "You may make one copy of the Content for your personal, non-commercial use... Any other copying, distribution, storing, or transmission of any kind, or any commercial use of our Content, is prohibited without The Fool's prior written permission" — [Fool Terms of Use](https://www.fool.com/legal/terms-and-conditions/fool-rules/)
- "You further agree not to create abstracts from or scrape our Content" — [Fool Terms of Use](https://www.fool.com/legal/terms-and-conditions/fool-rules/)
- Content, including "our writings", is described as "the property of The Motley Fool and/or providers of the content under license" — [Fool Terms of Use](https://www.fool.com/legal/terms-and-conditions/fool-rules/)

**Content mix (wire versus essay)**
- His 2010 columns won the SABEW Best in Business award in the opinion/column category for large websites, for the second straight year. The Fool praised them for "unbiased analysis in clear, tightly written packages" — [Fool SABEW post](https://www.fool.com/investing/general/2011/03/25/foolcom-wins-sabew-best-in-business-award.aspx)
- The archive includes a recurring "8 Fascinating Reads" link-roundup series, mostly quotations of other writers — [fool.com author listing (search-indexed)](https://www.fool.com/author/1611?page=62)
- He also co-bylined dialogue pieces such as "Our 3 Biggest Investment Mistakes" (2012) with Matt Koppenheffer — [Fool 2012](https://www.fool.com/investing/general/2012/12/20/our-3-biggest-investment-mistakes.aspx)
- 2010 columns carry inline tickers ("Morgan Stanley (NYSE: MS)"), disclosure footers ("Morgan Housel has no position in any stocks mentioned.") and comment calls ("Got a different take? Share it in the comments section below.") — [2010 "7 Words"](https://www.fool.com/investing/general/2010/03/03/the-7-words-that-will-save-america.aspx); [2010 "Greece"](https://www.fool.com/investing/general/2010/05/25/the-biggest-threat-from-greece-that-no-one-talks-a.aspx); [2014 "How I Got Started"](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)

### Inferences
- Count method: 3,059 articles by 2014-10-31 (primary). From Nov 2014 to Aug 30, 2016 is about 95 weeks; at two columns a week plus occasional extras that adds roughly 190 to 250, for a total of about 3,250 to 3,300. That matches the secondary "3,200 or 3,300" figure from a search summary and sits below the "3,600" summary. Housel's "4,000 blog posts" (2025) covers all outlets.
- Word method: five sampled column-type pieces average about 900 words (median 851). Early high-volume pieces were probably shorter (assumed 400 to 600 words). 3,250 articles at 500 to 800 words gives about 1.6 to 2.6M words, roughly 5 to 7 times the Collab corpus. The essay-like subset is smaller. If the twice-weekly column ran from about 2013 to 2016, that is about 350 to 450 columns, or about 0.3 to 0.4M words, comparable in size to the Collab corpus.
- Wire share: I could not sample 2007-2009 pieces. The early "three articles a day" volume (secondary), the "Contributing Analyst" title and Fool norms suggest a large share of short stock- or news-pegged items before about 2011. This is unverified.
- The 2017-2019 bylined items in the 2019 listing are probably evergreen Fool pages later updated by staff under his byline. Exclude anything dated after Aug 2016.
- The archive is "still online", not Wayback-only, but full enumeration requires the JS-paginated index or the Fool sitemaps. Either route would breach the robots and ToU restrictions if done by an AI-training crawler.
- Because Housel was a Fool employee, the Fool, not Housel, very likely owns the copyright. A licence request would go to the Fool, not to Housel.

### Gaps
- Exact article count and the share of wire-style versus essay pieces. Both would need the full listing.
- No 2007-2009 sample was fetched. The style of the earliest pieces is unverified.
- The Wayback robots.txt history between 2025 and the present (when CCBot was added) is incomplete.

## Wall Street Journal columns

### Takeaway
Housel wrote the WSJ's Saturday investing column while still at the Fool. Bios date it to roughly 2014-2015. The column count is unknown, probably tens of pieces. WSJ is hard-paywalled, its robots.txt disallows all agents by default and its notice prohibits automated collection without Dow Jones's written permission. It is also the most heavily edited Housel text. Not usable.

### Cited Findings
- "I was writing the Saturday investing column at the Wall Street Journal", "for several years" while full-time at the Fool. He called the WSJ "capital J journalism" and "very different" from his Fool writing, which was "more or less a blog" — [Bogleheads ep. 26 transcript, 2020](https://boglecenter.net/bogleheads-on-investing-episode-026-transcript/)
- Bios describe the role as "Wall Street Journal Contributor" in 2014-2015 or as a "former columnist" — [BigSpeak bio](https://www.bigspeak.com/speakers/morgan-housel); [Stable Investor interview intro, Jan 2016](https://stableinvestor.com/2016/01/morgan-housel-interview-part-1.html)
- A search summary attributed the quote "I was a columnist for The Wall-Street Journal for seven years" to an interview. I could not verify it; the Ritholtz transcript returned 403 to me. It conflicts with the 2014-2015 bios and with Fortune's "has also written for publications such as The Wall Street Journal" — [Ritholtz transcript (403)](https://ritholtz.com/2020/09/transcript-morgan-housel/); [Fortune](https://fortune.com/2016/08/30/motley-fool-collaborative-fund/)
- A search summary of another interview says his WSJ brief was to write "an investing column every week" for readers with no financial background, and that the WSJ "was very by the book" — [Perell podcast page](https://perell.com/podcast/morgan-housel-writing-for-the-internet/) (attribution from search summary, not fetched)
- The WSJ author page returns HTTP 401 to automated clients — [wsj.com/news/author/morgan-housel](https://www.wsj.com/news/author/morgan-housel)
- WSJ robots.txt sets `User-agent: * Disallow: /` and allowlists named search and ad crawlers plus ChatGPT-User, GPTBot and OAI-SearchBot. It does not name ClaudeBot, anthropic-ai, CCBot or Google-Extended, which therefore fall under the global Disallow. Its header reads: "Collection of content and other data on https://www.wsj.com/ through automated means is prohibited unless you have express written permission from Dow Jones & Company" — [wsj.com/robots.txt](https://www.wsj.com/robots.txt); terms referenced at [dowjones.com/terms-of-use](https://www.dowjones.com/terms-of-use/)

### Inferences
- A weekly column over about 1 to 2 years would be about 50 to 100 pieces and 50 to 100k words. That is an estimate with no direct count.
- The GPTBot entries on WSJ's allowlist are consistent with a publisher licensing deal with OpenAI. No such allowance exists for Anthropic or for open datasets.
- WSJ copy is desk-edited, so it is the furthest Housel text from his self-edited blog voice.

### Gaps
- Exact dates, column name and count. The WSJ archive is behind a paywall and blocks automated access, and the Wayback CDX had no captures of the author page URL I tried.
- The "seven years" claim remains unverified and likely mis-transcribed.

## USA Today and other syndication of Fool articles

### Takeaway
Fool columns by Housel were syndicated to Fox Business and Yahoo Finance (UK). I found no USA Today copies. Syndicated copies add no new text and carry the same Fool copyright. Their only effect is duplication, so dedupe against them if they ever enter the corpus.

### Cited Findings
- Fox Business reprints of Fool columns include "Investing Is a Fascinating Business" (his final Fool piece), "It's So Much Harder Than You Think" and "Smart-Sounding Temptations To Sell As the Market Rose" — [Fox Business 1](https://www.foxbusiness.com/markets/investing-is-a-fascinating-business); [Fox Business 2](https://www.foxbusiness.com/markets/its-so-much-harder-than-you-think); [Fox Business 3](https://www.foxbusiness.com/markets/smart-sounding-temptations-to-sell-as-the-market-rose)
- Yahoo Finance UK carried "This Time It's Different: Part 3 of Our Series on U.S. Downturns" — [Yahoo Finance UK](https://uk.finance.yahoo.com/news/time-apos-different-part-3-175500451.html)
- Housel found the Fool through a friend's Fool articles on Yahoo! Finance, which shows that Yahoo syndication of Fool content was standard — [Fool 2014](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)
- Fox Business robots.txt names none of GPTBot, ClaudeBot, anthropic-ai, CCBot or Google-Extended — [foxbusiness.com/robots.txt](https://www.foxbusiness.com/robots.txt)
- A targeted search found no USA Today pages carrying Housel's Fool articles — [search, 2026-11-08; no URL]

### Inferences
- Fox Business's permissive robots.txt does not change the underlying copyright, which stays with the Fool. A permissive mirror does not override the rights holder's opt-out.

### Gaps
- USA Today syndication is unconfirmed: none found, but its absence is not proven.
- The volume of syndicated copies is unknown.

## Guest essays on other sites and newsletters

### Takeaway
I found no evidence of a meaningful body of Housel guest essays outside the Fool, the WSJ and Collab Fund. His written output appears concentrated in those three outlets plus the books.

### Cited Findings
- Fortune (2016) lists only "publications such as The Wall Street Journal" besides the Fool — [Fortune](https://fortune.com/2016/08/30/motley-fool-collaborative-fund/)
- His personal site links only to the Collab Fund blog, Markel, his podcast, a YouTube channel (@Morgan-Housel) and X (@morganhousel). It links no other publications — [morganhousel.com](https://www.morganhousel.com/)
- A SlideShare deck, "What Makes Us Bad Investors", sits under a morganhousel account — [SlideShare](https://de.slideshare.net/morganhousel/what-makes-us-bad-investors)

### Inferences
- Any guest essays would be few, and probably repurposed Collab Fund or book material.

### Gaps
- I ran no exhaustive search of newsletters or outlets such as Medium reposts or forewords. Searches surfaced only fan summaries.

## Talk and podcast transcripts (spoken register)

### Takeaway
There is a sizeable amount of spoken Housel, all of it **spoken register**: his own podcast plus many long-form interviews, some with published transcripts. His podcast has 103 episodes (about 30 hours) with no transcripts in the feed, and its early episodes look like readings of existing essays. Spoken material is a poor fit for a written-style adapter and is owned by each show.

### Cited Findings
- "The Morgan Housel Podcast" (Apple id1675310669) now carries the feed title "The Psychology of Money with Morgan Housel". It has 103 episodes from Mar 2, 2023 ("The Art of Spending Money", described as "The first episode") to Nov 6, 2026. Median episode length is about 15.5 minutes, about 29.8 hours in total, and the RSS has no `podcast:transcript` tags. Early titles ("The Highest Form of Wealth", "Getting Rich vs. Staying Rich", "Rules of the Money Game") match his essay titles. Recent episodes add Q&A segments ("Plus: ...") and a State Street sponsor read — [podcast RSS](https://anchor.fm/s/104219ecc/podcast/rss); [Apple Podcasts](https://podcasts.apple.com/us/podcast/the-morgan-housel-podcast/id1675310669)
- A May 2026 episode announced a new format in which Housel answers listener questions (search summary) — [metacast listing](https://metacast.app/podcast/the-morgan-housel-podcast/OSibF03C)
- Full or near-full transcripts are hosted for:
  - Tim Ferriss Show (2022) — [tim.blog](https://tim.blog/2022/03/05/morgan-housel-the-psychology-of-money-transcript/)
  - How I Write (Oct 2025) — [Substack](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
  - Bogleheads on Investing ep. 26 (2020) — [boglecenter.net](https://boglecenter.net/bogleheads-on-investing-episode-026-transcript/)
  - Masters in Business (2020; 403 to my fetch) — [ritholtz.com](https://ritholtz.com/2020/09/transcript-morgan-housel/)
  - What Got You There #210 (403 to my fetch) — [whatgotyouthere.com](https://whatgotyouthere.com/210-morgan-housel-episode-transcript/)
- Other spoken appearances:
  - Knowledge Project #14 (2016) — [fs.blog](https://fs.blog/knowledge-project-podcast/morgan-housel/)
  - Acquired ACQ2 — [acquired.fm](https://www.acquired.fm/acq2-episodes/morgan-housel)
  - Perell, "Writing for the Internet" — [perell.com](https://perell.com/podcast/morgan-housel-writing-for-the-internet/)
  - Motley Fool Money (2024), with a Fool article adapting it — [fool.com podcast](https://www.fool.com/podcasts/motley-fool-money/2024-07-28-morgan-housel-on-market-history-and); [fool.com article](https://www.fool.com/investing/2024/08/07/morgan-housel-on-market-history-and-wild-minds)
  - Motley Fool Answers, "A History of Market Crashes" — [libsyn](https://motleyfoolanswers.libsyn.com/a-history-of-market-crashes-pt-4-the-great-recession)

### Inferences
- About 29.8 hours at an assumed 150 words a minute is about 270k spoken words. ASR would be required, and much of it duplicates written essays.
- In interview transcripts roughly half the words are the host's. Usable Housel speech is perhaps 50 to 150k words across 10 to 20 interviews, in a conversational register that would pull the adapter away from the written voice.
- Fool-hosted transcripts fall under the same Fool robots and ToU restrictions.

### Gaps
- The exact number of interviews with published transcripts was not enumerated.
- The terms of each host site were not checked.

## Twitter/X threads

### Takeaway
Housel posts as @morganhousel. X's terms prohibit crawling or scraping "in any form, for any purpose" without prior written consent, and the content is short aphorisms, often lines lifted from his essays. Not usable and of low marginal value.

### Cited Findings
- His site links twitter.com/morganhousel — [morganhousel.com](https://www.morganhousel.com/)
- X's terms (Sept 2023 update) state: "crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited" — [TechCrunch, 2023-09-08](https://techcrunch.com/2023/09/08/x-updates-its-terms-to-ban-crawling-and-scraping); [ConductAtlas provision record](https://conductatlas.com/platform/x/x-terms-of-service/acceptable-use-and-scraping-prohibition/)
- Secondary summaries report that X's developer rules bar using X content to train foundation or frontier models. This is unverified against the primary text; x.com/en/tos returned HTTP 402 to my fetch — [ConductAtlas](https://conductatlas.com/platform/x/x-terms-of-service/acceptable-use-and-scraping-prohibition/)
- Housel: "I always felt like social media was spring training" — [How I Write, 2025](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)

### Inferences
- Tweets act as idea tests that later became essays, so they mostly duplicate the Collab corpus in fragment form.

### Gaps
- Tweet count and thread volume are unknown. X requires login, and I made no attempt.

## Book excerpts published online

### Takeaway
*The Psychology of Money* (2020), *Same as Ever* (2023) and *The Art of Spending Money* (2025) are copyrighted commercial works. Any online excerpts are publisher- or outlet-licensed. Not usable.

### Cited Findings
- The books are listed by his publishers — [Harriman House author page](https://harriman-house.com/authors/morgan-housel/47222); [Penguin Random House author page](https://www.penguinrandomhouse.com/authors/2244345/morgan-housel/)
- The Art of Spending Money exists, sold in a box set with The Psychology of Money in Spanish translation — [Planeta de Libros](https://www.planetadelibros.com/libro-estuche-morgan-housel-la-psicologia-del-dinero-y-el-arte-de-gastar-dinero/426107). An October 2025 release date appeared in a search summary that did not identify its source.
- The 2016 Fool piece "1945-2016: Here's Basically What Happened" is a compressed US economic history in his later book style — [Fool 2016](https://www.fool.com/investing/2016/07/14/1945-2016-heres-basically-what-happened.aspx)

### Inferences
- Many book chapters grew out of blog posts, so the Collab corpus already covers much of the books' style. Book text adds little and is legally off-limits.
- The 1945-2016 piece appears to be a precursor of the Psychology of Money postscript on how the US consumer came to think the way it does. This rests on my recollection, not verified.

### Gaps
- No inventory of online excerpts was made, since they are unusable regardless.

## Housel text in public datasets (Hugging Face, Common Crawl, FineWeb)

### Takeaway
No Hugging Face dataset is named for Housel, the Fool or Collab Fund. Common Crawl does hold Collab Fund blog pages (at least 500 captures in CC-MAIN-2023-50). It holds plenty of pre-2020 fool.com pages but none in CC-MAIN-2023-50, and the specific Housel Fool URLs I tested were absent. FineWeb-style CC derivatives therefore likely contain Collab Fund posts and possibly some Fool pages. A third-party copy does not override the Fool's current AI opt-out or its ToU.

### Cited Findings
- HF dataset search for "housel", "morgan housel", "psychology of money", "psychology-of-money", "motley fool", "fool.com", "motley" and "collabfund" returned no relevant datasets. "housel" matched only HouseLayout3D and houselayout; "motley" matched only an unrelated "Motley-Four-Characters" — [HF API "housel"](https://huggingface.co/api/datasets?search=housel); [HF API "motley"](https://huggingface.co/api/datasets?search=motley)
- The Common Crawl index lists 129 crawls, from CC-MAIN-2008-2009 to CC-MAIN-2026-43 — [CC collinfo](https://index.commoncrawl.org/collinfo.json)
- collabfund.com/blog/* returned 500 captures (the query cap) in CC-MAIN-2023-50 and 184 in CC-MAIN-2025-30 — [CC-MAIN-2023-50 index query](https://index.commoncrawl.org/CC-MAIN-2023-50-index?url=collabfund.com/blog/*&output=json)
- Common Crawl captures of fool.com:
  - www.fool.com/investing/* returned 200 or more (query cap) in CC-MAIN-2016-40 and CC-MAIN-2019-35, and 0 in CC-MAIN-2023-50.
  - www.fool.com/investing/general/2010/* returned 1,000 or more (cap) in CC-MAIN-2013-20.
  - Tested Housel URLs absent: "Expectations vs. Forecasts" (2016-40), "1945-2016" (2019-35 and 2023-50) and "The 7 Words..." (2013-20).
  - Source: [CC index API](https://index.commoncrawl.org/CC-MAIN-2016-40-index?url=www.fool.com/investing/*&output=json)
- collabfund.com/robots.txt returned 404 (no robots file) on 2026-11-08 — [collabfund.com/robots.txt](https://collabfund.com/robots.txt)

### Inferences
- FineWeb and similar sets built from 2013-2024 CC snapshots likely include some Collab Fund posts and some pre-2020 fool.com pages, possibly including Housel articles. Only a handful of URLs were tested. Even if present, the Fool's current robots.txt (ClaudeBot and CCBot blocked, `ai-train=no`) and ToU still apply. A third-party copy is a fact about availability, not a licence.
- Zero fool.com captures in CC-MAIN-2023-50 suggests the Fool was blocking or rejecting CCBot by late 2023, although the Jan 2024 Wayback robots.txt named only GPTBot. The block may have come from server-side or CDN rules.

### Gaps
- FineWeb itself has no public URL lookup for a dataset that large, so I did not test whether specific Housel URLs are inside it.
- I tested only a few Housel URLs against Common Crawl.

## Style distance: Fool writing (2008-2016) versus Collab Fund essays (2016+)

### Takeaway
The voice converges over time. By 2014-2016 the Fool columns are essentially the Collab Fund voice: short declarative openings, conceptual distinctions, compressed history, first-person narrative. Housel himself groups Fool and Collab writing as "blog" style and singles out the WSJ as different. 2010 columns are more op-ed and news-pegged, with Fool furniture to strip: tickers, disclosures, comment calls and pun subheads. The earliest (2007-2009) high-volume pieces were not sampled and are likely furthest away.

### Cited Findings
- Housel calls his Fool work "more or less a blog" and his Collab Fund work "much more to the blog style of writing", with more room for personal opinion. He calls the WSJ "capital J journalism" — [Bogleheads transcript, 2020](https://boglecenter.net/bogleheads-on-investing-episode-026-transcript/)
- 2010 op-ed column, hook and setup: "'We expect you to repay your debts.' Those seven words could save America. Let me tell you why." (18 words). The column then uses subheads ("Heads, I win ...") and inline tickers ("Morgan Stanley (NYSE: MS)") — [Fool 2010-03-03](https://www.fool.com/investing/general/2010/03/03/the-7-words-that-will-save-america.aspx)
- 2010 macro column, an early form of his signature analogy: "Our immune system against economic ills is exhausted. And when a patient's immune system is exhausted, even a mild cold can be vicious." (23 words). The same piece uses a pun subhead ("Greece lightning") and ends "Got a different take? Share it in the comments section below." — [Fool 2010-05-25](https://www.fool.com/investing/general/2010/05/25/the-biggest-threat-from-greece-that-no-one-talks-a.aspx)
- 2014 personal narrative: "I had never once thought about writing, and figured it was a waste of time to apply. But I did, in October 2007." (23 words) — [Fool 2014-10-31](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)
- 2016 column in the Collab voice: "I expect there to be one or two recessions in the next decade. I have no idea when either will arrive. Those aren't contradictory statements. One is an expectation, the other is the rejection of a forecast." (37 words). It ends with a "For more:" link list — [Fool 2016-08-22](https://www.fool.com/investing/2016/08/22/expectations-vs-forecasts.aspx)
- 2016 history compression: "History is infinitely complicated. Too much stuff has happened for anyone to chronicle, so historians are forced to pick and choose." (21 words) — [Fool 2016-07-14](https://www.fool.com/investing/2016/07/14/1945-2016-heres-basically-what-happened.aspx)
- Secondary: he reportedly shifted from "the volume game" to fewer, more thoughtful pieces after pitching to write less for the same pay — [What Got You There #210 notes (via search summary)](https://whatgotyouthere.com/210-morgan-housel-episode-notes/)
- I found no published reviews that compare his Fool and Collab styles.

### Inferences
- Qualitative read of five pieces:
  - The 2014-2016 Fool essays are near-indistinguishable in voice from Collab posts: same sentence rhythm, the "X isn't Y; it's Z" distinctions, historical vignettes and first-person asides. They are the best augmentation candidates if the Fool grants a licence.
  - The 2010 columns share his clarity and analogies but are more argumentative-op-ed, tied to news (Greece, non-recourse mortgages), and wrapped in Fool conventions.
  - The 2007-2009 volume pieces are untested and probably the furthest from the target.
- If the archive were ever licensed, preprocessing should:
  - drop items dated after Aug 2016 and co-bylined pieces;
  - drop "8 Fascinating Reads" roundups, which are mostly other authors' text;
  - strip tickers, disclosure footers, "Check back every Tuesday and Friday" lines, comment calls and "For more:" lists;
  - dedupe against Fox Business and Yahoo copies and against any 2016 pieces re-run at Collab Fund;
  - optionally weight or tag by era (pre-2012 versus 2012-2016) to limit drift toward the older op-ed register.

### Gaps
- No 2007-2009 sample was read.
- No stylometric comparison was run; this is a qualitative read of five pieces.
- No independent reviewer commentary on his style evolution was found.

## Who edited what (editorial dilution)

### Takeaway
By his own account almost none of Housel's writing has been edited by others ("I bet 1% of what I've written has been edited by somebody else"). The WSJ column is the clear exception ("very by the book"). Fool and Collab Fund text is therefore largely his own voice. Fool house conventions (tickers, disclosures, headlines and possibly dek lines) are publisher overlays that can be stripped.

### Cited Findings
- "There's only been a couple of times in my career where I've worked with an editor." "I bet 1% of what I've written has been edited by somebody else." — [How I Write, 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- WSJ: "capital J journalism" — [Bogleheads transcript](https://boglecenter.net/bogleheads-on-investing-episode-026-transcript/); "very by the book" (search summary attributed to an interview) — [Perell podcast page](https://perell.com/podcast/morgan-housel-writing-for-the-internet/)
- Fool pages carry publisher-added furniture: standardized disclosures ("The Motley Fool recommends Bank of America. The Motley Fool owns shares of Bank of America."), ticker formatting and "Summarize with AI" page elements — [Fool 2014](https://www.fool.com/investing/general/2014/10/31/how-i-got-started-in-finance.aspx)
- Fool items bylined to him after he left (2017-2019) appear on his author page — [Wayback 2019](https://web.archive.org/web/20191018111105/https://www.fool.com/author/1611/)

### Inferences
- Editorial dilution by source, from least to most:
  - Collab Fund: self-published, roughly unedited.
  - Fool essay columns, 2010-2016: lightly edited, with house formatting.
  - Fool post-2016 updates: edited by others under his byline. Exclude.
  - WSJ: desk-edited. Exclude.
  - Books: professionally edited, and unusable anyway.

### Gaps
- Fool editorial practice for his columns (copy desk, headline writing) is undocumented in what I found. The headlines and dek lines may be the Fool's, not his.
