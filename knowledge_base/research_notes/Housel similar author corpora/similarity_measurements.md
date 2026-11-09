# Housel-similar authors: measured style similarity (StyleDistance + stylometry)

Run date: 2026-11-08. Everything was computed locally. Raw pages, scripts and outputs live in the session scratchpad at `/Users/natuanand/.quill/research/2026-11-08/simpass/` (called `simpass/` below). The full metric table is `simpass/results.csv` (24 rows × 45 columns).

**Labels.** **[M]** marks a number measured in this run. **[I]** marks my inference or interpretation. Unlabelled method text describes what was done.

---

## 1. Summary

- **[M] No candidate is stylistically indistinguishable from Housel.**
  - The within-Housel ceiling, half H-A vs half H-B, gives a StyleDistance verification AUC of **0.50**.
  - Every candidate scores between **0.87 and 1.00**, at a matched 20 passages per class. The best is Naval at 0.871 ± 0.06.
  - Burrows' Delta tells the same story: the ceiling is **0.75**, and candidates range from 0.95 to 1.37.
- **[M] The composite ranking** (mean of the AUC rank and the Delta rank) puts these seven first:
  1. Farnam Street (Shane Parrish bylines, 2012–16)
  2. Naval
  3. Seth Godin
  4. Josh Brown (small sample)
  5. Jason Zweig
  6. Ted Lamade
  7. James Clear

  The bottom four are Nick Maggiulli, Jonathan Clements, Warren Buffett and Joe Wiggins.
- **[M] The ranks are not sharp.**
  - The two main metrics agree only weakly: Spearman ρ between AUC and Delta is 0.33 across 20 candidates.
  - Simulated 10–90% rank intervals are wide. FS spans 1–7, Lamade 3–14 and Carlson 2–15.
  - Treat the table as tiers, not an exact order (§6).
- **[M] Two candidates are lexically closer to Housel than my own imitation.** FS (0.951) and Lamade (1.026) have a lower Delta than `claude_housel` (1.044). No candidate is closer to `claude_plain` than to Housel on both measures, except **Buffett** and **Wiggins**. They are nearer to `claude_plain` on both Delta and StyleDistance cosine.
- **[M] Several candidates are no closer than the distant control on the embedding metric.** Patrick McKenzie scores AUC 0.992 and Delta 1.100.
  - Clements, Buffett and Wiggins are worse on both metrics.
  - Graham (1.000) and Kelly (0.992) have AUCs at or above McKenzie's, and Marks (0.990) is within noise of it. All three have a Delta below McKenzie's.
- **[M] Claude imitating Housel is perfectly separable from Housel in StyleDistance space.** It scores AUC 1.00 and the lowest centroid cosine of any row (0.866). Yet on function-word Delta (1.044) it beats most humans. **[I]** A prompt-only imitation copies Housel's vocabulary profile but not what StyleDistance encodes. This supports the project's no-prompt-only rule.
- **[I] My recommendation for mixture experiments:**
  - **First pick: Ted Lamade.** He is in the top tier on both metrics, and has the largest clean sample in that tier (46k words, 144 passages). He also publishes on Housel's own venue. Caveat: 61% of his posts date from 2023 or later.
  - **Next: the rest of Tier 1 (§6): Farnam Street (Shane Parrish), Zweig, Clear, Holiday, Godin and Naval.** Ryan Holiday ranks 10th, but his AUC is 0.966 and his Delta 1.067, at a larger sample. Brown also qualifies, but his usable text is too thin.
  - **Deprioritise Buffett and Wiggins** (Tier 4). Treat Tier 3 (Graham, Clements, Kelly, Marks, Maggiulli, Fried) as no more Housel-like than the distant control in StyleDistance terms. These are measured differences, but topic and genre likely drive part of them (§8).

---

## 2. Method

### 2.1 Order of work (controls first)
1. Wrote the controls before opening any Housel text. Only Housel file *names* were listed. The 10 `claude_housel` essays (635–719 words each) were written in Housel's style from memory. The 10 `claude_plain` essays (647–739 words) were written in my default explanatory prose. Both sets cover compounding, risk, luck, history repeating, spending and status, forecasting, patience, incentives, debt and envy. The timestamp is in `simpass/controls/WRITTEN_AT.txt`.
2. Ran the access gate for each site, then sampled, extracted, built passages and scored.
3. Added six authors at the coordinator's request, using the same gate, cap, rate limit and metrics: Lamade, Zweig, Clements, Wiggins, Holiday and Naval.

### 2.2 Corpora
- **Housel:**
  - The crawl had 351 pages. 342 posts survived cleaning (337,898 words, 2016–2026). Nine were dropped as under 120 words, for example the "What we're reading" link lists.
  - The posts were split into two random halves by post (Python `random.Random(42)`): H-A has 171 posts (155.6k words, 482 passages) and H-B has 171 posts (182.3k words, 563 passages).
  - **H-B is the reference "Housel" for every comparison.** H-A is scored exactly like a candidate, which gives the ceiling.
- **McKenzie** (distant human control): the `kz_late` and `bam` crawls.
  - I excluded files with "podcast" in the name and pages with 2 or more case-insensitive "transcript" matches. That removed 20 pages.
  - 110 posts remained (448k words, 1,412 passages, 2011–2026).
- **Candidates:** up to 30 posts each. Posts under 120 words after cleaning were dropped; the threshold for Godin was 60, because his posts are short by design.

### 2.3 Extraction (stdlib `html.parser`, `simpass/scripts/textlib.py`)
- **Kept:** `p` and `li` text.
- **Dropped:** anything inside `blockquote`, `pre`, `code`, `table`, `figure` and `figcaption`. Also dropped: script, style, nav, header, footer, aside and form elements, and elements whose class or id marks them as comments, sidebar, share, newsletter, subscribe, byline, meta, related, footnotes and so on. Layout wrappers such as `content-sidebar-wrap` and `mainwrap … sidebar` are exempt from the class rule.
- **Main-content choice:** the deepest container holding at least 70% of paragraph words.
- **Paragraph filters:**
  - lines where links make up over 60% of a paragraph under 40 words;
  - a boilerplate regex (subscribe, further reading, disclosure, source:, and so on);
  - footnote markers;
  - paragraphs repeated across at least max(3, 10%) of an author's posts.
- **Site-specific parsers:**
  - Paul Graham: `<br><br>` paragraphs, with the date line, Notes and Thanks sections removed.
  - Buffett: tag-stripped text for the HTML letters and PyMuPDF text blocks for the PDFs. Tables, number rows and headings were dropped.
  - Marks: PyMuPDF blocks from Oaktree's "Complete Collection" PDF, split at `Memo to:` headers. Each memo's year comes from its © footer. The Legal Information section was dropped.
  - Godin and KK: year-archive pages split into individual posts.
  - HEY World: post pages.
- **Passages:** about 250–350 words, cut on paragraph boundaries. Paragraphs over 450 words are split at sentence boundaries. A post remainder under 250 words is carried into the next post's passage, which matters mainly for Godin. Each passage keeps its first post's id as its group label for cross-validation.

### 2.4 Metrics (`simpass/scripts/analyze.py`)
- **StyleDistance:** `StyleDistance/styledistance` via sentence-transformers 5.4.1, loaded normally with `trust_remote_code=False`. The snapshot contains no `.py` files. The model is RobertaModel with mean pooling, 768 dimensions; I set `max_seq_length=512` and normalised the embeddings.
  - **Cosine → Housel:** mean cosine of the author's passages to the normalised H-B centroid.
  - **Verification AUC (primary, `sd_auc_n20`):**
    - Draw 20 author passages and 20 H-B passages (Brown has only 14).
    - Classifier: StandardScaler, then LogisticRegression with C=1.
    - CV: 5-fold StratifiedGroupKFold, grouped by post so that one post never sits in both train and test.
    - Score: AUC on the out-of-fold predictions. Reported as the mean ± SD over 20 resamples.
  - Housel is subsampled to match, as specified. The 20-passage match exists because classifier power grows with n, which would make small-sample authors look more similar. `sd_auc_n60` repeats the test at 60 per class, over 10 resamples, for authors with at least 60 passages.
- **Burrows' Delta:**
  - **Word list:** the top 150 words by author-balanced pooled relative frequency over the basis set. The basis set is all authors except H-A and pooled Housel: the 20 candidates, H-B, McKenzie and both controls.
  - **z-scores:** standardised with the mean and SD across the basis profiles. The word list and the statistics are frozen in `simpass/delta_basis.json`.
  - **Score:** Delta is the mean |z_sample − z_H-B| over the 150 words. The sample is about 4,000 words of random passages, and I report the mean ± SD over 30 draws. Fixing the sample size equalises sampling noise across authors.
  - `delta_to_plain` uses the same procedure against the `claude_plain` profile.
- **Stylometrics** (over all of an author's passages):
  - **Sentence length:** words per sentence, mean and population SD. The splitter is a regex that protects abbreviations, initials and decimals.
  - **Paragraphs:** words per paragraph, and the share of one-sentence paragraphs.
  - **Questions and exclamations:** per 100 sentences.
  - **Pronouns:** first-person singular (I, me, my, mine, myself and their contractions) and second person (you, your and so on), per 1,000 words.
  - **Punctuation per 1,000 words:**
    - em dash: "—", plus spaced "--" and spaced en dash;
    - semicolon;
    - colon (excluding times and URLs);
    - opening parenthesis.
  - **MATTR:** window of 500 tokens.
- **Composite:**
  - Rank the 20 candidates by AUC n=20 (ascending) and by Delta (ascending), using average ranks for ties.
  - Take the mean of the two ranks, and break ties by AUC.
  - `rank_p10` and `rank_p90` come from 4,000 re-rankings, each with AUC and Delta perturbed by their own resample SDs. **[I]** This is an approximate uncertainty band, not a formal CI.
  - Why these two metrics: they are independent views, one learned and style-specific, the other classic function-word stylometry. The centroid cosine is left out because it is compressed into 0.87–0.98, and the distant control scores 0.961 on it, so it barely discriminates **[M]**.
- **Flags:**
  - `flag_delta_below_claude_housel`: the candidate's Delta is below `claude_housel`'s 1.044.
  - `flag_closer_to_plain_delta`: Delta to `claude_plain` is below Delta to Housel.
  - `flag_closer_to_plain_sd`: cosine to the `claude_plain` centroid is above cosine to the Housel centroid.
  - `flag_not_closer_than_mckenzie`: AUC ≥ 0.992 and Delta ≥ 1.100.
  - `flag_small_sample`: fewer than 20 passages, or fewer than 4,000 words.

---

## 3. Access verdicts **[M]**

**Gate rules:**
1. Fetch robots.txt first.
2. **Block** the site if `urllib.robotparser` refuses a sample content URL for `*`, GPTBot, ClaudeBot, anthropic-ai, CCBot or Google-Extended. Also block on a `Disallow: /` group for any of those agents, or on a `Content-Signal: ai-train=no` line.
3. Skip the site if it is hosted on Substack or Medium.
4. Scan all 463 fetched HTML pages for the following, and skip the site on a confirmed hit:
   - `noai` or `noimageai` meta tags;
   - `tdm-reservation`;
   - an `X-Robots-Tag: noai` header;
   - Substack or Medium fingerprints;
   - explicit no-AI-training wording.
5. I did not read site terms-of-service pages. That is a limitation.

**Fetch settings:** User-Agent `Mozilla/5.0 (quill-research)`, with no email or other identity sent. Requests to a site were at least 1.05 s apart, and HumbleDollar's were 10.5 s apart. The cap was 30 requests per site, **counting robots.txt, sitemaps and archive pages**.

**All 20 sites passed. None was skipped.**

| Candidate | Site / source used | robots.txt | Notes from gate | Requests |
|---|---|---|---|---|
| Ben Carlson | awealthofcommonsense.com, Yoast post sitemaps 3, 8, 13 | 200, `*` disallows calendar paths only | WordPress (Flywheel), clean | 30 |
| Michael Batnick | theirrelevantinvestor.com, beehiiv sitemap | 200; blocks Amazonbot and Nutch; no gated agent | **beehiiv, not Substack** (153 beehiiv strings on the homepage). Sitemap covers only about 2023 on, after the migration | 29 |
| Josh Brown | thereformedbroker.com, post sitemaps 8, 11, 13 | 200; **`Crawl-delay: 3` for `*`** | WordPress. **Deviation:** fetched at about 1.05 s gaps, within the 1 req/s rule but faster than the site's crawl-delay | 30 |
| Nick Maggiulli | ofdollarsanddata.com, post sitemap | 200, wp-admin only | WordPress | 29 |
| Seth Godin | seths.blog, year archives 2004–2022 | 200, wp-admin only | WordPress | 13 |
| James Clear | jamesclear.com, post sitemap | 200, `Disallow:` empty | WordPress | 29 |
| Farnam Street | fs.blog, post sitemap 1 | 200; **explicit `Allow: /`** for GPTBot, ClaudeBot, anthropic-ai, CCBot, Google-Extended and others ("owner preference updated 2026-10-31") | WordPress; Shane Parrish byline required (meta author) | 29 |
| Derek Sivers | sive.rs, /blog list with dates | 200, `Allow: /` | clean | 29 |
| Kevin Kelly | kk.org/thetechnium, year archives | 200; blocks MJ12bot, dotbot, meta-externalagent and Amazonbot only | Year archives for 2005, 2016 and 2018 returned 404. A homepage "no-AI wording" hit was a post *about* LLM training (false positive). Plus 3 requests for the add-author test (kk.org total 15) | 12 (+3) |
| Jason Fried | world.hey.com/jason | 200, `Allow: /` | HEY World. Older posts were reached by building the site's own `?page=` cursor (base64 `{created_at, id}`), which jumped to 2021–22 | 29 |
| Howard Marks | oaktreecapital.com, "The Complete Collection" PDF (26 MB, one request) | 200; disallows marketing, communication and events docs only | memos path allowed | 3 |
| Warren Buffett | berkshirehathaway.com/letters | **404 = no restrictions** | The 1998 and 2002 links are stubs, so the real files (`1998htm.html`, `2002pdf.pdf`) were fetched | 15 |
| Paul Graham | paulgraham.com/articles.html | 200; Roverbot only | clean | 30 |
| Carl Richards | behaviorgap.com, post sitemap | 200; `Disallow: /*?`; **`Crawl-delay: 3`** | WordPress. **Same crawl-delay deviation as Brown.** Every post's WordPress author is "jacqueline" (see §7) | 29 |
| Ted Lamade | collabfund.com author page | **404 = no restrictions** | Jekyll. One page's meta description reads "…ideas for this Substack": essays appear to be cross-posted from a Substack, but the pages fetched are served by Collab Fund | 30 |
| Jason Zweig | jasonzweig.com, WP core sitemap | 200, wp-admin only | WordPress; visible "By Jason Zweig" | 30 |
| Jonathan Clements | humbledollar.com, author archive (author id 14) pages 1, 14, 24, 34 | 200; disallows `/insight/`, `/preview/`; **`Crawl-delay: 10`, honoured (10.5 s)** | Multi-author WordPress. All 25 kept posts have the meta author "Jonathan Clements" | 30 |
| Joe Wiggins | behaviouralinvestment.com, sitemap | 200, WordPress.com default | WordPress.com | 30 |
| Ryan Holiday | ryanholiday.net, Yoast post sitemap | 200, `Disallow:` empty | WordPress | 30 |
| Naval | nav.al, Yoast post sitemap | 200, `Disallow:` empty | WordPress. Podcast and transcript rule applied; no page was excluded | 30 |

---

## 4. Ranked table **[M]**

Column notes:
- SD = StyleDistance; "cos→H" is the mean cosine to the H-B centroid.
- AUC: 0.5 means indistinguishable from Housel, 1.0 means perfectly separable.
- Delta: lower is closer. The ceiling is 0.753.
- Composite = mean of the AUC rank and the Delta rank (lower is better). "Rank 10–90%" is the simulated band **[I]**.
- "≤2022 share" is the share of kept posts dated 2022 or earlier.

| Rank | Rank 10–90% | Author | Posts | Passages | Words | Years | ≤2022 share | SD cos→H | SD AUC n=20 (±sd) | SD AUC n=60 | Delta 4k (±sd) | Composite | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1–7 | Farnam Street (Shane Parrish bylines) | 15 | 32 | 10301 | 2012-2016 | 1.0 | 0.969 | 0.939 ±0.04 | – | 0.951 ±0.06 | 2.8 | Delta<claude_housel |
| 2 | 1–7 | Naval Ravikant (nav.al) | 20 | 34 | 10871 | 2005-2021 | 1.0 | 0.974 | 0.871 ±0.06 | – | 1.063 ±0.06 | 3.5 | – |
| 3 | 2–10 | Seth Godin | 30 | 22 | 6913 | 2004-2022 | 1.0 | 0.927 | 0.939 ±0.03 | – | 1.059 ±0.04 | 4.8 | – |
| 4 | 2–11 | Josh Brown | 12 | 14 | 4313 | 2014-2020 | 1.0 | 0.978 | 0.915 ±0.05 | – | 1.096 ±0.02 | 6.2 | small sample (AUC at n=14) |
| 5 | 2–13 | Jason Zweig | 20 | 57 | 18266 | 2010-2019 | 1.0 | 0.958 | 0.960 ±0.02 | – | 1.057 ±0.07 | 7.0 | – |
| 6 | 3–14 | Ted Lamade (Collab Fund) | 28 | 144 | 46411 | 2021-2026 | 0.39 | 0.961 | 0.977 ±0.02 | 0.989 | 1.026 ±0.08 | 7.0 | Delta<claude_housel |
| 7 | 3–14 | James Clear | 26 | 90 | 29178 | 2012-2018 | 1.0 | 0.971 | 0.954 ±0.03 | 0.984 | 1.092 ±0.07 | 8.5 | – |
| 8 | 2–15 | Ben Carlson | 25 | 61 | 19411 | 2013-2022 | 1.0 | 0.967 | 0.934 ±0.04 | 0.957 | 1.142 ±0.11 | 8.8 | – |
| 9 | 4–15 | Michael Batnick | 21 | 32 | 9866 | 2017-2025 | 0.29 | 0.970 | 0.940 ±0.04 | – | 1.126 ±0.05 | 9.0 | – |
| 10 | 3–14 | Ryan Holiday | 25 | 77 | 24788 | 2007-2021 | 1.0 | 0.970 | 0.966 ±0.02 | 0.984 | 1.067 ±0.07 | 9.0 | – |
| 11 | 5–17 | Carl Richards (behaviorgap.com) | 25 | 29 | 9126 | 2019-2022 | 1.0 | 0.980 | 0.953 ±0.04 | – | 1.142 ±0.04 | 10.8 | – |
| 12 | 10–17 | Paul Graham | 25 | 168 | 53130 | 2001-2022 | 1.0 | 0.893 | 1.000 ±0.00 | 1.000 | 1.048 ±0.07 | 11.2 | nearer plain (SD) |
| 13 | 7–16 | Howard Marks | 15 | 245 | 77362 | 1998-2022 | 1.0 | 0.949 | 0.990 ±0.01 | 0.990 | 1.072 ±0.06 | 11.5 | – |
| 14 | 8–17 | Derek Sivers | 25 | 34 | 10759 | 2000-2022 | 1.0 | 0.978 | 0.958 ±0.03 | – | 1.185 ±0.05 | 13.0 | – |
| 15 | 7–17 | Jason Fried (HEY World) | 23 | 36 | 11127 | 2021-2022 | 1.0 | 0.908 | 0.981 ±0.02 | – | 1.140 ±0.07 | 13.0 | – |
| 16 | 8–16 | Kevin Kelly | 19 | 47 | 15098 | 2007-2020 | 1.0 | 0.944 | 0.992 ±0.01 | – | 1.096 ±0.04 | 13.2 | – |
| 17 | 12–19 | Nick Maggiulli | 26 | 123 | 38984 | 2017-2026 | 0.31 | 0.964 | 0.988 ±0.02 | 0.998 | 1.192 ±0.07 | 16.0 | – |
| 18 | 12–18 | Jonathan Clements (HumbleDollar) | 25 | 53 | 16843 | 2016-2020 | 1.0 | 0.971 | 0.996 ±0.01 | – | 1.177 ±0.08 | 16.5 | not closer than McKenzie |
| 19 | 18–20 | Warren Buffett | 11 | 305 | 97502 | 1980-2022 | 1.0 | 0.909 | 0.999 ±0.00 | 1.000 | 1.366 ±0.07 | 19.0 | nearer plain (Delta), nearer plain (SD), not closer than McKenzie |
| 20 | 18–20 | Joe Wiggins (Behavioural Investment) | 27 | 80 | 26352 | 2017-2022 | 1.0 | 0.908 | 1.000 ±0.00 | 1.000 | 1.362 ±0.07 | 19.2 | nearer plain (Delta), nearer plain (SD), not closer than McKenzie |

**[M]** Spearman across the 20 candidates:
- AUC vs Delta: 0.33.
- AUC vs (−cosine): 0.64.
- Delta vs (−cosine): −0.07.

The two StyleDistance metrics broadly agree. Delta measures something largely different.

---

## 5. Reference rows **[M]**

| Row | Passages | Words | SD cos→H | SD AUC n=20 (±sd) | SD AUC n=60 | Delta 4k (±sd) | Delta→plain | SD cos→plain |
|---|---|---|---|---|---|---|---|---|
| Housel H-A vs H-B (ceiling) | 482 | 154072 | 0.981 | 0.497 ±0.12 | 0.501 | 0.753 ±0.07 | 1.608 | 0.863 |
| claude_housel (Claude imitating Housel) | 20 | 6614 | 0.866 | 1.000 ±0.00 | – | 1.044 ±0.04 | 2.004 | 0.826 |
| claude_plain (Claude default prose) | 23 | 6768 | 0.879 | 1.000 ±0.00 | – | 1.511 ±0.04 | – | – |
| Patrick McKenzie (distant human control) | 1412 | 450442 | 0.961 | 0.992 ±0.01 | 0.997 | 1.100 ±0.06 | 1.376 | 0.895 |

**[M]** What the reference rows show:
- The method passes its sanity checks. The two Housel halves are indistinguishable (AUC 0.50, Delta 0.75). `claude_plain` is the most distant row on Delta (1.51).
- **[I]** The distant control (McKenzie) is not far from Housel on cosine (0.961) or Delta (1.10). Cosine and Delta therefore have a narrow dynamic range, and AUC is the more discriminating test. "Closer than McKenzie" is a useful minimum bar.

---

## 6. Tiers **[I]**

The thresholds below are my choice. They are anchored on the distant control, McKenzie (AUC 0.992, Delta 1.100), and leave a 0.01 margin on AUC because McKenzie's AUC SD is ±0.01.

- **Tier 1: AUC ≤ 0.98 and Delta < 1.10** (closer than McKenzie on both). Reasonable first adds:
  - Ted Lamade: largest clean sample in this tier, same venue.
  - Farnam Street / Shane Parrish: 2012–16 posts only, 15 posts.
  - Jason Zweig: 2010–2019.
  - James Clear.
  - Ryan Holiday.
  - Seth Godin: small sample, short posts.
  - Naval: lowest AUC, small sample.
  - Josh Brown: qualifies, but has only about 4k words of usable prose (14 passages), because most sampled posts were quote or chart posts.
- **Tier 2: AUC ≤ 0.98 but Delta ≥ 1.10.** Ben Carlson (1.142), Michael Batnick (1.126), Carl Richards (1.142; authorship caveat) and Derek Sivers (1.185). StyleDistance separates them from Housel less easily than the control, but their function-word profiles are no closer than McKenzie's.
- **Tier 3: AUC > 0.98, at McKenzie's level of separability.** Paul Graham (1.000), Jonathan Clements (0.996), Kevin Kelly (0.992), Howard Marks (0.990), Nick Maggiulli (0.988) and Jason Fried (0.981). Graham, Marks and Kelly still have a Delta below 1.10.
- **Tier 4: Delta > 1.3 and nearer `claude_plain` than Housel on both measures (deprioritise).** Warren Buffett (1.366) and Joe Wiggins (1.362).

---

## 7. Stylometric profiles **[M]**

**Housel's profile (all 342 posts):**
- Sentences average **14.7 words** (SD 9.4).
- Paragraphs average **32 words**, and **44%** of paragraphs are a single sentence.
- About 4 questions per 100 sentences, and almost no exclamations (0.27 per 100).
- Light first-person singular (**9.7/1k**) but heavy second person (**24.3/1k**).
- Em dashes **5.7/1k**, semicolons 0.9/1k, colons **6.1/1k**, opening parentheses 0.9/1k.
- MATTR(500) 0.53.
- H-A and H-B agree closely on every feature, so these are stable traits.

**Notable contrasts:**
- **claude_housel** over-shortens: 9.6-word sentences, 23-word paragraphs, 34% one-sentence paragraphs. It has *no* em dashes, semicolons or parentheses, against Housel's 5.7, 0.9 and 0.9 per 1k.
- **claude_plain** has 78-word paragraphs, no one-sentence paragraphs, and no first- or second-person pronouns. It has the highest MATTR (0.57).
- **Closest overall shapes (paragraphs and one-sentence share):**
  - Godin: 31.7 words per paragraph, 45% one-sentence;
  - Carlson: 28.3, 55%;
  - Brown: 36.6, 46%;
  - Lamade: 38.9, 46%;
  - Richards: 31.9, 37%.
- **Furthest:** Buffett and Graham (80 and 62 words per paragraph, 8% one-sentence), Wiggins and Marks (74 and 72), Kelly (70), and Holiday (59).
- **[I]** Paragraph shape is a big part of what an adapter would learn. On this axis Godin, Carlson, Lamade and Brown are the best matches.

| Row | Sent len | Sent SD | Words/para | 1-sent para | ?/100 sent | !/100 sent | 1st-sg/1k | 2nd/1k | Em dash/1k | ;/1k | :/1k | (/1k | MATTR500 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Housel (all 342 posts)** | 14.67 | 9.42 | 32.44 | 0.44 | 4.11 | 0.27 | 9.73 | 24.28 | 5.71 | 0.89 | 6.08 | 0.94 | 0.53 |
| **Housel H-A** | 14.44 | 9.28 | 32.94 | 0.42 | 3.44 | 0.23 | 10.92 | 26.52 | 5.13 | 0.79 | 5.74 | 0.90 | 0.53 |
| **Housel H-B (reference)** | 14.87 | 9.53 | 32.02 | 0.46 | 4.71 | 0.30 | 8.72 | 22.38 | 6.20 | 0.98 | 6.37 | 0.98 | 0.54 |
| Farnam Street (Shane Parrish bylines) | 17.03 | 9.90 | 34.92 | 0.39 | 5.12 | 0.33 | 5.14 | 16.31 | 2.14 | 0.97 | 6.21 | 3.11 | 0.52 |
| Naval Ravikant (nav.al) | 12.49 | 8.89 | 34.51 | 0.30 | 7.36 | 0.34 | 19.68 | 27.69 | 3.68 | 1.66 | 3.96 | 1.01 | 0.48 |
| Seth Godin | 14.20 | 8.69 | 31.71 | 0.45 | 5.75 | 1.03 | 13.45 | 33.85 | 0.00 | 0.14 | 3.33 | 5.06 | 0.52 |
| Josh Brown | 15.03 | 10.08 | 36.55 | 0.46 | 10.45 | 2.79 | 15.07 | 17.16 | 5.80 | 0.23 | 3.94 | 3.25 | 0.56 |
| Jason Zweig | 20.59 | 11.26 | 46.72 | 0.42 | 4.28 | 0.11 | 12.26 | 15.05 | 3.39 | 2.19 | 3.39 | 1.81 | 0.55 |
| Ted Lamade (Collab Fund) | 16.48 | 12.15 | 38.90 | 0.46 | 12.81 | 0.07 | 16.05 | 7.56 | 2.24 | 0.15 | 0.93 | 4.05 | 0.56 |
| James Clear | 15.49 | 8.90 | 37.26 | 0.33 | 7.06 | 0.16 | 18.95 | 39.38 | 3.15 | 0.17 | 2.57 | 2.23 | 0.49 |
| Ben Carlson | 15.68 | 9.06 | 28.30 | 0.55 | 6.62 | 0.40 | 12.16 | 20.66 | 0.98 | 0.31 | 6.08 | 4.43 | 0.51 |
| Michael Batnick | 13.84 | 8.10 | 33.56 | 0.31 | 7.01 | 2.38 | 26.86 | 15.00 | 0.30 | 0.30 | 1.01 | 2.33 | 0.52 |
| Ryan Holiday | 15.55 | 10.34 | 59.02 | 0.25 | 7.65 | 0.75 | 21.34 | 19.65 | 7.50 | 0.32 | 3.51 | 1.77 | 0.54 |
| Carl Richards (behaviorgap.com) | 13.13 | 8.50 | 31.91 | 0.37 | 11.37 | 1.73 | 28.93 | 34.19 | 1.43 | 0.33 | 4.49 | 2.30 | 0.50 |
| Paul Graham | 15.56 | 8.63 | 62.14 | 0.08 | 5.27 | 0.18 | 11.14 | 25.71 | 1.21 | 1.43 | 3.31 | 1.79 | 0.49 |
| Howard Marks | 20.08 | 13.76 | 71.76 | 0.17 | 7.35 | 0.36 | 13.06 | 7.24 | 5.54 | 2.15 | 4.45 | 5.83 | 0.54 |
| Derek Sivers | 11.49 | 7.24 | 29.08 | 0.34 | 3.95 | 3.53 | 55.95 | 25.75 | 1.95 | 0.00 | 3.90 | 2.51 | 0.51 |
| Jason Fried (HEY World) | 12.73 | 9.18 | 36.01 | 0.30 | 11.67 | 0.92 | 14.38 | 24.09 | 6.02 | 0.27 | 1.62 | 2.16 | 0.51 |
| Kevin Kelly | 15.73 | 10.15 | 70.22 | 0.26 | 2.71 | 1.25 | 13.97 | 9.60 | 6.42 | 1.06 | 2.58 | 3.51 | 0.54 |
| Nick Maggiulli | 17.13 | 8.34 | 44.00 | 0.22 | 7.12 | 1.27 | 15.83 | 35.89 | 0.95 | 0.00 | 6.26 | 8.90 | 0.47 |
| Jonathan Clements (HumbleDollar) | 17.15 | 10.40 | 47.31 | 0.23 | 9.78 | 0.00 | 13.48 | 16.86 | 11.58 | 0.00 | 5.17 | 0.95 | 0.55 |
| Warren Buffett | 19.82 | 10.11 | 80.45 | 0.08 | 1.28 | 0.16 | 8.28 | 7.03 | 4.15 | 1.62 | 3.83 | 5.63 | 0.54 |
| Joe Wiggins (Behavioural Investment) | 21.36 | 12.13 | 73.81 | 0.22 | 4.86 | 0.32 | 5.24 | 2.92 | 8.42 | 3.30 | 5.88 | 7.25 | 0.52 |
| claude_housel (Claude imitating Housel) | 9.61 | 5.97 | 23.37 | 0.34 | 2.47 | 0.00 | 7.86 | 32.36 | 0.00 | 0.00 | 1.97 | 0.00 | 0.51 |
| claude_plain (Claude default prose) | 18.39 | 8.27 | 77.79 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 | 0.15 | 0.15 | 0.57 |
| Patrick McKenzie (distant human control) | 19.77 | 12.79 | 55.47 | 0.25 | 5.53 | 1.48 | 17.11 | 16.62 | 1.18 | 1.38 | 4.66 | 7.29 | 0.54 |

---

## 8. Caveats

**Sample sizes:**
- **[M]** Candidate samples range from 4.3k to 97.5k words and from 14 to 305 passages. The matched-n AUC (n=20) and the 4k-word Delta remove most of the sample-size bias, but not the noise. At n=20 the ceiling's own AUC SD is ±0.12.
- **[M]** Brown has only 14 passages; 13 of his 25 sampled posts were under 120 words (quotes, videos, charts). FS kept 15 posts; 11 were too short once block quotes were removed, since early FS posts are mostly book excerpts. Godin kept 22 passages, Richards 29, Batnick and FS 32, Naval and Sivers 34.
- **[M]** An add-author test with 5 passages gave AUC 0.83. **[I]** Below about 20 passages, AUC is biased toward 0.5. The CSV flags this with `flag_small_sample`.

**Topic and genre confounds [I]:**
- StyleDistance is trained to ignore content, but not perfectly, and Delta's top 150 words include some topic-bearing items.
- Finance bloggers (Carlson, Batnick, Brown, Zweig) share Housel's topics. Graham, Kelly and Fried write about startups and technology. Buffett and Marks write shareholder letters and memos, with tables, legal text and long quoted passages. PDF block quotes could not be detected and removed, unlike HTML `<blockquote>`.
- Some of the separation for Buffett, Marks and Wiggins is likely genre, not voice. I did not run a topic-matched comparison.

**Date ranges [M]:**
- **Housel's corpus (2016–2026) was not date-filtered;** about 19% of its posts are after 2022.
- Sampling targeted 2022 or earlier. Candidates where at least 15 kept posts were dated 2022 or earlier had later posts dropped (the "soft rule"). Coordinator cut-offs were applied to Zweig (2021 or earlier) and Clements (before 2022-11-30; all kept posts are 2016–2020).
- **Exceptions:**
  - **Batnick:** the beehiiv sitemap only lists the migrated archive, and the 2015–2022 WordPress posts are not listed. Only 29% of kept posts are dated 2022 or earlier.
  - **Maggiulli:** many URLs are evergreen guides with republication dates; 31% are 2022 or earlier.
  - **Lamade:** kept as specified (2021–2026, 39% 2022 or earlier).
  - **Fried:** HEY World only starts in 2021, so all posts are 2021–22.
- Dates come from `article:published_time`, JSON-LD, `<time>`, the URL, or a page date string. They may be republication dates.

**Authorship [M]/[I]:**
- **Carl Richards:** every behaviorgap.com post has WordPress author "jacqueline", with no visible "by Carl Richards" byline. The text is first-person and consistent with Carl's voice, but **authorship is unverified**.
- **Zweig and Wiggins:** no meta author was found. Both are single-author sites; Zweig's pages say "By Jason Zweig".
- **FS:** only posts whose meta author is Shane Parrish were kept.
- **Clements:** only posts on his author archive with meta author Jonathan Clements.

**Gate and process deviations [M]:**
- **Brown and Richards:** both robots.txt files specify `Crawl-delay: 3`. I fetched at about 1.05 s, honouring the 1 req/s rule but not the site directive. That was 30 and 29 requests. HumbleDollar's crawl-delay of 10 was honoured. `add_author.py` now honours any `*` crawl-delay automatically.
- **Lamade:** one Collab Fund page's metadata refers to "this Substack". The pages fetched are hosted by Collab Fund, so the Substack-hosting rule does not apply. **[I]** The Substack originals may carry different terms.
- **Fried:** the HEY cursor parameter was built by hand to reach older posts.
- **ToS pages:** I did not read site terms-of-service pages for no-AI clauses. The scan covered robots.txt, meta tags, response headers and page text only.

**Extraction:**
- Some FS headings ("Consistency and Change Bias") survive as one-line paragraphs.
- Godin genuinely uses no em dashes in this sample, and his raw HTML contains none.
- Housel's extracted total (337,898 words) is within 1.2% of the crawl's own count (341,873).

**Controls:**
- **[M]** Each control set is about 6.7k words (20 and 23 passages), the minimum for the n=20 AUC.
- **[I]** `claude_housel` was written from memory before I read any Housel text. A different imitation prompt or model could score differently.

**StyleDistance:**
- One model only. Cosines are compressed (H-A 0.981 vs McKenzie 0.961), so small cosine differences are not meaningful.

---

## 9. Reproduce / extend

Set `SP=/Users/natuanand/.quill/research/2026-11-08/simpass` and `PY=/opt/anaconda3/bin/python3`. Every script that reads downloaded files runs with `-I`, from `/tmp`, with paths passed as arguments.

```bash
# 1. Gate + fetch (budgeted, logged in raw/<key>/_fetchlog.tsv)
$SP/scripts/f.sh <key> https://site/robots.txt                     # wrapper for fetch.py
$PY -I $SP/scripts/gate.py robots $SP/raw/<key>/<robots file> <sample content URL>
$PY -I $SP/scripts/select_urls.py $SP/raw $SP/lists <key>           # sitemap/archive -> spread URL list
$SP/scripts/f.sh <key> --list $SP/lists/<key>.txt                   # FETCH_MIN_GAP=10.5 for HumbleDollar
$PY -I $SP/scripts/gate.py scan $SP/raw/*/*.html                    # noai / Substack / Medium / wording scan

# 2. Corpus + passages (all authors, or name some)
$PY -I $SP/scripts/build_corpus.py $SP $SP/../crawl [author ...]

# 3. Metrics -> results.csv, housel_profile.csv, delta_basis.json (embeddings cached in emb/)
$PY -I $SP/scripts/analyze.py $SP
$PY -I $SP/scripts/report_tables.py $SP                            # markdown tables used above

# 4. Add a new author (reusable): gate + fetch <=29 URLs + build + append/re-rank
$PY -I $SP/scripts/add_author.py $SP <key> urls.txt --name "Display Name" [--byline 'Regex'] [--max-year 2022]
```

`add_author.py` aborts in three cases:
- robots.txt blocks a gated agent;
- a noai, tdm-reservation, Substack or Medium signal is found;
- the host is substack.com or medium.com.

It reuses the frozen Delta basis and the cached H-B embeddings, so the new row is comparable with the existing ones. It then re-ranks all candidate rows. It was tested end to end with two KK posts, and the test row was then removed.

**Files:**
- `simpass/results.csv`: all metrics and flags.
- `simpass/housel_profile.csv`: stylometrics for Housel, H-A and H-B.
- `simpass/delta_basis.json`: the 150 most frequent words, plus the frozen means and SDs.
- `simpass/corpus/<author>.jsonl`: passages.
- `simpass/corpus/<author>_posts.json`: URLs, years, bylines, dropped posts and removed boilerplate.
- `simpass/raw/<author>/`: raw pages and fetch logs.
- `simpass/controls/`: the 20 control essays.
- `simpass/scripts/`: all code.
