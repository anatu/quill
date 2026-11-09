# Practitioner Examples: Individuals Fine-Tuning / Adapting LLMs on Their Own Writing

Scope: projects where people trained or adapted a model on their own writing (texts, chats, Slack, tweets, blogs, newsletters, notes, email), plus commercial "write in my voice" products and practitioner/research comparisons of fine-tuning vs. prompting. Research date: 2026-11-07. Every item below was fetched or seen in search results. Items I could only see through a search snippet or mirror are marked that way.

---

## Q1. Catalog: what concrete practitioner projects exist, and what did each one do?

### Takeaway
I found about 30 verifiable projects from 2023 to 2026. Almost all are hobbyist write-ups that use LoRA/QLoRA on a 3B–13B open model (a few use 65–70B), plus a handful that used OpenAI's fine-tuning API. They nearly all report that the model gets the surface voice right (length, casing, slang, structure). They also nearly all report failures on facts, coherence, context, and long-form work. Evaluation is usually informal. Only a few used blind human tests or simple metrics.

### Cited Findings

#### A. Personal messages and group chats (iMessage / SMS / WhatsApp / Telegram / Discord)

- **Izzy Miller, "Replacing my best friends with an LLM trained on 500,000 group chat messages" (Apr 10, 2023).**
  - Data: a college-friends iMessage group chat (6 people, about 7 years). About 488k messages remained after filtering, pulled from the Mac `chat.db`.
  - Model and training: LLaMA 7B, trained with the Stanford Alpaca code. The FSDP `full_shard` setting means this was a full fine-tune, not LoRA. Ran on 4×A100 rented on vast.ai: 3 epochs, LR 2e-5, "a few hours." Paid for with about $100 of leftover credits.
  - Data format: Alpaca-style instruction/input/output records. The instruction was a persona prompt naming the six members. Messages were grouped into sessions using a 4-hour inactivity gap.
  - Deployment: Modal (A10G), behind an iMessage-style PWA.
  - Evaluation: qualitative, through heavy use with the friends. Result: "It really, really nailed the voice and perspectives of my friends."
  - Pitfalls: the bots over-used tapback reactions, and "Something about the training process optimized for outrageous behavior." Lesson: "I'd remove 'tapback' reactions as well as images, and possibly links." — [izzy.co](https://www.izzy.co/blogs/robo-boys.html)
  - The HN thread drew 751 points and 355 comments — [HN](https://hn.algolia.com/api/v1/items/35540154)
- **Edward Donner, "A simulation of me: fine-tuning an LLM on 240k text messages" (Jan 2, 2024), plus a 4-part step-by-step series.**
  - Data: 240,805 SMS/iMessage/WhatsApp messages with 288 people, exported with iMazing. Group chats and rarely-messaged contacts were excluded. These became 25,087 chunks of about 7–10 messages each, capped at 200 tokens.
  - Model and training: Llama 2 7B, then 13B ("a marked improvement in results"). QLoRA on Google Cloud V100 VMs, with "a $100 Xmas gift." He did an extensive hyperparameter search and notes "conflicting advice all over the internets."
  - Data format: a system instruction ("Write a realistic text message chat. Avoid repetition."), a user turn naming the two participants, and then `### Name: message` lines.
  - Evaluation: subjective. He estimates "more than half of the conversations would pass a Turing Test." He searched his history for regurgitated conversations and found none.
  - Pitfalls: early outputs were surreal and repetitive (endless rescheduling and lunch debates). Fixes came from changes to the prompt, input format, and decoding, not just from training. He notes quality kept improving while loss rose. Fictional personas were worse, because without backstory the model fell back on logistics. — [edwarddonner.com](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/); series snapshots: [part 1](https://web-clips.pages.dev/snapshots/Step%20by%20step%20guide_%20fine-tune%20an%20LLM%20on%20your%20texts%20(part%201)%20-%20Edward%20Donner%20-%20edwarddonner.com%20(2024-04-23T01_05_33.305Z).html)
- **"muttled", Show HN: "I trained a 65B LLM on my texts to talk to myself" (Jul 21, 2023).**
  - Data and training: about 30k of his own texts over 2 years. LLaMA-1 65B, LoRA rank 128, 5 epochs, batch 1, 256-token cutoff. Used the Oobabooga trainer with bitsandbytes 4-bit, on 2×RTX 3090 for about 16 hours. A loss of about 1.5 gave the most coherent output.
  - PII handling: he scripted swaps of real names and addresses for fake ones. Side effect: the model hallucinates fake personal details (a silly address, a mother who was an astronaut).
  - Behavior: it "tends to talk as if it's already friends with the user." — [HN](https://hn.algolia.com/api/v1/items/36815443)
- **Alex (@furiousteabag), "I fine-tuned an LLM with my Telegram chat history" (Jun 13, 2024).**
  - Data: 5 years of Telegram, 15,789 sessions from 466 chats, mostly in Russian.
  - Training: LoRA on Dolphin-2.2.1-Mistral-7B (1×RTX 3090, 5.5 h, about $2), and a full fine-tune of Mistral 7B (8×A100, about 20 min, about $3).
  - Data format: ChatML sessions, with loss computed on all participants' turns.
  - Results: LoRA "definitely captures the style," and full FT was "not significantly better."
  - Failures: weak context ("significantly lacks context in conversations"), Russian grammar errors, and many generic short replies like "ok" or "busy" that dominated the data. The samples shown were cherry-picked. Code: furiousteabag/doppelganger. — [HackerNoon](https://hackernoon.com/i-fine-tuned-an-llm-with-my-telegram-chat-history-heres-what-i-learned)
- **Aditya Rathod, "Training a bot on my own messages for fun and chaos" (Aug 18, 2024). This one used MLX.**
  - Data: more than 291k of his own Discord messages over about 4 years.
  - Model and training: Mistral 7B v0.3. QLoRA via MLX on an M1 Pro MacBook with 16 GB. The final run was 5,000 iterations (about 5 h), with about 7.2 GB peak memory.
  - Data format: `{"text": ...}` JSONL. Messages less than 15 minutes apart in the same channel were merged into one document.
  - Failures: the instruct model gave one- or two-word replies, so he switched to the base model. Short data still produced short answers ("I was literally conditioning it to give really short responses"). He also saw repetition loops like "i love rust."
  - Result: "It copied my all-lowercase typing style and brevity," and it was deployed as a Discord bot for friends. — [adibytes.dev](https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself)
- **Timo Stroet, "Training an LLM on 150K Discord messages" (Jan 2, 2024).**
  - Setup: facebook/opt-125m with TRL SFTTrainer. Alpaca-format examples (prior context → reply), with sessions split on 4-hour gaps. Trained on a GTX 1660 Super for about 2 weeks.
  - Results were mostly nonsense or echoes. A counting channel leaked numbers into outputs.
  - Lesson: "taking two weeks to fine-tune a model that was already a bit too small" was a waste of time. — [gotimo2.github.io](https://gotimo2.github.io/posts/training-an-llm-on-150k-discord-messages)
- **Duarte O. Carmo, "Fine-tuning FLAN-T5 on my Telegram group chat" (May 24, 2023).** flan-t5-small on 20k messages, using up to 10 prior messages as context and 120-minute session gaps. Trained on an A100 for about 20 minutes. The output was short Portuguese replies, and the stated goal was learning. — [duarteocarmo.com](https://duarteocarmo.com/blog/fine-tune-flan-t5-telegram)
- **iClone (GitHub ishan0102). Uses MLX.** "Clone your friends by finetuning Mistral-7B on your iMessage chat history," built for Apple Silicon. The multi-turn formatting (system prompt + ~5 messages → next message) is still listed as a TODO, and no results are reported. Date not shown. — [GitHub](https://github.com/ishan0102/iClone)
- **mlx-whatsapp (GitHub gavi). Uses MLX.** Trains a Mistral-7B-v0.1 base on a WhatsApp "Export Chat → Without Media" file, using `lora.py --iters 600 --batch-size 2`. It warns: "Dont upload your fused models to public sites such a huggingface." No results; date not shown. — [GitHub](https://github.com/gavi/mlx-whatsapp)
- **codebyandy/finetune-me (GitHub). Uses MLX.**
  - Data and model: iMessage (`chat.db`) plus Slack, trained on mlx-community/Qwen3-4B-8bit with mlx-lm LoRA: rank 16, LR 1e-4, 1000 iters ("~1–2h on M1 for 4B"), batch 4 ("safe for 16 GB").
  - Data format: the last 6 turns of context, then his reply as the target. The system prompt reads "You are Andy. You are messaging {contact} in {channel}," so the model can learn different registers per person and channel.
  - Planned evaluation: a blind quiz, perplexity, and a comparison against a frontier model given 20 of his examples. No results yet. Its stated caveat: "The model will sound like you while saying plausible nonsense." — [GitHub](https://github.com/codebyandy/finetune-me)
- **WeClone (GitHub xming521, 18.4k stars).** An open-source "digital twin from chat history" toolkit. Defaults to Qwen2.5-7B-Instruct with LoRA, needs about 16 GB of VRAM on an NVIDIA GPU, and filters PII with Microsoft Presidio ("100% detection is not guaranteed"). Telegram is the only fully supported source; WhatsApp, Discord, and Slack are under construction. No MLX support. — [GitHub](https://github.com/xming521/WeClone)
- **Heralax_Tekran, r/LocalLLaMA, "Trained an LLM on my own writings. Somewhat funny results" (Apr 8, 2024).** Seen via a search snippet and Reddit mirror; I couldn't fetch the full page.
  - Data: annotated personal notes, a book he wrote, and a ChatGPT export with the roles swapped, so the model learned from his own messages.
  - Training: a full fine-tune with GaLore on a rented H100 for about 2 hours.
  - He suspected the role-swapped ChatGPT data is "why it's slightly stilted." The model recalled training content it wasn't explicitly given as examples. — [Reddit mirror](https://lr.us.psf.lt/r/LocalLLaMA/comments/1bzczyc/trained_an_llm_on_my_own_writings_somewhat_funny/kyp20tu/?context=3)
  - Heralax is also the author of Augmentoolkit, a tool that turns plaintext into instruct-tuning data. I couldn't confirm it was used here. — [GitHub](https://github.com/e-p-armstrong/augmentoolkit/)

#### B. Work chat (Slack / email)

- **Ross Lazerowitz, "Fine-tuning GPT3.5-turbo based on 140k slack messages" (Sep 4, 2023).**
  - Data and cost: four years of Slack at Observe Inc. Used the OpenAI fine-tuning API: 10.4M tokens, about 3 hours, $83.20.
  - Data format: a system prompt (PM persona), preceding messages as the user turn, and his replies as the assistant turn. Slack's one-message-per-Enter habit made turn boundaries messy.
  - Results: it captured his Slack structure (short lines sent in sequence). His conclusion was that his Slack style is "type first and think later."
  - Problems: erratic output at temperature 1.0, which he fixed by lowering temperature and raising the frequency penalty. Some replies had a brusque tone. The model was worse at other tasks.
  - Lesson: work chat may not represent your general style. — [rosslazer.com](https://rosslazer.com/posts/fine-tuning); Simon Willison linked it on Nov 8, 2023 — [simonwillison.net](https://simonwillison.net/tags/fine-tuning/)
- **Modal DoppelBot (open source, modal-labs/doppel-bot, 270 stars).** A Slack app that "scrapes a target user's messages in Slack" and fine-tunes Llama 3.1. Training takes "few minutes to an hour, depending on how prolific your user is on Slack." It is limited to one target user per workspace. — [GitHub](https://github.com/modal-labs/doppel-bot)
  - A third-party writeup says earlier versions used OpenLLaMA, and a search summary says Modal's blog built "@erik-bot" from the CEO's Slack. Neither was fetched from a primary page. — [starlog](https://starlog.pages.dev/articles/llm-engineering/jerryjliu-doppel-bot)
- **Nic Lydon, "I trained an LLM on 75K of my own messages so it would stop writing like a chatbot" (dev.to, posted May 9; year not shown, but it references Qwen 3.5, so likely 2026).**
  - Data: 75,329 samples (about 3.1M tokens) from 12 platforms over about 23 years. The largest sources were iMessage (34,987), Google Chat, and Plaud recordings. Tapbacks, URL- and emoji-only messages, quoted replies, and PII were stripped.
  - Model and training: Qwen 2.5 3B Instruct (4-bit, Unsloth), QLoRA r16/α32 on all 7 projection modules. ShareGPT two-turn format, 3 epochs (14,127 steps, about 17 h) on an AMD Radeon 8060S (96 GB unified memory, ROCm).
  - Evaluation: a blind A/B on 12 prompts against the base model.
  - Findings: strongest on casual chat, work chat, and short email; weaker on long-form. Rank 8 underfit. Targeting only q/k/v gave "right structure but the wrong vocabulary."
  - Architecture: a frontier model drafts the content, and the 3B voice model rewrites it. His framing: "Frontier LLMs are good at figuring out *what* to say. They're bad at saying it the way you would." — [dev.to](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)
- **Nicolas Deville, "NicAI" voice-model plan (Sep 20, 2026; written by his AI assistant). Planned on MLX.**
  - Plan: a Qwen2.5-1.5B-Instruct "voice model" to rewrite frontier drafts, using `mlx_lm.lora` on a Mac Studio M1 Ultra (128 GB).
  - Data: 1,185 notes (about 677k words) plus 169 draft-and-sent email pairs, which he calls "the strongest supervision." A 490-line SOUL.md of voice rules is used for labels and checks, not training.
  - It warns that 99 notes are AI-written: "Train on those and the voice model learns to imitate an imitation."
  - Evaluation plan: split by entity, not row, and a frozen 30-pair blind test against "Claude with SOUL.md" as the real baseline.
  - No results yet. Quote: "The data work is the project, and the training is an afternoon at the end of it." — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)

#### C. Tweets / social posts

- **Gabor Cselle, `write-my-posts` (livestreamed build, Nov 29, 2023).**
  - Data: an X/Twitter archive of about 10.9k tweets.
  - Training: GPT-3.5-turbo via the OpenAI fine-tuning API, first on 200 train / 40 val tweets, then about 4,000 / 500 non-reply tweets. Planned prompt synthesis: run tweetnlp NER and use the entity tags as the prompt.
  - Results: the small run matched his tone "reasonably well" but the content was often incoherent. The 4k run was "a little bit better but not phenomenally so."
  - Motivation: his earlier few-shot approach at Pebble had failed to match users' voices. — [GitHub](https://github.com/gaborcselle/write-my-posts)
- **OpenAI community thread, "Fine tuning on someone's tweets to match their tone and writing style" (Jan 2023).** It shows the core formatting problem: standalone tweets have no prompts. Suggestions were a fixed prompt ("this is a tweet in the style of [user]:"), topic-summary prompts, or thread replies. No successful fine-tune was reported, and the original poster fell back to about 10 few-shot examples. — [OpenAI forum](https://community.openai.com/t/fine-tuning-on-someones-tweets-to-match-their-tone-and-writing-style/40213)
- **Shrestha Pandey, "I fine-tuned Llama 3.2 on my own writing style using LoRA, Unsloth and a free Colab GPU" (dev.to, Jun 7; year not displayed).** About 20 LinkedIn, Instagram, and technical posts as instruction/response pairs. Llama 3.2 3B Instruct with Unsloth LoRA on a Colab T4, exported to GGUF for Ollama. Is it ready for real content creation? "Probably not." — [dev.to](https://dev.to/shresthapandey/i-fine-tuned-llama-32-on-my-own-writing-style-using-lora-unsloth-and-a-free-colab-gpu-13l5)

#### D. Blogs / newsletters / essays

- **Lydia Nottingham, "I fine-tuned Llama-3.1-70B on my blog" (Nov 20, 2025), repo LydNot/clone.**
  - Data: 114 examples (about 91k tokens) from her Substack RSS, made up of 20 full-post completion examples, 33 instruction examples, and 61 Q&A examples, in prompt/completion format.
  - Training: Llama 3.1 70B via Thinking Machines' Tinker. 3 epochs, LR 5e-5, about 10 minutes, $0.13. Loss went from about 2.65 to 0.23.
  - Results: it "captures my actual views + lydia-coded stylistic elements," and she found metacognition posts key. Evaluation was informal. — [Substack](https://lydianottingham.substack.com/p/i-fine-tuned-llama-31-70b-on-my-blog); [GitHub](https://github.com/LydNot/clone)
- **Didier Lopes, "Fine-tuning an LLM on my blog posts" (Sep 2, 2025). Uses MLX.**
  - Data: 91 posts converted to about 2,100 Q&A exchanges.
  - Training: Phi-3-mini-4k-instruct with MLX LoRA on an M3 Max (48 GB). Rank 16 (8 was worse), 2,000 iterations with early stopping around iteration 1,500.
  - Evaluation: Jaccard word overlap rose from 0.157 to 0.201 (+27.6% relative). Response length fell from 865 to 382 characters, against 406 for the references.
  - Lessons: match the chat template exactly and keep the system prompt. Knowledge transfer was weaker than hoped. — [beehiiv](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts)
- **Kevin Leary, "Creating Custom AI Models on a MacBook Pro" (Sep 18, 2025). Uses MLX.**
  - Data: WordPress posts going back to 2009. Training on mlx-community/Meta-Llama-3.1-8B-Instruct-4bit with `mlx_lm.lora` (batch 1, 16 layers, 600 iters, LR 1e-5).
  - Data format: chat JSONL with a templated prompt per post: `write a blog post in markdown for kevinleary.net entitled "{title} - {lead-in}" as if it were originally published on {date}`.
  - No evaluation or sample outputs are shown. — [kevinleary.net](https://www.kevinleary.net/blog/custom-ai-models-macbook-pro/)
- **Andrea Griffiths (GitHub Sr. PM), "An Experiment in Voice: What Happens When AI Learns to Write Like You" (dev.to crosspost dated Mar 24, with a Mar 17, 2026 update).**
  - Data: 81 examples from three years of newsletters, talks, and developer conversations, in ChatML.
  - Model and training: Qwen3 8B, after switching from Llama 3.1 8B: "That switch alone improved the output more than any hyperparameter tweak I tried." Unsloth LoRA r16/α32, 60 steps, LR 1e-4, on a free Colab T4. Runs locally as a q4_k_m quant on a 16 GB MacBook Pro.
  - Result: "The model learned how I write. Not how I think." — [dev.to](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na)
- **Shane Larson (Grizzly Peak Software), "I Fine-Tuned a 7B Model on My Own Writing in One Evening" (Mar 13, 2026).**
  - Data: only 6 of his own articles (bot protection blocked his scraper) plus 161 OpenHermes examples, for 224 total.
  - Training: Mistral-7B-Instruct-v0.3 with LoRA r32, 5 epochs, on a DGX Spark. Loss fell from 1.05 to 0.09, with 97% token accuracy.
  - Failure: it "convincingly adopted the writing voice" but "hallucinated code. Confidently." — [grizzlypeaksoftware.com](https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E)
- **Michael Daigler, "Making AI Write Like You" (May 4, 2024).** Llama 3 via an Unsloth Colab notebook, in two stages: Alpaca-cleaned first, then his newsletters as instruction/output pairs with a blank input. The draft "showcased a writing style similar to my own." No metrics. — [beehiiv](https://michaeldaigler.beehiiv.com/p/making-ai-write-like-fine-tuning-llama-3-newsletters-stepbystep-guide)
- **Jeff Wang, "Automating Your Newsletters" (Apr 19, 2023).**
  - Setup: about 40 crypto newsletters (2 MB of raw text), LLaMA 7B LoRA in Oobabooga.
  - Results: it "already sounds like me" and reproduced his coin-analysis format, but invented prices, drifted off-topic, and needed forced continuation. His verdict: "you cannot automate a financial newsletter based on previous data." — [Substack](https://jeffwang.substack.com/p/automating-your-newsletters)
- **grapeot (yage.ai), "From Prompting to Fine-tuning: Making AI More Like 'Me'" (Dec 23, 2024).**
  - Data format (back-translation): an LLM translated each of his Chinese blog paragraphs into English. The English became the input and his original Chinese became the target.
  - Training: GPT-4o fine-tuning on 50 examples gave "less AI flavor." A larger GPT-4o run cost about $100 and was inconsistent. The final models were Qwen 2.5 3B and 7B with LoRA on a rented Lambda GH200 (about $1.80/h), and their tone was "often very close to the reference answer."
  - Every prompting approach he tried before that failed (details in Q6). — [yage.ai](https://yage.ai/finetuning-en.html)

#### E. Forum posts / notes / knowledge bases

- **Jonathan Prevost, "I Built an AI Clone of Myself – Fine-Tuning with 10 Years of Data and Voice Cloning" (dev.to, Feb 17; year not shown, likely 2026 given Qwen3-TTS).**
  - Data: 8,581 parsed forum posts, filtered down to 5,136 final entries. These include 100 hand-written Q&A pairs oversampled 4× and 500 French Alpaca rows.
  - Data prep: inputs were missing for about 75% of posts, so he generated them with "reverse prompting" (Llama 3.3 70B), then ran a second LLM quality filter.
  - Model and training: Gemma 3 12B with Unsloth LoRA r32, 2 epochs, on an RTX 4060 Ti 16 GB (about 1.5 h). An earlier 24B attempt ran out of memory.
  - Evaluation: a blind survey of 10 real-vs-clone pairs. Overall recognition was 66% (50% would mean indistinguishable), and two clone replies were judged more "real" than the originals. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
- **"BitsOfChris", "I trained an AI to think like me" (Apr 25, 2025).**
  - Setup: an Obsidian vault of about 2k notes, from which gpt-4o-mini generated 50 QA pairs on one concept. LoRA via LLaMA-Factory on Colab.
  - Results: the DeepSeek-R1-distill 1.5B produced "gibberish." The 8B worked only after tuning. He concluded that "teaching a LLM something new through fine-tuning is hard" and did not adopt the model. — [blog](https://khoa-nguyen-bk18.github.io/brain/SecondBrain/I-trained-an-AI-to-think-like-me-—-here’s-what-happened)

#### F. 2026 local-first tools and anecdotes

- **Writekin (scouttyg / HN user eggbrain), Show HN, Jul 28, 2026.**
  - What it is: a macOS app that ingests Apple Mail, iMessage, documents, and chat exports, curates a corpus, and runs on-device QLoRA via MLX-Swift. A Compose screen drafts and rewrites in your voice.
  - Motivation: a SKILL.md or system prompt of anti-AI-phrasing rules still left Pangram rating the output nearly 100% AI.
  - Status: v0.9 is "uneven," sometimes matching the author's voice well and sometimes "completely off." 16 GB minimum, 32 GB+ recommended. Licensed PolyForm Noncommercial. — [HN](https://hn.algolia.com/api/v1/items/49088436); [GitHub](https://github.com/scouttyg/writekin)
- **meyerdav, HN "Can my fine-tuned model pass Pangram?" (Nov 1, 2026).** Says that after 15 minutes of fine-tuning a small local model on their own writing, Pangram rated outputs 100% human "in different instances." Self-reported; the model and data size aren't given. — [HN](https://hn.algolia.com/api/v1/items/50324089)

### Inferences
- Two families of projects dominate. Chat-message "clones" (iMessage, Telegram, Discord, Slack) are mostly entertainment or self-simulation. "Write my blog/newsletter/email" projects aim at drafting help. The second family has grown since 2025 and has shifted toward small (1.5–8B) local "voice rewriter" models fed by a frontier model.
- Model sizes went down over time (7B/13B/65B in 2023 → 3B/4B/8B in 2025–26) while reported quality held. That suggests better small instruct models (Qwen 2.5/3, Gemma 3) made small voice models viable.
- Costs are trivial. Every reported training run cost between $0 and about $100.

### Gaps
- Very few projects report held-out or blind evaluations. Only Prevost (blind survey, 66% recognition), Lopes (Jaccard overlap), and Lydon (blind A/B on 12 prompts) did anything systematic.
- Several dev.to posts don't show the year. I inferred years from the model versions they mention.
- I could not get X/Twitter threads or YouTube write-ups. Search didn't surface any that held up as primary sources, and X isn't fetchable. A Gabor Cselle livestream existed, but I didn't verify the video.

---

## Q2. Which projects used Apple silicon / MLX?

### Takeaway
MLX projects exist but are a minority, and most are small GitHub repos or blog-level experiments. The best-documented are Aditya Rathod (Mistral 7B base QLoRA on an M1 Pro 16 GB, Discord), Didier Lopes (Phi-3-mini LoRA on an M3 Max, blog), Kevin Leary (Llama 3.1 8B 4-bit, blog), and codebyandy/finetune-me (Qwen3-4B, iMessage + Slack). In 2026 the trend moved to packaged on-device apps (Writekin on MLX-Swift). I found no MLX project with a rigorous evaluation.

### Cited Findings
- **Aditya Rathod (Aug 18, 2024):** MLX QLoRA on a 4-bit Mistral 7B v0.3 base, M1 Pro 16 GB, 5,000 iters in about 5 hours, about 7.2 GB peak memory, 291k Discord messages as `{"text":...}`. He chose MLX because it is "purpose-built for my hardware." — [adibytes.dev](https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself)
- **Didier Lopes (Sep 2, 2025):** MLX LoRA on Phi-3-mini on an M3 Max (48 GB). He chose MLX for unified memory and private local experimentation. — [beehiiv](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts)
- **Kevin Leary (Sep 18, 2025):** `mlx_lm.lora` on mlx-community/Meta-Llama-3.1-8B-Instruct-4bit on a "MacBook Pro M3+", 600 iters, batch 1. — [kevinleary.net](https://www.kevinleary.net/blog/custom-ai-models-macbook-pro/)
- **codebyandy/finetune-me:** mlx-lm LoRA on Qwen3-4B-8bit using iMessage `chat.db` and Slack. Defaults are tuned for a 16 GB Mac ("~1–2h on M1 for 4B"). — [GitHub](https://github.com/codebyandy/finetune-me)
- **iClone (Mistral-7B, iMessage)** and **mlx-whatsapp (Mistral-7B base, WhatsApp)** are the two personal-data projects in the official MLX "Community Projects" discussion. That list has no writing-style, email, blog, or notes projects. — [ml-explore/mlx #654](https://github.com/ml-explore/mlx/discussions/654); [iClone](https://github.com/ishan0102/iClone); [mlx-whatsapp](https://github.com/gavi/mlx-whatsapp)
- **Writekin (Jul 2026):** a native macOS app doing QLoRA via MLX-Swift on Mail and Messages, entirely on-device. 16 GB minimum, 32 GB+ for larger models. — [GitHub](https://github.com/scouttyg/writekin)
- **NicAI (Sep 2026, plan only):** `mlx_lm.lora` / `mlx_lm.fuse` / `mlx_lm.server` on a Mac Studio M1 Ultra 128 GB. It notes that "MLX's GGUF export doesn't cover Qwen" and that adapters only work with their exact base model. — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)
- **Andrea Griffiths:** trained on a Colab T4, not MLX, but runs the 5 GB q4_k_m model locally on a 16 GB MacBook Pro. — [dev.to](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na)
- **General MLX tooling surfaced but not personal-writing-specific:** mlx-lm-lora (LoRA, DoRA, full FT, SFT/DPO), MLX-LoRA-Studio (native Mac app), mlx-tune, and Courtyard ("open-source macOS app for local MLX fine-tuning," Show HN Feb 25, 2026). — [mlx-lm-lora](https://pypi.org/project/mlx-lm-lora/); [MLX-LoRA-Studio](https://github.com/Goekdeniz-Guelmez/MLX-LoRA-Studio); [Courtyard HN](https://hn.algolia.com/api/v1/search?query=fine-tune%20MLX%20my&tags=story&hitsPerPage=30)
- One Apple-silicon playbook suggests LoRA r=4 ("~0.1% of parameters, good for style adaptation"), starting at r=8 for general use, and 100–10,000 examples. It notes that MLX counts iterations, not epochs. — [mac-playbooks](https://svah-x.github.io/mac-playbooks/playbooks/mlx-lora)
- Apple's WWDC25 MLX session says MLX LM supports full fine-tuning and LoRA locally, "without sending data off the machine." — [Apple WWDC25](https://developer.apple.com/videos/play/wwdc2025/298/)

### Inferences
- For a 16 GB Mac, the practical ceiling seen in practice is a 4-bit 7B model (Rathod) or a 4B model at 8-bit (codebyandy). Practitioners with 48–128 GB still chose small models (Phi-3-mini, Qwen2.5-1.5B), which suggests model size isn't the bottleneck for style.
- The privacy argument (iMessage and Mail never leave the machine) is the main reason people chose MLX, more than speed.
- Practitioners who did report rank found r=16 better than r=8 (Lopes; Lydon, on non-MLX hardware). That conflicts with the playbook's r=4–8 "for style" suggestion.

### Gaps
- No MLX project published a blind human evaluation or before/after metrics apart from Lopes' word overlap.
- Dates for iClone, mlx-whatsapp, and finetune-me aren't shown on their pages. iClone and mlx-whatsapp use the 2023–24 `lora.py` from mlx-examples, which suggests early 2024, but I couldn't verify that.
- I found no "fine-tune on my tweets with MLX" or "fine-tune on my email with mlx-lm" write-up with results, apart from Writekin's anecdotal v0.9 notes.

---

## Q3. Verification of the "well-known" examples (Donner, Miller, Chieng, Willison, Yan)

### Takeaway
Edward Donner and Izzy Miller are confirmed with full primary write-ups. Simon Willison didn't fine-tune on his own writing; he link-blogged other people's projects. I found no source for a "Sarah Chieng Slack/tweets clone" or for Eugene Yan fine-tuning on his own writing.

### Cited Findings
- **Edward Donner:** confirmed (Jan 2, 2024; 240,805 messages; Llama 2 7B→13B; QLoRA; V100; about $100). — [edwarddonner.com](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/)
- **Izzy Miller:** confirmed (Apr 10, 2023; about 488k messages; LLaMA 7B full FT via Alpaca code; 4×A100). — [izzy.co](https://www.izzy.co/blogs/robo-boys.html)
- **Simon Willison:**
  - He linked Miller (Apr 12, 2023), calling it "one of the clearest explanations of the process of fine-tuning a model like this I've seen anywhere."
  - He linked Lazerowitz's Slack fine-tune (Nov 8, 2023).
  - On a Homer Simpson LLaMA fine-tune (Mar 17, 2023) he wrote: "I've been skeptical about how much value can be had from fine-tuning large models on just a tiny amount of new data. Clearly my mental model around this was incorrect."
  - He also quoted OpenAI's Ted Sanders (Apr 15, 2023): fine-tuning is not recommended "as a way to teach the model knowledge."
  - Sources: [simonwillison.net/tags/fine-tuning](https://simonwillison.net/tags/fine-tuning/); [Miller link](https://simonwillison.net/2023/Apr/12/replacing-my-best-friends)
- **Sarah Chieng:** no fine-tuning clone project found. The only hit was an unrelated Val Town Twitter-search tool credited to her and Alex Phan. — [val.town](https://val.town/v/alexdphan/twitterSearch/references?view=list)
- **Eugene Yan:** search returned only his writing-process essays and podcasts, nothing on fine-tuning a model on his own writing. — [eugeneyan.com](https://eugeneyan.com/speaking/writing-for-a-tech-career/)

### Inferences
- The caller may have confused the "Sarah Chieng" example with DoppelBot (Modal's Slack clone) or Ross Lazerowitz's Slack fine-tune, which are the well-known Slack-clone examples.

### Gaps
- Possible X/Twitter-only posts by Chieng or Yan couldn't be searched, since X isn't fetchable.

---

## Q4. How did people format the training data?

### Takeaway
There are five recurring formats:
1. Raw text continuation on a base model.
2. Multi-speaker transcripts under a persona instruction.
3. Context → my reply pairs from threads.
4. Synthetic or back-generated prompts for standalone writing (titles, NER tags, LLM-written questions, "reverse prompting," back-translation).
5. Draft → my rewrite pairs.

Reply pairs work naturally for chat and email. Standalone essays and tweets have no natural prompt, so people have to invent one. That step is where most of the effort, and many of the quality problems, come from.

### Cited Findings
- **Raw text continuation (base model).**
  - Rathod merged messages less than 15 minutes apart into `{"text":...}` docs and found that "Instead of fine-tuning the instruct models on free text, I should be training the _base_ models instead." — [adibytes.dev](https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself)
  - Jeff Wang trained a LoRA on a 2 MB raw-text file. — [Substack](https://jeffwang.substack.com/p/automating-your-newsletters)
  - CMU's StyleTunedLM trains LoRA with plain next-token prediction on 256-token chunks of author text. It masks person names out of the loss, and restores instruction following by merging with a LIMA instruction LoRA. — [arXiv 2409.04574](https://arxiv.org/html/2409.04574v1)
- **Multi-speaker transcript plus persona instruction.**
  - Donner: system "Write a realistic text message chat. Avoid repetition." plus `### Name: message` lines, in 7–10-message chunks. — [edwarddonner.com](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/)
  - Miller: an Alpaca instruction naming the six members, with sessions split on a 4-hour gap. — [izzy.co](https://www.izzy.co/blogs/robo-boys.html)
  - Telegram: ChatML sessions with loss on all participants, so the model can role-play partners. The author suggests training on one person's replies only as an improvement. — [HackerNoon](https://hackernoon.com/i-fine-tuned-an-llm-with-my-telegram-chat-history-heres-what-i-learned)
- **Context → my reply pairs.**
  - Lazerowitz: preceding Slack messages as the user turn, his replies as the assistant turn. — [rosslazer.com](https://rosslazer.com/posts/fine-tuning)
  - codebyandy: the last 6 turns, then his reply, under the system prompt "You are Andy. You are messaging {contact} in {channel}." — [GitHub](https://github.com/codebyandy/finetune-me)
  - DoppelBot converts scraped Slack messages into prompt/response pairs (per a search summary; the README itself doesn't describe the format). — [GitHub](https://github.com/modal-labs/doppel-bot)
  - Prevost: forum quote → reply. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
  - Carmo: up to 10 prior messages → next message, with a 120-minute session gap. — [duarteocarmo.com](https://duarteocarmo.com/blog/fine-tune-flan-t5-telegram)
- **Synthetic or back-generated prompts for standalone writing.**
  - Kevin Leary: a templated prompt from post metadata, e.g. `"write a blog post ... entitled "{title} - {lead-in}" as if it were originally published on {date}"`. — [kevinleary.net](https://www.kevinleary.net/blog/custom-ai-models-macbook-pro/)
  - Cselle: NER entity tags from each tweet used as the prompt. — [GitHub](https://github.com/gaborcselle/write-my-posts)
  - Prevost: "reverse prompting" with Llama 3.3 70B to invent the missing input for about 6,200 posts (about 18 minutes), then an LLM quality filter that removed tautological or hallucinated pairs. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
  - Lopes: 91 posts turned into about 2,100 Q&A exchanges in the Phi-3 chat template. — [beehiiv](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts)
  - Nottingham: a mix of 20 full-post completions ("Write a blog post about AI safety:"), 33 instructions, and 61 Q&A. She reports that the mix "produced a more versatile model." — [GitHub](https://github.com/LydNot/clone)
  - Sarah Constantin: she wrote the questions herself, with the target-author quotes as answers. — [Substack](https://sarahconstantin.substack.com/p/fine-tuning-llms-for-style-transfer)
  - Daigler: instruction plus blank input → newsletter. — [beehiiv](https://michaeldaigler.beehiiv.com/p/making-ai-write-like-fine-tuning-llama-3-newsletters-stepbystep-guide)
  - OpenAI forum suggestions for tweets: a fixed "tweet in the style of [user]:" prompt, topic summaries, or GPT-written prompts per tweet ("could get expensive at scale"). — [OpenAI forum](https://community.openai.com/t/fine-tuning-on-someones-tweets-to-match-their-tone-and-writing-style/40213)
- **Draft/translation → my version (rewrite pairs).**
  - grapeot back-translated his Chinese paragraphs into English (input) → original Chinese (output). — [yage.ai](https://yage.ai/finetuning-en.html)
  - Lydon's 3B model is used as a rewriter of frontier drafts, though it was trained on two-turn conversations. — [dev.to](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)
  - NicAI treats 169 "draft-and-sent" email pairs as the strongest supervision. — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)
- **Conditioning metadata:** contact and channel in the system prompt (codebyandy), source labels to route between email, chat, and post voices (Lydon), and the date in the prompt (Leary). — [codebyandy](https://github.com/codebyandy/finetune-me); [Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi); [Leary](https://www.kevinleary.net/blog/custom-ai-models-macbook-pro/)
- **Mixing in general instruction data:** Prevost added 500 French Alpaca rows, Larson added 161 OpenHermes rows, and Daigler first trained on Alpaca-cleaned. — [Prevost](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60); [Larson](https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E); [Daigler](https://michaeldaigler.beehiiv.com/p/making-ai-write-like-fine-tuning-llama-3-newsletters-stepbystep-guide)
- **Template correctness:** Lopes found early failures came from the wrong chat template and a missing system prompt. Larson notes that with an instruct model "raw text wastes training signal." — [Lopes](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts); [Larson](https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E)

### Inferences
- The format has to match the model type. Raw continuation goes with base models; chat-template pairs go with instruct models. Rathod's instruct-model failure and Lopes' template bug show this is a common first mistake.
- For long-form writing (blogs, essays), the most usable patterns seem to be a metadata-templated prompt (title, topic, date) or an LLM-generated "reverse prompt." Q&A conversion moves the model toward knowledge and answer length rather than essay voice (Lopes' output lengths moved toward the reference answers).
- Rewrite pairs (generic draft → your version) match the most useful downstream job, "rewrite this in my voice," and avoid asking the small model to reason. Several 2025–26 practitioners converged on this pattern independently (Lydon, NicAI, Writekin's "rewrite").

### Gaps
- No practitioner A/B-tested formats against each other on the same data (e.g., raw continuation vs. reverse-prompted pairs). That comparison isn't in the found sources.

---

## Q5. What data volumes were enough, and what failed?

### Takeaway
Tone and surface style appear with surprisingly little data: about 50 to a few hundred examples (grapeot's 50 for GPT-4o, Griffiths' 81, Nottingham's 114, Cselle's 200 tweets). Cselle saw only modest gains going from 200 to about 4,000 tweets. Large corpora (100k+ messages) don't fix coherence or context. The recurring failures are short or generic replies learned from short messages, repetition loops, exaggerated caricature, confident hallucination of facts, overfitting and memorization on tiny sets, loss of general ability, and leaks of private information.

### Cited Findings
**Volumes and outcomes (small to large):**
- **About 20 examples:** Pandey said the model was "Probably not" ready and flagged memorization risk. — [dev.to](https://dev.to/shresthapandey/i-fine-tuned-llama-32-on-my-own-writing-style-using-lora-unsloth-and-a-free-colab-gpu-13l5)
- **50 examples (GPT-4o):** "less AI flavor than native GPT-4o." — [yage.ai](https://yage.ai/finetuning-en.html)
- **81 examples (Qwen3 8B):** captured her style; "rank 16 was the sweet spot for eighty-one examples of my voice." — [dev.to](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na)
- **114 examples, about 91k tokens (Llama 3.1 70B):** she liked the outputs; informal evaluation. — [GitHub](https://github.com/LydNot/clone)
- **124 quotes (GPT-3.5, Dune style):** style transfer "clearly happening." — [Substack](https://sarahconstantin.substack.com/p/fine-tuning-llms-for-style-transfer)
- **200 tweets → about 4,000 tweets (GPT-3.5):** tone matched at 200; the 4k run was only "a little bit better." — [GitHub](https://github.com/gaborcselle/write-my-posts)
- **6 own articles inside 224 total (Mistral 7B, 5 epochs):** loss 0.09 and 97% token accuracy, which looks like memorization; it hallucinated code. — [grizzlypeaksoftware.com](https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E)
- **About 2,100 Q&A from 91 posts (Phi-3-mini):** +27.6% word overlap; knowledge transfer weak. — [beehiiv](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts)
- **5,136 entries (Gemma 3 12B):** 66% blind recognition. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
- **Large message corpora:** 15.8k sessions (Telegram), 25k chunks / 240k messages (Donner), about 30k messages (muttled 65B), 75k samples / 3.1M tokens (Lydon), 140k Slack messages / 10.4M tokens (Lazerowitz), 291k (Rathod), 488k (Miller). All captured style; all reported coherence, context, or register problems. — sources as cited in Q1.
- **Research:** StyleTunedLM's style-classifier accuracy rose with data: 0.11 at 5%, 0.44 at 35%, 0.81 at 70%, 0.88 at 100% of each author's books. Its experiments start around 80k tokens. It frames the target user as having "some 1k-50k tokens of prior work" and lists low-resource users as untested. — [arXiv 2409.04574](https://arxiv.org/html/2409.04574v1)
- **Rules of thumb from practitioners:** "Start with hundreds of paired examples, ideally 1,000+," LoRA rank about 16, 1–3 epochs for style. — [daehnhardt.com](https://daehnhardt.com/blog/2025/10/16/lora-fine-tuning-wins/) (seen in search summary; not fetched). A Reddit commenter said fine-tuning "requires hundreds of your own examples" with modest gains over a well-prompted base. — [Reddit snapshot, r/AI_Agents, ~Nov 2025](https://reddit.sentinel-team.org/posts/1t6dkqw/snapshots/2026-05-08T19%3A17%3A52.632086Z)

**Failure modes:**
- **Short or generic replies inherited from short messages.**
  - Rathod: "I was literally conditioning it to give really short responses." — [adibytes.dev](https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself)
  - Telegram: replies like "ok" or "busy" dominated. — [HackerNoon](https://hackernoon.com/i-fine-tuned-an-llm-with-my-telegram-chat-history-heres-what-i-learned)
  - Prevost: removed messages under 6 words. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
  - Unverified: a search summary says a Mistral-7B Telegram persona replied with single characters and emoji until short messages were filtered. — [blog-rgu (search snippet)](https://blog-rgu.pages.dev/blog/fine-tuning-mistral-telegram-persona)
- **Repetition loops.**
  - Donner: endless rescheduling and lunch debates. — [edwarddonner.com](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/)
  - Rathod: repeated "i love rust." — [adibytes.dev](https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself)
  - Stroet: echoed its input. — [gotimo2](https://gotimo2.github.io/posts/training-an-llm-on-150k-discord-messages)
- **Caricature or exaggeration.**
  - Miller: "optimized for outrageous behavior"; over-used tapbacks. — [izzy.co](https://www.izzy.co/blogs/robo-boys.html)
  - Constantin's bot "will spontaneously argue with and belittle the user" and is "more prone to non sequiturs." — [Substack](https://sarahconstantin.substack.com/p/fine-tuning-llms-for-style-transfer)
  - NicAI: style markers "become tics after too many epochs on few examples." — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)
  - Lazerowitz: an unwanted brusque tone. — [rosslazer.com](https://rosslazer.com/posts/fine-tuning)
- **Confident fabrication; style without facts.**
  - Wang: invented prices. — [Substack](https://jeffwang.substack.com/p/automating-your-newsletters)
  - Larson: "hallucinated code. Confidently." — [grizzlypeak](https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E)
  - codebyandy: "plausible nonsense." — [GitHub](https://github.com/codebyandy/finetune-me)
  - muttled: an astronaut mother. — [HN](https://hn.algolia.com/api/v1/items/36815443)
  - NicAI: "The rewriter washes out the facts." — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)
  - BitsOfChris: "teaching a LLM something new through fine-tuning is hard." — [blog](https://khoa-nguyen-bk18.github.io/brain/SecondBrain/I-trained-an-AI-to-think-like-me-—-here’s-what-happened)
- **Loss of general ability:** Lazerowitz's model was worse at other tasks. — [rosslazer.com](https://rosslazer.com/posts/fine-tuning)
- **Instruct vs. base mismatch:** Rathod's instruct model gave one-word replies on free text. — [adibytes.dev](https://hn.jakechampion.name/reader/https://adibytes.dev/writing/training-a-bot-on-myself)
- **Register mismatch.** Slack style isn't general style (Lazerowitz). A casual-heavy corpus is weak at long-form, and Lydon suggests oversampling formal writing. — [rosslazer.com](https://rosslazer.com/posts/fine-tuning); [dev.to](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)
- **Training on AI text.** Heralax's role-swapped ChatGPT export made the model "slightly stilted." NicAI warns of learning "to imitate an imitation." — [Reddit mirror](https://lr.us.psf.lt/r/LocalLLaMA/comments/1bzczyc/trained_an_llm_on_my_own_writings_somewhat_funny/kyp20tu/?context=3); [NicAI](https://notes.nicolasdeville.com/nicai/slm/)
- **Loss is a misleading signal.** Donner's quality kept rising while loss rose. NicAI: "Lower training loss can mean memorisation. Judge on held-out data only." — [Donner](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/); [NicAI](https://notes.nicolasdeville.com/nicai/slm/)
- **Noise in the data:** tapbacks, images, and links (Miller); a counting channel (Stroet); quoted reply text and duplicates (Lydon). — [izzy.co](https://www.izzy.co/blogs/robo-boys.html); [gotimo2](https://gotimo2.github.io/posts/training-an-llm-on-150k-discord-messages); [Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)
- **Privacy and PII.**
  - mlx-whatsapp warns that fused models can leak chat data. — [GitHub](https://github.com/gavi/mlx-whatsapp)
  - Donner removed a deceased friend's data as "extremely poor taste." — [edwarddonner.com](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/)
  - Prevost says PII scrubbing would be "absolutely critical" for any public release. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
  - HN commenters raised consent concerns about modeling partners or deceased people. — [HN](https://hn.algolia.com/api/v1/items/35540154)
- **Memory limits:** Qwen 3.5 9B ran inference but ran out of memory in training (Lydon). Mistral Small 24B ran out of memory on save (Prevost). — [Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi); [Prevost](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
- **Too-small models:** opt-125m (Stroet) and DeepSeek-R1-distill 1.5B (BitsOfChris) produced nonsense or gibberish. — [gotimo2](https://gotimo2.github.io/posts/training-an-llm-on-150k-discord-messages); [blog](https://khoa-nguyen-bk18.github.io/brain/SecondBrain/I-trained-an-AI-to-think-like-me-—-here’s-what-happened)

### Inferences
- Learning curves for voice appear to saturate early: a few hundred clean examples is enough for tone. Beyond that, the gains come from cleaning (length filters, deduplication, removing AI text) and from matching the training register to the target task, more than from raw volume.
- "Sounding like a caricature" seems tied to small datasets, many epochs, and noisy, emotionally loud chat data. Practitioners used lower LRs, fewer epochs, rank 16, and decoding controls (temperature, repetition or frequency penalty) to counter it.

### Gaps
- No one ran a controlled data-scaling curve on *personal* (non-famous) writing. StyleTunedLM's curve uses Gutenberg authors who are likely already in the pretraining data, a limitation the authors themselves state.
- Memorization was rarely measured. Only Donner searched for regurgitated conversations.

---

## Q6. Did fine-tuning beat a good style guide plus few-shot prompting with a frontier model?

### Takeaway
The evidence leans toward yes for voice: fine-tuning beats prompting at matching surface voice, especially casual or idiosyncratic voice. Supporting it: practitioner reports (grapeot, Constantin, Cselle, Writekin, Lydon), one controlled academic study (StyleTunedLM), and a 2025 study showing few-shot prompting failing on informal everyday authors. The caveats are that almost no practitioner ran a head-to-head against a well-built frontier prompt, and many advisors still say to prompt first. The emerging 2025–26 consensus is a hybrid: a frontier model decides *what* to say, and a small fine-tuned model decides *how* to say it.

### Cited Findings
- **grapeot tried every prompting approach first and all of them failed:** abstract style descriptions, referencing famous writers, random few-shot, retrieval-based few-shot ("no significant gain"), and commercial style features. Fine-tuned Qwen came "often very close to the reference." — [yage.ai](https://yage.ai/finetuning-en.html)
- **Sarah Constantin:** prompting is "lousy for making a bot with a writing style that's substantially different from the generic ChatGPT 'character'." With pasted samples, "it inexorably reverts to the bland 'house style.'" Fine-tuning worked, at a cost in coherence. — [Substack](https://sarahconstantin.substack.com/p/fine-tuning-llms-for-style-transfer)
- **Gabor Cselle:** his earlier few-shot approach at Pebble failed to match users' voices, which motivated fine-tuning. — [GitHub](https://github.com/gaborcselle/write-my-posts)
- **Writekin's author:** a SKILL.md or system prompt of anti-AI rules "improved the surface somewhat," but Pangram still rated the output nearly 100% AI. He fine-tuned instead, with uneven results. — [HN](https://hn.algolia.com/api/v1/items/49088436)
- **Nic Lydon:** "Prompt engineering has a ceiling for voice matching. I built the thing that goes above it." His baseline was the untuned base model, not a prompted frontier model. — [dev.to](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)
- **StyleTunedLM (CMU; Liu, Diddee, Ippolito; Sep 2024).** LoRA on author text beat 5-shot and 10-shot prompting and an instruct-plus-style-instruction baseline (Llama-2-7b family):

  | Method | Classifier accuracy | Lexical MSE | Surface MSE |
  |---|---|---|---|
  | StyleTunedLM | 0.879 | 1.39 | 2.04 |
  | 5-shot | 0.693 | 3.80 | 5.43 |
  | Instruct | 0.263 | — | — |

  Caveats: the authors were famous and likely present in pretraining data, and frontier models weren't tested. — [arXiv 2409.04574](https://arxiv.org/html/2409.04574v1)
- **"Catch Me If You Can? Not Yet" (arXiv 2509.14543, Sep 2025).** More than 400 real everyday authors across email, news, blogs, and forums, and more than 40,000 generations from GPT-4o, Gemini 2.0 Flash, DeepSeek-V3, Llama 4 and others. Few-shot imitation "can approximate user styles in structured formats like news and email," but "struggle[s] with nuanced, informal writing in blogs and forums." More examples gave diminishing gains. — [arXiv](https://arxiv.org/html/2509.14543v1)
  - A secondary review reports blog authorship-verification accuracy of roughly 17–21% at 5-shot, and that outputs were still flagged by GPTZero. I didn't verify these against the PDF. — [themoonlight.io](https://www.themoonlight.io/en/review/catch-me-if-you-can-not-yet-llms-still-struggle-to-imitate-the-implicit-writing-styles-of-everyday-authors)
- **A DEV Community experiment** compared Claude's custom style feature and manual prompting on Steven Pressfield's writing. It concluded that "finetuning remains the more reliable though often more resource intensive option." Seen via a search summary; not fetched. — [dev.to](https://dev.to/thatechmaestro/replicate-an-authors-writing-style-using-prompt-engineering-insights-from-an-experiment-with-2hfk)
- **arXiv 2507.04889 (Jul 2025):** on agent tone of voice, fine-tuning outperformed system prompting even with 100 samples. Seen via a search summary; not fetched. — [arXiv](https://arxiv.org/pdf/2507.04889.pdf)
- **Counter-views (prompt first).**
  - A Reddit commenter: fine-tuning is "overkill" for personal style; put 10–15 of your sentences in a system prompt instead. — [Reddit snapshot](https://reddit.sentinel-team.org/posts/1t6dkqw/snapshots/2026-05-08T19%3A17%3A52.632086Z)
  - NicAI: "Prompting comes first," and "The real baseline is a well-prompted frontier model, not a generic one." — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)
  - OpenAI's Ted Sanders (2023): fine-tuning isn't recommended for teaching knowledge. — [simonwillison.net](https://simonwillison.net/tags/fine-tuning/)
  - On Miller's HN thread, commenters argued that sounding like someone is not thinking like them, and that "you won't get more facts out than you provide as input" (MayeulC). — [HN](https://hn.algolia.com/api/v1/items/35540154)
- **Planned head-to-heads, no results yet:** codebyandy plans "a frontier model prompted with 20 examples," and NicAI plans "Claude with SOUL.md." — [codebyandy](https://github.com/codebyandy/finetune-me); [NicAI](https://notes.nicolasdeville.com/nicai/slm/)
- **Anthropic's Messages API has no fine-tuning endpoint**, so customizing Claude means prompting, caching, or tools (as stated on the NicAI page). — [notes.nicolasdeville.com](https://notes.nicolasdeville.com/nicai/slm/)

### Inferences
- In practitioner reports, fine-tuning wins most clearly for *casual, idiosyncratic, or non-default* voices (texting, lowercase, terse Slack, non-English blogs). That matches "Catch Me If You Can," which found few-shot works acceptably for structured formal genres.
- What counts as "better" depends on the task. Fine-tuned small models sound right but lose facts and reasoning. The hybrid draft-then-rewrite pattern (Lydon, NicAI, Writekin's rewrite mode) is how practitioners try to get both.
- AI-detector scores (Pangram, GPTZero) are becoming an informal metric for voice models in 2026 (Writekin, meyerdav). These reports are self-selected and not rigorous.

### Gaps
- I found no published practitioner head-to-head of "fine-tuned small model vs. frontier model plus style guide plus retrieved few-shot" judged blind on the same person's held-out writing. That is the key missing evidence.

---

## Q7. Commercial products for "write in my voice": how they claim to do it

### Takeaway
Nearly all mainstream products build the voice by analyzing samples into a profile or style description and injecting that into prompts, sometimes with sample retrieval. They don't fine-tune per user. The exceptions are Personal.ai, which claims a small per-user model, and Hypotenuse, whose marketing says "bespoke models" without detail. Several explicitly say they don't train models on customer data.

### Cited Findings
- **Jasper Brand Voice:** "Upload up to 8 examples of text, files (.txt, .pdf, or .docx), and/or URLs." Jasper analyzes tone and style to build an editable voice description. Style Guides (rules) are separate and Business-tier only. Memory stores facts. Jasper says it "doesn't train large language models (LLMs) on your data." — [Jasper help](https://help.jasper.ai/hc/en-us/articles/18618693085339-Brand-Voice); [Jasper help (alt)](https://help.jasper.ai/hc/articles/18618693085339-Brand-Voice)
- **Grammarly / Superhuman voice:** launched October 2023 as "personalized voice detection and application." It automatically builds a voice profile that "evolves as you write." The profile's role and dialect are editable, and it recognizes that short messages and long documents differ. Available on Business and Enterprise, and to Pro users via the Humanizer agent. A Paraphraser "custom voice" is built from a few examples. — [Grammarly support](https://support.grammarly.com/hc/en-us/articles/23153676821773-Introducing-voice-features); [Superhuman help](https://help.superhuman.com/hc/en-us/articles/46242251232781-Introducing-voice-features); [TechCrunch](https://techcrunch.com/2023/10/25/grammarlys-new-generative-ai-feature-learns-your-style-and-applies-it-to-any-text)
- **Writer.com:** a "personal voice profile" (AI Studio → Voice & style) built automatically from analyzed samples, or by picking style characteristics. TechTarget reports two Palmyra models, one for voice extraction and one for voice generation. — [Writer support](https://support.writer.com/articles/4354376534-how-to-set-up-and-use-your-personal-voice-profile); [TechTarget](https://www.techtarget.com/searchenterpriseai/news/366575533/Writer-Incs-new-AI-tool-generates-voice-of-marketers-content)
- **Hypotenuse AI:** claims to study "all of your existing content and brand guidelines" and that "bespoke models learn how your brand actually speaks." This is marketing with no technical detail. — [Hypotenuse](https://hypotenuse.ai/features/brand-voice)
- **Personal.ai:** claims a per-user "Personal Language Model" of about 120M parameters, trained on your "Memory Stack," plus retrieval of 8–10 memory blocks per prompt. It also says edits feed back into training. Company claims only, internally inconsistent, with no independent technical documentation. — [Personal.ai PLM](https://www.personal.ai/plm-personal-and-large-language-models); [PAI Academy](https://www.personal.ai/pai-academy/chat-prompting-and-carrying-context-with-a-persona)
- **Delphi (digital clones):** a RAG pipeline on Pinecone, with "over 100 million stored vectors across 12,000+ namespaces." Its CTO: "Even if we have billion-token context windows, RAG will still be important." I found no evidence of per-creator fine-tuning. — [CO/AI on Pinecone case study](https://getcoai.com/news/delphi-scales-ai-chatbots-to-100m-vectors-using-pinecone-database/)
- **Every's Spiral:** a v4 "Style Engine" computes a "writing fingerprint," picks relevant samples, and "uses stylometry" at draft time. Every says an LLM-as-judge blind-lineup eval runs on every draft, and claims drafts are indistinguishable 87% of the time (vendor claim). Help docs recommend 3–5+ samples and separate styles per context. — [Every announcement link](https://every.to/emails/click/6c97bb0a1707598998fd8cfab915fb8cecd7c5507e895982b0a15fd991072efd/eyJzdWJqZWN0IjoiU3BpcmFsIDQuMCBHb2VzIEFnZW50LW5hdGl2ZSIsInBvc3RfaWQiOjQyODgsInBvc3RfdHlwZSI6InBvc3QiLCJ1cmwiOiJodHRwczovL2V2ZXJ5LnRvL29uLWV2ZXJ5L3NwaXJhbC00LTAtZ29lcy1hZ2VudC1uYXRpdmUiLCJwb3NpdGlvbiI6Mn0=); [Every help](https://help.every.to/en/articles/13231409-why-don-t-the-drafts-match-my-writing-style)
- **Claude Styles (Anthropic, Nov 2024):** upload or paste writing samples (pdf/doc/txt) to create a custom style, or describe the style instead. The result is a reusable style instruction, i.e. prompting. — [Anthropic support](https://support.anthropic.com/en/articles/10181068-configuring-and-using-styles); [Claude blog](https://claude.com/blog/styles)
- **Rephrasy.ai** was promoted in a Reddit comment as learning style from uploaded text "without training a model" and as passing "every AI detector." Unsupported. — [Reddit snapshot](https://reddit.sentinel-team.org/posts/1t6dkqw/snapshots/2026-05-08T19%3A17%3A52.632086Z)
- **Open-source per-user fine-tuning "products":** DoppelBot (Slack, on Modal), WeClone (chat to digital twin, 18.4k stars), and Writekin (on-device macOS, noncommercial license). — [DoppelBot](https://github.com/modal-labs/doppel-bot); [WeClone](https://github.com/xming521/WeClone); [Writekin](https://github.com/scouttyg/writekin)

### Inferences
- Commercial vendors seem to avoid per-user fine-tuning, probably because of cost, privacy ("we don't train on your data" is a selling point), and the lack of fine-tuning on frontier APIs (e.g., Anthropic). So the "fine-tune on my writing" niche falls to open-source and local tools. That's an opening for an on-device product.
- Spiral's LLM-as-judge "pick the fake from a lineup" test is the most concrete automatic voice evaluation I found in a product, and it's a template individuals could copy.

### Gaps
- I found no documentation of how **Typefully** or **Lex** do voice matching. Searches returned nothing relevant, so they're omitted.
- None of the vendors' style-match claims are independently verified.

---

## Q8. Recurring lessons across projects

### Takeaway
Across 2023–2026 write-ups, the same points keep coming back:
1. Fine-tuning teaches voice, not facts.
2. The data work (export, cleaning, pairing, filtering) is the project; training is cheap and fast.
3. Match the data format to the model (base vs. instruct, exact chat template).
4. Short or noisy chat data produces short, noisy, looping output.
5. Training loss misleads; judge blind on held-out data.
6. Hybrid architectures (frontier for content, small tuned model for voice) are what people converge on.
7. Privacy is a first-class constraint, which is what drives local or MLX training.

### Cited Findings
- **Style, not knowledge.**
  - "The model learned my _style_. It did not learn the _facts_." — [Larson](https://grizzlypeaksoftware.com/articles/p/i-fine-tuned-a-7b-model-on-my-own-writing-in-one-evening-heres-exactly-how-8dj49E)
  - "Fine-tuning shapes behavior and style more than it adds information." — [Lopes](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts)
  - Fine-tuning "can't give AI a new ability"; tests showed it couldn't add knowledge. — [grapeot](https://yage.ai/finetuning-en.html)
  - "learned how I write. Not how I think." — [Griffiths](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na)
- **Data work dominates.**
  - "The data work is the project, and the training is an afternoon at the end of it." — [NicAI](https://notes.nicolasdeville.com/nicai/slm/)
  - "a model is only as good as its data." — [Prevost](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
  - "The actual training process ended up being the easiest step." — [Pandey](https://dev.to/shresthapandey/i-fine-tuned-llama-32-on-my-own-writing-style-using-lora-unsloth-and-a-free-colab-gpu-13l5)
- **Base model choice matters a lot:** switching to Qwen3 8B "improved the output more than any hyperparameter tweak" (Griffiths). Gemma 3 was the "sweet spot" after Qwen3 and Ministral gave inconsistent results (Prevost). 13B was a "marked improvement" over 7B (Donner). — [Griffiths](https://dev.to/andreagriffiths11/an-experiment-in-voice-what-happens-when-ai-learns-to-write-like-you-36na); [Prevost](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60); [Donner](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/)
- **LoRA is enough:** on the Telegram data, LoRA was nearly as good as a full fine-tune at a fraction of the cost. — [HackerNoon](https://hackernoon.com/i-fine-tuned-an-llm-with-my-telegram-chat-history-heres-what-i-learned)
- **Rank and modules:** rank 16 beat 8 (Lopes, Lydon). Including MLP projections mattered for vocabulary (Lydon: q/k/v-only gave "the wrong vocabulary"). — [Lopes](https://didierlopes.beehiiv.com/p/fine-tuning-an-llm-on-my-blog-posts); [Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi)
- **Decoding matters as much as training:** Donner (prompt, format, and generation changes), Lazerowitz (temperature and frequency penalty fixed erratic output), Miller (beam search, temperature 0.75). — [Donner](https://edwarddonner.com/2024/01/02/fine-tuning-an-llm-on-240k-text-messages/); [Lazerowitz](https://rosslazer.com/posts/fine-tuning); [Miller](https://www.izzy.co/blogs/robo-boys.html)
- **Evaluation:** "There is no dependable automatic metric for 'sounds like me'"; use a blind human comparison. — [NicAI](https://notes.nicolasdeville.com/nicai/slm/). Prevost's blind friends survey (66%) is the best practitioner example. — [dev.to](https://dev.to/jprevo/i-built-an-ai-clone-of-myself-fine-tuning-with-10-years-of-data-and-voice-cloning-4h60)
- **Separate reasoning from voice:** Lydon's two-tier design. NicAI warns it adds failure points, latency, and fact wash-out. — [Lydon](https://dev.to/niclydon/i-trained-an-llm-on-75k-of-my-own-messages-so-it-would-stop-writing-like-a-chatbot-1dpi); [NicAI](https://notes.nicolasdeville.com/nicai/slm/)
- **Privacy:** "Nothing leaves your machine" (Writekin). "Train locally" and keep data/adapters out of the repo (codebyandy). Don't publish fused models (mlx-whatsapp). Scrubbing PII can itself cause odd hallucinations (muttled). — [Writekin](https://github.com/scouttyg/writekin); [codebyandy](https://github.com/codebyandy/finetune-me); [mlx-whatsapp](https://github.com/gavi/mlx-whatsapp); [HN](https://hn.algolia.com/api/v1/items/36815443)
- **Cost:** about $0 (Colab, Griffiths), $0.13 (Tinker, Nottingham), $2–3 (vast.ai, Telegram), $83.20 (OpenAI, Lazerowitz), about $100 (Donner, Miller, and grapeot's GPT-4o run). NicAI advises budgeting "5 to 10 times your first estimate, because the spend is in the reruns." — sources as cited above.

### Inferences
- For a product that adapts a model to one person's writing on Apple silicon, these practitioner results point to the following design:
  - a 3–8B instruct model with LoRA r≈16 on attention and MLP projections;
  - a few hundred to a few thousand cleaned, register-labeled examples;
  - rewrite or reply pairs rather than raw dumps;
  - minimum-length and AI-text filters;
  - a blind held-out evaluation against a strong prompted frontier baseline;
  - facts supplied at inference time, not baked into the weights.
- The field has many anecdotes and almost no controlled evidence. Anyone who publishes a careful blind comparison (fine-tune vs. frontier plus style guide plus retrieved few-shot) on personal, non-famous writing would be filling a real gap.

### Gaps
- No longitudinal reports, e.g. whether people kept using their voice model after a few months. Griffiths notes the model freezes your voice in time ("will always sound like 2026 Andrea"), but nobody reports retraining cadence.
- Reddit r/LocalLLaMA threads were mostly unfetchable (reddit.com is blocked, and the mirrors were unstable), so community advice beyond the few cited snippets may be under-represented.
