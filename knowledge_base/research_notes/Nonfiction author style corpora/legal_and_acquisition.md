# Legal, ethical and practical considerations for a single-author style corpus (personal, local fine-tune), and the technical implications of targeting a famous author

Research summary current to 7 November 2026. This is not legal advice. Most legal sources are law-firm alerts, trackers and news reports. Where I read only secondary coverage, I say so, and courts' exact wording should be checked against the opinions. "Observed" means I fetched the live file myself on 2026-11-07.

## 1. US legal state of play (Nov 2026) and what it means for a private, local, non-commercial fine-tune on one author's freely readable posts

### Takeaway
No US court has ruled on an individual's private, non-commercial fine-tune. The two generative-AI rulings from June 2025 (Bartz, Kadrey) held that training itself was fair use. The legal exposure sits at the edges: how the copies were obtained and kept, and outputs that reproduce the author's text. The only appellate ruling, Thomson Reuters v. Ross (3d Cir., 29 Sept 2026), went against the AI developer. It concerned a commercial, non-generative product that competed with the plaintiff, and the court expressly declined to decide the generative-AI question. The fourth fair-use factor (market effect) is now the main battleground, through "market dilution". A model built to imitate one named author is the use case that theory, and the Chakrabarty/Ginsburg paper, target most directly.

### Cited Findings

**Bartz v. Anthropic (N.D. Cal.)**
- 23 June 2025 (Judge Alsup), partial summary judgment. Training Claude on books was fair use: "transformative—spectacularly so" — [Norton Rose Fulbright, Mar 2026](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- Scanning print books Anthropic had bought was also fair use. The digital copy was treated like the purchased print copy placed in the library, and the print original was destroyed. Downloading more than 7 million pirated books (Books3, LibGen, PiLiMi) to build a "permanent, general-purpose library" was not excused by fair use — [Akin Gump](https://www.akingump.com/en/insights/ai-law-and-regulation-tracker/district-court-rules-ai-training-can-be-fair-use-in-bartz-v-anthropic); [ChatGPT Is Eating the World, 24 Jun 2025](https://chatgptiseatingtheworld.com/2025/06/24/judge-alsup-grants-partial-summary-judgment-to-anthropic-ruling-training-copies-were-fair-use-but-judge-rules-no-fair-use-in-pirated-copies-of-books-used-to-build-a-central-library-they-are-infring/)
- Alsup compared training to teaching students to write: copyright targets copying, not rivals who learned from earlier works — [Ballard Spahr, Oct 2026](https://www.ballardspahr.com/insights/alerts-and-articles/2026/10/third-circuit-addresses-fair-use-in-ai-training-but-leaves-generative-ai-questions-unresolved)
- Settlement of $1.5B, about $3,000 per work — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- Final approval on 20 July 2026 (Judge Araceli Martínez-Olguín):
  - 482,460 works on the list; all 53 objections overruled.
  - The release covers conduct through 25 Aug 2025 and does not release claims about AI outputs or future conduct.
  - Appeals of the approval have been filed, so disbursement waits on them.
  - Sources: [JURIST, Jul 2026](https://www.jurist.org/news/2026/07/judge-approves-record-1-5-billion-settlement-involving-anthropic/); [Writer Beware, 23 Jul 2026](https://writerbeware.blog/2026/07/23/anthropic-settlement-update-final-settlement-approved/); [AAP](https://publishers.org/news/aap-welcomes-courts-final-settlement-approval-in-bartz-v-anthropic/)
  - Claims-rate figures differ: 91.3% in the motion vs. 92.77% per AAP. The final fee figure is also reported differently across sources.

**Kadrey v. Meta (N.D. Cal., No. 23-cv-03417-VC)**
- 25 June 2025 (Judge Chhabria): summary judgment for Meta on fair use, and for Meta on the DMCA claims. The plaintiffs "failed to develop a record in support of the right one" [argument] — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- Market dilution, in dicta. Training could harm the market by "helping to enable the rapid generation of countless works that compete with the originals, even if those works aren't themselves infringing". Chhabria said it "seems likely that market dilution will often cause plaintiffs to decisively win the fourth factor" — [Authors Alliance, 26 Jun 2025](https://www.authorsalliance.org/2025/06/26/meta-wins-on-fair-use-for-now-but-court-leaves-door-open-for-market-dilution/)
- Commentators read the dicta as suggesting most unauthorized commercial genAI training would be illegal. I could not verify the exact phrase "in many circumstances it will be illegal" against the opinion — [FisherBroyles](https://fisherbroyles.com/news/client-alert-summary-and-strategic-analysis-of-judge-chhabrias-fair-use-ruling-in-kadrey-v-meta)
- The ruling binds only these 13 plaintiffs on this record.
- On 11 Dec 2025 the plaintiffs moved to add a contributory-infringement claim over alleged torrent "seeding" — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)

**Thomson Reuters v. ROSS Intelligence**
- District court (D. Del., Judge Bibas), 11 Feb 2025: partial summary judgment for Thomson Reuters (TR). The headnotes were original and ROSS's copying was not fair use. Interlocutory appeal certified on 23 May 2025 ("the questions here are hard") — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- 3d Cir. No. 25-2153, decided 29 Sept 2026; opinion initially sealed, unsealed around 1 Oct 2026. It affirmed, and is the first federal appellate fair-use decision on AI training — [IPWatchdog, 30 Sep 2026](https://ipwatchdog.com/2026/09/30/third-circuit-affirms-revised-fair-use-ruling-against-ross-ai-legal-research-platform-in-sealed-opinion/); [Plagiarism Today, 1 Oct 2026](https://www.plagiarismtoday.com/2026/10/01/understanding-the-reuters-ross-ai-ruling/)
- Factor 1: the use was commercial and only minimally transformative. Copying only during training did not change the use's purpose.
- Factor 4: harm to the legal-research market and to a "rapidly developing" market for licensing AI training data.
- Intermediate-copying software cases (Sega, Connectix) were rejected.
- The opinion carves out generative AI: "Unlike the AI models in *Bartz* and *In re: OpenAI*, ROSS's AI platform cannot generate original expression…" — [Ballard Spahr](https://www.ballardspahr.com/insights/alerts-and-articles/2026/10/third-circuit-addresses-fair-use-in-ai-training-but-leaves-generative-ai-questions-unresolved)
- LawNext reports the court leaned on *Warhol v. Goldsmith*, rejected reliance on *Authors Guild v. Google*, and did not reach the Key Number System — [LawNext, Oct 2026](https://www.lawnext.com/2026/10/no-more-than-an-ordinary-copyright-case-3rd-circuit-unseals-its-opinion-in-thomson-reuters-case-against-ross.html)
- In April 2026 the Third Circuit ordered supplemental briefing on its own recent UpCodes decision, which had found likely fair use — [ChatGPT Is Eating the World, 27 Apr 2026](https://chatgptiseatingtheworld.com/2026/04/27/third-circuit-orders-thomson-reuters-ross-intelligence-to-file-supplemental-briefs-on-third-circuits-recent-decision-finding-likely-fair-use-by-upcodes/)
- Sources conflict on originality. Ballard Spahr and FindLaw say the court found the headnotes original. One search summary of LawNext mentioned the merger doctrine. Check the opinion.

**NYT v. Microsoft & OpenAI / In re OpenAI Copyright Litigation (S.D.N.Y., MDL No. 1:25-md-03143)**
- The case is pending. Motions to dismiss were largely denied in 2025, and no fair-use ruling has issued — [Axios, 1 Apr 2025](https://www.axios.com/2025/04/01/nyt-openai-microsoft-lawsuit-advances); [kb3k digest](https://kb3k.github.io/ai-copyright-digest/cases/nyt-v-openai.html)
- Discovery orders compelled 20M ChatGPT output logs (5 Jan 2026) and further pools of 78M and 10M logs (9 Mar 2026) — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- NYT amended its complaint on 25 June 2026. It dropped contributory infringement against OpenAI and the trademark claims, citing the Supreme Court's 25 Mar 2026 *Cox Communications* decision on secondary liability — [Giga Law, 27 Jun 2026](https://giga.law/daily-news/2026/6/27/new-york-times-amends-copyright-suit-against-openai-microsoft)
- US DOJ Statement of Interest, about 1 Sept 2026 (some reports say 2 Sept):
  - It urged that training be analyzed separately from outputs, called training on text standing alone a highly transformative fair use, and called market dilution a "deeply flawed theory".
  - It does not bind the court. Critics note the government was reportedly negotiating a stake in OpenAI.
  - Sources: [Sterne Kessler](https://www.sternekessler.com/news-insights/client-alerts/ip-hot-topic-the-doj-chimes-in-on-fair-use-and-ai/); [ChatGPT Is Eating the World, 2 Sep 2026](https://chatgptiseatingtheworld.com/2026/09/02/united-states-files-statement-of-interest-in-openai-lawsuits-ai-training-is-fair-use-dilution-is-deeply-flawed-theory-in-the-view-of-the-united-states/); [World Trademark Review](https://www.worldtrademarkreview.com/article/us-doj-intervenes-in-support-of-openai-in-ongoing-copyright-litigation); [ACEDS](https://aceds.org/joe-patrice-doj-tells-court-ai-training-is-fair-use-forgets-to-mention-its-negotiating-a-stake-in-openai/)

**US Copyright Office, Part 3 report "Generative AI Training"** (pre-publication, 9 May 2025)
- Training on large, diverse datasets is "often" transformative. Training a model to generate outputs substantially similar to the training works may not be.
- Fair use needs fact-specific, case-by-case analysis.
- Three kinds of market harm: lost sales, lost licensing, and dilution. The report says "[e]ven when the output is not substantially similar to a specific underlying work, stylistic imitation made possible by its use in training may impact the creator's market."
- It recommends letting voluntary licensing develop.
- Sources: [Sidley, 28 May 2025](https://datamatters.sidley.com/2025/05/28/generative-ai-meets-copyright-scrutiny-highlights-from-the-copyright-offices-part-iii-report/); [Authors Guild](https://authorsguild.org/news/us-copyright-office-ai-report-part-3-what-authors-should-know/)
- Register Shira Perlmutter was removed the day after the report issued. The Office indicated the final version would not differ in substance — [Authors Guild](https://authorsguild.org/news/us-copyright-office-ai-report-part-3-what-authors-should-know/)

**Other 2026 items**
- Thaler v. Perlmutter: certiorari denied 2 Mar 2026, leaving the human-authorship requirement in place — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
- Practitioner consensus in late Oct 2026: no single US decision makes all generative-AI training lawful or unlawful — [Ballard Spahr](https://www.ballardspahr.com/insights/alerts-and-articles/2026/10/third-circuit-addresses-fair-use-in-ai-training-but-leaves-generative-ai-questions-unresolved)

**Background doctrine relevant to personal use**
- Fair use weighs purpose (including commercial vs. non-profit), nature, amount and market effect — [17 U.S.C. §107](https://www.law.cornell.edu/uscode/text/17/107)
- Private, non-commercial home copying (time-shifting) was held fair use in *Sony v. Universal*, 464 U.S. 417 (1984) — [Justia](https://supreme.justia.com/cases/federal/us/464/417/)
- *Field v. Google* (D. Nev. 2006): a site owner who knew how to use robots.txt/no-archive and didn't was found to have granted an implied license for caching — [Wikipedia summary](https://en.wikipedia.org/wiki/Field_v._Google,_Inc.)

### Inferences
- **Training.** A LoRA or QLoRA fine-tune on one author's freely readable posts, for private use, falls on the favorable side of Bartz and Kadrey on factor 1: transformative and non-commercial. The difference is that it is built to imitate one author, not to learn language broadly. The Copyright Office's "stylistic imitation" passage and Chhabria's dilution dicta point at exactly that. For a private tool whose outputs are never published, factor 4 market harm is hard to show. That changes if outputs are distributed.
- **Storing the corpus.** Bartz turned on where the copies came from (pirated vs. purchased) and on keeping a general-purpose library. Saving freely served posts from the author's own site is lawful access, not piracy. A narrow, purpose-limited local copy is closer to the fair "purchased and scanned" branch than to the infringing "central library" branch. Keeping the corpus private, not sharing it, and deleting it when it is no longer needed all reduce the risk. Avoid paywalled posts obtained through a shared login, and avoid book PDFs from shadow libraries. Those map directly onto the infringing branch of Bartz.
- **Outputs.** Every authority above treats outputs that reproduce protected expression as a separate question. The Bartz release expressly excludes output claims, and DOJ urged courts to keep training and outputs apart. Verbatim or near-verbatim regurgitation from your model is the clearest exposure, especially if you publish it.
- **Pending.** The NYT/OpenAI MDL (S.D.N.Y.), Kadrey's remaining claims, any Supreme Court petition in Ross, and the Bartz settlement appeals are all live. A fair-use ruling in the MDL is the next likely big signal.

### Gaps
- I read no primary opinions in full. Exact quotations from Ross (3d Cir.) and Kadrey come via law-firm summaries.
- I found no authority on individual, non-commercial, single-author fine-tuning specifically.
- A search snippet reported a Ninth Circuit ruling in the GitHub Copilot case (16 Sept 2026) affirming dismissal of the DMCA claims. I could not tie it to a reliable source, so it is unverified.
- I did not determine whether ROSS will seek certiorari.

## 2. Style is not copyrightable; outputs that are substantially similar or memorized; right of publicity and passing off; what changes if you publish under your own name

### Takeaway
Copyright protects expression, not ideas or a "personal style". The Copyright Office declined in 2024 to recommend a federal style right, and pointed instead to passing-off, unfair-competition and right-of-publicity law. The live risks are threefold. Verbatim or near-verbatim passages are copying. Presenting output as the author's, or trading on their name, raises publicity and false-endorsement claims; the Grammarly "Expert Review" suit (S.D.N.Y., filed March 2026) is the current test case for text. And purely AI-generated text you publish under your own name may not be protectable.

### Cited Findings
- Copyright does not extend to any "idea, procedure, process, system, method of operation, concept, principle, or discovery" — [17 U.S.C. §102(b)](https://www.law.cornell.edu/uscode/text/17/102)
- Copyright Office Part 1 report on Digital Replicas (31 July 2024):
  - Case law treats "personal style" as akin to an unprotectable idea. The Office does not recommend style as protected subject matter.
  - It notes existing protection against unfair or deceptive copying of style under the Copyright Act, the Lanham Act (passing off, unfair competition) and state right-of-publicity law.
  - Sources: [Venable, 7 Aug 2024](https://www.venable.com/insights/publications/2024/08/overview-of-us-copyright-office-report); [A&O Shearman](https://www.aoshearman.com/en/insights/ao-shearman-on-tech/overview-of-the-us-copyright-offices-ai-digital-replicas); [Skadden](https://skadden.com/insights/publications/2024/08/copyright-office-advocates-for-federal-digital-replica-law)
- Lanham Act false-endorsement claims require showing consumer confusion — [Venable](https://www.venable.com/insights/publications/2024/08/overview-of-us-copyright-office-report)
- Copyright does not protect works written in an author's style or voice. Imitation can still infringe if it becomes "substantially similar" — [WFDD/NPR](https://www.wfdd.org/story/ai-contentious-among-authors-so-why-are-some-feeding-it-their-own-writing)
- The Copyright Office Part 3 report says models trained to produce substantially similar outputs may not be transformative — [Sidley](https://datamatters.sidley.com/2025/05/28/generative-ai-meets-copyright-scrutiny-highlights-from-the-copyright-offices-part-iii-report/)
- Grammarly "Expert Review":
  - The feature launched in Aug 2025 for paying users. It attributed edits to named real writers as "inspired by Julia Angwin" and similar.
  - Angwin filed a proposed class action on 11 Mar 2026 against Superhuman Platform Inc. (S.D.N.Y., 1:26-cv-02005), on behalf of a nationwide class and a New York subclass.
  - Grammarly disabled the feature and apologized.
  - Sources: [Nieman Lab, Mar 2026](https://www.niemanlab.org/2026/03/journalist-julia-angwin-files-class-action-lawsuit-over-grammarlys-ai-sloppelgangers/); [complaint on CourtListener](https://storage.courtlistener.com/recap/gov.uscourts.nysd.659486/gov.uscourts.nysd.659486.1.0.pdf); [eWeek](https://www.eweek.com/news/grammarly-expert-review-lawsuit/)
  - Authors Alliance argued that existing law, including publicity rights, is enough to address it — [Authors Alliance, 9 Apr 2026](https://www.authorsalliance.org/2026/04/09/will-the-grammarly-lawsuit-show-us-yet-another-area-where-existing-law-is-enough-we-think-so/)
- Fake AI-written books sold under real authors' names on Amazon have pushed authors to seek protection for their names — [Bloomberg Law](https://news.bloomberglaw.com/states-of-play/fake-books-on-amazon-drive-authors-to-shield-their-names-from-ai)
- GEMA v OpenAI (Munich, 11 Nov 2025) rejected GEMA's personality-rights claims based on misattributed, altered lyrics, while upholding the copyright claims — [Posteo](https://posteo.de/en/news/germany-gema-wins-court-case-against-openai)
- Publishing under your own name:
  - The human-authorship requirement stands after cert was denied in Thaler on 2 Mar 2026 — [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
  - The Authors Guild recommends disclosing AI use even when a model is tuned on your own work — [Authors Guild](https://authorsguild.org/resource/ai-best-practices-for-authors/)

### Inferences
- **Private use.** A private tool that writes in a famous author's style, kept on your machine, carries minimal publicity or passing-off risk. Those claims generally need commercial use or public presentation, plus confusion or appropriation of identity.
- **Publishing under your own name** raises four separate issues:
  - Memorized spans in published text are straightforward copying.
  - If readers can tell the piece imitates a specific living author, it invites the "dilution" framing, both reputational and legal.
  - Marketing it with the author's name ("in the voice of X", "X-GPT") is the Grammarly pattern.
  - Purely machine-generated passages may not be copyrightable by you. Heavy human revision helps on both the copyright and the ethics fronts.
- Never label output as the author's work, never put the author's name in product, model or file names you share, and run an overlap check (section 6) before anything leaves your machine.

### Gaps
- I found no US decision applying right of publicity to text style imitation, as opposed to names, voices or likenesses.
- The Grammarly case had no ruling as of my searches (latest coverage April 2026).
- I did not survey state statutes such as Tennessee's ELVIS Act or NY Civil Rights Law §§50–51 in detail.

## 3. EU (DSM Article 4 TDM exception with opt-out; AI Act GPAI obligations) and UK

### Takeaway
- **EU.** Article 4 of the DSM Directive permits reproductions of lawfully accessible works for text and data mining, unless the rightholder has reserved rights "in an appropriate manner, such as machine-readable means". Courts are working out what counts as a valid reservation (Kneschke v LAION) and whether a model that memorizes works falls outside the exception (GEMA v OpenAI).
- **AI Act.** GPAI obligations attach to providers who place models on the EU market. A purely personal model that is never distributed likely triggers none, but distributing weights could change that.
- **UK.** The UK has no commercial TDM exception. The government shelved its opt-out plan in March 2026. Getty v Stability held the model weights were not an "infringing copy", and that point is under appeal.

### Cited Findings
**DSM Directive 2019/790**
- Art. 3 covers TDM by research organisations and cultural-heritage institutions.
- Art. 4(1) is a general exception for reproductions and extractions of lawfully accessible works for TDM. Art. 4(2) lets copies be kept as long as necessary for TDM. Art. 4(3) applies only if use has not been "expressly reserved… in an appropriate manner, such as machine-readable means in the case of content made publicly available online".
- Source: [EUR-Lex, Directive (EU) 2019/790](https://eur-lex.europa.eu/eli/dir/2019/790/oj)

**Kneschke v LAION (Germany)**
- LG Hamburg, 27 Sept 2024 (310 O 227/23). It said in obiter that a natural-language opt-out in website terms could satisfy the "machine-readable" requirement — [Wolters Kluwer Copyright Blog](https://legalblogs.wolterskluwer.com/copyright-blog/kneschke-vs-laion-landmark-ruling-on-tdm-exceptions-for-ai-training-data-part-2/)
- OLG Hamburg, 10 Dec 2025 (5 U 104/24), appeal dismissed. Building the dataset was covered by the scientific-research TDM exception, which has no opt-out. A further appeal to the BGH is pending — [CMS case tracker](https://cms.law/en/rou/publication/artificial-intelligence-and-copyright-case-tracker/germany-robert-kneschke-v-laion-e.v)
- One summary says the OLG held a natural-language reservation was not effective at the relevant time. That is unconfirmed — [Blck Alpaca](https://blckalpaca.at/es/base-de-conocimiento/seo-geo/seo-tecnico/robotstxt-e-ia-marco-legal-de-la-ue-y-opt-out-de-tdm.md)

**GEMA v OpenAI (LG München I, 42 O 14139/24, 11 Nov 2025)**
- The court found that nine song lyrics memorized in the model and reproducible from simple prompts were reproductions. TDM covers training only where memorization does not occur.
- It granted injunction and damages, and rejected personality-rights claims. OpenAI is appealing.
- Sources: [Härting](https://haerting.de/en/insights/gema-wins-against-openai-strengthening-copyright-in-the-age-of-ai/); [Verfassungsblog, 19 Nov 2025](https://verfassungsblog.de/munich-regional-courts-ruling-in-gema-v-open-ai/); [MediaLaws](https://www.medialaws.eu/gema-v-openai-ai-memorisation-reconsidered/)

**Like Company v Google (CJEU C-250/25)**
- Advocate General Szpunar's opinion of 3 Nov 2026 proposed setting aside the training questions, because nothing in the file showed the articles were used to train Gemini. He found that real-time retrieval and reuse of press content by a chatbot may infringe press publishers' rights. The opinion is non-binding and there is no judgment yet.
- Sources: [Paperjam](https://en.paperjam.lu/article/gemini-may-infringe-the-rights-of-newspaper-publishers); [Courthouse News](https://courthousenews.com/eu-legal-adviser-finds-limited-uses-of-google-ai-could-run-afoul-of-publishers-rights/); [Wolters Kluwer Copyright Blog](https://legalblogs.wolterskluwer.com/copyright-blog/first-reflections-on-ag-szpunars-opinion-in-like-company/)

**EU AI Act**
- Art. 2(10): the Regulation "does not apply to obligations of deployers who are natural persons using AI systems in the course of a purely personal non-professional activity". This exempts deployers only, not providers — [AI Act Art. 2](https://artificialintelligenceact.eu/article/2/)
- Definitions in Art. 3 — [AI Act Art. 3](https://artificialintelligenceact.eu/article/3/):
  - A "provider" develops a system or model and places it on the market or puts it into service under its own name, paid or free.
  - "Placing on the market" is the first making available in the Union.
  - "Making available" is supply "in the course of a commercial activity".
  - A GPAI model excludes models used for research, development or prototyping before release.
- Commission GPAI guidelines (18 July 2025): a downstream modifier becomes a provider only if the modification uses more than one-third of the original model's training compute. If the original compute is unknown, the fallbacks are one-third of 10^25 FLOP (systemic-risk models) or 10^23 FLOP (others). This is an "indicative" presumption, and obligations are limited to the modification — [Bird & Bird](https://cm.twobirds.com/en/insights/2025/taking-the-eu-ai-act-to-practice-how-the-final-gpai-guidelines-shape-the-ai-regulatory-landscape); [WilmerHale, 24 Jul 2025](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20250724-european-commission-issues-guidelines-for-providers-of-general-purpose-ai-models)

**UK**
- Statutory report of 18 Mar 2026 under the Data (Use and Access) Act 2025: the government backed none of the options and shelved its preferred opt-out TDM exception. The s29A CDPA exception still covers non-commercial research only, so commercial TDM still needs a licence — [RPC](https://www.rpclegal.com/snapshots/technology-digital/summer-2026/uk-governments-report-on-copyright-and-ai/); [Osborne Clarke](https://www.osborneclarke.com/insights/opted-out-uk-government-moves-away-preferred-position-ai-and-copyright-following-report); [Simmons & Simmons](https://www.simmons-simmons.com/en/publications/cmn8tmopv0050ustoq2e6ndz2/a-masterclass-in-can-kicking-uk-government-views-on-ai-and-copyright)
- Getty Images v Stability AI, [2025] EWHC 2863 (Ch), 4 Nov 2025: the model weights were not an "infringing copy" because the trained model does not store the works. Getty won limited trademark points and got permission to appeal on 16 Dec 2025 — [AIPPI](https://www.aippi.org/news/getty-images-v-stability-ai-uk-high-court-finds-no-secondary-copyright-infringement-in-landmark-genai-ruling/); [Burges Salmon](https://www.burges-salmon.com/articles/102lydc/getty-images-v-stability-ai-getty-granted-permission-to-appeal)

### Inferences
- **EU-based builders.** Honour any machine-readable reservation. That means robots.txt AI-bot blocks, a `tdm-reservation` header or tdmrep.json, and probably clear natural-language "no AI training" notices given the split in the Hamburg rulings. Do this even for personal use. If no reservation exists, Art. 4 likely covers lawfully accessed public posts.
- **GEMA's logic** means a fine-tune that memorizes passages is riskier in Germany than in the UK under Getty. That is another reason to measure and suppress memorization.
- **AI Act.** A personal LoRA that is never distributed is not "placed on the market". Its compute is also orders of magnitude below one-third of the base model's. Posting the weights publicly (for example on Hugging Face) is where provider questions begin. Copyright exposure from distributing a model that may contain memorized text is a separate issue.
- **UK.** There is no private-copying or commercial TDM exception, so a UK resident relies on s29A only for genuinely non-commercial research. A personal writing tool is arguably not "research". This is the least permissive of the three regimes on paper.

### Gaps
- I did not read the GPAI Code of Practice copyright chapter of July 2025, including its robots.txt commitments, in this session.
- I did not examine whether member-state private-copying exceptions (InfoSoc Art. 5(2)(b), German §53 UrhG) cover a personal training corpus. I found no case on point.
- No Court of Appeal judgment in Getty has been found yet. The GEMA appeal status after Nov 2025 is unknown.

## 4. Website terms of service, robots.txt, ai.txt and TDM-reservation signals on popular writer platforms; is reading RSS and archives for personal use accepted?

### Takeaway
- **Substack's** terms (updated 6 Oct 2026) prohibit manual or automated crawling and scraping, and copying or storing "any significant portion" of its content. Its robots.txt does not block AI crawlers by default, but writers can switch on a "Block AI training" setting.
- **Medium** is the most restrictive. It has had a "default no" AI policy since Sept 2023, its robots.txt blocks major AI crawlers, and it publishes an RSL license file.
- **WordPress.com** terms have no explicit scraping or AI clause.
- **Ghost Foundation's** own terms bar crawlers on its services. Self-hosted Ghost sites set their own robots.txt.
- **RSS readers** are the accepted way to read posts. Logged-out access is weakly bound by browsewrap terms (Meta v. Bright Data). Bulk archive harvesting still breaches Substack's terms on their face.

### Cited Findings
**Substack**
- Terms of service, "Last Updated: October 6, 2026" — [Substack ToS](https://substack.com/tos):
  - They prohibit anyone who "Crawls," "scrapes," or "spiders" any page… (through use of manual or automated means).
  - They prohibit anyone who "Copies or stores any significant portion of the content on Substack".
  - Writers "own what you create". Users agree to use Substack "only… for your own personal or organizational use".
  - AI training is not expressly mentioned.
- Substack offers a publication-level AI-training block — [Substack support](https://support.substack.com/hc/en-us/articles/20382615953556)
- robots.txt, observed 2026-11-07 on substack.com, astralcodexten.com and experimental-history.com: `User-agent: *` disallows /action/, /subscribe, /embed, /p/*/comment/* and similar. BLEXBot is fully blocked. There are no GPTBot or ClaudeBot blocks on these publications — [substack.com/robots.txt](https://substack.com/robots.txt); [astralcodexten.com/robots.txt](https://www.astralcodexten.com/robots.txt)
- No `tdm-reservation` or `X-Robots-Tag` headers on the Substack homepages (observed).

**Medium**
- 2023 announcement "Default No to AI Training on Your Stories". The ToS was updated to bar scraping without consent, citing the hiQ v. LinkedIn precedent on enforceability — [Medium blog](https://blog.medium.com/default-no-to-ai-training-on-your-stories-abb5b4589c8); [The Register, 29 Sep 2023](https://www.theregister.com/2023/09/29/medium_ai_crawlers/)
- Help Center "third-party AI settings" include a "Minimize third-party training" option — [Medium Help](https://help.medium.com/hc/en-us/articles/39084471091991-Managing-Your-Third-Party-AI-Settings)
- robots.txt, observed 2026-11-07: Amazonbot, Applebot-Extended, Bytespider, ClaudeBot, FacebookBot, GoogleOther, GPTBot and meta-externalagent are disallowed from "/" except marketing pages. The file declares `License: https://medium.com/license.xml` (RSL syntax). Medium's ToS page and license.xml returned 403 or a Cloudflare challenge to automated fetch — [medium.com/robots.txt](https://medium.com/robots.txt)

**WordPress.com**
- ToS of 6 Oct 2026: no explicit scraping or AI-training clause. Users "will not overburden or interfere with our systems". Automattic may make public content available to "select third parties" to "analyze and/or distribute (but not publicly display)" it. The terms also govern visitors — [WordPress.com ToS](https://wordpress.com/tos/)
- robots.txt asks regular crawlers to use the WordPress firehose and has no AI-bot blocks at the root (observed) — [wordpress.com/robots.txt](https://wordpress.com/robots.txt)

**Ghost**
- Ghost Foundation terms prohibit downloading "data (including Content) from any Service" via "spiders, robots, crawlers, data mining tools or the like" other than generally available browsers (observed text) — [Ghost terms](https://ghost.org/terms/)
- Self-hosted Ghost sites set their own robots.txt. For example, 404 Media blocks GPTBot (observed) — [404media.co/robots.txt](https://www.404media.co/robots.txt)

**Personal sites**
- paulgraham.com has no AI-bot rules (observed) — [robots.txt](https://paulgraham.com/robots.txt)
- simonwillison.net explicitly allows ChatGPT-User (observed) — [robots.txt](https://simonwillison.net/robots.txt)

**Legal weight of terms**
- Meta v. Bright Data (N.D. Cal., 23 Jan 2024, Judge Chen): logged-out scraping of public data did not breach Meta's terms, because the scraper was a "visitor", not a "user". The ruling does not address logged-in or behind-login scraping — [Farella Braun + Martel](https://www.fbm.com/post/102kqw7/); [Quinn Emanuel](https://www.quinnemanuel.com/the-firm/news-events/client-alert-what-does-the-meta-v-bright-data-summary-judgment-ruling-mean-for-web-scraping/)

**Machine-readable signals (status Nov 2026)**
- Cloudflare Content Signals in robots.txt: `search`, `ai-input`, `ai-train`. The managed default is search=yes, ai-train=no, on more than 3.8M domains. Google has said crawlers ignore it — [Search Engine Land](https://searchengineland.com/cloudflare-content-signals-462538); [SEO Sherpa](https://seosherpa.com/google-says-cloudflares-content-signals-directive-is-ignored-by-crawlers-and-llms/)
- IETF AIPREF: the vocabulary is still an Internet-Draft (around -06/-07). A March 2026 note says it is reduced to "Search" and "Foundation Model Production" — [IETF Datatracker](https://datatracker.ietf.org/group/aipref/documents/); [W3C TDMRep list, Mar 2026](https://lists.w3.org/Archives/Public/public-tdmrep/2026Mar/0000.html)
- RSL 1.0 (Really Simple Licensing) became an official specification in Dec 2025 and supports attribution, pay-per-crawl and pay-per-inference terms — [Editor & Publisher](https://www.editorandpublisher.com/stories/rsl-ai-licensing-10-now-an-official-industry-standard,259144); [Creative Commons, 10 Dec 2025](https://creativecommons.org/2025/12/10/integrating-choices-in-open-standards/)
- W3C TDMRep is the source of the `tdm-reservation` header and `/.well-known/tdmrep.json`. Its list is now discussing aligning with the Cloudflare vocabulary — [W3C TDMRep list](https://lists.w3.org/Archives/Public/public-tdmrep/2026Mar/0000.html)

### Inferences
- **Reading via RSS** in a feed reader is plainly the intended use. Saving those posts locally for personal reading is commonplace and low-risk.
- **Substack.** Paging the whole back catalogue through `/api/v1/archive` or scripted page fetches is "scraping" under its terms, even if done slowly. That is contract risk, mostly theoretical for a logged-out individual after Bright Data. Lower-friction routes:
  - Accumulate the RSS feed over time.
  - Ask the author. Substack writers can export their own archive.
  - Fetch only what a browser would, politely and while logged out.
- **Medium.** The ToS and robots.txt prohibitions plus the RSL file are the strongest "no" signal of any platform here. Treat a Medium-only author as opted out unless they say otherwise.
- **Practical ethics rule.** Check the author's own domain robots.txt, headers and any "no AI" notice before collecting. If any reservation exists (an AI-bot block, `ai-train=no`, a tdm-reservation header, a platform AI-block toggle, or a written notice), treat it as a no, even though a personal crawler isn't GPTBot.

### Gaps
- I could not retrieve Medium's current ToS text (403), so its exact clause wording is unverified this session.
- I did not verify Substack's exact menu path or the robots.txt output of its "Block AI training" toggle on a site that has enabled it.
- I did not check Ghost(Pro)-hosted publications for platform-level AI-bot defaults.
- Reports of Automattic sharing data with AI firms in 2024 were not verified this session.

## 5. Ethics norms: writers' reactions to style-cloning; Authors Guild positions; best practice

### Takeaway
- Writers' objections centre on consent, control and power, not the technology itself.
- The Authors Guild's 2026 best practices tell members not to use AI to "copy or mimic the unique styles, voices, or other distinctive attributes" of other writers. The Guild is not opposed to authors tuning models on their own writing, but asks for disclosure.
- The most visible 2026 backlash (Grammarly's "Expert Review") came from attaching real writers' names to AI output.
- Mainstream assistants are pulling back: ChatGPT now declines named-author style requests.
- The responsible default is personal use only, no distribution of the corpus or weights, no use of the author's name on outputs, honouring opt-outs, and preferring to ask.

### Cited Findings
- Authors Guild "AI Best Practices for Authors" — [Authors Guild](https://authorsguild.org/resource/ai-best-practices-for-authors/); [Hypebeast, Jul 2026](https://hypebeast.com/2026/7/chatgpt-blocks-famous-author-styles-amid-copyright-push); [TNW, 28 Jul 2026](https://thenextweb.com/news/chatgpt-refuses-author-style-imitation-copyright):
  - First issued Feb 2024 and revised in 2026. One report dates the revision 11 May 2026.
  - Writers should not use AI to "copy or mimic the unique styles, voices, or other distinctive attributes" of others, warning of unfair-competition and infringement claims.
  - Disclosure is warranted even when you tune on your own writing.
  - The Guild calls them "guidelines, not rules".
- Authors Guild CEO Mary Rasenberger is not opposed to authors training models on their own writing. The Guild demands consent and payment from AI companies — [WFDD/NPR](https://www.wfdd.org/story/ai-contentious-among-authors-so-why-are-some-feeding-it-their-own-writing)
- Gero et al., CHI 2025 (arXiv:2409.14281): interviews with 33 creative writers. Principles were supporting the creative process, respecting writers, and the human element. Writers were "more concerned with power imbalances than the technology itself", and cited a lack of control and industry-scale impacts — [arXiv](https://arxiv.org/abs/2409.14281)
- Grammarly "Expert Review" backlash:
  - A PC Gamer editor found an AI version of his voice built from his published work without consent. Grammarly withdrew the feature, and Angwin sued in Mar 2026 — [Nieman Lab](https://www.niemanlab.org/2026/03/journalist-julia-angwin-files-class-action-lawsuit-over-grammarlys-ai-sloppelgangers/); [aiproductivity.ai](https://aiproductivity.ai/news/grammarly-ai-voice-clone-without-permission/)
  - The Superhuman CEO said the feature "missed the mark" — [eWeek](https://www.eweek.com/news/grammarly-expert-review-lawsuit/)
- Lab behaviour, per TNW summarizing the No Latency audit and Ars Technica, July 2026 — [TNW](https://thenextweb.com/news/chatgpt-refuses-author-style-imitation-copyright):
  - ChatGPT refused living-author style requests by 15 July 2026, and dead authors (Dickens, Hemingway, Christie) by about 27 July.
  - Claude complied with originality caveats. Gemini complied outright. Perplexity refused.
  - OpenAI made no statement, and its model spec has no written rule for text.
  - This was a small-sample audit.
- Creative Commons is building "signals" that let creators state AI-use preferences, integrated into RSL — [Creative Commons](https://creativecommons.org/2025/12/10/integrating-choices-in-open-standards/)
- Chakrabarty, Ginsburg & Dhillon argue that author-specific fine-tunes which emulate an author's works "should not be fair use", given measured substitution among readers — [arXiv:2510.13939v4](https://arxiv.org/html/2510.13939v4)

### Inferences
These are proposed best-practice norms synthesized from the sources above:
1. Prefer your own writing, or an author who has invited training (some bloggers explicitly allow AI bots), over an unwilling famous living author.
2. Ask first when the author is reachable. A short email costs little and resolves the ethics question.
3. Keep it personal: no distribution of the corpus, adapters or merged weights, and no hosted demo.
4. Never present outputs as the author's, and never use their name in published titles or marketing.
5. Disclose AI assistance in anything you publish.
6. Honour every opt-out signal from section 4.
7. Use the model to learn craft (sentence rhythm, structure, argument moves), not to produce publishable "new X essays". Publishable "new X essays" are the substitution and dilution scenario.
8. Delete the corpus if the author objects.

On the famous-vs-own trade-off, the Guild's line and the Grammarly backlash both target imitation of a specific other writer. Tuning on your own corpus avoids nearly all of these issues.

### Gaps
- I found no Authors Guild statement specifically addressing private, non-commercial fine-tuning on another author's work.
- I found no documented public reaction from a well-known essayist or blogger, such as Paul Graham, to a fine-tune of their own work.
- The PaulGPT write-up and Hugging Face datasets show such fine-tunes exist, but I found no author response.

## 6. Technical implications of targeting a famous author (fine-tune vs. prompting, memorization and regurgitation, topic leakage)

### Takeaway
- **Fine-tuning beats prompting decisively** for famous authors. In Chakrabarty et al., GPT-4o fine-tuned on each author's complete works was preferred by expert readers over MFA writers' imitations (odds ratio 8.16 for style). Detectors almost never flagged it, while in-context prompting was disfavoured by experts and almost always detected.
- **A famous target is already in the base model's pretraining data**, and fine-tuning can reactivate verbatim memorization. "Alignment Whack-a-Mole" (2026) found that summary-to-text fine-tuning on one author unlocked recall of 85–90% of held-out books.
- **Topic leakage is real.** Style and topic are entangled. The standard fix is a paraphrase-inversion setup (neutral rewrite to author's style) over diverse topics.

### Cited Findings
**Chakrabarty, Ginsburg & Dhillon, "Readers Prefer Outputs of AI Trained on Copyrighted Books over Expert Human Writers"** (arXiv:2510.13939, v4, 17 Mar 2026) — [arXiv HTML v4](https://arxiv.org/html/2510.13939v4); [abstract](https://arxiv.org/abs/2510.13939)
- **Setup.** 50 award-winning authors; 30 fine-tuned (e.g., Atwood, Murakami, Rushdie, Díaz).
  - In-context baselines: GPT-4o, Claude 3.5 Sonnet and Gemini 1.5 Pro, each given 20 sample excerpts, a style description and a content specification.
  - Only GPT-4o was fine-tuned, via the OpenAI API. Llama 3.1 was dropped for poor long-context instruction following.
- **Fine-tuning data.** ePubs were split into 250–650-word context-independent excerpts. GPT-4o wrote a content description for each, and training pairs used the prompt "Write a [n] word excerpt about the content below emulating the style and voice of [author]" (instruction back-translation).
  - 3 epochs for most authors, 1 epoch for Atwood, Ishiguro, Rushdie and Murakami. Batch size 1, LR multiplier 2, temperature 1.0.
  - Corpora ran from about 0.89M tokens (Tulathimutte) to 10.9M (Pamuk). No detectable relationship between corpus size and preference in that range.
- **Readers.** 28 MFA-trained readers and 516 college-educated general readers, in blind pairwise comparisons.
- **Results (odds ratios, above 1 favours AI)**:

| Condition | Reader group | Style fidelity | Writing quality |
|---|---|---|---|
| In-context | MFA-trained | 0.16 | 0.13 |
| In-context | General | 1.06 (n.s.) | 1.82 |
| Fine-tuned | MFA-trained | 8.16 | 1.87 |
| Fine-tuned | General | 16.65 | 5.42 |

  - 29 of 30 fine-tuned author models beat parity on fidelity (median win rate 0.83). Per-author style win rates ranged from 18% (Tulathimutte) to 98% (Roxane Gay).
- **Detection.** Pangram flagged 97% of in-context outputs but only 3% of fine-tuned outputs. GPTZero missed 100% of fine-tuned outputs. Cliché density mediated 16.4% of the detection effect on expert preference for in-context outputs, and 1.3% for fine-tuned outputs.
- **Memorization.** ROUGE-L between outputs and the original excerpts was 0.16–0.23. Outputs that regurgitated verbatim snippets were resampled and checked by hand. The prompt excerpts were held out of training.
- **Cost.** $25–$276 per author for fine-tuning and generation (median $81), excluding human editing.
- **Legal framing.** The authors argue author-specific fine-tunes should not be fair use. They propose output guardrails and AI-origin disclosure, and admit both are imperfect.

**Liu, Mireshghallah, Ginsburg & Chakrabarty, "Alignment Whack-a-Mole: Finetuning Activates Verbatim Recall of Copyrighted Books in LLMs"** (arXiv:2603.20957, Mar 2026; ICML 2026) — [arXiv PDF](https://arxiv.org/pdf/2603.20957v2); [ICML listing](https://icml.cc/virtual/2026/78905)
- GPT-4o, Gemini-2.5-Pro and DeepSeek-V3.1 were fine-tuned to expand plot summaries into full text. They then reproduced up to 85–90% of held-out copyrighted books, with single verbatim spans over 460 words, from semantic prompts alone.
- Fine-tuning only on Murakami unlocked recall for more than 30 unrelated authors. Random-author and public-domain fine-tuning data gave similar extraction, while synthetic text gave near-zero extraction.
- The memorized regions correlated across providers (r ≥ 0.90).
- Secondary summaries cite longer spans; the abstract's figure of 460+ words is the one to use.

**Cooper, Lemley et al., "Extracting memorized pieces of (copyrighted) books from open-weight language models"** (arXiv:2505.12546; ICML 2025) — [arXiv v4](https://arxiv.org/html/2505.12546v4)
- Llama 3.1 70B memorized the first Harry Potter book so thoroughly it could be generated near-verbatim from a few opening tokens. It also memorized *1984* almost entirely.
- Most books were not substantially memorized, and memorization varies by model and by book.

**StyleTunedLM** (arXiv:2409.04574, 2024) — [arXiv](https://arxiv.org/html/2409.04574v1)
- LoRA on Llama-2-7b with next-token prediction on raw text from 10 Project Gutenberg authors (e.g., Austen, Woolf, Richardson).
- A LIMA-trained instruction LoRA was merged back in to keep instruction following.
- A BERT authorship classifier was used for evaluation.
- It captured style better than prompt engineering or few-shot baselines.

**Paul Graham fine-tunes in the wild**
- Hugging Face hosts PG essay datasets: `sgoel9/paul_graham_essays` (~215 rows, labelled MIT, though that licence label does not reflect PG's copyright) and `emozilla/PaulGrahamEssays` — [HF sgoel9](https://huggingface.co/datasets/sgoel9/paul_graham_essays/tree/main); [HF emozilla](https://huggingface.co/datasets/emozilla/PaulGrahamEssays/tree/d2e716bfe68e882e23fd25804509e8c35ca6b32e/default)
- The "PaulGPT" write-up used about 5,000 Q&A pairs scraped with BeautifulSoup and a LoRA on a Llama-7B-class model, trained in about 15 minutes on one H100. The result was "more characterful" but produced nonsense more often — [Making PaulGPT](https://2025-personal-site.pages.dev/paulgpt.html)

**Topic leakage and style–content disentanglement**
- STRAP (Krishna et al., EMNLP 2020): a diverse paraphraser strips style, then a per-style inverse paraphraser is trained on pseudo-parallel data (paraphrase of author text mapped back to the original) — [review](https://liner.com/ko/review/reformulating-unsupervised-style-transfer-as-paraphrase-generation)
- ASTRAPOP (Liu, Agarwal & May, 2024): builds a neutral-paraphrase dataset, then trains neutral-to-target with SFT plus policy optimization for low-resource authorship style transfer — [arXiv:2403.08043](https://arxiv.org/pdf/2403.08043)
- "A well-documented problem… is the entanglement of style with semantic content, where the topic itself predicts authorship" — [arXiv:2606.10099](https://arxiv.org/pdf/2606.10099)

**Lab refusals**
- ChatGPT's July 2026 refusals of named-author style requests mean prompting-only baselines for famous authors are now provider-dependent — [TNW](https://thenextweb.com/news/chatgpt-refuses-author-style-imitation-copyright)

### Inferences
- **Famous author vs. your own.**
  - With a famous author, you get a strong prior: base models already "know" PG, Didion or Orwell. Prompting gives a recognizable caricature, and a small LoRA sharpens it quickly.
  - The cost is the highest memorization risk. Their essays are heavily duplicated across the web and in pretraining data, and Whack-a-Mole shows fine-tuning can surface that latent memorization.
  - The outputs are also the most legally and ethically fraught to publish.
  - Your own corpus has no regurgitation concern beyond self-plagiarism, and no consent issue. Fidelity has to come entirely from your own data volume.
- **Avoid the summary-to-full-text format on a famous author.** The "content description → exact original excerpt" pairing that Chakrabarty used is the same shape Whack-a-Mole showed reactivates verbatim recall. Safer recipes:
  - (a) Neutral-paraphrase → original (STRAP-style). The input is a meaning-preserving neutral rewrite, so the model learns transformation rather than recall.
  - (b) Plain continued pre-training on the text with dropout, few epochs (1–2) and a low LoRA rank.
  - (c) Synthetic multi-topic briefs. Whack-a-Mole found synthetic text yields near-zero extraction.
  - These are extrapolations, not tested claims.
- **Mitigations to implement:**
  - Deduplicate the corpus, including reposts, newsletter and blog duplicates, and quoted excerpts.
  - Hold out 5–10% of posts and measure verbatim recall by prompting with their summaries.
  - At inference, run an n-gram or longest-common-substring check against the corpus. Flag spans of 8–10 or more words and resample, as Chakrabarty did.
  - Avoid temperature 0 decoding.
  - Never prompt with exact opening lines of the author's essays. Cooper et al. show seed prompts trigger recall.
- **Topic leakage (e.g., a startup-essayist model pulling everything toward startups):**
  1. Label each post's topic and balance or cap topic share.
  2. Train on (topic-specific brief → text) pairs so content is supplied by the prompt, not baked into the weights.
  3. Add style-inversion pairs: neutral paraphrases of the author's own text, plus off-topic neutral drafts written by another model, mapped to author-style rewrites.
  4. Evaluate on briefs from domains the author never wrote about (cooking, sports), measuring topic drift with an embedding classifier alongside a style classifier, as StyleTunedLM used BERT.
- **Instruction following.** StyleTunedLM's merge of an instruction LoRA suggests you need either an instruct base model or a mixed-in instruction set, or the style tune erodes helpfulness. PaulGPT's "more nonsense" fits this.

### Gaps
- I could not retrieve Chakrabarty et al.'s Figure 19 overlap percentages or the exact verbatim-span thresholds.
- I found no paper measuring topic leakage specifically for blogger or essayist fine-tunes, and no study of Paul Graham-style models' memorization rates.
- I did not verify Whack-a-Mole's per-model extraction rates beyond the abstract.

## 7. Practical acquisition tooling and cleaning (trafilatura, newspaper4k, readability-lxml, feeds, sitemaps, polite crawling, Substack, footnotes, code, quotes, comments)

### Takeaway
Use feeds, sitemaps and platform APIs to enumerate posts. Use trafilatura with comments off, outputting XML or Markdown, for extraction. Then strip non-author text: block quotes, code, comments, embedded tweets and captions. Substack RSS gives the full text of only the 20 most recent posts. WordPress sites usually expose a public REST API. Many personal sites have a sitemap.

### Cited Findings
- trafilatura Python options — [trafilatura docs](https://trafilatura.readthedocs.io/en/latest/usage-python.html):
  - `include_comments` is on by default and must be set to False to exclude reader comments.
  - Also `include_tables` (default on), `include_formatting`, `include_links`, `include_images`.
  - `favor_precision=True` strips more boilerplate. `prune_xpath` removes specific elements first.
  - `output_format` accepts csv, json, html, markdown, txt, xml or xmltei.
  - `with_metadata=True` and `only_with_metadata=True` (date, title, URL). `record_id` for corpus tracking.
  - Discovery helpers: `feeds.find_feed_urls()`, `sitemaps.sitemap_search()` and `parse_sitemap()`.
- Substack RSS (`/feed`), observed on experimental-history.com on 2026-11-07: 20 `<item>`s, each with full `<content:encoded>` HTML (about 1.1 MB). `<copyright>` is set to the author's name (ACX feed) — [example feed](https://www.experimental-history.com/feed)
- Substack has an undocumented JSON archive endpoint, `/api/v1/archive?sort=new&limit=…` (observed; it rejected `offset=0`). Its use falls under the ToS scraping prohibition (section 4) — [Substack ToS](https://substack.com/tos)
- Substack robots.txt disallows `/p/*/comment/*` (observed). Comment pages are off-limits to crawlers and contain no author text anyway — [robots.txt](https://www.astralcodexten.com/robots.txt)
- The WordPress REST API `/wp-json/wp/v2/posts` returned HTTP 200 on a WordPress site (ma.tt, observed). It is a structured way to page through posts with full HTML.
- Paul Graham's essays have only a third-party "scraped feed provided by aaronsw.com". paulgraham.com's robots.txt lists a sitemap (observed) — [pgessays.rss](http://www.aaronsw.com/2002/feeds/pgessays.rss); [robots.txt](https://paulgraham.com/robots.txt)
- WordPress.com asks regular crawlers to use its firehose rather than crawl — [wordpress.com/robots.txt](https://wordpress.com/robots.txt)
- Chakrabarty et al.'s cleaning recipe: plain-text conversion, 250–650-word context-independent excerpts, and held-out evaluation excerpts — [arXiv:2510.13939v4](https://arxiv.org/html/2510.13939v4)

### Inferences
**Pipeline**
1. Enumerate posts from the sitemap, RSS/Atom, the WordPress REST API or the author's archive page.
2. Fetch politely: one request every 2–5 s, a descriptive User-Agent with contact email, robots.txt checked, and raw HTML cached so you never re-fetch. An equivalent wget is `wget --wait=3 --random-wait --limit-rate=200k -e robots=on --user-agent="..."`.
3. Extract with `trafilatura.extract(html, output_format="xml", include_comments=False, include_tables=False, include_images=False, include_links=False, favor_precision=True, with_metadata=True)`.

**Non-author text to remove**
- Drop or mask `<quote>`/`<blockquote>` elements. Quoted text is not the author's voice and is the most likely copyrighted third-party text.
- Drop code blocks, or replace them with a `[code]` placeholder.
- Drop image captions and embedded tweets or posts.
- Drop newsletter chrome: "Subscribe", "Thanks for reading", sponsor reads and paywall teasers.
- Drop comment threads.

**Footnotes and sidenotes**
- Common forms are Substack `footnote-anchor` links, Gwern-style sidenotes and WordPress footnote plugins.
- Either remove them, or keep them as endnotes, because footnote voice is often authorial.
- Remove the inline numerals so the model doesn't learn stray digits.

**Quality control**
- Spot-check about 20 posts by hand.
- Compare word counts against the visible page.
- Dedupe near-duplicates (MinHash or exact paragraph hashes), since cross-posted Medium and Substack copies are common.

**Alternatives**
- newspaper4k ([GitHub](https://github.com/AndyTheFactory/newspaper4k)) and readability-lxml ([GitHub](https://github.com/buriy/python-readability)) are fallbacks for odd templates. trafilatura already uses readability and jusText fallbacks unless `fast=True`, per its docs.

**Lowest-risk route for Substack**
- Subscribe and accumulate the feed over time.
- Or ask the author for their export.

### Gaps
- I did not verify how trafilatura's XML output tags block quotes and code (`<quote>`, `<code>`) against current docs. Test on a sample.
- I did not re-verify newspaper4k or readability-lxml documentation this session.
- I did not test Ghost Content API or RSS full-text defaults; the ghost.org blog feed returned no items to my fetch.
- I did not confirm a reader-side Substack archive export. As far as I found, export is a writer-side feature.
