# Open and Public-Domain English Nonfiction as Single-Author / House-Style Fine-Tuning Corpora (as of 2026-11-07)

## Q1. Which legally clean options have ≥100k words (ideally 200k+) from one author or a tightly consistent house style? (Candidate catalog)

### Takeaway
Many single-author public-domain (PD) nonfiction corpora clear 200k measured words and are PD in both the US and life+70 countries. The strongest for instructive prose with narrative flair are Arnold Bennett's self-help (~303k), Hendrik Willem van Loon (~268k), Emily Post's *Etiquette* (~205k), Edwin Slosson (~118k), Mark Twain's nonfiction (~1.04M), Fabre in translation (~407k counted, more available), T.H. Huxley (~900k) and John Tyndall (~656k). Bertrand Russell (~467k) is PD in the US only. For modern voice, the cleanest large sources are gwern.net (CC0, >4.38M words, one author), 18F's guides (US PD plus a worldwide CC0 waiver) and GOV.UK (OGL v3.0 house style). OpenStax is a trap: most current titles are now CC BY-NC-SA. Write the Docs' site is CC BY-NC-SA.

### Cited Findings

#### Method (how the numbers were produced)
- **Word counts were measured, not estimated.** On 2026-11-07 I downloaded each Project Gutenberg (PG) plain-text file (`https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt`). I counted whitespace-delimited words (`wc -w`) between the `*** START OF` and `*** END OF` markers. The counts include prefaces, editors' notes, footnotes, indexes and illustration captions, so treat them as upper bounds, likely 5–15% over (my estimate).
- **File-size rule of thumb.** Across these files, PG UTF-8 text runs about 5.8–6.0 bytes per word. For example, *Voyage of the Beagle* is 1,199 KB for 205,661 words ([PG #944](https://www.gutenberg.org/ebooks/944)), and *Life on the Mississippi* is 824 KB for 144,522 words ([PG #245](https://www.gutenberg.org/ebooks/245)). So words ≈ bytes ÷ 6.
- **Author and translator life dates** come from the PG catalog feed ([pg_catalog.csv](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv)).
- **Status rules applied:**
  - US: everything published before 1931 is PD ([Cornell chart, current as of 1 Jan 2026](https://guides.library.cornell.edu/copyright/publicdomain)).
  - EU: life+70 ([Directive 2006/116/EC, Art. 1](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006L0116)).
  - UK: life+70, "from the end of the calendar year in which the author dies" ([CDPA 1988 s12(2)](https://www.legislation.gov.uk/ukpga/1988/48/section/12)). A work therefore goes PD on 1 January of (death year + 71).
- **PG's own position:** "If you strip the Project Gutenberg license and all references to Project Gutenberg from the text, you are left with a text unrestricted by U.S. intellectual property law" ([PG license](https://www.gutenberg.org/policy/license.html)).
- **Bulk access:** PG's website "is intended for human users only". Automated access risks an IP block, so use mirrors or the offline catalogs for bulk pulls ([PG robot policy](https://www.gutenberg.org/policy/robot_access.html)).

#### A. Public-domain single-author corpora (measured word counts)

| Author (died) | Works counted (PG IDs) | Measured words | US status | EU/UK status | Other clean-text sources |
|---|---|---|---|---|---|
| Arnold Bennett (1931) | *How to Live on 24 Hours a Day* 2274 (12.9k); *Literary Taste* 3640 (24.7k); *The Author's Craft* 12743 (18.8k); *The Human Machine* 12811 (22.5k); *Mental Efficiency* 23347 (22.8k); *The Plain Man and His Wife* 13449 (17.6k); *Feast of St. Friend* 14653 (11.8k); *Self and Self-Management* 75928 (16.0k); *Journalism for Women* 8405 (16.9k); *Truth About an Author* 66661 (29.7k); *Books and Persons* 15717 (62.9k); *Your United States* 15063 (46.9k) | **~303k** (self-help subset ~118k) | PD (all pre-1931) | PD since 1 Jan 2002 | Standard Ebooks has only his novels ([SE Bennett](https://standardebooks.org/ebooks/arnold-bennett)) |
| Hendrik Willem van Loon (1944) | *Story of Mankind* 754 (129.2k); *Tolerance* 74798 (112.1k); *Ancient Man* 9991 (26.9k) | **~268k** | PD (1920–25 works) | PD since 1 Jan 2015 | [SE *Story of Mankind*](https://standardebooks.org/ebooks/hendrik-willem-van-loon) |
| Emily Post (1960) | *Etiquette* 14314 | **205.2k** | PD (1922) | Life+70 not until 1 Jan 2031; see Q3 on the shorter-term rule | — |
| Edwin E. Slosson (1929) | *Creative Chemistry* 17149 (88.0k); *Easy Lessons in Einstein* 75807 (29.5k) | **~118k** | PD | PD | IA scan of *Creative Chemistry*, flagged NOT_IN_COPYRIGHT ([IA](https://archive.org/details/creativechemist02slosgoog)) |
| Bertrand Russell (1970) | *Problems of Philosophy* 5827 (42.8k); *ABC of Relativity* 67104 (47.0k); *Conquest of Happiness* 77894 (58.7k); *Education and the Good Life* 70302 (68.3k); *What I Believe* 73782 (12.5k); *Mysticism and Logic* 25447 (71.8k); *Proposed Roads to Freedom* 690 (54.6k); *Political Ideals* 4776 (22.3k); *Analysis of Mind* 2529 (89.1k) | **~467k** | PD for pre-1931 works only | **In copyright until 1 Jan 2041** | [SE Russell](https://standardebooks.org/ebooks/bertrand-russell) |
| H. G. Wells (1946) | *A Short History of the World* 35461 (119.7k); *Outline of History* 45368 (463.8k) | ~584k, with heavy content overlap between the two | PD (1920/1922) | PD since 1 Jan 2017 | — |
| H. L. Mencken (1956) | *Prejudices* 1–5: 53538, 53467, 53474, 67978, 72510 (56.4k, 57.0k, 71.8k, 67.1k, 69.0k); *A Book of Prefaces* 19355 (60.3k); *Notes on Democracy* 73150 (41.2k); *The American Language* 43376 (138.9k) | **~562k** | PD for pre-1931 works | Life+70 runs to 1 Jan 2027; shorter-term rule likely applies already (Q3) | [SE *American Language*](https://standardebooks.org/ebooks/h-l-mencken/the-american-language) (listed as US PD, not yet produced) |
| Mark Twain (1910), nonfiction only | *Life on the Mississippi* 245 (144.5k); *Roughing It* 3177 (167.9k); *Innocents Abroad* 3176 (193.2k); *A Tramp Abroad* 119 (157.1k); *Following the Equator* 2895 (187.7k); *What Is Man? and Other Essays* 70 (94.4k); *Speeches* 3188 (92.2k); *How to Tell a Story* 3250 (7.2k) | **~1.04M** | PD, except the Mark Twain Project editions (Q3) | PD | SE: *Life on the Mississippi*, *Roughing It*, *Innocents Abroad*, and *Autobiography* (1924 Paine edition, 195,363 words) ([SE Twain](https://standardebooks.org/ebooks/mark-twain), [SE Autobiography](https://standardebooks.org/ebooks/mark-twain/the-autobiography-of-mark-twain)) |
| Jean-Henri Fabre (1915); translators Alexander Teixeira de Mattos (1865–1921) and Bernard Miall (1876–1953) | *Life of the Spider* 1887 (70.5k); *Life of the Fly* 3422 (95.2k); *Life of the Grasshopper* 66650 (86.8k); *Mason-Bees* 2884 (63.5k); *Social Life in the Insect World* 18350 (90.9k, Miall translation). About 24 English Fabre titles are on PG. | **~407k counted** (≥1M likely across all volumes, not measured) | PD | PD. Teixeira de Mattos translations PD; Miall translations PD since 1 Jan 2024 | — |
| T. H. Huxley (1895) | *Lay Sermons* 16729 (107.8k); *Science & Education* 7150 (108.8k); *Discourses* 10060 (95.6k); *Lectures and Essays* 6414 (164.5k); *Evolution and Ethics* 2940 (97.0k); *Critiques and Addresses* 12506 (100.9k); *Science and Culture* 52344 (93.8k); *Man's Place in Nature* 40257 (134.6k) | ~903k raw (the collections overlap; dedupe) | PD | PD | — |
| John Tyndall (1893) | *Fragments of Science* 24527 (287.4k); *Six Lectures on Light* 14000 (64.7k); *Forms of Water* 63803 (49.3k); *Hours of Exercise in the Alps* 47209 (108.7k); *Glaciers of the Alps* 34192 (145.7k) | ~656k | PD | PD | — |
| Michael Faraday (1867) | *Chemical History of a Candle* 14474 (41.7k); *On the Various Forces of Nature* 52293 (57.7k), both edited by William Crookes (d. 1919) | ~99k (just under the bar) | PD | PD | — |
| Charles Darwin (1882) | *Voyage of the Beagle* 944 (205.7k); *Autobiography* 2010 (22.7k); *Earthworms* 2355 (61.4k) | ~290k | PD | PD | [SE Darwin](https://standardebooks.org/ebooks/charles-darwin) |
| William James (1910) | *Talks to Teachers* 16287 (62.2k); *Pragmatism* 5116 (52.0k); *Will to Believe* 26659 (101.4k); *Memories and Studies* 20768 (65.6k); *Varieties* 621 (186.4k) | ~468k | PD | PD | [SE James](https://standardebooks.org/ebooks/william-james) |
| G. K. Chesterton (1936), essays | *Tremendous Trifles* 8092; *All Things Considered* 11505; *Alarms and Discursions* 9656; *The Defendant* 12245; *A Miscellany of Men* 2015; *Heretics* 470; *Orthodoxy* 130; *What's Wrong with the World* 1717; *What I Saw in America* 27250; *Uses of Diversity* 60057; *Fancies Versus Fads* 60164; *Short History of England* 20897 | ~708k | PD for pre-1931 works only | PD since 1 Jan 2007 | [SE Chesterton](https://standardebooks.org/ebooks/g-k-chesterton) |
| Robert Louis Stevenson (1894), essays and travel | 386, 381, 614, 627, 492, 535, 534, 516, 373, 425 | ~537k | PD | PD | SE "Travel Essays" ([SE RLS](https://standardebooks.org/ebooks/robert-louis-stevenson)) |
| John Muir (1914) | 32540, 10012, 7345, 60929, 18359 | ~381k | PD | PD | [SE Muir](https://standardebooks.org/ebooks/john-muir) |
| John Burroughs (1921) | *Wake-Robin* 4203; *Winter Sunshine* 4279; *Ways of Nature* 30249; *Locusts and Wild Honey* 6355 (4 of ~25 PG titles) | ~256k counted | PD | PD | — |
| Richard Jefferies (1887) | 36948, 13730, 36949, 6981, 7030, 6164 | ~454k | PD | PD | — |
| Benjamin Franklin (1790) | *Autobiography* 20203 (76.2k); *Complete Works* 48136–48138 (~464k, which includes letters and others' text) | ~540k | PD | PD | [SE *Autobiography*](https://standardebooks.org/ebooks/benjamin-franklin) |
| J. Berg Esenwein (1946) and Dale Carnegie (1955) | *The Art of Public Speaking* 16317 (1915) | 159.4k (co-authored) | PD | PD since 1 Jan 2026 (joint work; life+70 counted from the last surviving author, [EU Art. 1(2)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006L0116)) | Carnegie's solo *Public Speaking* (1926) is on IA ([IA](https://archive.org/details/publicspeaking0002dale)) |
| Sir James Jeans (1946) | *The Universe Around Us* 76356 (107.1k), posted by PG 2025-06-22 | 107.1k | PD (1929) | PD since 1 Jan 2017 | — |
| Sir Arthur Eddington (1944) | *Stars and Atoms* 73362 (37.7k); *Nature of the Physical World* 72963 (PG plain text came back empty, not counted) | ≥38k measured | PD (1927/1928) | PD since 1 Jan 2015 | IA scans ([IA](https://archive.org/details/natureofphysical1927eddi)) |
| Stewart Edward White (1946) | *Camp and Trail* 32950 (33.9k); *The Forest* 9376 (52.3k); *The Mountains* 465 (53.3k) | ~139k | PD | PD since 1 Jan 2017 | — |
| Edward Bok (1930) | *Americanization of Edward Bok* 3538 | 119.3k | PD | PD | — |
| Theodore Roosevelt (1919) | *An Autobiography* 3335 | 217.3k (plus many more titles on PG) | PD | PD | [SE Roosevelt](https://standardebooks.org/ebooks/theodore-roosevelt) |
| Daniel Carter Beard (1941) | *Shelters, Shacks and Shanties* 28255 (51.9k); *Book of Camp-Lore and Woodcraft* 44215 (56.8k) | ~109k | PD | PD since 1 Jan 2012 | — |
| Strunk (1946) | *The Elements of Style* 37134 (1918) | 13.9k (far too small alone) | PD | PD since 1 Jan 2017 | — |

Sources for every row: the PG ebook pages at `https://www.gutenberg.org/ebooks/{ID}`, e.g. [2274](https://www.gutenberg.org/ebooks/2274), [754](https://www.gutenberg.org/ebooks/754), [14314](https://www.gutenberg.org/ebooks/14314), [17149](https://www.gutenberg.org/ebooks/17149), [77894](https://www.gutenberg.org/ebooks/77894), [45368](https://www.gutenberg.org/ebooks/45368), [53538](https://www.gutenberg.org/ebooks/53538), [1887](https://www.gutenberg.org/ebooks/1887), [16729](https://www.gutenberg.org/ebooks/16729), [24527](https://www.gutenberg.org/ebooks/24527), [14474](https://www.gutenberg.org/ebooks/14474), [16317](https://www.gutenberg.org/ebooks/16317), [76356](https://www.gutenberg.org/ebooks/76356), [32950](https://www.gutenberg.org/ebooks/32950). Life dates come from the [PG catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv).

- **Not on PG but clean in the US, on Internet Archive:**
  - Horace Kephart, *Camping and Woodcraft* (1916 ed.). IA notes "The Library of Congress is unaware of any copyright restrictions" ([IA](https://archive.org/details/campingwoodcraft01keph)). Kephart died 1931 ([PG catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv)).
  - Will Durant, *The Story of Philosophy* (1926) ([IA](https://archive.org/details/dli.ernet.912)).
- **Standard Ebooks** says the texts "are already believed to be in the U.S. public domain, and Standard Ebooks dedicates its own work to the public domain" ([SE about](https://standardebooks.org/about)). Its pages also warn that a book "may still be under copyright in other countries" ([SE Twain Autobiography](https://standardebooks.org/ebooks/mark-twain/the-autobiography-of-mark-twain)).
- **Standard Ebooks has no author pages** for Huxley, Tyndall, Faraday, Fabre, Emily Post, Slosson, Strunk, Burroughs, Eddington or Jeans (404 on 2026-11-07 at `standardebooks.org/ebooks/{author}`). For these, PG is the clean-text source.

#### B. Government and public-sector house styles
- **18F (US GSA):**
  - License: "As a work of the federal government, this project is in the public domain within the United States. Additionally, we waive copyright and related rights in the work worldwide through the CC0 1.0 Universal public domain dedication" ([18F/content-guide LICENSE.md](https://github.com/18F/content-guide/blob/main/LICENSE.md)). The same text appears in [18F/18f.gsa.gov](https://github.com/18F/18f.gsa.gov/blob/main/LICENSE.md), [18F/guides](https://github.com/18F/guides/blob/main/LICENSE.md) and [18F/methods](https://github.com/18F/methods/blob/main/LICENSE.md).
  - Repo state: the content-guide repo is archived (last push 2023-12-14), while 18f.gsa.gov (the site and blog source) is not archived and was last pushed 2026-07-04 ([GitHub API content-guide](https://api.github.com/repos/18F/content-guide), [GitHub API 18f.gsa.gov](https://api.github.com/repos/18F/18f.gsa.gov)).
  - Shutdown: GSA eliminated 18F around March 1, 2025, and the website went offline the same day. The GitHub repositories stayed public ([CBS News](https://www.cbsnews.com/amp/news/general-services-administration-shutters-technology-unit-trump-doge); [FedScoop](https://fedscoop.com/elimination-of-18f-could-slow-trump-admins-digital-services/); [Wikipedia: 18F](https://en.wikipedia.org/wiki/18F)).
- **US federal works generally:** "Works prepared by federal employees as part of their official duties have no US copyright" (17 U.S.C. §105), with an exception for civilian faculty at service academies ([Cornell](https://guides.library.cornell.edu/copyright/publicdomain)).
- **National Park Service:** NPS material "unless otherwise indicated, is generally considered in the public domain". Commercial republication must carry a notice such as "No claim to original U.S. Government works" (17 U.S.C. §403), and "not all materials appearing" are NPS-created ([NPS disclaimer](https://www.nps.gov/aboutus/disclaimer.htm)).
- **NASA:** content is "generally... not subject to copyright in the United States". The NASA insignia and logotype "are not in the public domain", and third-party copyrighted items are marked ([NASA media guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/)). The NASA History Office has "prepared histories, chronologies, and oral history interviews and made them freely available" ([NASA History](https://www.nasa.gov/history/history-publications-and-resources/)).
- **NLM/NCBI:** "Information that is created by or for the US government on this site is within the public domain", and acknowledgment of NLM is requested ([NCBI policies](https://www.ncbi.nlm.nih.gov/home/about/policies/)).
- **plainlanguage.gov:** the `/guidelines/` URL now serves Digital.gov's "Plain language guide series" ([plainlanguage.gov/guidelines](https://www.plainlanguage.gov/guidelines/)).
- **GOV.UK:**
  - License: "All content is available under the Open Government Licence v3.0, except where otherwise stated", with a © Crown copyright notice.
  - Location: the style guide has moved from gov.uk/guidance/style-guide to guidance.publishing.service.gov.uk (301 redirect observed) ([GOV.UK style guides](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/)).
  - House rules include: "Use 'and' rather than '&'"; "Write all other numbers in numerals (including 2 to 9)"; "Avoid negative contractions like can't and don't"; explain abbreviations in full on first use; bulleted lists always take a lead-in line; "Always use sentence case, even in page titles"; "Plain English is mandatory for all of GOV.UK" (e.g. "use", not "utilise") ([A to Z style guide](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).

#### C. Openly licensed modern sources
- **gwern.net:** "This site is licensed under the Creative Commons public domain (CC-0) license." As of 2022-11-08, the site source was ">443 text files with >4.38m words" ([gwern.net/about](https://gwern.net/about)).
- **Distill.pub:**
  - Status: "We are now on an indefinite hiatus" ([Distill about](https://distill.pub/about/)).
  - The article footer says "Diagrams and text are licensed under Creative Commons Attribution CC-BY 2.0, unless noted otherwise", and figures reused from other sources are excluded ([Distill momentum article](https://distill.pub/2017/momentum/)).
  - The article's GitHub repo LICENSE, however, is CC BY 4.0 ([distillpub/post--momentum LICENSE](https://github.com/distillpub/post--momentum/blob/master/LICENSE)). This is a version discrepancy, but both are attribution-only.
- **Our World in Data:**
  - Writing may be republished "for free and without permission" with credit, under CC BY 4.0. "Data produced by us falls under our permissive CC BY license".
  - Third-party data and some third-party charts are excluded ([OWID FAQ](https://ourworldindata.org/faqs#can-i-use-or-reproduce-your-data)).
- **OpenStax: major correction to the common "CC BY" assumption.**
  - OpenStax's CMS API (queried 2026-11-07) lists 80 book records as "Creative Commons Attribution-NonCommercial-ShareAlike License", 38 as CC BY and 11 with no license value.
  - Only 4 *live* titles are CC BY: *Introduction to Intellectual Property*, *Physics*, *Statistics*, and *Física universitaria volumen 1*.
  - NC-SA titles include *Biology 2e*, *Psychology 2e*, *Chemistry 2e*, *U.S. History*, *University Physics*, *Principles of Economics 3e*, *Writing Guide with Handbook*, *Introduction to Python Programming* and the Calculus volumes ([OpenStax CMS API](https://openstax.org/apps/cms/api/v2/pages/?type=books.Book&fields=title,license_name,book_state&limit=200)).
- **Wikipedia / Wikibooks:**
  - Wikipedia text is under "Creative Commons Attribution-ShareAlike 4.0 International License" ([Wikipedia:Copyrights](https://en.wikipedia.org/wiki/Wikipedia:Copyrights)). The HF dump `wikimedia/wikipedia` is tagged cc-by-sa-3.0 plus GFDL ([HF](https://huggingface.co/datasets/wikimedia/wikipedia)).
  - Wikibooks: "Text is available under the Creative Commons Attribution-ShareAlike License" ([Wikibooks](https://en.wikibooks.org/wiki/Main_Page)).
- **The Open Source Way:** guidebook is "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)" ([theopensourceway/guidebook LICENSE](https://github.com/theopensourceway/guidebook/blob/main/LICENSE.md)).
- **Write the Docs:** the website repo is "Attribution-NonCommercial-ShareAlike 4.0 International", which is not clean for commercial use ([writethedocs/www LICENSE.md](https://github.com/writethedocs/www/blob/master/LICENSE.md)).
- **Python documentation:** "Python software and documentation are licensed under the Python Software Foundation License Version 2". Since 3.8.6, code examples in the docs are dual-licensed PSF-2.0 / Zero-Clause BSD ([Python History and License](https://docs.python.org/3/license.html)).
- **Django:** the repository (which includes `docs/`) is BSD-3-Clause, "Copyright (c) Django Software Foundation and individual contributors" ([django LICENSE](https://github.com/django/django/blob/main/LICENSE)).
- **Single-author CC BY-SA books:**
  - Karl Fogel, *Producing Open Source Software*: Creative Commons Attribution-ShareAlike 4.0 ([producingoss.com copyright](https://producingoss.com/en/copyright.html)).
  - Mark Pilgrim, *Dive Into Python 3*: "freely licensed under the Creative Commons Attribution Share-Alike license" ([diveintopython3.net](https://diveintopython3.net/)).
- **Blogs checked and dropped:**
  - Eli Bendersky: code in posts is public domain, but the site footer reads "© 2003-2026 Eli Bendersky", so the prose is not openly licensed ([about](https://eli.thegreenplace.net/pages/about)).
  - No CC statement on the homepages of [Lilian Weng](https://lilianweng.github.io/), [colah's blog](https://colah.github.io/) or [Julia Evans](https://jvns.ca/). Treat as all-rights-reserved unless a per-page license is found.

#### D. Checked but poor fits for this purpose
- **Montaigne** (Cotton translation, d. 1687, revised by W. C. Hazlitt, d. 1913): 525.9k words and PD everywhere ([PG #3600](https://www.gutenberg.org/ebooks/3600)), but the 17th-century syntax is extreme (see Q2 metrics).
- **Thoreau** *Walden* (115.8k, [PG #205](https://www.gutenberg.org/ebooks/205)) and **Emerson** *Essays* I–II plus *Conduct of Life* (~200k, [PG #2944](https://www.gutenberg.org/ebooks/2944)): PD, but aphoristic and transcendental rather than instructive.
- **Orwell:** almost nothing is PD in the US (Q3).
- **Strunk:** too small (13.9k).

### Inferences
- **Style cards for the shortlist.** Quantitative markers are from Q2's measurements; qualitative markers are my reading.
  - **Bennett (self-help):**
    1. Constant second-person address (20.1 "you"-words per 1k words, highest of all PD candidates measured).
    2. Short chapters, each a single practical argument.
    3. Brisk, ironic asides about "the average man" and his commute.
    4. Few semicolons (4.7/1k), mid-length sentences (mean 20.7 words).
    5. Concrete schedules and exercises (e.g., the 90-minute evening).
    - Diction: Edwardian but plain. Transfer to how-tos and memos: high.
  - **van Loon:**
    1. Chatty narrator who comments on the story and addresses the reader.
    2. Almost no semicolons (0.5/1k).
    3. Anachronistic, homely analogies.
    4. Simple vocabulary aimed at young readers.
    5. Each chapter ends with a moral or a forward hook.
    - Transfer to explainers: high. Caveat: 1920s cultural and racial attitudes need filtering.
  - **Emily Post *Etiquette*:**
    1. Prescriptive rules ("should", "never") framed as social consequences.
    2. Recurring fictional households and characters used as worked examples.
    3. Very low archaism (0.04/1k).
    4. Second person (11.4/1k).
    5. Hierarchical sections and sub-rules.
    - Transfer to how-tos and policy memos: high in form, dated in content.
  - **Slosson:**
    1. Journalistic ledes and industrial anecdotes.
    2. The lowest archaism (0.07/1k) and semicolon rate (1.5/1k) of all PD candidates.
    3. Analogy-driven explanation of chemistry and physics.
    4. Enthusiastic tone about technology.
    - Transfer to science explainers: very high, but only about 118k words on PG. Other Slosson books exist on IA but were not measured.
  - **Russell:**
    1. Lucid step-by-step argument.
    2. Everyday-object examples (the table in *Problems of Philosophy*).
    3. Dry ironic wit.
    4. Low archaism (0.32/1k).
    5. Hypotheticals.
    - Transfer: very high. Legal reach: US-only.
  - **Mencken:**
    1. Invective and mock-solemnity.
    2. Catalogues of examples.
    3. A mix of Latinate words and slang.
    4. Almost no "you" (1.5/1k).
    - Transfer: diction is modern, but the polemical tone would leak into memos.
  - **Twain (nonfiction):**
    1. First-person anecdote (14.2 "I"/1k).
    2. Deadpan exaggeration.
    3. Dialect dialogue.
    4. Digressions that mix statistics with tall tales.
    - Transfer: storytelling flair is excellent; register is 19th-century American.
  - **Fabre (translated):**
    1. Experiment told as a story.
    2. First-person field narration (12.0 "I"/1k).
    3. Anthropomorphism.
    4. Short sentences (mean 19.9).
    - Transfer: good for narrative science explainers. The translation carries some "translationese".
  - **Faraday:**
    1. Lecture-hall second person (13.4/1k) and first person (15.8/1k).
    2. Live demonstrations narrated step by step.
    3. Causal chains in simple words for a juvenile audience.
    - Transfer: high for explainers, but under 100k words.
  - **Huxley / Tyndall:**
    1. Long periodic sentences (Huxley mean 38.4).
    2. Analogies from everyday objects ("On a Piece of Chalk").
    3. Polemical "lay sermon" framing (Huxley).
    4. Tyndall pairs experiments with Alpine adventure narrative.
    - Transfer: moderate. Victorian cadence.
  - **gwern.net:**
    1. Long-form and heavily footnoted.
    2. Dense hyperlinks.
    3. Explicit uncertainty and epistemic hedging.
    4. Statistics and Bayesian jargon.
    5. Idiosyncratic vocabulary.
    - Transfer to 2026 explainers: very high for analysis, weaker for crisp how-tos. The distinctive voice is easy to overfit.
  - **GOV.UK / 18F:**
    1. Plain-English mandates.
    2. Sentence case.
    3. Numerals for all numbers (GOV.UK).
    4. No "&".
    5. Lead-in lines for bullets.
    - Transfer to memos and how-tos: maximal. Narrative flair: minimal, apart from 18F's blog.
- **Corpora meeting the ≥200k single-voice bar in both the US and the EU/UK:** Bennett (~303k), van Loon (~268k), Twain, Fabre (translation), Huxley, Tyndall, Darwin (~290k), William James, Muir, Jefferies, Stevenson, Wells, Franklin, and Roosevelt (Autobiography alone, 217k). Also gwern.net (CC0) and 18F (CC0), whose 18F size is unmeasured.
- **Corpora at ≥100k but not 200k:** Slosson (~118k), Esenwein & Carnegie (159k), S. E. White (~139k), Bok (119k), Jeans (107k) and Beard (~109k). These could be pooled into an "early-20th-century American how-to/explainer" house style. That pooling gives up single-author consistency.
- **Licensing of ShareAlike sources.** CC BY-SA sources (Wikipedia, Wikibooks, Open Source Way, Producing OSS, Dive Into Python 3) are usable, but whether ShareAlike reaches model weights or outputs is unsettled. For a "legally clean" corpus, prefer PD, CC0 and CC BY first.

### Gaps
- **Unmeasured modern corpora:** I did not measure word counts for GOV.UK (total guidance corpus), the 18F blog (`_posts` in 18F/18f.gsa.gov) or 18F guides, OWID articles per author (e.g., Hannah Ritchie, Max Roser), Distill's full article set, the Python or Django docs, *Producing OSS* or *Dive Into Python 3*. These need a crawl or repo clone to count.
- **Unmeasured books:** *Camping and Woodcraft* (Kephart), *The Story of Philosophy* (Durant), *Nature of the Physical World* (Eddington; the PG plain-text file was empty) and Carnegie's 1926 *Public Speaking* were not counted.
- **Edition questions:** I did not verify whether PG #45368 is the 1920 first edition of *The Outline of History* or a later revision. Revisions after 1930 would still be US-copyrighted.
- **Per-author OWID licensing:** not checked. The OWID FAQ is site-wide.
- **Unchecked blog licenses:** many individual CC-licensed tech and science blogs exist, but I found no verified single-author CC BY/CC0 blog with a measured ≥100k-word corpus, apart from gwern.net.

## Q2. Which read as modern enough to transfer to 2026 informational writing without sounding Victorian? (Ranking)

### Takeaway
The measured diction markers favour early-20th-century American and British popularizers. Ranked among PD sources by measured diction and fit: Slosson, Bennett, Emily Post, van Loon, Russell (US only), Wells, S. E. White, BT Washington and Bok. All have archaic-word rates ≤0.66 per 1k words, sentence means of 20–28 words and low semicolon use. Huxley, Stevenson, Franklin, Emerson and above all Montaigne measure as the most dated. The modern openly licensed sources (GOV.UK, 18F, gwern, OWID, Distill) transfer best of all, but most lack storytelling flair.

### Cited Findings
- **How the style metrics were computed** (on the PG texts listed in Q1):
  - Corpus: text between the PG START/END markers.
  - Sentence split: a naive regex on `.?!` followed by a capital.
  - "Archaic/1k": rate per 1,000 words of {thee, thou, thy, thine, hath, doth, whilst, amongst, wherein, whereof, hither, thither, ere, wherefore, hence, thence, whence, nay, aught, naught, betwixt}.
  - "you/1k" counts you/your/yours/yourself; "I/1k" counts the pronoun I; semicolons per 1k words.
  - Source texts are at `https://www.gutenberg.org/ebooks/{ID}`.

| Corpus (PG IDs) | Words | Mean / median sentence length | Archaic per 1k | "you" per 1k | "I" per 1k | Semicolons per 1k |
|---|---|---|---|---|---|---|
| Slosson (17149, 75807) | 116,759 | 24.9 / 21 | 0.07 | 3.6 | 1.5 | 1.5 |
| Emily Post (14314) | 205,310 | 27.5 / 23 | 0.04 | 11.4 | 2.1 | 6.5 |
| BT Washington, *Up from Slavery* (2376) | 77,441 | 25.8 / 22 | 0.03 | 2.1 | 26.1 | 2.6 |
| S. E. White, *Camp and Trail* (32950) | 33,691 | 21.4 / 18 | 0.09 | 21.0 | 9.7 | 5.3 |
| Bennett self-help (2274, 12811, 23347, 3640, 12743, 75928) | 118,014 | 20.7 / 17 | 0.66 | 20.1 | 12.2 | 4.7 |
| van Loon (754, 74798) | 242,510 | 24.2 / 20 | 0.43 | 1.5 | 1.9 | 0.5 |
| Russell popular (5827, 67104, 77894, 70302) | 218,021 | 25.5 / 23 | 0.32 | 3.9 | 5.4 | 5.3 |
| Wells, *Short History* (35461) | 115,982 | 24.1 / 19 | 0.25 | 0.2 | 0.9 | 4.9 |
| Bok (3538) | 120,244 | 22.9 / 19 | 0.22 | 7.5 | 6.7 | 7.1 |
| Jeans (76356) | 104,711 | 30.9 / 28 | 0.21 | 0.2 | 0.4 | 4.0 |
| Eddington, *Stars and Atoms* (73362) | 37,734 | 25.4 / 23 | 0.27 | 3.5 | 3.8 | 9.1 |
| Mencken, *Prejudices* 1–3 | 187,944 | 23.9 / 20 | 0.38 | 1.5 | 5.5 | 5.2 |
| Esenwein & Carnegie (16317) | 159,979 | 22.6 / 17 | 0.71 | 14.5 | 6.1 | 7.4 |
| Kephart, *Southern Highlanders* (31709) | 82,567 | 24.7 / 20 | 0.42 | 3.7 | 8.2 | 4.6 |
| Nessmuk, *Woodcraft* (24579) | 38,578 | 23.7 / 21 | 0.29 | 6.6 | 13.7 | 9.1 |
| Fabre, Teixeira translations (1887, 3422) | 167,172 | 19.9 / 18 | 0.87 | 2.1 | 12.0 | 8.0 |
| Faraday (14474, 52293) | 100,488 | 17.3 / 8 (artifact of short demo lines) | 0.22 | 13.4 | 15.8 | 10.4 |
| Twain travel (245, 3177, 119) | 480,325 | 25.2 / 20 | 0.38 | 6.6 | 14.2 | 10.3 |
| Chesterton essays (8092, 11505, 9656) | 167,448 | 23.0 / 20 | 0.19 | 5.5 | 17.9 | 11.2 |
| Burroughs (4203, 30249) | 132,585 | 22.7 / 20 | 0.54 | 2.0 | 9.8 | 7.8 |
| Woolf, *Common Reader* (64457) | 82,822 | 25.7 / 20 | 0.42 | 1.8 | 2.3 | 11.2 |
| William James (16287, 26659) | 163,956 | 27.7 / 24 | 0.72 | 5.8 | 6.9 | 7.7 |
| Tyndall (24527, 63803) | 337,111 | 25.2 / 22 | 0.71 | 3.2 | 5.3 | 7.4 |
| Jefferies (36948, 6981) | 126,435 | 26.5 / 24 | 0.28 | 4.5 | 4.6 | 11.8 |
| Darwin, *Beagle* (944) | 207,040 | 27.7 / 25 | 0.99 | 0.3 | 8.8 | 9.4 |
| Muir (32540, 10012) | 152,503 | 31.2 / 27 | 0.24 | 1.1 | 8.0 | 5.6 |
| Thoreau, *Walden* (205) | 117,248 | 30.4 / 24 | 0.78 | 3.9 | 17.2 | 9.2 |
| Stevenson essays (386, 614, 627) | 183,005 | 30.0 / 26 | 0.63 | 7.1 | 10.7 | 16.0 |
| Franklin, *Autobiography* (20203) | 75,523 | 34.6 / 27 | 1.11 | 3.0 | 20.9 | 11.6 |
| Huxley (16729, 7150, 6414) | 383,049 | 38.4 / 33 | 0.55 | 4.6 | 8.3 | 10.0 |
| Emerson (2944, 2945) | 133,823 | 22.9 / 18 | 2.61 | 4.9 | 7.1 | 11.4 |
| Montaigne, Cotton/Hazlitt (3600) | 527,808 | 52.2 / 39 | 3.50 | 3.2 | 12.9 | 15.3 |

(All values are my own measurements on PG texts, e.g. [PG #17149](https://www.gutenberg.org/ebooks/17149), [#14314](https://www.gutenberg.org/ebooks/14314), [#2274](https://www.gutenberg.org/ebooks/2274), [#754](https://www.gutenberg.org/ebooks/754), [#3600](https://www.gutenberg.org/ebooks/3600), [#6414](https://www.gutenberg.org/ebooks/6414).)
- **Modern style mandates in the government sources:** GOV.UK requires plain English and bans "&". It wants numerals for all numbers, avoids negative contractions and uses sentence case ([GOV.UK A to Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
- **Prior work on "modern" Gutenberg prose:** nbeerbower built a DPO set from books selected "for their 'modern' (early 20th century) language and concise prose" ([nbeerbower/gutenberg-moderne-dpo](https://huggingface.co/datasets/nbeerbower/gutenberg-moderne-dpo)).

### Inferences
- **Transferability ranking** for 2026 informational writing (memos, explainers, how-tos), with narrative flair weighed in:
  1. **GOV.UK** (OGL v3.0): house style is closest to 2026 plain-language norms; little storytelling.
  2. **18F guides and blog** (US PD + CC0): plain, friendly and modern. The blog adds case-study narrative.
  3. **gwern.net** (CC0, >4.38M words): modern and analytical with strong narrative essays, but idiosyncratic.
  4. **OWID** (CC BY) and **Distill** (CC BY): modern data/ML explainers with good narrative scaffolding; multi-author, though OWID has a strong house style.
  5. **Bennett self-help** (PD everywhere): the best PD match for instructive second-person prose with flair.
  6. **Slosson** (PD everywhere): the most modern-sounding PD science explainer measured; small corpus.
  7. **Russell's popular works**: very modern and lucid, but **US-only PD**.
  8. **van Loon** (PD everywhere): conversational storytelling explainer; content needs filtering.
  9. **Emily Post** (US PD; UK/EU likely PD via the shorter-term rule, see Q3): best for rule-plus-example how-to structure.
  10. **S. E. White, Nessmuk, Beard, Kephart:** outdoor how-to with anecdote; poolable into a ~300k "American how-to" style.
  11. **Wells** (*Short History*): plain declarative synthesis; impersonal.
  12. **Jeans / Eddington**: modern science popularization with analogies.
  13. **Mencken**: modern diction but abrasive tone.
  14. **Twain nonfiction**: maximum flair, 19th-century register.
  15. **Faraday**: model lecture-explainer voice; small.
  16. **Fabre (translated)**: narrative science.
  17. **William James**: *Talks to Teachers* is the most transferable part.
  18. **Tyndall, Darwin, Muir, Burroughs, Jefferies:** descriptive.
  19. **Chesterton**: paradox-driven; poor for memos.
  20. **Huxley**: long periodic sentences.
  21. **Stevenson**: ornate, semicolon-heavy.
  22. **Franklin, Thoreau, Emerson, Montaigne**: least transferable.
- **What the metrics show.**
  - Semicolon rate and mean sentence length separate "Victorian-sounding" from "modern-sounding" more sharply than the archaic-word list does. Huxley (38.4 words; 10/1k), Stevenson (16/1k), Franklin (34.6) and Montaigne (52.2; 15.3/1k) are the outliers. Modern targets would need sentence-splitting or semicolon-to-period rewriting.
  - High "you" rates (Bennett 20.1, S. E. White 21.0, Esenwein & Carnegie 14.5, Faraday 13.4, Post 11.4) mark the corpora most likely to teach an instructive, reader-addressed register.
- **Mixing strategy.** A practical recipe is a two-layer mix:
  1. A modern plain-language base for form (18F + GOV.UK, both CC0/OGL).
  2. One PD "flair" author for voice (Bennett or van Loon, PD in all key jurisdictions).
  - Russell and Mencken add quality but carry jurisdiction or tone risk.

### Gaps
- The metrics are crude proxies. There is no readability or formality classifier, no comparison against a modern reference corpus such as 2020s journalism, and no human rating.
- I did not compute the same metrics for GOV.UK, 18F, gwern, OWID or Distill (not downloaded). Their ranking above rests on their style rules and on reading, not measurement.

## Q3. What are the jurisdiction traps (Orwell, Chesterton, Mencken, US 95-year rule, 1930/1931 cutoffs)?

### Takeaway
There are two traps, one in each direction:
- **UK authors who died after 1955** (Orwell for most works, Russell, Aldous Huxley): life+70 governs the UK/EU, while the US runs on publication year plus 95.
- **US authors who died after 1955** (Mencken, Post, Durant): life+70 has not expired, but the EU/UK "rule of the shorter term" probably already frees their US-PD works.

Cutoffs as of November 2026:
- US: works published in 1930 entered the US PD on 1 Jan 2026. Works published in 1931 (Orwell's "The Spike", "A Hanging") enter on 1 Jan 2027, so they are **not yet PD** today.
- UK/EU: authors who died in 1955 (Dale Carnegie) entered the PD on 1 Jan 2026. Mencken (d. 1956) reaches life+70 on 1 Jan 2027.

### Cited Findings
- **US rule:**
  - Works published before 1931 are PD.
  - Works published 1931–1963 with notice and renewal last "95 years after publication date"; without renewal they are PD.
  - Works from 1964–1977 last 95 years.
  - Foreign works published 1931–1977 were often restored under the URAA, and "Foreign works published after 1928 are likely still under copyright because of URAA" ([Cornell chart](https://guides.library.cornell.edu/copyright/publicdomain)).
- **Evidence that 1930 works entered the US PD on 1 Jan 2026:** PG posted Hammett's *The Maltese Falcon* (1930) as #77600 and Sayers's *The Documents in the Case* (1930) as #77601, both on 2026-01-01. Russell's *The Conquest of Happiness* (1930) was posted 2026-02-09 as #77894 ([PG catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv); [PG #77894](https://www.gutenberg.org/ebooks/77894)).
- **EU rule:**
  - Life+70 (Art. 1); for joint works, counted from the last surviving author (Art. 1(2)).
  - Art. 7(1) (rule of the shorter term): where the country of origin is a third country and the author is not an EU national, "the term of protection... shall expire on the date of expiry of the protection granted in the country of origin of the work, but may not exceed the term laid down in Article 1" ([Directive 2006/116/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006L0116)).
- **UK rule:**
  - s12(2): life+70 from the end of the calendar year of death.
  - s12(6): where the country of origin is not the UK and the author is not a UK national, "the duration of copyright is that to which the work is entitled in the country of origin, provided that does not exceed" life+70 ([CDPA s12](https://www.legislation.gov.uk/ukpga/1988/48/section/12)).
- **Orwell (d. 1950; UK/EU PD since 1 Jan 2021 by life+70):**
  - Wikisource: "Some or all works by this author are in the public domain in the United States because they were published before January 1, 1931". It marks *Down and Out in Paris and London* as "Copyrighted in the United States until 2029 due to Renewal". It lists "The Spike" and "A Hanging" as 1931 essays ([Wikisource](https://en.wikisource.org/wiki/Author:George_Orwell)).
  - The Orwell Foundation: "This material remains under copyright in some jurisdictions, including the US", and it reprints the essays with the Estate's permission ([Orwell Foundation](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/)).
  - Pre-1931 prose: "Censorship in England" (*Monde*, 6 Oct 1928, in French); "A Farthing Newspaper" (*G. K.'s Weekly*, 29 Dec 1928, in English); "A Day in the Life of a Tramp" (*Progrès Civique*, 5 Jan 1929, in French); "Beggars in London" (12 Jan 1929, in French). His "Carlyle" review appeared in *The Adelphi* in March 1931 ([Wikipedia: George Orwell bibliography](https://en.wikipedia.org/wiki/George_Orwell_bibliography)).
  - Standard Ebooks: *Animal Farm* "will... enter the U.S. public domain... on January 1, 2041", and *Nineteen Eighty-Four* on January 1, 2045 ([SE Animal Farm](https://standardebooks.org/ebooks/george-orwell/animal-farm); [SE 1984](https://standardebooks.org/ebooks/george-orwell/nineteen-eighty-four)).
  - PG (US) has no Orwell titles. My catalog query for "Orwell" or "Blair, Eric" returned 0 ([PG catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv)).
- **Mark Twain:** the Mark Twain Project at UC Berkeley "has claimed copyright on that edition until 2047". Standard Ebooks instead uses the 1924 Paine collection ([SE Autobiography](https://standardebooks.org/ebooks/mark-twain/the-autobiography-of-mark-twain)).
- **Editorial-matter co-contributors:** PG #45368 (*Outline of History*) lists editors Ernest Barker (d. 1960) and Gilbert Murray (d. 1957), among others ([PG catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv)).
- **Translations:**
  - Fabre's main translator, Teixeira de Mattos, died 1921. Bernard Miall (*Social Life in the Insect World*) died 1953. Montaigne's translator Cotton died 1687, and editor Hazlitt 1913 ([PG catalog](https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv)).
- **Dataset and metadata traps:**
  - Internet Archive asked that `storytracer/US-PD-Books` be deleted, "because they consider the IA's metadata too unreliable to determine whether a book is in the public domain". The full texts were removed ([HF card](https://huggingface.co/datasets/storytracer/US-PD-Books)).
  - IA search metadata dates *How to Win Friends & Influence People* to 1913 (identifier `howtowinfriendsi0000dale_d7t0`) ([IA](https://archive.org/details/howtowinfriendsi0000dale_d7t0)). The book was first published in 1936, which shows IA dates cannot be trusted for PD decisions.
  - `yoonholee/style-eval-pg-karpathy-gwern` is tagged CC0, yet its contents include 229 Paul Graham essays (562,990 words) from paulgraham.com and Andrej Karpathy blog posts ([HF card](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern)).
- **License-drift traps:**
  - OpenStax titles now carry NC-SA licenses ([OpenStax CMS API](https://openstax.org/apps/cms/api/v2/pages/?type=books.Book&fields=title,license_name,book_state&limit=200)).
  - Write the Docs is CC BY-NC-SA ([LICENSE](https://github.com/writethedocs/www/blob/master/LICENSE.md)).
  - Distill's article footer says CC-BY 2.0 while the repo says CC BY 4.0 ([article](https://distill.pub/2017/momentum/); [repo](https://github.com/distillpub/post--momentum/blob/master/LICENSE)).
- **US government works:** they have no *US* copyright (17 U.S.C. §105) ([Cornell](https://guides.library.cornell.edu/copyright/publicdomain)). 18F closes the foreign gap with an explicit worldwide CC0 waiver ([18F LICENSE](https://github.com/18F/content-guide/blob/main/LICENSE.md)). NASA's wording is limited to "not subject to copyright in the United States" ([NASA](https://www.nasa.gov/nasa-brand-center/images-and-media/)).

### Inferences
- **Status matrix** (US / UK and EU; "PD from" = 1 Jan of death year + 71).
  - **PD everywhere:**
    - Franklin, Faraday, Darwin, Thoreau, Emerson, Jefferies, Nessmuk, Tyndall, Stevenson, Huxley, Twain (except the UC Berkeley edition), William James, Muir, Fabre (with Teixeira de Mattos or Miall translations), BT Washington, Roosevelt, Burroughs, Slosson and Bok.
    - Bennett and Kephart (EU/UK 2002); Beard and Woolf (EU/UK 2012); van Loon, Leacock and Eddington (EU/UK 2015); Wells, Jeans, Strunk, Esenwein and S. E. White (EU/UK 2017).
    - Applies only to their pre-1931 publications in the US.
  - **Chesterton:** EU/UK PD since 2007. US: pre-1931 works only. Post-1930 books (e.g., *Autobiography*, 1936) stay US-protected until 95 years after publication, so 1931 titles free up on 1 Jan 2027. Specific post-1930 titles are from memory, not verified.
  - **Orwell:** EU/UK PD since 2021. In the US, the only clean prose is a handful of 1928–29 pieces (one English, three originally in French; English translations of the French pieces may carry their own translator copyright). That is a few thousand words, so effectively no US Orwell corpus.
    - 1931 pieces ("Carlyle" review, "The Spike", "A Hanging") become US-PD 1 Jan 2027.
    - *Down and Out* (1933) becomes US-PD in 2029.
    - "Shooting an Elephant" (1936) becomes US-PD 1 Jan 2032 by the 95-year arithmetic.
    - "Politics and the English Language" (1946) becomes US-PD 1 Jan 2042.
  - **Russell (d. 1970, UK national):** US-PD for pre-1931 works (e.g., *Conquest of Happiness* since 2026). UK/EU-protected until 1 Jan 2041. The shorter-term rule does not help, because the UK is the country of origin and Russell is a UK national. Post-Brexit, the EU applies Art. 7 to a UK-origin work, which yields the same UK life+70 term anyway.
  - **Aldous Huxley (d. 1963):** *On the Margin* (1923, [PG #60866](https://www.gutenberg.org/ebooks/60866)) is US-PD but UK/EU-protected until 1 Jan 2034. Same trap pattern as Russell.
  - **Mencken (d. 1956, US national, US-origin works):** life+70 would run to 1 Jan 2027. Under EU Art. 7(1) and UK s12(6), protection for his pre-1931 US works probably already expired when the US term did. Post-1930 works (e.g., *Treatise on the Gods*, 1930, US-PD in 2026; later 1930s/40s books) follow the US 95-year dates, capped at life+70, so the UK/EU cap ends at 1 Jan 2027.
  - **Emily Post (d. 1960) and Durant (d. 1981):** the same shorter-term reasoning makes 1922 *Etiquette* and 1926 *Story of Philosophy* likely PD in the UK and in EU states applying Art. 7. A strict life+70 reading would run to 2031 and 2052 respectively, so conservative teams should treat them as US-only.
  - **Dale Carnegie (d. 1955):** UK/EU life+70 expired 31 Dec 2025, so his works are PD there from 1 Jan 2026, including *How to Win Friends* (1936). In the US, *How to Win Friends* is protected until 1 Jan 2032 under the 95-year rule if renewed. The 1915 *Art of Public Speaking* and 1926 *Public Speaking* are US-PD.
  - **Gutenberg, Twain and editors:** PG is a US-law clean source. For non-US training or distribution, check each author against the matrix above. Avoid any Twain text that originates from the Mark Twain Project. The *Outline of History* editors' notes could be separately protected in the UK/EU until 2031 (Barker d. 1960); use *A Short History of the World* (Wells alone) to sidestep this.
  - **Dataset license tags:** treat HF tags as describing the curator's contribution, not the underlying text. Pull from primary sources (PG, Standard Ebooks, gov repos) and keep a per-document provenance and license column.

### Gaps
- The Duke Center for the Study of the Public Domain's 2026 page returned HTTP 500. I relied on Cornell plus PG's January 2026 postings for the 1930 cutoff. I did not get an authoritative list of 1931 works due to enter on 1 Jan 2027.
- Some EU member states may not apply Art. 7's shorter-term rule to US works because of older bilateral treaties (Germany–US 1892 is often cited). Not verified here; get a legal check before relying on shorter-term reasoning for Mencken, Post or Durant in the EU.
- I did not verify whether US federal agencies (e.g., NIST) claim copyright abroad in their non-CC0 works; the NIST page did not render.
- I did not check renewal records (Stanford Copyright Renewal Database, US Copyright Office) for specific 1931–1963 titles (Carnegie, Mencken, Chesterton).
- Whether training (rather than redistributing text) on works PD in one jurisdiction but protected in another is lawful, or covered by TDM exceptions, was out of scope.

## Q4. Existing Hugging Face datasets and bulk sources relevant to these corpora

### Takeaway
No HF dataset packages a single-author nonfiction style corpus from these sources; you would build one from PG, Standard Ebooks or the government repos. Gutenberg mega-dumps (`deepmind/pg19`, `manu/project_gutenberg`, `sedthh/gutenberg_english`, `common-pile/project_gutenberg`) can be filtered by PG ID. The Gutenberg DPO sets (jondurbin, nbeerbower, sam-paech) are fiction-focused but give a reusable recipe: original passage as "chosen", LLM-generated as "rejected".

### Cited Findings
- **`deepmind/pg19`:** Apache-2.0. PG books "published before 1919", with title and publication-date metadata. Offensive words were mapped to placeholders and boilerplate removed ([HF](https://huggingface.co/datasets/deepmind/pg19); [GitHub README](https://github.com/google-deepmind/pg19)).
- **`manu/project_gutenberg`:** "over 70,000 free eBooks", one book per example, header and footer retained, language splits. License points to PG's license ([HF](https://huggingface.co/datasets/manu/project_gutenberg)).
- **`sedthh/gutenberg_english`:** MIT tag, 48,284 rows, metadata includes the PG `text_id` (useful for filtering by the IDs in Q1) ([HF](https://huggingface.co/datasets/sedthh/gutenberg_english)).
- **`common-pile/project_gutenberg` and `common-pile/project_gutenberg_filtered`:** English books "marked as in the Public Domain according to the provided metadata", plus all PG-19 books ([HF](https://huggingface.co/datasets/common-pile/project_gutenberg)).
- **Related Common Pile v0.1 subsets:**
  - `common-pile/usgpo`: 2,732,677 US Government Publishing Office documents, 74.5 GB (Federal Register, hearings, budget reports) ([HF](https://huggingface.co/datasets/common-pile/usgpo)).
  - `common-pile/library_of_congress`: over 130,000 PD books via LoC "Selected Digitized Books" ([HF](https://huggingface.co/datasets/common-pile/library_of_congress)).
  - `common-pile/pressbooks` and `common-pile/libretexts`: PD/CC BY/CC BY-SA (and GFDL for LibreTexts), with per-document license metadata ([HF pressbooks](https://huggingface.co/datasets/common-pile/pressbooks); [HF libretexts](https://huggingface.co/datasets/common-pile/libretexts)).
  - `common-pile/doab`: CC BY and CC BY-SA open-access books ([HF](https://huggingface.co/datasets/common-pile/doab)).
  - `common-pile/news`: CC BY / CC BY-SA news sites ([HF](https://huggingface.co/datasets/common-pile/news)).
  - `common-pile/comma_v0.1_training_dataset` ([HF](https://huggingface.co/datasets/common-pile/comma_v0.1_training_dataset)).
- **`PleIAs/common_corpus`:** 2.27 trillion tokens of "uncopyrighted or freely licensed" data ([HF](https://huggingface.co/datasets/PleIAs/common_corpus)).
- **`institutional/institutional-books-1.0`:** gated, auto-approval; the README is not readable without auth ([HF](https://huggingface.co/datasets/institutional/institutional-books-1.0)).
- **Standard Ebooks on HF:**
  - `Nelathan/standardebooks`: full text from Standard Ebooks, no license tag ([HF](https://huggingface.co/datasets/Nelathan/standardebooks)).
  - `enPurified/standardebooks-enPurified-openai-messages`: CC0 tag ([HF](https://huggingface.co/datasets/enPurified/standardebooks-enPurified-openai-messages)).
- **DPO sets:**
  - `jondurbin/gutenberg-dpo-v0.1`: CC BY 4.0, "meant to enhance novel writing capabilities". Chapters get LLM-written synthetic prompts and summaries ([HF](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1)).
  - `nbeerbower/gutenberg2-dpo`: Apache-2.0, books chosen by personal preference and Claude 3.5 Sonnet recommendation ([HF](https://huggingface.co/datasets/nbeerbower/gutenberg2-dpo)).
  - `nbeerbower/gutenberg-moderne-dpo`: Apache-2.0, early-20th-century "concise prose" ([HF](https://huggingface.co/datasets/nbeerbower/gutenberg-moderne-dpo)).
  - `sam-paech/gutenberg3-generalfiction-scifi-fantasy-romance-adventure-dpo`: 629 PD fiction novels, original text as chosen and LLM text as rejected ([HF](https://huggingface.co/datasets/sam-paech/gutenberg3-generalfiction-scifi-fantasy-romance-adventure-dpo)).
- **OpenStax on HF:**
  - `crumb/openstax-text`: "76 openstax textbooks", tagged CC BY 4.0, last modified 2023-07-14 ([HF](https://huggingface.co/datasets/crumb/openstax-text)).
  - `HuggingFaceTB/openstax_paragraphs`: CC BY 4.0 tag ([HF](https://huggingface.co/datasets/HuggingFaceTB/openstax_paragraphs)).
- **No relevant results:** HF API searches for "gov.uk", "18f", "plain-language", "distill" and "featured-articles" returned no dataset of GOV.UK guidance prose, 18F content, Distill articles or Wikipedia featured articles. The "gov.uk" hits were legislation and policy QA sets, e.g. `i-dot-ai/govuk-policy-qa-pairs` ([HF search](https://huggingface.co/api/datasets?search=gov.uk)).
- **Style-eval prior art:** `yoonholee/style-eval-pg-karpathy-gwern` ("11 internet writers with instantly recognizable but distinct styles") includes gwern; the gwern portion is CC0 at source ([HF](https://huggingface.co/datasets/yoonholee/style-eval-pg-karpathy-gwern); [gwern license](https://gwern.net/about)).

### Inferences
- **Fastest build path:**
  1. Filter `sedthh/gutenberg_english` (it has `text_id`) or `manu/project_gutenberg` by the Q1 PG IDs.
  2. Re-strip PG boilerplate, front matter and indexes.
  3. Deduplicate overlapping collections (Huxley, Wells).
  4. For a modern base, clone the 18F GitHub repos (CC0) and crawl GOV.UK guidance under OGL attribution.
- **Clean-text quality:** Standard Ebooks texts are typographically cleaner than PG. They cover only a subset of these authors (Twain, Darwin, Franklin, James, Russell, van Loon, Roosevelt, Muir, Chesterton, Stevenson travel essays).
- **OpenStax snapshots:** the 2023 `crumb/openstax-text` snapshot may predate OpenStax's move to NC-SA. Copies received under CC BY stay CC BY, since the CC BY 4.0 grant is "irrevocable" ([CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)). Confirm each book's license as of the snapshot date before relying on this.
- **DPO recipe:** for a "storytelling explainer" preference set, apply the nbeerbower/jondurbin recipe to nonfiction chapters (Bennett, van Loon, Slosson, Fabre). Use the original chapter as "chosen" and a base-model rewrite as "rejected".

### Gaps
- I did not inspect row-level contents of `Nelathan/standardebooks` (which titles, which license fields), `PleIAs/common_corpus`'s book subsets, or `institutional/institutional-books-1.0` (gated).
- I could not confirm the PG-19 book count. The README snippet I retrieved did not include it.
- I found no HF dataset of US federal plain-language web content (NPS, NASA, NIH explainers) apart from the USGPO dump, which is mostly legal and regulatory text, not narrative explainers.
