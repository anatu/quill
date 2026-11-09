# Nonfiction author style corpora: science, economics, finance, business, history and explanatory-essay writers

Scope: contemporary English-language nonfiction writers outside tech/software/startups whose freely readable online writing could serve as a single-author style corpus for fine-tuning a small LLM. Data checked 2026-11-07.

**How the numbers were produced (read this first).** Every word count below comes from one of five methods. The method is named in each entry. Nothing is a remembered figure.
- **[SUB] Substack archive API.** I paged through `https://<pub>/api/v1/archive?sort=new&limit=25&cursor=...` for every post and summed Substack's own per-post `wordcount` field, split by `audience` ("everyone" means fully free; "only_paid" means paywalled). These are exact post counts and Substack-computed word counts, not estimates. Example endpoint: [ACX archive API](https://www.astralcodexten.com/api/v1/archive?sort=new&limit=25).
- **[WP] WordPress REST API.** I read the post total from the `X-WP-Total` header of `/wp-json/wp/v2/posts`. I then took 50-post pages spread across the archive (newest, 25%, 50%, 75%, oldest), stripped the HTML, and counted words. Estimate = total posts × sampled mean. I also measured the share of words inside `<blockquote>`, which is quoted material and not the author's voice. Example: [acoup posts API](https://acoup.blog/wp-json/wp/v2/posts?per_page=1).
- **[BLG] Blogger feed API.** The post total comes from `openSearch$totalResults` in `/feeds/posts/default?alt=json`. I sampled about 250 posts across the archive and counted words the same way.
- **[PG] Page sampling.** For static sites I counted the posts listed on the archive page. I then counted the words in `<p>` and `<li>` elements on 8 to 14 randomly chosen posts. Menu and footer text can inflate these counts slightly.
- **[SITE] Published by the site itself.** Ribbonfarm and Gwern publish their own word statistics.

"Distance from LLM voice" is my own judgment, based on reading samples and on the style metrics I measured (table under Key Question 3). It is labeled as an inference.

---

## Which candidates have at least ~100k (ideally 200k+) words of freely accessible, single-author, informational prose with narrative flair?

### Takeaway
At least 25 candidates clear 200k free words, and many clear 1M. The largest clean single-author pools are:
- Scott Alexander: SSC about 2.7M plus ACX free essays about 1.8M
- Noah Smith: 3.0M free on Substack plus about 1.2M on the old blog
- Robin Hanson: 3.2M, but it needs byline filtering
- Bryan Caplan: 2.8M
- Venkatesh Rao: Ribbonfarm 1.54M (audited by the site) plus Contraptions 0.9M
- Bret Devereaux: about 2.1M
- Freddie deBoer: 2.1M, but political
- Aswath Damodaran: about 1.56M
- Ted Gioia: 1.1M free
- Howard Marks: about 0.9M of memos
- Brian Potter: 0.8M free

Mid-size corpora (200k to 700k) include Housel, Mastroianni, Dynomight, Constantin, Crawford, Urban, Newport, Slime Mold Time Mold, Dan Davies (254k) and Hannah Ritchie (217k). Below 200k free: Munroe's What If (about 155k), Henrik Karlsson (158k), Kyla Scanlon (163k free; mostly paywalled), Nadia Asparouhova (about 120k), and Bits about Money (about 210k, borderline). Matt Levine is the one big voice whose corpus is not freely accessible on the web; Tyler Cowen and Derek Lowe could not be measured.

### Cited Findings

#### Catalog (alphabetical within tiers; "free" = readable without paying)

**TIER A: large (>500k free words), single author, informational with narrative**

**Scott Alexander: Slate Star Codex (2013–2021) and Astral Codex Ten (2021–present)**
- URLs: https://slatestarcodex.com (frozen archive), https://www.astralcodexten.com (Substack).
- SSC [WP]: 1,241 posts, 2013-02-12 to 2021-01-21. A 241-post sample averaged 2,161 words (median 1,496), so about **2.68M words**, with 11% inside blockquotes. — [SSC WP API](https://slatestarcodex.com/wp-json/wp/v2/posts?per_page=1). A GitHub project independently describes the archive as "2.5 million words from SlateStarCodex". — [vlad-ds/scott-scraper](https://github.com/vlad-ds/scott-scraper)
- ACX [SUB]: 1,505 posts, 2020-08-30 to 2026-11-06. Free: 1,220 posts, 3,466,786 words. Paid: 285 posts, 151,933 words. — [ACX archive API](https://www.astralcodexten.com/api/v1/archive?sort=new&limit=25)
- ACX after removing non-Scott or low-value content [SUB, title-based filter]:
  - Removed:
    - "Your Book Review" guest entries: 78 posts, 581,562 words
    - "Highlights From The Comments" (mostly reader quotes): 76 posts, 463,350 words
    - Open Threads: 306 posts, 89,683 words
    - Links: 46 posts, 154,588 words
    - Contests, meetups, grants and Mantic/Model City Monday: 125 posts, 380,705 words
  - Left: **589 essays, 1,796,898 words**, mean 3,051. (Mantic Monday and Model City are Scott's own writing and could be added back.) — [ACX archive API](https://www.astralcodexten.com/api/v1/archive?sort=new&limit=25)
- Combined single-author estimate: about **4.5M words**.
- Free vs paid: about 96% of ACX words are free.
- License: none stated on either site (no license text found on the homepages). robots.txt does not block AI crawlers on ACX. — [ACX robots.txt](https://www.astralcodexten.com/robots.txt)
- Style markers, measured on 30 SSC posts:
  - mean sentence 20.5 words
  - 7.2% of sentences are questions
  - "you" 12.6 per 1k words; "I" 11.7 per 1k
  - short paragraphs (mean 64 words)
  - from reading: numbered Roman-numeral sections (I., II., III.), steelman-then-rebut structure, deadpan humor, invented dialogues and parables, heavy hedged probability talk
- Consistency: one voice over 13 years. ACX has no magazine editing. Guest book reviews are the main contamination, and they are easy to filter by title.
- Datasets:
  - HF `abhayesian/acx_posts_only`: 1,105 rows, about 20.5MB, fields text/author/title/source, created 2026-04-03, no license declared. — [HF API](https://huggingface.co/api/datasets/abhayesian/acx_posts_only)
  - HF `trentmkelly/LessWrong-43k` (CC0 per card) probably includes his older LessWrong posts. — [HF API](https://huggingface.co/api/datasets/trentmkelly/LessWrong-43k)
  - GitHub `evmn/Slate-Star-Codex` builds ebooks and does not host the text; its README says "over 1500 blogs in the archives". — [repo](https://github.com/evmn/Slate-Star-Codex)

**Bret Devereaux: A Collection of Unmitigated Pedantry (ACOUP)**
- URL: https://acoup.blog
- [WP]: 400 posts, 2019-05-03 to 2026-11-06. A 250-post sample (62% of the archive) averaged 5,291 words (median 5,488), so about **2.1M words**. Only 2% is inside blockquotes. — [acoup WP API](https://acoup.blog/wp-json/wp/v2/posts?per_page=1)
- Free: yes; Patreon supports the blog but posts are not paywalled. — [About page](https://acoup.blog/about-the-pedant/)
- License: none. The About page has no copyright, license, reuse or AI statement. — [About page](https://acoup.blog/about-the-pedant/)
- Style markers [measured on 30 posts]:
  - long sentences: mean 35 words, median 32 (the longest of anyone measured)
  - 6.7 footnote markers per post
  - 12.5 parentheses per 1k words
  - long paragraphs (mean 114 words)
  - from reading: multi-part series ("Part I/II/III"), pop-culture hooks (Game of Thrones, Lord of the Rings, Paradox games) used to teach real history, a dry academic-but-chatty register, explicit "the answer is complicated" framing
- Consistency: very high. One author, unedited, weekly since 2019.
- Topic lock-in: ancient and military history with pop-culture framing. — [About page](https://acoup.blog/about-the-pedant/)
- Datasets: none found on HF (searched "acoup", "devereaux", "pedantry") or GitHub. — [HF search](https://huggingface.co/api/datasets?search=acoup)

**Noah Smith: Noahpinion**
- URLs: https://www.noahpinion.blog (Substack, 2020–present), https://noahpinionblog.blogspot.com (2010–2020)
- Substack [SUB]: 1,379 posts, 2020-11-24 to 2026-11-07. Free: 1,139 posts, **3,015,765 words**. Paid: 240 posts, 666,636 words. 80 free posts with roundup, interview or guest titles total 286,656 words. — [Noahpinion archive API](https://www.noahpinion.blog/api/v1/archive?sort=new&limit=25)
- Old Blogspot [BLG]: 934 posts. A 150-post sample averaged 1,283 words, so about **1.2M words**, with 16% inside blockquotes. Some sampled posts list the author as "Unknown" or "Anonymous". — [Blogger feed](https://noahpinionblog.blogspot.com/feeds/posts/summary?alt=json&max-results=1)
- License: none stated.
- Style markers [measured on 20 posts]:
  - mean sentence 21.2 words
  - low second person (3.9 per 1k)
  - em-dashes 10 per 1k
  - from reading: many embedded charts, tweets and screenshots; informal asides; numbered "reasons" lists; strong opinions on policy and geopolitics
- Political bleed: high (US politics, China, industrial policy).

**Ted Gioia: The Honest Broker**
- URL: https://www.honest-broker.com
- [SUB]: 1,366 posts. 438 of them are dated 2000-01-01; these are imported book essays, 433 of them paid. Free: 614 posts, **1,103,026 words**. Paid: 752 posts, 1,071,433 words. Active posting runs 2021 to 2026. — [Honest Broker archive API](https://www.honest-broker.com/api/v1/archive?sort=new&limit=25)
- **robots.txt blocks** GPTBot, CCBot, ClaudeBot, anthropic-ai, Google-Extended, Bytespider and Applebot-Extended. Substack's AI opt-out appears to be switched on, which signals the author objects to AI training. — [robots.txt](https://www.honest-broker.com/robots.txt)
- Style markers [measured on 20 posts]:
  - short sentences (mean 16.2)
  - em-dashes 11.8 per 1k
  - short paragraphs (36 words)
  - from reading: numbered lists, personal anecdotes from a music career, contrarian cultural framing
- Topic: music history, culture, and the tech/media business (overlaps tech critique).

**Venkatesh Rao: Ribbonfarm (2007–2024, now a static archive) and Contraptions**
- URLs: https://ribbonfarm.com, https://contraptions.venkateshrao.com
- [SITE]: the site's own statistics page lists 1,117 posts and 2,117,465 words. **Venkat: 875 posts, 1,539,789 words, average 1,760 per post.** Next contributors: Sarah Perry (49 posts) and Jacob Falkovich (28). — [Ribbonfarm stats](https://ribbonfarm.com/stats/)
- Ribbonfarm retired in November 2024 after 17 years and was relaunched as a permanent static archive in April 2026. — [Ribbonfarm history](https://ribbonfarm.com/history/)
- License: All rights reserved, but with an **explicit AI-training grant**: "Limited non-exclusive permission is granted to AI and machine learning systems to crawl, index, and use this site's content for training language models … The only condition is that the source domain (ribbonfarm.com) be acknowledged in any public disclosure of training data provenance or lineage." — [Ribbonfarm copyright](https://ribbonfarm.com/copyright/). A machine-readable TDMRep file sets `"tdm-reservation": 0`. — [tdmrep.json](https://ribbonfarm.com/.well-known/tdmrep.json)
- Scope note: much of the content is management and organizational theory, with some tech and the "Gervais Principle". It overlaps the tech-writer track.

**Aswath Damodaran: Musings on Markets (finance and valuation)**
- URL: https://aswathdamodaran.blogspot.com
- [BLG]: 686 posts. A 247-post sample averaged 2,271 words (median 2,263), so about **1.56M words**. Every sampled post was by "Aswath Damodaran" and blockquotes were about 0%. Dates run 2008-09-17 to 2026-11-03. — [Blogger feed](https://aswathdamodaran.blogspot.com/feeds/posts/summary?alt=json&max-results=1)
- License: none found on the homepage.
- Style markers:
  - teacherly and instructive; second person 11.4 per 1k
  - from reading: data tables, "story and numbers" framing, explicit step-by-step valuation walk-throughs
  - the measured sentence length (40 words) is probably inflated because his Blogger posts use `<br>` breaks rather than `<p>` tags
- Political bleed: low. Transferability: excellent for analytic memos.

**Howard Marks: Oaktree memos (finance and investing)**
- URL: https://www.oaktreecapital.com/insights/memos
- [PG]: the memo index lists **166 dated memos, 1990 to 2026**. An 8-memo sample averaged about 5,800 words per page (some navigation text included), so roughly **0.85–0.95M words**. — [Oaktree memos](https://www.oaktreecapital.com/insights/memos)
- License: "© 2007- Oaktree Capital Management, L.P. All rights reserved." — [Oaktree memos](https://www.oaktreecapital.com/insights/memos)
- Free: yes. Form: literal memos to clients, the closest match to a "memo voice".
- Consistency: a single voice across 36 years, though they are corporate documents and some memos are co-signed.

**Brian Potter: Construction Physics**
- URL: https://www.construction-physics.com
- [SUB]: 365 posts, 2020-09-27 to 2026-11-07. Free: 252 posts, **803,653 words** (9 reading lists and interviews among them, 30,701 words). Paid: 113 posts, 296,065 words. — [Construction Physics archive API](https://www.construction-physics.com/api/v1/archive?sort=new&limit=25)
- Style markers [measured on 20 posts]:
  - long, plain, expository sentences (mean 28.4)
  - very little "I" (2.3 per 1k), "you" (3.4 per 1k) or questions (1.2%)
  - from reading: chart-dense, history of technology and industry, cost-curve analysis
- Distance from LLM voice: lowish. It is clean and neutral, close to a good analyst report.
- Political bleed: low (housing and energy policy at most).

**Gwern Branwen: gwern.net (statistics, psychology, history of science, plus AI)**
- URL: https://gwern.net
- [SITE]: "As of 2022-11-08, the source of Gwern.net is composed of >443 text files with >4.38m words or >31MB; this includes my writings & documents I have transcribed into Markdown." The own-writing share is lower. — [Gwern About](https://gwern.net/about)
- License: **CC0**. "This site is licensed under the Creative Commons public domain (CC-0) license." — [Gwern About](https://gwern.net/about)
- Datasets: HF `yoonholee/style-eval-pg-karpathy-gwern` (license cc0-1.0) is a style-eval set covering Paul Graham, Karpathy and Gwern. — [HF API](https://huggingface.co/api/datasets/yoonholee/style-eval-pg-karpathy-gwern)
- Style:
  - extremely dense; many links, margin notes and sidenotes; very long annotated essays
  - frequent AI and ML topics (partly overlaps tech)
  - the RSS-feed metrics (Substack link newsletters) were not representative and are omitted

**Terence Tao: What's new (mathematics)**
- URL: https://terrytao.wordpress.com
- [WP]: 1,175 posts, 2007-02-22 to 2026-11-06. Mean 1,875 words (median 1,012), so about **2.2M words**; LaTeX rendered as images is not counted. — [WordPress.com API](https://public-api.wordpress.com/wp/v2/sites/terrytao.wordpress.com/posts?per_page=1)
- Style markers [measured on 30 posts]:
  - second person 0.2 per 1k
  - 22.4 parentheses per 1k
  - 0.4% questions
  - formal theorem-proof exposition
- **Poor fit**: it is research mathematics.

**John D. Cook: blog (applied math, statistics, computing)**
- URL: https://www.johndcook.com/blog
- [WP]: 5,568 posts, 2008-01 to 2026-11. Mean 351 words, so about **1.95M words**. Many posts contain code and math. — [WP API](https://www.johndcook.com/blog/wp-json/wp/v2/posts?per_page=1)
- License: "John D. Cook © All rights reserved." — [blog](https://www.johndcook.com/blog/)
- Style markers:
  - short sentences (17.7), short posts, 14.6 "you" per 1k
  - from reading: crisp "here's a neat fact" notes
- Fit: weak-to-moderate. Too short and technical for memo voice, though clean.

**Sean Carroll: Preposterous Universe blog (physics)**
- URL: https://www.preposterousuniverse.com/blog
- [WP]: 2,228 posts, 2004-02 to 2025-11. Mean 546 words, so about **1.2M words**. Many recent posts are Mindscape podcast pages. — [WP API](https://www.preposterousuniverse.com/blog/wp-json/wp/v2/posts?per_page=1)
- Style: conversational physics explainer; 9.3% of sentences are questions.

**Tanner Greer: The Scholar's Stage (history, strategy, China)**
- URL: https://scholars-stage.org
- [WP]: 602 posts, 2008-04 to 2026-09. Mean 1,943 words, so about 1.17M, but **27% of the words are inside blockquotes**. Own words are about 0.85M. — [WP API](https://scholars-stage.org/wp-json/wp/v2/posts?per_page=1)
- License: "© All rights reserved." — [homepage](https://scholars-stage.org/)
- Political bleed: high (geopolitics, US politics).

**Ted Gioia, Noah Smith**: see above.

**TIER B: mid-size (about 200k–700k free words)**

**Morgan Housel: Collaborative Fund blog (behavioral finance, business)**
- URL: https://collabfund.com/blog/authors/morgan/
- [PG]: the author page lists **348 posts, Sep 2016 to Apr 2026**. A 14-post sample averaged 972 words (median 985), so about **340k words**. — [Collab Fund author page](https://collabfund.com/blog/authors/morgan/)
- Posts by year, from page dates: 2016: 27; 2017: 61; 2018: 42; 2019: 45; 2020: 41; 2021: 32; 2022: 38; 2023: 36; 2024: 17; 2025: 11; 2026: 2. Output fell sharply after 2023. — [Collab Fund author page](https://collabfund.com/blog/authors/morgan/)
- Not checked: his earlier Motley Fool and WSJ columns (2008–2016), which were publisher-edited.
- License: none found on the blog index; the site has a /terms-of-use page. — [Collab Fund blog](https://www.collabfund.com/blog/)
- Style (from reading):
  - short declarative sentences and one-line paragraphs
  - opens with a historical anecdote, then a single principle, then "the point is…"
  - aphorisms
- Political bleed: very low. Transferability to memos: very high.
- Datasets: none found on HF ("housel").

**Adam Mastroianni: Experimental History**
- URL: https://www.experimental-history.com
- [SUB]: 143 posts, 2022-01-01 to 2026-10-28. Free: 116 posts, **322,615 words**. Paid: 27 posts, 50,171 words. — [archive API](https://www.experimental-history.com/api/v1/archive?sort=new&limit=25)
- Style markers [measured on 20 posts]:
  - mean sentence 22.5
  - "you" 17.4 per 1k
  - 8.3% questions
  - frequent footnotes
  - from reading: jokey section headers, absurd analogies, first-person lab anecdotes, a mock-grandiose tone about science and academia
- Political bleed: low.

**Dynomight**
- URLs: https://dynomight.net, https://dynomight.substack.com
- [SUB]: 211 posts, 2021-05-11 to 2026-10-28, all free, **395,860 words** (3 link posts, 5,452 words). — [archive API](https://dynomight.substack.com/api/v1/archive?sort=new&limit=25)
- License: none stated on the About page. — [About](https://dynomight.net/about/)
- Explicit human-authorship statement: "All words are written by me (a human) by physically pressing keys with my fingers. All of them." AI is used only for research, fact-checking and spelling. — [AI usage](https://dynomight.net/ai/)
- The Substack mirror's robots.txt names AI crawlers (Substack opt-out). The dynomight.net robots.txt does not block them. — [Substack robots](https://dynomight.substack.com/robots.txt), [dynomight.net robots](https://dynomight.net/robots.txt)
- Style markers [measured on 30 posts]:
  - shortest sentences of the group (17.3)
  - 11.5% questions (highest)
  - "you" 19.6 per 1k
  - 10 parentheses per 1k
  - from reading: bulleted reasoning, explicit uncertainty, playful headers and self-mockery, "Grug" voice pieces
- Political bleed: low.

**Sarah Constantin: Rough Diamonds (Substack) and Otium (WordPress, 2014–2019)**
- URLs: https://sarahconstantin.substack.com, https://srconstantin.wordpress.com
- [SUB]: 151 posts, 2019-01-23 to 2026-10-07. Free: 142 posts, **291,117 words**. Paid: 9 posts. — [archive API](https://sarahconstantin.substack.com/api/v1/archive?sort=new&limit=25)
- Otium [WP]: 129 posts, 2014-04 to 2019-08. Mean 1,858 words, so about **240k words**. — [WP.com API](https://public-api.wordpress.com/wp/v2/sites/srconstantin.wordpress.com/posts?per_page=1)
- Combined: about 530k.
- Style: analytical, literature-review heavy (biotech, longevity, cognition); many footnotes and citations; 15.6 "I" per 1k.

**Jason Crawford: Roots of Progress**
- URLs: https://rootsofprogress.org, https://newsletter.rootsofprogress.org
- [SUB]: 252 posts, 2019-03-10 to 2026-09-03. Free: 233 posts, **405,659 words** (14 link and announcement posts, 10,689 words). Paid: 19 posts. — [archive API](https://newsletter.rootsofprogress.org/api/v1/archive?sort=new&limit=25)
- License: "Roots Of Progress Institute © 2026". No open license. — [rootsofprogress.org](https://rootsofprogress.org/)
- Organization status: it is now an institute, and some newsletter posts are announcements.
- Ideological lean: pro-progress and pro-technology ("techno-humanist manifesto").

**Tim Urban: Wait But Why**
- URL: https://waitbutwhy.com
- [WP]: 222 posts, 2013-07 to 2026-03. A 172-post sample averaged 2,867 words, but the median is only 668. A handful of giant posts (AI, Neuralink, the 2023 book) dominate. Total about **640k words**. Stick-figure images carry part of the meaning and are not text. — [WP API](https://waitbutwhy.com/wp-json/wp/v2/posts?per_page=1)
- License: "© WaitButWhy 2026". — [homepage](https://waitbutwhy.com/)
- Style markers [measured on 30 posts]:
  - "you" 17.6 per 1k
  - em-dash 9.9 per 1k
  - very short paragraphs (39 words)
  - 7.3 footnote markers per post
  - from reading: ALL-CAPS emphasis, invented characters and metaphors (the "Instant Gratification Monkey"), staircase diagrams
- Datasets: GitHub `mckaywrigley/wait-but-why-gpt` (337 stars), a retrieval/QA project over WBW posts. — [GitHub search](https://api.github.com/search/repositories?q=wait%20but%20why)

**Cal Newport: Study Hacks blog**
- URL: https://calnewport.com/blog
- [WP]: 1,130 posts, 2007-07 to 2026-10. Mean 601 words, so about **680k words**. — [WP API](https://calnewport.com/wp-json/wp/v2/posts?per_page=1)
- License: "Copyright © 2026 Cal Newport, All rights reserved." — [blog](https://calnewport.com/blog/)
- Style markers:
  - mean sentence 23.8; "you" 13.9 per 1k; short paragraphs (38)
  - from reading: thesis up front, named concepts ("deep work", "slow productivity"), anecdote, then a numbered rule
- Political bleed: low. Topic: productivity and tech critique (overlaps tech).

**Slime Mold Time Mold**
- URL: https://slimemoldtimemold.com
- [WP.com]: 214 posts, 2020-09 to 2026-10. Mean 2,732 words (median 1,262), so about **580k words**; 14% inside blockquotes. — [WP.com API](https://public-api.wordpress.com/wp/v2/sites/slimemoldtimemold.com/posts?per_page=1)
- **Not single-author.** The About page byline is "E & S & R" and it uses "We" throughout. No license statement. — [About](https://slimemoldtimemold.com/about/)
- Style: "you" 18.6 per 1k, "I" 2.1 per 1k, conspiratorial-playful science tone (e.g., the "A Chemical Hunger" obesity series).

**Casey Handmer: blog (space, energy, engineering economics)**
- URL: https://caseyhandmer.wordpress.com
- [WP.com]: 379 posts, 2010-06 to 2026-10. Mean 2,398 words, so about **910k words**. — [WP.com API](https://public-api.wordpress.com/wp/v2/sites/caseyhandmer.wordpress.com/posts?per_page=1)
- Style: engineer's back-of-envelope analysis with strong opinions; 1.9 exclamation marks per 1k.
- Scope note: partly a startup and tech founder voice (Terraform Industries).

**Brian Hayes: bit-player (computation and math, recreational)**
- URL: http://bit-player.org (rebuilt as an Eleventy static site)
- [PG]: the "all stories" list has **376 posts, 2006 to 2026**: 70 in 2006, under 10 a year since 2018. A 12-post sample averaged about 2,000 words (may include comments), so roughly 0.6–0.75M. — [all stories](http://bit-player.org/lists/all-stories/)
- License: none found.
- Style: graceful essayistic math exposition; posts are often built around a toy program.

**Derek Thompson: Substack (economics, culture, work)**
- URL: https://www.derekthompson.org
- [SUB]: 111 posts, 2025-06-20 to 2026-11-04. Free: 72 posts, **184,253 words**. Paid: 39 posts, 141,735 words. — [archive API](https://www.derekthompson.org/api/v1/archive?sort=new&limit=25)
- His larger body of work (The Atlantic, 2012–2025) is magazine-edited and partly metered. Political and policy content is moderate to high ("Abundance", "The Trump Decade Is Over").

**TIER C: small or inaccessible corpus**

**Randall Munroe: What If?**
- URL: https://what-if.xkcd.com
- [PG]: the archive lists **162 entries**. A 10-entry sample averaged 957 words, so about **155k words**. — [What If archive](https://what-if.xkcd.com/archive/)
- License: the xkcd comics are "licensed under a Creative Commons Attribution-NonCommercial 2.5 License". — [xkcd license](https://xkcd.com/license.html). The What If site footer shows only "©2026 xkcd, inc." with no CC statement, so the CC BY-NC grant is **not clearly extended to What If text**. — [What If](https://what-if.xkcd.com/)
- Style: absurd premise taken literally; deadpan escalation; stick-figure punchlines; "you" 14.6 per 1k.

**Patrick McKenzie: Bits about Money (finance infrastructure)**
- URL: https://www.bitsaboutmoney.com
- [PG]: 63 posts in the sitemap. An 8-post sample averaged 3,329 words, so about **210k words**. — [sitemap](https://www.bitsaboutmoney.com/sitemap-posts.xml)
- Style: long, wry, insider explanations of payments and banking.
- Scope note: the author is also a well-known software/startup writer (Kalzumeus), so this overlaps the tech track.

**Nadia Asparouhova: nadia.xyz**
- URL: https://nadia.xyz
- [PG]: /posts lists 72 dated entries (2014 to 2024; the latest is June 2024). A 10-post sample averaged 1,696 words (median 956), so about **120k words**. — [nadia.xyz posts](https://nadia.xyz/posts/)
- Topics: open source, philanthropy, tech culture; overlaps the tech track.

**Matt Levine: Money Stuff (Bloomberg Opinion)**
- Bloomberg's website requires a subscription. Money Stuff also arrives as a free email newsletter. — [Wikipedia](https://en.wikipedia.org/wiki/Matt_Levine_(columnist)), [roytang mirror note](https://mirror.roytang.net/2021/02/newsletters-redux)
- The newsletter launched in February 2015. One reader's word-count analysis says it "has gotten a bit longer in recent years" but publishes charts only, no figures. — [Daniel Stone, "Money Stuff is Linear-ish"](https://danielstone.substack.com/p/money-stuff-is-linear-ish)
- Unofficial scrapes exist:
  - GitHub `WhiteChair/moneystuff-archive`: "851+ issues classified by theme", sourced from NewsletterHunt, no license. — [repo](https://github.com/WhiteChair/moneystuff-archive)
  - GitHub `polybuildr/money-stuff`: topic analysis. — [GitHub search](https://api.github.com/search/repositories?q=money%20stuff%20levine)
- Style:
  - "builds up the relevant instruments and market context first, then delivers a punchline". — [Gwern, "Why so few Matt Levines?"](https://gwern.net/matt-levine)
  - "blending technical explanation with wit". — [Harvard Magazine](https://www.harvardmagazine.com/2025/07/harvard-bloomberg-column-matt-levine)

**Tyler Cowen: Marginal Revolution**
- URL: https://marginalrevolution.com
- Cloudflare blocked automated access, so I could not count posts. The blog's own fourth-anniversary post (Aug 2007) reported over 6,000 posts, about 4.4 a day. — [MR, "The revolution"](https://marginalrevolution.com/marginalrevolution/2007/08/the-revolution.html)
- The blog is co-written with Alex Tabarrok. Posts are typically short and quote-heavy.

**Derek Lowe: In the Pipeline (science.org)**
- science.org returned HTTP 403 to automated access, so I could not count posts.
- The blog dates from 2002 (Wikipedia cites a first post on 7 Feb 2002) and has run continuously, earlier on Corante and sciencemag.org. — [Wikipedia](https://en.wikipedia.org/wiki/Derek_Lowe_(chemist))
- Hosted by AAAS (Science), so the terms are the publisher's.

**Sabine Hossenfelder: Backreaction**
- URL: https://backreaction.blogspot.com
- [BLG]: **2,956 posts**, 2006 to 2026. The feed is summary-only, and HTML sampling picked up comments and sidebars, so I have **no reliable word estimate**. — [Blogger feed](https://backreaction.blogspot.com/feeds/posts/summary?alt=json&max-results=1)
- Recent posts look like YouTube video companions (e.g., "Physics is unravelling and it will get…", Nov 2026).

**Ed Yong**
- He left The Atlantic in 2023. His blog Not Exactly Rocket Science is "now-defunct" and ran on National Geographic's Phenomena network. — [Wikipedia](https://en.wikipedia.org/wiki/Ed_Yong)
- The work is magazine-edited and behind a paywall or meter. **Drop.**

**Richard Feynman: Feynman Lectures on Physics online**
- Caltech hosts the lectures free to read, but the copyright holders have not allowed download or redistribution, and the site blocks automated access (403 / Cloudflare). — [APS News](https://www.aps.org/apsnews/2014/10/feynman-lectures-now-freely-available-online), [Wikipedia](https://en.wikipedia.org/wiki/The_Feynman_Lectures_on_Physics)
- An HF repo `harisnaeem/The_Feynman_Lectures_on_Physics_Textbook_...` exists, which is likely a copyright problem. The lectures are also not a contemporary blog voice (transcribed lectures edited by Leighton and Sands). **Drop.** — [HF search](https://huggingface.co/api/datasets?search=feynman)

**Our World in Data (Max Roser, Hannah Ritchie)**
- See Key Question 2 for the license. Articles are team-produced and edited (Ritchie is "Deputy Editor and Science Outreach Lead"). Ritchie's own voice is on her Substack ("By the Numbers") and hannahritchie.com. — [OWID Hannah Ritchie page](https://ourworldindata.org/team/hannah-ritchie)

**Bryan Caplan: Bet On It (economics, libertarian)**
- URL: https://www.betonit.ai
- [SUB]: **6,041 posts, 2005-01-17 to 2026-10-30**. Free: 6,024 posts, **2,821,198 words** (mean 468). Of these, 5,077 posts (2.11M words) are dated before 2022 and appear to be his EconLog archive (2005–2021) imported into the Substack. — [archive API](https://www.betonit.ai/api/v1/archive?sort=new&limit=25)
- Style (from reading): short punchy argument posts; bets and challenges; "social desirability bias" style concept handles.
- **Political bleed: high** (libertarian, immigration, education).

**Freddie deBoer**
- URL: https://freddiedeboer.substack.com
- [SUB]: 1,412 posts, 2017-03-29 to 2026-11-04. Free: 1,077 posts, **2,067,409 words**. Paid: 334 posts, 567,955 words. — [archive API](https://freddiedeboer.substack.com/api/v1/archive?sort=new&limit=25)
- robots.txt lists AI crawlers (opt-out). — [robots.txt](https://freddiedeboer.substack.com/robots.txt)
- **Mostly political, cultural and education polemic, so skip** (as the candidate list suggested).

**Venkatesh Rao: Contraptions (Substack; formerly Breaking Smart / Ribbonfarm Studio)**
- URL: https://contraptions.venkateshrao.com
- [SUB]: 482 posts, 2015-08-14 to 2026-11-06. Free: 384 posts, **905,392 words**. Paid: 98 posts, 284,903 words. — [archive API](https://contraptions.venkateshrao.com/api/v1/archive?sort=new&limit=25)
- Combined with Ribbonfarm: about **2.4M words** of Rao.
- The Ribbonfarm AI-training grant covers ribbonfarm.com only, not this Substack.

**Dan Davies: Back of Mind (finance, economics, management cybernetics)**
- URL: https://backofmind.substack.com
- [SUB]: 312 posts, 2023-03-14 to 2026-11-04. Free: 311 posts, **254,207 words** (mean 817; 70–82 posts a year). — [archive API](https://backofmind.substack.com/api/v1/archive?sort=new&limit=25)
- Style (from reading): wry British, short, an ex-bank-analyst voice, accountability-sink concept handles.
- Political bleed: low-medium (UK politics appears).

**Henrik Karlsson: Escaping Flatland (essays on learning, attention, writing)**
- URL: https://www.henrikkarlsson.xyz
- [SUB]: 121 posts, 2021-10 to 2026-11. Free: 72 posts, **157,768 words**. Paid: 49 posts, 92,326 words. — [archive API](https://www.henrikkarlsson.xyz/api/v1/archive?sort=new&limit=25)
- Lyrical, personal essays. Below 200k free words.

**Kyla Scanlon (markets and economy explainers)**
- URL: https://kyla.substack.com
- [SUB]: 204 posts, 2021–2026. Free: only 48 posts, **162,778 words**. Paid: 156 posts, 375,327 words. — [archive API](https://kyla.substack.com/api/v1/archive?sort=new&limit=25)
- Mostly paywalled. A Gen-Z explainer voice ("vibecession"); much of her output is video.

**Hannah Ritchie: By the Numbers (formerly Sustainability by Numbers; energy, climate, food, development)**
- URL: https://hannahritchie.substack.com
- [SUB]: 173 posts, 2022-11-20 to 2026-11-03, **all free, 217,221 words** (mean about 1,256). — [archive API](https://hannahritchie.substack.com/api/v1/archive?sort=new&limit=25)
- License: no license text on the About page. — [About](https://hannahritchie.substack.com/about). Her OWID articles are CC BY, but they are team-edited. — [OWID About](https://ourworldindata.org/about)
- Style (from reading): calm, data-first myth-busting; a chart in every post; low snark.
- Political bleed: low-medium (climate policy).

**Robin Hanson: Overcoming Bias (economics, signalling, futurism)**
- URL: https://www.overcomingbias.com (now on Substack)
- [SUB]: **4,904 posts, 2006-11-20 to 2026-11-03**. Free: 4,900 posts, **3,225,072 words** (mean about 660). Posting peaked at 689 posts in 2007 and 791 in 2008, and has run about 100–130 a year since 2015. — [archive API](https://www.overcomingbias.com/api/v1/archive?sort=new&limit=25)
- **Multi-author before 2009:** of 5 random 2007 posts, 1 was bylined "Eliezer Yudkowsky" (e.g., "Self-Anchoring", 2007-10-22). Filter by `publishedBylines`. — [post API example](https://www.overcomingbias.com/api/v1/posts/self-anchoringhtml)
- Style (from reading): terse, provocative "X is not about X" signalling claims; short posts; very distinctive.
- Political bleed: medium (contrarian policy positions).

**Warren Buffett shareholder letters (possible addition)**
- HF `eagle0504/warren-buffett-annual-letters-1977-2022` turned out to be **Q&A pairs** (17,000 rows of "### Human / ### Assistant"), not the raw letters, so it is not usable as a style corpus. — [HF datasets-server](https://datasets-server.huggingface.co/rows?dataset=eagle0504/warren-buffett-annual-letters-1977-2022&config=default&split=train&offset=0&length=100)

#### Hugging Face / GitHub dataset search summary
- HF dataset-name searches returned **nothing** for these terms: slatestarcodex, astral codex, acoup, devereaux, matt levine, money stuff, wait but why, marginal revolution, noahpinion, terence tao, derek lowe, experimental history, dynomight, ribbonfarm, howard marks, construction physics, gioia, mastroianni, hossenfelder, cowen, hannah ritchie, roots of progress. — [HF API search](https://huggingface.co/api/datasets?search=dynomight)
- Hits: `abhayesian/acx_posts_only` (ACX), `yoonholee/style-eval-pg-karpathy-gwern` (CC0), and LessWrong dumps (`trentmkelly/LessWrong-43k` CC0, `x65617379/lesswrong_260509`, `xTimeCrystal/LessWrong-2025-09-24`, `achinta3/lesswrong-blogs`). — [HF API search](https://huggingface.co/api/datasets?search=lesswrong)
- For comparison, the tech-adjacent Paul Graham essays have more than 15 HF datasets (e.g., `sgoel9/paul_graham_essays`). — [HF API search](https://huggingface.co/api/datasets?search=paul%20graham)

### Inferences
- **Best "big, clean, single-voice, informational + narrative" pools outside tech:**
  - Scott Alexander (about 4.5M)
  - Bret Devereaux (about 2.1M, almost no quoting)
  - Aswath Damodaran (about 1.56M)
  - Venkatesh Rao (1.54M, audited)
  - Brian Potter (0.8M free)
  - Howard Marks (about 0.9M)
  - Noah Smith (about 4M, but political)
- **Best mid-size voices for a memo-style model:** Housel (about 340k), Mastroianni (about 320k), Dynomight (about 400k), Newport (about 680k), Constantin (about 530k). Each is large enough for a LoRA style fine-tune, where 100k–500k words is typically plenty.
- Substack's `wordcount` field gives exact free/paid splits. Using it, Noahpinion, ACX, Dynomight, Constantin and Roots of Progress are 80–100% free by word. Honest Broker and Derek Thompson are about 50% paywalled.
- Title filtering matters. On ACX it removes about 48% of free words (guest reviews, comment highlights, contests). Anyone building a corpus should filter by title and author before training.

### Gaps
- Matt Levine, Tyler Cowen and Derek Lowe: no measured free word counts. Bloomberg is paywalled; MR and science.org blocked automated access (Cloudflare / 403).
- Sabine Hossenfelder: post count only; the word estimate is unreliable.
- Housel, What If, Bits about Money, Nadia and Oaktree: estimates rest on 8–14 post samples and are accurate to about ±30%.
- Robin Hanson: see the update at the end of Key Question 4's Gaps. (deBoer, Caplan, Karlsson, Davies, Scanlon, Contraptions and Ritchie are measured above.)
- Bryan Caplan: 4 randomly sampled pre-2022 posts (2009, 2010, 2015, 2019) are all bylined "Bryan Caplan" in the Substack post API. That fits an import of only his own EconLog posts, but I did not check every post. — [example post API](https://www.betonit.ai/api/v1/posts/labeling_the_rihtml)

---

## Which have an explicit open license (CC0, CC-BY, CC-BY-SA) that makes corpus building clean?

### Takeaway
Very few. **Gwern (CC0)** and **Our World in Data (CC BY 4.0)** are the only candidates I verified with an explicit open license. OWID is team-written, so it gives you a clean license but no single author's voice. **Ribbonfarm** is all rights reserved but **explicitly grants AI/ML training permission** (attribution of the domain in provenance disclosures), with a TDMRep file. That makes it the cleanest large single-author option. xkcd comics are CC BY-NC 2.5, but that is not clearly extended to What If text. Everyone else is "all rights reserved" or states nothing, and two Substacks (Honest Broker, Dynomight's Substack mirror) actively opt out of AI crawling.

### Cited Findings
- Gwern: "This site is licensed under the Creative Commons public domain (CC-0) license." — [Gwern About](https://gwern.net/about)
- Our World in Data: "Our charts, articles, and data are licensed under CC BY, unless stated otherwise." It links to CC BY 4.0. Third-party materials are excepted. — [OWID About](https://ourworldindata.org/about); FAQ: "you can use, reproduce, and distribute any chart we made… provided that you cite us." — [OWID FAQs](https://ourworldindata.org/faqs)
- Ribbonfarm:
  - All posts by Venkatesh Rao are © Venkatesh Rao, 2007–2024. Guest contributors keep their own copyright.
  - "Limited non-exclusive permission is granted to AI and machine learning systems to crawl, index, and use this site's content for training language models… The only condition is that the source domain (ribbonfarm.com) be acknowledged in any public disclosure of training data provenance or lineage."
  - Substantial reproduction otherwise needs permission.
  - Source: [Ribbonfarm copyright](https://ribbonfarm.com/copyright/). The TDMRep file has `"tdm-reservation": 0` and points to that policy. — [tdmrep.json](https://ribbonfarm.com/.well-known/tdmrep.json)
- xkcd: "This work is licensed under a Creative Commons Attribution-NonCommercial 2.5 License." — [xkcd license](https://xkcd.com/license.html). The What If site footer says "©2026 xkcd, inc." with no CC text. — [What If](https://what-if.xkcd.com/)
- Explicit "All rights reserved":
  - Cal Newport — [blog](https://calnewport.com/blog/)
  - John D. Cook — [blog](https://www.johndcook.com/blog/)
  - Oaktree / Howard Marks — [memos](https://www.oaktreecapital.com/insights/memos)
  - Scholar's Stage — [homepage](https://scholars-stage.org/)
  - Wait But Why ("© WaitButWhy 2026") — [homepage](https://waitbutwhy.com/)
  - Roots of Progress ("Roots Of Progress Institute © 2026") — [homepage](https://rootsofprogress.org/)
- No license statement found:
  - ACOUP — [About](https://acoup.blog/about-the-pedant/)
  - Slime Mold Time Mold — [About](https://slimemoldtimemold.com/about/)
  - Dynomight — [About](https://dynomight.net/about/)
  - Terence Tao, SSC, Marginal Revolution, Backreaction, Damodaran, Collab Fund, bit-player, nadia.xyz: homepage text scanned for "license / creative commons / copyright / ©", no hits.
- Feynman Lectures online: copyright Caltech and co-holders; free to read; download and redistribution not permitted without consent. A 2013 DMCA takedown hit a script that built ebooks from the site. — [Wikipedia](https://en.wikipedia.org/wiki/The_Feynman_Lectures_on_Physics), [APS News](https://www.aps.org/apsnews/2014/10/feynman-lectures-now-freely-available-online)
- AI-crawler opt-outs in robots.txt:
  - The Honest Broker blocks GPTBot, CCBot, ClaudeBot, anthropic-ai, Google-Extended, Bytespider and Applebot-Extended. — [robots.txt](https://www.honest-broker.com/robots.txt)
  - freddiedeboer.substack.com and dynomight.substack.com also list AI crawlers. — [Freddie robots](https://freddiedeboer.substack.com/robots.txt), [Dynomight Substack robots](https://dynomight.substack.com/robots.txt)
  - No AI-bot blocks were found on acoup.blog, astralcodexten.com, waitbutwhy.com, what-if.xkcd.com, dynomight.net, calnewport.com, collabfund.com, gwern.net, ourworldindata.org, experimental-history.com, noahpinion.blog, construction-physics.com, aswathdamodaran.blogspot.com, ribbonfarm.com or oaktreecapital.com.
- LessWrong: no authoritative current site-wide license found. A 2018-era thread discussed moving to CC-BY, and individual authors self-license. — [LessWrong licensing discussion](https://www.lesswrong.com/posts/isc9fnLQ2e9dDjfuJ/licensing-discussion-for-lesswrong-posts). The sister EA Forum moved to CC BY 4.0 for posts after Dec 1, 2022. — [EA Forum license post](https://forum.effectivealtruism.org/s/HsxeFDis7YBDNhFnH/p/KK6AE8HzPkR2KnqSg)
- Existing third-party HF datasets lack licenses: `abhayesian/acx_posts_only` declares none; `trentmkelly/LessWrong-43k` self-declares cc0-1.0, which does not change the underlying authors' copyright. — [HF API](https://huggingface.co/api/datasets/abhayesian/acx_posts_only), [HF API](https://huggingface.co/api/datasets/trentmkelly/LessWrong-43k)

### Inferences
- For a commercial product, the legally cleanest single-author choices are **Gwern (CC0)** and then **Ribbonfarm/Venkatesh Rao**, whose permission targets AI training directly.
- OWID is CC BY but multi-author and house-edited. It suits a "clear data explainer" register rather than one person's voice.
- For everyone else, a clean route needs **direct permission from the author**. Many of these are independent writers on Substack or WordPress, which makes them reachable. Alternatively, keep the use to personal, non-distributed fine-tuning and get legal advice. The opt-out signals (Gioia, deBoer, the Dynomight Substack setting) suggest those authors would refuse.

### Gaps
- I did not read the full Substack Terms of Service or each Substack author's footer for custom license language.
- I did not check Bloomberg's, AAAS/Science's or The Atlantic's terms in detail, beyond noting they are publisher-owned.
- Hannah Ritchie's personal Substack license: not checked. Her robots.txt has no AI-bot blocks. — [robots.txt](https://hannahritchie.substack.com/robots.txt)

---

## Which voices are most distinctive and most transferable to everyday informational writing (memos, explainers, docs) rather than tied to one niche topic?

### Takeaway
For transferable memo and explainer voices with storytelling flair, the strongest are:
- **Morgan Housel**: anecdote leading to a principle; short sentences; nearly topic-agnostic.
- **Scott Alexander**: structured argument with humor; works on any topic.
- **Dynomight**: playful, rigorous, bulleted reasoning.
- **Adam Mastroianni**: comic, second-person science essays.
- **Howard Marks**: the literal investment memo.
- **Aswath Damodaran**: a teacherly how-to-analyze voice.

Highly distinctive but niche-locked: Devereaux (ancient and military history), Tao (math), Potter (construction and industry; a clean but neutral voice), Gioia (music). Matt Levine is perhaps the most distinctive explainer voice in finance, but his corpus is paywalled and Gwern argues the formula is "largely irreproducible". Wait But Why is distinctive, but part of the voice lives in drawings.

### Cited Findings
Style metrics I measured with one script over recent and older samples. Blockquotes, code and figures were excluded. Sentence splitting is heuristic.

| Author (sample) | Mean sentence len (words) | % questions | "you"/1k | "I"/1k | parens/1k | dashes/1k | mean para words | footnote markers/post |
|---|---|---|---|---|---|---|---|---|
| Devereaux ACOUP (30 posts) | 35.0 | 2.3 | 4.9 | 5.3 | 12.5 | 7.0 | 114 | 6.7 |
| Scott Alexander SSC (30) | 20.5 | 7.2 | 12.6 | 11.7 | 4.7 | 4.4 | 64 | 0 |
| Tim Urban WBW (30) | 25.1 | 6.5 | 17.6 | 13.0 | 4.7 | 9.9 | 39 | 7.3 |
| Cal Newport (30) | 23.8 | 5.1 | 13.9 | 11.4 | 4.2 | 4.1 | 38 | 0 |
| Mastroianni Exp. History (20) | 22.5 | 8.3 | 17.4 | 11.8 | 2.8 | 4.9 | 55 | 27.6* |
| Dynomight (30) | 17.3 | 11.5 | 19.6 | 15.4 | 10.0 | 1.4 | 42 | 8.1* |
| Sarah Constantin (20) | 23.5 | 5.5 | 12.1 | 15.6 | 11.7 | 2.7 | 32 | 39.4* |
| Brian Potter Constr. Physics (20) | 28.4 | 1.2 | 3.4 | 2.3 | 6.5 | 3.5 | 71 | 2.1 |
| Jason Crawford RoP (18) | 21.9 | 3.5 | 10.5 | 6.6 | 7.5 | 5.5 | 40 | 0 |
| Ted Gioia (20) | 16.2 | 3.3 | 10.1 | 12.6 | 2.6 | 11.8 | 36 | 0 |
| Noah Smith (20) | 21.2 | 3.0 | 3.9 | 6.3 | 1.6 | 10.0 | 49 | 11.3* |
| Damodaran (25)** | 40.1 | 2.0 | 11.4 | 10.6 | 7.1 | 0.0 | 78 | 0 |
| Munroe What If (5) | 24.2 | 6.4 | 14.6 | 2.9 | 2.4 | 7.4 | 41 | 0.2 |
| Nadia Asparouhova (10) | 27.1 | 3.9 | 8.0 | 12.9 | 6.2 | 4.4 | 54 | 8.3 |
| Slime Mold Time Mold (30) | 19.0 | 6.0 | 18.6 | 2.1 | 4.3 | 3.4 | 47 | 0 |
| Casey Handmer (30) | 20.4 | 3.8 | 3.5 | 7.6 | 4.6 | 2.3 | 67 | 0 |
| Tanner Greer (30) | 19.2 | 4.1 | 6.5 | 7.4 | 7.2 | 16.7 | 82 | 3.3 |
| Sean Carroll (30) | 20.6 | 9.3 | 7.6 | 7.1 | 5.2 | 6.6 | 69 | 0.1 |
| Terence Tao (30) | 28.3 | 0.4 | 0.2 | 2.2 | 22.4 | 1.7 | 41 | 0 |
| John D. Cook (30) | 17.7 | 3.6 | 14.6 | 12.3 | 9.3 | 0.0 | 36 | 0.5 |
| Otium/Constantin (30) | 23.7 | 4.8 | 12.4 | 8.4 | 9.0 | 3.2 | 46 | 0.1 |

\* Substack footnote anchors are probably counted twice (in-text and in the note list). \*\* Damodaran's Blogger HTML uses line breaks rather than paragraphs, which inflates his sentence and paragraph figures.
Data sources: WordPress REST APIs ([acoup](https://acoup.blog/wp-json/wp/v2/posts), [SSC](https://slatestarcodex.com/wp-json/wp/v2/posts), [WBW](https://waitbutwhy.com/wp-json/wp/v2/posts), [Newport](https://calnewport.com/wp-json/wp/v2/posts)) and RSS feeds ([Experimental History](https://www.experimental-history.com/feed), [Dynomight](https://dynomight.net/feed.xml), [Construction Physics](https://www.construction-physics.com/feed), [Noahpinion](https://www.noahpinion.blog/feed), [Damodaran](https://aswathdamodaran.blogspot.com/feeds/posts/default), [What If](https://what-if.xkcd.com/feed.atom)).

- Levine's method, per Gwern: build up the instruments and market context first, then deliver a punchline that shows how incentives produce odd behavior. Cowen, quoted by Gwern, considers the formula largely irreproducible. — [Gwern, "Matt Levine"](https://gwern.net/matt-levine)
- Levine on his own craft: his work needs more attention to language than the average financial column. The style traces to comic emails explaining derivative trades at Goldman Sachs. — [Harvard Magazine](https://www.harvardmagazine.com/2025/07/harvard-bloomberg-column-matt-levine)
- Dynomight states that all words are human-typed. That makes the corpus unusually unlikely to contain LLM-generated text. — [Dynomight AI usage](https://dynomight.net/ai/)
- Scott Alexander's own stated techniques. These map directly onto markers a fine-tune would pick up. — [SSC, "Nonfiction Writing Advice" (2016)](https://slatestarcodex.com/2016/02/20/writing-advice/)
  - small chunks and section breaks ("Nobody likes walls of text")
  - varied sentence length and tone
  - strong transition words
  - deliberate parallelism
  - "microhumor"
  - concrete example before the abstract principle
  - signalling to the audience's tribe
  - defusing counterarguments in advance
  - memorable "concept handles"
- Reader attention on Hacker News, as a proxy for how distinctive and popular each voice is: stories with more than 100 points whose URL matches each domain (HN Algolia API, URL-restricted search, 2026-11-07).
  - gwern.net 100; acoup.blog 63; slatestarcodex.com 60; dynomight.net 57; calnewport.com 40; construction-physics.com 37
  - ribbonfarm.com 24; bitsaboutmoney.com 24; experimental-history.com 20; astralcodexten.com 12; honest-broker.com 10
  - waitbutwhy.com 9; collabfund.com 7; slimemoldtimemold.com 7; noahpinion.blog 6; what-if.xkcd.com 3; oaktreecapital.com 1; aswathdamodaran.blogspot.com 0
  - Source: [HN Algolia example query](https://hn.algolia.com/api/v1/search?query=acoup.blog&restrictSearchableAttributes=url&tags=story&hitsPerPage=1&numericFilters=points%3E100). HN skews toward tech readers, so finance writers are under-represented.
- Ribbonfarm's most influential posts ("The Gervais Principle", "A Big Little Idea Called Legibility", "The Internet of Beefs") show its voice runs to coined concepts and grand theory. — [Ribbonfarm stats](https://ribbonfarm.com/stats/)

### Inferences
- **Distance from generic LLM voice**, my judgment ranked from most to least distinctive:
  - **Very far:** Matt Levine (deadpan finance comedy), Devereaux (35-word sentences, footnote-laden pedantry), Gwern (sidenote density), Tim Urban (caps, invented characters, drawings), Scott Alexander (Roman-numeral structure, steelmanning, parables), Dynomight (11.5% questions, self-mockery), Mastroianni (comic grandiosity), Venkat Rao (neologisms and grand theories).
  - **Moderately far:** Housel (aphoristic, but his short-sentence "insight" cadence has been widely imitated, including by LLMs), Gioia, Noah Smith, Constantin.
  - **Close to LLM-neutral:** Brian Potter, Jason Crawford, Sean Carroll, John D. Cook, OWID house style. These are clean and well organized, but a fine-tune would add little "voice".
- **Most transferable to everyday memos, explainers and docs**, with my reasoning:
  1. **Morgan Housel.** Topic-light principles, anecdote then lesson, low politics, short paragraphs. The corpus is small-mid (about 340k), but it is enough for a LoRA.
  2. **Scott Alexander.** Universal argumentative scaffolding. Filter out culture-war posts.
  3. **Howard Marks.** The memo form itself: client-facing, reflective, anecdotal, finance-centric but principle-driven.
  4. **Dynomight.** Explainer and decision-analysis voice; human-written guarantee; small-mid corpus.
  5. **Adam Mastroianni.** Great for punchy explainers; the humor may be too much for formal docs.
  6. **Aswath Damodaran.** Instructive how-to-analyze voice; strongly tied to valuation vocabulary.
- **Niche-locked:**
  - Devereaux: Roman and military history vocabulary will bleed into outputs.
  - Tao and Cook: math notation and code.
  - Gioia: music.
  - Potter: construction.
  - Munroe: absurd hypotheticals, and the corpus is small.

### Gaps
- No reader-discussion source (HN or Reddit) was gathered for each author's style. The markers above come from my measurements and reading, not from cited critics, except for Levine.
- Metrics for Levine, Cowen, Lowe, Housel, Marks and Bits about Money were not computed (paywall, blocking, or feed failure).

---

## Heavy editing (magazines) vs. raw single-author voice; political content that would bleed into outputs

### Takeaway
Most strong candidates are raw, self-published, single-author blogs:
- ACOUP, SSC/ACX, Dynomight, Experimental History, Damodaran, Ribbonfarm (Venkat posts), Construction Physics, Wait But Why, Cal Newport

The edited or institutional exceptions are:
- Ed Yong (The Atlantic, National Geographic)
- Derek Thompson's pre-2025 Atlantic work
- Matt Levine (Bloomberg Opinion, edited but famously idiosyncratic)
- OWID (team-edited)
- Oaktree memos (corporate)
- the Feynman Lectures (edited transcriptions)

Multi-author contamination to filter:
- ACX guest book reviews
- Ribbonfarm guest posts (242 non-Venkat posts)
- Marginal Revolution (Tabarrok)
- Overcoming Bias (Yudkowsky and others, 2006–2009)
- Slime Mold Time Mold (a group)
- Noahpinion guest posts and interviews
- Construction Physics interviews

Highest political bleed: Noah Smith, Freddie deBoer, Tanner Greer, Bryan Caplan, Derek Thompson, and some Scott Alexander. Lowest: Housel, Damodaran, Potter, Dynomight, Mastroianni, Munroe, Newport.

### Cited Findings
- Ribbonfarm author split: Venkat 875 of 1,117 posts (1,539,789 of 2,117,465 words); about 59 other contributors. — [Ribbonfarm authors](https://ribbonfarm.com/authors/), [stats](https://ribbonfarm.com/stats/)
- ACX contamination by title: 78 "Your Book Review" guest posts (581,562 words) and 76 "Highlights From The Comments" (463,350 words). — [ACX archive API](https://www.astralcodexten.com/api/v1/archive?sort=new&limit=25)
- Noahpinion: 80 free posts with roundup, interview or guest titles, 286,656 words. — [Noahpinion archive API](https://www.noahpinion.blog/api/v1/archive?sort=new&limit=25)
- Construction Physics: 9 free reading-list and interview posts, 30,701 words. — [archive API](https://www.construction-physics.com/api/v1/archive?sort=new&limit=25)
- Slime Mold Time Mold is written by "E & S & R" and uses "We" throughout. — [About](https://slimemoldtimemold.com/about/)
- Damodaran: all 247 sampled Blogger posts were by "Aswath Damodaran". — [Blogger feed](https://aswathdamodaran.blogspot.com/feeds/posts/default?alt=json)
- Old Noahpinion Blogspot: of 150 sampled posts, 109 were credited to "Noah Smith", 30 to "Unknown" and 11 to "Anonymous". The account may have changed, or there may be guest posts. — [Blogger feed](https://noahpinionblog.blogspot.com/feeds/posts/default?alt=json)
- Scholar's Stage: 27% of words inside blockquotes (heavy quotation of sources). Slime Mold Time Mold 14%; SSC 11%; Noahpinion Blogspot 16%; ACOUP 2%; Damodaran about 0%. — WP and Blogger APIs above.
- Ed Yong left The Atlantic in 2023. Not Exactly Rocket Science ran on National Geographic's Phenomena network and is now defunct. — [Wikipedia](https://en.wikipedia.org/wiki/Ed_Yong)
- Derek Thompson's 2025–26 Substack titles include "The Trump Decade Is Over" and "How China Thinks About AI", a mix of politics and AI. — [archive API](https://www.derekthompson.org/api/v1/archive?sort=new&limit=25)
- Marginal Revolution is co-authored. It averaged about 4.4 posts a day by 2007. — [MR 2007](https://marginalrevolution.com/marginalrevolution/2007/08/the-revolution.html)
- Feynman Lectures online are an edition edited by Leighton and Sands, with Caltech as a copyright holder. — [Wikipedia](https://en.wikipedia.org/wiki/The_Feynman_Lectures_on_Physics)

### Inferences
- **Political or ideological bleed**, my judgment from the topic mix:
  - **High:** Noah Smith (US politics, China, industrial policy), Freddie deBoer (left politics, education; candidate list says skip), Bryan Caplan (libertarian, immigration), Tanner Greer (geopolitics), Derek Thompson (Abundance policy).
  - **Medium:** Scott Alexander (periodic culture-war and psychiatry-policy posts; filter by title or tag), Jason Crawford (pro-progress ideology), Ted Gioia (anti-big-tech cultural criticism), Venkat Rao (Gervais-Principle cynicism about organizations).
  - **Low:** Housel, Damodaran, Marks (markets, mildly macro), Potter, Dynomight, Mastroianni, Munroe, Newport, Devereaux (mostly history, with occasional current-events commentary).
- **Single-voice consistency over time:**
  - Very consistent: Devereaux, Dynomight, Mastroianni, Housel, Damodaran.
  - Long-running with drift: Scott Alexander (2013–2026 voice is consistent, topics drift); Venkat (2007–2024; early Ribbonfarm is more essayistic, later more "breaking smart" and protocol-focused); Noah (2010 academic-econ blogger to a 2020s geopolitics newsletter).
  - Cal Newport's 2007–2012 student-advice era differs in topic from his later tech-critique posts.
- For a small-LLM style fine-tune, the cleanest pipeline is a single-author self-published blog, with guest, link and comment-roundup posts dropped by title and blockquotes stripped from the HTML. The [SUB] and [WP] APIs used here make that filtering easy.

### Gaps
- **Update: all of the Substack pulls that were pending are now done** and recorded in the Key Question 1 catalog: deBoer, Caplan, Karlsson, Davies, Scanlon, Contraptions, Ritchie and Hanson.
- Overcoming Bias needs byline filtering to separate Hanson from Yudkowsky and other 2006–2009 co-bloggers. I did not count how many posts are non-Hanson.
- No systematic per-post political classification was done; the political-bleed ratings are judgments.
