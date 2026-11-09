# Using negative (slop) examples in training or decoding for a local 7-9B style model on Apple silicon

Scope: methods that use text labeled bad / AI slop as a negative signal, for a QLoRA style adapter (author-voice rewriting of informational nonfiction). Training runs in mlx-lm / mlx-lm-lora / mlx-tune on an M4 Pro with 24 GB. Research date: 2026-11-07. Package versions checked on PyPI that day: mlx-lm 0.32.2 (uploaded 2026-10-16), mlx-lm-lora 5.10.2 (2026-10-26), mlx-tune 0.6.0 (2026-06-23). Code-level claims come from the `main` branches of those GitHub repos on the same day. "UNVERIFIED" marks claims that come from memory or reasoning rather than a fetched source.

---

## Key Question 1: Given noisy, unpaired, off-domain human slop labels, which method (if any) is likely to help a style adapter beyond synthetic paired negatives (the model's own outputs as rejected)?

### Takeaway
Don't put the harvested slop into a sequence-level preference loss (DPO, ORPO, CPO, SimPO, or KTO) as rejected text for the style adapter. On-domain paired negatives (your model's own outputs, or a generic LLM rewrite of the same content) are the stronger and safer signal, with direct precedent in SPIN, ASTRAPOP and StyleVector. The harvested slop is worth more as a source of features: mine it for over-represented words, phrases and regexes, then apply those through token-level FTPO on your own model's generations (native in mlx-lm-lora as `--train-mode ftpo`), through a decoding-time banlist, or through a reranking classifier. KTO is the only principled sequence-level method for unpaired binary labels. But mlx-lm-lora has no KTO trainer, and mlx-tune's `KTOTrainer` is a simplified loss without the KL reference point, so true KTO on MLX means writing custom code.

### Cited Findings

#### A. Preference optimization with paired negatives (sequence-level)

**DPO.**
- mlx-lm-lora: `--train-mode dpo`, `--beta` (default 0.1), `--dpo-cpo-loss-type` ∈ {`sigmoid`, `hinge`, `ipo`, `dpop`}, `--delta` (hinge margin, default 50.0). Data fields are `prompt`, `chosen`, `rejected` (optional `system`). Use `--reference-model-path` to set the reference; otherwise the main model is used — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- `train.py` loads a second full copy of the model as the reference (`load(args.reference_model_path)`, or `load(args.model)` when unset), so a DPO run holds two copies of the base weights — [mlx-lm-lora train.py](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora/blob/main/mlx_lm_lora/train.py).
- mlx-tune: `DPOTrainer`/`DPOConfig` is native MLX. It has a `label_smoothing` option (cDPO-style) and precomputes frozen reference log-probs from the pre-LoRA base — [mlx-tune rl_trainers.py](https://github.com/ARahim3/mlx-tune/blob/main/mlx_tune/rl_trainers.py); [mlx-tune PyPI](https://pypi.org/project/mlx-tune/).
- Known failure modes: DPO "lowering the likelihood of preferred responses", inducing verbosity and reducing diversity (cited in the Antislop related work). The paper also says β is "a coarse tool, impairing learning at high values and causing model degradation by allowing large logit divergences from reference at small (β)" — [Antislop, arXiv 2510.15061](https://arxiv.org/abs/2510.15061).

**ORPO.**
- mlx-lm-lora: `--train-mode orpo`, `--beta` (0.1), `--reward-scaling` (1.0). Takes an optional `preference_score` field, and chosen/rejected may be `{"messages": [...]}`. No reference model — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- mlx-tune: `ORPOTrainer` is native MLX — [mlx-tune PyPI](https://pypi.org/project/mlx-tune/).
- In the KTO paper, even the reference-free KTO variant "strictly outperforms ORPO" — [KTO, arXiv 2402.01306](https://arxiv.org/abs/2402.01306).

**CPO.**
- mlx-lm-lora: `--train-mode cpo`, with the same flags as DPO — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- Not listed in mlx-tune — [mlx-tune PyPI](https://pypi.org/project/mlx-tune/).

**SimPO.**
- mlx-tune has `SimPOTrainer`/`SimPOConfig` (reference-free) — [mlx-tune PyPI](https://pypi.org/project/mlx-tune/).
- mlx-lm-lora has no SimPO mode — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- SimPO uses a length-normalized implicit reward and a target margin, with no reference model — [SimPO, arXiv 2405.14734](https://arxiv.org/abs/2405.14734) (primary paper; not re-fetched in this session).

**IPO.**
- Available only as a loss type: `--dpo-cpo-loss-type ipo` in mlx-lm-lora — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- IPO replaces DPO's log-sigmoid with a squared loss to limit overfitting when preferences are near-deterministic — [IPO, arXiv 2310.12036](https://arxiv.org/abs/2310.12036) (primary paper; not re-fetched).

**ASTRAPOP (authorship style transfer).**
- Two stages: SFT, then PO with a reward of Toward (target-style similarity) + Away (1 − similarity to the source style) − a length penalty. The individual-author reward uses LUAR embeddings. Base model LLaMA-2-7B, LoRA r=16 on q_proj/v_proj — [ASTRAPOP, arXiv 2403.08043](https://arxiv.org/html/2403.08043v2).
- Individual-author task (Reddit, about 5 exemplars per author), Joint score: SFT 0.484, PPO 0.495, DPO 0.507, CPO 0.505.
- Community task, Joint score: SFT 0.659, PPO 0.665, DPO 0.767, CPO 0.827. DPO and CPO beat PPO on both tasks — [ASTRAPOP](https://arxiv.org/html/2403.08043v2).
- Harms:
  - PO lowered SBERT meaning preservation: individual task SFT 0.754 → DPO 0.733 / CPO 0.726.
  - In human evaluation, CPO's content preservation (1.018) was significantly below the STRAP (1.267) and STEER (1.279) baselines.
  - Without the length penalty, training "sometimes results in models that only generate empty or very short outputs" (reward hacking).
  - Low-resource individual transfer "is still much weaker" — [ASTRAPOP](https://arxiv.org/html/2403.08043v2).
- A follow-up, STAMP (multi-iteration preference optimization), reports improvements over STEER and ASTRAPOP — [arXiv 2406.11581](https://arxiv.org/pdf/2406.11581) (search snippet only; numbers not checked).

**SPIN (the model's own outputs as rejected, human text as chosen).**
- The policy is trained to prefer human SFT responses over its own previous-iteration generations, with no extra preference labels. On zephyr-7b-sft-full (Mistral-7B) the Open LLM Leaderboard average rose from 58.14 to 63.16 over iterations — [SPIN, arXiv 2401.01335](https://www.arxiv.org/pdf/2401.01335v3).
- This is the closest precedent for the plan of "chosen = author text, rejected = the model's own output".

**Gutenberg-DPO recipe.**
- chosen = an original Project Gutenberg chapter. rejected = an LLM-generated chapter (the `rejected_model` column includes, for example, bagel-7b-v0.1 and dolphin-2_2-yi-34b) — [jondurbin/gutenberg-dpo-v0.1](https://huggingface.co/datasets/jondurbin/gutenberg-dpo-v0.1/tree/main).
- The derivative gutenberg2-dpo describes the pipeline: summarize each chapter, build a prompt from the previous chapter's summary plus the current chapter, generate the rejected text from that prompt, and keep the original as chosen — [nbeerbower/gutenberg2-dpo](https://huggingface.co/datasets/nbeerbower/gutenberg2-dpo/blob/main/README.md).
- This is structurally the same as the planned "generic rewrite → author original" pairs, but paired and on the same content.

**Fine-tuning alone removes most slop.**
- Fine-tuning a model on each author's complete works reversed expert preference relative to prompting: MFA readers favored the fine-tuned AI for fidelity (OR=8.16) and quality (OR=1.87) — [Chakrabarty, Ginsburg & Dhillon, arXiv 2510.13939](https://arxiv.org/abs/2510.13939).
- Fine-tuned outputs were flagged by AI detectors 3% of the time, against 97% for prompted outputs.
- Mediation analysis attributes the gain to fine-tuning removing detectable stylistic quirks such as cliché density — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939).

#### B. Token-level negatives: FTPO, banlists, unlikelihood

**Antislop / FTPO.**
- Paper: Paech, Roush, Goldfeder, Shwartz-Ziv, arXiv 2510.15061 (v1 2025-10-16, v2 2025-10-21) — [arXiv](https://arxiv.org/abs/2510.15061). Presented at ICLR 2026 as a poster, per conference listings found by search; I did not see the OpenReview decision record itself — [search summary of listings](https://liner.com/review/antislop-a-comprehensive-framework-for-identifying-and-eliminating-repetitive-patterns).
- How it uses negatives: paired and token-level, inside the model's own inference trace. Each example is the prompt plus the response up to where a banned pattern began, one rejected token (the first token of the banned sequence), and a set of chosen coherent alternative tokens — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- Loss: a margin-gated softplus preference term on logit gaps (it switches off once chosen tokens lead the rejected token by margin m), plus MSE on target logits with a zero-penalty window τ, plus strong MSE anchoring of all non-target logits to the reference. The MSE is computed on logits, not a KL on probabilities, to avoid collateral pressure on unrelated tokens — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- Slop is defined relative to a human baseline: some patterns occur "over 1000× more frequently in LLM text than in human writing" — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- Results on gemma-3-12b at banlist sizes 2k/4k/8k (Table 2):

  | Method | Suppression | Writing-quality rubric | Lexical diversity (% of baseline) | Longform score |
  |---|---|---|---|---|
  | FTPO | 92.4 / 90.2 / 83.4% | 68.9 / 67.3 / 67.5 | 101 / 98 / 95 | 47.5 / 49.4 / 52.3 |
  | DPO (same pairs) | 82.0 / 80.6 / 81.4% | 63.0 / 58.2 / 54.6 | 91 / 82 / 74 | 36.6 / 34.8 / 26.9 |

  - FTPO keeps GSM8K and MMLU within 1-3% of baseline; DPO degrades both by 2-5% — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - The headline claim is "FTPO achieves 90% suppression with < 1% quality loss, while DPO achieves 80% suppression with 15% quality degradation" — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- Preference-accuracy ablation: FTPO trains to "nearly 100% preference accuracy with minimal degradation, while DPO only manages 40%" before substantial degradation. Raising DPO β to 1.0 reduces degradation but cuts suppression by 15.9% — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- Training recipe: freeze all layers except the last 5 and `lm_head`, LoRA r=256, 1 epoch, early stop at preference accuracy 0.85 — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061). The auto-antislop README says FTPO "works best with a high lora rank (128-256)" — [auto-antislop](https://github.com/sam-paech/auto-antislop).
- Caveats:
  - Llama-3.3-70B was "prone to repetition and degradation artifacts", and restricting LoRA to `lm_head` cut its suppression to 66% — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - All results are in creative writing. The authors "encourage future work to explore Antislop's performance in domains other than creative writing" — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - Listed harms include "unintended suppression of legitimate dialects, or minority styles". The authors recommend human review of banlists and a whitelist — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- MLX support:
  - mlx-lm-lora ships `--train-mode ftpo` ("FTPO / Antidoom") with flags `--lambda-mse-target`, `--tau-mse-target`, `--lambda-mse`, `--clip-epsilon-logits`. Data fields are `context_with_chat_template`, `rejected_decoded`, `multi_chosen_decoded`. The reference is a frozen copy of `--model` unless `--reference-model-path` is set — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
  - The trainer file `mlx_lm_lora/trainer/ftpo_trainer.py` has defaults lambda_mse_target=0.05, tau_mse_target=1.0, lambda_mse=0.4, clip_epsilon_logits=2.0 (the margin) — [ftpo_trainer.py](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora/blob/main/mlx_lm_lora/trainer/ftpo_trainer.py).
  - The reference pipeline (auto-antislop) needs an NVIDIA GPU with CUDA for vLLM and fine-tuning, using Unsloth or TRL, or else an external OpenAI-compatible endpoint. Modes are `ftpo`, `dpo`, `dpo_final_token` — [auto-antislop README](https://github.com/sam-paech/auto-antislop).
  - The pipeline profiles n-gram frequencies "against a human writing profile" to build the banlists. User-supplied `extra_ngrams_to_ban`, `extra_slop_phrases_to_ban` and `extra_regex_patterns` are merged in — [auto-antislop README](https://github.com/sam-paech/auto-antislop).

**Antislop sampler (backtracking, banned strings).**
- It triggers only after the whole banned string, n-gram or regex has appeared. It then backtracks to the first token, scales that token's probability by 10^(−10s), and resamples with min-p.
- The default is a soft ban: if the same token wins again, it is allowed through. s=0.4 suppressed 90% of uses in normal writing while fully allowing them when explicitly requested — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- It suppresses 8,000+ patterns while keeping quality, whereas token banning (logit bias −100) "becomes unusable at just 2,000". Token banning's rubric score falls to 28/100 at 8k, with severe repetition — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- Throughput drops 69% at a 1,000-item banlist and up to 96% at 8,000 (vLLM on one H100). The authors call these "worst-case values" and "overkill for most real-world usage" — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- The standalone sampler repo has an OpenAI-compatible server (transformers backend, no concurrency) and regex bans (no streaming with regex). It notes that KoboldCpp v1.76 includes antislop phrase banning, and that exllamav2 has a similar `banned_strings` feature — [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler).

**Unlikelihood training.**
- Token-level unlikelihood cut greedy 4-gram repetition from 0.442 to 0.283 (−36%). Sequence-level fine-tuning then cut it to 0.058. Perplexity was maintained, and humans preferred the output over nucleus sampling or beam blocking — [Welleck et al., arXiv 1908.04319](https://arxiv.org/pdf/1908.04319).
- This is the classic token-level "push down banned candidates" objective. It has no reference anchoring, unlike FTPO.
- Not in mlx-lm, mlx-lm-lora or mlx-tune as a named mode. I found no trainer for it in the repo listings — [mlx-lm-lora trainer dir](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora/tree/main/mlx_lm_lora/trainer). It would need custom code.

#### C. Unpaired negatives (binary labels)

**KTO.**
- Needs only a desirable/undesirable label per (x, y) — [KTO paper](https://arxiv.org/abs/2402.01306).
- It handled a 1:10 desirable:undesirable ratio: "up to 90% of the desirable data can in fact be discarded while still outperforming DPO" (Llama-7B) — [KTO paper](https://arxiv.org/abs/2402.01306).
- With one y per x (Mistral-7B, OpenAssistant), winrate vs. the SFT target was 0.631 for KTO against 0.600 for DPO, despite 72% less data — [KTO paper](https://arxiv.org/abs/2402.01306).
- Noise: as the implied reward goes to ±∞ the KTO update goes to zero, so very hard examples, possibly mislabeled ones, are "effectively ignored". The authors call this a "blessing in disguise" for noisy feedback, but it risks underfitting. Their guidance: if data has "sufficiently little noise and sufficiently little intransitivity, then DPO will work better" — [KTO paper](https://arxiv.org/abs/2402.01306).
- TRL guidance (KTOTrainer docs, v1.17.1): data format `{"prompt", "completion", "label"}`. Set `desirable_weight × n_pos : undesirable_weight × n_neg` within 1:1 to 4:3. Use per-step batch size ≥4 (the KL term is estimated from mismatched in-batch pairs; KL-estimating losses need batch >1 and sequential sampling). Use LR 5e-7 to 5e-6. "If using only rejected data, it is advisable to adopt a conservative learning rate." `loss_type="apo_zero_unpaired"` skips the KL estimate — [TRL KTO docs](https://huggingface.co/docs/trl/kto_trainer).
- mlx-lm-lora: no KTO mode in the README, and no `kto` trainer file in `mlx_lm_lora/trainer/`. The modes there are sft, dpo, cpo, dsla, orpo, ftpo, grpo, klpo, online_dpo, xpo, rlhf-reinforce, ppo — [README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora); [trainer dir](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora/tree/main/mlx_lm_lora/trainer).
- mlx-tune: `KTOTrainer`/`KTOConfig` exist and accept `{"prompt","completion","label"}` or `{"text","label"}`. But `kto_loss` in `mlx_tune/losses.py` computes −log σ(β·logratio) for positives and −log σ(−β·logratio) for negatives with no KL reference point (z0). Its internal weight is hard-coded to 1.0, and `KTOTrainer` calls `compute_kto_loss(model, input_ids, lengths, labels, self.beta)` without reference log-probs or the configured `desirable_weight`/`undesirable_weight` — [losses.py](https://github.com/ARahim3/mlx-tune/blob/main/mlx_tune/losses.py); [rl_trainers.py](https://github.com/ARahim3/mlx-tune/blob/main/mlx_tune/rl_trainers.py).

**BCO (Binary Classifier Optimization).**
- An alternative for thumbs-up/down data — [BCO, arXiv 2404.04656](https://arxiv.org/abs/2404.04656) (primary paper; not re-fetched).
- I found no MLX implementation in mlx-lm-lora or mlx-tune — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora); [mlx-tune PyPI](https://pypi.org/project/mlx-tune/).

**NPO (negative-only).**
- An alignment-style loss that uses only negative samples. Gradient ascent suffers "catastrophic collapse" because it diverges at a linear rate. NPO reduces to gradient ascent in the high-temperature limit but collapses "exponentially slower". On TOFU it was the first method to reasonably forget 50% or more of the data. Gradient-ascent outputs are "often gibberish" — [NPO, arXiv 2404.05868](https://arxiv.org/abs/2404.05868).
- Not available in the MLX trainers checked — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).

#### D. Robustness to label noise

- **rDPO** de-biases the DPO loss given a known flip rate ε. On IMDb with ε=0.4, rDPO kept a mean reward of 0.99, while cDPO/label smoothing reached 0.72 at 200 steps. It assumes random flips at a known fixed rate, and these are the authors' own results — [Chowdhury et al., arXiv 2403.00409](https://arxiv.org/pdf/2403.00409).
- **cDPO / label smoothing** is in mlx-tune as `DPOConfig(label_smoothing=...)` — [mlx-tune rl_trainers.py](https://github.com/ARahim3/mlx-tune/blob/main/mlx_tune/rl_trainers.py). `train.py` has no `label_smoothing` argument; its noise-relevant options are the `hinge`/`ipo`/`dpop` loss types — [mlx-lm-lora train.py](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora/blob/main/mlx_lm_lora/train.py).

#### E. Decoding-time contrast

**DExperts.**
- Combines base + expert − anti-expert logits at decoding time. GPT-2 Large base, with GPT-2 S/M/L experts fine-tuned on toxic and non-toxic Jigsaw data.
- Base GPT-2: average max toxicity 0.527, toxicity probability 0.520. The anti-expert-only ablation brought these to 0.352 and 0.191 — [DExperts, arXiv 2105.03023](https://arxiv.org/pdf/2105.03023); [secondary summary](https://liner.com/review/dexperts-decodingtime-controlled-text-generation-with-experts-and-antiexperts).
- The anti-expert-only variant loses some fluency and diversity. Fluency numbers conflict between sources (baseline PPL 25.45 vs. 32.4-32.5 quoted for DExperts variants, which would mean less fluent) — [ar5iv](https://ar5iv.arxiv.org/html/2105.03023); conflicting with the paper's "most fluent" framing — [arXiv](https://arxiv.org/pdf/2105.03023).

**Contrastive decoding.**
- Maximizes expert log-prob minus amateur log-prob (e.g., OPT-13B vs. OPT-125M), keeping only tokens with expert probability ≥ α × the expert's top probability (α=0.1). ACL 2023 — [Li et al., arXiv 2210.15097](https://arxiv.org/abs/2210.15097); [ACL Anthology](https://preview.aclanthology.org/setup/2023.acl-long.687).

**CFG with negative prompts.**
- Brings classifier-free guidance to LMs. Claimed SOTA on LAMBADA with LLaMA-7B. Adds negative prompting. In chatbot-style human evaluation, CFG outputs were preferred 75% of the time. Available in HF transformers (`guidance_scale`, `negative_prompt_ids`) and, per that summary, llama.cpp — [Sanchez et al., arXiv 2306.17806](https://export.arxiv.org/pdf/2306.17806); [EleutherAI](https://www.eleuther.ai/papers-blog/stay-on-topic-with-classifier-free-guidance).

**Weight-space negation (precedent for a "slop anti-expert LoRA").**
- Negating a task vector fine-tuned on toxic text cut toxic generations from 57% to 0.8% with perplexity barely changed. Gradient ascent reached 0.0% toxic, but its perplexity blew up — [Ilharco et al., arXiv 2212.04089](https://arxiv.org/pdf/2212.04089).
- For LoRA, negation is typically applied to the B factor ({A, −B}) — [survey, arXiv 2407.20516](https://arxiv.org/pdf/2407.20516).
- Plain negation also removes general knowledge. Ethos subtracts only the components specific to the unwanted behavior — [Ethos, arXiv 2403.08994](https://arxiv.org/html/2403.08994v2).

#### F. Representation steering

**StyleVector.**
- Contrasts last-token activations of (input + the user's own text) against (input + a style-agnostic response generated by gpt-3.5-turbo), takes the mean difference, and adds α·v at one middle-to-late layer (around layer 15+) at every generated position. Model: Llama-2-7B-chat — [StyleVector, arXiv 2503.05213](https://arxiv.org/html/2503.05213v1).
- ROUGE-L gains over the non-personalized base: +25.8% on Scholarly Title, +12.8% on Tweet Paraphrasing, +0.2% on Abstract Generation. Storage is 0.01 MB per user against 17 MB for SFT — [arXiv 2503.05213](https://arxiv.org/html/2503.05213v1).
- Too large an α "can cause abnormal activation values, thereby disrupting the generation process". A single vector may "conflate multiple stylistic dimensions" — [arXiv 2503.05213](https://arxiv.org/html/2503.05213v1).
- Note the design: the negative pole is generic LLM output on the same inputs (paired, on-domain), not unpaired slop.

**Style vectors (Konen et al.).**
- Adding style vectors (activation-based or training-based) to hidden layers shifts sentiment, emotion or writing style in a "parameterisable way". Findings of EACL 2024 — [ACL Anthology](https://aclanthology.org/2024.findings-eacl.52); [code](https://github.com/DLR-SC/style-vectors-for-steering-llms).

**Human evaluation of steering.**
- Over 7,000 ratings. Moderate strength (λ≈0.15) "reliably amplif[ies] target emotions while preserving comprehensibility". Effects were large for disgust and fear and minimal for surprise. LLaMA-3 steered more consistently than Alpaca — [arXiv 2601.21505](https://arxiv.org/abs/2601.21505).

**Style-specific neurons.**
- Deactivating source-style neurons improved transfer accuracy but hurt fluency, and the authors added contrastive decoding to recover it — [EMNLP 2024, arXiv 2410.00593](https://arxiv.org/html/2410.00593v1).

**CAA.**
- Contrastive Activation Addition uses the mean residual-stream difference between positive and negative examples of a behavior — [Panickssery/Rimsky et al., arXiv 2312.06681](https://arxiv.org/abs/2312.06681) (primary paper; not re-fetched).

#### G. Reward models and classifiers trained on negatives (rerank or gate)

**WQRM (AI-Slop to AI-Polish?, COLM 2025).**
- ModernBERT-Large with regression and pairwise heads, trained on the LAMP corpus of 1,282 AI drafts paired with expert edits (edited > original). 74.3% accuracy on the 4,729-judgment WQ benchmark, against O3 64.3%, Skywork-8B-v0.2 60.5% (despite 93% on RewardBench), and GPT-4o 5-shot 54.3% — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3).
- The Pangram AI detector scored 65.0% overall but is "near random on pairs that don't involve AI-vs-human distinctions". LLM judges tend to prefer AI-generated text — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3).
- Best-of-N: sample N=20 edits and select with WQRM. Nine professional writers' average ranks were best edit 1.58, random edit 2.09, first draft 2.26. Experts preferred the WQRM pick 66% of the time, and 72.2% when the reward gap was >1. Code: github.com/salesforce/creativity_eval — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3).

**Goodharting a detector.**
- DPO against a detector's "human" score for under a day on Llama-2-7B cut the OpenAI RoBERTa-Large detector's AUROC from 0.84 to 0.62/0.63, and the evasion transferred to other detectors — [Nicks et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1f9f07df0992ce21698d800eaa891bd8-Abstract-Conference.html).
- A follow-up found that DPO against FastDetectGPT drove that detector's AUROC to 0.18 while a style-based detector stayed at 0.95 — [Soto et al., arXiv 2505.14608](https://arxiv.org/html/2505.14608v1).

#### H. Evidence of harms from anti-slop or preference tuning (summary)

- **Quality and diversity loss.**
  - DPO on slop pairs: writing quality −6 to −15 points, lexical diversity down to 74-92% of baseline, longform score down to 26.9 from FTPO's ~50.
  - Token banning: quality collapses (28/100 at 8k) with heavy repetition — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - Post-training "tends to sharpen the output probability distribution and reduce the diversity" — [DivPO, arXiv 2501.18101](https://www.emergentmind.com/papers/2501.18101).
  - DDPO/DORPO reweight by deviation to restore diversity with a minimal drop in quality — [Chung et al., arXiv 2503.17126](https://arxiv.org/abs/2503.17126).
- **Meaning loss and reward hacking in style PO.** SBERT drops, empty or very short outputs without a length penalty, and lower human-rated content preservation — [ASTRAPOP](https://arxiv.org/html/2403.08043v2).
- **Over-suppression of legitimate style.** "Unintended suppression of legitimate dialects, or minority styles". The mitigations are a whitelist and human-reviewed banlists — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
- **Gradient-ascent-style negatives collapse the model** — [NPO, arXiv 2404.05868](https://arxiv.org/abs/2404.05868); [Ilharco et al.](https://arxiv.org/pdf/2212.04089).

### Inferences
- **Off-domain, unpaired slop as sequence-level negatives probably teaches the wrong contrast.** A rejected sequence differs from the author's text in topic, register, length and format as well as in "slop features". A sequence-level loss (DPO/KTO) can lower likelihood on any of those, including vocabulary of the target domain. FTPO avoids this because every rejected token sits inside your own model's on-domain context with on-domain alternatives. That is the main reason to route human slop through feature mining plus FTPO rather than KTO.
- **mlx-tune's `KTOTrainer` (as of main, Nov 2026) behaves like constant-weight likelihood/unlikelihood.** No KL reference point is passed, the configured weights are ignored, and with log_ref = stop_gradient(log_pi) the log-ratio is always zero. The gradient on negatives is then roughly a scaled gradient ascent (my reading of the code). Given the NPO and task-arithmetic evidence that unanchored push-down collapses models, I would not use it on noisy negatives without modification.
- **If you want true KTO on MLX**, the cleanest path is a custom trainer that reuses mlx-lm-lora's DPO machinery (frozen reference, LoRA): a per-example log-ratio, a batch-mismatched KL estimate (z0), λD/λU weights set by the 1:1-4:3 rule, LR ≤5e-6, β around 0.1. UNVERIFIED effort estimate: about 100-200 lines.
- **Expected marginal value of human slop over self-generated negatives: small for style.** Author-specific SFT already removes most detectable quirks (detection 3% vs. 97%). The harvested slop is most useful for (a) widening the banlist beyond what your own model emits, (b) training an AI-vs-human gate, and (c) eval. Its value as a training signal is lower.
- **A slop-vs-human classifier will behave like Pangram:** good at AI-vs-human, weak at ranking among N candidates that all come from your model. For best-of-N it should be one feature or a threshold gate next to style and meaning scores, not the main objective.
- **No precedent for a "slop anti-expert LoRA"** used DExperts-style for style or slop. The closest analogues are DExperts' anti-expert-only detox and task-vector negation for toxicity. These suggest it can suppress a broad register at some fluency cost, but they say nothing about author-style fidelity.

### Gaps
- I found no published result that trains with unpaired, off-domain human-labeled slop (as opposed to model-generated or edit-based pairs) and measures author-style fidelity.
- I could not verify Gutenberg-DPO's measured gains, such as EQ-Bench deltas for nbeerbower models, or look at "unslop/antislop" community fine-tune model cards (e.g., UnslopNemo). Not fetched.
- FTPO has only been evaluated on creative writing (Gemma-3-12B, Mistral-Small, Llama-3.3-70B), not on informational nonfiction or 7-9B models other than these, and I found no independent replication.
- KTO's noise robustness is shown theoretically and on public preference datasets, not on style or slop labels.
- Contrastive decoding's human-evaluation numbers and DExperts' exact fluency table were not confirmed (sources conflict).
- I did not verify that the published Antislop paper (ICLR 2026 camera-ready) matches arXiv v2.

---

## Key Question 2: What's the cheapest high-value use of negative signal: training, reranking, or decoding constraints?

### Takeaway
Use negative signal in this order:
1. **Measure.** Use the slop corpus to build a slop profile and score, as you already plan.
2. **Constrain decoding** with a small, author-whitelisted phrase and regex banlist using backtracking soft-bans, not token-level `logit_bias`.
3. **Rerank** best-of-N with a cheap classifier as one feature among style and meaning scores.
4. **Train it in** with FTPO, only after (1)-(3) show which patterns persist.

Sequence-level DPO on slop is the most expensive option and the one with the most documented harm.

### Cited Findings
- **Decoding constraints: phrase-level backtracking vs. token bias.**
  - The Antislop sampler reached 100% suppression while improving rubric quality above baseline. Token banning with logit bias −100 collapsed quality (28/100 at 8k patterns). A soft ban with s=0.4 kept 90% suppression while still allowing banned phrases when requested — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - Cost: 69% throughput loss at a 1k banlist and 96% at 8k on vLLM/H100, which the authors call "worst-case" stress tests — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - Per-token logit biasing is "quite ineffective since most slop words & phrases are more than one token, and it impairs output quality if we downregulate all those partial-word tokens" — [antislop-sampler README](https://github.com/sam-paech/antislop-sampler).
- **What mlx-lm offers natively.**
  - `make_logits_processors(logit_bias, repetition_penalty, presence_penalty, frequency_penalty, …)`; `make_sampler` with XTC options — [mlx-lm sample_utils.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/sample_utils.py).
  - The server accepts `logit_bias` (token-ID → bias), `repetition_penalty`, `presence_penalty`, `frequency_penalty`, `logprobs` (1-10 top tokens), per-request `adapters`, and `draft_model` — [mlx-lm SERVER.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md).
  - I found no built-in phrase or regex banning or backtracking in mlx-lm — [sample_utils.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/sample_utils.py).
- **Reranking.**
  - WQRM best-of-20 picks were preferred by experts 66% of the time (72.2% at reward gap >1). That reward model is a ModernBERT-Large trained on only about 1,000 edit pairs — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3).
  - Detectors are easy to optimize against when used as a training reward (AUROC 0.84 → 0.62/0.63 in under a day of DPO on 7B) — [Nicks et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1f9f07df0992ce21698d800eaa891bd8-Abstract-Conference.html).
  - The AI detector Pangram was "near random" on quality pairs that don't involve AI-vs-human — [arXiv 2504.07532](https://arxiv.org/html/2504.07532v3).
- **Training.**
  - FTPO bakes suppression in with under 1% quality loss on creative writing, while DPO on the same pairs costs 6-15 points of quality and up to 26% of lexical diversity — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).
  - FTPO data comes for free as a by-product of running the backtracking sampler: each backtrack event becomes one example — [auto-antislop README](https://github.com/sam-paech/auto-antislop).
  - Fine-tuning on an author's works alone cut AI-detector flag rates to 3% (from 97% for prompting) — [arXiv 2510.13939](https://arxiv.org/abs/2510.13939).

### Inferences
- **Cheapest: a phrase and regex banlist with soft backtracking at generation time.** It needs no training and works with any adapter. With a small curated banlist (tens to low hundreds of entries, whitelisted against the author corpus), throughput loss should be far below the 69-96% stress-test figures. UNVERIFIED: no published numbers for small banlists or on MLX.
- **Building it on MLX is custom code.** mlx-lm's `generate_step` exposes `logits_processors` and a prompt cache with `trim_prompt_cache`/`can_trim_prompt_cache` helpers in `generate.py`, which makes a backtracking loop feasible. It is not built in. Alternatively, KoboldCpp's phrase banning (Metal) or exllamav2-style `banned_strings` exist outside MLX. UNVERIFIED that KoboldCpp's implementation suits this workload.
- **Best-of-N is already in the plan, so a slop gate adds almost no cost.** The cost is N× generation, not the classifier (ModernBERT-scale inference is milliseconds on CPU or GPU). Use it to reject candidates above a slop threshold, not to maximize, so selection pressure on the classifier stays limited.
- **Train it in only when needed.** Once the banlist plus rerank shows a stable set of patterns your adapter still produces, FTPO on those backtrack events removes the runtime cost. This should come after, not instead of, the planned SFT plus optional ORPO/CPO on own-output negatives.
- **Never use `logit_bias` for multi-token slop phrases.** Limit it to single-token targets, such as an em-dash token if the author never uses one, and only after checking the author corpus.

### Gaps
- No published throughput numbers for backtracking samplers on Apple silicon or with small (<500) banlists.
- No study directly compares best-of-N with a slop classifier against FTPO for author-style tasks.
- I did not find a maintained MLX port of the antislop sampler, or confirm whether antislop-vllm's chunked OpenAI-endpoint mode works against `mlx_lm.server`. mlx_lm.server returns at most 10 top logprobs, which may limit the alternative-token set.

---

## Key Question 3: What can actually run on 24 GB with MLX at 7-9B, and at what time cost?

### Takeaway
Everything on the shortlist runs locally except true KTO, BCO, NPO, unlikelihood training, DExperts/CFG decoding and activation steering, which need custom MLX code.
- **Natively supported, with exact modes:**
  - SFT, DPO (sigmoid/hinge/ipo/dpop), CPO, ORPO and FTPO in mlx-lm-lora.
  - SFT, DPO (with label smoothing), ORPO, SimPO and a simplified KTO in mlx-tune.
- **Memory:** a 4-bit 8B base fits easily. DPO-family modes in mlx-lm-lora load a second full copy of the base as the reference.
- **Timing:** I found no published 7-9B timings on 24 GB Macs. Estimates below are labeled UNVERIFIED.

### Cited Findings
- **mlx-lm-lora (v5.10.2, 2026-10-26) modes and flags.**
  - Modes: `--train-mode` ∈ {`sft`, `dpo`, `cpo`, `dsla`, `orpo`, `ftpo`, `grpo` (incl. GSPO/Dr.GRPO/DAPO via flags), `klpo`, `online_dpo`, `xpo`, `rlhf-reinforce`, `ppo`}. There is a separate `python -m mlx_lm_lora.train_judge` to train a reward model from `prompt/chosen/rejected`.
  - QLoRA: `--load-in-4bits`, `--load-in-6bits`, `--load-in-8bits`.
  - Memory and training controls: `--grad-checkpoint`, `--num-layers`, `--max-seq-length`, `--gradient-accumulation-steps`, `--batch-size 1`. `--train-type` ∈ {`lora`, `dora`, `full`}; SFT `--mask-prompt`.
  - QAT is supported for SFT/DPO/ORPO/DSLA only — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora); [PyPI version](https://pypi.org/project/mlx-lm-lora/).
  - The README cites "version 0.1.0", which does not match PyPI 5.10.2 — [README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- **mlx-lm-lora reference model.** A second full model is loaded for reference-based modes (`load(args.model)` when `--reference-model-path` is unset) — [train.py](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora/blob/main/mlx_lm_lora/train.py). For FTPO the reference is "a frozen copy of `--model`" — [README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora).
- **mlx-tune (v0.6.0, 2026-06-23).**
  - Native MLX `SFTTrainer`, `DPOTrainer`, `ORPOTrainer`, `GRPOTrainer`, `KTOTrainer`, `SimPOTrainer`, plus `CPTTrainer`, embedding and VLM trainers.
  - Classifier "3 - Alpha". RL training is single-sample. The stated requirement is 8 GB+ RAM (16 GB+ recommended) — [mlx-tune PyPI](https://pypi.org/project/mlx-tune/).
  - Its DPO precomputes reference log-probs from the base once ("one-time"), so no second model is needed during training — [rl_trainers.py](https://github.com/ARahim3/mlx-tune/blob/main/mlx_tune/rl_trainers.py).
- **mlx-tune benchmarks (M4 Pro 48 GB, sub-1B models only, "rough indicators, not benchmarks").**
  - DPO, Qwen3.5-0.8B 4-bit, seq 512: about 540 ms/sample at ~1 GB peak.
  - ORPO, same model: about 430 ms/sample.
  - ORPO, Qwen3-0.6B bf16, seq 2048: ~0.41 it/s at 16.8 GB peak.
  - No 7B/8B numbers — [mlx-tune performance page](https://arahim.dev/mlx-tune/performance.html).
- **Inference-side options in mlx-lm (v0.32.2).**
  - `mlx_lm.server` takes a per-request `adapters` path. The server keys the loaded model by (model_path, adapter_path, draft_model_path) and calls `_load` for a new key, so switching adapters per request reloads rather than serving two adapters at once — [server.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/server.py); [SERVER.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md).
  - Speculative decoding through `--draft-model` — [generate.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/generate.py).
- **llama.cpp multi-LoRA (alternative inference path on Metal).**
  - `--lora` (comma-separated, multiple), `--lora-scaled FNAME:SCALE`, `--lora-init-without-apply`, `POST /lora-adapters`.
  - A per-request `lora: [{"id":0,"scale":0.5}, …]`. "Requests with different LoRA configurations will not be batched together" — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md).
  - This is weight-space mixing (a sum of scaled adapters), not DExperts logit arithmetic.
- **FTPO trains only the last layers and `lm_head`.** The paper froze all but the last 5 layers and `lm_head` (LoRA r=256), and trains on final-token pairs only — [arXiv 2510.15061](https://arxiv.org/abs/2510.15061).

### Inferences (all UNVERIFIED estimates, labeled as such)
- **Memory at 8B 4-bit.**
  - Weights are about 4.5-5 GB. A DPO/CPO/FTPO run in mlx-lm-lora holds about 9-10 GB of weights (policy plus reference) before activations. With `--grad-checkpoint`, `--batch-size 1` and `--max-seq-length` around 1024-2048, a 24 GB M4 Pro should fit.
  - macOS caps GPU-wired memory below total RAM (commonly about 65-75% by default), so leave headroom or raise `iogpu.wired_limit_mb` (UNVERIFIED default).
  - mlx-tune's precomputed-reference DPO avoids the second copy.
  - ORPO and SimPO need no reference and are the lightest preference options.
  - FTPO only needs final-position logits. The reference logits could be precomputed, though whether mlx-lm-lora does this was not verified.
- **Relative step cost vs. SFT on the same token count.**
  - ORPO/CPO/SimPO: about 2× (two sequences, one model).
  - DPO: about 2× policy passes plus 2 reference forward passes, so roughly 2.5-3×.
  - KTO: about 1× per example plus mismatched-pair KL forward passes.
  - FTPO: one forward pass over the context plus a cheap final-token loss, with backprop only into the last few layers if configured that way. Cheap per example, but you need many examples (thousands of backtrack events).
  - Rough absolute guess for an 8B 4-bit model on an M4 Pro: SFT at a few hundred tokens/s (UNVERIFIED). That puts a 1-2k-pair ORPO or DPO stage at 1k tokens per pair in hours, not days.
- **Decoding-time contrast costs.**
  - DExperts or contrastive decoding with two LoRAs on one base needs 2-3 forward passes per token, so roughly 2-3× decode latency and KV-cache memory. With one shared base kept in memory, weight memory grows only by the adapter size.
  - Neither mlx_lm.server (one adapter per loaded model) nor llama.cpp (summed adapters) does logit-space expert/anti-expert combination out of the box. It needs a custom generate loop in mlx-lm, with two adapter-wrapped views of one base or two model instances, at 2× weight memory if the base is not shared.
  - CFG with a negative prompt has the same 2× per-token cost.
- **Activation steering in MLX.** It means patching a decoder layer's `__call__` to add a vector to the hidden state, which is straightforward in mlx-lm's Python model definitions. I found no maintained MLX steering library (see Gaps). Inference cost is negligible, and computing the vector needs only forward passes over author vs. generic texts.
- **Feasibility ranking for this project.**

  | Status | Methods |
  |---|---|
  | Native and cheap | SFT; ORPO/CPO on own-output negatives; FTPO; best-of-N with a separate ModernBERT/DeBERTa classifier (train it in PyTorch on MPS or CPU, outside MLX) |
  | Native but heavier | DPO (two weight copies in mlx-lm-lora) |
  | Custom code | True KTO, BCO, NPO, unlikelihood, DExperts/CFG decoding, steering vectors, backtracking banlist sampler in mlx-lm |

### Gaps
- No published wall-clock or peak-memory measurements for DPO, ORPO or FTPO at 7-9B on a 24 GB Apple silicon machine. The only MLX preference-training benchmarks found are for 0.6-0.8B models on a 48 GB M4 Pro.
- Not verified:
  - whether mlx-lm-lora's FTPO precomputes reference logits or keeps the second model resident;
  - whether llama.cpp accepts negative LoRA scales (weight-space negation);
  - whether llama.cpp still ships CFG negative-prompt support in current builds (one 2023-24 summary says it was added; current status unchecked).
- I found no MLX-native activation-steering or representation-engineering tool, and no MLX implementation of DExperts or contrastive decoding.
- The `dsla` mode in mlx-lm-lora (latent-alignment variants of DPO/ORPO/CPO) was not investigated.
