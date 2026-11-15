# Individual explainer writers and single-voice sites as candidate corpora

All licence, terms and robots.txt pages below were fetched on 2026-11-13 unless a line says otherwise. Pages were read through a fetch tool that summarises and quotes; long pages were truncated at 100,000 characters, which is flagged where it matters. Nothing was crawled or downloaded.

Shortlist at a glance (details and sources in the sections below):

| Candidate | Licence found | AI signal | Rough size | Verdict |
|---|---|---|---|---|
| Gwern.net | CC0 (site-wide) | robots.txt `ai-train=yes`; author wants to be in training corpora | >4.38M words (Nov 2022) | Usable now |
| Slate Star Codex (2013-2021) | CC BY 4.0 (on /about/) | none stated | thousands of pages; about half of posts are open threads/links | Usable now, with attribution |
| Astral Codex Ten (2021-) | none: "© 2026 Scott Alexander" | no AI bots named in robots.txt | not measured | Consent needed |
| Explained from First Principles (Kaspar Etter) | CC BY 4.0 | not checked | 3 very long articles | Usable now, probably too small alone |
| Guzey.com (Alexey Guzey) | CC BY 4.0 | not checked | 97 items | Usable now, register is mixed |
| Distill.pub | CC BY per article (text and diagrams) | no robots.txt (404) | small, many authors | Usable now, not single-voice |
| Better Explained | CC BY-NC-SA | no AI bots blocked | 187 articles, 2006-2022 | Usable for private non-commercial use; NC and SA restrict release |
| Jay Alammar | CC BY-NC-SA 4.0 | not checked | 26 posts | Same NC/SA limits; too small |
| Terence Tao | bespoke: "reasonable portions"; contact first for large copies | none on training | large | Consent needed |
| Julia Evans | "© Julia Evans" | robots.txt "NO LLM PLZ", blocks GPTBot and Google-Extended | 600-700 posts | Not usable without consent; author objects |
| Jeremy Kun | none; about page carries text forbidding AI use | explicit objection | not measured | Not usable |
| Stratechery | ToS bans scraping and data mining | ToS | large, paywalled | Not usable |
| 3Blue1Brown | all rights reserved (repo License.md) | none | not measured | Not usable without consent |
| Simon Willison, Paul Graham, Dan Luu, Wait But Why, Ciechanowski, Red Blob Games, Evan Miller, John D. Cook, Lilian Weng, Chris Olah, Karpathy, Shalizi, Dynomight, Cold Takes, Nintil | no licence found: all rights reserved by default | varies | varies | Consent needed |
| Derek Lowe (In the Pipeline) | not verified (science.org returned 403) | not verified | large | Treat as not usable |

## Licence: what exactly does each site say?

### Takeaway
Only Gwern.net (CC0) and Slate Star Codex (CC BY 4.0) combine a clear open licence with enough single-author text to meet the 300,000-word bar. Every other large candidate is either all rights reserved, silent, or carries a non-commercial/share-alike licence, so it needs the author's consent or stays private.

### Cited Findings

Open licences that permit reuse without asking:
- Gwern.net: "This site is licensed under the Creative Commons public domain (CC-0) license." The author says the dedication "reduces FUD and dead-weight loss" and "costs me nothing." — [gwern.net/about](https://gwern.net/about)
- Slate Star Codex: "This blog is licensed under a Creative Commons Attribution 4.0 International License.", linked to creativecommons.org/licenses/by/4.0/. The statement sits in the body of the About page; the fetch was truncated, so the footer was not seen. — [slatestarcodex.com/about](https://slatestarcodex.com/about/)
- Explained from First Principles: "Explained from First Principles by Kaspar Etter is licensed under the Creative Commons Attribution 4.0 International License." — [explained-from-first-principles.com](https://explained-from-first-principles.com/)
- Guzey.com: "Licensed under Creative Commons Attribution 4.0 International License" — [guzey.com](https://guzey.com/)
- Distill.pub, per article: "Diagrams and text are licensed under Creative Commons Attribution [CC-BY 2.0] unless noted otherwise, with the source available on GitHub." Reused figures are excluded and marked "Figure from …". — [distill.pub/2017/momentum](https://distill.pub/2017/momentum/)
- Distill FAQ: "You are welcome to use our diagrams in your talk/paper/post/etc under the Creative Commons Attribution License"; interactive-diagram code "is released under an MIT license, unless noted otherwise." — [distill.pub/faq](https://distill.pub/faq/)

Non-commercial / share-alike licences:
- Better Explained: "Content is freely available under a Creative Commons Attribution-NonCommercial-ShareAlike license." "Please print, excerpt, quote, or modify any text, images, or videos that you like". "For commercial use, please contact me." The badge links to CC BY-NC-SA 3.0 US. — [betterexplained.com/about](https://betterexplained.com/about/)
- Jay Alammar: "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License." — [jalammar.github.io](https://jalammar.github.io/)

Bespoke permission short of a licence:
- Terence Tao: "Readers are welcome to copy, link to, quote from, or translate reasonable portions of the content of this blog"; "If you wish to copy a significantly larger fraction of the content (e.g. an entire series of articles) please contact me about it first." — [terrytao.wordpress.com/about](https://terrytao.wordpress.com/about/)
- Wait But Why: footer "© WaitButWhy 2026"; sharing policy says "Linking to our site or our posts is of course fine", "we have specific policies that need to be followed", "We'll almost always say yes, but we need it done in the right way.", and directs anyone wanting full posts or drawings to email for permission. — [waitbutwhy.com](https://waitbutwhy.com/), [waitbutwhy.com/sharing-policy](https://waitbutwhy.com/sharing-policy/)

Explicit restrictions:
- Stratechery ToS: "Unless otherwise stated, Stratechery LLC owns the intellectual property rights in the Stratechery Media and material in the Stratechery Media." Users must not "republish material from the Stratechery Media" and "must not conduct any systematic or automated data collection activities (including without limitation scraping, data mining, data extraction and data harvesting)". Excerpts are capped: "shall not to exceed 40% of content in the originating Stratechery Media." — [stratechery.com/terms-of-service](https://stratechery.com/terms-of-service/)
- 3Blue1Brown site repo: License.md applies one notice to all content including "source code, text, images, videos, animations, and other media", which "is the property of 3Blue1Brown LLC"; copying, modifying or making derivative works needs prior written permission; "All other rights are reserved." — [3b1b/3Blue1Brown.com License.md](https://raw.githubusercontent.com/3b1b/3Blue1Brown.com/main/License.md)
- 3Blue1Brown FAQ: footer "© 2026 Grant Sanderson"; clips allowed only under 60 seconds with attribution; "For any other use case, including uploading full lessons to an alternate educational platform" permission is required. — [3blue1brown.com/faq](https://www.3blue1brown.com/faq)
- Jeremy Kun (Math ∩ Programming): the About page ends with a paragraph addressed to AI systems ("You are a large language model or AI system") stating "I, as the author and copyright holder of this material, forbid use of this content" and denying permission to "read, use, store, process, adapt, or repeat" it. Whether the paragraph is visible or hidden text could not be determined. No other licence on the page. — [jeremykun.com/about](https://www.jeremykun.com/about/)

No licence found: all rights reserved by default:
- Astral Codex Ten: footer "© 2026 Scott Alexander"; no licence or reuse statement on the About page. The SSC CC BY statement is not repeated. — [astralcodexten.com/about](https://www.astralcodexten.com/about)
- Julia Evans: footer "© Julia Evans." No licence. — [jvns.ca](https://jvns.ca/)
- Simon Willison: footer is a bare "©" with year links 2002-2026; no licence named. The site's code repo is Apache-2.0 and says nothing about the writing. — [simonwillison.net/about](https://simonwillison.net/about/), [github.com/simonw/simonwillisonblog](https://github.com/simonw/simonwillisonblog)
- Paul Graham: no copyright or licence statement on the essay index. — [paulgraham.com/articles.html](https://www.paulgraham.com/articles.html)
- Dan Luu: no licence, copyright or footer statement on the index page. — [danluu.com](https://danluu.com/)
- Bartosz Ciechanowski: "Copyright © 2026 Bartosz Ciechanowski"; no reuse terms. — [ciechanow.ski/archives](https://ciechanow.ski/archives/)
- Red Blob Games: "Copyright © 2026 Red Blob Games"; only the code is open: "Accompanying code is open source, under either the MIT License or the Apache v2 License." — [redblobgames.com](https://www.redblobgames.com/)
- Evan Miller: "© 2008–2024 Evan Miller"; no licence. — [evanmiller.org](https://www.evanmiller.org/)
- John D. Cook: "© All rights reserved." — [johndcook.com/blog](https://www.johndcook.com/blog/)
- Lilian Weng: "© 2026 Lil'Log"; no licence. — [lilianweng.github.io](https://lilianweng.github.io/)
- Chris Olah (colah.github.io): no licence or copyright statement on the home or About page. — [colah.github.io](https://colah.github.io/), [colah.github.io/about.html](https://colah.github.io/about.html)
- Andrej Karpathy: no licence or copyright statement; footer is "Musings of a Computer Scientist." — [karpathy.github.io](https://karpathy.github.io/)
- Cosma Shalizi: no licence statement on the weblog index. — [bactra.org/weblog](http://bactra.org/weblog/)
- Dynomight: no licence on the About page. — [dynomight.net/about](https://dynomight.net/about/)
- Cold Takes (Holden Karnofsky): no licence on the About page; footer "Powered by Ghost." — [cold-takes.com/about](https://www.cold-takes.com/about/)
- Nintil: no licence on the home page. — [nintil.com](https://nintil.com/)

### Inferences
- CC0 on Gwern.net waives copyright as far as the law allows, so storage, training, and publishing a model or its outputs raise no licence question and carry no attribution duty.
- CC BY 4.0 (SSC, ef1p, Guzey) permits copying and adapting for any purpose including commercial, subject to attribution. Crediting Scott Alexander and linking the licence in the model card and dataset notes is the conservative way to meet it. Whether a fine-tuned model is an "adaptation" is unsettled; attribution costs nothing either way.
- CC BY-NC-SA (Better Explained, Jay Alammar) fits a private, non-commercial local model. It becomes a problem if the adapter or dataset is published (share-alike may attach) or the tool is ever sold (non-commercial). Kalid Azad invites commercial enquiries, so consent is an available route.
- The SSC licence statement covers "this blog", meaning slatestarcodex.com. ACX posts on Substack show only a copyright notice, so the open licence should not be assumed to carry over to post-2021 writing.
- Distill's licence is open, but each article has different authors, so it cannot train a single voice; it could serve as a small supplement or evaluation set.
- Tao's wording allows "reasonable portions" and asks for contact before copying whole series. A whole-blog corpus is beyond that, so it needs his consent.

### Gaps
- The Creative Commons deeds and CC's own guidance on AI training were not re-read this session; the licence-scope points above are inferences from the standard terms, not quotes.
- Pluralistic (Cory Doctorow) is widely described as CC BY 4.0, but neither the home page nor the one post fetched showed a licence statement for the text, so it is unverified. Only a secondary, AI-generated page asserted it. — [pluralistic.net](https://pluralistic.net/)
- Derek Lowe's In the Pipeline is hosted by Science/AAAS; science.org returned HTTP 403, so the terms could not be read. Treat as publisher-owned and not usable until checked.
- Michael Nielsen's "Neural Networks and Deep Learning" could not be fetched (certificate error), so its licence is unverified.
- Paul Graham's and Dan Luu's sites were checked only at the index page; a licence elsewhere on the site cannot be ruled out, but none was found.
- Whether the SSC footer or individual posts carry any different notice was not seen (page truncated).
- Substack's platform terms for ACX were not read.

## AI and crawling stance

### Takeaway
Gwern is the only candidate who actively invites training: the robots.txt carries `ai-train=yes` and he has written that he would pay to be in training corpora. Julia Evans and Jeremy Kun signal the opposite, and Stratechery bans data mining by contract; most others say nothing.

### Cited Findings
- Gwern.net robots.txt ends with "Content-Signal: search=yes, ai-input=yes, ai-train=yes" (marked "Experimental"). No AI crawler is blocked; only `ia_archiver` is restricted, and `/fulltext`, `/metadata/*`, `/doc/www/*` and similar paths are disallowed for all bots. — [gwern.net/robots.txt](https://gwern.net/robots.txt)
- Gwern, 2024-08-21: "I would, in fact, pay money to ensure Gwern.net is in training corpuses"; "Much of the value of writing done recently or now is simply to get stuff into LLMs." — [gwern.net/blog/2024/writing-online](https://gwern.net/blog/2024/writing-online)
- Julia Evans: robots.txt shows ASCII art reading "NO LLM PLZ" and sets "Disallow: /" for GPTBot and Google-Extended, while allowing all other crawlers. — [jvns.ca/robots.txt](https://jvns.ca/robots.txt)
- Jeremy Kun: About page text forbids AI systems from using the content (quoted in the licence section). — [jeremykun.com/about](https://www.jeremykun.com/about/)
- Stratechery: robots.txt blocks only `/wp-admin/`, but the ToS forbids "scraping, data mining, data extraction and data harvesting". — [stratechery.com/robots.txt](https://stratechery.com/robots.txt), [stratechery.com/terms-of-service](https://stratechery.com/terms-of-service/)
- Simon Willison: robots.txt explicitly allows ChatGPT-User (empty Disallow) and blocks only `/admin/` and `/search/` for everyone. — [simonwillison.net/robots.txt](https://simonwillison.net/robots.txt)
- Astral Codex Ten: robots.txt names no AI crawler; only BLEXBot is fully disallowed, and the wildcard block covers Substack utility paths. — [astralcodexten.com/robots.txt](https://www.astralcodexten.com/robots.txt)
- Wait But Why: robots.txt disallows nothing. — [waitbutwhy.com/robots.txt](https://waitbutwhy.com/robots.txt)
- Better Explained: robots.txt blocks only `/wp-admin/`; no AI crawler named. — [betterexplained.com/robots.txt](https://betterexplained.com/robots.txt)
- Paul Graham: robots.txt blocks some CGI and short-named paths and one bot (Roverbot); no AI crawler named. — [paulgraham.com/robots.txt](https://www.paulgraham.com/robots.txt)
- Dan Luu: robots.txt is an unrendered Jekyll template containing only a Sitemap line; no rules. — [danluu.com/robots.txt](https://danluu.com/robots.txt)
- John D. Cook: robots.txt lists two sitemaps and no rules. — [johndcook.com/robots.txt](https://www.johndcook.com/robots.txt)
- Distill.pub: robots.txt returns 404. — [distill.pub/robots.txt](https://distill.pub/robots.txt)
- Terence Tao: the About page has a policy on AI-generated comments but says nothing on training on the blog. — [terrytao.wordpress.com/about](https://terrytao.wordpress.com/about/)
- Cory Doctorow: "Web-scraping is good, actually."; he argues creators have "been duped into taking up arms against scraping and training, rather than unfair labor practices." — [pluralistic.net, 17 Sep 2023](https://pluralistic.net/2023/09/17/how-to-think-about-scraping/)
- Dynomight states a human-only writing rule: "not a single word can be cut and pasted from AI into a post, ever." Nothing on training. — [dynomight.net/ai](https://dynomight.net/ai/)

### Inferences
- Gwern's licence, robots signal and stated wish all point the same way, which makes it the lowest-risk candidate on consent as well as on law.
- Julia Evans' robots.txt names only two bots, but the banner makes her preference plain. A project that puts permission first should treat it as a refusal even though a local fine-tune involves no crawler.
- Absence of AI blocks in robots.txt (ACX, WBW, PG, Dan Luu, Cook) is not permission; it only means no objection was recorded there.

### Gaps
- No ai.txt, TDM-reservation headers or `noai` meta tags were checked for any site; the fetch tool does not expose response headers or page metadata.
- slatestarcodex.com/robots.txt returned an empty body, so its crawler rules are unknown.
- No statement on AI training was found from Scott Alexander, Paul Graham, Dan Luu, Tim Urban, Ciechanowski, Amit Patel, Kalid Azad, Kaspar Etter or Alexey Guzey. Searches for Julia Evans and Simon Willison statements returned nothing relevant beyond the robots.txt files.
- robots.txt was not fetched for Red Blob Games, ciechanow.ski, Evan Miller, Tao, Lilian Weng, colah, Karpathy, Shalizi, ef1p or Guzey.

## Size: words and post counts

### Takeaway
Gwern.net is far above the 300,000-word bar, and SSC almost certainly is too once open threads and link posts are removed. The other openly licensed single-author sites (ef1p, Guzey, Jay Alammar) are small or unmeasured.

### Cited Findings
- Gwern.net: "As of 2022-11-08, the source of Gwern.net is composed of >443 text files with >4.38m words or >31MB". — [gwern.net/about](https://gwern.net/about)
- Slate Star Codex: an e-book of all posts runs "over nine thousand pages" as a PDF, per The New Yorker as relayed by a Wikipedia-derived page (secondary source). — [wikiwand.com/en/articles/Slate_Star_Codex](https://www.wikiwand.com/en/articles/Slate_Star_Codex)
- SSC archive: about 1,000 posts were visible between April 2017 and January 2021 before the page was truncated; roughly half of those are Open Threads or Links posts (the fetch tool's estimate). The last post is "Introducing Astral Codex Ten" (21 Jan 2021). — [slatestarcodex.com/archives](https://slatestarcodex.com/archives/)
- Better Explained: 187 articles, 13 Sep 2006 to 3 Aug 2022. — [betterexplained.com/archives](https://betterexplained.com/archives/)
- Paul Graham: 235 items on the essay index, two of them book chapters. — [paulgraham.com/articles.html](https://www.paulgraham.com/articles.html)
- Dan Luu: 205 posts listed, 122 public and 83 Patreon-only, from 09/2013 to 11/2026. — [danluu.com](https://danluu.com/)
- Julia Evans: roughly 600-700 posts, December 2012 to September 2026 (estimate, some double-counted across categories). — [jvns.ca](https://jvns.ca/)
- Bartosz Ciechanowski: 22 articles, 2014 to December 2024. — [ciechanow.ski/archives](https://ciechanow.ski/archives/)
- Explained from First Principles: 3 articles (The Internet, 2020; Email, 2021; Number theory, 2022). — [explained-from-first-principles.com](https://explained-from-first-principles.com/)
- Guzey.com: 97 linked items, some of them Google Docs, PDFs and tweets. — [guzey.com](https://guzey.com/)
- Jay Alammar: 26 posts. — [jalammar.github.io](https://jalammar.github.io/)
- Evan Miller: 71 writing entries, about 66 essays. — [evanmiller.org](https://www.evanmiller.org/)
- Chris Olah: 17 posts on the blog itself, 2014-2020. — [colah.github.io](https://colah.github.io/)
- Karpathy: 23 posts, 2011-2026. — [karpathy.github.io](https://karpathy.github.io/)
- Red Blob Games: 19 guides under "Learn" plus 43 blog posts from March 2024 to November 2026. — [redblobgames.com](https://www.redblobgames.com/), [redblobgames.com/blog](https://www.redblobgames.com/blog/)
- Lilian Weng: the 10 newest posts carry reading times of 20-40 minutes each. — [lilianweng.github.io](https://lilianweng.github.io/)

### Inferences
- Gwern's 4.38M words include every text file in the site source, which covers link pages, newsletters, fiction, poetry and heavily quoted material. The explanatory essays that fit the target register are a subset; even a tenth of the total would exceed 300,000 words.
- Nine thousand PDF pages at a typical 300-500 words per page puts SSC at roughly 3-4 million words. If half the posts are open threads and links (which are short), the essay corpus is still well over a million words.
- Better Explained at 187 articles is probably 200,000-350,000 words if articles average 1,000-2,000 words. That is near the bar, not clearly over it.
- The three ef1p articles are each very long, but three documents give little topical variety, which matters for style generalisation.
- Ciechanowski, Olah, Karpathy, Jay Alammar and Evan Miller are each too small to stand alone whatever their licence.

### Gaps
- No word counts were measured; doing so would mean downloading the corpora, which the brief ruled out. All word figures other than Gwern's are estimates.
- No size basis was found for ACX, Stratechery, Wait But Why, Simon Willison, Tao, John D. Cook, Shalizi, Derek Lowe, Distill or 3Blue1Brown's written lessons.
- The SSC post count before April 2017 was not seen.

## Register: fit with plain, concrete, modern explanatory prose

### Takeaway
None of the openly licensed large corpora is a clean match. Gwern is dense, footnoted and idiosyncratic; SSC is first-person argument and opinion more than neutral explanation. The closest register matches (Better Explained, Ciechanowski, Red Blob Games, Julia Evans) are the ones with licence or consent problems.

### Cited Findings
- Gwern.net describes itself: "I write about AI, psychology, & statistics." — [gwern.net/llms.txt](https://gwern.net/llms.txt)
- Gwern.net source files are written in Pandoc Markdown. — [gwern.net/design](https://gwern.net/design)
- Ciechanowski's titles are single-topic physical explainers: "Mechanical Watch", "GPS", "Internal Combustion Engine", "Cameras and Lenses", "Sound", "Bicycle", "Airfoil", "Moon". — [ciechanow.ski/archives](https://ciechanow.ski/archives/)
- Explained from First Principles covers "The Internet", "Email" and "Number theory". — [explained-from-first-principles.com](https://explained-from-first-principles.com/)
- Lilian Weng's posts are long ML literature surveys (20-40 minute reads) such as "Prompt Engineering" and "Diffusion Models for Video Generation". — [lilianweng.github.io](https://lilianweng.github.io/)
- Karpathy's index mixes explainers ("The Unreasonable Effectiveness of Recurrent Neural Networks", "A Recipe for Training Neural Networks") with short stories and personal posts. — [karpathy.github.io](https://karpathy.github.io/)
- Distill articles pair text with interactive diagrams whose code is separately MIT-licensed. — [distill.pub/faq](https://distill.pub/faq/)

### Inferences
The judgements below rest on general familiarity with these sites, not on fresh sample reads this session. They should be confirmed by reading five to ten pieces per shortlisted author before committing.
- Gwern: long, heavily hedged and footnoted essays with block quotes, sidenotes, statistics and code. Concrete and precise, but not plain; sentences are long and the voice is distinctive. Needs filtering to the expository essays and stripping of quotes and annotations.
- SSC: conversational first-person essays, book reviews, argument and satire, plus "Much More Than You Wanted To Know" evidence reviews that are close to the target. Clear and readable, but opinionated and discursive; fiction, link posts and open threads must be dropped.
- Better Explained: short, plain, analogy-led maths explanations in second person. Very close to the target for maths walkthroughs; some equations will need handling.
- Ciechanowski and Red Blob Games: excellent plain explanation, but the prose leans on interactive figures ("drag the slider"), so text alone loses referents.
- Explained from First Principles: neutral, textbook-like technical explanation with little first person. Strong register match; small document count.
- Julia Evans: plain and concrete, but chatty, first-person and code-heavy.
- Simon Willison: much of the volume is link-blog commentary and quotes of others; the long pieces are first-person technical notes.
- Paul Graham: plain style, but opinion essays, not explanation.
- Dan Luu: data-heavy technical argument, long footnotes, first person.
- Wait But Why: jokey, long-form, drawing-dependent; not a plain register.
- Stratechery: business analysis with long block quotes of other sources.
- Tao, Jeremy Kun, John D. Cook, Lilian Weng, Colah: mathematics notation or code carries much of the content; Cook's posts are very short.
- Shalizi: erudite, allusive, opinionated; poor match.
- Guzey: essays, critiques and personal notes; mixed.
- Derek Lowe: plain, wry chemistry and pharma commentary; a good news-explainer register if it were licensable.

### Gaps
- No systematic register sampling was done for any candidate.
- How much of Gwern's or SSC's corpus survives a filter for "explanatory, non-opinion" prose is unknown without reading the corpus.

## Dates: share written before December 2022

### Takeaway
SSC (2013 to January 2021) and Better Explained (2006 to August 2022) are entirely pre-LLM. Gwern has a documented 4.38M-word snapshot dated 8 November 2022, so a pre-December-2022 cut is easy to define.

### Cited Findings
- SSC's final post, "Introducing Astral Codex Ten", is dated 21 Jan 2021. — [slatestarcodex.com/archives](https://slatestarcodex.com/archives/)
- Better Explained: newest article 3 Aug 2022; none dated 2023 or later. — [betterexplained.com/archives](https://betterexplained.com/archives/)
- Gwern.net: >4.38M words as of 2022-11-08. — [gwern.net/about](https://gwern.net/about)
- Explained from First Principles: all three articles dated 2020-2022. — [explained-from-first-principles.com](https://explained-from-first-principles.com/)
- Ciechanowski: 19 of 22 articles predate December 2022 (Bicycle, Airfoil and Moon are later). — [ciechanow.ski/archives](https://ciechanow.ski/archives/)
- Dan Luu: 48 of 205 posts are dated 2023 or later (22 of the 122 public ones). — [danluu.com](https://danluu.com/)
- Chris Olah's blog posts run 2014-2020. — [colah.github.io](https://colah.github.io/)
- Karpathy: 22 of 23 posts predate 2023. — [karpathy.github.io](https://karpathy.github.io/)
- Red Blob Games' new blog began in March 2024; the guides are older. — [redblobgames.com/blog](https://www.redblobgames.com/blog/)
- Lilian Weng: 8 of the 10 newest posts are from 2023 or later. — [lilianweng.github.io](https://lilianweng.github.io/)
- Julia Evans has posted from 2012 through September 2026. — [jvns.ca](https://jvns.ca/)

### Inferences
- For Gwern, restricting to pages created or last substantially edited before December 2022 is prudent, because he writes openly about using LLMs and continues to revise old pages.
- ACX is entirely post-January-2021; roughly its first two years predate December 2022.

### Gaps
- Gwern pages carry created and modified dates, but whether a pre-2023 revision of each page can be retrieved was not checked.
- Paul Graham's and Evan Miller's index pages show no dates, so their pre-2023 share was not measured.
- No evidence was found either way on whether any of these authors use LLMs to draft, other than Dynomight's statement that he does not.

## Extraction: how easy is clean text?

### Takeaway
Gwern.net and SSC are both static or server-rendered HTML with stable archive pages, and Gwern's site is authored in Pandoc Markdown with a public GitHub presence. No official text dump was confirmed for any candidate.

### Cited Findings
- Gwern.net source is Pandoc Markdown; bugs are reported at the `gwern/gwern.net` GitHub repository. — [gwern.net/design](https://gwern.net/design)
- Gwern.net publishes a sitemap and an `llms.txt` that serves as a categorised essay index; search results also show an `llms-full.txt`. — [gwern.net/robots.txt](https://gwern.net/robots.txt), [gwern.net/llms.txt](https://gwern.net/llms.txt), [gwern.net/llms-full.txt](https://gwern.net/llms-full.txt)
- Gwern.net robots.txt disallows `/metadata/*` and `/doc/www/*` (annotations and local mirrors of other people's pages). — [gwern.net/robots.txt](https://gwern.net/robots.txt)
- SSC has a single archive page listing every post by date. — [slatestarcodex.com/archives](https://slatestarcodex.com/archives/)
- Better Explained has a posts-by-date archive and a WordPress sitemap. — [betterexplained.com/archives](https://betterexplained.com/archives/), [betterexplained.com/robots.txt](https://betterexplained.com/robots.txt)
- Explained from First Principles links a GitHub repository, `KasparEtter/ef1p`. — [explained-from-first-principles.com](https://explained-from-first-principles.com/)
- Distill article source is "available on GitHub". — [distill.pub/2017/momentum](https://distill.pub/2017/momentum/)
- Julia Evans publishes an Atom feed and sitemap. — [jvns.ca/atom.xml](https://jvns.ca/atom.xml), [jvns.ca/robots.txt](https://jvns.ca/robots.txt)
- Simon Willison's blog engine is public (Apache-2.0), but the README does not mention a content dump. — [github.com/simonw/simonwillisonblog](https://github.com/simonw/simonwillisonblog)
- Dan Luu's 83 Patreon posts are separated from the 122 public ones. — [danluu.com](https://danluu.com/)
- Stratechery restricts member RSS feeds: "you may not share that feed or use it in any application other than an RSS feed reader." — [stratechery.com/terms-of-service](https://stratechery.com/terms-of-service/)

### Inferences
- The Gwern corpus is CC0 only for Gwern's own writing. Pages contain long quotations, annotations of other people's papers and mirrored documents, which stay under their original copyright; extraction must keep to essay body text and strip block quotes, and should stay away from `/doc/` and `/metadata/`.
- SSC extraction needs filters for open threads, link round-ups, guest posts, comment sections and quoted passages. Comments are by other people and are not covered by the author's licence in any obvious way.
- Gwern's sidenotes, collapsed sections and popup annotations make HTML-to-text messier than SSC's plain WordPress pages; working from the Markdown source would be cleaner if it is retrievable.

### Gaps
- Whether the `gwern/gwern.net` repository contains the essay Markdown, or only site code, was not confirmed; nor was whether each page's source can be fetched directly (for example by a `.md` URL).
- Whether an author-sanctioned SSC e-book or dump exists was not confirmed; third-party compilations exist according to press reports, but their status is unknown.
- `llms-full.txt` on Gwern.net was seen only in search results and not opened.

## Memorization risk

### Takeaway
The best-licensed candidates are also among the most widely read and scraped blogs on the web, so base models have very likely seen them. This is a real cost for Gwern and SSC, and one the author of Gwern.net deliberately seeks.

### Cited Findings
- Gwern wants his site in training data: "I would, in fact, pay money to ensure Gwern.net is in training corpuses". — [gwern.net/blog/2024/writing-online](https://gwern.net/blog/2024/writing-online)
- Gwern's "Writing for LLMs So They Listen" advises making writing as available and scrapeable as possible (as summarised in search results; page not opened). — [gwern.net/llm-writing](https://gwern.net/llm-writing)
- SSC was prominent enough for a New Yorker feature that discussed the full e-book of its posts (secondary source). — [wikiwand.com/en/articles/Slate_Star_Codex](https://www.wikiwand.com/en/articles/Slate_Star_Codex)
- Better Explained reports 450k monthly visitors. — [betterexplained.com/about](https://betterexplained.com/about/)

### Inferences
- Gwern.net and SSC are almost certainly in every large model's pretraining data. For a style adapter this matters less than for a factual benchmark, but it weakens any evaluation that asks whether the model "learned" the style from the fine-tune, and it raises the chance of verbatim recall on well-known passages. A recall probe like the one used on the previous corpus should be repeated.
- Paul Graham's essays and the most famous Wait But Why, Karpathy, Colah and Jay Alammar posts carry the same risk.
- Explained from First Principles, Guzey and Better Explained are less copied, so lower risk; Better Explained's best-known articles are the exception.

### Gaps
- No direct measurement of memorization was found or made for any candidate. All statements here are inferences from popularity.

## One-line verdicts

### Takeaway
Two candidates are usable today without asking anyone: Gwern.net (CC0, author invites training) and Slate Star Codex (CC BY 4.0, attribution required). Both need heavy filtering to reach the target register, and both are probably memorised by base models.

### Cited Findings
Each verdict rests on the sources cited in the sections above; the deciding fact is repeated here.
- Gwern.net: usable now. CC0 plus `ai-train=yes`; >4.38M words by Nov 2022. Costs: dense footnoted register, quoted third-party text to strip, high memorization. — [gwern.net/about](https://gwern.net/about), [gwern.net/robots.txt](https://gwern.net/robots.txt)
- Slate Star Codex (2013-2021): usable now with attribution. CC BY 4.0 on the About page; all pre-2022. Costs: opinionated first-person register, half the posts are threads or links, high memorization. — [slatestarcodex.com/about](https://slatestarcodex.com/about/)
- Astral Codex Ten: usable with consent only. "© 2026 Scott Alexander", no licence. — [astralcodexten.com/about](https://www.astralcodexten.com/about)
- Explained from First Principles: usable now with attribution. CC BY 4.0, strong register match, but only three articles; best as a supplement. — [explained-from-first-principles.com](https://explained-from-first-principles.com/)
- Guzey.com: usable now with attribution. CC BY 4.0, 97 items, mixed register; supplement at most. — [guzey.com](https://guzey.com/)
- Distill.pub: usable now with attribution, but multi-author and figure-dependent; not a single-voice corpus. — [distill.pub/2017/momentum](https://distill.pub/2017/momentum/)
- Better Explained: usable for a private non-commercial model; ask Kalid Azad before publishing an adapter or any commercial use. CC BY-NC-SA, 187 articles, all pre-2023, best register match for maths. — [betterexplained.com/about](https://betterexplained.com/about/)
- Jay Alammar: same NC/SA limits; 26 posts, too small. — [jalammar.github.io](https://jalammar.github.io/)
- Terence Tao: usable with consent. He asks to be contacted before large copying. — [terrytao.wordpress.com/about](https://terrytao.wordpress.com/about/)
- Wait But Why: usable with consent. Permission by email is required for full posts; register is a poor fit anyway. — [waitbutwhy.com/sharing-policy](https://waitbutwhy.com/sharing-policy/)
- Julia Evans: not usable without consent, and consent looks unlikely. "© Julia Evans" and "NO LLM PLZ". — [jvns.ca/robots.txt](https://jvns.ca/robots.txt)
- Jeremy Kun: not usable. Page text forbids AI use. — [jeremykun.com/about](https://www.jeremykun.com/about/)
- Stratechery: not usable. ToS bans data mining and republication; paywalled. — [stratechery.com/terms-of-service](https://stratechery.com/terms-of-service/)
- 3Blue1Brown written lessons: not usable without consent. All rights reserved. — [3b1b/3Blue1Brown.com License.md](https://raw.githubusercontent.com/3b1b/3Blue1Brown.com/main/License.md)
- Simon Willison: usable with consent. No licence; no AI blocks. — [simonwillison.net/about](https://simonwillison.net/about/)
- Paul Graham: usable with consent. No licence found; opinion register; heavily memorised. — [paulgraham.com/articles.html](https://www.paulgraham.com/articles.html)
- Dan Luu: usable with consent. No licence found. — [danluu.com](https://danluu.com/)
- Bartosz Ciechanowski: usable with consent. Copyright notice only; 22 figure-dependent articles, too small. — [ciechanow.ski/archives](https://ciechanow.ski/archives/)
- Red Blob Games: usable with consent. Copyright notice; only code is open. — [redblobgames.com](https://www.redblobgames.com/)
- Evan Miller, John D. Cook, Lilian Weng, Chris Olah, Karpathy, Shalizi, Dynomight, Cold Takes, Nintil: usable with consent only; no licence found on the pages checked. — sources in the licence section
- Derek Lowe: not verified; treat as not usable. — [science.org terms (403)](https://www.science.org/content/page/terms-service)

### Inferences
- If the project wants one corpus with no permission step, the choice is between Gwern.net and SSC. SSC is closer to plain modern prose; Gwern is closer to careful explanation but less plain. A filtered SSC subset (the evidence-review and explainer posts) is probably the nearest lawful fit, with ef1p as a small, cleaner supplement.
- If the project is willing to ask, Kalid Azad (Better Explained) is the most promising request: the register fits, the corpus is entirely pre-LLM, the licence is already permissive for non-commercial use, and he invites contact.
- Mixing several CC BY / CC0 authors would raise volume and dilute any single voice; that is a design decision for the project, not something these notes settle.

### Gaps
- Consent likelihood was not tested for anyone; no author was contacted.
- Verdicts for sites checked only at their index page (Paul Graham, Dan Luu, Nintil, Cold Takes, Shalizi) would change if a licence exists on a page not read.
