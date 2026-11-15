# Open textbooks as candidate training corpora (licence checked book by book)

Research date: 13 November 2026. Research only: licence pages, front matter, repository READMEs and one sample section per book were read; nothing was cloned or mirrored. Two process notes the report writer should know:

- The fetch tool auto-saved one chapter PDF of Erickson's *Algorithms* (chapter 1, CC BY 4.0) to the session's tool-results folder when I opened it to read a sample. That was the only book file that landed on disk, and I deleted it after reading three pages.
- I read two pages on `book.systemsapproach.org` before I read that host's robots.txt, which disallows a long list of AI agents (including `Claude-User` and `Claude-Code`). The licensed source for that book is the GitHub repository, which is where any later extraction should come from.

Markers used below: **[P]** = read on the book's own site, front matter or repository this session; **[M]** = read on a mirror that shows a per-page licence (LibreTexts); **[S]** = secondary source or search snippet only, not confirmed on the book itself; **[R]** = my recollection, not checked this session. Word counts are my estimates unless a page count is cited; none were measured.

Nothing here is legal advice.

## 1. Licence: what each book or source actually says

### Takeaway
Every OpenStax title checked is now CC BY-NC-SA 4.0 and carries an explicit statement that it may not be used to train large language models without written permission; OpenStax announced the move from mixed CC BY / NC-SA to all NC-SA in a post dated 22 April 2026. The attribution-only books that survived checking are few and mostly computer science and mathematics: Peterson and Davie's *Computer Networks*, Erickson's *Algorithms*, DeVoe's *Thermodynamics and Chemistry*, the Open Logic Project, *Open Data Structures*, Austin's *Understanding Linear Algebra*, Kuttler's *A First Course in Linear Algebra*, Earle's *Physical Geology*, and Lane's public-domain *Online Statistics Education*.

### Cited Findings

#### OpenStax (all titles checked on each book's own preface page)

- Policy change: the post "An update on OpenStax licensing" is dated 2026-04-22 and says OpenStax "transitioned our textbook library from a mix of CC BY and CC BY-NC-SA licensing to CC BY-NC-SA licensing", applying to "all newly released and updated versions of our titles, with limited exceptions." It also says "No action is needed by anyone who has previously created derivatives of CC BY content." Reason given: "highly permissive licenses unintentionally limit our ability to sustain, steward, and guide responsible use of our work." The post does not name the exceptions and does not mention AI. — [OpenStax CMS record of the post](https://openstax.org/apps/cms/api/v2/pages/?type=news.NewsArticle&slug=openstax-licensing&fields=*) (the rendered page at [openstax.org/blog/openstax-licensing](https://openstax.org/blog/openstax-licensing) returned only its title to the fetcher)
- Help centre: "OpenStax textbooks are published under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license." — [OpenStax help: licensing](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks). "Request commercial use: OpenStax Content Reuse Request Form". — [OpenStax help: commercial use](https://help.openstax.org/s/article/Commercial-use-under-the-Creative-Commons-License)
- Statement addressed to AI use, on every preface checked: "This book may not be used in the training of large language models or otherwise be ingested into large language models or generative AI offerings without OpenStax's prior written permission." and "Anyone who intends to incorporate this content (including text, images, and other components) into large language models" is directed to request permission. Recorded as the rights holder's stated position. — [University Physics vol 1 preface](https://openstax.org/books/university-physics-volume-1/pages/preface), [Calculus vol 1 preface](https://openstax.org/books/calculus-volume-1/pages/preface)
- OpenStax help on AI tools: content "may be used with AI tools for noncommercial educational purposes"; you may "use AI to summarize, adapt, create study materials"; the retrieved text was cut off after "Do not upload..." and does not address training. — [OpenStax help: AI tools](https://help.openstax.org/0TO6f0000003F84GAE)
- robots.txt: `User-agent: GPTBot` / `Disallow: /books/`; no other AI crawler named. — [openstax.org/robots.txt](https://openstax.org/robots.txt)
- Source repository: the University Physics repository README says the books "are available under the Creative Commons Attribution-NonCommercial-ShareAlike License license"; folders are `collections`, `modules`, `media`. — [github.com/openstax/osbooks-university-physics](https://github.com/openstax/osbooks-university-physics)
- Wikipedia: before the change "the majority of books were available under the CC BY" licence; OpenStax "has now standardised all of its textbook licences to CC BY-NC-SA"; an older revision says CC BY "except for Calculus, which is available under CC BY-NC-SA". No date given. [S] — [Wikipedia: OpenStax](https://en.wikipedia.org/wiki/OpenStax)
- An earlier CC BY 4.0 copy of University Physics is still published on LibreTexts: "This page titled 5.2: Forces was last modified on Mon, 12 Sep 2022 23:36:27 GMT and is shared under a CC BY 4.0 license and was authored, remixed, and/or curated by OpenStax". [M] — [LibreTexts: University Physics I, 5.2 Forces](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/Book%3A_University_Physics_I_-_Mechanics_Sound_Oscillations_and_Waves_(OpenStax)/05%3A_Newton's_Laws_of_Motion/5.02%3A_Forces)

Per-title results (each from the book's preface page on openstax.org, read this session; "pub." is the citation-block publication date on that page):

| Title (edition checked) | Licence on preface | LLM-training prohibition on page | Pub. date | Source |
|---|---|---|---|---|
| University Physics vol 1 | CC BY-NC-SA 4.0 | yes | 19 Sep 2016 | [preface](https://openstax.org/books/university-physics-volume-1/pages/preface) |
| University Physics vols 2, 3 | not fetched individually; same repository README states NC-SA | not checked | not checked | [repo](https://github.com/openstax/osbooks-university-physics) |
| College Physics 2e | CC BY-NC-SA 4.0 | yes | 13 Jul 2022 | [preface](https://openstax.org/books/college-physics-2e/pages/preface) |
| Calculus vol 1 | CC BY-NC-SA (version not in the quoted sentence) | yes | 30 Mar 2016 | [preface](https://openstax.org/books/calculus-volume-1/pages/preface) |
| Calculus vols 2, 3 | not fetched | not checked | not checked | none |
| Precalculus 2e | CC BY-NC-SA | yes | 21 Dec 2021 | [preface](https://openstax.org/books/precalculus-2e/pages/preface) |
| College Algebra 2e | CC BY-NC-SA 4.0 | yes | 21 Dec 2021 | [preface](https://openstax.org/books/college-algebra-2e/pages/preface) |
| Introductory Statistics 2e | CC BY-NC-SA 4.0 | yes | 13 Dec 2023 | [preface](https://openstax.org/books/introductory-statistics-2e/pages/preface) |
| Biology 2e | CC BY-NC-SA 4.0 | yes | 28 Mar 2018 | [preface](https://openstax.org/books/biology-2e/pages/preface) |
| Concepts of Biology | CC BY-NC-SA | yes | 25 Apr 2013 | [preface](https://openstax.org/books/concepts-biology/pages/preface) |
| Chemistry 2e | CC BY-NC-SA 4.0 | yes | 14 Feb 2019 | [preface](https://openstax.org/books/chemistry-2e/pages/preface) |
| Anatomy and Physiology 2e | CC BY-NC-SA 4.0 | yes | 20 Apr 2022 | [preface](https://openstax.org/books/anatomy-and-physiology-2e/pages/preface) |
| Microbiology | CC BY-NC-SA 4.0 | yes | 1 Nov 2016 | [preface](https://openstax.org/books/microbiology/pages/preface) |
| Astronomy 2e | CC BY-NC-SA | yes | 9 Mar 2022 | [preface](https://openstax.org/books/astronomy-2e/pages/preface) |
| Principles of Economics 3e | CC BY-NC-SA 4.0 | yes | 14 Dec 2022 | [preface](https://openstax.org/books/principles-economics-3e/pages/preface) |
| Psychology 2e | CC BY-NC-SA 4.0 | yes | 22 Apr 2020 | [preface](https://openstax.org/books/psychology-2e/pages/preface) |
| Introduction to Sociology 3e | CC BY-NC-SA 4.0 | yes | 3 Jun 2021 | [preface](https://openstax.org/books/introduction-sociology-3e/pages/preface) |
| American Government 4e | CC BY-NC-SA 4.0 | yes | 23 Jul 2025 | [preface](https://openstax.org/books/american-government-4e/pages/preface) |
| U.S. History | CC BY-NC-SA 4.0 | yes | 30 Dec 2014 | [preface](https://openstax.org/books/us-history/pages/preface) |
| Introduction to Computer Science | CC BY-NC-SA 4.0 | yes | 13 Nov 2024 | [preface](https://openstax.org/books/introduction-computer-science/pages/preface) |
| Introduction to Python Programming | CC BY-NC-SA 4.0 | yes | 13 Mar 2024 | [preface](https://openstax.org/books/introduction-python-programming/pages/preface) |
| Principles of Data Science | CC BY-NC-SA | yes | 24 Jan 2025 | [preface](https://openstax.org/books/principles-data-science/pages/preface) |

A search result reported that the *Maternal-Newborn Nursing* preface still states CC BY 4.0, which may be one of the "limited exceptions"; not opened. [S] — [OpenStax Maternal-Newborn Nursing preface](https://openstax.org/books/maternal-newborn-nursing/pages/preface)

#### Attribution-only or public domain (verified)

- **Peterson and Davie, *Computer Networks: A Systems Approach*** — README: the source "is available on GitHub under terms of the Creative Commons (CC BY 4.0) license." Requested attribution: title, "Authors: Larry Peterson and Bruce Davie", "Copyright: Elsevier, 2012", "Source: https://github.com/SystemsApproach/book", "License: CC BY 4.0". [P] — [github.com/SystemsApproach/book](https://github.com/SystemsApproach/book). The Open Textbook Library also lists CC BY. — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/computer-networks-a-systems-approach). The HTML site's robots.txt disallows `/` for a long list of AI agents (GPTBot, ClaudeBot, Claude-User, Claude-Code, CCBot, Google-Extended, PerplexityBot and others). — [book.systemsapproach.org/robots.txt](https://book.systemsapproach.org/robots.txt)
- The other Systems Approach books are not CC BY: the SDN book is "available on GitHub under terms of the Creative Commons (CC BY-NC-ND 4.0) license." [P] — [github.com/SystemsApproach/sdn](https://github.com/SystemsApproach/sdn)
- **Jeff Erickson, *Algorithms*** — the textbook "is licensed under a Creative Commons Attribution 4.0 International license"; "All other lecture notes are licensed under a more restrictive Attribution-NonCommercial-ShareAlike 4.0 International" licence; "You do not need to ask my permission". [P] — [jeffe.cs.illinois.edu/teaching/algorithms](https://jeffe.cs.illinois.edu/teaching/algorithms/). robots.txt returned 404 (no file).
- **Howard DeVoe, *Thermodynamics and Chemistry*, 2nd ed.** — Open Textbook Library lists CC BY; LibreTexts page "is shared under a CC BY 4.0 license and was authored, remixed, and/or curated by Howard DeVoe". [M] — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/thermodynamics-and-chemistry), [LibreTexts 2.1](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/02%3A_Systems_and_Their_Properties/2.01%3A_The_System_Surroundings_and_Boundary). A search snippet says the author's page states CC BY 4.0 and that a 2012 version carried CC BY-NC-ND, so the version matters. [S] — [www2.chem.umd.edu/thermobook](https://www2.chem.umd.edu/thermobook) (returned 404 to the fetcher)
- **Open Logic Project** — "The Open Logic Text by The Open Logic Project is licensed under a Creative Commons Attribution 4.0 International License." [P] — [github.com/OpenLogicProject/OpenLogic](https://github.com/OpenLogicProject/OpenLogic). Derived books: *Sets, Logic, Computation*; *Incompleteness and Computability*; *Boxes and Diamonds*; *Set Theory: An Open Introduction*; *Intermediate Logic*. — [builds.openlogicproject.org](https://builds.openlogicproject.org/)
- **forall x: Calgary** — "This work is licensed under a Creative Commons Attribution 4.0 International License." [P] — [forallx.openlogicproject.org](https://forallx.openlogicproject.org/)
- **Pat Morin, *Open Data Structures*** — the book and sources "are released under a Creative Commons Attribution License", linked to CC BY 2.5 Canada. [P] — [opendatastructures.org](https://opendatastructures.org/)
- **David Austin, *Understanding Linear Algebra*** — "This work is licensed under a Creative Commons Attribution 4.0 International License"; "2023 Update"; "©2023 David Austin". [P] — [colophon](https://understandinglinearalgebra.org/colophon-1.html)
- **Ken Kuttler, *A First Course in Linear Algebra*** (Lyryx) — OTL lists CC BY; LibreTexts page "shared under a CC BY 4.0 license and was authored, remixed, and/or curated by Ken Kuttler". [M] — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/a-first-course-in-linear-algebra-2017), [LibreTexts 1.2](https://math.libretexts.org/Bookshelves/Linear_Algebra/A_First_Course_in_Linear_Algebra_(Kuttler)/01%3A_Systems_of_Equations/1.02%3A_Elementary_Operations). lyryx.com did not resolve.
- **Steven Earle, *Physical Geology* (BCcampus)** — LibreTexts page "authored, remixed, and/or curated by Steven Earle" and "shared under a CC BY 4.0 license". [M] — [LibreTexts 3.2](https://geo.libretexts.org/Bookshelves/Geology/Physical_Geology_(Earle)/03%3A_Intrusive_Igneous_Rocks/3.02%3A_Magma_and_Magma_Formation). The BCcampus host returned 403; its robots.txt carries a content signal "search=yes, ai-train=no" and disallows GPTBot, ClaudeBot, CCBot, Google-Extended and about thirty other crawlers. Recorded as BCcampus's stated position. — [opentextbc.ca/robots.txt](https://opentextbc.ca/robots.txt)
- **David Lane et al., *Online Statistics Education*** — "This work is in the public domain. Therefore, it can be copied and reproduced without limitation." "However, we would appreciate a citation where possible." [P] — [onlinestatbook.com/2](https://onlinestatbook.com/2/index.html). robots.txt: `User-agent: *` / `Allow: /`. — [robots.txt](https://onlinestatbook.com/robots.txt)
- **Milne Open Textbooks (SUNY Geneseo)** — site footer: "This work is licensed under a Creative Commons Attribution 4.0 International License", except where otherwise noted; per-title licences not shown on the page. Titles include *Real Analysis* (Towsley), *A Contextual Introduction to Real Analysis* (Rogers and Boman), *Introduction to the Modeling and Analysis of Complex Systems* (Sayama). [P, publisher level only] — [milneopentextbooks.org](https://milneopentextbooks.org/)

#### ShareAlike or GFDL (verified)

- **SICP (MIT Press web edition)** — "Structure and Interpretation of Computer Programs by Harold Abelson and Gerald Jay Sussman with Julie Sussman is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License by the MIT Press." [P] — [MIT Press SICP](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/index.html)
- **SICP JS** — text under "a Creative Commons Attribution-ShareAlike 4.0 International License"; programs under "the GNU General Public License v3.0"; the README notes print and ebook versions are published under CC BY-NC-SA. XML source. [P] — [github.com/source-academy/sicp](https://github.com/source-academy/sicp)
- **Benjamin Crowell (Light and Matter, Simple Nature, Conceptual Physics, Mechanics, Fields and Circuits, Modern Physics, relativity books)** — "Web site and books (c) 1998-2019 Benjamin Crowell, CC-BY-SA license.", linked to CC BY-SA 3.0 US. [P] — [lightandmatter.com](https://www.lightandmatter.com/), [Simple Nature page](https://www.lightandmatter.com/area1sn.html)
- **Jim Hefferon, *Linear Algebra*** (also *Theory of Computation*, *Introduction to Proofs*) — "Use it under either the GNU Free Documentation License or the Creative Commons Attribution-ShareAlike 3.0 United States License, at your discretion." [P] — [hefferon.net/source.html](https://hefferon.net/source.html)
- **OpenIntro Statistics** — "Most of OpenIntro's resources, including the Statistics textbooks, are released under a Creative Commons BY-SA 3.0 license." [P] — [openintro.org/license](https://www.openintro.org/license)
- **Dive into Deep Learning** — "This open source book is made available under the Creative Commons Attribution-ShareAlike 4.0 International License."; code "under a modified MIT license." [P] — [github.com/d2l-ai/d2l-en](https://github.com/d2l-ai/d2l-en)
- **Jiří Lebl, *Basic Analysis* I and II; *Notes on Diffy Qs*** — "This work is dual licensed under a Creative Commons Attribution-Noncommercial-Share Alike 4.0 License and Creative Commons Attribution-Share Alike 4.0 License." [P] — [jirka.org/ra](https://www.jirka.org/ra/), [jirka.org/diffyqs](https://www.jirka.org/diffyqs/)
- **Category Theory for Programmers (Milewski; LaTeX edition by Igal Tabachnik)** — the PDF, `.tex` files and figures "are licensed under" CC BY-SA 4.0; content "taken, with permission, from Bartosz Milewski's blogpost series". The blog post itself shows no licence. [P] — [github.com/hmemcpy/milewski-ctfp-pdf](https://github.com/hmemcpy/milewski-ctfp-pdf), [blog chapter 1](https://bartoszmilewski.com/2014/11/04/category-the-essence-of-composition/)
- **Steven Ellingson, *Electromagnetics* vol 1** — OTL lists CC BY-SA; LibreTexts page "is shared under a CC BY-SA 4.0 license and was authored, remixed, and/or curated by Steven W. Ellingson". [M] — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/electromagnetics-vol-1), [LibreTexts 2.2](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electro-Optics/Book%3A_Electromagnetics_I_(Ellingson)/02%3A_Electric_and_Magnetic_Fields/2.02%3A_Electric_Field_Intensity)
- **Grinstead and Snell, *Introduction to Probability*** — OTL lists "Free Documentation License (GNU)". [S: finder only; the Dartmouth page returned 404] — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/21)
- **Judson, *Abstract Algebra: Theory and Applications*** — repository description: "Source in PreTeXt format for open source GFDL-licensed undergraduate textbook". [P, description only; colophon hosts did not resolve] — [github.com/twjudson/aata](https://github.com/twjudson/aata)
- **Wikibooks** — "Text is available under the Creative Commons Attribution-ShareAlike License; additional terms may apply." Featured science and maths books include *Linear Algebra*, *Formal Logic*, *Human Physiology*, *Special Relativity*, *Control Systems*, *Algorithms*, *Haskell*. robots.txt names no AI crawler. [P] — [Wikibooks featured books](https://en.wikibooks.org/wiki/Wikibooks:Featured_books), [robots.txt](https://en.wikibooks.org/robots.txt)

#### NonCommercial (private use at most)

- **Downey**: *Think Python* 3e "is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License" — [ThinkPython](https://allendowney.github.io/ThinkPython/); *Think Stats* 3e: free to copy and modify "as long as you attribute the source and don't use it for commercial purposes" — [ThinkStats](https://allendowney.github.io/ThinkStats/); *Think Bayes* 2e: CC BY-NC-SA 4.0 — [ThinkBayes2](https://allendowney.github.io/ThinkBayes2/); *Think Complexity* 2e: CC BY-NC-SA 4.0 — [Green Tea Press](https://greenteapress.com/wp/think-complexity-2e/). [P]
- **Trench, *Introduction to Real Analysis***: "offered subject to the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License"; dated 12-2013. [P] — [Trinity Digital Commons](https://digitalcommons.trinity.edu/mono/7/)
- **Strang, *Calculus* (MIT OCW)**: footer licence link is CC BY-NC-SA 4.0; first published 1991. [P] — [OCW RES.18-001](https://ocw.mit.edu/courses/res-18-001-calculus-fall-2023/)
- **MIT OpenCourseWare**: CC BY-NC-SA 4.0 with an AI section: "OCW content may be used to train, develop, and improve artificial intelligence and machine learning models"; models must be used non-commercially; derivative models and AI systems that incorporate OCW content through training must be distributed under the same CC BY-NC-SA 4.0 terms or a compatible licence; attribution is required in training documentation. (Fetcher returned short quotes plus paraphrase; the sibling note `institutional_open_publishers.md` holds longer quotes.) robots.txt: `User-Agent: *` / `Allow: /`. [P] — [OCW terms](https://ocw.mit.edu/pages/privacy-and-terms-of-use/), [robots.txt](https://ocw.mit.edu/robots.txt)
- **Nielsen, *Neural Networks and Deep Learning***: CC BY-NC 3.0 Unported per a scraped copy and LibreTexts. [S; the site's certificate failed] — [LibreTexts copy](https://eng.libretexts.org/Bookshelves/Computer_Science/Applied_Programming/Neural_Networks_and_Deep_Learning_(Nielsen))
- **McAfee, *Introduction to Economic Analysis***: OTL and Wikipedia list CC BY-NC-SA (3.0 per Wikipedia); the author's page says only "licensed under a Creative Commons License". [S; author site returned 404] — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/introduction-to-economic-analysis), [Wikipedia](https://en.wikipedia.org/wiki/Introduction_to_Economic_Analysis)
- **APEX Calculus**: OTL lists CC BY-NC; version not confirmed. [S] — [OTL calculus subject page](https://open.umn.edu/opentextbooks/subjects/calculus)
- **Active Calculus**: conflicting. LibreTexts copy shows "CC BY-SA 4.0: 96.8% (92 pages)"; OTL and AIM list CC BY-NC-SA. The book's own colophon returned 404. [S, unresolved] — [LibreTexts detailed licensing](https://math.libretexts.org/Bookshelves/Calculus/Active_Calculus_(Boelkins_et_al.)/zz%3A_Back_Matter/21%3A_Detailed_Licensing)

#### NoDerivatives or all rights reserved (not usable)

- **How to Design Programs 2e**: "© 1 August 2014 MIT Press This material is copyrighted and provided under the Creative Commons CC BY-NC-ND license". [P] — [htdp.org](https://htdp.org/2024-11-6/Book/index.html)
- **Hammack, *Book of Proof***: "© 2018 by Richard Hammack; Licensed under a Creative Commons Attribution-NonCommercial-NoDerivative 4.0 License". [P] — [Book of Proof](https://richardhammack.github.io/BookOfProof/)
- **CORE Econ, *The Economy***: "Licensed under Creative Commons BY NC ND", linked to 4.0. [P] — [CORE Econ](https://books.core-econ.org/the-economy/microeconomics/0-3-contents.html)
- **Physically Based Rendering 4e**: "© 2004-2023 Matt Pharr, Wenzel Jakob, and Greg Humphreys", linked to CC BY-NC-ND 4.0. [P] — [pbr-book.org](https://pbr-book.org/4ed/contents)
- **Motion Mountain**: CC BY-NC-ND (3.0 Germany, with a modification) per the Creative Commons wiki. [S] — [CC wiki case study](https://wiki.creativecommons.org/wiki/Motion_Mountain_-_The_Free_Physics_Textbook)
- **Operating Systems: Three Easy Pieces**: no licence on the page; "This book is and will always be free in PDF form"; instructors are asked to "please just link to them directly (instead of making a copy locally)". All rights reserved by default. [P] — [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- **Mathematics for Machine Learning**: "Copyright 2020 by Marc Peter Deisenroth, A. Aldo Faisal, and Cheng Soon Ong."; "We will keep PDFs of this book freely available."; no open licence. [P] — [mml-book.github.io](https://mml-book.github.io/)
- **David Tong's lecture notes**: "copyright © 2009 David Tong unless otherwise credited"; no CC licence found. [S; site certificate failed] — [Tong teaching page](https://www.damtp.cam.ac.uk/user/tong/teaching.html)
- **Feynman Lectures online**: free to read; Caltech's posting does not grant a right to download any portion. [S; site returned 403] — [feynmanlectures.caltech.edu](https://www.feynmanlectures.caltech.edu)

#### Unclear or unverified

- **Software Foundations**: the LICENSE file begins "Copyright (c) 2026" with wording that matches the MIT licence but does not name it. Thirty-plus contributors; version 7.1 dated 2026-08-24. [P] — [LICENSE](https://softwarefoundations.cis.upenn.edu/lf-current/LICENSE), [index](https://softwarefoundations.cis.upenn.edu/lf-current/index.html)
- **Mathematics for Computer Science (Lehman, Leighton, Meyer)**: listings say CC BY-SA 3.0; the OCW page footer is CC BY-NC-SA 4.0; LibreTexts marks it CC BY-NC-SA 4.0. Not confirmed on the PDF's copyright page. [S, conflicting] — [OCW textbook page](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/resources/mit6_042js15_textbook_pdf/)
- **Levin, *Discrete Mathematics: An Open Introduction***: README licence entry empty to the fetcher; colophon 404. [R: CC BY-SA 4.0] — [github.com/oscarlevin/discrete-book](https://github.com/oscarlevin/discrete-book)
- **LibreTexts**: no sitewide licence page retrieved (404). Licences are per page, shown in a footer line and a "Detailed Licensing" back-matter page per book. robots.txt names no AI crawler. — [libretexts.org/robots.txt](https://libretexts.org/robots.txt)
- **AIM approved textbook list**: about 60 titles; the list page shows no licences, so it is a finder only. — [AIM approved textbooks](https://textbooks.aimath.org/textbooks/approved-textbooks/)
- **Open Textbook Library**: each record has a "Conditions of Use" licence field; site content itself is CC BY 4.0. Finder only. — [OTL entry example](https://open.umn.edu/opentextbooks/textbooks/computer-networks-a-systems-approach)
- **Creative Commons, 3 Sept 2026**: says its existing guidance on AI still holds ("The short answer is: yes.") and that "licensing alone cannot address all of the challenges to sharing that AI presents"; the detailed analysis is in a separate document I did not open. — [CC guidance post](https://creativecommons.org/2026/09/03/guidance-on-using-cc-licenses-in-an-ai-ecosystem/)

### Inferences

What each condition means for the three uses (my reading, not legal advice):

| Condition | Private local fine-tune | Sample outputs in a public README | Releasing adapter weights |
|---|---|---|---|
| CC BY, CC BY 2.5 CA | Fine | Fine; credit the sources in the README | Fine; ship an attribution file |
| CC0 / public domain | Fine | Fine | Fine |
| CC BY-SA | Fine | Fine if outputs are original; any verbatim or closely adapted excerpt must be CC BY-SA | If weights count as adapted material the adapter must be CC BY-SA; plan for that |
| GFDL | Fine | Awkward: verbatim excerpts need the full licence text attached | As ShareAlike, with heavier notice duties; use the CC BY-SA option where dual-licensed (Hefferon) |
| CC BY-NC(-SA) | Probably fine while the project stays non-commercial | Non-commercial only, plus SA where present | Non-commercial only; MIT OCW states derived models must carry CC BY-NC-SA |
| ND | Disputed; avoid | Avoid | No |
| All rights reserved | Rests on fair use alone | Avoid quoting | Not advised |

- OpenStax is the one publisher in this set that pairs an NC-SA licence with an explicit no-LLM-training statement, so it is out even for a private fine-tune unless permission is requested.
- MIT OCW is the one NC source that explicitly permits training, and it explicitly binds the resulting model to NC-SA.
- Copies of OpenStax books obtained under CC BY 4.0 before the change (for example the LibreTexts copy of University Physics, last modified September 2022) remain under CC BY 4.0, since CC licences are not revocable. Using them would be within that licence but against OpenStax's current stated wishes; I would not build the corpus on them.
- LibreTexts licence tags can differ from the original (MCS is tagged CC BY-NC-SA there against CC BY-SA 3.0 elsewhere), so a LibreTexts tag is good evidence only when it agrees with the book's own statement.
- The Systems Approach and BCcampus robots files restrict crawling of their HTML hosts, not the CC BY grant. Taking the text from the GitHub repository (Peterson and Davie) respects both.

### Gaps
- The exact OpenStax effective date per title and the "limited exceptions" are not stated in the post. Calculus vols 2 and 3 and University Physics vols 2 and 3 prefaces were not opened individually.
- Wayback Machine was unreachable, so I could not confirm what each OpenStax preface said before April 2026.
- Not confirmed on the book's own page: DeVoe (author site 404), Kuttler (Lyryx unreachable), Earle (BCcampus 403), Grinstead and Snell, Judson, Nielsen, McAfee, APEX, Active Calculus, Motion Mountain, Tong, Feynman, MCS, Levin.
- Saylor's book page returned only a title; BCcampus collection pages returned 403. No licence information retrieved for either beyond Earle.
- The full Creative Commons 2026 guidance document was not read.

## 2. Size: words of prose and chapters

### Takeaway
No single attribution-only book reaches 300,000 clean words on its own with confidence; the target needs three or four books. Peterson and Davie is the largest verified CC BY prose source.

### Cited Findings
- Erickson *Algorithms*: 472 pages, 13 chapters (0 to 12). — [book page](https://jeffe.cs.illinois.edu/teaching/algorithms/)
- Peterson and Davie: 9 chapters; the sampled section (1.2 Requirements) is about 4,000 words and over 95% prose. — [contents](https://book.systemsapproach.org/), [section 1.2](https://book.systemsapproach.org/foundation/requirements.html)
- Lebl: *Basic Analysis* vol I 312 pages, vol II 217 pages; *Notes on Diffy Qs* 466 pages. — [jirka.org/ra](https://www.jirka.org/ra/), [jirka.org/diffyqs](https://www.jirka.org/diffyqs/)
- Ellingson *Electromagnetics* vol 1: 238 pages, 9 chapters. — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/electromagnetics-vol-1)
- DeVoe: 14 chapters. — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/thermodynamics-and-chemistry)
- Kuttler: 9 chapters; a reviewer describes an earlier edition as "over 400 pages". — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/a-first-course-in-linear-algebra-2017)
- Sampled section lengths: ODS 2.1 about 1,100 words of prose; Austin 2.1 about 2,500 to 3,000; Lane sampling-distribution intro about 1,400; DeVoe 2.1 about 1,000; Lebl 2.1 about 3,000 to 3,500; D2L 3.1 about 3,000 to 3,500; SICP 1.1 about 4,500; Kuttler 1.2 about 1,500 to 2,000. — sample URLs in section 4

### Inferences
Estimated clean prose (pages × roughly 350 to 400 words, reduced for exercises, code and displayed mathematics; treat as ±30%):

| Book | Estimated prose words | Basis |
|---|---|---|
| Peterson and Davie | 200,000 to 250,000 | 9 chapters, roughly 45 sections near 4,000 words; print edition about 800 pages [R] |
| Erickson *Algorithms* | 120,000 to 150,000 | 472 pages, exercises and pseudocode removed |
| DeVoe | 110,000 to 150,000 | about 530 pages [R], prose-heavy in the sample |
| Lane *Online Statistics Education* | 120,000 to 160,000 | about 700 PDF pages [R] |
| Open Logic (all content) | 150,000 to 250,000 prose | very large [R], but only 35 to 45% running prose |
| Kuttler | 60,000 to 80,000 | 400+ pages, about half equations |
| Austin | 60,000 to 90,000 | not measured |
| Open Data Structures | 50,000 to 70,000 | about 300 pages [R], 55 to 65% prose |
| Earle *Physical Geology* | 150,000 to 200,000 | 22 chapters [R] |
| Lebl (three books) | 180,000 to 230,000 | 995 pages, 55 to 65% prose |
| D2L | 250,000+ | about 1,000 pages [R] |
| SICP | 180,000 to 200,000 | about 650 pages [R], 65 to 70% prose |
| Crowell (series) | 300,000+ with heavy overlap between books | [R] |
| Hefferon | 80,000 to 100,000 | about 500 pages [R], proof-heavy |
| OpenIntro Statistics | 100,000 to 120,000 | about 420 pages [R] |
| Each OpenStax science title | 250,000 to 500,000 | [R] |

### Gaps
- No word count was measured; counting would require the source, which I was told not to download.
- Page counts marked [R] were not confirmed this session.

## 3. Source format

### Takeaway
The best extraction targets are the books with plain-markup source in a public repository: Peterson and Davie (reStructuredText), Lebl (LaTeX), Open Data Structures (LaTeX), D2L (Markdown/Jupyter), SICP JS (XML). Erickson and DeVoe are PDF only as far as I could confirm.

### Cited Findings
- Peterson and Davie: reStructuredText, Sphinx build, 420 commits. — [repo](https://github.com/SystemsApproach/book)
- Open Data Structures: "The book's LaTeX sources, Java/C++/Python sources, and build scripts are available through github." — [opendatastructures.org](https://opendatastructures.org/)
- Open Logic: the repository "contains LaTeX source files only"; the sampled file relies on custom macros (`\olsection`, `\iftag`, `!!{formula}` placeholders), so plain-text extraction is not clean. — [repo](https://github.com/OpenLogicProject/OpenLogic), [sample file](https://raw.githubusercontent.com/OpenLogicProject/OpenLogic/master/content/first-order-logic/syntax-and-semantics/terms-formulas.tex)
- Lebl: LaTeX on GitHub (`realanal.tex`, `realanal2.tex`, `diffyqs.tex`); HTML editions also exist. — [jirka.org/ra](https://www.jirka.org/ra/), [jirka.org/diffyqs](https://www.jirka.org/diffyqs/)
- Erickson: the GitHub repository is described as "Bug-tracking for Jeff's algorithms book"; top level shows PDFs, not `.tex`. — [repo](https://github.com/jeffgerickson/algorithms)
- Hefferon: LaTeX on GitLab. — [hefferon.net/source.html](https://hefferon.net/source.html)
- OpenIntro: LaTeX on GitHub (linked from the book page). — [openintro.org/book/os](https://www.openintro.org/book/os/)
- D2L: "drafted in Jupyter notebooks" (Markdown). — [repo](https://github.com/d2l-ai/d2l-en)
- SICP JS: "XML sources of SICP and SICP JS". — [repo](https://github.com/source-academy/sicp)
- CTFP: LaTeX. — [repo](https://github.com/hmemcpy/milewski-ctfp-pdf)
- Judson AATA and Levin: PreTeXt XML. — [aata repo](https://github.com/twjudson/aata), [discrete-book repo](https://github.com/oscarlevin/discrete-book)
- Crowell: LaTeX source linked from the site's books page; PDFs on archive.org. — [Simple Nature page](https://www.lightandmatter.com/area1sn.html)
- Lane: HTML pages; Austin: HTML built from PreTeXt (repository not listed on the colophon). — [onlinestatbook.com](https://onlinestatbook.com/2/index.html), [colophon](https://understandinglinearalgebra.org/colophon-1.html)
- OpenStax: Git repositories with `collections` and `modules` folders. — [repo](https://github.com/openstax/osbooks-university-physics)
- Austin's HTML carries repeated interactive-widget boilerplate that must be stripped. — [section 2.1](https://understandinglinearalgebra.org/sec-vectors-lin-combs.html)

### Inferences
- reStructuredText and Markdown convert to clean prose with the least work; LaTeX needs a math-stripping pass; PreTeXt and CNXML need an XML walk; PDF needs layout-aware extraction and loses the most.
- DeVoe and Earle are easiest to take from their LibreTexts HTML copies, which carry the CC BY 4.0 tag per page.

### Gaps
- Whether DeVoe or Erickson release LaTeX on request was not checked.
- OpenStax module format (CNXML) is my recollection; the README did not name it.

## 4. Prose quality and register (one sampled section each)

### Takeaway
The closest matches to "define, then proceed in steps, one idea per paragraph, precise" are DeVoe, Lebl, Open Data Structures, Lane and the technical core of Peterson and Davie. Erickson is precise but deliberately playful; Earle and Crowell are conversational; Open Logic is precise but more formula than prose.

### Cited Findings
- **Peterson and Davie, 1.2 Requirements**: key terms defined and italicised at first use (link, node, packet, switch, router, multiplexing); each subsection closes with a "Key Takeaway"; over 95% prose, six figures, no code or equations; technical passages dry, with conversational asides ("as if that problem isn't hard enough") and some restating. Sample: "A system that is designed to support growth to an arbitrarily large size is said to scale." — [section](https://book.systemsapproach.org/foundation/requirements.html)
- **DeVoe, 2.1 The System, Surroundings, and Boundary**: terms defined before use, one idea per paragraph, high precision, mostly dry and formal, almost entirely prose with four displayed equations. Sample: "The rest of the physical universe constitutes the surroundings of the system." — [LibreTexts 2.1](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/02%3A_Systems_and_Their_Properties/2.01%3A_The_System_Surroundings_and_Boundary)
- **Erickson, 1.1 Reductions and 1.2 Simplify and Delegate** (read from the chapter PDF): defines the term in the first sentence ("*Reduction* is the single most common technique used in designing algorithms."), argues in clear steps, one idea per paragraph; but openly jokey: "I like to call that someone else the Recursion Fairy", invented words ("skreeble", "glurps", "grindlebloff") and a footnote about elves. About 80% prose on these pages, with one recurrence and one pseudocode box. — [chapter 1 PDF](https://jeffe.cs.illinois.edu/teaching/algorithms/book/01-recursion.pdf)
- **Open Data Structures, 2.1 ArrayStack**: dry expository register; steps given in order (check capacity, resize, shift, store); connectives "Thus", "Therefore"; 55 to 65% prose, five pseudocode blocks. Sample: "Accessing and modifying the elements of an ArrayStack using get(i) and set(i,x) is trivial." — [section](https://opendatastructures.org/ods-python/2_1_ArrayStack_Fast_Stack_O.html)
- **Open Logic, terms and formulas (first-order logic)**: dry and precise, definitions before use, inductive definitions in numbered clauses; only 35 to 45% running prose. Sample: "At the third stage, we construct new formulas from the atomic formulas and those obtained in the second stage, and so on." — [source file](https://raw.githubusercontent.com/OpenLogicProject/OpenLogic/master/content/first-order-logic/syntax-and-semantics/terms-formulas.tex)
- **Lane, Introduction to Sampling Distributions**: plain instructional prose, terms defined, staged argument from a three-ball example to the general case, careful qualifiers ("To be strictly correct, the relative frequency distribution approaches the sampling distribution as the number of samples approaches infinity."); 80 to 85% prose; some second-person address. — [section](https://onlinestatbook.com/2/sampling_distributions/intro_samp_dist.html)
- **Austin, 2.1 Vectors and linear combinations**: definitions precede use, worked example in ordered steps, short paragraphs; first-person plural, mild hedging; 50 to 60% prose, a quarter activities; a few typos ("the the point"). Sample: "A vector is most simply thought of as a matrix with a single column." — [section](https://understandinglinearalgebra.org/sec-vectors-lin-combs.html)
- **Kuttler, 1.2 Elementary Operations**: dry, definitions first, each operation named and shown; roughly half equations; some repetition. — [LibreTexts 1.2](https://math.libretexts.org/Bookshelves/Linear_Algebra/A_First_Course_in_Linear_Algebra_(Kuttler)/01%3A_Systems_of_Equations/1.02%3A_Elementary_Operations)
- **Earle, 3.2 Magma and Magma Formation**: conversational and pedagogical, long analogy ("we partially melted some pretend rock to create some pretend magma"), frequent approximate wording; prose dominant with captions carrying content. — [LibreTexts 3.2](https://geo.libretexts.org/Bookshelves/Geology/Physical_Geology_(Earle)/03%3A_Intrusive_Igneous_Rocks/3.02%3A_Magma_and_Magma_Formation)
- **Lebl, 2.1 Sequences and limits**: numbered definitions before use, proofs in visible stages, high precision, mostly dry with brief asides ("why?", "do it!"); 55 to 65% prose. Sample: "Analysis is essentially about taking limits." — [section](https://www.jirka.org/ra/html/sec_seqsandlims.html)
- **D2L, 3.1 Linear Regression**: terms defined in the opening paragraph, numbered algorithm steps, line-by-line derivation, mostly dry with a few asides; 65 to 75% prose. Sample: "The weights determine the influence of each feature on our prediction." — [section](https://d2l.ai/chapter_linear-regression/linear-regression.html)
- **SICP, 1.1 The Elements of Programming**: evaluation rule as a numbered procedure, high precision, conversational and instructive, occasionally wry; 65 to 70% prose. — [section 1.1](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/full-text/book/book-Z-H-10.html)
- **Ellingson, 2.2 Electric Field Intensity**: definitions first, worked arithmetic, prose dominant; conversational openings ("Imagine the universe is empty..."), a digression, one duplicated word. — [LibreTexts 2.2](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electro-Optics/Book%3A_Electromagnetics_I_(Ellingson)/02%3A_Electric_and_Magnetic_Fields/2.02%3A_Electric_Field_Intensity)
- **CTFP, chapter 1**: clear but blog-voiced, rhetorical questions and humour ("A category is an embarrassingly simple concept."), digressions. — [chapter 1](https://bartoszmilewski.com/2014/11/04/category-the-essence-of-composition/)
- **OpenStax University Physics, 5.2 Forces (2022 LibreTexts copy)**: terms defined before use, a four-step problem-solving box, one idea per paragraph, 80 to 85% prose. Sample: "Dynamics is the study of the forces that cause objects and systems to move." — [LibreTexts 5.2](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/Book%3A_University_Physics_I_-_Mechanics_Sound_Oscillations_and_Waves_(OpenStax)/05%3A_Newton's_Laws_of_Motion/5.02%3A_Forces)

### Inferences
- For an expert judge who does not want "fun", DeVoe and Lebl are the purest register; Peterson and Davie gives the most prose per page; Erickson would teach the model jokes and invented words along with the structure and would need filtering or a lower weight.
- Mathematics books lose a third to a half of each page when equations are stripped, and sentences that lean on displayed formulas become fragments. Prose-dominant subjects (networks, thermodynamics concepts, statistics concepts, geology) extract more cleanly.
- Open Logic's house style is uniform but its prose share is low; its `explain` and `intro` blocks are the usable part.

### Gaps
- Not sampled this session: Hefferon, OpenIntro, Crowell (HTML chapter URLs returned 404), Grinstead and Snell, Judson, Levin, Active Calculus, APEX, Trench, Strang, Downey's books, Nielsen, OSTEP, HtDP, Software Foundations, MML, CORE, PBR, Motion Mountain, Tong, Feynman, McAfee, MCS, Wikibooks titles, forall x. Most of these are excluded on licence anyway; Hefferon, OpenIntro and Crowell are the ones that matter for the ShareAlike option.
- Each judgement rests on one section and was summarised by the fetch model, except Erickson, which I read directly.

## 5. Authorship and consistency

### Takeaway
Single-author books with a uniform voice: Erickson, DeVoe, Lebl, Morin, Austin, Kuttler, Earle, Ellingson, Crowell, Hefferon. Peterson and Davie is a two-author book with one voice. OpenStax, Open Logic, D2L, Wikibooks and LibreTexts are multi-contributor.

### Cited Findings
- Erickson: sole author, "Copyright 2019 Jeff Erickson". — [repo](https://github.com/jeffgerickson/algorithms)
- Peterson and Davie: "Authors: Larry Peterson and Bruce Davie"; community corrections accepted through GitHub. — [repo](https://github.com/SystemsApproach/book)
- Open Logic: "authored and edited by an international team of logicians" and "open to contributions by the community". — [openlogicproject.org](https://openlogicproject.org/)
- Lane: "Developed by Rice University (Lead Developer), University of Houston Clear Lake, and Tufts University"; project leader David M. Lane; the sampled section is by Lane. — [onlinestatbook.com](https://onlinestatbook.com/2/index.html)
- OpenStax Calculus: two senior contributing authors (Strang, Herman) plus sixteen contributing authors. — [Calculus vol 1 preface](https://openstax.org/books/calculus-volume-1/pages/preface)
- D2L: four named authors (Zhang, Lipton, Li, Smola) plus community contributors. — [d2l.ai](https://d2l.ai/)
- Software Foundations vol 1: eight authors and twenty-three further contributors. — [index](https://softwarefoundations.cis.upenn.edu/lf-current/index.html)
- Kuttler: "originally by K. Kuttler and redesigned by the Lyryx editorial team". — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/a-first-course-in-linear-algebra-2017)
- Earle 2nd edition: Karla Panchuk also appears as an author on a 2nd-edition title page. [S] — [CCC Online Pressbooks copy](https://pressbooks.ccconline.org/physicalgeology/chapter/title-page-physical-geology-2nd-edition/)

### Inferences
- Several books by one author with a house style, as the brief prefers, exist only under ShareAlike: Lebl (three books), Crowell (about ten), Hefferon (three). Under attribution-only, the nearest equivalent is the Open Logic family, which is one edited style across five or six books.
- Lane's book has chapters by other contributors; filtering to Lane-authored sections would tighten the voice.

### Gaps
- Voice consistency across whole books was not tested; one section per book was read.

## 6. Dates and pre-December-2022 status

### Takeaway
Most strong candidates were written well before December 2022. The exceptions are the newest OpenStax titles and anything under continuous revision (Open Logic, Lebl, Software Foundations), where later edits are small relative to the body.

### Cited Findings
- Erickson: 1st edition June 2019. — [book page](https://jeffe.cs.illinois.edu/teaching/algorithms/)
- Peterson and Davie: attribution copyright "Elsevier, 2012"; site shows 6th edition, "Version 6.2-dev", "© Copyright 2024"; OTL copyright year 2019. — [repo](https://github.com/SystemsApproach/book), [site](https://book.systemsapproach.org/), [OTL entry](https://open.umn.edu/opentextbooks/textbooks/computer-networks-a-systems-approach)
- DeVoe: 2nd edition, copyright 2019, updated 2020. — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/thermodynamics-and-chemistry)
- Austin: "2023 Update". — [colophon](https://understandinglinearalgebra.org/colophon-1.html)
- Kuttler: 2023 edition of an older text. — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/a-first-course-in-linear-algebra-2017)
- Lebl: *Basic Analysis* version 6.3, 15 May 2026; *Diffy Qs* version 6.11, 18 May 2026. — [jirka.org/ra](https://www.jirka.org/ra/), [jirka.org/diffyqs](https://www.jirka.org/diffyqs/)
- Open Logic: builds generated from a revision dated 2026-07-12. — [builds](https://builds.openlogicproject.org/)
- Crowell: copyright range 1998 to 2019. — [lightandmatter.com](https://www.lightandmatter.com/)
- Ellingson vol 1: 2018. — [OTL entry](https://open.umn.edu/opentextbooks/textbooks/electromagnetics-vol-1)
- Trench: 2013; Strang *Calculus*: 1991; HtDP 2e: 2014; Hammack 3rd ed.: 2018 (edition 3.4 issued 5 February 2025 for typos); MML: 2020; PBR 4e: 2023. — sources in section 1
- Downey: *Think Python* 3e, *Think Stats* 3e and *Think Bayes* 2e pages all show "© Copyright 2023". — [ThinkPython](https://allendowney.github.io/ThinkPython/)
- OpenStax titles published after December 2022: Introductory Statistics 2e (Dec 2023), Introduction to Python Programming (Mar 2024), Introduction to Computer Science (Nov 2024), Principles of Data Science (Jan 2025), American Government 4e (Jul 2025). Principles of Economics 3e is dated 14 Dec 2022. — per-title table in section 1

### Inferences
- Erickson, DeVoe, Crowell, Ellingson, SICP, Trench, Lane, Open Data Structures and the bulk of Peterson and Davie predate common LLM-assisted writing. Lebl and Open Logic have pre-2022 bodies with ongoing small revisions; pinning a pre-2023 Git tag would remove doubt.
- Austin's first edition predates 2022 [R]; the 2023 update's extent is unknown.

### Gaps
- First-publication dates for Lane, Open Data Structures, Hefferon, OpenIntro, D2L, Earle and Open Logic were not confirmed this session (my recollection: roughly 2003 to 2013, 2013, 1990s to 2020, 2009 to 2019, 2019 to 2023, 2015 and 2019, 2014 onward).

## 7. Memorisation risk

### Takeaway
No source measured this; the ranking below is my judgement from how widely each text is mirrored.

### Cited Findings
- The texts with many public mirrors found in this session's searches: MCS (many PDF mirrors and OCW), Nielsen (several scraped PDF copies), Feynman, SICP (MIT Press full text online). — [MCS search hit: OCW](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/resources/mit6_042js15_textbook_pdf/), [Nielsen LibreTexts copy](https://eng.libretexts.org/Bookshelves/Computer_Science/Applied_Programming/Neural_Networks_and_Deep_Learning_(Nielsen)), [SICP](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/index.html)
- Earle, DeVoe, Kuttler, Ellingson and OpenStax books are mirrored on LibreTexts and on multiple Pressbooks instances. — [search result list for Earle](https://geo.libretexts.org/Bookshelves/Geology/Physical_Geology_(Earle))

### Inferences
- High: SICP, Feynman, OSTEP, D2L, OpenStax core titles, Nielsen, Think Python, MCS.
- Medium: Peterson and Davie (a standard networking text for decades), Erickson, Hefferon, OpenIntro, Crowell, Grinstead and Snell.
- Lower: DeVoe, Lebl, Open Logic, Open Data Structures, Austin, Kuttler, Lane, Ellingson, Earle.
- For a style fine-tune, memorisation mainly weakens held-out evaluation; hold out whole chapters and prefer the lower-risk books for test sets.

### Gaps
- No memorisation probe was run and no published measurement was found for any of these books.

## 8. One-line verdict per book

### Takeaway
Nine sources are usable now, about a dozen are usable with ShareAlike strings, and all of OpenStax moves to "not usable without permission".

### Cited Findings
(Licence sources are in section 1; the verdict column is my conclusion.)

| Book or source | Licence | Verified | Verdict |
|---|---|---|---|
| Peterson and Davie, *Computer Networks* | CC BY 4.0 | [P] | Usable now (take from GitHub) |
| Erickson, *Algorithms* | CC BY 4.0 | [P] | Usable now; jokey register, PDF only |
| DeVoe, *Thermodynamics and Chemistry* 2e | CC BY 4.0 | [M] | Usable now; confirm on the PDF |
| Open Logic Project texts | CC BY 4.0 | [P] | Usable now; low prose share |
| forall x: Calgary | CC BY 4.0 | [P] | Usable now; not sampled |
| Open Data Structures | CC BY 2.5 CA | [P] | Usable now; small |
| Austin, *Understanding Linear Algebra* | CC BY 4.0 | [P] | Usable now |
| Kuttler, *First Course in Linear Algebra* | CC BY 4.0 | [M] | Usable now; confirm on the PDF |
| Earle, *Physical Geology* | CC BY 4.0 | [M] | Usable now by licence; host says ai-train=no; conversational |
| Lane, *Online Statistics Education* | Public domain | [P] | Usable now |
| Milne Open Textbooks | CC BY 4.0 site default | [P] | Check each title |
| Lebl, *Basic Analysis* I, II; *Diffy Qs* | CC BY-SA 4.0 (or NC-SA) | [P] | ShareAlike strings |
| Hefferon, *Linear Algebra* | CC BY-SA 3.0 US or GFDL | [P] | ShareAlike strings |
| OpenIntro Statistics | CC BY-SA 3.0 | [P] | ShareAlike strings |
| Crowell series | CC BY-SA 3.0 US | [P] | ShareAlike strings |
| D2L | CC BY-SA 4.0 | [P] | ShareAlike strings; memorised |
| SICP; SICP JS | CC BY-SA 4.0 | [P] | ShareAlike strings; memorised |
| CTFP (LaTeX edition) | CC BY-SA 4.0 | [P] | ShareAlike strings; blog voice |
| Ellingson, *Electromagnetics* | CC BY-SA 4.0 | [M] | ShareAlike strings |
| Wikibooks featured books | CC BY-SA | [P] | ShareAlike strings; uneven |
| Judson AATA; Grinstead and Snell | GFDL | [S] | ShareAlike strings, awkward notices |
| MCS; Levin; Active Calculus | conflicting or unconfirmed | [S] | Do not use until confirmed |
| Software Foundations | MIT-style text, unnamed | [P] | Licence fine if MIT; mostly code |
| MIT OCW, Strang *Calculus* | CC BY-NC-SA 4.0, training allowed non-commercially | [P] | Private or non-commercial only; model inherits NC-SA |
| Downey's *Think* books; Trench; Nielsen; McAfee; APEX | NC variants | [P]/[S] | Private use only |
| All OpenStax titles checked | CC BY-NC-SA 4.0 plus no-LLM statement | [P] | Not usable without permission |
| HtDP; Hammack; CORE; PBR; Motion Mountain | CC BY-NC-ND | [P]/[S] | Not usable |
| OSTEP; MML; Tong; Feynman | All rights reserved | [P]/[S] | Not usable |

### Inferences
- The brief's assumption that OpenStax could anchor the corpus no longer holds as of April 2026.

### Gaps
- Books marked [M] or [S] need one look at the PDF's own copyright page before use.

## 9. Ranked top ten, best combinations and subject coverage

### Takeaway
An attribution-only corpus of roughly 500,000 to 700,000 estimated words is reachable from Peterson and Davie, DeVoe, Lane, Erickson and Open Data Structures, but it is computer-science heavy and has no life science or economics. Accepting ShareAlike adds Lebl, Crowell, Hefferon, OpenIntro and Ellingson, which fills mathematics and physics; life science and economics stay empty.

### Cited Findings
- All licence, size and prose facts used here are cited in sections 1 to 6.

### Inferences

**(1) Ranked top ten for the stated goal** (licence first, then register, prose share and ease of extraction):

1. Peterson and Davie, *Computer Networks* — CC BY 4.0, RST source, over 95% prose, largest single source; trim the conversational asides.
2. DeVoe, *Thermodynamics and Chemistry* — CC BY 4.0, single author, the driest and most exact register sampled.
3. Lebl, *Basic Analysis* and *Notes on Diffy Qs* — best single-author house style with LaTeX source; ShareAlike.
4. Lane, *Online Statistics Education* — public domain, plain careful exposition, HTML.
5. Open Logic Project texts — CC BY 4.0, uniform and exact; use the explanatory blocks only.
6. Erickson, *Algorithms* — CC BY 4.0, excellent structure; down-weighted for humour and PDF-only source.
7. Open Data Structures — CC BY, LaTeX, dry; small.
8. Kuttler, *A First Course in Linear Algebra* — CC BY, dry; half equations.
9. D2L — strong step-by-step exposition, Markdown source; ShareAlike, multi-author, memorised.
10. Austin, *Understanding Linear Algebra* — CC BY 4.0; activity-heavy and conversational "we".

Next in line: Hefferon, OpenIntro, Crowell, Ellingson (all ShareAlike), Earle (CC BY but conversational, and the host signals no AI training), SICP (memorised).

**(2) Best attribution-only combination (CC BY, CC0, public domain)**

Peterson and Davie + DeVoe + Lane + Erickson + Open Data Structures, with Kuttler and the Open Logic explanatory prose as optional additions. Estimated total 600,000 to 780,000 words before cleaning, so the 300,000 minimum holds even if the estimates are 40% high or Erickson is dropped. The first three alone come to an estimated 430,000 to 560,000.

**(3) Best combination if ShareAlike is acceptable**

The set above plus Lebl (three books), Crowell (pick *Simple Nature* or the *Light and Matter* series, not both, because they overlap), Hefferon, OpenIntro Statistics and Ellingson. Estimated total above 1.2 million words. The adapter and any published excerpts should then be treated as CC BY-SA.

**(4) Subject coverage**

| Subject | Attribution-only set | ShareAlike set adds |
|---|---|---|
| Mathematics | Kuttler, Austin (linear algebra); Open Logic (logic, set theory) | Lebl (analysis, differential equations), Hefferon |
| Physics | DeVoe covers thermodynamics only | Crowell (introductory physics), Ellingson (electromagnetics) |
| Computer science | Peterson and Davie, Erickson, Open Data Structures | D2L, SICP |
| Statistics | Lane | OpenIntro Statistics |
| Chemistry | DeVoe (physical chemistry) | none |
| Life science | none | none verified (Wikibooks *Human Physiology* is a lead) |
| Economics | none | none |
| Earth science | Earle, if used | none |

- The only verified open sources for life science and economics in this pass were OpenStax (now closed to training), CORE (ND) and McAfee (NC-SA, unconfirmed).

### Gaps
- No CC BY or CC BY-SA economics or biology textbook was verified. Leads not checked: Open Oregon *Principles of Biology*, University of Minnesota Libraries editions of former Flat World titles (usually NC-SA), Lyryx economics titles, individual Milne titles.
- The combination totals rest on unmeasured word estimates.
- Whether OpenStax would grant written permission for a non-commercial local fine-tune is unknown; its reuse request form is the route.
