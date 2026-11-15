# Institutional, journalistic and educational open-licence publishers as candidate training corpora

Research date: 2026-11-13. Method: licence, terms and robots.txt pages were fetched directly where the server allowed it. No corpus was crawled or downloaded.

Read this first (reliability notes):
- "Verified" below means I fetched the publisher's own page in this session. The fetch tool returns quotes as short fragments (about 125 characters each), so quoted strings are exact fragments, not full clauses. Re-read the linked page before relying on any clause.
- Several pages refused the fetch (HTTP 403 or 404): Knowable republish and about pages, Cochrane Library copyright page, PLOS terms and licence pages, Khan Academy terms and help article, LibreTexts legal page, Carpentries licence pages on carpentries.org, OpenStax licensing blog post. For those, the status is marked "not verified directly" and comes from search snippets or a secondary page.
- Items marked "recollection" come from my own background knowledge and were not confirmed in this session.
- Not researched at all (no fetch attempted): Scientific American, Vox, Wikipedia Signpost licence page, PLOS blogs licence page, Aeon robots.txt, Undark AI policy page.

## 1. Licence: which licence, what it covers, and what it means for training, README samples and adapter weights

### Takeaway
The cleanly open (CC BY or equivalent) sources verified in this session are Our World in Data, Wikinews, Global Voices, EFF, eLife, Science Journal for Kids and The Carpentries; PLOS is CC BY 4.0 per its journal licence pages (seen through search only). Three premises in the brief were wrong or outdated: OpenStax's help centre now states CC BY-NC-SA 4.0 (not CC BY), Aeon's republish page offers no CC licence (paid republication), and Undark uses its own republishing terms with no CC licence. Quanta, Khan Academy and Cochrane are not open for this use.

### Cited Findings

Creative Commons general position (applies to every CC source below):
- CC FAQ: "The licenses grant permission for reuse in any situation that requires permission under copyright." and, for new technology, "then the CC license allows that use without the need to seek permission from the copyright owner" "so long as the license conditions are respected." — [CC FAQ](https://creativecommons.org/faq/)
- CC FAQ on ShareAlike in the AI context: "Regarding ShareAlike, the condition only applies if a work is modified and if the work is shared publicly." — [CC FAQ](https://creativecommons.org/faq/)
- CC FAQ on NoDerivatives: "The NoDerivatives licenses do not permit remixing except for private use"; and for data, "If a ND is applied, you may produce an adapted database but cannot share it publicly." — [CC FAQ](https://creativecommons.org/faq/)
- CC FAQ on NonCommercial: the test is whether uses "are primarily intended for commercial advantage or monetary compensation." — [CC FAQ](https://creativecommons.org/faq/)
- CC FAQ on attribution in datasets: "Where a CC-licensed work is distributed as part of a database or dataset," "then the license conditions must be respected." — [CC FAQ](https://creativecommons.org/faq/)
- The CC FAQ text retrieved did not state whether a trained model or its outputs count as an adaptation. — [CC FAQ](https://creativecommons.org/faq/)

Our World in Data (OWID):
- Article footer: "All visualizations, data, and articles produced by Our World in Data are completely open access" "under the Creative Commons BY license." "You have the permission to use, distribute, and reproduce these in any medium, provided the source and authors are credited." Third-party data is excluded: "subject to the license terms" "from the original third-party authors." — [OWID sample article](https://ourworldindata.org/much-better-awful-can-be-better)
- FAQ links the licence to CC BY 4.0 and says of text: "You can republish or reproduce our writing, online or in print, for free and without permission." The same FAQ also carries the line "You must not edit the material, except to reflect relative changes in time, location and editorial style." Logo use and the Grapher software are excluded ("the Grapher is not freely licensed for reuse without permission."). No mention of AI or machine learning. — [OWID FAQ](https://ourworldindata.org/faqs)

Quanta Magazine:
- Terms (Simons Foundation): "These Terms permit you to use the Site for your personal, non-commercial use only." "You must not reproduce, distribute, modify, create derivative works of, publicly display, publicly perform," "republish, download, store, or transmit any of the material on our Site, other than as permitted by law." "You must not conduct any systematic or automated data collection activities" "(including, without limitation, scraping, data mining, data extraction and data harvesting)". No open licence; no explicit AI clause. — [Quanta Terms & Conditions](https://www.quantamagazine.org/terms-conditions/)

The Conversation:
- "publish all our work under a Creative Commons — Attribution/No Derivatives license" (link target is by-nd/4.0). "You can't edit our material, except to reflect relative changes in time, location and editorial style." "You can't systematically republish all of our articles." "Commercial, non-journalism usage: license fees may apply." Images excluded: "You have to confirm you're licensed to republish images in our articles." No mention of AI or data mining on the page. — [The Conversation republishing guidelines](https://theconversation.com/us/republishing-guidelines)

ProPublica:
- Page links to CC BY-NC-ND 3.0 US (version inferred from the link URL, not page text). "You can't edit our material, except to reflect relative changes in time, location and editorial style." "You can't republish our material wholesale, or automatically; you need to select stories to be republished individually." "You cannot republish our photographs or illustrations without specific permission." No AI or scraping clause; the page notes "publishers cannot fully control when certain third parties automatically summarize or crawl content." — [ProPublica Steal Our Stories](https://www.propublica.org/steal-our-stories)

Wikinews:
- Material after December 16, 2024: "licensed under the terms of the Creative Commons Attribution 4.0 License". Material published after September 25, 2005 and before that date: CC BY 2.5. Before September 25, 2005: "is in the public domain." Images: "Copyright on images may vary, please check individual image pages prior to duplication." Attribution: "This work may be attributed to "Wikinews"." — [Wikinews:Copyright](https://en.wikinews.org/wiki/Wikinews:Copyright)

Wikipedia featured articles, Simple English Wikipedia, Wikibooks (same Terms of Use):
- Text is under "Creative Commons Attribution-ShareAlike 4.0 International License" ("CC BY-SA 4.0") and the GFDL; reusers may comply with either. "Reuse of content that we host is welcome," but "Any reuse must comply with the underlying license(s)." Attribution for text can be a link to the page or a list of authors. Modified content must be licensed "CC BY-SA 4.0 or later". The Terms of Use text does not mention AI or LLM training. — [Wikimedia Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use)

Khan Academy:
- A Khan Academy help-centre guideline (seen only as a search snippet; the page returned 403) lists as prohibited using scraping tools or bots to copy data from the site and using Khan Academy content or data to train, test or develop AI or machine learning models. — [Khan Academy help article](https://support.khanacademy.org/hc/de/articles/42929097425037)
- Khan Academy support says a CC BY-NC-SA licence governs reuse of its videos and exercises outside the site; the terms distinguish CC-licensed content from non-CC partner content. — [Khan Academy support](https://support.khanacademy.org/hc/en-us/articles/202262954-Can-I-use-Khan-Academy-s-videos-name-materials-links-); [Khan blog, Terms of Service update](https://blog.khanacademy.org/terms-of-service-update)

OpenStax:
- "OpenStax textbooks are published under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license." The page lists "Creative Commons BY-NC-SA 4.0" and asks reusers to "Credit OpenStax, include the book title, and link to the free version." — [OpenStax help: licensing information](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks)
- OpenStax help on AI: content "may be used with AI tools for noncommercial educational purposes" if the licence is followed; you "may use AI to summarize, adapt, create study materials, change reading level, or translate content." The retrieved text did not address model training. — [OpenStax help: using content with AI tools](https://help.openstax.org/0TO6f0000003F84GAE)
- Another OpenStax help page says it publishes under two licence types, CC BY and CC BY-NC-SA (search snippet). — [OpenStax help: textbook licensing and customization](https://help.openstax.org/s/article/Openstax-textbook-licensing-and-customization)

MIT OpenCourseWare:
- "Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)". "Non-commercial use means that users may not sell, profit from, or commercialize OCW materials or works derived from them." Explicit AI section, "Permitted Use of AI Training": "OCW content may be used to train, develop, and improve artificial intelligence and machine learning models"; "Non-commercial means not primarily intended for or directed towards commercial advantage or monetary compensation."; the page refers to "Any derivative models, or AI systems that incorporate OCW Content through training"; "Any commercial application of OCW content through AI training is strictly prohibited." — [MIT OCW terms](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)

Cochrane plain-language summaries:
- Reuse runs through permissions, not an open licence: the Cochrane Library uses RightsLink for permissions, and only registered Cochrane groups may re-publish plain language summaries without contacting the publisher (search snippet; copyright page returned 403). — [Cochrane Library permissions](https://cochranelibrary.com/en/help/permissions)

Knowable Magazine:
- About page (search snippet; page returned 403) says content is published under a CC BY-ND copyright licence and encourages republication under its guidelines. Version number not seen. — [Knowable about](https://knowablemagazine.org/about)

Aeon:
- No CC licence on the republish page. "Essays may only be republished after entering into an agreement with us." Fee "$650 USD". "Psyche Ideas are available for republication for USD 350." "Psyche Guides are NOT available for republication." — [Aeon republish](https://aeon.co/republish)

Undark:
- No CC licence named; own terms, last updated 10/1/2023. Only stories with a "Republish" link qualify: "If you do not see the word "Republish," then it is very likely that this piece is not available for re-use." Stories older than 90 days need the author's permission. No selling, no republishing all articles, permission revocable. — [Undark republishing guidelines](https://undark.org/republishing-guidelines/)

Mongabay:
- Articles are under a "Creative Commons Attribution-NoDerivatives 4.0 International License". Edits limited to "relative changes in time, location, or basic editorial style." No translation without permission; no paywalls; "you must link to the original story and include the original links embedded in the story." Third-party photos need permission. No AI mention. — [Mongabay Creative Commons page](https://news.mongabay.com/copyright/creative-commons/)
- The general terms page is more restrictive (viewing for "personal, informational, and non-commercial purposes only" unless a page says otherwise). — [Mongabay terms](https://news.mongabay.com/terms/)

Carbon Brief:
- Site footer (search snippet; my direct fetches did not return the footer) says content is published under a CC licence and may be reproduced unadapted, in full, for non-commercial use with credit and a link; commercial use needs contact. The exact licence name and version were not confirmed. — [Carbon Brief](https://www.carbonbrief.org/regions)

Global Voices:
- "This site is licensed as Creative Commons Attribution 3.0." "Unless otherwise stated, all content created by Global Voices is published under a Creative Commons Attribution-Only license." Third-party media excluded: "Photos, video, audio sourced from other creators may not always be available on the same terms." — [Global Voices attribution policy](https://globalvoices.org/about/global-voices-attribution-policy/)
- AI policy covers its own writing (it will not accept "automatically generated" text; "Relying on LLMs to do the writing or translation" risks its principles). It does not grant or deny training on its content, though it speaks of "respect for the authors and illustrators whose work was used without permission". — [Global Voices policy on AI](https://globalvoices.org/about/global-voices-policy-on-ai/)

EFF Deeplinks:
- Original EFF material is under "Creative Commons Attribution 4.0 International License (CC-BY)" "unless otherwise noted"; the badge on the same page links to CC BY 3.0 US. "Permission to do such things is explicitly granted." "it is appreciated if you make it known where the file originated." "All material that is not original to EFF may require permission from the copyright holder to redistribute." No AI clause. — [EFF copyright policy](https://www.eff.org/copyright)

eLife (digests and articles):
- Articles are "licensed under a Creative Commons Attribution license" (link target CC BY 4.0), "subject to citation of the original source", "except where otherwise noted." Terms page mentions neither text mining nor AI, and does not name digests separately. — [eLife terms](https://elifesciences.org/terms)
- The official XML repository states articles are open access under CC BY or CC0. — [elife-article-xml](https://github.com/elifesciences/elife-article-xml)

PLOS (articles with "author summary" sections):
- PLOS journal licence pages (seen through search; plos.org pages returned 403) say PLOS applies CC BY 4.0, that anyone may reuse content in whole or part for any purpose, including commercially, with citation, and that this ensures content "can be mined without barriers". Third-party images and tables can carry other terms. — [PLOS ONE content licence](https://journals.plos.org/plosone/s/content-license); [PLOS Biology licences and copyright](https://journals.plos.org/plosbiology/s/licenses-and-copyright)
- PLOS released the "allofplos" corpus for unrestricted text and data mining. — [PLOS blog, allofplos](https://theplosblog.plos.org/2017/11/unrestricted-text-and-data-mining-with-allofplos/)

Science Journal for Kids:
- "Science Journal for Kids applies the Creative Commons Attribution (CC BY) license to all works we publish." (link target CC BY 4.0). "Anyone may copy, distribute or reuse these articles, as long as the author and original source are properly cited." "Figures, tables, and images are also published under the Creative Commons Attribution (CC BY) license." No AI clause on this page; a separate "AI Disclosure Policy" exists and was not read. — [SJK content licence](https://www.sciencejournalforkids.org/content-license.html)

The Carpentries:
- Lesson repository licence file: "All Carpentries (Software Carpentry, Data Carpentry, and Library Carpentry) instructional material" "is made available under the Creative Commons Attribution license." (CC BY 4.0). Attribution: "You must give appropriate credit (mentioning that your work is derived from work that is Copyright (c) The Carpentries" and "where practical, linking to https://carpentries.org/)". Software is MIT. — [swcarpentry/shell-novice LICENSE](https://github.com/swcarpentry/shell-novice/blob/main/LICENSE.md)

Extra candidates found:
- Congressional Research Service reports: EveryCRSReport hosts 23,620 reports with bulk download; the page did not itself state copyright status. — [EveryCRSReport about](https://www.everycrsreport.com/about.html)
- US federal definition: "Government work is something created by a U.S. government officer or employee as part of their official duties."; federal sites may also contain third-party material. — [USA.gov government copyright](https://www.usa.gov/government-copyright)
- Frontiers for Young Minds: the journal page describes "freely available scientific articles" written by scientists and reviewed by "Kids and teens between the ages of 8-15", with 5,410 authors listed; the page did not state a licence. — [Frontiers for Young Minds](https://kids.frontiersin.org/about/journal)
- Leads from search snippets only: Climate Feedback (CC BY 4.0), Inside Climate News (CC BY-NC-ND 3.0), Dialogue Earth and SAPIENS (republishing pages exist). — [Climate Feedback republishing](https://climatefeedback.org/?p=7217); [Inside Climate News republishing](https://insideclimatenews.org/republishing-guidelines/); [Dialogue Earth republishing](https://dialogue.earth/en/republishing/); [SAPIENS terms](https://sapiens.org/terms-use)

### Inferences
What the licence elements mean for the three uses. None of this is settled law; it is my reading of the CC FAQ passages above plus the licence texts.
- (a) Fine-tuning a private local model. CC BY, CC BY-SA, CC BY-ND 4.0 and CC BY-NC-(SA/ND) 4.0 all allow private, non-commercial copying and private adaptation; ND and SA conditions attach only when adapted material is shared. So private training is low risk under every CC 4.0 licence here. ProPublica's 3.0 ND licence is weaker ground: version 3.0 ND licences did not grant a private-adaptation right (recollection; the 4.0 change added it).
- (b) Publishing sample outputs in a public README. If outputs do not reproduce the source's expression, they are probably not adaptations, and no licence condition applies. If an output closely tracks a source article, ND forbids sharing it, SA requires the same licence, NC forbids commercial use, and BY requires credit. Crediting the corpus in the README is cheap and satisfies BY in spirit.
- (c) Distributing adapter weights. This is the open question. If weights were treated as adapted material, ND would forbid distribution, SA would force CC BY-SA on the adapter, and NC would forbid commercial distribution. MIT OCW's terms explicitly treat trained models as derivative works ("Any derivative models, or AI systems that incorporate OCW Content through training"), which shows at least one licensor reads it that way. CC BY, CC0 and public-domain sources are the only ones where adapter distribution is safe on either reading.
- Site terms are a separate layer from the CC licence. Quanta and Khan Academy forbid scraping or AI use by contract regardless of copyright. The Conversation ("can't systematically republish all") and ProPublica ("can't republish our material wholesale, or automatically") signal that bulk taking is unwelcome even where single-article reuse is licensed.
- OWID's FAQ line "You must not edit the material" sits oddly beside a CC BY 4.0 grant, which permits adaptation. The licence controls legally, but the line suggests OWID prefers unaltered republication; attribution to OWID and named authors is the safe course.
- OpenStax books published earlier under CC BY 4.0 stay available under that licence for copies already obtained under it, because CC licences are irrevocable; current editions should be treated as CC BY-NC-SA 4.0 unless the book page says otherwise.
- Wikipedia Signpost is hosted on English Wikipedia, so the same CC BY-SA 4.0 Terms of Use should apply; I did not check a Signpost-specific page.

### Gaps
- OpenStax: when the switch from CC BY to CC BY-NC-SA happened and which titles remain CC BY. The "An update on OpenStax licensing" post returned a title only, then 404.
- Khan Academy: exact CC licence version and the full terms; both pages refused the fetch. The AI-training ban rests on a search snippet of the help article.
- Carbon Brief: exact CC licence variant and version (the brief says CC BY-NC-ND; I could confirm only "CC license", non-commercial, unadapted).
- Knowable: licence version and republishing conditions (403).
- Cochrane: full copyright terms and any text-mining policy (403). Some Cochrane reviews are open access, which I could not check.
- LibreTexts: no licence page retrieved. A secondary source says licences vary by page (including CC BY-NC-SA and a CK-12 licence that bars AI training); unverified.
- PLOS blogs licence, Scientific American and Vox terms: not checked. The brief states Scientific American and Vox are not open; I have no evidence against that.
- CRS reports as public domain under 17 U.S.C. § 105: recollection, not confirmed from a fetched primary source.
- Frontiers for Young Minds licence (I believe CC BY; not confirmed).
- No source retrieved says whether model weights are an adaptation under CC licences.

## 2. robots.txt and AI stance

### Takeaway
Among the open-licence sources, only The Conversation blocks AI crawlers outright; OpenStax and Khan Academy block GPTBot specifically; EFF allows AI crawlers with a crawl delay. MIT OCW is the only source found with an explicit clause permitting AI training (non-commercial only).

### Cited Findings
- The Conversation: a group naming GPTBot, ClaudeBot, CCBot, Google-Extended, PerplexityBot, Bytespider, Applebot-Extended and others carries `Disallow: /`. — [theconversation.com/robots.txt](https://theconversation.com/robots.txt)
- OpenStax: `User-agent: GPTBot` / `Disallow: /books/`; other AI crawlers not named. — [openstax.org/robots.txt](https://openstax.org/robots.txt)
- Khan Academy: `User-agent: GPTBot` / `Disallow: /`; other AI crawlers not named. — [khanacademy.org/robots.txt](https://www.khanacademy.org/robots.txt)
- EFF: GPTBot, Google-Extended, anthropic-ai and ClaudeBot get a 30-second crawl delay, CCBot 60 seconds, no disallow; the file's comment reads "AI training crawlers — higher delay (or Disallow: / if preferred)". — [eff.org/robots.txt](https://www.eff.org/robots.txt)
- Quanta: only `/wp-admin/` disallowed; no AI crawler named (but the terms ban scraping, see section 1). — [quantamagazine.org/robots.txt](https://www.quantamagazine.org/robots.txt)
- ProPublica: `User-agent: *` with empty `Disallow:`; no AI crawler named. — [propublica.org/robots.txt](https://www.propublica.org/robots.txt)
- Global Voices: no AI crawler named; crawl-delay 10. — [globalvoices.org/robots.txt](https://globalvoices.org/robots.txt)
- Mongabay: nothing disallowed; crawl-delay 10. — [news.mongabay.com/robots.txt](https://news.mongabay.com/robots.txt)
- Carbon Brief: nothing disallowed; crawl-delay 10. — [carbonbrief.org/robots.txt](https://www.carbonbrief.org/robots.txt)
- eLife: no AI crawler named; `/search` and `/download/` disallowed; crawl-delay 10; Amazonbot and some SEO bots fully blocked. — [elifesciences.org/robots.txt](https://elifesciences.org/robots.txt)
- English Wikipedia: no AI crawler named; article pages allowed. — [en.wikipedia.org/robots.txt](https://en.wikipedia.org/robots.txt)
- Wikimedia robot policy: "Consider if dumps are more efficient than live requests."; "Always identify your bot clearly via its User-Agent HTTP header"; "keep the average requests per second below 20."; no AI-specific text. — [Wikimedia Robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy)
- Wikimedia Enterprise published a structured English and French Wikipedia dataset on Kaggle aimed at machine-learning use, to give developers an alternative to scraping. — [Wikimedia Enterprise blog](https://enterprise.wikimedia.com/blog/kaggle-dataset/)
- MIT OCW explicit AI clause: see section 1. — [MIT OCW terms](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)
- OWID: the fetch of robots.txt returned only a sitemap line. — [ourworldindata.org/robots.txt](https://ourworldindata.org/robots.txt)

### Inferences
- robots.txt governs crawlers, not what a licensee may do with lawfully obtained copies. But The Conversation's full AI block, next to its ND licence and "can't systematically republish" rule, is a clear signal that bulk AI use is unwelcome there.
- For the Wikimedia projects, dumps are the intended route and avoid any robots question.

### Gaps
- OWID robots.txt may have been truncated by the fetch; treat "no AI block" as unconfirmed.
- Not fetched: robots.txt for Knowable, Aeon, Undark, Cochrane, PLOS, LibreTexts, MIT OCW, Carpentries, Science Journal for Kids, Wikinews, Wikibooks, Simple Wikipedia.
- No published AI-training policy found for OWID, eLife, EFF, Wikinews, Mongabay, Carbon Brief or The Carpentries.

## 3. Size, dumps and APIs

### Takeaway
Every Wikimedia source has official dumps and far exceeds 300,000 words. eLife (GitHub XML), PLOS (allofplos), The Carpentries (GitHub Markdown) and CRS reports (bulk download) also have official bulk routes. OWID, the best register match, has no text dump that I could find.

### Cited Findings
- Simple English Wikipedia: 286,705 content pages; 71,421,558 words; 3,421 active users. — [Simple Wikipedia statistics](https://simple.wikipedia.org/wiki/Special:Statistics)
- English Wikinews: 22,237 content pages; 9,985,755 words; 36 active users. — [Wikinews statistics](https://en.wikinews.org/wiki/Special:Statistics)
- English Wikibooks: 99,202 content pages; 103,895,311 words; 646 active users. — [Wikibooks statistics](https://en.wikibooks.org/wiki/Special:Statistics)
- English Wikipedia: 7,032 featured articles out of 7,263,786 articles. — [Wikipedia:Featured articles](https://en.wikipedia.org/wiki/Wikipedia:Featured_articles)
- The Conversation US: more than 21,000 articles in its first decade, from scholars at more than 1,200 institutions; US edition launched October 2014; nine other editions exist. — [The Conversation US, who we are](https://theconversation.com/us/who-we-are)
- eLife: the `elife-article-xml` repository holds full XML for every article and revision and is kept current. — [elife-article-xml](https://github.com/elifesciences/elife-article-xml)
- eLife digests: began in 2012; over 2,400 articles summarised by 2017; since 2016 digests cover a selection of papers, not all (search summary of eLife's own guide). The digests page is still active, newest item dated Nov 12, 2026. — [eLife inside guide to digests](https://elifesciences.org/articles/25410); [eLife digests](https://elifesciences.org/digests)
- A published lay-summary dataset pairs PLOS (large-scale) and eLife (medium-scale) articles with their lay summaries. — [arXiv 2210.09932](https://arxiv.org/abs/2210.09932)
- PLOS: allofplos gives the whole corpus for mining. — [PLOS blog, allofplos](https://theplosblog.plos.org/2017/11/unrestricted-text-and-data-mining-with-allofplos/)
- OWID: the `owid/owid-content` repository holds explorer configurations, not article text, and was archived on Apr 8, 2025. The site has paginated "latest" listings (at least 39 pages) and a sitemap. — [owid-content](https://github.com/owid/owid-content); [OWID latest](https://ourworldindata.org/latest)
- CRS reports: 23,620 reports, all downloadable with metadata. — [EveryCRSReport about](https://www.everycrsreport.com/about.html)
- The Carpentries: lessons live as Markdown in public GitHub repositories. — [swcarpentry/shell-novice](https://github.com/swcarpentry/shell-novice/blob/main/LICENSE.md)

### Inferences
- The Conversation US alone is probably over 15 million words (21,000 articles at an assumed 800 to 1,000 words each). This is my estimate, not a published figure.
- eLife digests are short (a few hundred words each, recollection), so several thousand digests would give roughly 1 to 2 million words. Estimate only.
- Featured articles: 7,032 long articles likely total tens of millions of words. Estimate only.
- OWID would have to be fetched page by page from the sitemap at a polite rate; several hundred long articles would likely clear 300,000 words by a wide margin. Estimate only.

### Gaps
- No article or word counts found for OWID, ProPublica, Mongabay, Carbon Brief, Global Voices, EFF Deeplinks, Knowable, Science Journal for Kids, Carpentries, OpenStax, LibreTexts, MIT OCW or Khan Academy.
- Exact counts for the lay-summary dataset (I recall about 27,500 PLOS and about 4,800 eLife articles; not confirmed this session).
- Whether eLife XML carries the digest as a tagged section and a publication date per article (I believe both are true; the repository page did not say).
- OpenStax GitHub source repositories: I believe they exist; not checked.
- Whether The Conversation, Global Voices or Mongabay offer an API or bulk export.

## 4. Register and house style

### Takeaway
OWID and eLife digests are the closest matches to "plain, concrete, modern explanatory prose" among the clean-licence sources. Wikinews gives news-summary structure but flat prose; The Carpentries gives technical walkthrough structure. My register judgements rest on only two sampled pages plus prior familiarity, so treat most of this section as inference.

### Cited Findings
- OWID sample (Max Roser, "The world is awful. The world is much better. The world can be much better."): short declarative sentences, for example "It is wrong to think these three statements contradict each other." and "Millions of child deaths are preventable."; first-person voice; dense, precise numbers restated in everyday units; clear thematic headings; little hedging. — [OWID sample article](https://ourworldindata.org/much-better-awful-can-be-better)
- eLife digests describe themselves as "cutting jargon and putting research in context."; short, sometimes playful headlines ("Rise to the top", "CRY me to sleep"); active voice, for example "Activating torpor-controlling neurons in rats triggers a protective response in the heart". — [eLife digests](https://elifesciences.org/digests)
- The Conversation: written by academics for the general public and "edited by our team of journalists." — [The Conversation US, who we are](https://theconversation.com/us/who-we-are)
- Science Journal for Kids and Frontiers for Young Minds adapt research papers for school-age readers (Frontiers reviewers are aged 8 to 15). — [SJK content licence](https://www.sciencejournalforkids.org/content-license.html); [Frontiers for Young Minds](https://kids.frontiersin.org/about/journal)

### Inferences
(From prior familiarity, not sampled this session.)
- Simple English Wikipedia: very plain but stilted and uneven; restricted vocabulary produces choppy sentences. Poor model of prose readers prefer.
- Wikipedia featured articles: polished but encyclopedic, long sentences, heavy citation, neutral and flat.
- Wikinews: inverted-pyramid news summaries, neutral, attribution-heavy; quality varies by volunteer.
- Wikibooks: textbook-like, very uneven in quality and completeness.
- The Conversation, Knowable, Mongabay, Carbon Brief, ProPublica: professional journalism; Conversation pieces are short explainers with a consistent edited shape; Carbon Brief is data-heavy with long Q&A explainers; ProPublica is long narrative investigation, less explanatory.
- OpenStax and LibreTexts: textbook register with learning objectives, worked examples and exercises; clear but formulaic.
- Carpentries: second-person, imperative, step-by-step, interleaved with code.
- EFF Deeplinks: advocacy register; opinionated, legal and policy vocabulary.
- Global Voices: reported pieces by many volunteers, many translated; uneven.
- PLOS author summaries: one paragraph each, written by researchers, more technical and variable than eLife digests, which are professionally edited.
- CRS reports: plain, neutral policy explanation, dry and heavily structured.
- Children's science sources: clear, but pitched too young for a general adult reader.

### Gaps
- No sample pieces read for any source except one OWID article and the eLife digests index. A proper register check needs three to five pieces per shortlisted source.
- No measured readability or sentence-length statistics for any source.

## 5. Voice consistency and style guides

### Takeaway
OWID is the only candidate with a small, named author group. eLife digests are the next most consistent because a small editorial team writes or edits them to a published guide. Everything else is hundreds to thousands of authors, held together (or not) by editing.

### Cited Findings
- OWID articles carry named bylines (the sample is by Max Roser). — [OWID sample article](https://ourworldindata.org/much-better-awful-can-be-better)
- eLife publishes guidance on writing digests; digests are written mainly by the editorial team with the authors (search summary). — [eLife: how to write an eLife digest](https://elifesciences.org/inside-elife/85518309/plain-language-summaries-how-to-write-an-elife-digest); [eLife inside guide](https://elifesciences.org/articles/25410)
- The Conversation US: authors from more than 1,200 institutions, edited by staff journalists; it links to editorial policies and a charter. — [The Conversation US, who we are](https://theconversation.com/us/who-we-are)
- Mongabay has a public style guide site (found in search; not read). — [Mongabay style guide](https://sites.google.com/wildmadagascar.org/mongabaystyleguide/general-guidelines/article-components)
- Cochrane publishes standards for plain language summaries (found in search; not read). — [Cochrane PLS standards](https://training.cochrane.org/resource/cochrane-standards-preparing-plain-language-summaries)
- Frontiers for Young Minds lists 5,410 authors. — [Frontiers for Young Minds](https://kids.frontiersin.org/about/journal)
- Wikinews has 36 active users; Simple Wikipedia 3,421; Wikibooks 646. — [Wikinews statistics](https://en.wikinews.org/wiki/Special:Statistics); [Simple Wikipedia statistics](https://simple.wikipedia.org/wiki/Special:Statistics); [Wikibooks statistics](https://en.wikibooks.org/wiki/Special:Statistics)

### Inferences
- OWID's byline metadata would allow filtering to two or three authors (for example Hannah Ritchie and Max Roser) for a near single-voice corpus, the nearest thing here to the project's earlier single-author setup.
- Wikimedia projects have manuals of style, and featured articles are reviewed against them, but the authorship is collective; the result is a consistent register with no personal voice.

### Gaps
- Number of OWID authors and words per author: not found.
- Style guides for Carbon Brief, Knowable, Global Voices, EFF, ProPublica, OpenStax and Carpentries: not searched.

## 6. Dates (share written before December 2022; per-item dates)

### Takeaway
All journalistic and journal sources carry a publication date per item, so filtering to before December 2022 is feasible. Wikimedia content is continuously edited, so the filter must be applied to revision history or by choosing an older dump.

### Cited Findings
- OWID exposes `datePublished` and revision notes: the sample was published July 20, 2022, first version October 2018, revised February 2024. — [OWID sample article](https://ourworldindata.org/much-better-awful-can-be-better)
- Wikinews licence periods are date-based (2005 and December 2024 boundaries), and its articles are dated news items. — [Wikinews:Copyright](https://en.wikinews.org/wiki/Wikinews:Copyright)
- eLife digests started in 2012 and continue in November 2026. — [eLife inside guide](https://elifesciences.org/articles/25410); [eLife digests](https://elifesciences.org/digests)
- The Conversation US has published since October 2014. — [The Conversation US, who we are](https://theconversation.com/us/who-we-are)
- Global Voices states it does not accept machine-generated writing, which lowers contamination risk for later text. — [Global Voices policy on AI](https://globalvoices.org/about/global-voices-policy-on-ai/)
- The eLife XML repository keeps each revision of each article. — [elife-article-xml](https://github.com/elifesciences/elife-article-xml)

### Inferences
- With 36 active users today and about 22,000 articles, most Wikinews text almost certainly predates December 2022, and nearly all of it falls under CC BY 2.5.
- OWID articles are revised in place, so a pre-2022 publication date does not guarantee pre-2022 text; the Wayback Machine or the revision note is needed for a strict filter.
- For most sources here a decade or more of archive precedes December 2022, so the date filter should not threaten the 300,000-word floor.

### Gaps
- No per-source figure for the share of text written before December 2022.
- Whether Carpentries lesson history (git) is clean enough to pin to a pre-December-2022 commit: likely, not checked.

## 7. Extraction effort and pitfalls

### Takeaway
Lowest effort: Carpentries (Markdown in git), eLife (JATS XML), PLOS (allofplos XML), Wikimedia dumps (wikitext, needs a parser). Highest effort: OWID (no dump, chart embeds), OpenStax and MIT OCW (book markup and PDFs), Science Journal for Kids (PDF articles, recollection).

### Cited Findings
- OWID: no article-text repository; the archived content repo holds only explorer configs. Third-party data and charts are excluded from OWID's licence. — [owid-content](https://github.com/owid/owid-content); [OWID FAQ](https://ourworldindata.org/faqs)
- Wikimedia: dumps preferred over live requests. — [Wikimedia Robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy)
- Images are carved out of the text licence at The Conversation, ProPublica, Mongabay, Global Voices, EFF and Wikinews, so text-only extraction is the correct scope. — [The Conversation](https://theconversation.com/us/republishing-guidelines); [ProPublica](https://www.propublica.org/steal-our-stories); [Mongabay](https://news.mongabay.com/copyright/creative-commons/); [Global Voices](https://globalvoices.org/about/global-voices-attribution-policy/); [EFF](https://www.eff.org/copyright); [Wikinews](https://en.wikinews.org/wiki/Wikinews:Copyright)
- eLife and Global Voices ask for a 10-second crawl delay. — [elifesciences.org/robots.txt](https://elifesciences.org/robots.txt); [globalvoices.org/robots.txt](https://globalvoices.org/robots.txt)
- Carpentries lessons mix prose (CC BY) with code (MIT). — [swcarpentry/shell-novice LICENSE](https://github.com/swcarpentry/shell-novice/blob/main/LICENSE.md)

### Inferences
- OWID pitfalls: chart embeds, footnotes, "cite this work" and "reuse this work" boilerplate, data-insight snippets too short to be useful, topic pages that are mostly charts.
- Wikimedia pitfalls: templates, infoboxes, citation markers, tables, lists; Wikinews adds dateline templates, "Sources" sections and category boilerplate.
- eLife and PLOS: pull only the digest or author-summary element; strip inline citation references.
- The Conversation and Mongabay: republish footers, donation asks, embedded tweets, author bios.
- Textbooks: learning objectives, exercises, equations (MathML or LaTeX), figure captions, glossary blocks.
- Carpentries: code blocks, callouts and exercise blocks dominate some lessons; prose yield per lesson is modest.

### Gaps
- No extraction was attempted, so every pitfall above is expected, not observed.
- Format of Science Journal for Kids articles (PDF or HTML) not confirmed.

## 8. Memorization risk (presence in common pretraining sets)

### Takeaway
All of these are public web text and should be assumed present in the base model's pretraining data; Wikipedia family content certainly is. The risk is highest for Wikipedia featured articles and lowest for niche, low-traffic text such as eLife digests and Carpentries lessons.

### Cited Findings
- Wikimedia itself packages Wikipedia for machine-learning use through Wikimedia Enterprise and Kaggle. — [Wikimedia Enterprise blog](https://enterprise.wikimedia.com/blog/kaggle-dataset/)
- eLife and PLOS lay summaries are already a published NLP dataset. — [arXiv 2210.09932](https://arxiv.org/abs/2210.09932)
- PLOS's full corpus has been offered for mining since 2017. — [PLOS blog, allofplos](https://theplosblog.plos.org/2017/11/unrestricted-text-and-data-mining-with-allofplos/)
- Sites with no AI-crawler block (ProPublica, Mongabay, Carbon Brief, Global Voices, eLife, Quanta, English Wikipedia) have been open to AI crawlers. — robots.txt files cited in section 2, for example [propublica.org/robots.txt](https://www.propublica.org/robots.txt)

### Inferences
- For a style fine-tune, prior exposure matters less than for a knowledge benchmark: the adapter learns register, and the base model has already seen far more Wikipedia than anything else, which is one reason Wikipedia-style prose reads as "generic AI writing". Training on Wikipedia would push toward the register the project wants to beat.
- Prior exposure does raise the chance of verbatim regurgitation in README samples, which matters most for ND and SA sources. Running an overlap check on outputs against the corpus, as the project already does with its recall probe, covers this.

### Gaps
- I found no source listing which of these sites appear in any specific open model's pretraining data.

## 9. One-line verdicts

### Takeaway
Best fits on licence plus register: Our World in Data and eLife digests, with Wikinews for news-summary shape and The Carpentries for technical walkthroughs. CC BY-ND and NC sources are fine for private training but carry real doubt for distributing adapter weights. Quanta, Khan Academy, Aeon, Undark and Cochrane are out.

### Cited Findings
Verdicts are my judgement; the licence fact behind each is cited.

Usable now (attribution only):
- Our World in Data: CC BY 4.0 on text; best register match; small author group; no dump, so fetch individual articles politely and credit OWID and authors. — [OWID FAQ](https://ourworldindata.org/faqs)
- eLife digests: CC BY 4.0; edited plain-language science; official XML on GitHub. — [eLife terms](https://elifesciences.org/terms); [elife-article-xml](https://github.com/elifesciences/elife-article-xml)
- Wikinews: CC BY 2.5 (2005 to 2024), CC BY 4.0 after; about 10 million words; dumps; flat style. — [Wikinews:Copyright](https://en.wikinews.org/wiki/Wikinews:Copyright)
- The Carpentries: CC BY 4.0 lessons in git; good for technical explainers; modest prose volume. — [swcarpentry/shell-novice LICENSE](https://github.com/swcarpentry/shell-novice/blob/main/LICENSE.md)
- Global Voices: CC BY 3.0; many authors and translations, uneven. — [Global Voices attribution policy](https://globalvoices.org/about/global-voices-attribution-policy/)
- EFF Deeplinks: CC BY (4.0 in text, 3.0 US badge); advocacy tone limits fit. — [EFF copyright policy](https://www.eff.org/copyright)
- PLOS author summaries: CC BY 4.0 with a bulk corpus; more technical than the target. — [PLOS ONE content licence](https://journals.plos.org/plosone/s/content-license)
- Science Journal for Kids: CC BY; register too young for the main corpus. — [SJK content licence](https://www.sciencejournalforkids.org/content-license.html)

Usable with conditions:
- Simple English Wikipedia, Wikipedia featured articles, Wikibooks, Signpost: CC BY-SA 4.0; dumps; ShareAlike doubt on adapter weights; encyclopedic or uneven prose; highest memorization. — [Wikimedia Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use)
- MIT OCW: CC BY-NC-SA 4.0 with explicit permission for non-commercial AI training; derived models appear bound by the same terms; notes are heterogeneous. — [MIT OCW terms](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)
- OpenStax: now stated as CC BY-NC-SA 4.0; non-commercial only; GPTBot blocked from books. — [OpenStax help](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks)
- The Conversation: CC BY-ND 4.0; private training defensible, but AI crawlers are blocked and systematic republication is barred; do not distribute weights without asking. — [The Conversation republishing guidelines](https://theconversation.com/us/republishing-guidelines); [robots.txt](https://theconversation.com/robots.txt)
- Mongabay: CC BY-ND 4.0; same ND caution. — [Mongabay Creative Commons page](https://news.mongabay.com/copyright/creative-commons/)
- Knowable: CC BY-ND per its about page (unverified version); same ND caution. — [Knowable about](https://knowablemagazine.org/about)
- Carbon Brief: CC licence, non-commercial and unadapted (variant unconfirmed); private non-commercial training only. — [Carbon Brief](https://www.carbonbrief.org/regions)
- ProPublica: CC BY-NC-ND 3.0 US, no wholesale or automatic republication; weakest of the CC group and a poor register fit. — [ProPublica Steal Our Stories](https://www.propublica.org/steal-our-stories)
- CRS reports: bulk download exists; public-domain status to be confirmed; dry register. — [EveryCRSReport about](https://www.everycrsreport.com/about.html)
- LibreTexts: per-page licences, unverified. — no primary source retrieved; see Gaps.

Not usable:
- Quanta Magazine: all rights reserved; terms ban storing, scraping and data mining. — [Quanta Terms & Conditions](https://www.quantamagazine.org/terms-conditions/)
- Khan Academy: guideline bars scraping and AI training. — [Khan Academy help article](https://support.khanacademy.org/hc/de/articles/42929097425037)
- Aeon: no CC licence; paid republication. — [Aeon republish](https://aeon.co/republish)
- Undark: own revocable terms, 90-day window, no CC licence. — [Undark republishing guidelines](https://undark.org/republishing-guidelines/)
- Cochrane plain-language summaries: permissions-based reuse through the publisher. — [Cochrane Library permissions](https://cochranelibrary.com/en/help/permissions)
- Scientific American, Vox: stated as not open in the brief; not checked here.

### Inferences
- A corpus that needs no licence caveats and still fits the three target genres could combine OWID articles (explanatory, data-led), eLife digests (science walkthroughs) and Wikinews (news summaries), with Carpentries prose for technical explainers. All are CC BY, so adapter weights and README samples can be published with an attribution list.
- If a single consistent voice matters more than genre coverage, OWID filtered to one or two authors is the closest analogue to the project's earlier single-author corpus.
- Asking permission is realistic for the ND publishers (The Conversation, Mongabay, Knowable) if their prose turns out to be the best fit; their licences already allow free republication and each lists a rights contact.

### Gaps
- No mathematics-walkthrough source with a clean CC BY licence and good prose was confirmed. OpenStax is now NC-SA, Khan is closed, Quanta is closed. Older CC BY editions of OpenStax maths books and CC BY Wikibooks-style texts are leads I did not verify.
- Verdicts for register rest on little sampling (section 4).
