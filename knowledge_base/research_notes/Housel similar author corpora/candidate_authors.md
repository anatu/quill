# Housel-similar author corpora: candidate authors (access, size, legal facts)

Research date: 2026-11-08. Scope: authors and corpora stylistically close to Morgan Housel that could serve as auxiliary QLoRA training text. Style similarity is not measured here. A separate agent is embedding-scoring the seed list. Everything below about "why it resembles Housel" is either a cited link (Housel's own words, a shared publisher or blog, interviews) or is marked as an inference.

**Methods used throughout (so the report writer can state them):**
- **robots.txt:** fetched directly on 2026-11-08 with a generic client string (`research-client/1.0`). I grepped each file for GPTBot, ClaudeBot, Claude-Web, anthropic-ai, CCBot, Google-Extended, Bytespider, PerplexityBot, Applebot-Extended, meta-externalagent, cohere-ai and Cloudflare `Content-Signal` lines.
- **Homepage checks:** each homepage was grepped for `noai`/`noimageai` meta tags and for platform fingerprints (substackcdn, wp-content, Webflow, Wix, Posthaven, Kit/ConvertKit). I also requested `/ai.txt` and `/llms.txt`. No `noai` meta tag was found on any homepage checked. `/ai.txt` returned 404 everywhere except oliverburkeman.com, which returned 400. `/llms.txt` exists only on oliverburkeman.com (Wix).
- **Post counts:** taken from the WordPress REST `X-WP-Total` header (`/wp-json/wp/v2/posts?per_page=1`) where the site exposes it, otherwise from the number of `<loc>` URLs in post sitemaps. Sitemap counts can include non-post pages.
- **Words per post:** mean word count inside `<p>` elements over n=4 post URLs drawn at random (seed 42) from one post sitemap. This is crude. It includes comment text on sites that render comments in `<p>` (it clearly inflates JL Collins, HumbleDollar and probably Cal Newport), so treat those figures as upper bounds. Estimated words = posts × mean, with roughly ±50% error.
- **Public-domain books:** HEAD request only (no download) for the Project Gutenberg plain-text file's Content-Length, words ≈ bytes ÷ 6. The figure includes about 3k words of PG licence boilerplate.
- **Not done:** no bulk downloads. When timharford.com refused the generic client (connection failure), I did not retry with a spoofed browser user-agent. Its robots.txt was read via a normal fetch tool instead.

## Q1. Which writers are documented as Housel-like, name Housel as an influence, or are named alongside him (Collab Fund, Ritholtz Wealth, finance-Twitter essay cluster, reviewers)?

### Takeaway
Reviewer-made comparisons between Housel and named writers are scarce. Search found no review that ranks him against specific stylists. The strongest documented links run the other way: writers Housel himself names (Munger, Maggiulli, James Clear, Naval, Taleb, Erik Larson), people who publish on his own Collab Fund blog (Ted Lamade), and his publisher and podcast circle (Jonathan Clements via Harriman House, Jack Raines via Ritholtz's podcast). The best non-seed finance candidates by fit and access are Ted Lamade, Jason Zweig, Jonathan Clements, Joe Wiggins, Jack Raines and Cullen Roche. Patrick O'Shaughnessy and William Bernstein are close in topic but are "permission only".

### Cited Findings

**Housel's own named influences and admired writers (David Perell's "How I Write" interview):**
- Housel says he "shamelessly stole" the title format of *The Psychology of Money* from Charlie Munger's speech "The Psychology of Human Misjudgment" — [How I Write: Morgan Housel](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- He praises Erik Larson (transcribed as "Eric Larson"): Larson "can tell in a page and a half what would take other historians 17 pages." He also praises Doris Kearns Goodwin's *No Ordinary Time* ("not a single word can be stripped from that book"), Robert Caro, Ken Burns and Mark Twain — [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- He says of Yuval Noah Harari and Nassim Taleb, "They said it really well." He calls Nick Maggiulli a writer who was "talented from day one". Of James Clear's *Atomic Habits* he says, "after three pages, you can't stop reading that book." He relays Naval Ravikant's advice to paraphrase rather than quote — [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- On his own process: "I write truly one sentence at a time." He also praises The Economist's prose as "very, very well written" — [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- A podcast summary says Housel was shaped by Frederick Lewis Allen's popular histories of American life. This comes from a low-quality aggregator and is unverified — [podwise.ai summary](https://podwise.ai/dashboard/episodes/54384)

**Collab Fund colleagues:**
- The Collab Fund blog currently shows these authors: Craig Shapiro, Ted Lamade, Andrew Montgomery, Morgan Housel, Amanda Amos and Hamza Choudery. Most non-Housel posts are firm announcements, for example "Welcoming Jason Spinell" (Nov 5, 2026) and "Why we're investing in Dr. Max's" — [Collab Fund blog](https://collabfund.com/blog/)
- **Ted Lamade** (managing director at the Carnegie Institution for Science, going by the URL slug) has 34 essays on Collab Fund from Aug 24, 2021 to Oct 30, 2026. Titles are life-lesson and history essays in Housel's register: "Read Old Books", "Fear of Acorns", "The Cost of Comfort", "Significance > Success", "Safer, Yet More Afraid Than Ever", "The Tide Is Going Out" — [Ted Lamade author page](https://collabfund.com/blog/authors/ted-lamade-managing-director-at-the-carnegie-institution-for-science/)
- My sample of 3 Lamade posts gave 1,229, 1,613 and 2,275 words, at 30–46 words per paragraph. That puts the whole corpus at about 58k words — measured from [collabfund.com/blog/significance-success/](https://collabfund.com/blog/significance-success/), [the-power-of-constraints](https://collabfund.com/blog/the-power-of-constraints/) and [read-old-books](https://collabfund.com/blog/read-old-books/)
- collabfund.com has no robots.txt (a 404 page is returned). The site runs on Jekyll and GitHub Pages (server `GitHub.com`, generator `Jekyll v4.3.4`) — [collabfund.com/robots.txt](https://collabfund.com/robots.txt)

**Publisher, podcast and finance-cluster links:**
- **Jonathan Clements** (ex-WSJ columnist, HumbleDollar founder). Harriman House, which published *The Psychology of Money*, published his *Money and Me*, a collection of HumbleDollar articles — [Harriman House](https://harriman-house.com/authors/jonathan-clements/money-and-me/9781804093764); for Housel's Harriman House link see [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- Clements died on September 21, 2025, after a lung-cancer diagnosis in May 2024 — [NJCFE](https://njcfe.org/?p=7965); [AARP](https://www.aarp.org/money/personal-finance/cancer-changed-retirement-plan/)
- HumbleDollar is a multi-author WordPress site with 3,812 posts since 2014-11-20, so Clements's own share must be filtered by author. Posts per year: 2019=349, 2020=378, 2021=665, 2022=669, 2023=574, 2024=426, 2025=113, 2026=92 — [humbledollar.com WP REST](https://humbledollar.com/wp-json/wp/v2/posts)
- **Jack Raines** (Young Money): Barry Ritholtz interviewed him on *Masters in Business* in Aug 2026 — [ritholtz.com](https://ritholtz.com/2026/08/mib-jack-raines/). His book *Young Money: A Field Guide to Wealth and Purpose in Your Twenties* is published by Penguin Random House — [PRH](https://www.penguinrandomhouse.com/books/786678/young-money-by-jack-raines/9798217336913/). He started the newsletter in July 2021 and is known for satirical "hustle-culture" LinkedIn posts — [Poets&Quants](https://poetsandquants.com/2026/08/18/how-jack-rainess-linkedin-fame-built-mocking-grind-culture-at-his-columbia-mba-turned-into-a-book-deal/). I found no source in which Raines names Housel as an influence.
- **Jamie Catherwood** (Investor Amnesia) writes on financial history (manias, bubbles, railway booms), sends a Sunday financial-history newsletter and works at O'Shaughnessy Asset Management — [Alex Danco interview](https://alexdanco.com/2019/11/07/an-interview-with-jamie-catherwood/); [Bogle Center](https://boglecenter.net/2021/02/25/march-podcast-guest-jamie-catherwood/)
- **Barry Ritholtz** (founder of Ritholtz Wealth Management, employer of seeds Carlson, Batnick and Brown) runs ritholtz.com. Its sitemap index has 78 post sitemaps dating from 2002-09-18. The 40 sitemaps I counted held 40,001 URLs, so the full archive is probably more than 70k posts, much of it link lists and charts — [ritholtz.com/sitemap.xml](https://ritholtz.com/sitemap.xml)

**Reviewers' comparisons (weak):**
- Shortform says *The Psychology of Money* differs from typical finance books in having almost no equations or tactics, and attributes Housel's style to a journalism background — [Shortform](https://www.shortform.com/blog/?p=59731)
- Reviews of *Same as Ever* describe "short, almost essayistic" chapters, each orbiting one insight, with anecdotes from history and psychology — [Bobby Powers](https://bobbypowers.net/review-same-as-ever); [Literary Yard](https://literaryyard.com/2025/04/07/book-review-same-as-ever-by-morgan-housel/)
- A Goodreads reviewer says *Same as Ever* largely summarises ideas from Taleb (*Antifragile*, *Skin in the Game*). That is a comparison of content, not of style — [Goodreads](https://www.goodreads.com/book/show/218312269)

### Inferences
- Ted Lamade is probably the closest non-seed match available. He publishes on the same blog with the same editorial framing, and his titles follow the Housel pattern of a historical vignette leading to a single lesson. The catch is size: about 58k words would be roughly 17% of Housel's 342k, so it fits as a small, low-dilution add-on.
- Jason Zweig is the most "journalist-voiced" finance writer in the cluster. The WSJ column origin of many posts raises a rights question (see Q5).
- Jonathan Clements shares Housel's UK publisher and his plain, life-lessons register, but the HumbleDollar corpus is mostly other contributors and must be filtered by author.

### Gaps
- I found no professional review (FT, WSJ, Kirkus, Publishers Weekly) that names a stylistic peer of Housel's. Search surfaced only blog reviews and summary sites.
- I could not confirm whether any Ritholtz Wealth employees beyond Ritholtz and the seeds (for example Callie Cox or Blair duQuesnay) keep a personal blog. I did not search further.
- The Frederick Lewis Allen influence comes from an aggregator summary only.

## Q2. Which aphoristic generalist essayists match his cadence (short paragraphs, anecdote then principle)?

### Takeaway
The best generalist matches are Ryan Holiday and Daily Stoic (history anecdote leading to a lesson, in short paragraphs), Tim Harford (one economic anecdote, then a principle), Eric Barker, Naval Ravikant (aphorisms, small corpus), Cal Newport, Mark Manson, Ozan Varol and Fred Wilson (AVC). All of these sites have robots.txt files with no AI-bot rules. The biggest risks are team-written or high-volume output (Daily Stoic, Sahil Bloom) and quote-heavy posts (early Barking Up the Wrong Tree).

### Cited Findings
- **Ryan Holiday (ryanholiday.net):** about 936 post URLs in the post sitemap, lastmod from 2007-01-31 to 2026-11-04. A sample of 4 posts gave 1,751, 960, 776 and 1,449 words (mean about 1,234), for an estimate of about 1.15M words. robots.txt is `User-agent: * Disallow:` with no AI rules. The REST API needs a login (401) — [robots](https://ryanholiday.net/robots.txt); [sitemap](https://ryanholiday.net/sitemap_index.xml)
- **Daily Stoic (dailystoic.com):** about 3,584 URLs across 4 post sitemaps, 2016-07-17 to 2026-11-07. A sample of 4 posts gave 245–306 words (mean 273), for an estimate of about 1.0M words. It runs on WordPress with no AI rules — [robots](https://dailystoic.com/robots.txt). A ConvertKit case study describes the email as about 500 words "hand-delivered by Holiday every single day" — [ConvertKit case study](https://convertkit.com/resources/blog/daily-stoic-case-study). Some posts are interviews (for example "lori-gottlieb-on-…").
- **Tim Harford (timharford.com):** WordPress. robots.txt reads `User-agent: * / Disallow: /wp-admin/` with no AI rules, and the site has 3 child sitemaps, all read through a normal fetch — [robots](https://www.timharford.com/robots.txt); [sitemap-index-1](https://timharford.com/sitemap-index-1.xml). The site refused connections from my generic command-line client, both the homepage and the REST API, so post count and word count were not measured.
- **Eric Barker, Barking Up the Wrong Tree (bakadesuyo.com):** 5,591 posts since 2009-07-04, at 11–34 posts a year from 2019 to 2026. A sample of 4 posts gave 178, 497, 3,154 and 4,680 words: early posts are short research excerpts, later ones are long essays. Estimate: several million words. WordPress, no AI rules — [robots](https://bakadesuyo.com/robots.txt); [WP REST](https://bakadesuyo.com/wp-json/wp/v2/posts)
- **Naval Ravikant (nav.al):** 240 posts since 2005-11-29. Sampled posts ran 62–543 words (mean 331), for about 80k words. Output by year: 2019=56, 2020=21, 2021=59, 2022=2, 2023=2, 2024=4, 2025=17, 2026=9. robots.txt is `User-agent: * Disallow:` — [robots](https://nav.al/robots.txt); [WP REST](https://nav.al/wp-json/wp/v2/posts)
- **Cal Newport (calnewport.com):** 1,130 posts since 2007-07-20. Samples ran 2,114–3,698 words, probably inflated by comments, so the corpus is about 1.1–3.5M words. Output by year: 2019=44 … 2024=17, 2025=35, 2026=34. robots.txt is `User-agent: * Disallow:` — [robots](https://calnewport.com/robots.txt)
- **Mark Manson (markmanson.net):** 283 posts since 2010-08-09. Samples ran 1,444–4,169 words (mean about 3,000), for about 0.85M words. Output by year: 2019=26, 2020=44, 2021=38, 2022=11, 2023=23, 2024=4, 2025=4, 2026=0. No AI rules — [robots](https://markmanson.net/robots.txt). The register is profane and casual, which is a style mismatch.
- **Fred Wilson, AVC (avc.com):** about 9,046 post URLs from 2003-09-23 to 2024-05-02. Recent posts ran 161–508 words (mean about 311), for about 2.8M words. The final post is "I've moved onchain" (May 2024). robots.txt has no AI rules — [robots](https://avc.com/robots.txt); [sitemap](https://avc.com/sitemap_index.xml)
- **Ozan Varol (ozanvarol.com):** over HTTPS, robots.txt returned a WordPress 500 error page. The http/www variant serves a Yoast block, `User-agent: * Disallow:`, with Crawl-delay 10. The sitemap returned 500, so the post count is unknown — [robots](https://www.ozanvarol.com/robots.txt)
- **Oliver Burkeman (oliverburkeman.com):** a Wix site with only 33 sitemap pages. It serves an `/llms.txt` and has no AI rules in robots — [robots](https://oliverburkeman.com/robots.txt). His essay corpus (*The Imperfectionist* newsletter) is hosted elsewhere and I did not check it.
- **David Perell (perell.com):** only 67 sitemap URLs. robots.txt is `User-agent: * Disallow:` — [robots](https://perell.com/robots.txt). He is linked to Housel because he hosted the "How I Write" interview — [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- **Sam Altman (blog.samaltman.com):** hosted on Posthaven. robots.txt disallows only `/posthaven/` and `/private/` — [robots](https://blog.samaltman.com/robots.txt). Post count was not measured.
- **Sahil Bloom (sahilbloom.com):** built on Webflow with Kit (ConvertKit) for email. robots.txt contains only a Sitemap line and no rules. There are 591 sitemap URLs, 522 of them under `/newsletter/`, with lastmod 2024-07-12 to 2026-10-29. Samples ran 1,197–2,494 words (mean about 1,810), for about 0.95M words — [robots](https://www.sahilbloom.com/robots.txt). Entrepreneur reports the newsletter earns more than $70k a month and that he had no prior writing experience — [Entrepreneur](https://www.entrepreneur.com/starting-a-business/how-sahil-bloom-built-a-newsletter-that-makes-70000-a/467228)

### Inferences
- Holiday's daily-email format (Daily Stoic: one ancient anecdote, a lesson, about 270 words) is structurally the closest to Housel's "story, principle, the point is" form. The voice is more exhortatory, and the topic (Stoicism) would pull the adapter toward philosophy vocabulary.
- Harford is probably the best "anecdote then principle" economics match, but his post count and his FT rights are both unverified.
- Naval is aphoristically close, but at about 80k words, much of it podcast transcripts and tweetstorms, he adds cadence rather than volume.

### Gaps
- Tim Harford's post count and words, and whether his site's columns are FT reprints (rights).
- Where Burkeman's and Varol's essay archives live and how big they are.
- Whether Daily Stoic posts are written by Holiday alone or by staff. The ConvertKit case study says Holiday; I found no independent confirmation.

## Q3. Which investor letters, memos and speeches match (Marks, Buffett, Munger, Bogle, Klarman, others)?

### Takeaway
Beyond the seeds (Marks, Buffett), the usable investor-voice corpora are Bogle's eBlog (speeches and memos, 2007–2019, no robots.txt), Munger's *Poor Charlie's Almanack* (free to read online from Stripe Press, but copyrighted and with no stated licence) and Tren Griffin's 25iq. 25iq is mostly quotations of other investors, which contaminates it. William Bernstein's Efficient Frontier and Patrick O'Shaughnessy's Investor Field Guide both explicitly prohibit the use (permission only). I found no public source for Klarman's text.

### Cited Findings
- **John C. Bogle, "The Bogle eBlog" (johncbogle.com):** WordPress with no robots.txt (404) and no copyright notice in the footer. Content: speeches (JOIM, CFA, Morningstar 2017), "Memos to Principals and Veterans", "Ask Jack" and press clippings. The archive spans about 25 listing pages; the oldest linked post is 2007-02-09 and the last is "In Memoriam" (Jan 16, 2019) — [johncbogle.com](https://johncbogle.com/); [robots 404](https://johncbogle.com/robots.txt). The REST API returned 404, so there is no exact count. About 250 posts is an estimate from 25 pages.
- **Charlie Munger, *Poor Charlie's Almanack*:** Stripe Press released a free online edition in Dec 2023 because Munger and editor Peter Kaufman wanted to reach the widest audience — [Stripe Press announcement](https://stripepress.substack.com/p/poor-charlies-almanack-is-out-now); [Daring Fireball](https://daringfireball.net/linked/2023/12/29/poor-charlies-almanack). Requests for www.stripe.press/robots.txt redirect to the book page, so there is no robots file. The book page is titled "Experience the wit and wisdom of Charles T. Munger online, for free" — [stripe.press](https://www.stripe.press/poor-charlies-almanack/book). It includes "The Psychology of Human Misjudgment", the talk Housel says he took his title format from — [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- **Tren Griffin (25iq.com):** 300 posts per the WP REST API (835 sitemap URLs, including image entries), dated 2012-10-15 to 2024-10-01. Samples ran 404–1,046 words (mean about 645), for about 190k words. Posts are "A Dozen Things I've Learned from [investor]" compilations, heavily quoting Munger, Livermore and others. robots.txt has no AI rules — [robots](https://25iq.com/robots.txt); [sitemap](https://25iq.com/sitemap.xml)
- **William Bernstein (efficientfrontier.com):** no robots.txt (404). The homepage states that downloading or storing material is "granted for viewing use only. Material may not be reproduced in any form without the express written permission of William J. Bernstein. Reproduction or editing by any means, mechanical or electronic … is strictly prohibited." — [efficientfrontier.com](https://efficientfrontier.com/). That makes it permission only.
- **Patrick O'Shaughnessy (investorfieldguide.com):** Cloudflare-managed robots.txt with `Content-Signal: search=yes,ai-train=no,use=reference` and `Disallow: /` for GPTBot, ClaudeBot, anthropic-ai, Claude-Web, CCBot, Google-Extended, Applebot-Extended, Bytespider, Diffbot, Amazonbot, omgili and cohere-ai. That makes it permission only — [robots](https://investorfieldguide.com/robots.txt). Housel credits O'Shaughnessy with the "wide funnel and a tight filter" reading idea — [How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)
- **Seed letters, access only:** oaktreecapital.com robots.txt disallows only marketing, communication and events document paths, with no AI rules — [robots](https://www.oaktreecapital.com/robots.txt). berkshirehathaway.com has no robots.txt (404) — [robots](https://www.berkshirehathaway.com/robots.txt).

### Inferences
- Bogle's speeches are long and oratorical, more formal than Housel. His memos and "Ask Jack" posts are closer. The text should be filtered to exclude press clippings, which are other journalists' writing.
- The Munger text is copyrighted. Free online reading is not a licence to copy or train, so ask permission or use it only for evaluation.

### Gaps
- **Seth Klarman:** I did not verify the status of *Margin of Safety* (1991) or Baupost letters this session. My background knowledge is that the book is copyrighted and out of print and that the letters are confidential to limited partners. Unverified.
- **Bogle's Vanguard-hosted speech archive** (the Bogle Financial Markets Research Center pages): not located or checked.
- **Stripe Press terms of use:** not fetched.
- **Other letter writers** (Bill Miller, Li Lu, Klarman-style memos): not researched.

## Q4. Which public-domain or openly licensed nonfiction has a similar plain, anecdote-driven money and life-lessons voice?

### Takeaway
There is plenty of US public-domain material: Franklin, Barnum, Bennett, Samuel Smiles (*Self-Help*, *Thrift*), Conwell, Mackay, Lefèvre (borderline creative) and Clason (borderline creative). All sit on Project Gutenberg or Wikisource, whose robots.txt files carry no AI restrictions. Schwed's *Where Are the Customers' Yachts?* (1940) has unverified renewal status and should be treated as in copyright. Frederick Lewis Allen's *Only Yesterday* (1931) is reportedly a Housel influence and becomes US public domain on 2027-01-01. The main cost of this material is dated 18th–19th century diction.

### Cited Findings
- **Project Gutenberg robots.txt** disallows only `/ebooks/search` and has no AI rules — [gutenberg.org/robots.txt](https://www.gutenberg.org/robots.txt)
- **Wikisource robots.txt** has no GPTBot, ClaudeBot, CCBot or Google-Extended rules (grep returned nothing) — [en.wikisource.org/robots.txt](https://en.wikisource.org/robots.txt). archive.org robots.txt disallows only `/control/` and `/report/` — [archive.org/robots.txt](https://archive.org/robots.txt)
- **Standard Ebooks** robots.txt disallows `/ebooks/*/downloads/*` and `/ebooks/*/text*` for listed SEO crawlers and for the user agents chatgpt-user, claude-user, claude-web, MistralAI-User and Perplexity-User — [standardebooks.org/robots.txt](https://standardebooks.org/robots.txt)

| Work | Year | Source (ID) | Approx. words (HEAD bytes ÷ 6) | US PD status | Fit notes |
|---|---|---|---|---|---|
| P. T. Barnum, *The Art of Money Getting* | 1880 | [PG #8581](https://www.gutenberg.org/ebooks/8581) | ~16k | PD (pre-1931) | Short rules illustrated with anecdotes; very close to the "anecdote then principle" form |
| Benjamin Franklin, *The Way to Wealth* | 1758 | [PG #43855](https://www.gutenberg.org/ebooks/43855) | ~7k | PD | Aphorisms (Poor Richard); tiny |
| Benjamin Franklin, *Autobiography* | 1791+ | [PG #20203](https://www.gutenberg.org/ebooks/20203) (also #148) | ~78k | PD | Life lessons from anecdote; 18th-century diction |
| Arnold Bennett, *How to Live on 24 Hours a Day* | 1908 | [PG #2274](https://www.gutenberg.org/ebooks/2274) | ~15k | PD (Bennett d. 1931) | Plain, wry self-help essays; other Bennett titles exist on PG but were not enumerated |
| Samuel Smiles, *Self-Help* | 1859 | [PG #935](https://www.gutenberg.org/ebooks/935) | ~144k | PD | Strings of biographical anecdotes, each feeding a principle |
| Samuel Smiles, *Thrift* | 1875 | [PG #14418](https://www.gutenberg.org/ebooks/14418) | ~125k | PD | Money habits and saving; the same anecdote-driven structure |
| Russell Conwell, *Acres of Diamonds* | 1890 lecture | [PG #368](https://www.gutenberg.org/ebooks/368) | ~44k (includes a biography by another author) | PD | Parable-like lecture: anecdote, then moral |
| Charles Mackay, *Extraordinary Popular Delusions…* | 1841 | [PG #24518](https://www.gutenberg.org/ebooks/24518) | ~281k (only the opening chapters on financial manias are on-topic) | PD | Financial-history manias (Mississippi, South Sea, tulips) |
| Edwin Lefèvre, *Reminiscences of a Stock Operator* | 1923 | [PG #60979](https://www.gutenberg.org/ebooks/60979) (released 2019-12-20) | ~103k | PD (1923 works entered PD on 2019-01-01) | **Borderline creative** (fictionalised Livermore memoir) |
| George S. Clason, *The Richest Man in Babylon* | pamphlets 1920–24; book 1926 | Wikisource / Internet Archive / LibriVox ([Wikipedia](https://en.wikipedia.org/wiki/The_Richest_Man_in_Babylon)) | not measured | PD (1926 → PD since 2022-01-01) | **Borderline creative** (Babylonian parables); "Seven Cures for a Lean Purse" and "Five Laws of Gold" are rule lists |
| Fred Schwed Jr., *Where Are the Customers' Yachts?* | 1940 (Simon & Schuster) | none (in print from Wiley) | n/a | **Unverified; treat as in copyright** | Witty, plain Wall Street skepticism; very Housel-adjacent |
| Frederick Lewis Allen, *Only Yesterday* | 1931 | not checked | n/a | Becomes PD on 2027-01-01 at the latest (1931 + 95 years) | Informal narrative history; reportedly a Housel influence (unverified) |

- Clason's material first appeared as pamphlets distributed by banks and insurance companies from 1920 to 1924, was bound as a book in 1926, and was reissued in 1930 as *The Richest Man in Babylon and Other Stories*. Wikipedia notes full texts on Wikisource and Internet Archive and a public-domain LibriVox audiobook — [Wikipedia](https://en.wikipedia.org/wiki/The_Richest_Man_in_Babylon)
- Schwed's book was first published in 1940 by Simon & Schuster and reprinted in 1955 and in 1995 (Wiley); Wiley editions continue into 2005–06 — [search results: Raptis Rare Books](https://www.raptisrarebooks.com/product/where-are-the-customers-yachts-fred-schwed-first-edition-peter-arno-rare-2/); [Knox County Library record](https://discover.knoxcountylibrary.org/Record/430348). No source found states the renewal status.
- **Public dataset copies of PD books:** the Hugging Face dataset `sedthh/gutenberg_english` (about 18k downloads) is a Gutenberg English dump that likely contains these titles — [HF](https://huggingface.co/datasets/sedthh/gutenberg_english)

### Inferences
- **Copyright terms:** US works published 1927–1977 with notice get 95 years from publication if they were renewed (for pre-1964 works). So a 1931 work is protected at most until 2026-12-31, and *Only Yesterday* is PD on 2027-01-01 whatever its renewal status. For Schwed (1940), a renewal filed in 1967–68 would mean protection until the end of 2035. Without one, the book has been PD since 1968.
- **Diction:** the PD material is anecdote-dense but archaic. Mixed in at low weight it could teach the anecdote-to-maxim move, but it risks adding Victorian vocabulary ("industry", "frugality", long periodic sentences). It is better suited as a small slice or for structure-only use, for example as paraphrased training pairs.
- **Seneca:** Gummere's translation of *Moral Letters to Lucilius* (1917–25) is PD and aphoristic, but it is a translation and was not checked.

### Gaps
- **Schwed renewal:** not verified. The Stanford Copyright Renewal Database returned a JavaScript bot challenge and HathiTrust returned 403 to automated requests. Check by hand at exhibits.stanford.edu/copyrightrenewals (Schwed, 1967–68 renewals) or in the 1967–68 Catalog of Copyright Entries on archive.org.
- ***Only Yesterday*:** renewal status and Gutenberg availability not checked.
- **Other PD titles not verified:** Henry Clews, *Fifty Years in Wall Street* (1908); Carnegie, *The Empire of Business* and *The Gospel of Wealth*; Rockefeller, *Random Reminiscences*; Thomas Gibson, *The Pitfalls of Speculation*. The Gutendex API errored on these lookups.
- **Gutenberg's bulk-download (mirror) policy** was not fetched this session.

## Q5. Access and legal facts for every candidate (robots.txt, AI opt-outs, platform, terms, paywall)

### Takeaway
Of the non-seed web candidates, four are **permission only** because of an explicit opt-out: Investor Field Guide (O'Shaughnessy), Mr. Money Mustache, Abnormal Returns and Efficient Frontier (Bernstein; written terms). Substack-hosted candidates (Young Money, Joachim Klement, Frederik Gieschen) carry no AI rules in robots.txt, but **Substack's Terms of Use forbid crawling, scraping or storing a significant portion of content**, so those should also be permission only or limited to RSS. The rest of the candidates (WordPress, Webflow, Posthaven, Jekyll) have no AI rules and no `noai` tags.

### Cited Findings
- **Substack ToS:** users may not use any process that "Crawls," "scrapes," or "spiders" any page, data, or portion of Substack (through use of manual or automated means), or that "Copies or stores any significant portion of the content on Substack." Substack also states that its own content licence "does not permit us to use your content to train third-party AI models" — [substack.com/tos](https://substack.com/tos)
- **Cloudflare-managed AI opt-out:** investorfieldguide.com and mrmoneymustache.com serve identical Cloudflare-managed robots.txt files: `Content-Signal: search=yes,ai-train=no,use=reference`, plus `Disallow: /` for GPTBot, ClaudeBot, anthropic-ai, Claude-Web, CCBot, Google-Extended, Applebot-Extended, Bytespider, Diffbot, Amazonbot, omgili and cohere-ai — [investorfieldguide robots](https://investorfieldguide.com/robots.txt); [MMM robots](https://www.mrmoneymustache.com/robots.txt)
- **Abnormal Returns:** `Disallow: /` for ChatGPT-User, GPTBot, Google-Extended, anthropic-ai, Claude-Web and CCbot — [abnormalreturns robots](https://abnormalreturns.com/robots.txt)

#### Master candidate table (non-seed)

Columns: corpus URL · posts (method) · estimated words · dates · register/topics · Housel link · access.

| # | Author / corpus | Corpus URL | Posts (method) | Est. words | Dates | Register / topics | Why Housel-like (evidence) | robots.txt / AI rules | Platform, terms, paywall | Access verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ted Lamade | [collabfund.com author page](https://collabfund.com/blog/authors/ted-lamade-managing-director-at-the-carnegie-institution-for-science/) | 34 (author page) | ~58k (n=3: 1.2k–2.3k) | 2021-08 → 2026-10 | Life lessons, risk, history vignettes | Publishes on Housel's Collab Fund blog | No robots.txt (404) | Jekyll/GitHub Pages; free | Open (same host as Housel corpus) |
| 2 | Jason Zweig | [jasonzweig.com wp-sitemap](https://jasonzweig.com/wp-sitemap.xml) | 802 (WP REST) | ~0.5M (n=4 mean 652) | 2004-08 → 2026; 2021–23 ≈ 0–1/yr | Behavioural finance, investor psychology; journalist voice | Same finance-journalism cluster (inference) | No AI rules ([robots](https://jasonzweig.com/robots.txt)) | WordPress; many posts are WSJ-column reprints (rights unclear) | Open by robots; rights caveat |
| 3 | Jonathan Clements / HumbleDollar | [humbledollar.com sitemap](https://humbledollar.com/sitemap.xml) | 3,812 all authors (WP REST) | ~2M max for Clements (comments inflate; site is multi-author) | 2014-11 → 2026 | Plain personal finance and life lessons | Harriman House (Housel's publisher) published *Money and Me* | No AI rules; Crawl-delay 10 ([robots](https://humbledollar.com/robots.txt)) | WordPress; free; author died 2025-09-21 | Open; filter to Clements's own posts |
| 4 | Joe Wiggins, Behavioural Investment | [behaviouralinvestment.com sitemap](https://behaviouralinvestment.com/sitemap.xml) | ~315 sitemap URLs | not measured (sample failed) | 2017-08 → 2026-11 | Behavioural finance essays | Topic overlap (inference) | No AI rules ([robots](https://behaviouralinvestment.com/robots.txt)) | WordPress.com; free | Open |
| 5 | Jack Raines, Young Money | [youngmoney.co sitemap](https://www.youngmoney.co/sitemap.xml) | ~342 | ~0.57M (n=4 mean 1,660) | 2021-07 → 2026 (sitemap lastmod from 2024) | Money, careers, life for twenty-somethings; humorous | Interviewed on Ritholtz's MIB | Substack template; blocks only BLEXBot ([robots](https://www.youngmoney.co/robots.txt)) | **Substack (ToS bars scraping)** | Permission / RSS only |
| 6 | Joachim Klement | [klementoninvesting.substack.com sitemap](https://klementoninvesting.substack.com/sitemap.xml) | ~1,932 | ~1.6M (n=4 mean 848) | lastmod 2024-05 → 2026-11 | Research-driven investing notes; daily | Behavioural finance overlap (inference) | Substack template ([robots](https://klementoninvesting.substack.com/robots.txt)) | **Substack** | Permission / RSS only |
| 7 | Frederik Gieschen (Neckar's Notes → frederikjournals.com) | [frederikjournals.com sitemap](https://www.frederikjournals.com/sitemap.xml) | ~411 | ~0.58M (n=4: 147–4,977) | lastmod 2023-01 → 2026-10 | Investor profiles, financial history, psychology | Financial-history storytelling (inference) | Substack template ([robots](https://www.frederikjournals.com/robots.txt)); neckar.substack.com redirects here | **Substack** | Permission / RSS only |
| 8 | Jamie Catherwood, Investor Amnesia | investoramnesia.com | unknown | unknown | 2017– | Financial history | History-first finance; O'Shaughnessy AM | robots.txt returned Cloudflare 520 on 2026-11-08; investoramnesia.substack.com 404 | unknown | Unverified; recheck |
| 9 | Cullen Roche (Pragmatic Capitalism) | [pragcap.com wp-sitemap](https://www.pragcap.com/wp-sitemap.xml) | 8,416 (WP REST); 0 posts since 2024 | ~6.6M (n=4 mean 783) | 2008-09 → 2023 | Macro, money, investing explainers | Finance blogger cluster (inference) | No AI rules ([robots](https://www.pragcap.com/robots.txt)) | WordPress; free | Open |
| 9b | Cullen Roche (Discipline Funds) | [disciplinefunds.com wp-sitemap](https://disciplinefunds.com/wp-sitemap.xml) | ~209 | not measured | 2022 → 2026-09 | Same, plus fund marketing | — | No AI rules ([robots](https://disciplinefunds.com/robots.txt)) | WordPress; commercial fund site | Open; marketing contamination |
| 10 | Barry Ritholtz | [ritholtz.com sitemap](https://ritholtz.com/sitemap.xml) | ≥40,001 URLs in 40 of 78 post sitemaps | huge, mostly link lists | 2002-09 → 2026-11 | Markets, behavioural finance, link curation | Founder of Ritholtz Wealth (seed cluster) | No AI rules ([robots](https://ritholtz.com/robots.txt)) | Cloudflare; free | Open; heavy filtering needed |
| 11 | Tren Griffin, 25iq | [25iq.com sitemap](https://25iq.com/sitemap.xml) | 300 (WP REST) | ~0.19M (n=4 mean 645) | 2012-10 → 2024-10 | "A Dozen Things I've Learned from…" (quote-heavy) | Munger/Buffett lessons format | No AI rules ([robots](https://25iq.com/robots.txt)) | WordPress; free | Open; quote contamination |
| 12 | John C. Bogle, eBlog | [johncbogle.com](https://johncbogle.com/) | ~250 (estimate from 25 listing pages) | not measured | 2007-02 → 2019-01 | Speeches, memos, Q&A on index investing | Investor-letter register | No robots.txt (404) | WordPress; no copyright notice in footer | Open; exclude press clippings |
| 13 | Charlie Munger, *Poor Charlie's Almanack* | [stripe.press](https://www.stripe.press/poor-charlies-almanack/book) | 1 book (talks) | not measured | talks 1986–2007; ed. 2023 | Speeches, aphorisms | Housel copied Munger's title format | No robots.txt (redirects to book page) | Free to read; © Stripe Press | Permission (copyrighted) |
| 14 | Patrick O'Shaughnessy | [investorfieldguide.com](https://investorfieldguide.com/) | not measured | — | — | Investing essays (now mostly podcast) | Housel credits his reading heuristic | **ai-train=no; blocks GPTBot, ClaudeBot, CCBot, Google-Extended** | Cloudflare-managed | **Permission only** |
| 15 | William Bernstein, Efficient Frontier | [efficientfrontier.com](https://efficientfrontier.com/) | not measured | — | 1996–2010s | Financial history, asset allocation | History-heavy finance (inference) | No robots.txt (404) | **Written terms bar reproduction without written permission** | **Permission only** |
| 16 | Ryan Holiday | [ryanholiday.net sitemap](https://ryanholiday.net/sitemap_index.xml) | ~936 (sitemap) | ~1.15M (n=4 mean 1,234) | 2007 → 2026-11 | Stoicism, history anecdote to lesson | Structural match (inference) | `Disallow:` empty ([robots](https://ryanholiday.net/robots.txt)) | WordPress + Kit; REST locked | Open |
| 17 | Daily Stoic | [dailystoic.com sitemap](https://dailystoic.com/sitemap_index.xml) | ~3,584 (sitemap) | ~1.0M (n=4 mean 273) | 2016-07 → 2026-11 | Daily ~270-word anecdote-lesson emails | Format closest to Housel's short posts (inference) | No AI rules ([robots](https://dailystoic.com/robots.txt)) | WordPress + Kit; company-run; has a store | Open; authorship mixed |
| 18 | Tim Harford | [timharford.com sitemap](https://timharford.com/sitemap.xml) | not measured | — | 2000s → 2026-11 | Economics via one anecdote | Anecdote, then principle (inference) | No AI rules ([robots](https://www.timharford.com/robots.txt)) | WordPress; refuses non-browser clients; FT column rights unclear | Open by robots; rights caveat |
| 19 | Eric Barker | [bakadesuyo.com sitemap](https://bakadesuyo.com/sitemap_index.xml) | 5,591 (WP REST) | several M; high variance | 2009-07 → 2026-10 | Psychology research to life advice | Psychology/life-lesson overlap | No AI rules ([robots](https://bakadesuyo.com/robots.txt)) | WordPress; free | Open; early posts quote research |
| 20 | Naval Ravikant | [nav.al sitemap](https://nav.al/sitemap_index.xml) | 240 (WP REST) | ~80k | 2005-11 → 2026 | Aphorisms on wealth and happiness | Housel cites Naval's advice | `Disallow:` empty ([robots](https://nav.al/robots.txt)) | WordPress | Open |
| 21 | Cal Newport | [calnewport.com sitemap](https://calnewport.com/sitemap_index.xml) | 1,130 (WP REST) | ~1.1–3.5M | 2007-07 → 2026-10 | Work and attention essays | Plain explanatory essays (inference) | `Disallow:` empty ([robots](https://calnewport.com/robots.txt)) | WordPress + Kit | Open |
| 22 | Mark Manson | [markmanson.net sitemap](https://markmanson.net/sitemap.xml) | 283 (WP REST) | ~0.85M | 2010-08 → 2025 | Self-help; profane, casual | Life lessons (weak style match) | No AI rules ([robots](https://markmanson.net/robots.txt)) | WordPress + Kit; has a "subscribers-only" section | Open (free posts) |
| 23 | JL Collins | [jlcollinsnh.com sitemap](https://jlcollinsnh.com/sitemap_index.xml) | ~287 | ~0.6–1.5M (comments inflate samples) | 2011-06 → 2026-07 | Plain index-investing advice, life stories | Plain money-and-life voice (inference) | `Disallow:` empty ([robots](https://jlcollinsnh.com/robots.txt)) | WordPress | Open |
| 24 | Fred Wilson, AVC | [avc.com sitemap](https://avc.com/sitemap_index.xml) | ~9,046 | ~2.8M | 2003-09 → 2024-05 | Short daily VC and life posts | Short, plain, daily (inference) | No AI rules ([robots](https://avc.com/robots.txt)) | WordPress; ended (moved onchain) | Open |
| 25 | Sahil Bloom | [sahilbloom.com sitemap](https://www.sahilbloom.com/sitemap.xml) | ~522 newsletters | ~0.95M | sitemap lastmod 2024-07 → 2026-10 | Frameworks and life lessons, listicle-ish | Topic overlap; mass-market | robots.txt has only a Sitemap line ([robots](https://www.sahilbloom.com/robots.txt)) | Webflow + Kit; free | Open; high AI-risk (Q7) |
| 26 | Ozan Varol | ozanvarol.com | not measured (sitemap 500) | — | — | Thinking and decision essays | Anecdote to principle (inference) | Yoast `Disallow:` empty, Crawl-delay 10 ([robots](https://www.ozanvarol.com/robots.txt)) | WordPress | Open; site errors |
| 27 | Mr. Money Mustache | [mrmoneymustache.com](https://www.mrmoneymustache.com/) | 542 (WP REST) | — | 2011-04 → | Frugality, FIRE | Money life lessons | **ai-train=no; blocks AI bots** | Cloudflare-managed | **Permission only** |
| 28 | Abnormal Returns (Tadas Viskanta) | [abnormalreturns.com](https://abnormalreturns.com/) | — | — | — | Link curation | Finance cluster | **Blocks GPTBot, anthropic-ai, CCbot, Google-Extended** | WordPress | **Permission only** (also low prose) |
| 29 | Philosophical Economics ("Jesse Livermore") | [wp-sitemap](https://www.philosophicaleconomics.com/wp-sitemap.xml) | ~75 | — | 2012 → 2020 | Dense quantitative essays | Finance cluster, poor style fit | No AI rules ([robots](https://www.philosophicaleconomics.com/robots.txt)) | WordPress | Open; low fit |
| 30 | Oliver Burkeman | [oliverburkeman.com](https://www.oliverburkeman.com/) | 33 site pages | — | — | Time and mortality essays | Aphoristic life lessons (inference) | No AI rules ([robots](https://oliverburkeman.com/robots.txt)); has `/llms.txt` | Wix; essays are hosted elsewhere | Unverified corpus location |
| 31 | Sam Altman | [blog.samaltman.com](https://blog.samaltman.com/) | not measured | — | — | Short aphoristic essays | Aphoristic (inference) | Only `/posthaven/` and `/private/` disallowed ([robots](https://blog.samaltman.com/robots.txt)) | Posthaven | Open |
| 32 | Public-domain shelf (Q4) | gutenberg.org / Wikisource | 9 titles | ~0.8M total (Mackay alone ~281k) | 1758–1926 | Money maxims, thrift, manias | Anecdote-to-maxim form | PG disallows only `/ebooks/search`; no AI rules | Public domain | Open (US) |

#### Seed list: access facts only (measurement left to the other agent)

| Seed | robots.txt finding (fetched 2026-11-08) | Platform / notes |
|---|---|---|
| Ben Carlson, awealthofcommonsense.com | Flywheel default; only calendar/event paths disallowed; no AI rules — [robots](https://awealthofcommonsense.com/robots.txt) | WordPress |
| Michael Batnick, theirrelevantinvestor.com | Blocks only Amazonbot and Nutch; no GPTBot/ClaudeBot/CCBot rules — [robots](https://theirrelevantinvestor.com/robots.txt) | Paths (`/p/*/likes`, `/polls/`, `/nectar_analytics`) suggest a hosted newsletter platform; platform not confirmed, so check its ToS |
| Josh Brown, thereformedbroker.com | No AI rules — [robots](https://thereformedbroker.com/robots.txt) | WordPress |
| Nick Maggiulli, ofdollarsanddata.com | No AI rules (WP virtual robots) — [robots](https://ofdollarsanddata.com/robots.txt) | WordPress |
| Seth Godin, seths.blog | No AI rules — [robots](https://seths.blog/robots.txt) | WordPress |
| James Clear, jamesclear.com | No AI rules — [robots](https://jamesclear.com/robots.txt) | WordPress |
| Farnam Street, fs.blog | **Explicit `Allow: /`** for GPTBot, ClaudeBot, anthropic-ai, PerplexityBot, Google-Extended, Applebot-Extended, Bytespider, CCBot, meta-externalagent, MistralAI-Training, Perplexity-User — [robots](https://fs.blog/robots.txt) | WordPress; some content is members-only (not checked) |
| Derek Sivers, sive.rs | `User-agent: * Allow: /` — [robots](https://sive.rs/robots.txt) | Custom |
| Kevin Kelly, kk.org | Blocks meta-externalagent, Amazonbot, MJ12bot, dotbot; `Allow: /` for all others — [robots](https://kk.org/robots.txt) | WordPress |
| Jason Fried, signalvnoise.com / world.hey.com/jason | signalvnoise.com has no robots.txt (404); world.hey.com is `User-Agent: * Allow: /` — [SvN](https://signalvnoise.com/robots.txt); [HEY World](https://world.hey.com/robots.txt) | — |
| Howard Marks, oaktreecapital.com | Only marketing, communication and events doc paths disallowed; no AI rules — [robots](https://www.oaktreecapital.com/robots.txt) | Site terms of use not checked |
| Warren Buffett, berkshirehathaway.com | No robots.txt (404) — [robots](https://www.berkshirehathaway.com/robots.txt) | Static HTML/PDF; HF copies exist (Q6) |
| Paul Graham, paulgraham.com | Disallows some internal paths and Roverbot only; no AI rules — [robots](https://paulgraham.com/robots.txt) | HF copies exist (Q6) |
| Carl Richards, behaviorgap.com | No AI rules — [robots](https://behaviorgap.com/robots.txt) | WordPress |

### Inferences
- Under the project's precedent (an explicit AI opt-out means "permission only"), the permission-only set is Investor Field Guide, Mr. Money Mustache, Abnormal Returns and Efficient Frontier, the last on written terms rather than robots. Substack-hosted authors add a platform-ToS bar on top of whatever the author wants.
- Farnam Street's explicit AI-crawler allow-list is the strongest positive signal of any seed.
- A permissive robots.txt is not a licence: the content is still copyrighted. "Open" in the tables means "no machine-readable or written opt-out found", not "licensed".

### Gaps
- I did not read site-level terms of use for most WordPress sites. I checked only Substack's ToS and Bernstein's homepage notice.
- Platform for theirrelevantinvestor.com and Investor Amnesia; Tim Harford's FT reprint rights; Jason Zweig's WSJ reprint rights.
- Medium ToS for Taleb's essays (Taleb is not in the table because I did not check access).

## Q6. Does a public dataset copy already exist (Hugging Face, Kaggle)?

### Takeaway
Hugging Face has copies only for seeds (Buffett letters, Paul Graham essays) and for Naval (a copyrighted book), plus generic Gutenberg dumps. Searches turned up no HF dataset for Housel or for any non-seed web candidate. Kaggle was not searched.

### Cited Findings
- **Buffett letters:** `eagle0504/warren-buffett-annual-letters-1977-2022` (also `…-1977-to-2019` and a Q&A-augmented 1998–2024 set) — [HF](https://huggingface.co/datasets/eagle0504/warren-buffett-annual-letters-1977-2022)
- **Paul Graham:** `sgoel9/paul_graham_essays` (about 1,186 downloads), `pookie3000/paul_graham_all_essays`, `chromadb/paul_graham_essay`, and `Mindofmachine/paul_graham_and_sam_altman_articles` (about 399 downloads; includes Altman) — [HF sgoel9](https://huggingface.co/datasets/sgoel9/paul_graham_essays); [HF Mindofmachine](https://huggingface.co/datasets/Mindofmachine/paul_graham_and_sam_altman_articles)
- **Naval:** `harshalmore31/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant`, apparently the full text of a copyrighted book — [HF](https://huggingface.co/datasets/harshalmore31/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant)
- **Stoic texts:** `jamescalam/stoic-corpus` and others, likely classical texts rather than Holiday — [HF](https://huggingface.co/datasets/jamescalam/stoic-corpus)
- **Gutenberg:** `sedthh/gutenberg_english` (about 18k downloads) and `umm-maybe/gutenberg_english_pre1928` — [HF](https://huggingface.co/datasets/sedthh/gutenberg_english)
- HF name searches for housel, "psychology of money", munger, "howard marks", bogle, "ryan holiday", "tim harford", "mark manson", "seth godin", ritholtz, "sahil bloom", humbledollar and "mr money mustache" returned no relevant datasets — [HF datasets API](https://huggingface.co/api/datasets?search=housel)

### Inferences
- Redistributed HF copies do not change the underlying rights. The Naval Almanack dataset in particular looks like an unlicensed book copy and should not be used.

### Gaps
- Kaggle was not searched. HF search matches dataset names only, so corpora with generic names (for example "finance blogs") could be missed.

## Q7. What is the risk that post-2023 output is AI-assisted?

### Takeaway
Several candidates stopped or slowed before or around 2023: Zweig, Manson, Pragmatic Capitalism, Naval and AVC. Their archives are mostly pre-ChatGPT and low-risk. The highest-risk sources are high-volume or company-run newsletters (Klement at about 1,900 Substack posts, Sahil Bloom's media business, Daily Stoic's daily cadence, multi-author HumbleDollar). No candidate was found disclosing AI use, but absence of disclosure is not evidence.

### Cited Findings
- **Posts per year from WP REST, 2019→2026:**
  - Jason Zweig: 64, 38, 1, 0, 1, 15, 2, 2 — [WP REST](https://jasonzweig.com/wp-json/wp/v2/posts)
  - Mark Manson: 26, 44, 38, 11, 23, 4, 4, 0 — [WP REST](https://markmanson.net/wp-json/wp/v2/posts)
  - Pragmatic Capitalism: 77, 44, 67, 77, 12, 0, 0, 0 — [WP REST](https://www.pragcap.com/wp-json/wp/v2/posts)
  - Naval: 56, 21, 59, 2, 2, 4, 17, 9 — [WP REST](https://nav.al/wp-json/wp/v2/posts)
  - Cal Newport: 44, 88, 39, 34, 22, 17, 35, 34 (no jump) — [WP REST](https://calnewport.com/wp-json/wp/v2/posts)
  - Barking Up the Wrong Tree: 16, 11, 21, 34, 25, 26, 27, 22 (no jump) — [WP REST](https://bakadesuyo.com/wp-json/wp/v2/posts)
  - HumbleDollar (all authors): 349, 378, 665, 669, 574, 426, 113, 92 (the drop tracks Clements's illness and death) — [WP REST](https://humbledollar.com/wp-json/wp/v2/posts)
- AVC's last on-site post was May 2024 ("I've moved onchain"), so the archive is almost entirely pre-2023 — [avc.com sitemap](https://avc.com/sitemap_index.xml)
- **Sahil Bloom:** the newsletter is a business earning more than $70k a month, built by someone with no prior writing background — [Entrepreneur](https://www.entrepreneur.com/starting-a-business/how-sahil-bloom-built-a-newsletter-that-makes-70000-a/467228). Search found no reporting of ghostwriters or AI use.
- **Daily Stoic:** the email is described as written daily by Holiday — [ConvertKit](https://convertkit.com/resources/blog/daily-stoic-case-study). Sitemap posts number about 3,584 between 2016 and 2026 — [sitemap](https://dailystoic.com/sitemap_index.xml)
- **Joachim Klement:** the Substack sitemap holds about 1,932 posts, lastmod 2024-05 to 2026-11 — [sitemap](https://klementoninvesting.substack.com/sitemap.xml). Substack sitemap lastmod is not the publish date, so per-year output could not be computed without crawling, which Substack's ToS bars.

### Inferences
- Use a hard cutoff before 2022-11-30 (the ChatGPT launch) for high-volume newsletter sources, or score post-cutoff text with the project's AI-slop detector before including it.
- Ted Lamade's 34 posts are low-volume (3–10 a year: 2021=3, 2022=10, 2023=5, 2024=7, 2025=5, 2026=4 per the author page) with no rate jump, so the risk is low. Still, 21 of the 34 date from 2023 or later.
- Zweig, Manson, Pragmatic Capitalism and AVC are effectively closed pre-2023 archives, which makes them attractive on AI-contamination grounds.

### Gaps
- Publish-date distributions for Substack, Webflow and other non-WordPress sources (Young Money, Klement, Gieschen, Sahil Bloom, Ryan Holiday) were not computed.
- No candidate was checked for an AI-use disclosure page.
