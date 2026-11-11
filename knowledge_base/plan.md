# Quill build plan, v2

Date: 2026-11-08. Machine: Apple M4 Pro, 24 GB unified memory (about 20.5 GB usable), macOS 26.6, Python 3.13 (anaconda), uv, ollama.
Target voice: Morgan Housel, Collaborative Fund blog. The v1 plan targeted the user's own writing and is retired.
Sources: `lit_review.md` carries the general evidence. Decisions come from `housel_augmentation.md`, `style_library.md`, `negative_signal.md` and `negative_signal_priors.md`. Measurements live in `~/.quill/research/2026-11-08/`.
Labels: **[P]** marks a proposal with no style-specific evidence behind it. "Estimate" marks an unmeasured number. Nothing here is legal advice.

## What changed from v1

- **Target.** Quill now learns Morgan Housel's voice from the Collaborative Fund blog, not the user's writing. The user reports written consent from Collab Fund, and its Terms of Use make that consent load-bearing ([style_library.md](style_library.md), header and §5).
- **Corpus and Phases 0-1.** 342 cleaned posts, 337,898 words, tier T3; the crawl, cleaning measurements and similarity profile are done, and the v1 corpus audit is superseded ([housel_augmentation.md](housel_augmentation.md)). Phases 0-1 are rebuilt for public HTML. Gmail and Drive parsing, quote stripping, signatures, recipients and the Presidio pipeline are gone ([style_library.md](style_library.md) §6).
- **Training.** Housel-only SFT (design D0) comes first. The neighbour mixture (Lamade, Farnam Street, Naval) is an optional gated phase that must beat D0 on held-out Housel text ([housel_augmentation.md](housel_augmentation.md)).
- **Pairs and runtime.** Pairs use paraphrase and generic-draft inversion only. `write` becomes draft-then-restyle. The memorization gate tightens to 8-10 words against the whole corpus, and a base-model recall probe joins the ship gate ([style_library.md](style_library.md) §5-6).
- **Splits.** Topic-disjoint clusters, with reposts beside their twins. The test set freezes before any neighbour text is pulled ([housel_augmentation.md](housel_augmentation.md)).
- **Baselines and blind tests.** B0 is Claude prompted to write like Housel. A reader who knows Housel picks the real passage. The binomial maths is unchanged ([style_library.md](style_library.md) §6).
- **Evaluation.** A negative-signal layer arrives: rebuilt lexicons, a ~10k-item negative set, artifact gate H11, M13 and M14. A 5-way attribution classifier and a tic-profile check join. StyleDistance and Burrows' Delta become diagnostics ([negative_signal.md](negative_signal.md) §5; [negative_signal_priors.md](negative_signal_priors.md) §4-5; [housel_augmentation.md](housel_augmentation.md)).
- **Preference stage.** Own-output rejects only. FTPO needs a fused SFT reference. No harvested AI text enters any loss ([negative_signal.md](negative_signal.md) items 10, 12).
- **Feedback.** `record_final` edits are the user's writing, not Housel's, so they no longer train the adapter ([style_library.md](style_library.md) §6).

## 1. Summary

- Quill is a local style model plus a scoring pipeline, exposed to Claude Code as MCP tools. Claude decides what to say. Quill rewrites it the way Housel would.
- The core is a QLoRA adapter (4-bit base, mlx-lm) on a 7-9B open-weight instruct model, trained on Housel's own text. Prompt-only imitation plateaus at a generic voice. Weight updates are the only approach with strong human-judged wins ([Catch Me If You Can](https://arxiv.org/html/2509.14543v1); [Chakrabarty et al.](https://arxiv.org/abs/2510.13939); [Panza](https://arxiv.org/html/2407.10994)). The skill only routes requests to the tool. A prompt-only product is out of scope.
- Training data is style inversion. An LLM turns each Housel chunk into a neutral paraphrase and a generic assistant draft. The model learns to map both back to his verbatim original. Every fact in a target also appears in its input, so the model learns to restyle, not to invent.
- At runtime `restyle` takes a draft. `write` takes a brief and facts, drafts plainly, then restyles. Quill samples 4 candidates. It drops any that lose or add a name, number, date or link, emit chatbot artifacts, or copy 8-10 words of Housel's text. It ranks the rest by style and meaning and returns the best. If none passes, it returns the input and says so.
- The eval harness, the negative-signal layer and B0 come before the first training run. The adapter ships only if it beats B0 on a blind test and on automatic metrics (Section 6).
- Housel alone first. Similar authors enter only through a gated experiment, and they serve as evaluation impostors either way. Everything trains and serves on the Mac; the corpus and adapters never leave it.

## 2. Architecture

### 2.1 Diagram

```
RUNTIME
 User in Claude Code -> Claude (session model) works out the brief, facts and length
   | thin skill "quill" routes the request (no style instructions)
   v
 quill MCP server (stdio, no models) --HTTP--> quill daemon 127.0.0.1:8765
   1 write only: plain draft from brief + facts (untuned base, no adapter)
   2 render the shared prompt template (op, input, length, voice)
   3 sample N=4 from mlx_lm.server 127.0.0.1:8080 (base 4-bit + adapters/prod)
   4 hard gates: entities/numbers/dates/links kept, none added; MIS >= 0.7;
     no 8-10-word span from the Housel corpus; no chatbot artifacts; length
   5 soft rank: geomean(style score [CISR + stylometry], MIS)
   6 best passing candidate, else status=fallback + reasons; log locally
   <-- {text, status, output_id, checks, scores}; Claude shows text verbatim
 record_final --> ~/.quill/feedback (the user's own writing; never Housel training data)

OFFLINE
 raw/collabfund (read-only) -> extract + clean (block quotes, chrome, promos, near-empty, twins, AI-text check)
   -> chunk 150-800 words -> corpus.sqlite -> frozen topic-disjoint splits -> pairs (Claude API if consent covers it, else local)
   -> curate -> mlx chat JSONL
   -> mlx_lm.lora D0 (two stages) -> [neighbour mixture, gated] -> [ORPO/CPO/FTPO, optional]
   -> eval harness + negative-signal layer vs B0/B1 -> ship gate -> adapters/prod
```

### 2.2 Components

| Component | Choice | Reason |
|---|---|---|
| Content | The calling Claude Code session | Frontier models are good at what to say ([Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)). No API key or extra egress at runtime. |
| Style model | `mlx_lm.server` with per-request `adapters` | OpenAI-compatible; adapter swap per request; no fuse step ([SERVER.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md)) |
| `write` drafter **[P]** | The untuned base on the same server, with no adapter | No API key, no extra memory. The same model drafts half of the training inputs (Phase 4, step 9), so runtime drafts stay in distribution. A7 tests a Claude draft instead. |
| Pipeline | `quill daemon`, one long-running local process | Each Claude Code session starts its own stdio MCP process. Scorers there would duplicate ~2-3 GB per session. |
| Tool surface | MCP Python SDK 2.x, stdio | `from mcp.server import MCPServer` per the 2026-07-28 spec docs ([MCP build-server](https://modelcontextprotocol.io/docs/develop/build-server)) |
| Skill | `~/.claude/skills/quill/SKILL.md`, routing only | User rule: a skill is a thin wrapper around the tool |
| Data-prep LLM | Claude API (Message Batches) if the consent covers sending Housel's text to the API; a local instruct model otherwise | Consent scope (8.3, question 1) |

### 2.3 Tool contract

| Tool | Inputs | Output |
|---|---|---|
| `write` | `brief` (1-3 sentences), `facts` (list), `length_words?` | `{text, status: ok/fallback, output_id, checks, scores}` |
| `restyle` | `draft`, `length_words?` | same |
| `record_final` | `output_id`, `final_text` | ack |
| `status` | none | adapter version, server health |

Rules:
- One register: essay. `register`, `recipient_type` and `reply_to` are gone, because Housel's corpus has no recipients or threads. Length is the only control. Free-text style instructions are refused: they override learned style ("personalization collapse", [PsPLUG](https://arxiv.org/abs/2601.06362)).
- `write` drafts plainly from the brief and facts, then restyles. Brief-to-text training is the summary-to-text shape that reactivated verbatim recall in [Alignment Whack-a-Mole](https://arxiv.org/pdf/2603.20957v2), so v2 trains none. LLM fingerprints survive rewriting ([Idiosyncrasies in LLMs](https://arxiv.org/abs/2502.12150)); M14 measures how much survives.
- Inputs longer than 800 words (the training maximum) are restyled section by section on paragraph boundaries, with the previous output section as context. Long rewrites lose local coherence ([Unslopper](https://huggingface.co/N8Programs/Unslopper-GGUF/blob/main/README.md)).
- Exemplars are off by default. Retrieval at inference made Panza's fine-tuned model copy too much unless it was trained with retrieval in context ([Panza](https://arxiv.org/html/2407.10994)). Ablation A2 tests that. When on, exemplars are random within the length bucket; topic-similar exemplars hurt attribution ([Catch Me If You Can](https://arxiv.org/html/2509.14543v1)).
- Rerank and eval use different style models, so selection cannot game the metric ([TinyStyler](https://arxiv.org/html/2406.15586)). Rerank uses Wegmann CISR plus stylometry. Decisions use M1, M15 and M4. StyleDistance and LUAR are diagnostics.
- Tool, file and adapter names never carry Housel's name. Neither do outputs.

### 2.4 Data, legal and process rules

Not legal advice ([style_library.md](style_library.md) §5).

- **Consent is load-bearing.** Collab Fund's Terms of Use (updated Feb 2026) ban automated copying and storage without express written consent. The user reports that consent, received by 2026-11-08. A copy and its scope record live in `~/.quill/legal/`. Any use outside the recorded scope stops until the scope is clear.
- **Robots and pacing.** Honour every robots.txt AI opt-out (named AI-bot blocks, `ai-train=no`, `tdm-reservation`) and every `Crawl-delay`. Otherwise use 2-5 s gaps. Cache raw HTML once and never re-fetch. The 2026-11-08 pass broke Brown's and Richards' `Crawl-delay: 3`, so their cached pages are final.
- **Identity.** Use a generic User-Agent. Never send the user's email. Ask the user before any pull that needs an account or contact details (a GitHub search token; the Wikipedia recipe in `negative_signal.md` §6.1). Prefer dumps and Hugging Face mirrors.
- **"Open" means no opt-out was found.** It never means licensed. Platform terms count too: Substack and Ghost(Pro) bar crawling, so Substack sources are RSS or permission only.
- **Non-commercial pools are eval-only.** WildAI (CC BY-NC-SA 4.0) and non-CC Grokipedia (xAI Community License) never enter training and stay local. Review derived artifacts before any output goes into paid work. No harvested AI text enters SFT, preference or mixture data ([negative_signal.md](negative_signal.md) §4).
- **Names.** Never present an output as Housel's. Disclose AI help in anything published. Passing off is the live risk: Julia Angwin's class action over Grammarly's named-expert edits ([Nieman Lab](https://www.niemanlab.org/2026/03/journalist-julia-angwin-files-class-action-lawsuit-over-grammarlys-ai-sloppelgangers/)).
- **Locality.** The corpus, adapters and fused weights stay on the Mac (FileVault). Never upload them ([mlx-whatsapp](https://github.com/gavi/mlx-whatsapp)). Delete the corpus if the rights holder objects.
- **Motley Fool.** Do not fetch. Its robots.txt blocks ClaudeBot and sets `ai-train=no` ([robots](https://www.fool.com/robots.txt)), and its terms ban automated harvesting and storing copies ([ToU](https://www.fool.com/legal/terms-and-conditions/fool-rules/)). A written licence is the only route (Branch F).

## 3. Repo layout

Code lives in the repo. Corpus, models and adapters live in `~/.quill/` (FileVault on, never in git).

```
/Users/natuanand/quill/
  pyproject.toml, uv.lock     uv project (scripts: quill, quill-mcp); pins mlx-lm 0.32.x, mlx-lm-lora, mcp>=2.0.0
  .gitignore                  *.safetensors, *.gguf, .env, any local data path
  configs/                    quill.yaml (paths, length buckets, thresholds, ports, consent flags);
                              prompts/ (paraphrase, facts, draft, brief, style_guide, judge); train/{probe,sft,sft-anneal,orpo}.yaml
  src/quill/
    cli.py                    quill audit | ingest | split | pairs | train | eval | blind | negpool | up | down | retrain
    template.py               THE prompt template, shared by pair builder and daemon (byte-identical)
    ingest/collabfund.py      HTML extraction, ported from simpass/scripts/textlib.py
    clean/                    boilerplate  twins  ai_check  pii_regex  chunk
    corpus/                   store (SQLite)  split (topic clusters, twin groups)
    pairs/                    generate (API batch or local)  curate  to_mlx  prefs  mix
    pipeline/                 draft  sample  gates  artifacts  rerank  longform  retrieve
    scorers/                  cisr styledistance luar mis nli entities stylometry lexicon attribution alpha residue memo detector wqrm
    negpool/                  harvest  provenance
    eval/                     harness  baselines  blind  judge  recall_probe  report
    daemon.py, mcp_server.py  daemon on 127.0.0.1:8765 holds scorers and the output log; MCP server is thin stdio, HTTP to daemon only
    feedback/log.py
  skill/quill/SKILL.md        symlinked to ~/.claude/skills/quill/SKILL.md; launchd/ holds com.quill.mlx and com.quill.daemon plists
  tests/                      extractor cases, twin grouping, entity-gate mutations, artifact-gate cases
  eval_reports/, knowledge_base/   aggregate metrics only (no raw text); research notes, decision docs, plan.md

~/.quill/
  legal/                      consent copy, scope.yaml, Fool licence correspondence
  research/2026-11-08/        crawl/ (raw pages, housel.json), simpass/ (similarity pass, profiles, scripts)
  raw/collabfund/             read-only copy of crawl/housel (351 pages); raw/fool/ only if licensed
  corpus/corpus.sqlite  splits/v1/  pairs/v1/  negpool/  eval/neg-v2/
  data/mlx/{sft-v1-s1, sft-v1-s2, pref-v1, mix-*}/
  models/  adapters/{probe-*, sft-*, mix-*, orpo-*, prod -> sft-vN}  logs/  feedback/  audit/
```

Environment: `uv python pin 3.12` (uv-managed, isolated from anaconda; 3.13 is fine if every wheel resolves). Core deps: `mlx-lm[train]`, `mlx-lm-lora`, `mcp[cli]`, `httpx`, `anthropic`, `sentence-transformers`, `transformers`, `torch` (MPS, scorers only), `scikit-learn`, `spacy`, `datasketch`, `datasets` (streamed pulls), `ruptures` (PELT), `faststylometry`, `starlette` + `uvicorn`. Dropped from v1: Presidio, email-reply-parser, Talon.

## 4. Corpus facts and size gates

Measured 2026-11-08 ([housel_augmentation.md](housel_augmentation.md); `simpass/housel_profile.csv`):

| Fact | Value |
|---|---|
| Posts and words | 351 crawled, 342 kept (9 under 120 words dropped, e.g. link lists). 337,898 words of Housel's own text, Sep 2016 to 2026; about 440k tokens at 1.3 tokens per word. |
| Quotes and reuse | 34.5k block-quote words stripped (9.2%). Cross-post 10-gram reuse 6.4%; 12 posts share >30% with another (reposts, book excerpts). |
| Recent output | About 19% of posts are post-2022: 17, 11 and 2 posts in 2024, 2025 and 2026. |
| Shape | 14.7 words per sentence (SD 9.4); 32 words per paragraph; 44% one-sentence paragraphs; 4.1 questions per 100 sentences. |
| Tics per 1k words | "you" 24.3; em dash 5.7; colon 6.1 |
| Within-Housel ceiling | StyleDistance AUC 0.497, Delta 0.753, on random halves (not yet topic-disjoint) |

The two random halves agree on every stylometric feature, so these traits are stable. By his own account about 1% of his writing has been edited by someone else ([How I Write](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)), so the blog is his unedited voice.

Size gates (clean, target-authored, deduplicated words): **T0** under 10k: no adapter ([Eder](https://computationalstylistics.github.io/projects/methodology); [InMyStyle](https://arxiv.org/abs/2607.29238)). **T1** 10-40k: low-data SFT, ≤3 repetitions, preference stage by default ([Panza](https://arxiv.org/html/2407.10994); [DITTO](https://arxiv.org/html/2406.00888)). **T2** 40-100k: rank 16, 2-3 repetitions ([StyleTunedLM](https://aclanthology.org/2024.inlg-main.34.pdf)). **T3** 100k-1M: rank 16 (32 above 500k words), 1-2 repetitions, 12-14B stretch allowed; per-author inverse paraphrasers need >100k words ([Patel et al.](https://arxiv.org/abs/2212.08986)). **T4** over 1M: cap a run at ~1M words. Housel sits in T3, at three times the 100k floor. Volume is not the gap. Coverage of registers he never wrote (memos, technical explainers) is, and no neighbour author fills it. If the Fool licence comes, the set grows to roughly 0.6-0.7M words (estimate) and the adapter moves to rank 32.

## 5. Phases

| Phase | Dev days | Compute on M4 Pro 24 GB | Gate |
|---|---|---|---|
| 0 Source and consent audit | 0.5 (estimate) | minutes | consent stored, scope recorded, counts reproduced |
| 1 Extraction and cleaning | 3.5-4.5 | < 1 h | spot check; AI-text flags decided |
| 2 Splits, eval harness, baselines | 5-7.5 | one night (B1) | metrics sane, ceiling recomputed, B0/B1 scored |
| 2b Negative-signal layer (parallel with 3-5) | 7 | 2-4 h CPU, ~1 h embedding, ~1.25 h paced API | scorers validated on neg-v2 |
| 3 Training pairs | 2-3 | API: hours. Local: 7-11 h (estimate) | curation pass |
| 4 Probes and bake-off | 3.25-4.25 | ~1 night + 3-5 h lexicon v1 | winner beats B1 |
| 5 Housel-only SFT (D0) and ablations | 3.5-5.5 | ~3.1 h per D0 run; ~11 h total (estimate) | beats B0 on dev |
| 5b Neighbour mixture (optional, gated) | 4-6 (estimate) | ~20 h over 2-3 nights | every dilution check passes |
| F Motley Fool archive (only if licensed) | 3-5 (estimate) | similarity pass + one retrain | 2014-16 columns land near the ceiling |
| 6 Inference pipeline (parallel with 3-5) | 3.5-4.5 | minutes | gates and latency pass |
| 7 Preference stage (optional) | 2-3 | 4-8 h | no regression |
| 8 Ship gate | 1-2 + 2 reader sessions | 2.5-4 h (estimate) | Section 6 |
| 9 Serving and Claude Code integration | 2-3 | none | smoke tests |
| 10 Retraining and feedback | 2 setup | 4-5 h per cycle (estimate) | promotion rule |

**Total: about 35-47 dev days** for Phases 0-10, counting Phase 7 as v1 did, and excluding 5b and F. v1 was 25-38. The negative-signal layer adds 11.25 required days (10.75 net of the slop-score port v1 already budgeted): 2.0 in Phase 1, 7.0 in 2b, 1.25 in Phase 4, 0.5 in Phase 5 and 0.5 in Phase 6 ([negative_signal.md](negative_signal.md) §5; [negative_signal_priors.md](negative_signal_priors.md) §5.1). The Housel-specific evaluation adds 1.5-2 days (estimate). The finished crawl and measurements save 2-4 days in Phases 0-1. Optional items add more if they fire: 5b 4-6, F 3-5, M10b 3-4, WQRM gate 2-3, FTPO 2-3, backtracking sampler 3-5, lexicon gate 0.5. Speed assumptions: 100-200 tok/s for 8-9B QLoRA training and 30-50 tok/s decode at 4-bit, both estimates (notes silicon Q2/Q5). The one measured M4 Pro anchor is llama.cpp LLaMA 7B Q4_0 at 50.7 tok/s decode ([llama.cpp #4167](https://github.com/ggml-org/llama.cpp/discussions/4167)). Training time ≈ target tokens × repetitions × 2.3 (prompt + target) / 150 tok/s. Housel's ~280k training words at 2 repetitions give ~3.1 h.

### Phase 0: Source and consent audit

**Status 2026-11-08: done, except the consent copy.** `uv run quill audit` reproduces every figure (351 pages, 342 kept, 337,898 words, 34,503 quote words, 12 twin posts, 19% post-2022) and writes `~/.quill/audit/inventory.json`. Pages sit read-only in `~/.quill/raw/collabfund/pages/`. `~/.quill/legal/scope.yaml` records the scope: storage, training, Claude API and Lamade are yes; new posts and outputs leaving the Mac are unknown. Its `copy` field stays `pending` until the consent document is saved there. Phase 1 cases are in `tests/cases/phase0_extraction.md`.

The crawl (351 pages), the cleaning measurements and the similarity profile were done on 2026-11-08. Deliverables: `~/.quill/legal/` (consent copy, `scope.yaml`), `~/.quill/raw/collabfund/` (read-only pages plus `housel.json`: file, year, words, quote words, author), `~/.quill/audit/inventory.json`, and a decision record in `configs/quill.yaml`.

Steps
1. Store the consent in `~/.quill/legal/`. Record its scope in `scope.yaml`: grantor, date, and yes / no / unknown for each use. The uses are storage, training, sending text to the Claude API (pairs, B0, judge), Ted Lamade's essays, new posts, and outputs leaving the Mac. An "unknown" blocks the step that needs it.
2. Record source status: collabfund.com robots.txt (404 on 2026-11-08), the Feb 2026 Terms of Use, and the consent reference.
3. Copy without re-fetching: `cp -R ~/.quill/research/2026-11-08/crawl/housel ~/.quill/raw/collabfund && chmod -R a-w ~/.quill/raw/collabfund`.
4. `uv run quill audit --raw ~/.quill/raw/collabfund` must reproduce 342 kept posts, 337,898 words, 34.5k block-quote words and 12 twin posts. Explain any mismatch before Phase 1. Read 20 random raw pages and log extraction problems (bylines, "Copy Link" chrome, book promos, subscribe blocks) as Phase 1 test cases.
5. If the user agrees (8.3), send the Motley Fool the written licence request in `drafts/fool_licence_request.md` (not yet sent; it asks for 2012 to August 2016 columns). It costs no compute and can run while D0 trains.

Exit gate
- Consent copy stored. Storage and training are in scope. If training is not: stop and fall back to McKenzie (Kalzumeus 2011+, [style_library.md](style_library.md)).
- API scope known before Phase 3. Lamade scope known before his passages enter the impostor pool or Phase 5b. Counts reproduce.

### Phase 1: Extraction and cleaning

**Status 2026-11-09: done; `uv run quill gate` passes.** `uv run quill ingest` writes `~/.quill/corpus/corpus.sqlite` and `cleaning_report.md`: 330 posts, 318,971 words, 835 chunks, tier T3. `uv run quill aicheck` writes `~/.quill/lexicon/v0.json` and `~/.quill/corpus/ai_flags.md`: 5 of 61 post-cutoff posts flagged, no sustained shift; all 5 kept, with notes (`quill flags`). The 2026-01-06 post is reviewed again when M10 exists. Spot check: Claude read the samples, not the user. Sample 1 (seed 1) had 4 bad chunks in 100 and failed. The causes were fixed. Sample 2 (seed 2) had 3 and passes at the limit; those 3 were fixed too. A read by the user is still worth doing before Phase 3.

Differences from the steps below, all in `configs/quill.yaml` or `configs/lexicon/seed_v0.yaml`:
- The reader is built for the Collab Fund layout (`section.longform`), not the 70% heuristic. `quill audit` keeps the Phase 0 reader.
- Dropped whole: 3 book announcements, 1 podcast transcript, 5 interviews (the guest's words). Paragraphs that are one whole quotation go with the block quotes, as do epigraphs and embedded tweets. Quotations set as plain paragraphs with no marks cannot be detected; the ones found by reading are listed in `corpus.unmarked_quotes` (5 posts). More remain.
- 39% of chunks hold a lead-in whose quote or image was removed ("X writes:"). They carry `dangling_leadin`. Decided: `chunks.text_marked` puts a `<QUOTE>` or `<IMAGE>` line at each gap (298 and 87 chunks) and Phase 3 trains on it; `chunks.text` stays the author's words only, and every scorer uses that, so the markers cannot become a tell.
- Kobak words more common than 0.1 per 1k in general English are left out (the list includes "this"). Pattern baselines use the pre-2023 impostor passages; word baselines use wordfreq.
- A link with `utm_source=chatgpt.com` raises `llm_link` (one post, 2026-01-06).
- Bold and italics are not kept. slop-score's 35 POS patterns are not ported.

Deliverables: `corpus.sqlite` with table `posts` (url, date, title, byline, fetch date, consent ref, words, kept/dropped reason, twin_group) and table `chunks` (id, post_id, twin_group, words, length_bucket, text, flags); a cleaning report; unit tests from the Phase 0 cases; seed lexicon v0; the reviewed AI-text flag list.

Steps
1. Extract. Port `simpass/scripts/textlib.py` (stdlib `html.parser`), which produced the measured corpus. Keep `p` and `li` text from the deepest container holding ≥70% of paragraph words. Drop `blockquote`, `pre`, `code`, `table`, `figure`, `figcaption`, nav, header, footer, aside and form, and classes such as share, newsletter, subscribe, byline, meta, related and footnotes. Drop footnote markers, link-heavy short paragraphs and paragraphs repeated in ≥max(3, 10%) of posts.
2. Strip Collab-specific furniture: bylines, "Copy Link" chrome, book promos and subscribe boilerplate. Replace code with `<CODE>`. Keep only posts whose author field is Morgan Housel.
3. Drop near-empty posts: under 120 words after cleaning.
4. Handle twins. Posts that share >30% of 10-grams get one `twin_group` (12 posts on 2026-11-08). MinHash over paragraphs (datasketch, 5-gram shingles, Jaccard ≥ 0.85) keeps one copy of each repeated paragraph, so no passage trains twice **[P]**. Twins always share a split.
5. Chunk on paragraph boundaries into 150-800-word pieces (≤1,024 target tokens). One register: essay. Tag each chunk with a length bucket (**[P]** 150-300, 300-500, 500-800).
6. AI-text check on the ~19% of posts dated after 2022.
   - Seed lexicon v0: Wikipedia "Signs of AI writing" vocabulary and structures from all eras, Kobak excess words, and slop-score's "not X, but Y" regex. Drop slop-score's word and trigram lists (mostly fiction vocabulary) and the Signs page's "ineffective indicators". Whitelist any word, name or pattern Housel's pre-2022-12-01 text uses at or above a pre-2022 general baseline; his names and his em dashes (5.7 per 1k) stay exempt. Flag posts above the 95th percentile of his pre-2022-12-01 text.
   - Changepoint check: build a pre-2022 centroid of function words, punctuation rates and the sentence-length distribution. Score each later post's distance, run PELT, and flag only sustained shifts after 2023-03 ([negative_signal_priors.md](negative_signal_priors.md) item 1). Also look for quoted LLM output.
   - The user reviews all flags together, with M10 once it exists. Never auto-drop.
7. Light PII pass: regex for email addresses and phone numbers only. The text is published essays and runtime is local, so v1's Presidio stack and reversible pseudonymization are gone. Expect zero hits; review any.
8. Log Housel's own tell rates (em dash, colon, contrast constructions, tricolons, parentheticals) for the lexicon whitelist.

Time and compute: 3.5-4.5 dev days. Extraction and cleaning take 1.5-2.5 (estimate; the extractor exists). The AI-text check takes 2.0 (lexicon seed 1.25, filter 0.25, changepoint 0.5). CPU minutes.

Exit gate: 100 random chunks hold ≤3 with leftover quote, byline, chrome, promo or subscribe text. Word counts match 337,898 or the difference is explained. Tier T3 confirmed. Every AI-text flag reviewed and decided.

### Phase 2: Splits, eval harness, baselines (before any training)

**Status 2026-11-09: splits and the model-free half of the harness are built.** Results: `eval_reports/phase2-sanity.md`.
- Done: frozen split v1 (`uv run quill split`; the post-to-split map is hashed, chunk ids derive from it); impostor pool from the cached similarity-pass passages; M1, M2, M5 (regex only), M6, M7, M8, M9, M12, M15; `uv run quill eval --sanity` and `--system human|impostor|llm|<name>`; the topic-disjoint ceiling.
- Sanity on dev: M1 AUC 0.994 (ceiling accept 93.5%, impostors 3.3%); M2 classifier AUC 0.994; M6 and M8 pass. Ceiling: StyleDistance AUC 0.54 at n=60, Delta 0.765.
- M15 fails sanity: FS, Naval and the LLM class are called the author on over 20% of passages. Each has about 10k cached words or fewer. It needs B0 outputs for the LLM class and more FS and Naval text, or it is dropped.
- The tic profile's reference pools are drawn inside one topic cluster. With pools mixed across topics, the held-out advice cluster failed on "you" (43.6 vs 22.5 per 1k).
- Not built on 2026-11-09: M3, M4, M10, M11, the decision composite, spaCy NER, the blind kit, the coverage probe. All were built on 2026-11-10 (below).

**Status 2026-11-09, baselines on dev.** Decisions: Claude runs through scripted `claude -p` (Sonnet 5.5 for facts and briefs, Opus 5.5 for drafts, the style guide and B0); the base model is Qwen3.5-9B, 4-bit MLX. Reports: `eval_reports/{b0,b1,b2}-dev.md`, `recall-probe-base-dev.md`.
- Done: frozen eval inputs v1 for dev and test (`uv run quill inputs`); B0, B1, B2 on dev (`uv run quill baseline`); the base recall probe (`uv run quill recall`). The reranker is a stand-in: gates on M5, M12, M9 and chat artifacts, then M2 delta. Test baselines are not run.
- M1 accept on dev: ceiling 93.5%, B0 47.4%, B1 32.4%, B2 (the plain draft) 32.1%, impostors 3.1%.
- **The M1 floor is too high.** The verifier accepts a third of plain drafts because they carry the author's content. Read M1 against B2 until the verifier is retrained with drafts of train chunks as negatives (about 690 generations; Phase 3 makes them anyway).
- B1 adds nothing over the draft on M1. B0 is a caricature: sentence length 9.9 words against 14.7 (z = -3.6). B1 writes almost no em dashes (z = -2.6) and has flat sentence lengths (SD z = -3.5).
- Fallback at N=4: B0 17.7%, B1 25.8%. B1 misses length on 44% of candidates.
- M9: outputs rebuild the held-out target because the facts pin the content (B0 median 10-word span against its own target). In eval the target's post is exempt from the gate and reported apart. Against other corpus text: B0 9 of 124 flagged (max 14), B1 2 (max 9).
- Recall probe, untuned base, 186 prompts: max span 12 words; 15 at or over the 8-word gate (summary 5, paraphrase 6, opening 4); median 0. This is the H8 baseline.
- **Verifier check 2026-11-10** (`uv run quill eval --verifiers`; `eval_reports/verifier-check-dev.md`, `verifier-check-drafts-dev.md`). Topic words are not the cause: masking content words (Stamatatos distortion) raised draft accepts to 44-56%. The cause is the negative set: no scorer had seen LLM text on the author's content, and drafts sit between the impostors and the author. Zero-shot draft accepts: M1 35%, StyleDistance classifier 10%, LUAR classifier 28%. With drafts of other dev posts as negatives (4 folds, an estimate): M1 6%, StyleDistance 1%, LUAR 10%; author accepts 88-99%. So the fix is draft negatives from train chunks, for any feature set. The scorers disagree on B0 (24%, 45%, 81%), so report M1 and the StyleDistance classifier side by side; LUAR is the most lenient. M3 is built (local copy of LUAR-MUD, CPU, episodes of 8 token windows).
- **Verifier retrained 2026-11-10** with plain drafts of all 688 train chunks (933 passages; `uv run quill inputs --train-drafts`) as negatives for M1, the M15 LLM class and the M2 LLM centroid. Dev M1 accept: ceiling 94.8%, B0 23.7%, B1 1.6%, B2 0.0%, impostors 5.0%. StyleDistance classifier accept (same 5% rule): ceiling 98.7%, B0 44.2%, B1 2.2%, B2 0.0%. M1 AUC vs impostors 0.993. These replace the M1 and M15 figures above. M15 no longer calls LLM text the author (B0 10%, B1 3%, B2 0%); it still fails sanity on FS and Naval, which have 6 and 8 dev passages. The reranker's M2 centroid changed, so B0's fallback is now 16.1%.
- **Phase 2 closed 2026-11-10; exit gate passes on dev** (`uv run quill eval --report`; `eval_reports/baseline-v2.md`). The test split is untouched: test baselines run once, with the finalist, in Phase 8.
  - M4 built. `restyle`: MIS on ~110-word input windows, each against its best nearby output span (identical text 0.95, B0 0.94, B1 0.81, mismatched pairs 0.02). `write`: share of the chunk's facts entailed (DeBERTa-v3 MNLI; originals 1.0, mismatched 0.18). MIS costs about 2.5 min per system on dev, cached.
  - M5 uses spaCy NER (`en_core_web_sm`) only to rescue names seen at a sentence start, and never for words that occur in lower case in the train texts. Left free, NER tagged "Luck" and "Vanity" as names and raised B0's fallback from 16% to 24%.
  - M15 classes are now {author, Lamade, other humans, LLM}; FS and Naval had 6 and 8 dev passages. It passes sanity (author 88.3% on author; no class called author over 20%).
  - Decision composite built: geometric mean of M1 accept, M15 author share and M4, with entity-gate failures scored 0; bootstrap over chunks; `uv run quill eval --compare A B` gives the paired difference. Dev: B0 0.25 [0.17, 0.33], B1 0.06 [0.00, 0.10], B2 0. B0 - B1 = +0.19 [0.11, 0.29].
  - M10 fails sanity and is dropped: Fast-DetectGPT with gpt-neo-2.7B scores B0, B1 and plain Opus drafts as human as the author (AUC 0.50, 0.49, 0.40; `eval_reports/m10-dev.md`). It still flags the older Claude controls (0.91). M10b stays a Phase 2b decision. The Phase 1 flag review "with M10" cannot use it.
  - M11 judge built and valid (`uv run quill judge`; Sonnet 5.5, both orders, consistent picks only): real over impostor 40/40. Real over B0 32-1 with 7 inconsistent; real over B1 40-0; B0 over B1 40-0. $3 per run.
  - Blind kit built (`uv run quill blind --test A|R --system NAME`): frozen, length-matched, quotes and whitespace normalized, one chunk per post first, resumable, logs reason and recognition, reports the one-sided binomial p. Dev kits exist as a smoke test; nobody has read them.
  - Coverage probe built (`uv run quill baseline b1 --split coverage`): style metrics plus topic drift toward the nearest author topic centroid, threshold at the dev 95th percentile. **Not run: it needs 30-50 briefs from the user** at `~/.quill/eval/coverage/briefs.jsonl`.
  - The stand-in reranker still ranks on style only; M4 joins it in Phase 6.
- Base model: 29-48 tok/s, 7.0 GB peak. B1 took 2.9 h for 496 generations.

Deliverables: frozen splits `~/.quill/splits/v1/{train,dev,test}.ids` with a recorded hash, built before any neighbour training text is pulled; frozen eval inputs for each dev and test chunk (a brief + facts for `write`, a Claude generic draft for `restyle`, made with the Phase 3 prompts); `uv run quill eval --system <name> --split dev|test`, writing JSON and a markdown table to `eval_reports/`; the impostor pool, calibrated scorers, recall-probe baseline, B0/B1 results and blind kit.

Split rules
- Embed every post with a content (topic) encoder, not a style encoder, and cluster the posts (k ≈ 15). Hold out whole clusters: about 10% of words for test (≈34k words, roughly 60-100 chunks) and about 7% for dev. Whole posts and whole twin groups stay together. Held-out topics control topic leakage in style metrics ([Wegmann et al.](https://arxiv.org/abs/2204.04907)).
- Pick checkpoints on dev. Touch test once per finalist.
- Recompute the within-Housel ceiling (StyleDistance AUC, Delta) on topic-disjoint halves. Expect it above the random-half 0.50.
- Coverage probe: 30-50 real briefs from the user's PM work. No reference text exists. Score them with style metrics and a topic-drift classifier that catches drift toward Housel's pet topics.

Metrics

| # | Metric | Implementation | Use |
|---|---|---|---|
| M1 | AV accept rate | Char 3-5-gram TF-IDF (top 10k) + logistic regression, Housel train vs impostors ([Jemama & Kumar](https://arxiv.org/abs/2509.24930)). ModernBERT-base on MPS if AUC < 0.90. Report the held-out ceiling, the impostor floor and each system. | Decision |
| M2, M3 | StyleDistance delta; LUAR | cos(output, Housel centroid) minus cos(output, generic-LLM centroid) ([StyleDistance](https://arxiv.org/html/2410.12757)); `rrivera1849/LUAR-MUD`, episodes of 8, topic-leaky ([LUAR card](https://huggingface.co/rrivera1849/LUAR-MUD)) | Diagnostic |
| M4 | Meaning | MIS `s-nlp/Mutual_Implication_Score` for `restyle` ([MIS](https://huggingface.co/s-nlp/Mutual_Implication_Score)); per-fact MNLI entailment for `write` | Decision |
| M5 | Entity preservation | spaCy NER + regex for names, numbers, money, dates, URLs; normalization rules; mutation tests | Hard gate |
| M6 | Stylometry | Tic profile: per-feature z against Housel held-out text for sentence length mean and SD, paragraph length, one-sentence share, "you", em dash, colon, semicolon, parentheses, questions, MATTR; pools ≥2,000 words. Burrows' Delta (faststylometry) on the same pools. | Tic profile: soft + alarm. Delta: diagnostic only |
| M7 | Lexicon rates | Hits per 1k words against Housel's held-out rate, per family: vocabulary, structure, artifacts, Claude (Phase 2b) | Soft |
| M8 | Signature-phrase ratio | Top-50 Housel-distinctive n-grams (log-odds vs impostors); output rate / held-out rate | Soft |
| M9 | Memorization | Longest verbatim span shared with the whole Housel corpus (train, held-out and dropped text). Flag ≥8-10 words; set the exact length on dev **[P]**. Spans that also appear in the input are exempt **[P]**. | Hard gate |
| M10 | Detector | Fast-DetectGPT with gpt-neo-2.7B, threshold at 5% FPR on Housel held-out text; validated on neg-v2. Binoculars needs ~28 GB and does not fit. | Diagnostic |
| M11 | Frontier judge (optional) | Claude, pairwise, both orders, consistent wins only; must pick real over impostor ≥75% on dev first. Local 8B judges scored below chance ([Jangra et al.](https://arxiv.org/html/2508.06374v4)). | Diagnostic |
| M12 | Length adherence | Within ±30% of the requested length | Gate |
| M13 | Corpus AI share α | Liang's estimator; P = Housel held-out, Q = B0 and B1 outputs (Phase 2b) | Soft |
| M14 | Claude residue | Drafter-probe AUC on outputs plus residue ratio R (Phase 2b) | Soft |
| M15 | 5-way attribution | Classes {Housel, Lamade, FS, Naval, LLM}; the LLM class comes from the Claude controls and B0 outputs. Reports Housel share and neighbour share. | Decision |

**Decision composite:** the geometric mean of (M1 accept rate, M15 Housel share, M4 MIS), with the entity gate applied first. A collapse on any axis sinks the score ([TinyStyler](https://arxiv.org/html/2406.15586)). It ranks Phase 4 candidates, picks Phase 5 checkpoints and decides Phase 5b. `housel_augmentation.md` proposes it for the mixture decision; using it throughout is **[P]**.

**Why StyleDistance and Delta only diagnose.** They selected the neighbour authors, so they cannot judge a mixture of them. Delta also passes caricature. Claude writing as Housel from memory is perfectly separable from him on StyleDistance (AUC 1.000; centroid cosine 0.866, the lowest of any row), yet its Delta of 1.044 beats 18 of the 20 human candidates. It writes 9.6-word sentences and 23-word paragraphs, uses no em dashes, semicolons or parentheses, and overshoots "you" (32.4 vs 24.3 per 1k). Delta can never be a ship metric on its own. The tic profile catches exactly these errors.

Metric sanity check (as [Baumler et al.](https://arxiv.org/html/2604.24444) did for LUAR): on dev, each style metric must rank Housel's held-out text above same-register impostor text. AV AUC ≥ 0.90; embedding AUC ≥ 0.80. A failing metric is dropped.

Impostor pool (close but separable is exactly what a verifier needs):
- Cached passages of the 20 similarity-pass candidates, with McKenzie as the distant control. Lamade joins only if the consent covers him. Exclude Richards (authorship unverified) and Zweig (WSJ reprints). If Phase 5b runs, hold out about 20% of each neighbour's passages for this pool.
- The Claude controls (imitating Housel; default prose), plus B0 and base-model outputs on train inputs. These also form M2's generic-LLM centroid. Optional (0.25 d): 2,000 pre-2022 FineWeb Finance & Business nonfiction documents, so the verifier cannot score finance vocabulary as Housel.

Baselines and recall probe
- **Recall probe,** before any training: prompt the untuned base with held-out summaries, neutral paraphrases and opening lines. Record the longest verbatim spans against the Housel corpus. The adapter must not raise them (H8).
- **B0, the bar:** Claude prompted to write like Housel, plus a one-page style guide and 5 exemplars, plus the same N=4 sampling and reranker. Claude writes the guide from 30 train chunks; then it is frozen. Exemplars are random within the length bucket; going from 2 to 10 shots changed little in [Catch Me If You Can](https://arxiv.org/html/2509.14543v1). Score B0 as specified. The from-memory probe had no guide or exemplars, so it says nothing about B0's strength. Claude only: ChatGPT refuses named-author style requests ([TNW](https://thenextweb.com/news/chatgpt-refuses-author-style-imitation-copyright)).
- **B1:** the untuned base with the B0 prompt. It measures what the adapter adds. The same model is the `write` drafter.
- **B2:** the input itself. Floor.

Blind kit: `uv run quill blind --test A|R --n 40` builds shuffled, length-matched pairs with whitespace and quotes normalized. It records each answer, a one-line reason, and whether the reader recognized the passage **[P]**, then reports the binomial p. Reasons feed the tic-profile and lexicon checks.

Time and compute: 5-7.5 dev days: v1's 4-6, minus the slop-score port (~0.5, now in Phase 1), plus the topic split and ceiling (0.5), the recall probe (0.5), and M15 with the tic profile (0.5-1); the additions are estimates. AV classifier: minutes. B1 at N=4: ~150 dev and test chunks × 2 ops × 4 × ~600 tokens ≈ 0.7M tokens ≈ 4-6.5 h at 35 tok/s (estimate), overnight.

Exit gate: AV AUC ≥ 0.90 on dev. M15 and the embedding metrics pass sanity or are dropped. Topic-disjoint ceiling and split hash recorded. B0 and B1 scored. Report saved as `eval_reports/baseline-v2`.

### Phase 2b: Negative-signal measurement layer

Measure first, gate rarely, never reward. No scorer gates or decides anything until it passes validation here. Sources: [negative_signal.md](negative_signal.md) §5-6 and [negative_signal_priors.md](negative_signal_priors.md) §4-6. Runs in parallel with Phases 3-5.

Steps
1. **Harvest** the negative pool into `~/.quill/negpool/`, local only, with a provenance table (source, URL, date, licence, label, labeling-function votes, model version where known).
   - WildAI `ai`, `human` and `mixed`: 20k + 20k for mining and 3,000 for neg-v2. Keep FineWeb-source documents of 300-3,000 tokens in informational formats, Personal Blog and Nonfiction Writing among them, in Housel's topics (Finance & Business first; the rest set from a topic classifier over his posts **[P]**). Match AI to Human by dump, format, topic and length. Cap 20 per domain and split by domain.
   - FineWeb 2021-22, dated before 2022-12-01: 20k human controls; 2021 dumps for FPR calibration. Claude Code PRs with the literal footer, 20k + 1,000; pre-2023 human PRs, 20k + 1,000 (needs a GitHub token; ask first). LMArena Claude answers against No Robots human answers.
   - Gold and pairs: a 300-page Wikipedia {{AI-generated}} sample with human predecessors, Human Detectors (300), Beemo informational rows (1,602), LAMP nonfiction (311), 500 Grokipedia-to-Wikipedia-20220301 paragraph pairs (pilot 200 articles first) and 2,000 WildAI-monthly 2025-26 documents.
2. **Lexicon v0, final.** Report three families per 1k words against Housel's held-out rate: vocabulary; structure (contrast and "rather than" parallelisms, copula avoidance such as "serves as", trailing significance "-ing" clauses, tricolons, "In summary / Overall" closers, bold-lead bullets, participial-clause and nominalization rates); artifacts. Add two mined families. Informational: WildAI AI against same-dump WildAI Human and against pre-2022 FineWeb. Claude: Claude Code PRs against pre-2023 human PRs, and LMArena Claude against No Robots. A Claude tell enters only when two contrasts agree: Phase 3 Claude drafts against Housel (same content), and October 2026 Claude PRs against pre-2023 PRs (current model). **Two-control rule:** keep a pattern only if ρ ≥ 1.5 **[P]** against both controls, and only if it is over-represented in ≥3 of {WildAI, Claude PRs, Grokipedia, Wikipedia tagged sections, quill outputs}. Exclude nouns and named entities from mining. The Housel whitelist from Phase 1 applies.
3. **neg-v2** (~10k items, `~/.quill/eval/neg-v2/`, frozen): neg-v1 (Wikipedia tagged sections and predecessors, Human Detectors, Beemo, LAMP; ~2.3k) plus 1,000 + 1,000 WildAI matched pairs, 1,000 WildAI Mixed as a hard class, the Grokipedia pairs, 1,000 + 1,000 Claude and pre-2023 PRs, and the 2,000 WildAI-monthly documents.
4. **Validate.** Each M7 family must reach AUC ≥ 0.80 on Human Detectors and on Wikipedia tagged-vs-predecessor sections, reported per source. It must rank Beemo expert edits above raw outputs on most pairs, and flag ≤5% of Housel's held-out pre-2022 paragraphs at its gate threshold. Report the same AUCs for M10. A failing family leaves the soft criteria.
5. **M13, corpus α.** P = Housel held-out text; Q = B0 and B1 outputs on the same inputs. Validate to ≤3 points error on 0-25% synthetic mixtures. Report per system with bootstrap CIs. α reads adjectives, so a near-zero α says nothing about structure; report it beside M6.
6. **M14, Claude residue.** Train a word and char n-gram probe to tell Claude drafts from local drafts on held-out raw drafts; it needs AUC ≥ 0.90 **[P]**. Run it on restyled outputs grouped by drafter. Add the residue ratio over the Claude family: R = (f_output − f_Housel) / (f_draft − f_Housel), where 0 means removed and 1 means untouched.
7. **Over-correction alarm**, run on every suppression step (lexicon gate, sampler, ORPO, FTPO). MATTR stays within 5% of its pre-step value. Tic-profile punctuation and sentence-length SD stay within pooled |z| ≤ 2 of Housel. A diff of the top-50 over-represented n-grams fails the step if any new entrant exceeds 2× Housel's rate.
8. **M10b, gated.** Trigger: Fast-DetectGPT fails AUC ≥ 0.80 on neg-v2's WildAI pairs or on Human Detectors. Expect it to fire: Fast-DetectGPT caught 23.3% of humanized nonfiction. Then train a local classifier on WildAI plus anchors and constructed sets, needing AUROC ≥ 0.85 on held-out sources, with its threshold at 5% FPR on Housel held-out text. A WildAI-distilled classifier inherits Pangram's blind spot (Pangram caught 3% of author-fine-tuned outputs). So it stays a diagnostic: never a reward, never a rerank gate, never a certificate.

Time and compute: 7 dev days (neg-v1 1.5, neg-v2 1.0, mined families 2.0, M13 1.0, M14 1.0, alarm 0.5). 2-4 h of CPU n-gram counting, ~10-20 GB streamed (estimate), ~1 h embedding, ~1.25 h of paced Wikipedia calls. M10b adds 3-4 days if it fires. Exit gate: every M7 family, M10, M13 and M14 validated or dropped. Results saved to `eval_reports/neg-v2`.

### Phase 3: Training pairs

**Status 2026-11-10: pairs built; the automatic gate passes; the hand check of 50 pairs is not done.** `uv run quill pairs` writes `~/.quill/pairs/v1/{raw,curated}.jsonl`, `~/.quill/data/mlx/sft-v1-{s1,s2}/` and `eval_reports/pairs-v1.md`.
- Train: 688 chunks. Form A keeps 675 (98.1%), form B keeps 641 (93.2%), both forms 637 (92.6%; the gate is 85%). Dev: A 62 of 62, B 59 of 62; dev rows are `valid.jsonl`. Four chunks exceed 2,048 tokens and are dropped, not re-chunked.
- Generator: Sonnet 5.5 paraphrases the marked chunk. Form B reuses the Opus train drafts from the verifier retrain. `sft-v1-s2` holds Claude drafts only until Phase 4 step 9 adds the local half.
- Markers: the target is `text_marked`. The paraphrase keeps each `<QUOTE>`/`<IMAGE>` line. For drafts, Claude names the paragraph each marker follows and the code inserts it, so the input always carries the target's markers.
- Closure is tolerant of form (numbers as words, percent signs, list numbers, idioms such as "a 180", acronyms, capitalized ordinary words). Without that it failed 34% of pairs, almost all false alarms.
- Retry: a failed input is regenerated once with the lost items named in the prompt (form B rebuilds the fact list first). It replaced 76 paraphrases and 79 drafts. The usual real loss: Claude drops figurative numbers ("100% confident") when told to remove figures of speech.
- Inputs are plain: on dev the verifier accepts 7.7% of paraphrase passages and 0% of draft passages (targets 94.8%). Targets are verbatim in every row (checked in code). No test chunk is in the pairs.
- `template.py` maps the two under-150-word chunks to the `150-300` length tag.
- Cost: $21.89 (paraphrases and marker placement $13.21, retries $8.68).

Deliverables: `~/.quill/pairs/v1/*.jsonl` (all variants, with provenance and the generator's model id per pair); `~/.quill/data/mlx/sft-v1-s1/` (form A) and `sft-v1-s2/` (form B) in mlx chat format, which `housel_augmentation.md` calls `mix-a000-s1/s2`, with Housel-only dev chunks in `valid.jsonl` for loss monitoring; a curation report.

| Form | Op / input tag | Generator | Teaches |
|---|---|---|---|
| A: neutral paraphrase | `restyle` / paraphrase | Data-prep LLM | Surface style: lexicon, punctuation, rhythm |
| B: generic assistant draft from the fact list | `restyle` / draft | Half Claude (pinned to the session model, id recorded), half the Phase 4 winner's untuned base | Removing assistant voice; matches both runtime inputs |

- **Fact lists** are made per chunk. They feed the drafts and the fact-closure check. They are not a training input.
- **Dropped forms.** v1's brief + facts and facts-only forms are gone (2.3). Reintroduce brief-to-text pairs only if the recall probe stays clean (A7). Briefs are still made for dev and test `write` inputs.
- **Drafter mix.** Keep at least half of form-B inputs Claude-drafted. The neutralizer should differ from the deployment drafter or be diversified (notes data Q1), and restyle training should match deployment drafts (Q7). The half-and-half split does both.
- **Order [P].** Make form A, the fact lists and the Claude drafts now. Make the local half of form B after Phase 4 picks the winner, so the training drafter is the runtime `write` drafter. The bake-off trains on form A only.
- **Prompt sketches** (`configs/prompts/`): paraphrase ("Rewrite in plain, neutral English. Keep every fact, name, number, date and link, in order. Remove personal style: standard punctuation, no slang, no idioms."); facts ("List every fact, claim, name, number, date and link as terse bullets. Reuse names and numbers only."); draft ("Write this as a helpful assistant would, from these facts."); brief, dev and test only ("Write the 1-3 sentence request a person would type to get this text written.").

mlx chat line (one per pair):

```json
{"messages": [
  {"role": "system", "content": "quill v2\nop: restyle\ninput: draft\nlength: 300-500\nvoice: v0"},
  {"role": "user", "content": "<generic draft>"},
  {"role": "assistant", "content": "<Housel's original, verbatim after cleaning>"}
]}
```

`voice: v0` is constant in D0. It keeps the template byte-identical if Phase 5b adds neighbour tags **[P]**. `--mask-prompt` trains the assistant turn only. Prompt loss barely matters for long completions ([Huerta-Enochian & Ko](https://arxiv.org/html/2401.13586v2)), but masking is still required: the prompt holds LLM-written text, and loss on it would train the assistant voice.

Curation (drop or regenerate)
1. Fact closure: every entity, number and date in the target appears in the input. Missing facts teach invention ([codebyandy](https://github.com/codebyandy/finetune-me); [zwischenzugs](https://zwischenzugs.com/2025/11/04/fine-tuning-an-ai-part-i/)).
2. MIS(input, target) ≥ 0.7 ([TinyStyler](https://arxiv.org/html/2406.15586) filter). No near-copies: normalized edit similarity ≤ 0.85. Input length 0.5-2× the target.
3. Rendered length ≤ 2,048 tokens. mlx-lm truncates from the end and would cut the target, so re-chunk instead.
4. Never rewrite the target side ([Back-and-Forth](https://arxiv.org/abs/2408.04614) rewrites responses; that would erase the voice). No harvested AI text on either side.

Time and compute: 2-3 dev days. About 3 generations per chunk at ~600 tokens. Train holds roughly 500-800 chunks (derived from 60-100 test chunks per 34k words). API via Message Batches: hours. Local only, if the API is out of scope: ~0.9-1.4M tokens ≈ 7-11 h at 35 tok/s (estimate), overnight. The local half of form B after Phase 4: ~2 h (estimate).

Exit gate: ≥85% of train chunks keep both forms after curation. Hand check of 50 pairs: facts closed; inputs free of Housel's tics; targets verbatim.

### Phase 4: Probes and model bake-off

**Status 2026-11-10: Qwen3.5-9B fails the day-1 probe; the base is now Qwen3-8B, 4-bit (user decision).** Training Qwen3.5-9B with mlx-lm 0.32.2 runs out of memory from about 1,000 tokens, with gradient checkpointing on, and reaches 20 tok/s where it fits. Its Gated DeltaNet layers have no gradient through the Metal kernel, so training falls back to a per-token loop. Details: [logbook.md](logbook.md). `--iters` counts micro-batches; the optimizer and schedule step once per accumulation. The chat template renders the same at training and inference with thinking off. B1 and the recall probe are rerun on the new base. Config: `configs/train/sft.yaml`.

**Status 2026-11-11: stage 1 on Qwen3-8B passes the bake-off gates on dev.** Adapter `sft-v1-s1p` (form A, input paragraphs merged in part of the rows, one pass). Composite at N=4 with rerank: 0.508 [0.44, 0.57]; +0.252 [+0.159, +0.346] over B1 on the same base; +0.256 over B0. Training peak 12.84 GB. Decode 27-28 tok/s with the adapter loaded. Fusing back into 4-bit erases the adapter (composite 0.098); fused with `--dequantize` and quantized to 6-bit it holds style (N=1 composite 0.655) at 30.2 tok/s and 7.4 GB. Recall probe: 3 prompts at or over the gate, max 9 words (base: 4, max 9); 31 paraphrase prompts rebuild a span of the item's own held-out post, which H8 no longer counts. Entity failures came from the `write` drafter, not the adapter; a draft retry that names lost items brings N=4 to composite 0.681 [0.61, 0.74], entity pass 92.7% and fallback 10.5% (H9 limit 15%). Details: [logbook.md](logbook.md).

Candidates (notes silicon Q4)

| Candidate | Why | Caveats from the notes |
|---|---|---|
| Qwen3.5-9B instruct, 4-bit (plus an 8-bit probe) | Top of its size class on the AA index; base released; Apache 2.0. A switch to Qwen3 8B "improved the output more than any hyperparameter tweak" ([Griffiths](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na)) | Multimodal: the 4B crashed MLX LoRA until vision weights were stripped; thinking template broke chat formatting ([sciences44](https://github.com/sciences44/mlx-lora-finetune)); larger quantization loss; Gated DeltaNet LoRA support unconfirmed |
| Ministral 3 8B instruct, 4-bit | Base, instruct and reasoning variants; Apache 2.0; dense | mlx-lm support and `model_type` unverified; older Ministral "inconsistent" for one practitioner |
| Gemma 4 E4B-it, bf16 LoRA | Fast iteration; no quantization loss; ~7.9 GB peak reported | Only report trains via `mlx_vlm.lora`; fused checkpoint failed; mlx_vlm server dropped adapters (#907) |
| Fallback: Qwen3-8B, 4-bit | Only model with an M4 Pro 24 GB training figure: ~6-10 GB peak at 4k context, self-reported ([mlx-lm-lora](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora)) | Older |
| Reserve and stretch | OLMo 3 7B in reserve. Gemma 4 12B or Ministral 3 14B in QLoRA at ≤1,024 tokens | Stretch only if the 8-9B winner fails the ship gate on style |

Steps
1. Verify HF repo ids, licences and vision weights (8.2). Convert with `uv run mlx_lm.convert --hf-path <repo-id> --mlx-path ~/.quill/models/<name>-4bit -q --q-bits 4`. QLoRA turns on when `--model` is quantized ([LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)).
2. Settle what `--iters` counts: run a 32-iteration probe and count the examples consumed. A wrong reading runs 16 passes instead of one.
3. Probe each candidate for 30 iterations (`--iters 30 --steps-per-eval 1000 --adapter-path ~/.quill/adapters/probe-<name>`) at batch 1, seq 2048, all layers, grad checkpointing, with `mlx_lm.server` stopped. Record peak memory and tok/s. Read the adapter safetensors keys to confirm MLP projections are adapted.
4. Template check: render one example through the chat template. Confirm no thinking tags and that inference renders the identical string. Template mismatches caused early failures ([Lopes](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts)).
5. Bake-off SFT: one pass over the form-A rows, same config for every candidate.
6. Dev eval at N=1, ranked on the decision composite. The winner gets an N=4 + rerank run.
7. Base vs instruct for the winning family, if a base exists. Instruct models drift further from human style ([Reinhart et al.](https://arxiv.org/abs/2410.16107)). Keep base only if it wins style and passes M12.
8. Lexicon v1: profile the untuned winner on ~2,000 train inputs against Housel's pre-2022 text and a pre-2022 informational baseline, with the Antislop ratio method. Profile the Claude family separately on `restyle` outputs.
9. Generate the local half of form B with the winner's untuned base.

Starting config (`configs/train/sft.yaml`, mlx-lm 0.32.x)

```yaml
model: /Users/natuanand/.quill/models/qwen3.5-9b-4bit   # quantized base -> QLoRA
train: true
data: /Users/natuanand/.quill/data/mlx/sft-v1-s1          # stage 1: form A
adapter_path: /Users/natuanand/.quill/adapters/sft-v1-s1
fine_tune_type: lora           # dora in ablation A3
mask_prompt: true              # loss on the assistant turn only
num_layers: -1                 # all blocks; no `keys` = every linear layer (attn + MLP)
lora_parameters: {rank: 16, scale: 2.0, dropout: 0.05}   # scale is a direct multiplier (default 20); 2.0 = PEFT alpha 32 at r 16
optimizer: adamw
learning_rate: 1.0e-4
lr_schedule: {name: cosine_decay, warmup: 10, warmup_init: 1.0e-7, arguments: [1.0e-4, <decay>, 1.0e-6]}  # decay = updates - warmup
batch_size: 1
grad_accumulation_steps: 16    # effective batch 16
iters: <rows in train.jsonl>   # one pass if --iters counts micro-batches; confirm in step 2
grad_checkpoint: true
max_seq_length: 2048
steps_per_report: 10
steps_per_eval: 100
val_batches: 25
save_every: 100
seed: 0
```

Basis: all linear layers, rank 16-32, LR ~1e-4, effective batch 8-16, 1-3 epochs ([LoRA Without Regret](https://thinkingmachines.ai/blog/lora/); [Unsloth guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)). Rank 8 underfit and q/k/v-only gave "the wrong vocabulary" ([Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)). On `scale`, see 8.1 item 5.

Time and compute: 3.25-4.25 dev days (2-3 base, 1.25 lexicon v1). Probe: 10-20 min per candidate. Bake-off: one form-A pass ≈ 1.6 h per 8-9B candidate; one night for three. Lexicon v1 generation: 3-5 h.

Exit gate
- Winner: peak ≤ 17 GB at seq 2048, decode ≥ 30 tok/s at 4-bit, dev composite above B1 with a bootstrap 95% CI excluding 0.
- No candidate beats B1: stop and fix data (Phases 1 and 3) before scaling.

### Phase 5: Housel-only SFT (D0) and ablations

| Setting | Value |
|---|---|
| Rank / scale | 16 / 2.0 (32 if Branch F lifts the set above 500k words) |
| Repetitions | 2 per target, one per input form. Within T3's 1-2 and well under ~4 epochs ([Muennighoff et al.](https://arxiv.org/abs/2305.16264)) |
| Schedule **[P]** | Stage 1: form A, LR swept over {5e-5, 1e-4}, cosine, 10 warmup updates. Stage 2: form B at half the stage-1 LR, own YAML (`sft-anneal.yaml`), 10 warmup updates, resumed from stage 1 |
| Effective batch / run time | 16 / ~3.1 h per two-stage run at 150 tok/s (estimate) |

This is `housel_augmentation.md`'s E0 schedule, so D0 doubles as the mixture control. Stage 2 needs its own YAML because the YAML `lr_schedule` sets the LR, not a `--learning-rate` override. It needs its own warmup because `--resume-adapter-file` loads adapter weights only, with a fresh optimizer. Fine-tuning is "highly sensitive to learning rate and the number of training epochs" ([Panza](https://arxiv.org/html/2407.10994)). Evaluate checkpoints every 100 iterations and select on the dev composite. Val loss is not a selection metric: quality rose while loss rose for [Donner](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/). Training loss under ~0.2 flags memorization.

Ablations (one run each on a 30% train subsample, dev eval, keep only winners)
- A1 form schedule: two stages (A then B) vs one shuffled pass of both forms vs draft only.
- A2 RAFT exemplars: 2 length-matched exemplars from other posts in the prompt, at training and inference, vs none ([Panza](https://arxiv.org/html/2407.10994)).
- A3 rank 16 vs 32; LoRA vs DoRA.
- A4 raw-text voice pass first (completions format, 1 pass, 256-1,024-token chunks), then SFT ([StyleTunedLM](https://aclanthology.org/2024.inlg-main.34.pdf)). Watch M9 and the recall probe: this format is closest to plain memorization.
- A5 10% general-instruction anchor data, only if M12 regresses vs B1.
- A7 `write` drafter: untuned base vs a Claude draft, same dev briefs; reports M14. Brief-to-text pairs join A7 only if the recall probe stays clean.

Lexicon v2: re-profile the chosen adapter's dev outputs (N=4). Output residual tell lists, general and Claude, ranked by ρ = f_adapter / f_Housel. They feed the Phase 6 gates and Phase 7 FTPO.

```
uv run mlx_lm.lora -c configs/train/sft.yaml --adapter-path ~/.quill/adapters/sft-v1-s1
uv run mlx_lm.lora -c configs/train/sft-anneal.yaml --data ~/.quill/data/mlx/sft-v1-s2 \
  --resume-adapter-file ~/.quill/adapters/sft-v1-s1/adapters.safetensors --adapter-path ~/.quill/adapters/sft-v1-s2
uv run quill ckpt-export ~/.quill/adapters/sft-v1-s2 --iter 600   # checkpoint + adapter_config.json -> servable dir
uv run quill eval --system adapter:sft-v1-s2@600 --split dev --n 4
```

Time and compute: 3.5-5.5 dev days (3-5 base, 0.5 lexicon v2). Two LR runs at ~3.1 h plus five ablations at ~0.9 h ≈ 11 h (estimate), over 1-2 nights.

Exit gate: dev composite above B0, bootstrap 95% CI excluding 0. Fallback rate at N=4 ≤ 15%. 0 outputs with an 8-10-word span from the Housel corpus; recall-probe spans no longer than the base model's; training loss ≥ 0.2 at the chosen checkpoint.

### Phase 5b: Neighbour mixture (optional, gated)

**Ship D0 unless a mixture passes every dilution check.** Start only if D0 passed Phase 5, the user wants the test, the consent covers Lamade, and the topic-disjoint test set is frozen. Everything in this phase is **[P]** unless marked as measured.

Why it is gated. Measured on 2026-11-08: every neighbour is separable from Housel (AUC 0.87-1.00, Delta 0.95-1.37), while his own halves are not (0.50, 0.75), and no candidate closes more than 43% of the gap on Delta or 24% on AUC. Published evidence: every gain from pooling authors has a target of about 16 texts. With plentiful target data, "one model per author works better" ([ASTRAPOP](https://arxiv.org/html/2403.08043v2)), and mixing "can lead to performance conflicts" ([Dong et al.](https://arxiv.org/html/2310.05492)). The neighbours also under-use Housel's tics: a word-weighted pool of Lamade, FS and Naval runs at about 2.6 em dashes, 3.4 colons and 16 "you" per 1k, against his 5.7, 6.1 and 24.3.

| Element | Stage 1: tagged pool | Stage 2: anneal | Whole run |
|---|---|---|---|
| Housel rows | Every target once, form A | Every target once, form B | 2× upsampling |
| Neighbour rows | ≤100k words: Lamade ≤40k, FS (Parrish) ≤30k, Naval ≤30k | Replay ≤2% of stage-2 tokens, pro rata | ≤~106k words |
| Housel share of target tokens | ≥73.7% | ≥98% | ≥84% |
| Tags (system line, masked) | `voice: v0` Housel; `v1`-`v3` neighbours | Same | Always `v0` at inference |
| LR | D0's stage-1 LR | Half of it | Pick on D0 first |

Data rules
- Report absolute neighbour word counts beside shares; the amount matters more than the ratio ([Dong et al.](https://arxiv.org/html/2310.05492)). Do not top up a short supply from other authors. Use opaque voice codes. Chunk neighbours to Housel's 150-800-word distribution. Hold out ~20% of each neighbour's passages for impostors. Drop topical near-duplicates of Housel test essays.
- Build neighbour pairs with the same pipeline. Keep a pair only if its target sits closer to Housel than its input does (the "style gap" filter). Drop post-2022 neighbour posts above Housel's 90th percentile on M7. Lamade: Collab Fund copies only; his essays look cross-posted from his Substack, so check its robots.txt and AI-training toggle, then ask him. FS: Parrish bylines only; no book excerpts, block quotes or member content. Cached supply is ~10k words each for FS and Naval, so more must be fetched under 2.4.
- mlx-lm v0.32.2 has no sampling weights, loss weights or adapter merging (measured from source). The mixture lives in the files: duplicate rows, shuffle with a fixed seed, put the tag in the system message, keep `valid.jsonl` Housel-only. Batches are length-sorted and loss averages over tokens, so longer targets carry more gradient.

| Run | Design | Neighbour words | Question | Est. training |
|---|---|---|---|---|
| E0a, E0b | D0, two seeds | 0 | Control and seed noise floor | 2 × 3.1 h |
| E1 | Tagged pool | 40k (Lamade) | Does the nearest same-venue author help? | 3.3 h |
| E2 | Tagged pool | ≤100k (Lamade, FS, Naval) | Does a k = 3 pool help? | 3.7 h |
| E3 | E2 without the voice line | ≤100k | Do tags protect Housel's identity? | 3.7 h |
| E4 | E0a + an aux-only adapter merged at w ∈ {0.1, 0.25}, plus middle layers only | ≤100k | Does a post-hoc dial beat pooling? | 0.6 h + minutes per merge |
| E5 | E0 and E2 on 30% of Housel train | 0 / ≤100k | Do neighbours help only when Housel data is scarce? | 0.9 h + 1.5 h |

E4 merges by rank concatenation: stack the A matrices and the weighted B matrices along the rank axis, and write a rank-32 `adapter_config.json`. mlx-lm's `LoRALinear` computes `y + scale·((x @ A) @ B)`, so equal scales give an exact weighted sum ([tuner/lora.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/tuner/lora.py)). Never average A and B separately; that adds cross-terms ([LoRA Soups](https://arxiv.org/html/2410.13025)). Do not run this grid on the generic 30% subsample, which biases the result toward augmentation helping. E5 uses that bias on purpose.

Decision rule, on the frozen topic-disjoint test set:

| Check | Pass condition |
|---|---|
| Hard gates | Entity-gate pass rate no worse than E0; zero 8-10-word spans against the whole Housel corpus |
| Verifier (M1, neighbours as impostors) | Accept rate ≥ E0 − 0.02 |
| Attribution (M15) | Housel share ≥ E0 − 0.03 and neighbour share ≤ E0 + 0.03 |
| Tic profile (em dash, colon, "you", sentence length) | Divergence from held-out Housel ≤ E0 |
| Gain | Composite above E0, paired-bootstrap 95% CI excluding 0 and exceeding the E0a-E0b gap; or the same on the coverage-probe composite with every dilution check passing |
| Humans | Preferred over E0 in at least half of ≥30 blind matched pairs |
| Choice | The smallest neighbour amount that passes every row. If none passes, ship E0 and stop pulling neighbour text. |

Readings: if neighbours help at 30% of Housel but not at 100%, the regime claim holds and the case at full size is closed. If E3 matches E2, the model ignores the tags. Confirm by generating dev outputs under `voice: v1`: if M15 does not shift, the tags carry no information.

Time and compute: 4-6 dev days (estimate). ~20 h of training over 2-3 nights, plus evaluation. Stop early if E1 and E2 both fail the dilution checks on dev.

### Branch F: Motley Fool archive (only if licensed)

The Fool holds the only large pool of extra Housel prose: about 3,250 articles and an estimated 1.5-2.5M words from 2007 to August 2016, of which perhaps 0.3-0.4M are essay columns (estimates). As an employee's work, its copyright is very likely the Fool's, so the request goes to the Fool. Copies in Common Crawl, FineWeb or reprints do not override its opt-out. Until a written licence arrives: no fetching and no manual copies.

If licensed **[P]**:
1. Store the licence in `~/.quill/legal/` and record its scope.
2. Use only pieces inside the licensed scope, and none after August 2016 (the draft request asks for 2012-2016). Drop co-bylines and the "8 Fascinating Reads" roundups. Strip tickers, disclosures, comment calls and "For more:" lists. Dedupe against reprints and Collab posts.
3. Run the 2014-16 columns through the similarity pass against H-B first. If they land near the ceiling, train on them as Housel, with an era line in the prompt.
4. Fool text joins train only; the frozen Collab test set stays for comparability. The set grows to roughly 0.6-0.7M words, so retrain D0 at rank 32 and rerun the ship gate. Time: 3-5 dev days (estimate), plus a retrain.

### Phase 6: Inference pipeline (starts after Phase 2, with B1 as a stand-in)

Deliverables: `quill daemon`, pipeline modules, entity-gate and artifact-gate tests, latency benchmark. Steps:
1. `write` only: draft plainly from the brief and facts with the untuned base (no adapter) on the same server.
2. Render the prompt with `template.py`, the module the pair builder used.
3. Sample N=4 from `mlx_lm.server`. If concurrent requests are not batched, sample sequentially and cap N at 3 for outputs over 300 words.
4. Hard gates: M5 (all input entities present, none new; this also stops Housel's pet people and companies leaking in); MIS ≥ 0.7 or all facts entailed; M9; length ±30%; the artifact gate (H11). The artifact list covers user-directed chatbot phrases ("I hope this helps", "Certainly!", "Would you like…", "Here is a … version"), refusal and knowledge-cutoff text, unfilled bracket placeholders, markdown fences, `oaicite`, `turn0search0`, `attributionIndex`, `utm_source=chatgpt.com/openai/copilot.com`, and AI-search UI strings from Wikipedia abuse filter 1325. Run it over Housel's corpus first; narrow or drop anything that fires.
5. Soft rank: geometric mean of (CISR centroid delta + stylometry distance, MIS). Return the best, else `status: fallback` with the failed checks. Inputs over 800 words are restyled section by section.
6. Decoding grid on dev: temperature {0.5, 0.7, 0.9}, never 0; top_p 0.95; mild repetition penalty. Lower temperature fixed erratic output in practice ([Lazerowitz](https://rosslazer.com/posts/fine-tuning)), but human text dips into low-probability tokens ([StyleMC](https://arxiv.org/html/2312.17242)), so the grid decides. Never seed a prompt with Housel's opening lines.
7. Log every call to `~/.quill/logs/outputs.sqlite`: input hash, rendered prompt, candidates, scores, M7 on all N, choice, adapter version.

Optional, each behind a measured trigger
- **Lexicon threshold gate** (0.5 d): drop candidates whose vocabulary, structure or Claude-family rate exceeds 1.2× Housel's held-out rate. Keep it out of the geometric mean. Switch it on only if returned-output M7 on dev exceeds 1.2×.
- **WQRM floor gate** (2-3 d, plus 1-2 h of user judging): pre-screen on LAMP nonfiction test items, Beemo pairs and WritingPreferenceBench nonfiction slices, then on 100 in-domain pairs the user judges. Adopt only at ≥65% agreement. Score per paragraph and reject below the 10th percentile of Housel's held-out paragraphs. Never maximize it; keep it out of eval.
- **Backtracking soft-ban sampler** (3-5 d of custom code on mlx-lm's `generate_step`), for residual tells only. Trigger: the lexicon gate pushes fallback above 15%, or the same tells survive two re-profiles.

Latency targets (7-9B 4-bit at 30-50 tok/s, prefill ~1-2 s; pending the user's answer in 8.3)

| Case | Target |
|---|---|
| One candidate, 150-word output (~200 tokens) | ≤ 7 s |
| `restyle`, N=4, 150 words | p50 ≤ 20 s if batched, ≤ 30 s if sequential |
| `restyle`, N=3, 400 words (~550 tokens) | p50 ≤ 60 s |
| `write` draft pass; scoring overhead | +4-18 s for 150-400 words (derived from 30-50 tok/s); ≤ 2 s per call |

Time: 3.5-4.5 dev days: v1's 3-4, plus the artifact gate (0.5) and the draft step (0.5, estimate), minus the pseudonymizer (0.5, estimate).

Exit gate: the entity gate catches 50 of 50 seeded mutations (dropped number, shifted date, new name, changed link). The artifact gate fires on every seeded artifact and on no Housel chunk. Latency targets are met on the stand-in model.

### Phase 7: Preference stage (optional)

Start only if the SFT adapter passed Phase 5 and dev still shows a gap: M1 well below the ceiling, a gap in M15 Housel share or the tic profile, or M7 above Housel's rate.

Data
- 500-2,000 pairs, up to two per train chunk. prompt = the SFT system and user turns; chosen = Housel's original; rejected = the SFT model's own sample. Self-generated rejects target exactly what the model still gets wrong ([Quill-v1](https://huggingface.co/sam-paech/Quill-v1); [DITTO](https://arxiv.org/html/2406.00888); [Gutenberg-DPO](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1)). Keep a pair only if the rejected text passes the entity gate and MIS(chosen, rejected) ≥ 0.7, so the preference stays stylistic ([ASTRAPOP](https://arxiv.org/html/2403.08043v2) lost meaning because its reward ignored semantics).
- `pref-v1` holds own-output rejects only: no WildAI, GitHub, Grokipedia, chat-log or Wikipedia text. DPO on harvested slop pairs cut writing quality from 67.8 to 54.6-63.0 in [Antislop](https://arxiv.org/html/2510.15061).

Method: ORPO (reference-free) or CPO in mlx-lm-lora, continuing from the SFT adapter; DPO and CPO scored about equal in ASTRAPOP. LR 1e-6 to 5e-6, 1 pass, batch 1, grad accumulation 8, seq ≤ 1,024, with warmup because the optimizer starts fresh. DPO only if memory allows, and only with the fused reference below. mlx-lm-lora has no KTO, and mlx-tune's KTO approximates gradient ascent on negatives.

```
uv run mlx_lm_lora.train --train-mode orpo --train \
  --model ~/.quill/models/<winner>-4bit --data ~/.quill/data/mlx/pref-v1 \
  --resume-adapter-file ~/.quill/adapters/sft-v1-s2/adapters.safetensors \
  --adapter-path ~/.quill/adapters/orpo-v1 --learning-rate 2e-6 --batch-size 1 --max-seq-length 1024 --iters 1000
# confirm flag names with: uv run mlx_lm_lora.train --help
```

FTPO (optional; 2-3 d plus 2-4 h of training). Trigger: any M7 family above 1.2× Housel's rate on dev after SFT (and ORPO, if run). Targets: only tells the adapter actually emits at ≥1.2× Housel's rate, ranked by cross-source agreement. Data: final-token pairs at each residual-tell onset in the adapter's own outputs (custom script). Reference: mlx-lm-lora uses a frozen copy of `--model` unless `--reference-model-path` is set, which would anchor outputs to the untuned base. Fuse the SFT adapter with `mlx_lm.fuse` and pass the fused copy as `--reference-model-path`. Probe 20 iterations. FTPO is tested only on creative writing.

Time and compute: 2-3 dev days. Rejects: ~2.5 h per 500 pairs at 35 tok/s (estimate). ORPO: ~2-4 h per 1,000 pairs (estimate). Probe 20 iterations first.

Exit gate (keep the stage only if all hold on dev): composite up, CI excluding 0; expect a modest gain, as ASTRAPOP saw ~5% relative. Median MIS within 0.02 of SFT. Hard-gate pass rate not lower. M7 not higher. Over-correction alarm passes.

### Phase 8: Ship gate

Steps
1. Freeze the candidate: adapter, decoding settings, reranker config. Run `quill eval --split test` for the system and B0, both at N=4 with the same reranker.
2. Blind test R (relative), first: a reference excerpt from a train post, plus system vs B0 on the same test input, n=40, "which reads more like Housel?" It shows no test originals.
3. Blind test A (absolute): the real held-out Housel passage vs the system's restyle of that passage's frozen draft, n=40, "which is the real Housel?" Running R first lets A reuse R's items if test holds fewer than 80 chunks **[P]**.
4. Reader: the user, or someone they name, who knows Housel's writing. Familiar readers are stricter (expert κ 0.54-0.58 vs lay 0.07-0.22, [arXiv 2601.18353](https://arxiv.org/html/2601.18353v1)). A familiar reader may also recognize a passage from memory. Report H1 with and without recognized items; the pass rule counts all items **[P]**. Sessions at least 3 days apart; log reasons.
5. Optional utility arm **[P]**: "which would you use?" on coverage-probe briefs, system vs B0. Reported only.

Time and compute: 1-2 dev days. Test generation: 60-100 chunks × 2 ops × 4 × 600 tokens ≈ 2.5-4 h (estimate). Two reader sessions of ~1 h.

Exit gate: every hard criterion in Section 6 passes. Then `ln -sfn sft-vN ~/.quill/adapters/prod`. On failure, diagnose from the tic profile, M15, M7, M14 and the blind-test reasons. Then fix data (Phases 1 and 3), rerun ablations (Phase 5) or try the stretch model. After 3 failed loops, review with the user. A prompt-only product stays out of scope.

### Phase 9: Serving and Claude Code integration

Steps
1. launchd agents (`launchd/`, installed to `~/Library/LaunchAgents/`). `com.quill.mlx` runs `/Users/natuanand/quill/.venv/bin/mlx_lm.server --model /Users/natuanand/.quill/models/<winner>-4bit --host 127.0.0.1 --port 8080` with `WorkingDirectory` = `/Users/natuanand/.quill`; per-request `adapters` paths resolve against the start directory, so call the venv binary directly. `com.quill.daemon` runs `/Users/natuanand/quill/.venv/bin/quill daemon --port 8765`.
   - `quill down` unloads both before training; `quill up` reloads them. Bind to 127.0.0.1 only; SERVER.md says `mlx_lm.server` is not production-grade.
   - Request body: `{"model": "...", "adapters": "adapters/prod", "messages": [...], "max_tokens": 1100, "temperature": 0.7, "top_p": 0.95}`. The `write` draft pass sends the same body without `adapters`.
2. MCP server (`src/quill/mcp_server.py`):

   ```python
   import logging, sys, httpx
   from mcp.server import MCPServer
   logging.basicConfig(stream=sys.stderr, level=logging.INFO)  # stdout carries JSON-RPC; never print
   DAEMON, mcp = "http://127.0.0.1:8765", MCPServer("quill")

   async def _call(method: str, path: str, payload: dict | None = None) -> dict:
       async with httpx.AsyncClient(timeout=110) as client:
           r = await client.request(method, DAEMON + path, json=payload)
           r.raise_for_status()
           return r.json()

   @mcp.tool()
   async def write(brief: str, facts: list[str], length_words: int | None = None) -> dict:
       """Write new prose in the quill voice. Put every name, number, date, link and commitment in `facts`. Show `text` verbatim."""
       return await _call("POST", "/write", {"brief": brief, "facts": facts, "length_words": length_words})

   # restyle(draft, length_words) -> POST /restyle; docstring: show `text` verbatim; on "fallback", show the draft and failed checks.
   # record_final(output_id, final_text) -> POST /feedback.  status() -> GET /status.  main(): mcp.run(transport="stdio").
   ```

3. Register at user scope ([Claude Code MCP docs](https://code.claude.com/docs/en/mcp)): `claude mcp add --scope user --transport stdio quill -- uv --directory /Users/natuanand/quill run quill-mcp`. Set the server's `"timeout": 120000` (ms) in `~/.claude.json`, or set `MCP_TOOL_TIMEOUT`.
4. Skill (`skill/quill/SKILL.md`, symlinked to `~/.claude/skills/quill/SKILL.md`):

   ```markdown
   ---
   name: quill
   description: Use when the user asks for prose in the quill voice (memo, update, essay, post) or asks to rewrite a draft with quill. Routes the writing to the local quill style model.
   ---
   1. Work out the content: purpose, target length, and every fact, name, number, date, link and commitment. Ask the user for anything missing.
   2. New text: call `mcp__quill__write` with `brief`, `facts` and `length_words`. Existing draft: call `mcp__quill__restyle`.
   3. Add no tone or style instructions.
   4. Show the returned `text` verbatim. Do not polish or paraphrase it. If `status` is `fallback`, say so and list the failed checks.
   5. When the user shares the version they used, call `mcp__quill__record_final`.
   ```

5. Smoke test: 10 real requests (5 `write`, 5 `restyle`) from a fresh Claude Code session.

GGUF and Ollama stay out of the serving path. `mlx_lm.fuse --export-gguf` supports only llama, mistral and mixtral ([fuse.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/fuse.py)), and Ollama's MLX engine targets Macs with more than 32 GB ([Ollama MLX](https://ollama.com/blog/mlx)). Never merge into a 4-bit model: it can erase small LoRA updates ([mlx-tune](https://github.com/ARahim3/mlx-tune)). The fused 16-bit copy for an FTPO reference stays local. Time: 2-3 dev days.

Exit gate: 10/10 smoke requests go through the tool. Claude returns the text unchanged. p50 latency within Phase 6 targets. Daemon and server survive a reboot. The MCP server writes nothing to stdout.

### Phase 10: Retraining and feedback loop

New data
1. New Housel posts on Collab Fund, if the consent covers them, fetched under 2.4. Output is thin (2 posts in 2026), so retrain after +10% words. Assign each new post to its nearest topic cluster; posts nearest a test cluster stay out of train **[P]**. Branch F text joins if licensed.
2. `record_final` finals are the user's writing, not Housel's. Store them in `~/.quill/feedback/` as the user's own corpus. They never become Housel SFT targets, preference pairs for this adapter, or eval items: post-edited text stays much closer to the LLM draft than to the writer's own (g = −1.43, [Baumler et al.](https://arxiv.org/html/2604.24444)). They could seed an own-voice adapter once they clear T1 or T2.

Retrain procedure (`uv run quill retrain`)
1. Ingest, clean, pair and curate the new data. Retrain from the base with the current recipe (~3 h); no adapter stacking.
2. Evaluate candidate vs prod on the frozen test set. Promote only if no hard criterion regresses and the composite is ≥ prod. Run blind test A every second release. Keep the last 3 adapters for rollback.
3. If stylometry drifts between the oldest and newest thirds of the corpus, cap the share of old data ([Griffiths](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na)).
4. Re-profile the lexicon after every retrain (~0.5 d). Each quarter, diff the Signs page for new era tells, and refresh the Claude family from the newest month of Claude Code PRs, keyed by commit-trailer model version (~0.25 d). Rebuild α's Q corpus when the drafter model changes.

Automation: a quarterly launchd timer **[P]** checks for new posts and diffs the Signs page. Training stays user-triggered (memory, heat). Compute: ~3 h training + 1-2 h eval per cycle.

Exit gate: one full cycle completed end to end, with a promotion decision logged.

## 6. Ship criteria

On the frozen topic-disjoint test set. System = adapter + pipeline. B0 = Claude prompted to write like Housel, with style guide and exemplars, plus the same pipeline.

Hard (all must pass)

| # | Criterion | Threshold | Basis |
|---|---|---|---|
| H1 | Blind A: a reader who knows Housel picks the real passage over the system's, matched content | ≤ 25/40 correct, i.e. indistinguishable. ≥ 26/40 means reliable detection (one-sided p = 0.040). | 8.1 item 8 |
| H2 | Blind R: system vs B0, "reads more like Housel" | System wins ≥ 26/40 (p = 0.040) | 8.1 item 8 |
| H3 | AV accept rate (M1) | System ≥ B0 + 10 points and ≥ 70% of the real-text ceiling | 5-shot prompting passes AV ~17-21% on blogs ([Catch Me If You Can](https://arxiv.org/html/2509.14543v1)) |
| H4 | Entities, numbers, dates and links kept | 100% | Pipeline invariant |
| H5 | Meaning, `restyle` | Every returned output MIS ≥ 0.70; median ≥ 0.75 | [TinyStyler](https://arxiv.org/html/2406.15586) filter |
| H6 | Fact coverage, `write` | ≥ 98% of facts entailed | Plan threshold |
| H7 | New entities in output (Housel's recurring names and companies included) | 0 | Replaces v1's PII criterion |
| H8 | Memorization | 0 returned outputs with an 8-10-word span from the whole Housel corpus; recall-probe spans no longer than the base model's. Recall means spans from the corpus outside the item's own post; spans rebuilt from a paraphrase of the item's own post are reported and not gated (user decision 2026-11-11) | [Whack-a-Mole](https://arxiv.org/pdf/2603.20957v2); [Chakrabarty et al.](https://arxiv.org/html/2510.13939) resampled regurgitation |
| H9 | Fallback rate | ≤ 15% | Plan threshold |
| H10 | Latency | Phase 6 p50 targets | Notes silicon Q5 |
| H11 | Artifact count on returned outputs | 0 | [negative_signal.md](negative_signal.md) item 13 |

Soft (report all; each failure needs a written reason in the release note)
- M15 Housel share: system > B0, CI excluding 0 **[P]**. Tic profile (M6): pooled |z| ≤ 2 on every feature. Signature phrases: none above 2× the real-text rate.
- M7: each validated family ≤ 1.2× Housel's held-out rate, on returned outputs and on all N candidates; Claude family ≤ 1.2× on `restyle` outputs.
- M14: drafter-probe AUC on outputs ≤ 0.60 **[P]**, with residue ratio R reported. M13: α(system) < α(B0), CI excluding 0.
- M10 (or M10b) flag rate: system ≤ B0; it never certifies an output. Topic drift on coverage-probe briefs below a threshold set on dev.
- Reported only: M2 StyleDistance, M3 LUAR, Burrows' Delta, the utility arm.

## 7. Risks and mitigations

| Risk | Signal | Mitigation | Source |
|---|---|---|---|
| Verbatim reproduction of Housel | M9 hits; recall-probe spans above base | Paraphrase and draft inversion only; twin groups and paragraph dedup; 2 repetitions; stop below train loss 0.2; 8-10-word gate on the whole corpus; temperature > 0; no opening-line seeds | [Whack-a-Mole](https://arxiv.org/pdf/2603.20957v2); [Chakrabarty et al.](https://arxiv.org/html/2510.13939) |
| Consent or licence gap | A use missing from `scope.yaml`; API prep outside scope; NC-licensed pools near paid work | Block that step; local generator; keep everything local; WildAI and Grokipedia eval-only; delete on objection | Collab Fund Terms of Use (Feb 2026); [negative_signal_priors.md](negative_signal_priors.md) §5.2 |
| Passing off; impersonation if the adapter leaks | Output presented as Housel's; his name on files | No name on outputs, adapters, files or tools; disclose AI help when publishing; never upload; FileVault; 127.0.0.1 only | [Nieman Lab](https://www.niemanlab.org/2026/03/journalist-julia-angwin-files-class-action-lawsuit-over-grammarlys-ai-sloppelgangers/); [Panza](https://arxiv.org/html/2407.10994) |
| Caricature, tic overuse | Tic-profile \|z\| > 2 (one-line paragraphs, "you"); M8 ratio > 2; blind reasons | Fewer repetitions; rank 16; LR sweep; dev checkpoints; adapter copy at `scale` × 0.5-0.75; FTPO on emitted tells | [NicAI](https://notes.nicolasdeville.com/nicai/slm/); Claude's imitation: "you" 32.4 vs 24.3 |
| Meaning drift, fact wash-out | MIS < 0.7; entity failures | Fact closure; hard gates; fallback; Phase 7 gated on MIS | [ASTRAPOP](https://arxiv.org/html/2403.08043v2) |
| Housel's names and anecdotes leak into user text | New entity in output; topic drift | Facts in the prompt; fact closure; H7 gate; topic-drift check | [codebyandy](https://github.com/codebyandy/finetune-me); [style_library.md](style_library.md) §6 |
| Capability loss; personalization collapse | M12 regresses vs B1; style drops when instructions vary | Instruct base; LoRA forgets less ([Biderman et al.](https://arxiv.org/abs/2405.09673)); A5 anchor data; length tag only, no style instructions | [PsPLUG](https://arxiv.org/abs/2601.06362) |
| Short or looping output | Length failures; repeated n-grams | Length tags; mild repetition penalty; decoding grid | [Donner](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/) |
| AI-assisted Housel posts in training | Lexicon flags; changepoint after 2023-03 | Lexicon + changepoint + M10; user review; no auto-drop | [Kusumegi et al.](https://arxiv.org/abs/2601.13187) |
| Residual Claude fingerprint | M14 probe AUC on outputs; residue ratio R | More Claude-drafted Housel pairs; A7; local drafter for `write` | [Idiosyncrasies in LLMs](https://arxiv.org/abs/2502.12150) |
| Evaluator gaming, topic leakage, Delta false pass, detector blind spot | Metric gains without blind-test gains; Delta near ceiling while M1 separates; detector calls outputs human while blind tests fail | Topic-disjoint splits; same-register and finance impostors; separate rerank and eval; StyleDistance and Delta diagnostic only; M10 never certifies; blind tests decide | [TinyStyler](https://arxiv.org/html/2406.15586); Claude's imitation: Delta 1.044 at AUC 1.000; Pangram caught 3% of author-fine-tuned output ([Chakrabarty et al.](https://arxiv.org/html/2510.13939v3)) |
| Neighbour dilution (5b only) | M15 Housel share falls; tic profile drifts | Caps, tags, anneal, decision rule; ship D0 by default | [housel_augmentation.md](housel_augmentation.md) |
| Reader recall or bias | Reader recognizes passages; one reader | Log recognition; sessions 3 days apart; logged reasons | [Baumler et al.](https://arxiv.org/html/2604.24444) |
| Over-correction, tell substitution | MATTR or punctuation-variety drop; new over-represented n-grams | Over-correction alarm on every suppression step | [Antislop](https://arxiv.org/html/2510.15061); [Geng & Trotta](https://aclanthology.org/2025.findings-acl.657) |
| Stale lexicon; era leakage in mined lexicons | M7 AUC falls on fresh Wikipedia tags; a tell fails the same-crawl control | Re-profile per retrain; quarterly Signs diff and PR refresh; two-control rule | [negative_signal_priors.md](negative_signal_priors.md) §3.5 |
| Thin recent output, frozen era | 17, 11, 2 posts in 2024-26; drift between corpus thirds | Drift check; cap old data; era line if Fool text enters | [Griffiths](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na) |
| Tooling breakage, out of memory, slow calls | Probe crash; peak > 17 GB or swap; latency over target | Pin versions; probe every candidate; serve unfused adapters; Qwen3-8B fallback; batch 1, grad checkpointing, seq ≤ 2,048; stop servers during training; N=3 for long outputs | Notes silicon Q1/Q4/Q5; [mlx-optiq](https://mlx-optiq.com/docs/finetune) |

## 8. Deviations and open questions

### 8.1 Where the evidence contradicts or refines the approach

1. **SimPO and KTO are not in mlx-lm-lora.** Its methods include SFT, DPO, CPO, ORPO, FTPO and the GRPO family. Plan: ORPO or CPO. (Retrieved exemplars stay off by default, as in v1; see 2.3.)
2. **Selection metrics cannot judge.** StyleDistance and Delta selected the neighbours, and Delta passes a caricature (Phase 2). Plan: decide on M1, M15 and M4; report StyleDistance, LUAR and Delta.
3. **Content handoff for `write`.** v1 had Claude never draft first. `style_library.md` makes draft-then-restyle the default to avoid summary-to-text training. Plan: the untuned base drafts **[P]**; A7 tests a Claude draft; M14 measures residue.
4. **LoRA is the weakest adapter type in Panza.** RoSA and full fine-tuning beat it. mlx-lm offers LoRA, DoRA and full, and full FT of 8B does not fit 24 GB. Plan: all-layer LoRA at rank 16-32 plus a DoRA ablation.
5. **mlx-lm `scale` is not PEFT alpha.** `scale` (default 20.0) multiplies the LoRA output directly, with no division by rank (checked in `mlx_lm/tuner/lora.py`, 2026-11-07). Scale 32 at rank 16 with LR 1e-4 would be ~16× hotter than PEFT alpha 32. Plan: scale 2.0, LR 1e-4, LR sweep. The same read said `iters` counts micro-batches; the mixture notes disagree, so the 32-iteration probe settles it.
6. **Which model writes the training inputs.** The neutralizer should differ from the deployment drafter, and restyle training should match deployment drafts. Plan: half Claude, half the runtime local drafter; eval reports restyle results per drafter.
7. **Neighbour authors do not help at this size.** Published gains from pooling need ~16-text targets, and no study tests 100k-500k words. Plan: Housel-only first; mixture gated (Phase 5b).
8. **The 2AFC rule needs care.** "≤6 of 20 correct" means the reader picks quill's text as real more often than chance, with one-sided p = 0.058. Results of 7-14 of 20 are an absence of evidence. At n=20, a reader who truly detects 70% of the time reaches significance only 42% of the time. Plan: n=40 with threshold 26 (p = 0.040, 81% power at 70%). A pass at ≤25/40 shows no reliable detection; it does not prove identity.
9. **General instruction data.** Notes data Q3 suggests 10-30%, but assistant-voice data could pull outputs toward that voice. Plan: off by default; A5 only if length adherence regresses.
10. **Feedback edits are not Housel's writing.** Plan: store them as the user's corpus; never train this adapter on them.
11. **Runtime content source.** The calling Claude Code session handles content, so runtime needs no API key. The API serves data prep, B0 and the optional judge, and only within the consent scope.
12. **Base vs instruct is unsettled,** and masking matters little for long outputs. Plan: test both bases for the winning family; mask the prompt anyway, because it is LLM-written text.
13. **Harvested slop stays out of training.** No study trains a style adapter on unpaired, off-domain slop, and DPO on slop pairs cut quality and diversity in Antislop. Detectors never become rewards: under a day of DPO against one cut its AUROC from 0.84 to 0.62, and the evasion transferred ([Nicks et al.](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1f9f07df0992ce21698d800eaa891bd8-Abstract-Conference.html)).
14. **B0 strength for a famous author.** `style_library.md` warned that LLMs imitate Housel's cadence, so an adapter may buy less. The probe found Claude's from-memory imitation a caricature (AUC 1.000), but it had no guide or exemplars. Plan: score B0 as specified.

### 8.2 Facts to verify on day 1 of Phase 4

- Exact HF repo ids, base/instruct availability and vision weights for Qwen3.5-9B, Ministral 3 8B and Gemma 4 E4B; Ministral 3 `model_type`; Qwen3.5 Gated DeltaNet LoRA end to end; whether `mlx_lm.convert` drops the vision tower; Gemma 4 E4B through `mlx_lm` vs `mlx_vlm`.
- Whether `mlx_lm.server` batches concurrent requests and has an `--adapter-path` startup flag. This sets real best-of-N latency.
- **What `--iters` counts:** a 32-iteration probe, counting the examples consumed. Also whether `lr_schedule` steps count optimizer updates (assumed) or micro-batches.
- **`--resume-adapter-file` loads adapter weights only,** with no visible optimizer-state restore. Every resumed stage (D0 stage 2, ORPO, mixture anneal) gets its own warmup.
- **mlx-lm has no sampling weights, per-sample loss weights or adapter merging.** The mixture lives in the files; E4's merge is custom code.
- mlx-lm-lora flag names (`--resume-adapter-file`, `--reference-model-path`, beta), ORPO peak memory at 8-9B and seq 1,024, and whether the FTPO reference stays resident.
- MCP Python SDK 2.x `MCPServer` API as documented for the 2026-07-28 spec. LUAR custom code on MPS. MIS licence (a third-party listing says CC BY-NC-SA 4.0; fine for personal use). Not planned: raising `iogpu.wired_limit_mb` (unverified).

### 8.3 Questions for the user

1. **Consent scope.** Answered 2026-11-08: the consent covers training, sending text to the Claude API (pairs, B0, judge) and Lamade's essays. Still open: posts published after 2026-11-08, and the consent copy for `~/.quill/legal/`.
2. **Jurisdiction.** US, UK or EU? The UK has no commercial TDM exception, and EU opt-outs carry legal weight.
3. **Where outputs go.** Do they stay on the Mac, go into work memos, or get published? The answer sets the verbatim-overlap threshold (8 or 10 words; stricter for publication) and the exposure from the non-commercial WildAI and Grokipedia licences.
4. **Blind-test reader.** Will you take the blind tests, or name someone who knows Housel's writing?
5. **Fool licence.** Should we send the Motley Fool a written licence request now?
6. **Latency.** Is ~20-30 s acceptable for a short restyle and ~60 s for a 400-word piece? `write` adds a 4-18 s draft pass.
7. **Scope.** Confirm that quill only returns text and never sends or publishes anything.
