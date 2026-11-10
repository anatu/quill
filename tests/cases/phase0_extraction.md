# Phase 0 extraction findings (2026-11-08)

Method: `quill audit` on 351 raw pages, plus a pattern scan of all 342 kept posts and a read of the first and last two paragraphs of 20 random posts (seed 7).

Clean already (0 hits in kept text): "Copy Link", "by Morgan Housel", "@morganhousel", "click here", raw URLs, subscribe widgets, `[n]` footnote markers.

Cases for Phase 1:

1. **Title suffix.** Every title ends in " · Collaborative Fund". Strip it before titles are used as context.
2. **Book announcement posts.** Three posts are promotions, not essays: `book-the-psychology-of-money`, `my-new-book-same-as-ever` and `my-new-book-the-art-of-spending-money`. They carry third-party blurbs (for example, Chris Davis's praise). Decide: drop them, or keep only Housel's own paragraphs and drop quoted praise. The 1-line promo "My book, The Psychology of Money, is now out." is in the first one.
3. **Book mentions inside essays stay.** "I highlighted a similar story in my book, The Psychology of Money." is authorial. A promo filter must not remove it.
4. **Numbered lists.** 75 posts have paragraphs that start "1. ", "2. " and so on. This is his listicle format. Keep it, and make the chunker keep a list item with its number.
5. **Short-post drops (9, under 120 words).** "What We're Reading" link roundups (3), "Podcast With Howard Marks" (embed), "The Limits of Investing Sanity" (0 words: check whether it is an image post), and 4 short essays of 74-102 words ("An Interpretation of Stated Odds", "The Bad Side of a Good Idea", "Too Far", "You Can See Where This is Going"). Decide whether short essays come back as a short-length bucket.
6. **Satire.** "An Honest Business News Update" (2017) is a parody news story. Keep it, but tag it so it does not count as a newswire register.
7. **Authorial footnote.** "* Nothing, and yet everything, about this post is accurate." Keep: it is his voice.
8. **Boilerplate.** Only one repeated paragraph was removed across posts: "more on this topic".
9. **Twins.** 12 posts share over 30% of their 10-grams with other posts. There are 4 pairwise groups of 2. The other 4 posts share with several posts at once. Splits keep each group together. Phase 2 should also keep the 4 multi-overlap posts away from their sources.

## Phase 1 outcomes (2026-11-09)

Tests: `tests/test_phase1.py`. Settings: `configs/quill.yaml`.

- Case 1: suffix stripped. Case 2: the three posts are dropped (`corpus.drop_posts`); promo lines go everywhere. Case 3: mentions stay.
- Case 4: typed numbers stay; `<ol>` items get their number; `<ul>` items get "- ".
- Case 5: still dropped under 120 words. "The Limits of Investing Sanity" is an image post.
- Case 6: chunks carry the `satire` flag. Case 7: kept. Case 8: handled by the related-links rule.
- Case 9: `clean.twins.split_groups` puts the 4 multi-overlap posts with their sources (4 groups; the largest has 14 posts).
- New: 5 interviews and 1 podcast transcript dropped; whole-paragraph quotations dropped; quote and image gaps flagged on chunks.
- Spot check (2 samples of 100): epigraphs with a "– Name" line or tail, embedded tweets, "More:" and "For more:" link labels, a disclosure line, a "download the report here" line, and unmarked quotations after "X explained:" (config list). A literal "[x]" is text, not a footnote.
