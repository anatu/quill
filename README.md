# quill

A local style model that rewrites drafts in one author's voice, exposed to Claude Code as an MCP tool.

Claude decides what to say. Quill rewrites it. The core is a QLoRA adapter on a 7-9B open-weight model, trained and served on an Apple Silicon Mac with MLX. Prompt-only imitation is out of scope.

Target voice: Morgan Housel's essays on the Collaborative Fund blog, used with Collaborative Fund's consent. The corpus, adapters and weights stay on the local machine. None of them are in this repo.

## Status

| Phase | State |
|---|---|
| 0 Source and consent audit | Done, except the stored consent copy |
| 1 Extraction and cleaning | Built. Two gate items open: the spot check and the AI-text flag decisions |
| 2 Splits, eval harness, baselines | Splits frozen; model-free metrics built and sanity-checked. Baselines and eval inputs open |
| 2b-10 | Not started |

The full plan is in [knowledge_base/plan.md](knowledge_base/plan.md).

## Setup

Needs [uv](https://docs.astral.sh/uv/) and Python 3.12.

```
uv sync
uv run pytest
```

Data lives in `~/.quill/`, outside the repo. Raw pages go in `~/.quill/raw/collabfund/pages/`. Paths and thresholds are in [configs/quill.yaml](configs/quill.yaml).

## Commands

| Command | What it does |
|---|---|
| `uv run quill audit` | Inventories the raw pages and checks them against the Phase 0 figures |
| `uv run quill ingest` | Extracts, cleans, dedupes and chunks the pages into `~/.quill/corpus/corpus.sqlite`; writes `cleaning_report.md` |
| `uv run quill aicheck` | Builds lexicon v0 and flags posts dated after 2022-12-01 for review; writes `ai_flags.md` |
| `uv run quill flags [slug keep\|drop]` | Lists the flags, or records a decision on one |
| `uv run quill spotcheck [--record N]` | Writes 100 random chunks for a human read; records the count of bad ones |
| `uv run quill gate` | Shows the Phase 1 exit gate |
| `uv run quill split` | Freezes topic-disjoint train/dev/test splits, or shows the frozen ones |
| `uv run quill eval --sanity` | Checks each style metric on dev and recomputes the within-author ceiling |
| `uv run quill eval --system NAME --split dev` | Scores a system; reports go to `eval_reports/` |

Run them in that order. A rebuild with `ingest` keeps flag decisions and clears the spot-check result.

## What Phase 1 does

1. **Extract.** A parser for the Collab Fund page layout keeps body paragraphs, list items and headings. It drops navigation, share bars, newsletter boxes and captions.
2. **Clean.** Block quotes, whole-paragraph quotations, related-post lists, promo lines and separators go. Every dropped block is stored with a reason.
3. **Drop posts.** Posts by other authors, posts under 120 words, and posts named in `corpus.drop_posts` (book announcements, interviews, a transcript).
4. **Twins.** Posts that share more than 30% of their 10-grams get a `twin_group`, so they stay on one side of every split.
5. **Dedupe.** MinHash over paragraphs keeps the earliest copy of each repeated paragraph.
6. **Chunk.** 150-800 words on paragraph boundaries, in three length buckets. Chunks carry flags such as `list`, `quote_gap` and `dangling_leadin`.
7. **AI-text check.** Three review signals on later posts: lexicon rates above the author's own pre-cutoff 95th percentile, a sustained style shift (PELT), and LLM mentions or chatbot referrer links. Nothing is dropped without a decision.
8. **PII.** A regex pass for email addresses and phone numbers.

Current output: 331 posts, 320,817 words, 841 chunks.

## Layout

```
configs/
  quill.yaml            paths, thresholds, dropped posts, decisions
  lexicon/              seed lexicon v0 and the Kobak excess-word list
src/quill/
  cli.py                the commands above
  audit.py              Phase 0 inventory
  ingest/               page parser; textlib (the Phase 0 reader and stylometrics)
  clean/                boilerplate, twins, dedupe, chunk, pii_regex, ai_check
  corpus/               build (the pipeline), store (SQLite), gate, split
  scorers/              lexicon, contrast, av (verifier, attribution), stylometry, memo, entities, embed
  eval/                 pool (author chunks, impostors), harness
eval_reports/           aggregate metrics only
tests/                  synthetic pages only; no corpus text
knowledge_base/         plan, literature review, research notes, decision docs
```

## Data rules

- The corpus is used under the rights holder's consent. The record is `~/.quill/legal/scope.yaml`. A use marked unknown there is blocked.
- Raw pages are cached once and never re-fetched. Crawls honour robots.txt, AI opt-outs and crawl delays.
- The corpus, adapters and fused weights never leave the machine. `.gitignore` blocks weights, databases, JSONL and HTML.
- Outputs are never presented as the author's own writing.

Details are in [knowledge_base/plan.md](knowledge_base/plan.md), section 2.4. Nothing here is legal advice.

## Third-party material

- `configs/lexicon/kobak_excess_words.csv`: Kobak et al., [llm-excess-vocab](https://github.com/berenslab/llm-excess-vocab), MIT. Licence in `configs/lexicon/kobak_LICENSE`.
- `src/quill/scorers/contrast.py`: a port of the stage-1 regexes from [slop-score](https://github.com/sam-paech/slop-score), Copyright (c) 2025 Sam Paech, MIT.
- `configs/lexicon/seed_v0.yaml`: vocabulary and patterns drawn from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), CC BY-SA 4.0.
