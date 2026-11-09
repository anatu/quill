# Tech, software, startup, product and AI nonfiction writers as single-author style corpora (as of Nov 2026)

**How the numbers were produced (read this first).** All word counts below were measured in this session (7 Nov 2026) unless marked "unmeasured".
- **Crawl count:** I listed each site's posts from its archive page or sitemap, fetched the posts, stripped `script/style/nav/header/footer/aside/form`, kept `<article>`/`<main>` where present, and counted alphanumeric tokens. "FULL" means every post was fetched. "sample=N" means the mean of N randomly sampled posts multiplied by the post count. These counts include code blocks, math, footnotes, reference lists and captions, so prose-only totals for technical blogs are lower, probably by 5–20% (my guess).
- **Validation:** my Paul Graham full crawl gave 572,705 words. An independent dataset (yoonholee/style-eval-pg-karpathy-gwern) reports 562,990 words for 229 PG essays, a gap of about 2%.
- **Substack:** counts come from the `wordcount` field of the publication's own `/api/v1/archive` endpoint, split by `audience` ("everyone" = free, "only_paid" = paywalled) and by byline.
- **WordPress:** counts come from `/wp-json/wp/v2/posts` (`X-WP-Total` header for the post count, `content.rendered` for words), sampled from the first, middle and last result pages.
- **Simon Willison:** counted with SQL over his public Datasette copy of the blog database. The SQL counts whitespace tokens in the HTML body, which inflates the total slightly.

## Q1. Which candidates have at least ~100k (ideally 200k+) words of freely accessible, single-author informational prose?

### Takeaway
Most of the candidates clear 200k free words. The largest clean single-author corpora are:
- Cory Doctorow's Pluralistic: about 5.2M gross words, but much of each post is link roundups.
- Gwern: about 2.8–3.0M.
- Coding Horror: about 1.5M.
- Simon Willison: about 1.4M in entries.
- Will Larson: about 1.2M.
- patio11's Kalzumeus: about 1.2M.
- Joel on Software: 1,114 posts, word count unmeasured.
- Casey Handmer, Construction Physics (free part), Interconnects (free part), Steven Sinofsky, Dan Luu, Julia Evans and Paul Graham: each roughly 0.57–0.87M.

These fall short or should be dropped:
- Karpathy: about 130k, marginal.
- Chris Olah: about 51k, too small.
- Distill: multi-author, so not a single-author corpus.
- Bret Victor: noisy, interactive pages.
- Jason Fried: very short posts.
- Not Boring: large, but about 20% of posts carry another byline, so it needs filtering.

### Cited Findings

#### Size summary (measured unless noted)
| Author / outlet | Posts found | Free words (method) | Dates | Access |
|---|---|---|---|---|
| Cory Doctorow, Pluralistic | 1,746 | ~5.23M gross (WP REST, 246 posts sampled, mean 2,995); includes link roundups and boilerplate | 2020-02 to 2026-11 | Free |
| Gwern Branwen, gwern.net | 609 non-/doc/ pages | ~3.04M (sample of 40, mean 4,996, median 2,026); another dataset counts 2,800,357 for 220 pieces | 2010 to 2026 | Free |
| Packy McCormick, Not Boring | 677 (625 free) | 2,652,374 free + 246,840 paid (Substack); only 532 posts carry Packy's byline | 2019-05 to 2026-11 | Mostly free |
| Jeff Atwood, Coding Horror | 1,438 | ~1.55M (sample of 40, mean 1,080) | 2004 to 2020s | Free |
| Simon Willison | 3,344 entries + 8,503 link posts | ~1.43M entries + ~572k link-post commentary (SQL) | 2002-06 to 2026-11 | Free |
| Will Larson, lethain.com | 949 sitemap URLs | ~1.19M (sample of 40, mean 1,249; includes some non-post URLs) | 2007 to 2026 | Free |
| Patrick McKenzie, kalzumeus.com | 571 (site says 575) | ~1.17M (sample of 30, mean 2,044, median 665; high variance) | 2006 to 2025 | Free |
| Joel Spolsky, Joel on Software | 1,114 (site's own count) | **Unmeasured** (crawler blocked); a third-party scrape holds 209 pieces / 123,984 words | 1999-12 to 2022-12 | Free |
| Casey Handmer | 379 | ~867k (279 posts sampled, mean 2,287) | 2010-06 to 2026-10 | Free |
| Brian Potter, Construction Physics | 365 (252 free) | 803,653 free + 296,065 paid (Substack) | 2020-09 to 2026-11 | Partly paywalled |
| Nathan Lambert, Interconnects | 385 (340 free) | 799,378 free + 92,044 paid; 88 posts are podcasts | 2020-06 to 2026-11 | Mostly free |
| Steven Sinofsky, Hardcore Software | 165 | 709,906 (Substack; all marked free) | 2021-01 to 2026-09 | Free |
| Kevin Kelly, The Technium | 880 | ~0.7M, rough (only the latest 100 posts measured, mean 801) | 2024–2026 measured; older not measured | Free |
| Dan Luu | 122 | ~687k (FULL, mean 5,635, median 4,155) | ~2013 to 2026 | Free |
| Julia Evans, jvns.ca | 603 | ~627k (sample of 40, mean 1,040) | 2013-02 to 2026-09 | Free |
| Paul Graham | 236 | ~573k (FULL, mean 2,427, median 1,530) | ~2001 to 2026 | Free |
| Maciej Cegłowski, idlewords.com | 16 talks + 13 essays on index; another dataset counts 353 pieces | ~131k on index pages; the other dataset counts 524,614 | 2002 to 2026 | Free |
| Hillel Wayne | 40 site posts + 358 newsletter issues | ~70k + ~434k (samples of 30, means 1,763 and 1,211) | ~2016 to 2026 | Free |
| Eugene Yan | 182 | ~359k (sample of 30, mean 1,971) | 2015 to 2026 | Free |
| Lilian Weng, Lil'Log | 52 | ~302k (FULL, mean 5,816; includes math and references) | 2017-06 to 2026-07 | Free |
| Steve Yegge, Blogger | 66 | 270,865 (FULL feed) + other blogs not counted | 2006-03 to 2018-01 | Free |
| Ethan Mollick, One Useful Thing | 141 | 245,272 (Substack; all free) | 2022-11 to 2026-10 | Free |
| Charity Majors (charity.wtf, now on Substack) | 130 | 236,250 (all free) | 2015-12 to 2026-10 | Free |
| Patrick McKenzie, Bits about Money | 63 | ~191k (sample of 20, mean 3,031) | 2021 to 2026 | Free (paywall not verified) |
| Bret Victor, worrydream.com | 47 pages | ~190k nominal (sample of 40; median only 1,194; one page of 60k) | ~2006 to 2020s | Free |
| Andrej Karpathy | 23 + 15 posts | ~85k + ~43k, about 128k with code (FULL); another dataset counts 101,337 | 2011 to 2026 | Free |
| Chris Olah, colah.github.io | 15 | ~51k (FULL) | 2014-03 to 2020-05 | Free |
| Eli Bendersky | 1,330 (site's own per-year counts) | Unmeasured (only 10 recent posts fetched, mean 2,521) | 2003 to 2026 | Free |
| Ben Thompson, Stratechery (free weekly Articles only) | ≥61 archive pages × 10 ≈ 600+ | Unmeasured (HTTP 403/429) | 2013-04 to 2026-11 | Articles free; Updates for subscribers |
| DHH / Jason Fried, HEY World | Feed shows only the last 30 posts each | DHH mean 582 words/post; Jason mean 261 | DHH 2021–2026; Signal v. Noise archive 2005–2021 | Free |
| Byrne Hobart, The Diff | Not obtained | Unmeasured | — | Partly paywalled (prior knowledge) |
| Martin Fowler | Not obtained | Unmeasured | 2000s to 2026 | Free |
| Avery Pennarun, apenwarr.ca | Not obtained (no archive index) | Unmeasured | Posts linked from 2006 to 2026 | Free |

#### Per-candidate facts (with sources)
- **Paul Graham.**
  - The full crawl of 236 essays from the archive page gave mean 2,427 words, median 1,530 and about 573k total. [articles.html](https://paulgraham.com/articles.html)
  - The only rights notice is "© mmxxvi pg" on the index page; there is no license. [paulgraham.com/index.html](https://paulgraham.com/index.html)
  - An independent dataset counts 229 essays and 562,990 words. [yoonholee/style-eval-pg-karpathy-gwern](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)
- **Patrick McKenzie (patio11).**
  - The Kalzumeus homepage links "All 575 Essays", and its footer reads "© Patrick McKenzie (Kalzumeus Software, LLC) 2006 - 2026". [kalzumeus.com](https://www.kalzumeus.com/)
  - The archive gave 571 post URLs from 2006-06-27 ("So you want to be a microISV") to 2025-02-10. A sample of 30 gave mean 2,044 and median 665, so totals are skewed by a few 10k+ essays (largest sampled: 14,745). [archive](https://www.kalzumeus.com/archive/)
  - Bits about Money: the homepage says "You can read all 63 essays here" with footer "© 2021-2026 Kalzumeus Software, LLC". The sitemap lists 63 posts, and a sample of 20 gave mean 3,031 (range 441–7,500). [bitsaboutmoney.com](https://www.bitsaboutmoney.com/)
- **Dan Luu.**
  - Every one of the 122 posts linked from the homepage was fetched: mean 5,635, median 4,155, about 687k words. [danluu.com](https://danluu.com/)
  - No copyright or license text was found on the homepage or /about/. [danluu.com/about](https://danluu.com/about/)
- **Julia Evans.**
  - The sitemap lists 603 /blog/ posts from 2013-02-24 ("Trying out Octopress") to 2026-09-27. A sample of 40 gave mean 1,040 and median 928. [jvns.ca sitemap](https://jvns.ca/sitemap.xml)
  - The footer reads "© Julia Evans"; no license. [jvns.ca/about](https://jvns.ca/about/)
- **Simon Willison.**
  - His public Datasette database has these tables. [datasette.simonwillison.net](https://datasette.simonwillison.net/simonwillisonblog)
    - `blog_entry`: 3,344 rows (2002-06-12 to 2026-11-03), about 1.43M whitespace tokens of HTML body.
    - `blog_blogmark` (link posts): 8,503 rows, about 572k words of commentary.
    - `blog_quotation`: 1,480 rows, which are other people's words and should be excluded.
    - Further tables: `blog_note`, `blog_beat`, `guides_chapter`.
  - Entry words per year show two different eras:
    - 2002: 674 entries / 75k words. 2003: 648 / 116k. These are short link-blog posts.
    - 2020 onward: 76k (2020), 90k (2021), 124k (2022), 189k (2023), 152k (2024), 203k (2025). These are long-form. [same Datasette](https://datasette.simonwillison.net/simonwillisonblog)
  - The site footer shows only "©" with the years 2002–2026; no content license. [simonwillison.net/about](https://simonwillison.net/about/)
  - The blog's code repo is Apache-2.0. That covers the code only, not the writing. [simonw/simonwillisonblog](https://github.com/simonw/simonwillisonblog)
- **Gwern.**
  - The About page states: "This site is licensed under the Creative Commons public domain (CC-0) license", linking creativecommons.org/public-domain/cc0. [gwern.net/about](https://gwern.net/about)
  - The sitemap has 609 essay-like pages after excluding /doc/, /ref/ and /metadata/. A sample of 40 gave mean 4,996, median 2,026 and max 41,257. [gwern.net/sitemap.xml](https://gwern.net/sitemap.xml)
  - Markdown source is served by appending `.md` to a page URL; `/scaling-hypothesis.md` returned 147 KB. [gwern.net/scaling-hypothesis.md](https://gwern.net/scaling-hypothesis.md)
  - The site code is on GitHub (848 stars). [gwern/gwern.net](https://github.com/gwern/gwern.net)
- **Joel Spolsky.**
  - The archive states "1114 posts over 16 years". Its monthly archive runs from Dec 1999 to Dec 2022: every month from 2001 to 2009, then 11 months in 2010, 7 in 2011, 5 in 2012, and 1–3 a year after that. [joelonsoftware.com/archives](https://www.joelonsoftware.com/archives/)
  - There is no copyright or license statement ("Proudly powered by WordPress"). [same](https://www.joelonsoftware.com/archives/)
  - My crawler got HTTP 403 on the WordPress API and HTTP 429 on the sitemap, so the word count is unmeasured.
  - One existing dataset holds 209 Joel pieces / 123,984 words, a partial scrape. [yoonholee dataset](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)
- **Steve Yegge.**
  - The Blogger feed returned all 66 posts (2006-03-15 to 2018-01-23), totalling 270,865 words with mean 4,104. [steve-yegge.blogspot.com feed](https://steve-yegge.blogspot.com/feeds/posts/default?alt=json&max-results=500)
  - No license statement was found. [steve-yegge.blogspot.com](https://steve-yegge.blogspot.com/)
- **Maciej Cegłowski.**
  - The talks index lists 16 talks: mean 5,440, median 6,167, about 87k words. Examples are "Website Obesity", "Haunted by Data" and "Build a Better Monster". [idlewords.com/talks](https://idlewords.com/talks/)
  - The homepage links 13 essays (2003 to 2026-03, "Artemis II is not safe to fly"), mean 3,368. [idlewords.com](https://idlewords.com/)
  - The yoonholee dataset counts 353 pieces / 524,614 words from idlewords.com, so the full archive is much bigger than the index pages. [yoonholee dataset](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)
- **Andrej Karpathy.**
  - karpathy.github.io: 23 posts (2011-04 to 2026-02-12 "microgpt"), about 84.8k words including code. [karpathy.github.io](https://karpathy.github.io/)
  - Bearblog: 15 posts, about 43.5k words. [karpathy.bearblog.dev/blog](https://karpathy.bearblog.dev/blog/)
  - No license was found on either site.
- **Lilian Weng.**
  - All 52 posts in the sitemap were fetched: 2017-06-21 to 2026-07-04, mean 5,816, about 302k words. [lilianweng.github.io sitemap](https://lilianweng.github.io/sitemap.xml)
  - The footer reads "© 2026 Lil'Log". [lilianweng.github.io](https://lilianweng.github.io/)
  - The site source repo has 778 stars. [lilianweng/lilianweng.github.io](https://github.com/lilianweng/lilianweng.github.io)
- **Chris Olah and Distill.**
  - colah.github.io has 15 posts (2014-03 to 2020-05), about 51k words, with no license found. [colah.github.io](https://colah.github.io/)
  - Distill article footers say: "Diagrams and text are licensed under Creative Commons Attribution CC-BY 4.0 with the source available on GitHub, unless noted otherwise", with reused figures excepted. Distill articles are multi-author. [distill.pub, Zoom In](https://distill.pub/2020/circuits/zoom-in/)
- **Martin Fowler.**
  - The footer reads "© Martin Fowler | Disclosures". [martinfowler.com](https://martinfowler.com/)
  - The bliki landing page now shows only recent entries (24 Mar to 29 Oct 2026), so I could not get a full count. One entry, dated 29 Oct 2026, is titled "LLM-Voice". [martinfowler.com/bliki](https://martinfowler.com/bliki/)
- **Ben Thompson.**
  - The free Articles archive is paginated 10 per page. Page 60 covers 19 Apr to 29 May 2013 and links to a page 61, so there are about 600+ free weekly Articles. [Stratechery page 60](https://stratechery.com/category/articles/page/60/)
  - The section describes itself as "all free articles on Stratechery". Updates sit under "Stratechery Plus", and the footer reads "© Stratechery LLC 2026" with Terms of Service. [stratechery.com/category/articles](https://stratechery.com/category/articles/)
  - Existing scrapers include a Stratechery-to-CSV crawler that covers Daily Updates and Articles [BOBO-LU/Stratechery-crawler](https://github.com/BOBO-LU/Stratechery-crawler) and a chatbot over Articles [benfwalla/BenThompsonChatbot](https://github.com/benfwalla/BenThompsonChatbot).
- **Byrne Hobart.** The footer reads "© 2026 The Diff · Byrne Hobart". Substack's archive API returned nothing for this publication, so there is no count. [thediff.co/about](https://www.thediff.co/about)
- **Packy McCormick.**
  - The Substack API returned 677 posts, 2019-05-16 to 2026-11-06. 625 are free (2,652,374 words) and 52 are paid-only (246,840 words). [notboring.co](https://www.notboring.co/about)
  - Byline counts: Packy McCormick 532, Daniel McCormick 155, and single guests such as Elliot Hershberg (2), Alex Danco, Sam D'Amico and Mike Solana.
  - The footer reads "© 2026 Packy McCormick". [notboring.co/about](https://www.notboring.co/about)
- **Jason Fried / DHH.**
  - signalvnoise.com says: "Signal v. Noise is closed… With the launch of HEY World, everyone at Basecamp who was writing for SvN now has their own blog". It keeps archives for 2005–2021, which were multi-author. [signalvnoise.com](https://signalvnoise.com/)
  - DHH's HEY World feed holds his last 30 posts (2025-12-09 to 2026-10-24), mean 582 words. [world.hey.com/dhh](https://world.hey.com/dhh)
  - Jason Fried's feed holds 30 posts (2025-02 to 2026-08), mean 261 words. [world.hey.com/jason](https://world.hey.com/jason)
  - No pagination was exposed, so neither total is known.
- **Bret Victor.** 47 top-level pages; a sample of 40 gave mean 4,038 but median 1,194, with a min of 1 and a max of 60,198. Many pages are interactive, video, or reference/quote collections. [worrydream.com](https://worrydream.com/)
- **Ethan Mollick.** 141 posts from 2022-11-10 to 2026-10-20, all audience "everyone", 245,272 words; 140 carry a single byline (Mollick). The footer reads "© 2026 Ethan Mollick". [oneusefulthing.org/about](https://www.oneusefulthing.org/about)
- **Hillel Wayne.**
  - The site's /post/ index lists 40 essays (sample mean 1,763). [hillelwayne.com/post](https://www.hillelwayne.com/post/)
  - The Buttondown newsletter archive has 358 issues (sample mean 1,211, about 434k words). [buttondown.com/hillelwayne/archive](https://buttondown.com/hillelwayne/archive/)
  - The footer reads "© 2026 Hillel Wayne". [hillelwayne.com](https://www.hillelwayne.com/)
- **Charity Majors.** charity.wtf now serves a Substack ("Charity Majors | Substack") with 130 posts from 2015-12-27 to 2026-10-08. All are free, all carry her single byline, and they total 236,250 words. The old WordPress archive appears to have been imported. [charity.wtf](https://charity.wtf/)
- **Avery Pennarun.**
  - Posts use the URL pattern `/log/YYYYMMDD-slug`, and the index shows only about 5 posts with a "previous post" link, so no count was possible.
  - The page carries the disclaimer "Everything here is my opinion. I do not speak for your employer"; there is no license. [apenwarr.ca/log](https://apenwarr.ca/log/)
- **Kevin Kelly.** The Technium's WordPress API reports `X-WP-Total: 880` posts. The latest 100 posts (2024-01-15 to 2026-10-30) average 801 words, and that page includes "Weekly Links" posts. [kk.org Technium API](https://kk.org/thetechnium/wp-json/wp/v2/posts)
- **Brian Potter.**
  - 365 posts from 2020-09-27 to 2026-11-07; 252 are free (803,653 words) and 113 paid-only (296,065 words).
  - 364 carry a single byline; one is co-bylined with Austin Vernon.
  - The footer reads "© 2026 Brian Potter". [construction-physics.com/about](https://www.construction-physics.com/about)
- **Casey Handmer.** The WordPress.com API reports 379 posts from 2010-06-07 to 2026-10-23. 279 were sampled: mean 2,287, median 1,624, estimated total about 867k. The homepage blocked my fetcher, so no license check. [WordPress.com API](https://public-api.wordpress.com/wp/v2/sites/caseyhandmer.wordpress.com/posts); [caseyhandmer.wordpress.com](https://caseyhandmer.wordpress.com/)

#### Additions found (not on the original list)
- **Cory Doctorow, Pluralistic (tech policy and platforms).**
  - The WordPress API reports 1,746 posts from 2020-02-19 to 2026-11-07. 246 sampled posts gave mean 2,995 and median 2,860. [pluralistic.net API](https://pluralistic.net/wp-json/wp/v2/posts)
  - Each post states: "This work – excluding any serialized fiction – is licensed under a Creative Commons Attribution 4.0 license. That means you can use it any way you like, including commercially, provided that you attribute it to me, Cory Doctorow, and include a link to pluralistic.net… Quotations and images are not included in this license". [Pluralistic post, 7 Nov 2026](https://pluralistic.net/2026/11/07/aeiou-but-sometimes-why/)
  - Posts mix a main essay with "Hey look at this" link lists, "Object permanence" retrospective links and a repeated colophon, visible on the homepage. [pluralistic.net](https://pluralistic.net/)
- **Steven Sinofsky, Hardcore Software (Microsoft history and product lessons).** 165 posts from 2021-01-28 to 2026-09-29, all marked "everyone", single byline, 709,906 words. [hardcoresoftware.learningbyshipping.com](https://hardcoresoftware.learningbyshipping.com/)
- **Nathan Lambert, Interconnects (AI/LLM post-training).**
  - 385 posts from 2020-06-12 to 2026-11-04: 340 free (799,378 words) and 45 paid-only.
  - By type: 296 newsletter posts, 88 podcast posts and 1 restack.
  - Co-bylines appear: Florian Brand on 25, Dean W. Ball on 2, others on 1 each.
  - The footer reads "© 2026 Interconnects AI, LLC". [interconnects.ai/about](https://www.interconnects.ai/about)
- **Jeff Atwood, Coding Horror.** The Ghost sitemap lists 1,438 posts; a sample of 40 gave mean 1,080 (range 320–3,220). No site-wide content license was found. [Coding Horror sitemap](https://blog.codinghorror.com/sitemap-posts.xml)
- **Will Larson, lethain.com (engineering management).** The sitemap lists 949 URLs, and the oldest listed posts are reposts from April and June 2007. The footer reads "© Will Larson 2026". [lethain.com](https://lethain.com/)
- **Eugene Yan (ML, RecSys, LLM practice).** 182 /writing/ URLs, sample mean 1,971; the footer reads "© Eugene Yan 2015 - 2026". [eugeneyan.com](https://eugeneyan.com/)
- **Eli Bendersky.** The archive per-year counts sum to 1,330 posts, 2003 to 2026; the notice is "© 2003-2026 Eli Bendersky" and there is no CC statement. [archives/all](https://eli.thegreenplace.net/archives/all)
- **Michael Lopp, Rands in Repose (management).**
  - The footer's "© 2002-2026" is itself a link to creativecommons.org/licenses/by-nc-nd/4.0/.
  - The homepage shows "39,520 words written in the last year".
  - [randsinrepose.com](https://randsinrepose.com/)
- **Derek Sivers.** Already in the yoonholee dataset: 546 pieces / 231,786 words from sive.rs. [yoonholee dataset](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)

### Inferences
- **Clean, large and single-author:**
  - Dan Luu, Julia Evans, Paul Graham, patio11 (Kalzumeus plus Bits about Money, about 1.36M combined), Simon Willison (2017+ entries alone are about 1M), Gwern, Joel, Coding Horror, Will Larson, Casey Handmer, Sinofsky, Charity Majors, One Useful Thing, Hillel Wayne (site plus newsletter) and Eugene Yan.
  - Construction Physics, if you use only its 252 free posts.
- **Large but needing filtering:**
  - Pluralistic: strip the link roundups, colophon and quotations. My guess is that the essay portion is half or less of the 5.2M gross.
  - Not Boring: filter to Packy-only bylines and remove sponsor blocks.
  - Interconnects: drop podcast transcripts and co-bylined posts.
  - Kevin Kelly: drop "Weekly Links".
  - Bret Victor: most pages are interactive.
- **Too small for a single-author fine-tune:** Chris Olah (about 51k) and Karpathy (about 100–130k). Distill is multi-author, so drop it as a single-voice corpus.
- **Drift is a real concern for long-running blogs:**
  - Simon Willison's 2002–2003 link-blog posts differ from his 2020s long-form, as the year counts above show.
  - patio11's 2006–2010 microISV posts differ from his later finance-infrastructure essays.
  - Julia Evans' 2013 Hacker School daily notes differ from her later explainers.
  - A date filter (for example post-2015) is probably worth applying.

### Gaps
- Word counts for Joel on Software, Stratechery, The Diff, Martin Fowler, apenwarr, DHH's full HEY World archive and Eli Bendersky's full archive could not be measured. Blocks (403/429), API failures and JS-only or unpaginated archives prevented it.
  - My unmeasured guess for Joel: 1,114 posts × 600–1,200 words ≈ 0.7–1.3M.
  - My unmeasured guess for Stratechery Articles: 600+ × 2–3.5k ≈ 1.2–2M.
  - Both are speculative, not measured.
- Steve Yegge's Drunken Blog Rants (sites.google.com, 2004–2006) and his Medium posts (2018+) were not counted.
- Kevin Kelly's older Technium posts (pre-2024) were not measured, so the ~0.7M figure assumes the latest-100 average holds.
- I did not verify whether Bits about Money has any paywalled essays.
- Prose-only fraction (excluding code, math, quotes and references) was not measured per author.

## Q2. Which have an explicit open license (CC0, CC-BY, CC-BY-SA) that makes corpus building clean?

### Takeaway
Only two sizeable single-author tech corpora carry explicit, permissive, commercial-use-OK licenses verified on the site itself: **Gwern (CC-0)** and **Cory Doctorow's Pluralistic (CC BY 4.0, excluding serialized fiction, quotations and images)**. Distill is CC BY 4.0 but multi-author. A few others use non-commercial or no-derivatives CC licenses: Kevin Kelly (conflicting signals), Rands (BY-NC-ND), Jay Alammar (BY-NC-SA) and Michael Nielsen's book (BY-NC). Everyone else on the list shows only a © notice or no statement at all.

### Cited Findings
- Gwern: "This site is licensed under the Creative Commons public domain (CC-0) license", with a link to creativecommons.org/public-domain/cc0/. [gwern.net/about](https://gwern.net/about)
- Pluralistic: "This work – excluding any serialized fiction – is licensed under a Creative Commons Attribution 4.0 license… you can use it any way you like, including commercially, provided that you attribute it to me, Cory Doctorow, and include a link to pluralistic.net… Quotations and images are not included in this license". [Pluralistic post](https://pluralistic.net/2026/11/07/aeiou-but-sometimes-why/)
- Distill: "Diagrams and text are licensed under Creative Commons Attribution CC-BY 4.0… unless noted otherwise. The figures that have been reused from other sources don't fall under this license". [distill.pub](https://distill.pub/2020/circuits/zoom-in/)
- Kevin Kelly gives two different signals:
  - The Technium sidebar has a link labelled "Creative Commons" pointing to CC BY-NC-SA 3.0. [kk.org/thetechnium](https://kk.org/thetechnium/)
  - The kk.org footer has a CC icon linking to CC BY 4.0. [kk.org](https://kk.org/)
  - There is no explanatory license text, and the two conflict.
- Rands in Repose: the footer "© 2002-2026" links to CC BY-NC-ND 4.0. [randsinrepose.com](https://randsinrepose.com/)
- Jay Alammar: "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License". [jalammar.github.io](https://jalammar.github.io/)
- Michael Nielsen's *Neural Networks and Deep Learning*: "licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License… free to copy, share, and build on this book, but not to sell it". [neuralnetworksanddeeplearning.com](http://neuralnetworksanddeeplearning.com/)
- **© notice only, no license:**
  - Paul Graham ("© mmxxvi pg") [paulgraham.com](https://paulgraham.com/index.html)
  - Patrick McKenzie / Kalzumeus Software LLC [kalzumeus.com/about](https://www.kalzumeus.com/about/); [bitsaboutmoney.com](https://www.bitsaboutmoney.com/)
  - Julia Evans [jvns.ca](https://jvns.ca/)
  - Simon Willison [simonwillison.net](https://simonwillison.net/)
  - Lilian Weng [lilianweng.github.io](https://lilianweng.github.io/)
  - Martin Fowler [martinfowler.com](https://martinfowler.com/)
  - Stratechery LLC [stratechery.com/category/articles](https://stratechery.com/category/articles/)
  - The Diff [thediff.co/about](https://www.thediff.co/about)
  - Packy McCormick [notboring.co/about](https://www.notboring.co/about)
  - Ethan Mollick [oneusefulthing.org/about](https://www.oneusefulthing.org/about)
  - Hillel Wayne [hillelwayne.com](https://www.hillelwayne.com/)
  - Brian Potter [construction-physics.com/about](https://www.construction-physics.com/about)
  - Will Larson [lethain.com](https://lethain.com/)
  - Eugene Yan [eugeneyan.com](https://eugeneyan.com/)
  - Eli Bendersky [eli.thegreenplace.net](https://eli.thegreenplace.net/)
  - Interconnects AI LLC [interconnects.ai/about](https://www.interconnects.ai/about)
- **No statement found:**
  - Dan Luu [danluu.com](https://danluu.com/)
  - Joel on Software [archives](https://www.joelonsoftware.com/archives/)
  - Steve Yegge [blogspot](https://steve-yegge.blogspot.com/)
  - idlewords [idlewords.com](https://idlewords.com/)
  - Karpathy [karpathy.github.io](https://karpathy.github.io/)
  - colah [colah.github.io](https://colah.github.io/)
  - Bret Victor [worrydream.com](https://worrydream.com/)
  - apenwarr [apenwarr.ca/log](https://apenwarr.ca/log/)
  - DHH / Jason Fried on HEY World [world.hey.com/dhh](https://world.hey.com/dhh)
- Several existing PG datasets on Hugging Face carry licenses the uploaders had no right to grant. sgoel9/paul_graham_essays is tagged `license:mit` [HF](https://huggingface.co/datasets/sgoel9/paul_graham_essays), pookie3000/paul_graham_all_essays `apache-2.0` [HF](https://huggingface.co/datasets/pookie3000/paul_graham_all_essays), and lance-bundle/paul-graham-essays `mit` [HF](https://huggingface.co/datasets/lance-bundle/paul-graham-essays). The yoonholee style-eval card instead says non-CC authors are included as "publicly posted writing, research use under fair use". [yoonholee dataset](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)

### Inferences
- **For a commercial product:**
  - Gwern (CC-0, no attribution needed) and Pluralistic (CC BY 4.0, attribution plus link) are the only clean large options.
  - For Pluralistic, the license explicitly excludes quotations, images and serialized fiction, so the corpus builder should strip quoted blocks and fiction serials. That also improves style purity.
- **Non-commercial or no-derivatives terms (Rands BY-NC-ND, Alammar BY-NC-SA, Nielsen BY-NC, possibly Kevin Kelly BY-NC-SA):**
  - These restrict commercial use. ND may also bar derivative works, and whether a fine-tuned model or its outputs count as an adaptation is legally unsettled (my inference, not legal advice).
  - Kevin Kelly's conflicting BY-NC-SA 3.0 and BY 4.0 links should be clarified with him before relying on either.
- **Everyone else is all-rights-reserved by default:**
  - Using their text for training depends on fair-use arguments or permission.
  - Paywalled Substack and Stratechery content adds a Terms-of-Service problem on top of copyright.

### Gaps
- I did not read the full Terms of Service for Stratechery, Substack or HEY World regarding scraping and AI training.
- I did not check Casey Handmer's, Steve Blank's or Derek Sivers' sites for license statements; the fetches failed or were out of time.
- I did not verify whether Distill's per-article "unless noted otherwise" exceptions affect text.

## Q3. Which voices are most distinctive and most transferable to everyday informational writing (memos, explainers, docs)?

### Takeaway
My assessment, from familiarity with these writers' work rather than measured stylometry:
- **Most distinctive and most transferable to memos, explainers and how-tos:** Joel Spolsky, Paul Graham, Patrick McKenzie, Julia Evans, Jeff Atwood, Charity Majors and Maciej Cegłowski.
- **Distinctive but niche or hard to transfer:** Gwern, Doctorow, Yegge and Bret Victor.
- **Large and clean but close to neutral explainer prose, nearer "LLM voice":** Lilian Weng, Will Larson, Eugene Yan, Construction Physics and Eli Bendersky.

### Cited Findings
- **Published analyses of Paul Graham's style:**
  - One says his sentences link like "a silver chain" and that he breaks each point down to its smallest, most precise form. [Sasha Chapin](https://sashachapin.substack.com/p/paul-graham-isnt-a-simple-writer); [The Common Reader](https://www.commonreader.co.uk/p/paul-grahams-plain-rhetoric) (as summarized in search results; not read in full)
  - A style guide for his X posts describes "plain-English compression, observation-then-implication structure, founder-as-protagonist framing". [autotweet.io](https://www.autotweet.io/creators/paul-graham-style)
- **Register labels used by the yoonholee style-eval corpus:** PG "Contrarian startup essays"; Karpathy "Tutorial-as-thinking-aloud"; Gwern "Quantitative empiricist"; Cegłowski "Sardonic literary tech critic"; Joel "Narrative tech management"; Sivers "Zen-minimalist aphorisms". [yoonholee dataset](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)
- **Post-length profiles (from Q1):**
  - Dan Luu: median 4,155 words. Lilian Weng: median 5,362. Both write long-form.
  - Julia Evans: median 928. Coding Horror: median 926. Hillel's newsletter: median 1,155. These are short-to-mid form, closer to memo length.
  - Sources: [danluu.com](https://danluu.com/), [lilianweng.github.io](https://lilianweng.github.io/), [jvns.ca](https://jvns.ca/sitemap.xml), [Coding Horror](https://blog.codinghorror.com/sitemap-posts.xml)
- Martin Fowler published a bliki entry titled "LLM-Voice" on 29 Oct 2026, a sign that "LLM voice" is now a named concern among tech writers. I did not read its content. [martinfowler.com/bliki](https://martinfowler.com/bliki/)

### Inferences
The style signatures below are my assessment from prior reading, not stylometric measurement. They should be spot-checked against samples. "LLM distance" means how far the voice is from generic assistant prose.

| Author | Style signature (3–5 markers) | Distance from LLM voice | Transfer to memos/docs | Consistency |
|---|---|---|---|---|
| Paul Graham | Short declarative sentences; plain Anglo-Saxon words; argument built from a surprising claim plus everyday analogies; frequent "you"; few headers; ends with "Notes" and a thanks line | High in rhythm, but his surface tics are heavily imitated | High for essays and memos; low for step-by-step docs | Very consistent across 2001–2026; acknowledges draft readers in thanks lines |
| Patrick McKenzie | Very long, digressive sentences with parentheticals; insider detail; dry wit; "Bits about Money" financial-plumbing explainers; footnotes | High | High for analyses and explainers of systems | Drift: microISV diary (2006–10) → long-form finance/infra essays |
| Dan Luu | Long data-heavy essays; lists of examples; frequent footnotes and appendices; deadpan; contrarian empiricism | High | Medium-high for analyses; posts are very long | Consistent; heavy quoting of others in some posts |
| Julia Evans | Short sentences; first person; enthusiasm ("I learned…"); questions; numbered steps; friendly second person; tiny examples | High (warm, unpolished) | Very high for how-tos, docs and explainers | Drift from 2013 daily notes to polished explainers |
| Simon Willison | Plain conversational; "Here's how I…"; heavy quoting and linking; code snippets; TIL-style notes; caveats | Medium (clear, plain, quote-heavy) | High for technical posts and docs | Two eras (2002–03 link blog vs 2020s long-form); since 2023 contains quoted LLM output (contamination risk) |
| Gwern | Dense, hedged; epistemic-status metadata; sidenotes; statistics; rare vocabulary; enormous footnotes | Very high | Low (niche, dense) | Single author, but pages are continuously revised; heavy quotation |
| Joel Spolsky | Funny anecdotes; strong opinions; second person; numbered tests and lists; cartoonish analogies; management narratives | High | Very high for memos and management/product writing | Consistent, but mostly 2000–2010 references (dated tech) |
| Steve Yegge | Very long rants; digressions; self-deprecating humour; profanity; story-first | Very high | Low-medium (form too rambling) | Spread across 3+ platforms and eras |
| Maciej Cegłowski | Sardonic aphorisms; vivid analogies; literary cadence; talk-transcript structure | Very high | Medium (persuasive essays and talks; less for docs) | Consistent but sparse after ~2019 |
| Karpathy | Tutorial thinking aloud; enthusiasm; code-first; first person | Medium-high | Medium for technical explainers | Consistent, but corpus small |
| Lilian Weng | Survey/textbook; neutral; dense headings, citations and math | Low (closest to neutral academic/LLM survey prose) | Medium for technical docs; little narrative flair | Very consistent |
| Martin Fowler | Measured, definitional; pattern names; short bliki entries | Medium | High for docs and engineering explainers | Site mixes his and colleagues' articles (needs filtering) |
| Ben Thompson | Framework-driven (Aggregation Theory); recurring self-citation; long structured analysis; first person | Medium-high (signature concepts) | Medium-high for business analysis memos | Very consistent; best material paywalled |
| Byrne Hobart | Dense, allusive, finance plus tech; long sentences; many asides | High | Medium | Unmeasured |
| Packy McCormick | Casual, hype-y, memes and pop culture; long deep dives | Medium-high | Medium | Mixed bylines and sponsor segments |
| DHH | Combative, punchy, short posts | High | Medium (opinion memos) | Single author on HEY; SvN multi-author |
| Ethan Mollick | Accessible AI explainers; concrete examples; second person; prompts shown | Medium | High for AI-related explainers, but topic-locked | Single author; posts embed AI-generated examples (contamination risk) |
| Hillel Wayne | Nerdy humour; formal-methods and history-of-SE topics; crisp; footnotes | High | Medium-high | Consistent |
| Charity Majors | Profane, energetic, opinionated; management and observability; lists | Very high | High for opinion memos; profanity may need filtering | Single author |
| Kevin Kelly | Aphoristic, optimistic, big-picture; short posts | Medium-high | Medium | Includes link-roundup posts |
| Brian Potter | Analytical, chart-heavy, historical, sober | Low-medium | High for analyses; little humour | Consistent, single byline |
| Casey Handmer | Engineering back-of-envelope; contrarian; long technical arguments | Medium-high | Medium | Single author 2010–2026 |
| Cory Doctorow | Polemical; coined terms ("enshittification"); long cumulative sentences; links-as-evidence | Very high | Low-medium (very recognizable, polemical) | Single author, but templated post structure |
| Steven Sinofsky | Insider memoir plus product lessons; long narrative; first person | Medium-high | High for product/strategy memos with storytelling | Single author |
| Jeff Atwood | Punchy, humorous, quotes, pop culture, strong opinions | High | High for developer explainers and opinion posts | Consistent |
| Will Larson / Eugene Yan / Eli Bendersky | Structured, clear headers, frameworks and tutorials | Low-medium | High for docs, but weak voice signal | Consistent |

- **Best overall fits** (distinctive, informational with narrative, large and single-author): Joel Spolsky, Patrick McKenzie, Julia Evans, Jeff Atwood, Paul Graham and Charity Majors.
- **Best fit if a clean license is mandatory:** Gwern (CC-0). The voice is highly distinctive but less transferable to everyday memos. Pluralistic (CC BY 4.0) is highly distinctive and polemical.
- **Voices near neutral explainer prose** (Lilian Weng, Larson, Yan, Bendersky, Potter): a fine-tune would mostly teach topic and structure, not voice. That makes them poor targets if the goal is distance from generic LLM output.

### Gaps
- No quantitative stylometry (sentence-length distributions, second-person rate, type-token ratio) was computed in this session.
- I found no rigorous source comparing how far each author sits from LLM output. A search for Hacker News style discussions of Dan Luu returned nothing specific. [search results incl. simonwillison.net/tags/dan-luu](https://simonwillison.net/tags/dan-luu/)

## Q4. Are any already popular as LLM style fine-tuning targets? Do frontier LLMs already imitate them well from prompting alone?

### Takeaway
Paul Graham is by far the most-scraped and most-imitated author: more than 15 Hugging Face datasets, a 990-star Markdown export, a 2.6k-star RAG repo, multiple "write like Paul Graham" GPTs and skills, and at least one SFT dataset of PG excerpts. A CC0 style-eval corpus already bundles PG, Karpathy, Gwern, Cegłowski, Joel Spolsky and Derek Sivers. I found no Hugging Face datasets for the other candidates, apart from synthetic QA built from Lilian Weng's blog. Anecdotal reports say prompt-only imitation of PG drifts toward generic "LinkedIn post" prose; I found no rigorous evaluation.

### Cited Findings
- **Hugging Face search for "paul graham"** returned:
  - baber/paul_graham_essays, 27,873 downloads, the most-downloaded [HF](https://huggingface.co/datasets/baber/paul_graham_essays)
  - sgoel9/paul_graham_essays, 1,215 downloads; card calls it "a complete collection of essays" [HF](https://huggingface.co/datasets/sgoel9/paul_graham_essays)
  - Mindofmachine/paul_graham_and_sam_altman_articles, 398 [HF](https://huggingface.co/datasets/Mindofmachine/paul_graham_and_sam_altman_articles)
  - alessiodevoto/paul_graham_essays, 199 [HF](https://huggingface.co/datasets/alessiodevoto/paul_graham_essays)
  - LangChainDatasets/question-answering-paul-graham, 104 [HF](https://huggingface.co/datasets/LangChainDatasets/question-answering-paul-graham)
  - pingzhili/PaulGrahamEssays, 69 [HF](https://huggingface.co/datasets/pingzhili/PaulGrahamEssays)
  - emozilla/PaulGrahamEssays, 49 rows [HF](https://huggingface.co/datasets/emozilla/PaulGrahamEssays)
  - pookie3000/paul_graham_all_essays [HF](https://huggingface.co/datasets/pookie3000/paul_graham_all_essays)
  - pookie3000/pg_essays_split_1000_t [HF](https://huggingface.co/datasets/pookie3000/pg_essays_split_1000_t)
  - chromadb/paul_graham_essay [HF](https://huggingface.co/datasets/chromadb/paul_graham_essay)
  - RNDRandoM/paul-graham-essays-qa [HF](https://huggingface.co/datasets/RNDRandoM/paul-graham-essays-qa)
  - arthurmello/paul-graham-essays [HF](https://huggingface.co/datasets/arthurmello/paul-graham-essays)
  - lance-bundle/paul-graham-essays, Aug 2026 [HF](https://huggingface.co/datasets/lance-bundle/paul-graham-essays)
  - Download counts are as returned by the HF API on 7 Nov 2026.
- **matthewagi/paul-graham-original-assistant-sft-qwen3-0.6b (Jul 2026)** is an explicit style-SFT dataset: "Each row has an empty prompt and a Paul Graham original excerpt as the assistant completion", 215 rows, derived from "matthewagi/paul-graham-summary-rewrite-qwen3-8b". [HF](https://huggingface.co/datasets/matthewagi/paul-graham-original-assistant-sft-qwen3-0.6b)
- **yoonholee/style-eval-pg-karpathy-gwern (CC0 curation, Apr 2026)**:
  - Covers 11 writers "with instantly recognizable but distinct styles", built "for style-as-reward-inference experiments".
  - Contents: PG (229 pieces / 562,990 words), Karpathy (34 / 101,337), Gwern (220 / 2,800,357), Cegłowski (353 / 524,614), Joel Spolsky (209 / 123,984), Derek Sivers (546 / 231,786), plus Scott Alexander, Naval, Yudkowsky, dril and Trump.
  - Schema: author, title, url, text (markdown) and word_count.
  - [HF](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)
- **Lilian Weng:** only synthetic QA derivatives exist, such as creaoai/lilianweng_blog_url_synthetic_data_extractive and _abstractive (Aug 2024). These are not style corpora. [HF](https://huggingface.co/datasets/creaoai/lilianweng_blog_url_synthetic_data_extractive)
- **No other authors:** HF searches for patio11, kalzumeus, danluu, julia evans, jvns, simon willison, spolsky, yegge, idlewords, karpathy blog, colah, martin fowler, stratechery, byrne hobart, not boring, signal v noise, bret victor, mollick, hillel, charity majors, apenwarr, kevin kelly, construction physics, handmer, doctorow and codinghorror returned no author datasets. [HF dataset search API](https://huggingface.co/api/datasets?search=stratechery)
- **GitHub:**
  - ofou/graham-essays (990 stars; "Download the full collection of Paul Graham essays in EPUB, PDF & Markdown") [GitHub](https://github.com/ofou/graham-essays)
  - mckaywrigley/paul-graham-gpt (2,662 stars; RAG) [GitHub](https://github.com/mckaywrigley/paul-graham-gpt)
  - evmn/Paul-Graham (175 stars, Kindle) [GitHub](https://github.com/evmn/Paul-Graham)
  - gwern/gwern.net (848 stars, site infrastructure) [GitHub](https://github.com/gwern/gwern.net)
  - lilianweng/lilianweng.github.io (778 stars, site source) [GitHub](https://github.com/lilianweng/lilianweng.github.io)
  - Stratechery crawler and chatbot repos (see Q1)
  - tamnd/joelonsoftware-cli and tamnd/lilianweng-cli (readers) [GitHub](https://github.com/tamnd/joelonsoftware-cli)
- **Prompt-based PG imitation is a product category:**
  - A "Write like Paul Graham" GPT [theresanaiforthat](https://theresanaiforthat.com/gpt/write-like-paul-graham/?term=write)
  - Claude skills such as "pg" [claudskills.com](https://claudskills.com/skills/pg/) and "pg-writer" by jaredpalmer, which reportedly runs a script to check output against PG's measured habits [skills.rest](https://skills.rest/skill/pg-writer-jaredpalmer)
  - The WWPGW experiment ("What would Paul Graham write?"), which feeds reference essays to an LLM [GitHub README](https://raw.githubusercontent.com/GeorgeStrakhov/wwpgw/main/README.md)
- **Anecdotal failure report:** one developer who built a PG persona said the output read like a LinkedIn post, with the wrong rhythm and framing. This comes from the search summary; I did not read the page in full. [dev.to](https://dev.to/tedtalk/i-gave-paul-grahams-essays-to-an-ai-and-stress-tested-it-for-2-hours-heres-what-broke-it-1om)

### Inferences
- **PG is "overfished".** Frontier models have certainly seen his essays many times. As prior knowledge, not verified this session: PG essays are also the default "haystack" in Greg Kamradt's needle-in-a-haystack long-context test and the default sample document in LlamaIndex tutorials.
  - A PG fine-tune is therefore the least differentiated choice.
  - Prompting already gets surface tics (short sentences, "you", contrarian openers) but reportedly misses rhythm.
  - That makes PG a good **baseline or benchmark author**, not a differentiating one.
- **Less-exploited, distinctive, large single-author corpora** (no HF datasets found): Joel Spolsky (only partially scraped in yoonholee), Patrick McKenzie, Julia Evans, Dan Luu, Jeff Atwood, Charity Majors, Simon Willison (export is trivial via his public Datasette) and Sinofsky.
- **The yoonholee corpus** is a ready-made multi-author eval set. Its PG/Gwern/Cegłowski/Joel splits could serve as held-out style-classifier training data for evaluating a fine-tuned model.

### Gaps
- I found no rigorous study measuring how well frontier models imitate any of these authors from prompting alone, versus fine-tuning. The evidence here is anecdotal blog posts and tool listings.
- I did not inspect the contents or quality of each PG HF dataset (deduplication, completeness, footnote handling), beyond row counts and cards.
- GitHub search covered repo names and descriptions only, not code search. Scrapes embedded inside larger repos would be missed.
