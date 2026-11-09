# Pangram WildAI and EditLens: coordinator check (2026-11-07)

Found by the coordinator after the five research passes; none of them listed it. All facts below are from the Hugging Face cards and API, read 2026-11-07, plus a local summary of 11 label shards.

## Takeaway
`pangram/WildAI` is a public, ungated pool of ~96M English Common Crawl / FineWeb documents (2024 to mid-2026), each labeled Human / Mixed / AI by Pangram 3.3.2, the detector with the strongest independent nonfiction results in our notes. Every document also carries WebOrganizer topic and format labels, so AI and human documents can be matched on format (Tutorial, Knowledge Article, Nonfiction Writing) and topic. License CC BY-NC-SA 4.0: fine for private, non-commercial use; adaptations must share alike.

## Cited findings
- Composition (self-reported, card): human 4,177,080 CC + 54,736,995 FineWeb docs; AI 1,490,771 CC + 31,050,180 FineWeb; mixed 262,131 CC + 4,325,289 FineWeb. Paper: Russell, Glickenhaus, Thai, Wieting, Iyyer, Spero, Emi, "How Much Is an AI Token Worth? Scaling Laws for Wild AI-Generated Web Text", arXiv:2609.40295 (2026). — https://huggingface.co/datasets/pangram/WildAI
- Construction (card): FineWeb v1.4.0 dumps CC-MAIN-2024-10 to 2025-26 and Common Crawl 2025-30 to 2026-25 (first 2.6% of WARC files). Preselected by EditLens (`pangram/editlens_Llama-3.2-3B`); EditLens-AI buckets and a crawl-matched EditLens-human draw became candidates; a label-blind "natural" 2026 draw was added. Pangram scored up to three 512-token windows (first, middle, last); Human or AI only when all windows agree, else Mixed. Not a natural sample of the web: AI is over-represented by design.
- Fields (measured via datasets-server): id, text, url, date, dump, source, token_count, truncated, pangram_label, pangram_fraction_ai / _ai_assisted / _human, pangram_version, topic, topic_score, format, format_score, language_score, selection, sampling_hash (sorting by it gives uniform prefixes). A `labels` config has all metadata without text (961 parquet shards, 9.46 GB, measured).
- `pangram/WildAI-monthly` (card): 310,000 label-blind docs, 5,000 per crawl month, Jan 2021 to Aug 2026; Pangram labels 285,105 Human, 3,901 Mixed, 20,994 AI. Usable as a per-month prior and as a natural-distribution eval set. — https://huggingface.co/datasets/pangram/WildAI-monthly
- Models: `pangram/editlens_Llama-3.2-3B` is access-restricted (card says "Access ... is restricted"; API lists 1,673 downloads). `pangram/editlens_roberta-large` is listed (0 downloads; access not checked). `pangram/WildAI-models` are 19.9M-973M LMs trained on controlled AI/human mixtures (not detectors).

## Measured: format x label in 11 of 961 label shards (1,042,446 rows)
Shards evenly spaced (0, 96, ..., 960). Extrapolation x87.4 gives 91.1M rows, matching the card's ~96M. Shards appear block-ordered by selection, so per-format totals are rough estimates (±30% or worse).

| Format | AI (sample) | Human (sample) | AI share in pool | Est. AI total | Est. Human total |
|---|---|---|---|---|---|
| Tutorial | 50,850 | 42,834 | 0.52 | ~4.4M | ~3.7M |
| Nonfiction Writing | 37,388 | 47,184 | 0.43 | ~3.3M | ~4.1M |
| Knowledge Article | 32,960 | 29,379 | 0.51 | ~2.9M | ~2.6M |
| Listicle | 26,290 | 27,770 | 0.46 | ~2.3M | ~2.4M |
| News Article | 10,458 | 78,451 | 0.11 | ~0.9M | ~6.9M |
| Personal Blog | 4,571 | 61,504 | 0.07 | ~0.4M | ~5.4M |
| FAQ | 1,719 | 4,401 | 0.27 | ~0.15M | ~0.38M |
| Documentation | 378 | 3,955 | 0.08 | ~33k | ~0.35M |
| Product Page | 99,434 | 167,682 | 0.35 | ~8.7M | ~14.6M |

- AI docs: median 758 GPT-2 tokens, p90 2,288 (sample, measured). Sampled AI rows dated 2024 (100k) and 2025 (200k).
- Script: /private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/scripts_wildai_summary.py; shards in .../scratchpad/wildai/.

## Inferences
- Volume in informational formats is no longer a constraint: ~10M+ AI-labeled Tutorial / Knowledge / Nonfiction / Listicle docs with format- and topic-matched human docs from the same crawls (estimate).
- Label precision inherits Pangram's: very low FPR on human nonfiction in independent tests (notes: lexicons_and_detectors.md), but Pangram flagged only 3% of fine-tuned author-style outputs (Chakrabarty et al.) and misses some humanized text. WildAI "AI" is high precision for unedited AI prose; WildAI "Human" (2024-26) contains some undetected AI. Use pre-2022 FineWeb for the clean human side.
- Topic/format matching lets contrastive lexicon mining and classifier training control for content, the main defect of off-domain negatives found in the first pass.
- A local classifier trained on WildAI is effectively a distilled Pangram (non-commercial license applies). It will share Pangram's blind spot for fine-tuned style outputs, so it cannot certify quill's adapter outputs as human-like.

## Gaps
- Per-format totals are extrapolated from block-ordered shards; a full pass over the `labels` config (9.46 GB) gives exact counts.
- arXiv:2609.40295 not read; window-agreement precision of Pangram on this pool not reported on the card.
- editlens_roberta-large access status unchecked.
