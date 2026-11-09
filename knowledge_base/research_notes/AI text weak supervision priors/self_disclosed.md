# Self-disclosed and labeled-by-construction AI text: harvestable volume, register fit, terms (as of 2026-11-07)

Scope: text whose AI provenance is declared by its own author, publisher or platform, or is certain by construction (agent bot accounts, tool footers, synthetic corpora, chat logs). Volume labels used throughout:
- **MEASURED**: I ran a read-only query on 2026-11-07. The query URL is given so anyone can re-run it.
- **REPORTED**: a number from a publisher, vendor or press source, not checked by me.
- **ESTIMATED**: my own arithmetic or inference.

Method notes (needed to read the numbers):
- **GitHub.** Counts are `total_count` values from the REST search API, queried with the user's authenticated `gh`, read-only.
  - GitHub phrase search matches loosely, so headline counts need correcting. I measured precision by pulling the 100 most recent October 2026 hits per query and checking for the literal string.
  - Commit search returned `incomplete_results=true`, so commit totals are approximate.
  - Raw data is in `/private/tmp/claude-501/-Users-natuanand-quill/8abcef51-55b0-4d7f-93a8-c529b14b7a17/scratchpad/priors/data/` (gh_counts.tsv, gh_samples_oct2026.json, gh_repo_prior.json, epmc_counts.json, wildchat48_models.json).
- **Europe PMC (EPMC).** Counts are `hitCount` from the REST search over EPMC full text, which is mostly the PMC open-access subset plus author manuscripts. OpenAlex counts use its `fulltext.search` filter, which has partial coverage.

---

## Q1. Which self-labeled sources give >=10k informational documents retrievable as text with workable terms (Nov 2026)? Rank by volume x register fit x recency of generating models

### Takeaway
GitHub is the largest self-disclosed source by far and the most recent. Agent and tool-attributed pull request (PR) and issue bodies run to millions per month in 2026, are written by 2025-2026 frontier models, and sit in an explanatory-technical register (problem / change / test plan). Most carry machine-readable markers that bound the AI-written span exactly.

Three other sources clear the 10k bar with usable terms:
- **Scientific papers with positive AI-use declarations** in the PMC open-access CC BY subset: roughly 5k-15k per year in 2026. The text is AI-polished, though, not AI-written.
- **Grokipedia**: 5.86M URLs (MEASURED via a sitemap dataset); 884k articles already scraped in a dump. Encyclopedic register, Grok 2025-26, but 56% is near-Wikipedia text.
- **Open chat logs**: WildChat-4.8M (ODC-BY, GPT-4o/4.1-mini, to July 2025) and the LMArena 2025 releases (Claude Opus 4, Gemini 2.5, o3).

News outlets with AI labels and UI-labeled platform text (LinkedIn, Amazon, Google AI Overviews) are either too small or not legally harvestable at volume.

### Cited Findings

#### A. GitHub: agent and tool attribution in PR, issue and commit text (all MEASURED 2026-11-07 unless noted)

**Disclosure strings, observed in the 100-item October 2026 samples**
- **Claude Code.**
  - PR and issue footer: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
  - Commit trailer: `Co-Authored-By: Claude ... <noreply@anthropic.com>`.
  - Claude Code exposes `attribution.commit` / `attribution.pr` settings to "change or hide" these, and the older `includeCoAuthoredBy` key is deprecated. So the label is on by default and can be removed. — [Claude Code settings reference](https://code.claude.com/docs/en/settings-reference.md)
- **CodeRabbit.** An AI summary block bounded by `<!-- This is an auto-generated comment: release notes by coderabbit.ai -->` ... `## Summary by CodeRabbit` ... `<!-- end of auto-generated comment: release notes by coderabbit.ai -->`. All 100 sampled PRs had both markers. — [measured sample, query](https://api.github.com/search/issues?q=is:pr+in:body+%22Summary+by+CodeRabbit%22+created:2026-10-01..2026-10-31)
- **Cursor background/cloud agent.** The body sits between `<!-- CURSOR_AGENT_PR_BODY_BEGIN -->` and `<!-- CURSOR_AGENT_PR_BODY_END -->`, followed by an "Open in Cursor" badge linking `cursor.com/background-agent`. 100/100 sampled PRs had both markers. — [query](https://api.github.com/search/issues?q=is:pr+in:body+%22cursor.com/background-agent%22+created:2026-10-01..2026-10-31)
- **GitHub Copilot coding agent.** The PR author is the `copilot-swe-agent` app, and the body contains `<!-- START COPILOT CODING AGENT SUFFIX -->`. — [query](https://api.github.com/search/issues?q=is:pr+author:app/copilot-swe-agent+created:2026-10-01..2026-10-31)
- **Google Jules.** The author is `google-labs-jules[bot]`, and the footer reads `*PR created automatically by Jules for task [id](https://jules.google.com/task/...) started by @user*`. — [query](https://api.github.com/search/issues?q=is:pr+author:app/google-labs-jules)
- **Devin.** The author is `devin-ai-integration[bot]`, and the footer reads `Link to Devin session: https://app.devin.ai/sessions/...` plus `Requested by: @user`. — [query](https://api.github.com/search/issues?q=is:pr+author:app/devin-ai-integration)
- **OpenAI Codex cloud.** In 2025 the body contained `https://chatgpt.com/codex/tasks/task_e_...`. — [query](https://api.github.com/search/issues?q=is:pr+in:body+%22chatgpt.com/codex/tasks%22)
- **Aider.** By default it appends "(aider)" to the git author and committer name. The `aider:` message prefix and the Co-authored-by trailer are opt-in flags. — [Aider git docs](https://aider.chat/docs/git.html)

**Volumes**

| Source (query) | All-time | Oct 2026 | Precision (n=100, Oct 2026) | Median body words | Share >=150 words | Unique repos /100 |
|---|---|---|---|---|---|---|
| Claude Code PRs (`is:pr in:body "Generated with Claude Code"`) | 22,398,119 | 7,293,892 | 0.95 exact `[Claude Code]` footer; 1.00 contain "Claude Code" | 276.5 | 0.69 | 96 |
| Claude Code issues | 336,409 | 130,088 | 0.92 | 199.5 | 0.65 | 67 |
| CodeRabbit summaries in PRs | 3,862,679 | 509,335 | 1.00 | 353.5 (whole body); 65 (AI span only) | 0.85 | 94 |
| Cursor agent PRs (`cursor.com/background-agent`) | 1,631,781 | 408,705 | 1.00 | 197 (marked span 159.5) | 0.71 | 82 |
| Copilot coding agent PRs (author) | 2,145,376 | 60,573 | 1.00 (by construction) | 109.5 | 0.31 | 65 |
| Devin PRs (author) | 333,507 | 53,041 | 1.00 | 240.5 | 0.83 | 45 |
| Jules PRs (author) | 337,665 | 11,530 | 1.00 | 118 | 0.27 | 36 |
| Codex cloud PRs (`chatgpt.com/codex/tasks`) | 1,969,476 | 755 | 1.00 | 19 | 0.06 | 10 |

Source for the table: [GitHub search API, issues endpoint](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests), queries as listed, MEASURED.

**Monthly Claude Code PR counts (MEASURED)**
- 2025: Feb 224, Mar 1,107, Apr 1,209, May 4,560, Jun 21,801, Jul 33,917, Aug 36,453, Sep 30,046, Oct 57,527, Nov 55,774, Dec 90,340.
- 2026: Jan 163,358, Feb 319,563, Mar 603,855, Apr 743,717, May 1,155,075, Jun 1,717,277, Jul 2,286,656, Aug 2,055,687, Sep 4,074,362, Oct 7,293,935.
- Totals (ESTIMATED by summing): about 333k in 2025 and about 20.4M in Jan-Oct 2026.
- Source: [query template](https://api.github.com/search/issues?q=is:pr+in:body+%22Generated+with+Claude+Code%22+created:2026-10-01..2026-10-31)

**Share of all PRs (MEASURED)**
- All PRs created: 2022: 75,617,364; 2025: 78,578,643; 2026 YTD: 171,542,310; October 2026: 32,597,516.
- So Claude Code-footer PRs were about 22% of all PRs created in October 2026 (ESTIMATED ratio).
- Source: [query](https://api.github.com/search/issues?q=is:pr+created:2026-10-01..2026-10-31)

**Other monthly series (MEASURED)**
- **Copilot coding agent.**
  - Rose from 5,035 (May 2025) to a peak of 315,120 (Mar 2026), then fell: 238,837 (Apr), 151,103 (May), 67,254 (Jun), 67,888 (Jul), 61,721 (Aug), 59,306 (Sep), 60,573 (Oct 2026).
  - The drop probably reflects an attribution or authoring change, not lower usage; that is unverified.
  - [query](https://api.github.com/search/issues?q=is:pr+author:app/copilot-swe-agent)
- **Codex.**
  - 433,997 (Jun 2025), then 300k-430k per month through Oct 2025, then 51,951 (Nov 2025), 97 (Dec 2025), and under 800 per month in 2026.
  - The task-link marker effectively disappeared, and 2026 hits are one-line bodies.
  - [query](https://api.github.com/search/issues?q=is:pr+in:body+%22chatgpt.com/codex/tasks%22)
- **Cursor.** 5,701 (Jul 2025), 54,735 (Aug 2025), a trough of 14,260 (Jan 2026), then 152,676 (Jul), 257,171 (Aug), 345,742 (Sep), 408,701 (Oct 2026). — [query](https://api.github.com/search/issues?q=is:pr+in:body+%22cursor.com/background-agent%22)
- **CodeRabbit by year.** 2023: 11,740; 2024: 162,771; 2025: 727,153; 2026 YTD: 2,960,712. — [query](https://api.github.com/search/issues?q=is:pr+in:body+%22Summary+by+CodeRabbit%22)
- **Devin by year.** 2024: 3,447; 2025: 46,544; 2026: 283,534.
- **Jules by year.** 2025: 151,980; 2026: 185,690.
- **Claude Code issues by year.** 2025: 11,957; 2026: 324,355.

**Smaller and unverified markers (MEASURED counts, precision not checked)**
- "Summary by Sourcery": 763,277 all-time. The 2022 count of 7,646 predates the product, which shows loose matching.
- "Generated with Gemini": 15,216 (2026: 14,274).
- "Link to Devin run" (older Devin format): 81,100.
- "OpenHands": 56,142.
- codegen-sh app PRs: 9,438.
- "Generated with Amp": 7,168.

**Loose phrase matching inflates generic strings (MEASURED)**
- "Generated by Claude" returned 2,868,046 PRs for October 2026, but only 1/100 sampled bodies contained the literal phrase.
- "This PR was generated by" had precision 0.60.
- Only tool-specific URLs, HTML markers and bot authors are reliable.
- [query](https://api.github.com/search/issues?q=is:pr+in:body+%22Generated+by+Claude%22+created:2026-10-01..2026-10-31)

**Commits (MEASURED, `incomplete_results=true`, so approximate)**
- `"Co-Authored-By: Claude"`: 3,028,287 (2025) and 19,786,353 (2026). An earlier all-time query returned 43,469,534; that inconsistency shows the commit counts are noisy.
- `"Generated with Claude Code"` commits, all-time: 6,775,703.
- GitHub commit search only covers default branches.
- [query](https://api.github.com/search/commits?q=%22Co-Authored-By:+Claude%22+committer-date:2026-01-01..2026-12-31); [GitHub docs: searching commits](https://docs.github.com/en/search-github/searching-on-github/searching-commits)
- Other trailers, MEASURED 2025 / 2026 by committer date:
  - `"Co-authored-by: Cursor Agent"`: 74,154 / 919,621 (incomplete results).
  - `"Co-authored-by: Copilot"`: 665,661 / 4,009,189 (incomplete). The 2026 jump coincides with the fall in Copilot bot-authored PRs.
  - Aider `author-name:"(aider)"`: 260,403 / 11,121 (complete results; precision not sampled).
  - Aider `"aider:"` message matches: 127,195 / 269,050 (precision not sampled; loose matching likely).
  - Commit messages are short and mostly not informational prose, so they matter mainly as provenance for which repos and PRs are agent-written.
  - [query](https://api.github.com/search/commits?q=%22Co-authored-by:+Cursor+Agent%22+committer-date:2026-01-01..2026-12-31)

**Register and form (MEASURED on the Oct 2026 samples)**
- Claude Code PR bodies:
  - 61% use markdown headings and 79% use bullets.
  - 94% are more than 90% Latin-script; the rest are mostly CJK.
  - 5% also contain a CodeRabbit block, so tools stack.
- Jules bodies use emoji section templates ("💡 What / 🎯 Why").
- Copilot bodies often fill the repo's PR template.
- Source: sample analysis of the [Claude Code PR query](https://api.github.com/search/issues?q=is:pr+in:body+%22Generated+with+Claude+Code%22+created:2026-10-01..2026-10-31)

**Licensing and same-repo history**
- **Model-version labels in commit trailers (MEASURED).**
  - October 2026: 100 most recent `Co-Authored-By: Claude` commits, from 87 unique repos, all with the literal trailer. 76 name "Claude Opus 5.5", 11 "Claude Sonnet 5.5", 10 "Claude Opus 5.5 (1M context)", 6 "Claude Fable 5.1", and 1 each Opus 5, Haiku 5.5 and Opus 4.8. Only 2 are plain "Claude".
  - October 2025: all 109 trailers in 100 commits were plain "Claude <noreply@anthropic.com>".
  - So 2026 commits carry the generating model version by construction. PR bodies do not, but they can be joined to their commits.
  - Median commit message length was 41 words (Oct 2026) and 73 words (Oct 2025), excluding trailers.
  - [query](https://api.github.com/search/commits?q=%22Co-Authored-By:+Claude%22+committer-date:2026-10-01..2026-10-31&sort=committer-date)
- **Repo licenses and age (MEASURED, 20 unique repos from the Oct 2026 Claude Code PR sample).**
  - Licenses: MIT 7, Apache-2.0 2, GPL/AGPL 3, NOASSERTION 2, no license 6.
  - Creation dates: 17 in 2026, 2 in 2025, 1 in 2013.
  - Most have 0-52 stars (one has 10,842).
  - Pre-2023 PRs: 0 in all 20 repos, including the 2013 one.
  - So "most public repos are MIT/Apache" holds for under half here, and same-repo pre-2023 human PRs basically do not exist for these repos.
  - [repos API](https://docs.github.com/en/rest/repos/repos#get-a-repository); [example pre-2023 query](https://api.github.com/search/issues?q=repo:we-promise/sure+is:pr+created:%3C2023-01-01)

#### B. Scientific publishing: mandatory AI-use declarations

**Elsevier's required statement**
- Heading: "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process". The policy was updated June 2026; the earlier heading was "...in the writing process".
- Template: "During the preparation of this work, the author(s) used [NAME OF TOOL / SERVICE] in order to [REASON]", followed by a sentence saying the authors reviewed and edited the content and take full responsibility.
- Placement: a separate section just before the references.
- Exempt: basic grammar, spelling and punctuation checks.
- Source: [Elsevier generative AI policies](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals)

**Other publishers and venues**
- **Springer Nature.** LLM use must be documented in Methods (or acknowledgements or preface for books). "AI-assisted copy editing" for readability, style or error correction does not need to be declared. So Springer Nature declarations under-count polishing. — [Springer Nature AI guidance](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities)
- **ICLR 2026.** Any LLM use must be disclosed in the paper and the submission form. Significant use goes in a separate section, which can be an appendix outside the page limit. Undisclosed extensive use leads to desk rejection. — [ICLR 2026 LLM policy blog](https://blog.iclr.cc/?p=1046); [ICLR author guide](https://iclr.cc/Conferences/2026/AuthorGuide)
- **ACL.** The Responsible NLP checklist item E1 reads "If you used AI assistants, did you include information about their use?" The 2026 ACL Anthology publishes per-paper checklist PDFs as attachments, and authors answer inconsistently (some untick E1 despite using AI to "refine and revise phrasing"). — [example 2026.acl-long.776 checklist](https://aclanthology.org/attachments/2026.acl-long.776.checklist.pdf); [2026.findings-acl.1232 checklist](https://aclanthology.org/attachments/2026.findings-acl.1232.checklist.pdf)

**Europe PMC full-text counts by publication year (MEASURED; format is all / OPEN_ACCESS:y / LICENSE:"cc by")**
- **Elsevier positive template** ("reviewed and edited the content as needed and take full responsibility"):
  - 2023: 130 / 106 / 59
  - 2024: 1,059 / 969 / 517
  - 2025: 3,405 / 3,139 / 2,008
  - 2026 YTD: 8,478 / 8,062 / 5,289
  - [query](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22reviewed%20and%20edited%20the%20content%20as%20needed%20and%20take%20full%20responsibility%22%20AND%20PUB_YEAR:2026&format=json&pageSize=1)
- **Elsevier declaration heading, old wording** (covers positive and negative declarations): 2023: 259; 2024: 1,736; 2025: 4,590; 2026: 7,679 (CC BY 3,964). The new June 2026 heading had 2,236 hits in 2026. — [query](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Declaration%20of%20generative%20AI%20and%20AI-assisted%20technologies%20in%20the%20writing%20process%22%20AND%20PUB_YEAR:2026&format=json&pageSize=1)
- **MDPI positive template** ("have reviewed and edited the output and take full responsibility for the content of this publication"): 2024: 6; 2025: 2,453; 2026: 6,944. MDPI is fully CC BY. — [query](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22have%20reviewed%20and%20edited%20the%20output%20and%20take%20full%20responsibility%20for%20the%20content%20of%20this%20publication%22%20AND%20PUB_YEAR:2026&format=json&pageSize=1)
- **Frontiers** (fully CC BY):
  - Positive "declare that Gen AI was used in the creation of this manuscript": 2024: 36; 2025: 1,590.
  - Negative "declare that no Gen AI was used..." plus the "no Generative AI..." variant: about 54.7k in 2025 (19,705 + 35,042).
  - All variants fall to under 300 in 2026, so the template wording changed in 2026.
  - [query](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22declare%20that%20Gen%20AI%20was%20used%20in%20the%20creation%20of%20this%20manuscript%22%20AND%20PUB_YEAR:2025&format=json&pageSize=1)
- **Broad upper bounds (noisy):**
  - `"used ChatGPT" AND (readability OR language)`: 2026: 13,500 (CC BY 9,877). This includes studies about ChatGPT.
  - Generic declaration headings: 2026: 16,163.
  - "no generative AI"-type statements: 2025: 80,081; 2026: 96,793.
  - [query base](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22used%20ChatGPT%22%20AND%20PUB_YEAR:2026&format=json&pageSize=1)

**OpenAlex full-text counts (MEASURED; format is all works / arXiv as primary location)**
- "reviewed and edited the content as needed": 2023: 746 / 34; 2024: 4,821 / 103; 2025: 13,257 / 412; 2026: 33,753 / 1,735.
- "LLMs were used": 2026: 1,503 / 573.
- "ChatGPT was used to": 2026: 8,509 / 703.
- [query](https://api.openalex.org/works?filter=fulltext.search:%22reviewed%20and%20edited%20the%20content%20as%20needed%22,publication_year:2026)

**arXiv**
- The arXiv API searches metadata fields only (title, author, abstract, comments, journal ref, category, ID), not full text. Acknowledgment and declaration harvesting needs bulk source or PDF download. — [arXiv API user manual](https://info.arxiv.org/help/api/user-manual.html)
- arXiv papers carry a mix of licenses, and many use the non-exclusive arXiv license rather than CC. — [arXiv license page](https://info.arxiv.org/help/license/index.html)

#### C. Grokipedia: AI-written encyclopedia, labeled by construction

**Size**
- The sitemap URL dataset `caentzminger/grokipedia-urls` (refreshed weekly) has 5,857,612 rows (MEASURED via the HF datasets-server size endpoint). — [HF dataset](https://huggingface.co/datasets/caentzminger/grokipedia-urls)
- A press report gives "more than 6 million articles" and "over 1.1 million approved edits" as of October 2026 (REPORTED). — [Basenor](https://www.basenor.com/blogs/news/grokipedia-calls-for-community-edits-6m-article-milestone); [Wikipedia: Grokipedia](https://en.wikipedia.org/wiki/Grokipedia)

**v0.1 scrape (Triedman & Mantzarlis)**
- 883,858 articles, about 99.8% of the 885,279 at launch (late Oct / early Nov 2025).
- 496,058 (56%) carry the notice "The content is adapted from Wikipedia, licensed under Creative Commons Attribution-ShareAlike 4.0 License".
- Mean chunk similarity to Wikipedia: 0.90 for CC-licensed articles vs 0.77 (bimodal) for the rest.
- The median non-CC article is about 4.6x longer than its Wikipedia counterpart.
- The dump is on HF as NDJSON.
- Source: [arXiv 2511.09685 (HTML)](https://arxiv.org/html/2511.09685); [HF dump htriedman/grokipedia-v0.1-dump](https://huggingface.co/datasets/htriedman/grokipedia-v0.1-dump)

**License**
- Most articles use the X Community License (non-commercial and research use; commercial use limited by xAI's Acceptable Use Policy). Wikipedia-derived articles are CC BY-SA 4.0. — [Wikipedia: Grokipedia](https://en.wikipedia.org/wiki/Grokipedia)

#### D. Labeled-by-construction chat logs and synthetic corpora (HF metadata MEASURED 2026-11-07)

**WildChat-4.8M**
- ODC-BY, ungated. 3,199,860 non-toxic conversations from 4,804,190 collected; the full version is manually gated. Data runs up to but excluding 2025-08-01. — [HF card](https://huggingface.co/datasets/allenai/WildChat-4.8M)
- Model mix, MEASURED by reading the `model` and `timestamp` columns of all 86 parquet shards:

  | Model | Conversations |
  |---|---|
  | gpt-4o-2024-08-06 | 782,393 |
  | gpt-4o-mini-2024-07-18 | 643,147 |
  | gpt-4.1-mini-2025-04-14 | 634,037 |
  | gpt-3.5-turbo-0613 | 347,770 |
  | gpt-3.5-turbo-0301 | 179,157 |
  | gpt-3.5-turbo-0125 | 161,973 |
  | gpt-4-1106-preview | 91,226 |
  | gpt-4o-2024-05-13 | 83,084 |
  | gpt-4-0125-preview | 64,106 |
  | o1-mini | 58,529 |
  | o1-preview | 53,307 |
  | gpt-4-0314 | 47,581 |
  | gpt-4o-2024-11-20 | 31,156 |
  | gpt-4-turbo-2024-04-09 | 22,392 |

- Months run from 2023-04 to 2025-07, peaking at 443,691 (Oct 2024) and 429,722 (Nov 2024). — [HF parquet files](https://huggingface.co/datasets/allenai/WildChat-4.8M/tree/main/data)
- **WildChat-1M**: ODC-BY, 2023-04 to 2024-05, GPT-3.5 and GPT-4 only. — [HF card](https://huggingface.co/datasets/allenai/WildChat-1M); [WildChat paper](https://arxiv.org/abs/2405.01470)

**LMArena releases**
- **arena-human-preference-140k**: 135,634 votes, so about 271k model responses. Dates 2025-04-17 to 2025-07-24, 52% English. Prompts are CC-BY-4.0; "model outputs are governed by the terms of use set by the respective model providers".
  - Top models by battle count, model_a slot: claude-opus-4-20250514 (4,957), gemini-2.5-flash (4,911), mistral-medium-2505, gemini-2.5-pro, qwen3-235b, o3-2025-04-16, claude-sonnet-4, chatgpt-4o-latest-20250326, deepseek-r1-0528, gpt-4.1, grok-3.
  - [HF card](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k)
- **arena-expert-5k** (Nov 2025): 5,128 expert-vote rows including claude-opus-4-1, kimi-k2 and qwen3-235b-2507, with occupational tags. — [HF card](https://huggingface.co/datasets/lmarena-ai/arena-expert-5k)
- **search-arena-24k**: 24,069 conversations from 2025-03-18 to 2025-05-08, with search-grounded answers from Perplexity Sonar variants, gpt-4o-search-preview and Gemini 2.5 grounding. Same terms split as above. — [HF card](https://huggingface.co/datasets/lmarena-ai/search-arena-24k)

**Older and stale logs**
- **LMSYS-Chat-1M**: 1M conversations with 25 LLMs from 2023, gated under a custom license. — [arXiv 2309.11998](https://arxiv.org/abs/2309.11998); [HF](https://huggingface.co/datasets/lmsys/lmsys-chat-1m)
- **Chatbot Arena conversations**: 33k, 2023, gated. — [HF](https://huggingface.co/datasets/lmsys/chatbot_arena_conversations)
- **ShareGPT_Vicuna_unfiltered**: tagged apache-2.0 by the uploader, but it is scraped 2023 ChatGPT shares. — [HF](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered)
- **UltraChat**: MIT, 2023 ChatGPT API. — [HF](https://huggingface.co/datasets/stingning/ultrachat)
- **Anthropic HH-RLHF**: MIT, Dec 2022 Anthropic model. — [HF](https://huggingface.co/datasets/Anthropic/hh-rlhf)
- **Magpie**: Llama 3 / 3.3 licenses. — [HF](https://huggingface.co/datasets/Magpie-Align/Magpie-Llama-3.3-Pro-1M-v0.1)

**Synthetic informational corpora (AI by construction)**
- **Cosmopedia**: Apache-2.0, 10M-100M size category. Mixtral-generated textbooks, blog posts, WikiHow-style and educational pieces. Viewer configs show auto_math_text with 1,191,606 rows (MEASURED). — [HF](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia); [Cosmopedia blog](https://huggingface.co/blog/cosmopedia)
- **Nemotron-Post-Training-Dataset-v1**: CC-BY-4.0, July 2025. — [HF](https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v1)

**Detection benchmarks with paired human text**
- **HC3**: CC-BY-SA-4.0. 48,644 viewer rows across configs (MEASURED). Human and ChatGPT answers to the same questions (ELI5, open_qa, wiki_csai, finance, medicine). — [HF](https://huggingface.co/datasets/Hello-SimpleAI/HC3); [arXiv 2301.07597](https://arxiv.org/abs/2301.07597)
- **RAID**: MIT. 4,981,100 viewer rows (MEASURED). 11 generators across domains including abstracts, news, wiki, reviews and recipes. — [HF](https://huggingface.co/datasets/liamdugan/raid); [arXiv 2405.07940](https://arxiv.org/abs/2405.07940)
- **Kaggle "LLM - Detect AI Generated Text"**: student persuasive essays, about 1,378 labeled training essays, poor register fit. — [project page citing train_essays.csv](https://bt5153msba.github.io/project/pyp2024/group02.pdf); [i-programmer](https://www.i-programmer.info/news/204-challenges/16731-kaggle-contest-to-detect-chatbot-essays.html)

#### E. News and publishers with AI disclosures (mostly small, copyrighted)

- **CNET Money**: 77 AI-assisted explainers (Nov 2022 to Jan 2023), about 1% of CNET output. Bylined "CNET Money Staff", later "CNET Money". The disclosure was a variant of "This article was assisted by an AI engine and reviewed, fact-checked and edited by our editorial staff". 41 of the 77 needed corrections (REPORTED). — [Engadget](https://www.engadget.com/cnet-corrected-41-of-its-77-ai-written-articles-201519489.html); [Futurism on disclaimer](https://futurism.com/cnet-adds-disclaimer-articles-ai)
- **AP automated earnings stories**: tagline "This story was generated automatically by Automated Insights" with Zacks data. About 3,000 per quarter (2015) up to about 4,700 (Q1 2018) (REPORTED). These are template natural-language generation from before LLMs, not LLM text. — [Poynter](https://www.poynter.org/news/aps-robot-written-stories-have-arrived); [ir-impact](https://www.ir-impact.com/2018/06/how-automated-financial-news-changing-quarterly-earnings-coverage)
- **Gannett / LedeAI**: high-school sports recaps credited to LedeAI. Paused late August 2023 after mockery (REPORTED). — [CNN](https://edition.cnn.com/2023/08/30/tech/gannett-ai-experiment-paused)
- **Quartz "Quartz Intelligence Newsroom"** byline (G/O Media): roughly 400-word aggregated articles from January 2025, with an AI warning note. Editors reportedly review each one. Total count not found. — [TechCrunch](https://techcrunch.com/2025/01/27/quartz-has-been-quietly-publishing-ai-generated-news-articles); [Futurism](https://futurism.com/quartz-ai-generated-articles-slop-errors)
- **Hoodline**: AI-written local news under human-sounding persona bylines, with a small "AI-assisted" badge added after criticism, across about 25 cities (REPORTED 2024). — [Nieman Lab](https://www.niemanlab.org/2024/06/whats-in-a-byline-for-hoodlines-ai-generated-local-news-everything-and-nothing/)
- **Patch**: AI newsletters scaled to about 30,000 US communities in 2025 (REPORTED). I could not confirm the disclosure wording. — [Axios](https://www.axios.com/2025/03/04/patch-news-ai-newsletters-local-communities)
- **US newspaper audit**: 186,507 articles from 1,528 newspapers (summer 2025). About 9% were AI or mixed per the Pangram detector. In a manual audit of 100 AI-flagged articles, 95% of authors did not disclose. So disclosed AI news is a small minority. — [arXiv 2510.18774](https://arxiv.org/abs/2510.18774)
- **AI labels in 2026**: 24% of people across nine countries had seen an "AI-made" label in the past week, and the BBC uses "How we used AI" labels (REPORTED). — [Reuters Institute 2026](https://reutersinstitute.politics.ox.ac.uk/generative-ai-and-news-report-2026-standalone-tools-information-infrastructure)

#### F. Platform AI text with UI labels

- **LinkedIn Collaborative Articles** (launched March 2023): articles start from "AI-powered conversation starters", and experts add contributions. — [LinkedIn news](https://news.linkedin.com/2023/march/collaborative-articles)
  - Size: reportedly 10M pages in one year (REPORTED). — [Search Engine Journal](https://www.searchenginejournal.com/how-linkedin-unlocked-a-genius-seo-strategy/511227/)
  - Status: Top Voice badges were retired. Whether the articles are read-only or still active in 2025-26 is disputed. — [Social Media Today](https://www.socialmediatoday.com/news/linkedins-removing-top-voice-badges-collaborative-articles/728247/); [Closely](https://blog.closelyhq.com/linkedin-collaborative-articles-complete-contributor-guide); [contentin.io](https://contentin.io/glossary/collaborative-article/)
  - Retrievability: Common Crawl indexes CC-MAIN-2025-05 and CC-MAIN-2024-33 return 0 blocks for `www.linkedin.com/advice/*` (MEASURED). The Wayback CDX has 63 index pages of captures for the `linkedin.com/advice/` prefix (MEASURED). — [CC index API](https://index.commoncrawl.org/CC-MAIN-2025-05-index?url=www.linkedin.com/advice/*&output=json&showNumPages=true); [Wayback CDX](https://web.archive.org/cdx/search/cdx?url=linkedin.com/advice/&matchType=prefix&showNumPages=true)
- **Amazon "Customers say"**: a paragraph labeled "AI-generated from the text of customer reviews", built from verified-purchase reviews. — [About Amazon](https://www.aboutamazon.com/news/retail/amazon-ai-generated-review-highlights)
- **Medium**: requires AI-assisted stories to be disclosed within the first two paragraphs. Undisclosed AI text is limited to network-only distribution, and AI content cannot be paywalled. There is no public label field to filter on. — [Medium help: AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)
- **Google AI Overviews**: a Hugging Face search for AI-overview datasets (MEASURED) found only derived traffic and citation panels with no answer text, e.g. `audiofreak7/wikipedia-ai-overviews-panels-2026-09` ("Derived counts and metrics only. No article text"). — [HF dataset](https://huggingface.co/datasets/audiofreak7/wikipedia-ai-overviews-panels-2026-09)
- **DeepWiki** (Cognition): AI-generated documentation for over 50,000 top public repos at launch, May 2025 (REPORTED). Only small community scrapes exist on HF. — [Cognition blog](https://cognition.com/blog/deepwiki); [HF archit11/deepwiki](https://huggingface.co/datasets/archit11/deepwiki)

### Inferences

**Ranking for quill negatives** (volume x informational register x recency of generating model, with terms as a gate)

| Rank | Source | Volume | Register fit | Generators | Terms | Notes |
|---|---|---|---|---|---|---|
| 1 | GitHub agent PR/issue bodies (Claude Code footer, Cursor marked span, Devin, Copilot, Jules; CodeRabbit summary spans) | Tens of millions (MEASURED); >=150-word bodies are about 69% of Claude Code PRs | Good for "docs/memo" style: problem/approach/testing; markdown-heavy and code-laden | Claude 4.x-5.x, GPT-5.x, Gemini 2.5-3.x, 2025-26 | Text is retrievable via REST/GraphQL; GH Archive after Oct 2025 gives only PR IDs (MEASURED); redistribution rights unclear | Best by far |
| 2 | Scientific papers with positive AI declarations in PMC OA CC BY (Elsevier template, MDPI, Frontiers 2025) | About 5k-15k CC BY per year in 2026 (MEASURED subsets) | Analytical-scientific | Mostly ChatGPT-class | CC BY | Document-level label on mostly human text, so a weak, mixed signal |
| 3 | Grokipedia non-Wikipedia-derived articles | About 385k in v0.1; up to several million URLs in 2026 | Encyclopedic explainer, high fit | Grok, 2025-26 | Research/non-commercial | Filter out near-Wikipedia chunks |
| 4 | LMArena 2025 releases + search-arena-24k | About 271k + 48k responses | Q&A explainers; search-arena is the legal proxy for answer-engine prose | Many 2025 frontier models | Prompts CC-BY; outputs under provider ToS | Model-diverse |
| 5 | WildChat-4.8M informational subset | 3.2M conversations, needs intent filtering | Mixed | GPT-4o / 4.1-mini, to Jul 2025 | ODC-BY | |
| 6 | Cosmopedia and similar synthetic corpora | Huge | Exact fit (textbook / blog / how-to) | Stale generators (Mixtral, 2024) | Apache-2.0 | Good bulk "generic explainer" negatives |
| 7 | HC3 / RAID | Large | Mixed | Older (2022-24) | Open | Paired human text by construction |
| 8 | News with AI labels (CNET 77, Quartz, AP template NLG, Hoodline) | Small or non-LLM | News | Mixed | Copyrighted, Wayback-only | Low value |
| 9 | UI-labeled platform text (LinkedIn CA, Amazon, Google AI Overviews, Yelp, Reddit Answers) | Large in principle | Varies | Varies | Not legally harvestable at volume (ToS / anti-scraping; absent from CC); ESTIMATED from the CC absence and the lack of datasets | Effectively closed |

Further inferences:
- **Extracting the AI span.** For quill, the most valuable property of the GitHub sources is that many carry exact begin/end markers. This lets one extract the AI span without human editing around it: the CodeRabbit block, the `CURSOR_AGENT_PR_BODY_BEGIN/END` span, and Copilot/Devin/Jules bot-authored bodies. The Claude Code footer marks the whole body, but humans may have edited it.
- **Clearing the 10k bar.** Clearing ">=10k informational docs" with English, >=150-word, marker-bounded text needs only a few days of Oct 2026 Claude Code or Cursor PRs. Applying the measured rates (0.94 Latin x 0.69 >=150 words) to 7.29M gives about 4.7M qualifying Claude Code PR bodies in October 2026 alone (ESTIMATED).
- **Rate limits are the bottleneck, not volume.** Search returns at most 1,000 results per query, so harvesting needs date-sliced queries at roughly 30/min, or GH Archive to enumerate PR IDs plus GraphQL to fetch the bodies.
- **Grokipedia** is the only large self-labeled source in the encyclopedic-explainer register written by a 2025-26 model. Its Wikipedia derivation means it needs a chunk-level similarity filter against the matched Wikipedia article before use.
- **The scientific declarations** add an analytical register and same-venue human controls, but they label documents, not spans. The declared use is mostly language polishing.

- **GH Archive no longer carries PR text.** GitHub announced that Activity Events API payloads would be slimmed from 2025-10-07 ([GitHub changelog 2025-08-08](https://github.blog/changelog/2025-08-08-upcoming-changes-to-github-events-api-payloads/)). In GH Archive hour 2026-10-15-12, I parsed 969 PullRequestEvents (509 "opened"). The `pull_request` object had only `base, head, id, number, url`, and 0 of 969 had a body (MEASURED; [data.gharchive.org/2026-10-15-12.json.gz](https://data.gharchive.org/2026-10-15-12.json.gz)).
  - Consequence: bulk harvesting after Oct 2025 needs GH Archive (or search) to enumerate PR numbers, then REST or GraphQL calls to fetch the bodies.
  - At 5,000 GraphQL requests per hour with 100 PR nodes each, the ceiling is roughly 500k bodies per hour per token (ESTIMATED; not tested).

### Gaps
- GH Archive dumps from before 2025-10-07 should still contain full PR bodies, which covers the 2025 Codex, Copilot and early Claude Code era. I did not verify this.
- The legal status of PR and issue text: repo LICENSE files cover repo contents, while PR text is user content under the [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service). Whether training on it is permitted needs legal review. I did not find an explicit statement.
- Copilot agent PR counts fell from 315k (Mar 2026) to about 60k/month. I did not determine whether Copilot changed the authoring identity (e.g., PRs opened under the user with a co-author trailer).
- I found no 2026 Codex marker to replace the `chatgpt.com/codex/tasks` link. Branch-prefix (`codex/`) search was not tested.
- Precision was not measured for Sourcery, Gemini, OpenHands or Amp strings, or for commit-search totals. The commit totals are internally inconsistent (all-time 43.5M vs 2025 + 2026 = 22.8M).
- Quartz Intelligence Newsroom total article count, Patch newsletter disclosure wording, and BuzzFeed / Arena Group / Reach / MSN / Business Insider / Yahoo / Axel Springer AI-labeled volumes were not found. Searches surfaced no counts.
- LinkedIn Collaborative Articles' current (2026) status is disputed, and its article count is only a 2024 press figure.
- arXiv acknowledgment counts need bulk full text; OpenAlex's arXiv subset is a partial lower bound.
- The 2026 Frontiers declaration wording was not identified, so 2026 Frontiers counts are missing.

---

## Q2. Which give natural same-source human counterparts (pre-2023 or undisclosed) for contrast?

### Takeaway
The best contrast pairs come from sources where the same venue or page holds both an AI-labeled and a human version:
- Grokipedia vs the same-title Wikipedia article (881,743 mapped pairs; ideally pre-2023 Wikipedia revisions).
- Journals that require declarations and publish both positive and explicit negative statements (Frontiers 2025: about 1.6k positive vs about 54.7k "no Gen AI"; Elsevier and MDPI templates), plus the same journals before 2023.
- GitHub PRs from 2022 and earlier, though most AI-PR repos are new, so the counterpart is cross-repo rather than same-repo.
- HC3 / RAID (paired by construction) and OpenAssistant (human assistant-register replies).

### Cited Findings
- **Grokipedia to Wikipedia.** `lewoniewski/grokipedia-wikipedia-16-languages` maps 881,743 Grokipedia v0.1 pages to Wikipedia titles in 16 languages (Wikipedia/Wikidata dumps of 2025-11-01). Only 3,536 Grokipedia URLs had no Wikipedia match. Apache-2.0. — [HF](https://huggingface.co/datasets/lewoniewski/grokipedia-wikipedia-16-languages)
- **Similarity caveat.** CC-licensed Grokipedia articles average 0.90 chunk similarity to Wikipedia, and non-CC ones 0.77. So the human/AI contrast is strongest in the non-CC, lower-similarity subset (biographies, politics, controversial topics show lower similarity). — [arXiv 2511.09685](https://arxiv.org/html/2511.09685)
- **Frontiers 2025** (all CC BY, in PMC; MEASURED): 1,590 papers declare "Gen AI was used in the creation of this manuscript", against 19,705 + 35,042 that declare no Gen AI. — [EPMC query](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22declare%20that%20no%20Generative%20AI%20was%20used%20in%20the%20creation%20of%20this%20manuscript%22%20AND%20PUB_YEAR:2025&format=json&pageSize=1)
- **Elsevier and MDPI templates.** Pre-2023 counts of the template phrases are 0 (2022: 0 for every Elsevier phrase; MEASURED). Pre-2023 issues of the same journals are clean human controls by date. — [EPMC query](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22reviewed%20and%20edited%20the%20content%20as%20needed%20and%20take%20full%20responsibility%22%20AND%20PUB_YEAR:2022&format=json&pageSize=1)
- **GitHub baseline.** 75,617,364 PRs were created in 2022 (MEASURED), a huge pre-LLM-agent human pool, matchable by language and topic. — [query](https://api.github.com/search/issues?q=is:pr+created:2022-01-01..2022-12-31)
- **GitHub same-repo history.** 0 of 20 sampled repos with Oct 2026 Claude Code PRs had any PR created before 2023, and 17 of 20 were created in 2026 (MEASURED). The AI-PR population lives mostly in new repos, so the human counterpart must come from other, pre-2023 repos matched on language and domain, not from the same repo. — [example query](https://api.github.com/search/issues?q=repo:we-promise/sure+is:pr+created:%3C2023-01-01)
- **LinkedIn Collaborative Articles** pair the AI-generated starter text with human expert contributions (125-750 characters each, REPORTED) on the same page. They are blocked by terms and crawl absence (see Q1). — [Closely guide](https://blog.closelyhq.com/linkedin-collaborative-articles-complete-contributor-guide); [LinkedIn news](https://news.linkedin.com/2023/march/collaborative-articles)
- **Amazon review highlights** are generated from the human verified-purchase reviews on the same page, a natural pair. Retrieval at volume conflicts with Amazon's terms. — [About Amazon](https://www.aboutamazon.com/news/retail/amazon-ai-generated-review-highlights)
- **HC3** pairs human expert/community answers with ChatGPT answers to the same questions. **RAID** pairs generations with their human source domains. — [arXiv 2301.07597](https://arxiv.org/abs/2301.07597); [arXiv 2405.07940](https://arxiv.org/abs/2405.07940)
- **OpenAssistant oasst1/oasst2** (Apache-2.0) contain human-written assistant-style replies, a human counterpart in the chatbot-answer register. — [HF oasst2](https://huggingface.co/datasets/OpenAssistant/oasst2)
- **News counterparts.** CNET Money's human-written explainers before Nov 2022, and AP's roughly 300 per quarter human-written earnings stories before automation (REPORTED). — [AP via armenpress](https://armenpress.am/en/article/767841); [CNN on CNET](https://edition.cnn.com/2023/01/25/tech/cnet-ai-tool-news-stories)

### Inferences
- For quill's informational register, the strongest pair is Grokipedia (non-CC subset) vs pre-2023 Wikipedia revisions of the same title. It is topic-matched, register-matched (encyclopedic explainer) and at scale (hundreds of thousands of pairs).
- In GitHub, PRs within a repo that lack an AI marker in 2026 are not reliably human, because markers can be turned off. Use pre-2023 PRs as the human side and match on repo language and topic.
- The Frontiers 2025 negative-declaration set (about 55k CC BY papers) is a rare explicitly self-declared human set from 2025. It is a contemporaneous control for the same journals, though a negative declaration is self-report, not proof.

### Gaps
- I did not measure how many Claude Code / Cursor PR repos have meaningful pre-2023 PR history beyond the 20-repo sample above.
- No source gives span-level human/AI alignment except CodeRabbit- and Cursor-style marker blocks inside otherwise human PR bodies, which are mixed documents. That mixing could be exploited as within-document contrast.

---

## Q3. What biases come with self-disclosure?

### Takeaway
Self-disclosed AI text is a biased sample of AI text:
- **Defaults over intent.** It over-represents tools that label by default (Claude Code footers, bot authors) and users who did not switch the label off.
- **Effort.** It over-represents reviewed, higher-effort output (publishers promise "reviewed, fact-checked and edited").
- **Polish vs generation.** In science it is mostly AI-polished human text.
- **Model and template confounds.** It is tied to tool-specific templates and single model families, which a style model can learn instead of "AI-ness".
- **Unlabeled slop is much larger.** Undisclosed AI text, the slop quill most wants to avoid, is far more common (95% non-disclosure in the newspaper audit).

### Cited Findings
- **Disclosure is rare in news.** In 100 AI-flagged newspaper articles, 95% of authors and 91% of publishers did not disclose AI use. Opinion pages at NYT / WaPo / WSJ were 6.4x more likely to contain AI than their news articles. So disclosed AI news is unrepresentative of AI news. — [arXiv 2510.18774](https://arxiv.org/abs/2510.18774); [Pangram summary search result](https://www.pangram.com/ai-news)
- **Disclosed AI news is error-prone.** A Pangram-based study reports 41% of AI-labeled news contained at least one hallucinated claim, against 5% of predicted-human articles. That is detector-based, REPORTED. — [Nieman Lab 2026](https://www.niemanlab.org/2026/06/how-should-news-organizations-label-their-ai-use-for-audiences-new-studies-suggest-some-answers/)
- **Publisher disclosures imply review.** CNET: "reviewed, fact-checked and edited by our editorial staff". Quartz: editors review each AI story. Disclosed items are human-reviewed AI. — [Futurism](https://futurism.com/cnet-adds-disclaimer-articles-ai); [TechCrunch](https://techcrunch.com/2025/01/27/quartz-has-been-quietly-publishing-ai-generated-news-articles)
- **Scientific declarations are mostly language polishing**:
  - Elsevier's template requires the authors to state they "reviewed and edited the content".
  - Springer Nature exempts AI copy editing from disclosure altogether.
  - ACL authors inconsistently tick E1 when AI was used "only to refine and revise phrasing".
  - [Elsevier](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals); [Springer Nature](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities); [ACL checklist examples](https://aclanthology.org/attachments/2026.findings-acl.1675.checklist.pdf)
- **Disclosure strings are opt-out and drift over time.** Claude Code lets users change or hide its commit and PR attribution ([settings reference](https://code.claude.com/docs/en/settings-reference.md)). Aider's "(aider)" author suffix can be disabled ([Aider docs](https://aider.chat/docs/git.html)). Measured drift:
  - The Codex task-link marker fell from 426,398 (Oct 2025) to 97 (Dec 2025).
  - Frontiers' 2025 template phrases nearly vanish in 2026.
  - Elsevier's heading changed in June 2026.
  - [Codex query](https://api.github.com/search/issues?q=is:pr+in:body+%22chatgpt.com/codex/tasks%22+created:2025-12-01..2025-12-31)
- **Template confounds (MEASURED in samples).**
  - Jules bodies use fixed emoji section templates.
  - Copilot fills repo PR templates and appends a machine suffix.
  - Devin and Jules append session links.
  - 5% of Claude Code PRs also contain a CodeRabbit block, so multiple AI tools stack in one body.
  - [sample query](https://api.github.com/search/issues?q=is:pr+author:app/google-labs-jules+created:2026-10-01..2026-10-31)
- **Grokipedia is partly human and partly copied.** Over 1.1 million approved community edits are REPORTED, and 56% of v0.1 articles are adapted from Wikipedia. — [Basenor](https://www.basenor.com/blogs/news/grokipedia-calls-for-community-edits-6m-article-milestone); [arXiv 2511.09685](https://arxiv.org/html/2511.09685)
- **Generic phrases are unreliable.** "Generated by Claude" matched 2.87M October 2026 PRs, but only 1% literally contained the phrase (MEASURED). Count-based harvesting must use tool-specific markers. — [query](https://api.github.com/search/issues?q=is:pr+in:body+%22Generated+by+Claude%22+created:2026-10-01..2026-10-31)

### Inferences
- **Effort and review bias.** Disclosed GitHub agent text is probably higher-effort than average slop, because agents write structured PR descriptions with test plans and are reviewed in-repo. Disclosed news is human-reviewed. As negatives, these sources teach quill to avoid competent, polished AI style, which is likely what matters for a style model. They under-represent low-effort content-farm slop; pair them with the social-media and Wikipedia-tag slices from other researchers.
- **Model-family confound.** Each source maps to roughly one model family (Claude Code to Claude; Grokipedia to Grok; WildChat to OpenAI). A classifier or contrastive objective trained on one source will partly learn model-family quirks. Mix sources, or balance by model, using LMArena's labeled model field.
- **Polishing confound.** Scientific "AI-polished" papers should be treated as a separate label, "AI-edited human", not as AI negatives. They are useful for learning which surface edits read as AI, not as fully generated prose.
- **Boilerplate must be stripped before training.** Marker comments, footers, session links and emoji templates would otherwise become trivial shortcuts.
- **Language and register skew.** About 6% of Claude Code PR bodies and about 14% of its issues are mostly non-Latin script (MEASURED). PR text is code-dense (inline code, file paths), so an informational-prose filter is needed: for example, drop bodies where more than 20% of tokens are in code spans.

### Gaps
- There is no quantitative estimate of how often users remove default AI attribution (the undisclosed share of Claude Code / Cursor output), so the coverage of self-disclosure is unknown.
- I did not measure how much humans edit agent PR bodies after generation. Comparing the PR body's edit history (`userContentEdits` in GraphQL) would quantify it.
- Whether disclosed scientific text differs measurably from undisclosed AI-polished text has not been tested.
