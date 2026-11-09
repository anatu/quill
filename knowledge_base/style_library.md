# Patrick McKenzie tops the style shortlist

> Decision 2026-11-08: the user chose **Morgan Housel**, trained on Housel alone first (`housel_augmentation.md`). The user reports written consent from Collaborative Fund; its Terms of Use (Feb 2026) otherwise ban scraping and storage. McKenzie (Kalzumeus 2011+) is the fallback.

Date: 7 Nov 2026. Built from the four notes in `research_notes/Nonfiction author style corpora/`. Technical constraints (corpus size, memorization, eval) come from `lit_review.md` and `plan.md`. Not legal advice.

Size labels used throughout:
- **measured**: every post or file counted (full crawl, Substack's own `wordcount` field, `wc -w` on Gutenberg text).
- **estimated**: sampled mean × post count.
- **self-reported**: the site's own statistics.
- **guess**: an unmeasured figure from the notes.

## 1. Top picks

| Role | Option | Why | Clean corpus |
|---|---|---|---|
| **Best overall fit** | Patrick McKenzie (patio11): Kalzumeus + Bits about Money | Explains how money, software and institutions work through insider anecdotes and dry wit. Modern. No public dataset copies found. | ~460k words of written essays, measured 2026-11-08 (2011+ Kalzumeus + Bits about Money) |
| Cleanest licence | Venkatesh Rao, Ribbonfarm | Explicit AI-training permission. No other large, modern, single-author corpus in the notes has that. | 1,539,789 words, self-reported |
| Best memo voice | Morgan Housel, Collaborative Fund blog | Anecdote, then one principle, in ~1,000-word posts. Near-zero politics. Topic-agnostic. | ~340k, estimated (±30%) |
| Best how-to and docs voice | Julia Evans, jvns.ca | Warm first-person explainers with numbered steps and tiny examples. | ~627k, estimated |
| Public-domain fallback | Arnold Bennett, self-help and essays | Second-person practical argument with ironic asides. Public domain in the US, UK and EU. | ~303k, measured (upper bound) |

Wildcard worth one email: **Dynomight**. It fits as well as anyone and carries the only human-authorship guarantee in the library. The author has switched on Substack's AI-training block, so use it only with written permission.

**Recommendation: Patrick McKenzie.**
1. **Genre.** His essays explain mechanisms and wrap them in stories. That matches a PM's daily output: how a system works, why it breaks, what to do.
2. **Distance from LLM prose.** The notes rate his voice "High": long parenthetical sentences, insider asides, dry wit. Housel ties him on total, but Housel's cadence "has been widely imitated, including by LLMs", so a Housel adapter buys less over the prompt-only baseline.
3. **Headroom.** ~460k words of written essays from 2011 on (measured 2026-11-08). That clears the 200k floor after dropping the 2006-2010 microISV era, podcast transcripts and a 10% holdout.
4. **Low prior exposure.** No Hugging Face dataset of his writing turned up. Paul Graham has 15+. That means a weaker prompt-only baseline to beat. By inference it also means less latent memorization to reactivate.
5. **The cost is consent.** His work is all rights reserved. A private, local, undistributed fine-tune sits on the favourable side of the 2025 rulings (Section 5), but that rests on fair use, and he has granted nothing. His robots.txt (checked 2026-11-07) restricts nothing and adds a 2025 note welcoming AI crawlers; Bits about Money's robots.txt blocks no AI bots. That is a friendly signal, not a licence. Crawl politely and email him first.

Taste check before committing: read two of his essays. If the long sentences grate, swap to Housel (shorter) or Joel Spolsky (punchier, harder to acquire).

## 2. Selection criteria and scoring

The scores are my judgment calls, grounded in the notes. 5 is always best, so for contamination and bleed a 5 means low risk. The notes rate "distance from LLM voice" for most modern authors. I map their labels to the Voice column: very high or very far = 5, high = 4, medium-high, moderately far or medium = 3, low-medium = 2, close to neutral = 1. A † marks a Voice score that is my own judgment (no rating in the notes, or I departed from it).

| Criterion | 5 means | 1 means | Middle bands |
|---|---|---|---|
| Genre | Most pieces explain or instruct and also tell stories | Neither | 3 = one of the two |
| Voice | Very far from generic LLM prose | Close to neutral explainer prose | see mapping above |
| Transfer | Topic-agnostic, memo-length pieces | Locked to one niche | |
| Size | ≥500k clean words after obvious filtering | <100k or unknown | 4 = 300-500k; 3 = 200-300k; 2 = 100-200k |
| Legal | PD in US/UK/EU, CC0, CC BY, OGL, or explicit training grant | Author has opted out of AI training | 4 = PD in US and probably UK/EU, or conflicting open licences; 3 = all rights reserved or silent, self-hosted, no opt-out found, or US-only PD; 2 = platform terms bar crawling, or the site blocks bots |
| Contamination | One author, little quoting, no LLM text | Heavy quotes, guests, co-authors or LLM output | |
| Bleed | Low politics, broad topics | Partisan, or one niche | |
| Diction | 2010s-2020s prose | Victorian periodic sentences | 3 = plain 1920s; 2 = Edwardian |

"Copies" is unscored. It records public dataset copies found in the notes. More copies mean a stronger prompt-only baseline and, by inference, more latent memorization in base models.

Group letters: (a) open or training-permitted modern; (b) public domain; (c) copyrighted tech and product; (d) copyrighted science, business and history; (e) house style.

| Option | Genre | Voice | Transfer | Size | Legal | Contam. | Bleed | Diction | **Total** | Copies |
|---|---|---|---|---|---|---|---|---|---|---|
| Patrick McKenzie (c) | 5 | 4 | 4 | 5 | 3 | 4 | 4 | 5 | **34** | none found |
| Morgan Housel (d) | 4 | 3 | 5 | 4 | 3 | 5 | 5 | 5 | **34** | none found |
| Venkatesh Rao, Ribbonfarm (a) | 3 | 5 | 3 | 5 | 5 | 4 | 3 | 5 | **33** | none found |
| Dynomight (d) | 5 | 5 | 4 | 4 | 1 | 5 | 4 | 5 | **33** | none found |
| Paul Graham (c) | 4 | 3† | 4 | 5 | 3 | 5 | 4 | 5 | **33** | 15+ HF sets |
| Joel Spolsky (c) | 5 | 4 | 5 | 3 | 2 | 4 | 5 | 4 | **32** | partial (yoonholee) |
| Julia Evans (c) | 4 | 4 | 4 | 5 | 3 | 4 | 3 | 5 | **32** | none found |
| Scott Alexander (d) | 4 | 5 | 4 | 5 | 3 | 3 | 3 | 5 | **32** | ACX HF set, yoonholee |
| Cal Newport (d) | 4 | 3† | 5 | 5 | 3 | 4 | 3 | 5 | **32** | not searched |
| Arnold Bennett (b) | 4 | 4† | 4 | 3 | 5 | 4 | 4 | 3 | **31** | Gutenberg dumps |
| Bertrand Russell (b, US only) | 4 | 4† | 5 | 4 | 3 | 4 | 3 | 4 | **31** | Gutenberg dumps |
| Jeff Atwood (c) | 4 | 4 | 4 | 5 | 3 | 3 | 4 | 4 | **31** | none found |
| Dan Luu (c) | 4 | 4 | 3 | 5 | 3 | 3 | 4 | 5 | **31** | none found |
| Charity Majors (c) | 4 | 5 | 4 | 3 | 2 | 5 | 3 | 5 | **31** | none found |
| Adam Mastroianni (d) | 4 | 5 | 3 | 4 | 2 | 4 | 4 | 5 | **31** | none found |
| Edwin Slosson (b) | 5 | 3† | 4 | 2 | 5 | 4 | 3 | 4 | **30** | Gutenberg dumps |
| Steven Sinofsky (c) | 4 | 3 | 4 | 5 | 2 | 4 | 3 | 5 | **30** | not searched |
| Maciej Cegłowski (c) | 3 | 5 | 3 | 4 | 3 | 4 | 3 | 5 | **30** | yoonholee |
| Howard Marks (d) | 5 | 3† | 4 | 5 | 3 | 3 | 3 | 4 | **30** | none found |
| Aswath Damodaran (d) | 5 | 3† | 3 | 5 | 3 | 4 | 2 | 5 | **30** | not searched |
| Bret Devereaux (d) | 4 | 5 | 2 | 5 | 3 | 5 | 2 | 4 | **30** | none found |
| Gwern (a) | 3 | 5 | 2 | 5 | 5 | 2 | 3 | 4 | **29** | yoonholee |
| Kevin Kelly (a) | 3 | 3 | 3 | 4 | 4 | 3 | 4 | 5 | **29** | none found |
| Simon Willison (c) | 4 | 3 | 4 | 5 | 3 | 2 | 3 | 5 | **29** | none found |
| H. L. Mencken (b) | 3 | 5† | 2 | 5 | 4 | 4 | 2 | 4 | **29** | Gutenberg dumps |
| GOV.UK (e) | 2 | 2† | 5 | 3 | 5 | 4 | 3 | 5 | **29** | none found |
| 18F (e) | 3 | 2† | 5 | 2 | 5 | 3 | 4 | 5 | **29** | none found |
| Cory Doctorow, Pluralistic (a) | 3 | 5 | 2 | 5 | 5 | 2 | 1 | 5 | **28** | none found |
| Hendrik van Loon (b) | 4 | 4† | 3 | 3 | 5 | 4 | 2 | 3 | **28** | Gutenberg dumps |
| Mark Twain, nonfiction (b) | 3 | 5† | 2 | 5 | 5 | 3 | 2 | 2 | **27** | Gutenberg dumps |
| T. H. Huxley (b) | 4 | 4† | 2 | 5 | 5 | 3 | 3 | 1 | **27** | Gutenberg dumps |
| Emily Post (b) | 4 | 3† | 3 | 3 | 4 | 4 | 2 | 4 | **27** | Gutenberg dumps |
| Our World in Data (e) | 3 | 1 | 4 | 2 | 5 | 3 | 3 | 5 | **26** | not searched |

How to read the totals:
- **They cluster between 26 and 34.** Treat the total as a screen. Three columns decide: Voice (the only reason to fine-tune at all), Transfer (your tasks are memos and docs) and Legal.
- **Almost nobody writes memos.** Only Howard Marks (client memos) and the house styles write in memo or doc form. For everyone else, transfer is the bet. Chunking posts into 150-800-word pieces gets you memo-length targets.
- **Tie at 34.** McKenzie beats Housel on Voice and Size. Housel beats McKenzie on Transfer. The fine-tune exists to move away from LLM prose, so Voice breaks the tie.
- **Dynomight with permission scores 37.** Its Legal score jumps from 1 to 5. That puts it top of the table.
- **Paul Graham scores well and is a poor pick.** He is the most scraped author in the notes. Prompting already gets his surface tics. Use him as a benchmark author.

## 3. Option profiles

### (a) Openly licensed or training-permitted modern authors

#### Venkatesh Rao, Ribbonfarm (33): cleanest licence
- **Corpus:** [ribbonfarm.com](https://ribbonfarm.com), a static archive since April 2026. Rao: 875 posts, **1,539,789 words**, average 1,760 (self-reported, [stats page](https://ribbonfarm.com/stats/)). The site holds 1,117 posts and 2,117,465 words in total, with about 59 guest contributors. His Contraptions Substack adds 905,392 free words (measured), but the grant does not cover it.
- **Licence and signals:** All rights reserved, plus "Limited non-exclusive permission is granted to AI and machine learning systems to crawl, index, and use this site's content for training language models". The only condition is to acknowledge ribbonfarm.com in any *public* disclosure of training-data provenance. `tdmrep.json` sets `"tdm-reservation": 0`. No AI-bot blocks. Guests keep their own copyright, so drop guest posts ([copyright](https://ribbonfarm.com/copyright/)).
- **Markers:** coined concepts and neologisms; grand organising theories; organisational and management analysis; essay-length arguments.
- **Best for:** strategy analyses, org-design memos, framing essays.
- **Risks:** the grand-theory register overshoots plain memos and how-tos. Gervais-Principle cynicism about organisations (medium bleed). Drift from early essays to later protocol-focused writing.
- **Read:** "The Gervais Principle", "A Big Little Idea Called Legibility", "The Internet of Beefs", all listed on the [stats page](https://ribbonfarm.com/stats/).

#### Gwern Branwen, gwern.net (29)
- **Corpus:** 609 essay-like pages, **~3.04M words** (estimated: 40-page sample, mean 4,996, median 2,026). A third-party set counts 2,800,357 words for 220 pieces. The site self-reports >4.38M words (2022), including documents he transcribed. Append `.md` to any page URL to get Markdown.
- **Licence:** CC0 ([about](https://gwern.net/about)). No AI-bot blocks.
- **Markers:** dense, hedged prose with epistemic-status notes; sidenotes and very long footnotes; statistics and Bayesian vocabulary; rare words; heavy quotation.
- **Best for:** long analyses and literature reviews.
- **Risks:** weak transfer to memos. The notes disagree here: the tech note says "low", the open-licence note says "very high for analysis, weaker for crisp how-tos". Heavy quotation and transcribed text. Pages are revised continuously. His AI pages may embed model output (my inference; check). He is in the yoonholee style-eval set.
- **Read:** [The Scaling Hypothesis](https://gwern.net/scaling-hypothesis); [Why so few Matt Levines?](https://gwern.net/matt-levine).

#### Kevin Kelly, The Technium (29)
- **Corpus:** 880 posts (WordPress API). **~0.7M words**, a rough estimate: the latest 100 posts average 801 words, and older posts were not measured. Drop the "Weekly Links" roundups.
- **Licence:** the signals conflict. The Technium sidebar links CC BY-NC-SA 3.0; the kk.org footer links CC BY 4.0 ([Technium](https://kk.org/thetechnium/)). Either licence permits private, non-commercial copying with attribution. Ask him which applies before relying on BY.
- **Markers:** aphoristic; optimistic; big-picture technology essays; short posts.
- **Best for:** short framing memos on technology trends.
- **Risks:** posts are short; the size is uncertain; nobody knows whether ShareAlike reaches model weights.
- **Read:** [The Technium](https://kk.org/thetechnium/) (the notes name no single post).

#### Cory Doctorow, Pluralistic (28)
- **Corpus:** 1,746 posts, **~5.23M gross words** (estimated: 246-post sample, mean 2,995). The essay share is probably half or less after removing the link lists, the "Object permanence" sections and the colophon (guess).
- **Licence:** CC BY 4.0, excluding serialized fiction, quotations and images. Attribution plus a link is required ([post footer](https://pluralistic.net/2026/11/07/aeiou-but-sometimes-why/)).
- **Markers:** polemical; coined terms ("enshittification"); long cumulative sentences; links as evidence; the same post structure every time.
- **Best for:** advocacy and tech-policy argument.
- **Risks:** the highest political bleed of the open options; very recognisable; templated boilerplate.
- **Read:** [the 7 Nov 2026 post](https://pluralistic.net/2026/11/07/aeiou-but-sometimes-why/).

### (b) Public-domain authors

These rules apply to every author in this group:
- Counts are `wc -w` on Project Gutenberg (PG) text between the START and END markers. They include prefaces, notes and indexes, so they run 5-15% high (estimate).
- PG's website is for human users. Bulk pulls should come from mirrors or the offline catalogue, or from filtering `sedthh/gutenberg_english` by PG ID ([PG robot policy](https://www.gutenberg.org/policy/robot_access.html)).
- Standard Ebooks texts are cleaner where they exist.
- Style metrics were computed in the notes on the PG texts.

#### Arnold Bennett (31): public-domain fallback
- **Corpus:** **~303k words** across 12 PG titles (measured). The self-help subset is ~118k (measured). PD in the US (all pre-1931) and in the UK/EU since 1 Jan 2002.
- **Markers:**
  - Measured on the self-help subset: "you" 20.1 per 1k words, the highest of any PD candidate; mean sentence 20.7 words; 4.7 semicolons per 1k; 0.66 archaic words per 1k.
  - From reading: short chapters, each one practical argument; ironic asides about "the average man" and his commute; concrete schedules, such as the 90-minute evening.
- **Best for:** how-tos, advice memos, habit and process docs.
- **Risks:** Edwardian diction and references. The 303k mixes literary criticism (*Books and Persons*, 62.9k) and travel writing (*Your United States*, 46.9k) in with the self-help. The self-help alone only just clears the 100k minimum.
- **Read:** [How to Live on 24 Hours a Day](https://www.gutenberg.org/ebooks/2274); [The Human Machine](https://www.gutenberg.org/ebooks/12811).

#### Bertrand Russell (31): US only
- **Corpus:** **~467k words** over 9 pre-1931 titles (measured). The four popular titles total 218,021 (measured).
- **Jurisdiction:**
  - US: pre-1931 works are PD. *The Conquest of Happiness* entered the PD on 1 Jan 2026, and PG posted it on 9 Feb 2026.
  - UK/EU: protected until 1 Jan 2041.
  - The shorter-term rule does not help: he is a UK national and the works are UK-origin.
- **Markers:**
  - Measured: mean sentence 25.5; 0.32 archaic words per 1k.
  - From reading: lucid step-by-step argument; everyday-object examples (the table in *Problems of Philosophy*); dry irony; hypotheticals.
- **Best for:** explainers of abstract ideas, decision memos, analyses.
- **Risks:** protected outside the US until 2041. Drop the political titles (*Proposed Roads to Freedom*, *Political Ideals*). Less storytelling than Bennett.
- **Read:** [The Problems of Philosophy](https://www.gutenberg.org/ebooks/5827); [The Conquest of Happiness](https://www.gutenberg.org/ebooks/77894).

#### Edwin E. Slosson (30)
- **Corpus:** **~118k words** (measured): *Creative Chemistry* 88.0k and *Easy Lessons in Einstein* 29.5k. More of his books are on Internet Archive, unmeasured. PD everywhere (he died in 1929).
- **Markers:**
  - Measured: the lowest archaism (0.07 per 1k) and semicolon rate (1.5 per 1k) of any PD candidate; mean sentence 24.9.
  - From reading: journalistic ledes; industrial anecdotes; science explained through analogy; enthusiasm about technology.
- **Best for:** science and technology explainers.
- **Risks:** only just over the 100k minimum; 1919-era chemistry and industry topics.
- **Read:** [Creative Chemistry](https://www.gutenberg.org/ebooks/17149); [Easy Lessons in Einstein](https://www.gutenberg.org/ebooks/75807).

#### H. L. Mencken (29): US, probably UK/EU
- **Corpus:** **~562k words** (measured): *Prejudices* 1-5, *A Book of Prefaces*, *Notes on Democracy* and *The American Language*.
- **Jurisdiction:**
  - US: pre-1931 works are PD.
  - UK/EU: life+70 ends on 1 Jan 2027. The rule of the shorter term probably frees his US-origin works already.
  - Some EU states may not apply that rule to US works. This is unverified; get a legal check before relying on it there.
- **Markers:**
  - Measured: "you" 1.5 per 1k; mean sentence 23.9.
  - From reading: invective and mock-solemnity; catalogues of examples; Latinate words mixed with slang.
- **Best for:** opinion pieces and critique, if you want bite.
- **Risks:** the abrasive, polemical tone will leak into memos; political content.
- **Read:** [Prejudices, First Series](https://www.gutenberg.org/ebooks/53538).

#### Hendrik Willem van Loon (28)
- **Corpus:** **~268k words** (measured): *The Story of Mankind* 129.2k, *Tolerance* 112.1k, *Ancient Man* 26.9k. PD in the US (1920-25 works) and in the UK/EU since 1 Jan 2015.
- **Markers:**
  - Measured: 0.5 semicolons per 1k; "you" 1.5 per 1k; mean sentence 24.2.
  - From reading: a chatty narrator who comments on the story and talks to the reader; homely, anachronistic analogies; simple vocabulary; chapters that end on a moral or a hook.
- **Best for:** narrative explainers and "history of X" sections.
- **Risks:** 1920s cultural and racial attitudes need filtering; history topic gravity; too little second person for how-tos.
- **Read:** [The Story of Mankind](https://www.gutenberg.org/ebooks/754).

#### Emily Post (27): US, probably UK/EU
- **Corpus:** *Etiquette* (1922), **205.2k words** (measured).
- **Jurisdiction:** PD in the US. Probably PD in the UK/EU through the shorter-term rule. A strict life+70 reading runs to 1 Jan 2031.
- **Markers:**
  - Measured: 0.04 archaic words per 1k, the lowest of any candidate; "you" 11.4 per 1k.
  - From reading: prescriptive rules framed as social consequences; recurring fictional households as worked examples; nested sections and sub-rules.
- **Best for:** policy docs and rule-plus-example how-tos.
- **Risks:** one book on one topic; dated content.
- **Read:** [Etiquette](https://www.gutenberg.org/ebooks/14314).

#### Mark Twain, nonfiction (27)
- **Corpus:** **~1.04M words** over 8 titles (measured). PD everywhere.
  - Avoid the Mark Twain Project (UC Berkeley) edition, which claims copyright until 2047.
  - Standard Ebooks uses the 1924 Paine *Autobiography* instead.
- **Markers:**
  - Measured: "I" 14.2 per 1k; 10.3 semicolons per 1k; mean sentence 25.2.
  - From reading: deadpan exaggeration; dialect dialogue; digressions that mix statistics with tall tales.
- **Best for:** anecdote-led openings and speeches.
- **Risks:** a 19th-century register and attitudes; dialect; weak transfer to docs.
- **Read:** [Life on the Mississippi](https://www.gutenberg.org/ebooks/245); [How to Tell a Story](https://www.gutenberg.org/ebooks/3250).

#### T. H. Huxley (27)
- **Corpus:** **~903k words raw** over 8 collections (measured). The collections overlap, so dedupe them. PD everywhere.
- **Markers:**
  - Measured: mean sentence 38.4 (median 33); 10.0 semicolons per 1k.
  - From reading: analogies built on everyday objects (the notes cite "On a Piece of Chalk"); "lay sermon" polemic.
- **Best for:** science explainers for lay readers, if you can accept a Victorian cadence.
- **Risks:** the most dated syntax on the shortlist. The output would need sentence splitting to read as modern.
- **Read:** [Lay Sermons, Addresses and Reviews](https://www.gutenberg.org/ebooks/16729).

### (c) Copyrighted modern tech and product writers

Everyone here is all rights reserved or makes no statement. Using them rests on fair use for a private, undistributed fine-tune (Section 5). Check each site's robots.txt, `tdm-reservation` header and any written notice before the first fetch.

#### Patrick McKenzie (34): recommended
- **Corpus:**
  - [kalzumeus.com/archive](https://www.kalzumeus.com/archive/): 571 posts, 2006-06-27 to 2025-02-10, **~1.17M words** (estimated: 30-post sample, mean 2,044, median 665). A few 10k+ essays skew the mean.
  - [bitsaboutmoney.com](https://www.bitsaboutmoney.com/): 63 essays, **~191k** (estimated: 20-post sample, mean 3,031). A second 8-post sample gave ~210k.
  - Combined: ~1.36M (estimate), but most of it is unusable. Full crawl 2026-11-08 (body text, block quotes excluded):
    - Kalzumeus 2011+: 67 posts, 454k words. 19 are podcast or talk transcripts (256k, multi-speaker, spoken): exclude. Written essays: 48 posts, **198k**.
    - Kalzumeus 2006-2010: 504 of 571 posts. Every-8th-post sample: 57.5k words in 63 posts, so **~460k** (estimate). MicroISV era; excluded by default.
    - Bits about Money: 63 essays, 2021-2026, **261k** (measured; includes a short support blurb per issue).
    - Usable written essays 2011+: **~460k**. Cross-post 10-gram reuse 1.7%.
- **Licence and signals:**
  - "© Patrick McKenzie (Kalzumeus Software, LLC) 2006 - 2026". No licence.
  - robots.txt (checked 2026-11-07): kalzumeus.com restricts nothing; its 2025 comment welcomes AI crawlers ("enjoy a special sort of welcome!"). bitsaboutmoney.com disallows only Ghost admin paths; no AI-bot rules.
  - Not checked: whether Bits about Money has paywalled essays.
  - Bits about Money serves `sitemap-posts.xml`, which is a Ghost convention (my inference). If Ghost(Pro) hosts it, Ghost's terms bar crawlers ([Ghost terms](https://ghost.org/terms/)).
- **Markers:** very long, digressive sentences carried by parentheticals; insider detail; dry wit; footnotes; "financial plumbing" explainers of how systems actually run.
- **Best for:** explainers of how a system works, analyses, strategy and incident memos.
- **Risks:**
  - Era drift: the 2006-10 microISV diary reads differently from the later finance and infrastructure essays. Apply a date cut and re-measure; the notes give no per-year split.
  - Long sentences can bloat short memos. The plan's length tag controls this.
  - Finance vocabulary gravity.
- **Read:** the [Bits about Money index](https://www.bitsaboutmoney.com/) ("You can read all 63 essays here") and the [Kalzumeus archive](https://www.kalzumeus.com/archive/). The only essay the notes name is his first post, "So you want to be a microISV" (2006), which predates his mature voice.

#### Paul Graham (33)
- **Corpus:** [paulgraham.com/articles.html](https://paulgraham.com/articles.html): 236 essays, **~573k words** (measured, full crawl; mean 2,427, median 1,530). An independent count gives 562,990 words for 229 essays.
- **Licence:** "© mmxxvi pg"; no licence. His robots.txt has no AI-bot rules. Hugging Face copies tagged MIT or Apache carry licences their uploaders had no right to grant.
- **Markers:** short declarative sentences; plain Anglo-Saxon words; a surprising claim argued through everyday analogies; frequent "you"; few headers; a closing "Notes" section and a thanks line.
- **Best for:** argument essays and persuasive memos.
- **Risks:**
  - The most scraped author in the notes: 15+ HF datasets and a 990-star GitHub export ([ofou/graham-essays](https://github.com/ofou/graham-essays)).
  - Prompt-only imitation is a product category, so the prompt-only baseline is strong and a fine-tune adds the least.
  - The highest memorization risk on the shortlist.
  - Weak for step-by-step docs.
- **Read:** [the essay index](https://paulgraham.com/articles.html).

#### Joel Spolsky (32)
- **Corpus:**
  - [joelonsoftware.com/archives](https://www.joelonsoftware.com/archives/): 1,114 posts, Dec 1999 to Dec 2022 (self-reported). Most of the output is 2001-2009.
  - Unmeasured: the WordPress API returned 403 and the sitemap returned 429.
  - A third-party scrape holds 209 pieces and 123,984 words. Guess for the full archive: 0.7-1.3M.
- **Licence and signals:** no copyright or licence statement. Treat the 403/429 responses as a bot block. Either fetch slowly at browser pace or skip.
- **Markers:** funny anecdotes; strong opinions; second person; numbered tests and lists; cartoonish analogies; management narratives.
- **Best for:** product and management memos, specs, hiring and process docs. His topics are the closest match to a PM's.
- **Risks:** hard to acquire; dated 2000s technology references; a partial copy sits in the yoonholee set.
- **Read:** [the archive](https://www.joelonsoftware.com/archives/) (the notes name no single post).

#### Julia Evans (32): best how-to and docs voice
- **Corpus:** [jvns.ca](https://jvns.ca/): 603 posts, 2013-02-24 to 2026-09-27, **~627k words** (estimated: 40-post sample, mean 1,040, median 928).
- **Licence:** "© Julia Evans"; no licence. robots.txt (checked 2026-11-08) opens with a "NO LLM PLZ" banner and disallows GPTBot and Google-Extended. That is an explicit AI opt-out: permission only, like Dynomight. Her Legal score should drop to 1.
- **Markers:** short sentences; first person with open enthusiasm ("I learned…"); questions; numbered steps; friendly second person; tiny worked examples.
- **Best for:** how-tos, docs, onboarding guides, technical explainers.
- **Risks:** her 2013 daily notes differ from her later explainers, so apply a date filter. Topic gravity toward Linux and networking. Storytelling is light.
- **Read:** [jvns.ca](https://jvns.ca/) (the notes name no single post).

#### Jeff Atwood, Coding Horror (31)
- **Corpus:** 1,438 posts, 2004 to the 2020s, **~1.55M words** (estimated: 40-post sample, mean 1,080, range 320-3,220).
- **Licence:** no site-wide licence found. robots.txt not checked. The sitemap is Ghost-style ([sitemap](https://blog.codinghorror.com/sitemap-posts.xml)).
- **Markers:** punchy; humorous; quotes; pop culture; strong opinions.
- **Best for:** developer explainers and opinion posts.
- **Risks:** heavy quotation; dated developer culture.
- **Read:** [blog.codinghorror.com](https://blog.codinghorror.com/) (the notes name no single post).

#### Dan Luu (31)
- **Corpus:** [danluu.com](https://danluu.com/): 122 posts, **~687k words** (measured, full crawl; mean 5,635, median 4,155). The count includes code, footnotes and quotes, so prose alone is 5-20% lower (guess).
- **Licence:** no copyright or licence text found.
- **Markers:** long, data-heavy essays; lists of examples; footnotes and appendices; deadpan; contrarian empiricism.
- **Best for:** evidence-heavy analyses and postmortems.
- **Risks:** posts run far longer than memos; some posts quote others heavily.
- **Read:** [danluu.com](https://danluu.com/).

#### Charity Majors (31)
- **Corpus:** charity.wtf now serves a Substack: 130 posts, 2015-12-27 to 2026-10-08, **236,250 words** (measured), all free, all under her byline.
- **Licence and signals:** no licence. Substack's terms bar crawling and storing "any significant portion" of content ([Substack ToS](https://substack.com/tos)). Accumulate the RSS feed (20 posts) or ask her for an export.
- **Markers:** profane, energetic, opinionated; engineering management and observability; lists.
- **Best for:** opinionated engineering-management memos.
- **Risks:** profanity; observability topic gravity; the corpus gets thin after filtering.
- **Read:** [charity.wtf](https://charity.wtf/).

#### Steven Sinofsky, Hardcore Software (30)
- **Corpus:** 165 posts, 2021-01-28 to 2026-09-29, **709,906 words** (measured), all free, one byline.
- **Licence:** Substack terms apply (see Charity Majors).
- **Markers:** insider memoir; product lessons; long first-person narrative.
- **Best for:** product strategy memos told through history; launch retrospectives.
- **Risks:** Microsoft-history topic lock; Substack terms; the notes rate his distance from LLM voice only medium-high.
- **Read:** [hardcoresoftware.learningbyshipping.com](https://hardcoresoftware.learningbyshipping.com/).

#### Maciej Cegłowski (30)
- **Corpus:** the index pages list 16 talks (~87k) and 13 essays, **~131k measured** in total. The yoonholee set counts 353 pieces and 524,614 words, so the full archive is larger.
- **Licence:** no statement.
- **Markers:** sardonic aphorisms; vivid analogies; literary cadence; talk-transcript structure.
- **Best for:** persuasive talks and essays; critiques of tech.
- **Risks:** he has written little since about 2019; the talk format; a tech-critique slant.
- **Read:** "Website Obesity", "Haunted by Data" and "Build a Better Monster" on the [talks index](https://idlewords.com/talks/); "Artemis II is not safe to fly" (Mar 2026) on [idlewords.com](https://idlewords.com/).

#### Simon Willison (29)
- **Corpus:** his public [Datasette](https://datasette.simonwillison.net/simonwillisonblog).
  - `blog_entry`: 3,344 rows, **~1.43M** whitespace tokens of HTML (measured by SQL, so slightly inflated).
  - Long-form output: 76k-203k words a year over 2020-2025.
  - Link-post commentary: another ~572k.
  - The `blog_quotation` table (1,480 rows) holds other people's words; exclude it.
- **Licence:** © only. The blog's code is Apache-2.0, which covers the code and not the prose. His robots.txt explicitly allows ChatGPT-User. He publishes the database himself, which makes this the politest acquisition path in the library.
- **Markers:** plain and conversational; "Here's how I…"; heavy quoting and linking; code snippets; TIL notes; caveats.
- **Best for:** AI-tooling write-ups and technical how-tos.
- **Risks:** since 2023 his posts contain quoted LLM output; medium distance from LLM voice; two eras.
- **Read:** [simonwillison.net](https://simonwillison.net/).

### (d) Copyrighted modern science, business and history writers

#### Morgan Housel (34): best memo voice
- **Corpus:** [collabfund.com/blog/authors/morgan](https://collabfund.com/blog/authors/morgan/): 348 posts, Sep 2016 to Apr 2026, **~340k words** (estimated: 14-post sample, mean 972, median 985; ±30%).
  - Full crawl 2026-11-08: 351 posts, **342k words** of his own text, plus 34.5k words of block quotes (9.2%). Median 806 words. 4 posts are near-empty. Cross-post 10-gram reuse 6.4%; 12 posts share over 30% with another post (reposts and book excerpts).
  - Output fell after 2023: 17 posts in 2024, 11 in 2025, 2 in 2026.
  - His earlier Motley Fool and WSJ columns are publisher-edited and were not checked.
- **Licence:** none on the blog index. A /terms-of-use page exists (not read). No AI-bot blocks.
- **Markers:** short declarative sentences; one-line paragraphs; a historical anecdote, then a single principle, then "the point is…"; aphorisms.
- **Best for:** memos, team updates, decision write-ups, short essays.
- **Risks:** his cadence is widely imitated, including by LLMs, so the adapter may add little over the prompt-only baseline. Light on mechanism. The size estimate rests on 14 posts.
- **Read:** [author page](https://collabfund.com/blog/authors/morgan/).

#### Dynomight (33): permission only
- **Corpus:** 211 posts, 2021-05-11 to 2026-10-28, all free, **395,860 words** (measured). Drop the 3 link posts (5,452 words).
- **Licence and signals:** no licence. The Substack mirror's robots.txt names AI crawlers, which is the author's opt-out ([Substack robots](https://dynomight.substack.com/robots.txt)); dynomight.net does not. Treat it as a no unless the author agrees in writing.
- **Markers:**
  - Measured on 30 posts: the shortest sentences of the science group (17.3 words); 11.5% questions, the highest; "you" 19.6 per 1k; 10 parentheses per 1k.
  - From reading: bulleted reasoning; explicit uncertainty; playful headers; self-mockery.
- **Best for:** decision analyses, explainers, evidence reviews.
- **Risks:** the opt-out. It also has a unique strength: "All words are written by me (a human)", the only human-authorship guarantee in the library ([AI usage](https://dynomight.net/ai/)).
- **Read:** [dynomight.net/about](https://dynomight.net/about/) and the [Substack archive](https://dynomight.substack.com/).

#### Scott Alexander (32)
- **Corpus:**
  - SSC: 1,241 posts, 2013-2021, **~2.68M words** (estimated: 241-post WordPress sample, mean 2,161; 11% of words are in blockquotes).
  - ACX: **1,796,898 words** in 589 essays (measured) after dropping guest book reviews, comment highlights, open threads, link posts and contests by title.
  - Use SSC. It is a frozen WordPress archive, it clears the threshold on its own, and it avoids Substack's terms.
- **Licence:** none stated. ACX's robots.txt has no AI blocks.
- **Markers:**
  - Measured on 30 SSC posts: mean sentence 20.5; 7.2% questions; "you" 12.6 and "I" 11.7 per 1k; 64-word paragraphs.
  - From reading: Roman-numeral sections; steelman, then rebut; deadpan humour; invented dialogues and parables.
  - His own list of techniques: the concrete example before the principle, concept handles, defusing counterarguments in advance ([Nonfiction Writing Advice](https://slatestarcodex.com/2016/02/20/writing-advice/)).
- **Best for:** argued analyses; explainers of contested questions.
- **Risks:**
  - Culture-war and psychiatry-policy posts need filtering.
  - Guest content.
  - He is famous: he appears in the yoonholee set and has an HF set of his ACX posts. Expect a strong prompt-only baseline and a higher recall risk.
  - Long pieces.
- **Read:** [Nonfiction Writing Advice](https://slatestarcodex.com/2016/02/20/writing-advice/) (2016), which is also his style manual.

#### Cal Newport (32)
- **Corpus:** 1,130 posts, Jul 2007 to Oct 2026, **~680k words** (estimated: WordPress, mean 601).
- **Licence:** "Copyright © 2026 Cal Newport, All rights reserved." No AI-bot blocks.
- **Markers:**
  - Measured: mean sentence 23.8; "you" 13.9 per 1k; 38-word paragraphs.
  - From reading: the thesis up front; named concepts ("deep work", "slow productivity"); an anecdote, then a numbered rule.
- **Best for:** memos that propose a practice; process docs.
- **Risks:** his named concepts will leak into outputs; the 2007-2012 student-advice era; productivity topic gravity.
- **Read:** [calnewport.com/blog](https://calnewport.com/blog/).

#### Adam Mastroianni, Experimental History (31)
- **Corpus:** 116 free posts, **322,615 words** (measured); 27 paid posts excluded.
- **Licence:** Substack terms apply. No AI-bot block on experimental-history.com.
- **Markers:**
  - Measured: mean sentence 22.5; "you" 17.4 per 1k; 8.3% questions.
  - From reading: jokey section headers; absurd analogies; first-person lab anecdotes; a mock-grandiose tone.
- **Best for:** punchy explainers; essays that challenge the status quo.
- **Risks:** the humour is too strong for formal docs; academia topic gravity.
- **Read:** [experimental-history.com](https://www.experimental-history.com).

#### Howard Marks, Oaktree memos (30)
- **Corpus:** 166 memos, 1990-2026, **~0.85-0.95M words** (estimated: 8-memo sample at ~5,800 words per page, navigation included; ±30%).
- **Licence:** "© 2007- Oaktree Capital Management, L.P. All rights reserved." No AI-bot blocks.
- **Markers:** literal memos to clients; reflective; anecdotal; principle-driven; one voice across 36 years.
- **Best for:** long stakeholder memos and letters.
- **Risks:** bound to finance; these are corporate documents, and some are co-signed; the memos are long.
- **Read:** [the memo index](https://www.oaktreecapital.com/insights/memos).

#### Aswath Damodaran, Musings on Markets (30)
- **Corpus:** 686 posts, 2008-2026, **~1.56M words** (estimated: 247-post Blogger sample, mean 2,271). Every sampled post is his, and almost none of the text is in blockquotes.
- **Licence:** none found. No AI-bot blocks.
- **Markers:**
  - Measured: "you" 11.4 per 1k.
  - From reading: teacherly step-by-step walk-throughs; data tables; "story and numbers" framing.
- **Best for:** analytical how-tos and model walk-throughs.
- **Risks:** valuation vocabulary lock-in; tables need stripping. His Blogger HTML uses line breaks instead of paragraph tags, which inflates the sentence metrics.
- **Read:** [aswathdamodaran.blogspot.com](https://aswathdamodaran.blogspot.com).

#### Bret Devereaux, ACOUP (30)
- **Corpus:** 400 posts, 2019-2026, **~2.1M words** (estimated: 250-post WordPress sample, mean 5,291). Only 2% of the text is in blockquotes.
- **Licence:** no copyright, licence or AI statement. No AI-bot blocks.
- **Markers:**
  - Measured: mean sentence 35.0, the longest measured; 6.7 footnotes per post; 12.5 parentheses per 1k; 114-word paragraphs.
  - From reading: multi-part series; pop-culture hooks used to teach real history.
- **Best for:** long explainers that correct a popular misconception.
- **Risks:** Roman and military vocabulary will bleed into outputs; posts are far too long for memos.
- **Read:** [acoup.blog](https://acoup.blog) and its [About page](https://acoup.blog/about-the-pedant/).

### (e) House styles: the plain-language fallback

#### GOV.UK (29)
- **Corpus:** GOV.UK guidance, unmeasured. The style guide now lives at guidance.publishing.service.gov.uk.
- **Licence:** Open Government Licence v3.0 unless stated otherwise; Crown copyright; attribution required.
- **Markers:**
  - Plain English is mandatory ("use", not "utilise").
  - "and", never "&".
  - Numerals for all numbers, including 2-9.
  - No negative contractions.
  - Sentence case everywhere.
  - A lead-in line before every bullet list.
- **Best for:** procedures, policy docs, how-tos.
- **Risks:** no storytelling; many authors; government topics.
- **Read:** [A to Z style guide](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/).

#### 18F (29)
- **Corpus:** the content guide, guides, methods and blog source on GitHub; unmeasured.
  - GSA eliminated 18F around 1 Mar 2025 and the site went offline ([CBS News](https://www.cbsnews.com/amp/news/general-services-administration-shutters-technology-unit-trump-doge)).
  - The repos are still public. The site repo was last pushed on 4 Jul 2026.
- **Licence:** US public domain plus a worldwide CC0 waiver ([LICENSE](https://github.com/18F/content-guide/blob/main/LICENSE.md)).
- **Markers:** plain, friendly, modern. The blog adds case-study narrative.
- **Best for:** product, research and process docs. Government digital services sit close to PM work.
- **Risks:** a multi-author blog; small or unknown size; no single voice.
- **Read:** [18F/content-guide](https://github.com/18F/content-guide); [18F/18f.gsa.gov](https://github.com/18F/18f.gsa.gov).

#### Our World in Data (26)
- **Corpus:** unmeasured; written and edited by a team.
- **Licence:** CC BY 4.0 for writing and charts ([about](https://ourworldindata.org/about)).
- **Markers:** calm, data-first explainers built around charts.
- **Best for:** data explainers.
- **Risks:** the notes rate its house style close to LLM-neutral; no single voice.
- **Read:** [ourworldindata.org/about](https://ourworldindata.org/about).

The notes also suggest a two-layer mix:
1. A modern plain-language base for form (18F plus GOV.UK).
2. One public-domain author for flair (Bennett or van Loon).

This breaks the single-author brief and is untested.

## 4. Excluded and why

| Option | Why out |
|---|---|
| Noah Smith | High political bleed (US politics, China, industrial policy). His old blog has 16% blockquotes and posts credited to "Unknown" or "Anonymous". |
| Freddie deBoer | Political and cultural polemic; his Substack opts out of AI crawlers. |
| Bryan Caplan | High political bleed; short posts (mean 468). |
| Tanner Greer | Geopolitics; 27% of words sit in blockquotes. |
| Derek Thompson | Politics mixed in; only 184k free words; ~44% of words paywalled. |
| Robin Hanson | Multi-author before 2009; medium politics; short posts. |
| Ted Gioia | robots.txt blocks AI crawlers; music topic. |
| Matt Levine | Paywalled. Only unofficial scrapes exist. |
| Tyler Cowen (Marginal Revolution) | Co-written; blocked by Cloudflare; short, quote-heavy posts. |
| Derek Lowe | Publisher-hosted (AAAS); returned 403; unmeasured. |
| Ben Thompson | His best material is paywalled; returned 403/429; unmeasured. |
| Byrne Hobart | Unmeasured; partly paywalled. |
| Packy McCormick | ~20% of posts carry other bylines; sponsor blocks; hype register. |
| Ethan Mollick | Posts embed AI-generated examples; topic locked to AI. |
| Lilian Weng, Will Larson, Eugene Yan, Eli Bendersky, Brian Potter, Jason Crawford, Sean Carroll, John D. Cook, Hannah Ritchie | Near-neutral voices. A fine-tune would teach topic and structure, and little voice. |
| Casey Handmer | Space and energy topic gravity; licence unchecked (the homepage blocked the fetcher). |
| Sarah Constantin | Citation-dense literature reviews; biotech topic gravity. |
| Dan Davies | 254k words; UK politics; Substack terms. |
| Hillel Wayne | Formal-methods niche; split across a site (~70k) and a newsletter (~434k). |
| Tim Urban | Part of the voice lives in the drawings; median post 668 words. |
| Randall Munroe (What If) | ~155k; the comics' CC BY-NC licence is not clearly extended to the text. |
| Slime Mold Time Mold | Written by a group of three. |
| Henrik Karlsson, Kyla Scanlon, Nadia Asparouhova | Under 200k free words (158k, 163k, ~120k). |
| Terence Tao | Research mathematics. |
| Sabine Hossenfelder | No reliable word estimate; recent posts are video companions. |
| Ed Yong | Magazine-edited; blog defunct; paywalled. |
| Feynman Lectures | Rights holders bar download; edited transcripts. |
| Andrej Karpathy, Chris Olah | Too small (~100-130k with code; ~51k). |
| Distill | Multi-author; on hiatus. |
| Bret Victor | Interactive pages; median 1,194 words. |
| DHH, Jason Fried | Short posts (mean 582 and 261 words); totals unknown; Signal v. Noise was multi-author. |
| Steve Yegge | Rambling rants spread over three or more platforms. |
| Derek Sivers | Minimalist aphorisms rather than informational prose. |
| Rands in Repose | CC BY-NC-ND (the no-derivatives term is a problem); size unmeasured. |
| Jay Alammar, Michael Nielsen | Non-commercial licences; unmeasured or a single textbook. |
| Martin Fowler | Site mixes in colleagues' articles; unmeasured. |
| Avery Pennarun | No archive index; unmeasured. |
| Warren Buffett letters | The HF copy is Q&A pairs; the raw letters were not measured. |
| George Orwell | Almost nothing is US-PD before 2027. |
| Aldous Huxley | Protected in the UK/EU until 2034; small. |
| G. K. Chesterton | Paradox-driven; poor for memos; only pre-1931 works are US-PD. |
| Stevenson, Franklin, Thoreau, Emerson, Montaigne | Ornate or archaic (Montaigne's mean sentence is 52.2 words; Emerson uses 2.61 archaic words per 1k). |
| Darwin, Muir, Tyndall, Burroughs, Jefferies | Descriptive nature and travel writing. |
| Michael Faraday | ~99k, under the minimum. |
| William James | Only *Talks to Teachers* transfers; 0.72 archaic words per 1k. |
| H. G. Wells | Impersonal ("you" 0.2 per 1k). The *Outline* editors' notes may be protected in the UK/EU until 2031. |
| Jeans, Eddington | 107k and ≥38k; impersonal. |
| Strunk | 13.9k words. |
| Esenwein and Carnegie | Co-authored. |
| Pooled outdoor how-to (S. E. White, Beard, Kephart, Nessmuk) | Pooling breaks single-author consistency. |
| Will Durant | Unmeasured; UK/EU status uncertain. |
| OpenStax | Most titles are now CC BY-NC-SA; multi-author. |
| Write the Docs | CC BY-NC-SA. |
| Wikipedia, Wikibooks | Multi-author; unclear whether ShareAlike reaches model weights. |
| Python and Django docs | Multi-author reference prose. |
| *Producing Open Source Software*, *Dive Into Python 3* | Single CC BY-SA books; unmeasured. |

## 5. Legal and ethics summary

As of 7 Nov 2026. Not legal advice. Most sources are law-firm alerts and news reports, so check the opinions themselves before relying on a quote.

**US courts have not ruled on your case.** No US court has ruled on a private, non-commercial, single-author fine-tune.
- **Bartz v. Anthropic (23 Jun 2025):** training was fair use, "transformative—spectacularly so". Building a library from pirated books was not excused. The $1.5B settlement was approved on 20 Jul 2026, and its release excludes claims about outputs ([Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026); [JURIST](https://www.jurist.org/news/2026/07/judge-approves-record-1-5-billion-settlement-involving-anthropic/)).
- **Kadrey v. Meta (25 Jun 2025):** Meta won on that record. The judge added that "market dilution" will often decide the market-effect factor for plaintiffs ([Authors Alliance](https://www.authorsalliance.org/2025/06/26/meta-wins-on-fair-use-for-now-but-court-leaves-door-open-for-market-dilution/)).
- **Thomson Reuters v. Ross (3d Cir., 29 Sep 2026):** the AI developer lost. The product was commercial, non-generative and competing, and the court left the generative-AI question open ([Ballard Spahr](https://www.ballardspahr.com/insights/alerts-and-articles/2026/10/third-circuit-addresses-fair-use-in-ai-training-but-leaves-generative-ai-questions-unresolved)).
- **The Copyright Office (May 2025)** warned that "stylistic imitation made possible by its use in training may impact the creator's market" ([Sidley](https://datamatters.sidley.com/2025/05/28/generative-ai-meets-copyright-scrutiny-highlights-from-the-copyright-offices-part-iii-report/)).
- **Chakrabarty, Ginsburg and Dhillon** argue that author-specific fine-tunes "should not be fair use" ([arXiv:2510.13939](https://arxiv.org/html/2510.13939v4)).

**What it means for each stage of this build.**

| Stage | Exposure | Do |
|---|---|---|
| Storing | Low if you fetch the author's own free pages | Keep the copy narrow and private; delete it if the author objects. Never use paywalled posts through a shared login or book PDFs from shadow libraries: that is the losing branch of Bartz. |
| Training | Favourable on purpose (private, non-commercial, transformative). Weaker on market effect, because imitating one named author is exactly what dilution theory targets. | Keep the corpus, adapters and merged weights off the internet. Market harm is hard to show while outputs stay private. |
| Outputs | The clearest exposure. A verbatim span is copying, and every authority treats outputs separately. | Apply the overlap filter in Section 6 before any text leaves the Mac, and more strictly for anything you publish. |

**EU and UK.**
- **EU:** Article 4 of the DSM Directive allows text and data mining unless rights are reserved "in an appropriate manner, such as machine-readable means" ([EUR-Lex](https://eur-lex.europa.eu/eli/dir/2019/790/oj)).
- **GEMA v OpenAI (Munich, 11 Nov 2025):** song lyrics the model had memorized and could reproduce counted as reproductions outside that exception ([Härting](https://haerting.de/en/insights/gema-wins-against-openai-strengthening-copyright-in-the-age-of-ai/)).
- **EU AI Act:** a personal LoRA that is never distributed is not "placed on the market".
- **UK:** there is no commercial TDM exception, and the government shelved its opt-out plan on 18 Mar 2026 ([Osborne Clarke](https://www.osborneclarke.com/insights/opted-out-uk-government-moves-away-preferred-position-ai-and-copyright-following-report)). Getty v Stability (4 Nov 2025) held that model weights are not an "infringing copy"; that is on appeal. On paper the UK is the strictest of the three.

**Opt-outs and platform terms.**
- **Treat any reservation as a no:** a robots.txt AI-bot block, a `tdm-reservation` header or file, a platform AI-block toggle, or a written notice.
- **Substack** (terms updated 6 Oct 2026) bars crawling and storing "any significant portion" of content ([Substack ToS](https://substack.com/tos)). Use RSS or ask the writer for an export.
- **Medium** defaults to no.
- **Meta v. Bright Data** weakens browsewrap terms against logged-out visitors. That is a defence in litigation. It grants no permission.

**Names and passing off.**
- Style is not copyrightable ([17 U.S.C. §102(b)](https://www.law.cornell.edu/uscode/text/17/102)). The Copyright Office declined to recommend a style right in 2024.
- The real risks are passing off and publicity claims. Grammarly's "Expert Review" put real writers' names on AI edits, and Julia Angwin filed a class action on 11 Mar 2026 ([Nieman Lab](https://www.niemanlab.org/2026/03/journalist-julia-angwin-files-class-action-lawsuit-over-grammarlys-ai-sloppelgangers/)).
- Never put the author's name on outputs, adapters, files or tools you share. Never present an output as theirs. Disclose AI help in anything you publish.

**Authors Guild and the labs.**
- The Guild's 2026 best practices say writers should not use AI to "copy or mimic the unique styles, voices, or other distinctive attributes" of other writers. It calls them "guidelines, not rules", and it does not oppose authors tuning models on their own work ([Authors Guild](https://authorsguild.org/resource/ai-best-practices-for-authors/)).
- The notes' ethical default:
  - Prefer an author who invited training.
  - Ask when the author is reachable.
  - Keep it personal.
  - Delete the corpus on objection.
- A small July 2026 audit found that ChatGPT refuses named-author style requests and Claude complies with caveats ([TNW](https://thenextweb.com/news/chatgpt-refuses-author-style-imitation-copyright)).

**Memorization.**
- **Chakrabarty et al.:** fine-tuned GPT-4o beat expert human imitators on style (odds ratio 8.16 with MFA-trained readers). Detectors flagged almost none of it: Pangram caught 3% and GPTZero 0%. ROUGE-L against the originals was 0.16-0.23, and outputs that regurgitated text were resampled ([arXiv](https://arxiv.org/html/2510.13939v4)).
- **"Alignment Whack-a-Mole":** GPT-4o, Gemini-2.5-Pro and DeepSeek-V3.1 were fine-tuned to expand plot summaries into full text ([arXiv](https://arxiv.org/pdf/2603.20957v2)).
  - The models then reproduced up to 85-90% of held-out books, with single verbatim spans over 460 words.
  - Training on Murakami alone unlocked recall for more than 30 unrelated authors.
  - Public-domain and random-author training data did the same. Synthetic text gave near-zero extraction.
- **The lesson:** the training format and the use of real human text drive the risk, more than the choice of author. A public-domain author does not make a summary-to-text tune safe. The mitigations are in Section 6.

## 6. What changes in the build plan

Phase 0, the audit:
- Replace the Gmail and Drive audit with a source audit.
- List posts from the archive page, sitemap, WordPress REST API or Blogger feed.
- Before the first content fetch, record robots.txt, `tdmrep.json`, the `tdm-reservation` header, any platform AI toggle and any written notice. Any reservation stops collection.
- Pick the author after the taste check (Section 7), then freeze the choice.

Phase 1, acquisition and cleaning:
- **Fetch politely:** one request every 2-5 s; a descriptive User-Agent with a contact email; honour robots.txt; cache the raw HTML once and never re-fetch.
- **Substack:** accumulate the RSS feed or ask the author for an export. Never page through `/api/v1/archive`.
- **Project Gutenberg:** use mirrors or the offline catalogue, never the website in bulk.
- **Extract** with trafilatura: `include_comments=False, include_tables=False, include_images=False, include_links=False, favor_precision=True, with_metadata=True`, XML output. Check on 20 posts how it tags quotes and code; the notes did not verify this.
- **Strip** block quotes, code (replace with a placeholder), captions, embedded tweets, newsletter chrome, sponsor reads and footnote numerals. Decide by taste whether footnote text stays as endnotes; footnote voice is often authorial.
- **Drop** guest posts and co-bylines (by byline field or author page), link roundups, comment highlights, podcast posts and open threads. Apply a date cut for drift (McKenzie's microISV era, Evans' 2013 notes).
- **Dedupe** with MinHash across cross-posts, reposts and quoted excerpts. Dedupe overlapping Gutenberg collections (Huxley, Wells).
- **Add a provenance table:** URL, fetch date, licence, robots status, byline, and the reason each item was kept or dropped.
- **Mostly drop PII scrubbing:** the text is public. Keep one NER pass that swaps the author's recurring entities (employer, products, colleagues) for placeholders. That pass now serves topic-leak control.
- **Retarget the AI-text filter** at quoted LLM output in post-2022 posts, in place of the user's AI-assisted drafts.
- **Use the Claude API** (Message Batches) for all data prep. No privacy constraint remains. Keep a local model as a second drafter for diversity only.
- **Replace the register enum** (`email_casual` and the rest) with form tags assigned per chunk: explainer, argument, how-to or list, anecdote. Chunk to 150-800 words on section boundaries to get memo-length targets.
- **Re-tier by author words.** A ≥200k-word author lands in T3. McKenzie's ~460k usable words land in T3 (measured 2026-11-08); no cap needed.

Phase 2, splits, eval and baselines:
- **Hold out by post, by topic cluster and by era.** Keep 5-10% of posts for the recall test and never train on them.
- **Run a base-model recall probe before any training.** Prompt the untuned base model with held-out summaries, neutral paraphrases and opening lines, and record the longest verbatim spans. The adapter must not raise them.
- **Train the authorship verifier (M1)** on the author's held-out text against same-genre impostors: other authors in this library (public-domain and CC0 texts are the cleanest) plus Claude and base-model outputs on the same briefs. The yoonholee set is a ready multi-author pool. Its CC0 tag does not cover most of its contents, so keep it local and use it for eval only.
- **Make B0 "Claude asked to write like <author>"**, plus a style guide and exemplars. It is much stronger for famous authors (Paul Graham, Scott Alexander, Gwern) than for McKenzie or Housel. Claude-only, because ChatGPT now refuses.
- **Add a target-task set:** 30-50 real briefs from your PM work. The author never wrote about your product, so there is no reference text. Score these with style metrics plus an embedding topic classifier that catches drift toward the author's pet topics.
- **Rewrite blind test A:** a reader picks the real held-out author passage over the system output on a matched brief.
- **Rewrite blind test R:** "which reads more like <author>", system against B0. Read about 30 of the author's posts first, or recruit a reader who knows them.
- **Add a utility arm:** "which would you send?" on your own briefs. Fidelity to the author is the proxy; usefulness is the goal.

Phase 3, training pairs:
- **Drop "brief + facts → original" and "facts only → original" for the author corpus.** That is the summary-to-text shape that reactivated verbatim recall in Whack-a-Mole.
- **Train on paraphrase inversion:** neutral paraphrase → original, and generic draft → original, across all topics. The fact-closure and MIS filters stay. These formats are safer by extrapolation; nobody has tested them.
- **Balance topics:** label each post's topic, cap any one topic's share, and up-sample thin topics at most 2×.
- **Make `write` draft-then-restyle at runtime.** A drafter (Claude or local) turns the brief and facts into a plain draft, and Quill restyles it. This makes the plan's A7 alternative the default and accepts some residual drafter fingerprint. Reintroduce brief-to-text pairs only if the held-out recall test stays clean.

Phases 4-5, training:
- Run 1-2 epochs.
- Keep the existing stop at training loss < 0.2.

Phase 6, inference:
- **Tighten the memorization gate (M9/H8).** Change it from a ≥12-word span against train targets to a ≥8-10-word span against the whole author corpus: train, held-out and dropped text. Resample on any hit.
- **Decode safely:** temperature above 0, and never seed a prompt with the author's opening lines.
- **Keep the no-new-entity gate strict.** It also stops the author's pet companies and people from leaking into your memos.

Phase 8, ship gate:
- **Rewrite H1 and H2** as above.
- **Add H11:** the adapter's longest verbatim span on held-out summaries is no longer than the base model's.
- **Add H12:** topic drift on your own briefs stays under a threshold set on dev.

Phases 9-10, serving and retraining:
- **Keep the author's name out** of adapter names, file names, tool names and any shared output.
- **Keep the corpus and adapters on the Mac,** and delete them if the author objects.
- **Use `record_final` edits to build your own corpus.** They are your writing. Plan a blend or a switch to your own voice once they clear T1 or T2.

## 7. Open questions for the user

1. **Taste.** Read two pieces each from McKenzie, Housel, Evans and Rao. Which do you want to sound like?
2. **Jurisdiction.** Are you in the US, the UK or the EU? The answer changes Russell and Mencken and how much opt-outs weigh legally.
3. **Where outputs go.** Will outputs leave your machine (work memos, published posts)? That sets the overlap threshold and the ethics bar.
4. **Asking.** Will you email the author for permission? Ask McKenzie first. Dynomight is usable only with a yes.
5. **The blind test.** Do you know the author's writing well enough to judge it, or can you name a reader who does?
6. **Era.** Is a 2000s voice (Spolsky) or an Edwardian one (Bennett) acceptable, or must the diction be 2020s?
7. **Long-term voice.** Should Quill drift toward your own voice as your edits accumulate, or stay with the author?
