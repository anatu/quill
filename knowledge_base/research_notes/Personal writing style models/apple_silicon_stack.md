# Local fine-tuning and serving on Apple silicon (M4 Pro, 24 GB): training a personal style adapter and serving it as a tool (as of Nov 7, 2026)

Scope note: every source here was fetched or searched on 2026-11-07. Many figures come from community blogs, not controlled benchmarks. Each item says whether it is **measured**, **self-reported**, or an **estimate**. GitHub release pages often omit the year, so years are inferred where noted. Reference hardware: the M4 Pro has 273 GB/s memory bandwidth in both the 16-core and 20-core GPU configurations ([llama.cpp Apple silicon benchmark](https://github.com/ggml-org/llama.cpp/discussions/4167)).

## Q1. MLX / mlx-lm: version, fine-tune types, config, data formats, fusing/GGUF, preference optimization

### Takeaway
mlx-lm (latest v0.32.2, Oct 16 [2026]) is still the default tool for training on a Mac. It does LoRA, DoRA and full fine-tuning, and it switches to QLoRA automatically when the base model is quantized. It reads text, chat, completions and tool-call JSONL, and it has `--mask-prompt`, gradient checkpointing and adapter fusing. Its built-in GGUF export only handles Llama, Mistral and Mixtral models in fp16. Preference optimization (DPO, ORPO and others) is not in mlx-lm itself; it comes from community packages. **mlx-lm-lora** is the most complete of these, and **mlx-tune** is the alternative with an Unsloth-style API.

### Cited Findings
**Version and release cadence**
- The latest release is **v0.32.2 (16 Oct)**, after v0.32.1 and v0.32.0 (15 Oct), v0.31.3 (22 Apr), v0.31.2 (07 Apr, added Gemma 4 support and its tool parser), v0.31.0 (07 Mar, Qwen 3.5 tensor parallelism), v0.30.7 (12 Feb, GLM5, Qwen 3.5 without vision) and v0.30.6 (04 Feb, Transformers v5 support). Training changes in these notes are minor: v0.30.7 made the validation set optional and v0.31.2 fixed trainer memory clearing. None of these releases mention GGUF. — [mlx-lm releases](https://github.com/ml-explore/mlx-lm/releases)
- Install for training with `pip install "mlx-lm[train]"`. The entry point is `mlx_lm.lora`. — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

**Fine-tune types**
- `--fine-tune-type` takes `lora` (the default), `dora` or `full`. QLoRA needs no flag: "If `--model` points to a quantized model, then the training will use QLoRA, otherwise it will use regular LoRA." You make a quantized model with `mlx_lm.convert -q`. — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- The model-family list in LORA.md is stale: Mistral, Llama, Phi2, Mixtral, Qwen2, Gemma, OLMo, MiniCPM, InternLM2. The release notes show newer architectures such as Gemma 4 and Qwen 3.5 being added for inference. — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md); [releases](https://github.com/ml-explore/mlx-lm/releases)

**Config defaults** (verbatim from `CONFIG_DEFAULTS` in `mlx_lm/lora.py`)
- `fine_tune_type: lora`, `optimizer: adam` (choices adam, adamw, muon, sgd, adafactor), `num_layers: 16` (`-1` means all layers), `batch_size: 4`, `iters: 1000`, `val_batches: 25`, `learning_rate: 1e-5`, `steps_per_report: 10`, `steps_per_eval: 200`, `save_every: 100`, `max_seq_length: 2048`, `grad_checkpoint: False`, `grad_accumulation_steps: 1`, `clear_cache_threshold: 0`, `lr_schedule: None`, `lora_parameters: {rank: 8, dropout: 0.0, scale: 20.0}`, `mask_prompt: False`, `report_to: None` (wandb and/or swanlab), `seed: 0`. — [mlx_lm/lora.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/lora.py)
- CLI flags include `--fine-tune-type`, `--optimizer`, `--mask-prompt`, `--num-layers`, `--batch-size`, `--iters`, `--learning-rate`, `--grad-accumulation-steps`, `--resume-adapter-file`, `--adapter-path`, `--save-every`, `--test`, `--max-seq-length`, `-c/--config` (YAML), `--grad-checkpoint`, `--clear-cache-threshold`, `--report-to` and `--trust-remote-code`. Rank, scale and dropout have no CLI flag; set them under `lora_parameters` in the YAML config. — [mlx_lm/lora.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/lora.py)

**Memory-saving advice in the docs**
- Use QLoRA. Lower batch size from 4 to 2 or 1 and keep the effective batch with `--grad-accumulation-steps`. Lower `--num-layers` from 16 to 8 or 4. Split long examples. Use `--grad-checkpoint`. The one hardware figure in the docs: Mistral-7B-v0.1 at `--batch-size 1 --num-layers 4` on a 32 GB M1 Max runs "about 250 tokens-per-second". — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

**Data formats**
- Put `train.jsonl` (required), `valid.jsonl` (optional) and `test.jsonl` in the `--data` directory, one example per line. The format is detected automatically:
  - **text:** `{"text": ...}`
  - **chat:** `{"messages": [{role, content}, ...]}`
  - **completions:** `{"prompt": ..., "completion": ...}`, with custom key names allowed via `prompt_feature` and `completion_feature`
  - **tools:** `messages` with assistant `tool_calls` plus a top-level `tools` schema list
- Hugging Face datasets work through an `hf_dataset` YAML block. Chat templates are applied by default. — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- `--mask-prompt` only works with **chat** and **completions** datasets. For chat data, the last message is treated as the completion. — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

**Evaluation, generation and fusing**
- Test perplexity with `mlx_lm.lora --test`. Generate with an unfused adapter via `mlx_lm.generate --adapter-path`. — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)
- `mlx_lm.fuse` flags are `--model`, `--save-path` (default `fused_model`), `--adapter-path`, `--upload-repo`, `--dequantize`, `--export-gguf`, `--gguf-path` (default `ggml-model-f16.gguf`) and `--trust-remote-code`. — [mlx_lm/fuse.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/fuse.py)
- GGUF export only allows `model_type` values `llama`, `mixtral` and `mistral`. Anything else raises `ValueError("Model type {model_type} not supported for GGUF conversion.")`. Export does not dequantize unless you also pass `--dequantize`. — [mlx_lm/fuse.py](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/fuse.py); [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md) ("limited to Mistral, Mixtral, and Llama style models in fp16 precision")
- mlx-tune confirms that GGUF export "doesn't work directly from a 4-bit base model (mlx-lm limitation)". Its suggested workarounds are a non-quantized base or dequantizing at export. It also warns that merging an adapter into a 4-bit model "can erase small LoRA updates", so its default merge is 16-bit. — [mlx-tune](https://github.com/ARahim3/mlx-tune)
- A Hugging Face forum thread reports that a Gemma 4 E4B adapter worked when loaded unfused but the fused checkpoint failed. It also cites an mlx_vlm server issue (#907) where `--adapter-path` dropped the adapter from the cache. — [HF forum](https://discuss.huggingface.co/t/gemma4-e4b-adaptors-fuse-after-training-how/176429)

**Preference optimization (community packages)**
- **mlx-lm-lora** (Goekdeniz-Guelmez, Apache-2.0, `pip install -U mlx-lm-lora`, entry point `mlx_lm_lora.train --train-mode <mode>`):
  - Methods: SFT; DPO, CPO, ORPO, DSLA, FTPO (repairs repetition loops); GRPO, GSPO, Dr. GRPO, DAPO, KLPO; Online DPO, XPO, RLHF Reinforce, PPO.
  - Training types: LoRA, DoRA and full. Quantized (QLoRA) training at 4, 6 and 8 bits. Quantization-aware training for SFT, DPO, ORPO and DSLA.
  - DPO data uses `prompt`, `chosen` and `rejected` (optional `system`). ORPO adds an optional `preference_score`.
  - Online DPO and XPO use a `--judge` model. `train_judge` trains a custom judge.
  - — [mlx-lm-lora GitHub](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora); [PyPI](https://pypi.org/project/mlx-lm-lora/)
- **mlx-tune** (formerly "unsloth-mlx", latest v0.6.0, community project, not affiliated with Unsloth or Apple): Unsloth-style API (`get_peft_model` with `r` and `lora_alpha`) covering SFT, DPO, ORPO, GRPO, KTO and SimPO, plus continual pretraining (CPT), vision, audio and embeddings. Exports adapters, merged models and GGUF (with the 4-bit caveat above) and pushes to the Hub. Requires macOS 13+ and Python 3.9+; 8 GB RAM minimum, 16 GB+ recommended. RL training is single-sample only. — [mlx-tune](https://github.com/ARahim3/mlx-tune)
- **mlxsmith** is an alpha wrapper around mlx-lm-lora that exposes DPO, ORPO and GRPO. — [PyPI mlxsmith](https://pypi.org/project/mlxsmith/0.1.3/)
- **mlx-optiq** fine-tuning adds fused cut-cross-entropy, which turns on automatically above `max_seq_length=4096`, and an opt-in `--fused-dpo` so long-context SFT and DPO fit in 24 GB (numbers in Q2). — [mlx-optiq docs](https://mlx-optiq.com/docs/finetune)

### Inferences
- For a style adapter, mlx-lm alone is enough for SFT. Add mlx-lm-lora only if a second preference stage is planned, for example DPO with "my real text" as chosen and "generic model output" as rejected. Its DPO/ORPO data format and its QLoRA support suit 24 GB.
- Training data is plain JSONL, so the same corpus can be used as `text` (continued-pretraining style, no masking) or as `completions` or `chat` with `--mask-prompt` (instruction-conditioned "write X in my voice").
- The defaults (rank 8, scale 20, 16 layers, lr 1e-5, 1000 iters, seq 2048) are a reasonable first run. For stylistic depth, common next steps are `num_layers: -1` and rank 16–32. That is extrapolated from general LoRA practice, not from an mlx-specific style benchmark.
- The planned base models (Qwen, Gemma) are not llama/mistral types, so plan on this GGUF path: `mlx_lm.fuse --dequantize`, then llama.cpp `convert_hf_to_gguf.py`, then `llama-quantize`. I did not verify the llama.cpp conversion scripts in this session.

### Gaps
- I could not find the exact year on the GitHub release dates. v0.32.x is assumed to be October 2026, because Gemma 4 (released March 31, 2026) is supported from v0.31.2 (April).
- The example YAML (`lora_config.yaml`) returned 404 at the path I tried, so I could not confirm the `lora_parameters.keys` option (which modules get LoRA) from the source.
- I found no official statement on whether mlx-lm LoRA supports Qwen 3.5's hybrid Gated DeltaNet layers end to end. One user had to strip vision weights first (see Q4).

## Q2. Memory usage and throughput for LoRA training at 3B–14B on M-series Macs; what is realistic on 24 GB

### Takeaway
On a 24 GB M4 Pro, realistic training is **QLoRA (4-bit base) on 3B–9B models with sequences of 2k–4k tokens**, and QLoRA on 12–14B models is possible with short-to-moderate sequences. bf16 LoRA is comfortable up to about 4B and tight at 7–8B. Peak memory depends more on sequence length than on parameter count: a 4-bit 4B model reaches about 7.7 GB at 2k context, 11.4 GB at 4k and 19.9 GB at 8k. Expect roughly 100–400 training tokens/s depending on model size, which means tens of minutes to a few hours for a typical style dataset.

### Cited Findings
**Measured or self-reported numbers on Apple silicon**
- **M4 Pro 24 GB** (self-reported by the mlx-lm-lora author: all LoRA layers, batch 1, max context 4096, 100 steps):
  - Qwen3-8B 4-bit SFT: ~4.1 it/s, ~6–10 GB peak.
  - Qwen3-0.6B bf16: SFT ~4.7 it/s at ~2 GB; ORPO ~4.5 it/s at ~2–4 GB; GRPO ~0.02 it/s at ~9–20 GB.
  - mlx-tune on the same setup: Qwen3-8B SFT ~0.07 it/s at ~8–18 GB, and out of memory on ORPO and GRPO.
  - The tables give no tokens/s. The 4.1 it/s figure implies short sequences in practice.
  - — [mlx-lm-lora README](https://github.com/Goekdeniz-Guelmez/mlx-lm-lora)
- **Qwen3.5-4B 4-bit OptiQ by context length** (self-reported by mlx-optiq: M3 Max 36 GB, batch 1, all layers, `--grad-checkpoint`). On a **24 GB M4**, 8k context peaks at about 14.7 GB with fused cut-cross-entropy; the plain path runs out of memory. Without `--fused-dpo`, DPO on 24 GB runs out of memory at about 4k. — [mlx-optiq docs](https://mlx-optiq.com/docs/finetune)

  | Context | SFT step time | SFT peak | DPO step time (`--fused-dpo`) | DPO peak |
  |---|---|---|---|---|
  | 2k | 2.8 s | 7.7 GB | 29 s | 8.7 GB |
  | 4k | 6.7 s | 11.4 GB | 144 s | 10.9 GB |
  | 8k | 45 s | 19.9 GB | 216 s | 17.3 GB |

- **Measured on an M1 with 64 GB** (rank 8, 16 layers, lr 1e-5, 600 iters, short text-to-SQL samples, gradient checkpointing on). The author hit 97% RAM with batch 2 on the 2B model. — [sciences44/mlx-lora-finetune](https://github.com/sciences44/mlx-lora-finetune)

  | Model (4-bit) | Peak memory | Training speed | Time | Trainable params |
  |---|---|---|---|---|
  | Qwen3.5-0.8B | 3.9 GB | ~475 tok/s | ~15 min | — |
  | Qwen3.5-2B | 5.9 GB | ~180 tok/s | ~8 min | — |
  | Qwen3.5-4B | 11.1 GB | ~115 tok/s | ~12 min | 13.6M (0.32%) |
  | Mistral-Nemo-12B | 8.2 GB | ~210 tok/s | ~8 min | 18.0M (0.15%) |

- **Gemma 4 E4B** LoRA via `mlx_vlm.lora` on an M4 Max 128 GB: peak 7.876 GB, ~190 tok/s training. — [HF model card](https://huggingface.co/deadbydawn101/gemma-4-E4B-mlx-4bit)
- **Qwen2.5-3B 4-bit smoke test:** ~16 s run, ~2.5 GB peak. — [DEV Community](https://dev.to/rainytechlab/fine-tune-an-llm-on-your-mac-with-mlx-qlora-in-16-seconds-real-run-no-cloud-39ni)
- **Mistral-7B LoRA, M1 Max 32 GB**, batch 1, 4 layers: ~250 tok/s (official docs). — [LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md)

**Estimates and guides** (not measured)
- One guide (updated Nov 4, 2026) says a **24 GB Mac** can do LoRA at 7B–8B and QLoRA at 8B–14B, rated "Comfortable":
  - Per-model memory: Llama 3.1 8B ~14 GB LoRA / ~7 GB QLoRA; Qwen 2.5 14B ~24 GB LoRA / ~12 GB QLoRA. The article also gives 14–18 GB for 14B LoRA, so it contradicts itself.
  - 8B LoRA throughput: M2 Pro 16 GB ~200, M1 Max ~250, M3 Max ~320, M4 Max ~380 tok/s.
  - Gradient checkpointing adds about 30% to training time.
  - 200–500 examples at 300–600 iterations takes about 15–45 minutes.
  - The article names no test machine and marks memory figures with "~".
  - — [InsiderLLM guide](https://insiderllm.com/guides/fine-tuning-mac-lora-mlx/)
- Another guide (Apr 20, 2026) says macOS reserves about 3.5 GB, leaving about 20.5 GB usable on a 24 GB Mac. It calls the M4 Pro 24 GB "marginal" for fine-tuning larger Qwen 3.5 models and advises 4-bit or 8-bit bases. It reports ~2 h for 600 iterations of a 9B LoRA on an M4 Max 64 GB, and says a full fine-tune of the 9B needs 40+ GB. — [willitrunai Qwen 3.5 guide](https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide)
- Unsloth's generic GPU minimums: 7B is 5 GB with QLoRA and 19 GB with LoRA. These are GPU VRAM figures, not unified memory. — [Unsloth requirements](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements)

### Inferences
- **What fits on 24 GB:**

  | Model | Approach | Fit | Notes |
  |---|---|---|---|
  | 3–4B | bf16 LoRA | Fits | ~8 GB of weights plus activations |
  | 3–4B | QLoRA | Easy | Up to ~8k context with fused CE (mlx-optiq) |
  | 7–9B | QLoRA | Best balance | ~5–6 GB of weights; the 6–10 GB peak at 4k context is self-reported on an M4 Pro 24 GB |
  | 7–9B | bf16 LoRA | Tight / risky | ~16–18 GB of weights alone |
  | 12–14B | QLoRA | Feasible | ~7–8 GB of weights; batch 1, grad checkpointing, ≤2k–4k context |
  | 12–14B | bf16 LoRA | Does not fit | — |
  | Any size | Full fine-tune | Only below ~1–2B | — |

- **Throughput on the M4 Pro (rough inference):** about 100–200 tok/s training for QLoRA at 8–14B and about 200–400 tok/s at 3–4B. These are bracketed by the M1 Max, M2 Pro and M3 Max figures above.
- **Time for a typical style dataset:** a corpus of about 1M tokens (for example 1,000 passages of 1k tokens) would take roughly 1–3 hours per epoch at 8B QLoRA, and less at 4B.
- **Sequence length drives memory.** For prose style, chunking essays into 1–2k-token windows is the biggest memory lever.

### Gaps
- I found no independent measured mlx_lm.lora tokens/s plus peak-memory run on an M4 Pro 24 GB for Qwen3/3.5 4B–9B, Gemma 3/4 or Llama 3.x 8B with long prose sequences. The only M4 Pro 24 GB figures are self-reported it/s from mlx-lm-lora.
- I found no measurement of how often macOS memory pressure or swapping hurts 12–14B QLoRA on 24 GB.
- I did not verify the macOS GPU wired-memory limit (raised via `sysctl iogpu.wired_limit_mb`) or its default on 24 GB machines in this session. It is often cited as a way to get more headroom.

## Q3. Alternatives: PyTorch MPS + PEFT/TRL, Unsloth on Mac, Axolotl/LLaMA-Factory, Apple's Foundation Models adapter toolkit

### Takeaway
- **PyTorch MPS + PEFT/TRL** works and can be faster than MLX on raw throughput at small sizes. It has no practical 4-bit QLoRA, needs fp16/fp32 instead of bf16, and cannot load a 3B model in fp16 on 16 GB, so it is a poor fit for 7B+ on 24 GB.
- **Unsloth:** Unsloth Studio (the GUI) now claims Mac training via MLX. The core Python library still says Apple/MLX support is "in the works", and DPO/GRPO on Mac is reportedly not covered.
- **Apple's Foundation Models adapter toolkit** does not fit this project. It needs a 32 GB or larger Mac, its final release is 26.0.0 and it is not compatible with OS 27, and it targets Apple's own ~3B system model.

### Cited Findings
**PyTorch MPS with PEFT/TRL**
- A Hugging Face blog compared PyTorch MPS and MLX for Qwen 2.5 (0.5B–3B) LoRA SFT on a 16 GB Mac over 10 controlled runs:
  - MPS had 2.2x–5.7x higher raw throughput.
  - MPS could not load a 3B model in FP16 on 16 GB; MLX 4-bit QLoRA fit.
  - Dequantization explains only about 1.07x–1.4x of the gap, leaving a ~4.1–4.6x framework-level gap.
  - Eval loss tracked closely across the two backends.
  - — [HF blog, harshitkgupta](https://huggingface.co/blog/harshitkgupta/fine-tuning-coding-agents-on-mac-pytorch-mps-mlx). I saw this only through a search summary, not the full page.
- A Mac-focused post reports:
  - Apple still labels MPS "beta".
  - PyTorch documents AdamW on MPS for float32 and float16 only, and an open PyTorch issue reports BFloat16 unsupported on some MPS setups.
  - TRL turns `bf16` on when `fp16` isn't set, which the author calls a trap on MPS.
  - TRL enables gradient checkpointing by default, which the author says can misbehave (citing a Gemma 4 issue).
  - The post recommends fp16 for training and fp32 for smoke tests.
  - — [longform.social post](https://longform.social/post/did:plc:pgryn3ephfd2xgft23qokfzt/3mjg7wgy5dc22/source)
- An older Mac playbook warns that fp16 backward passes on MPS can produce NaN gradients and recommends fp32, which roughly doubles memory. This may be outdated. — [mac-playbooks: PyTorch MPS](https://svah-x.github.io/mac-playbooks/playbooks/pytorch-mps)

**Unsloth**
- The requirements page says Unsloth Studio on macOS has "full support for training, MLX and GGUF inference". It needs Python 3.11 up to (not including) 3.14, and training needs 3.11–3.13. For Unsloth Core (the code library), Apple silicon/MLX support "is in the works". Export on CPU is "coming very soon". The page has no dates. — [Unsloth requirements](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements)
- A PR to the unslothai repo describes the MLX backend as "a first-class path". It says `unsloth train`, `chat`, `inference` and `export` detect MLX on Apple silicon. — [unsloth PR #14457](https://github.com/unslothai/unsloth/pull/14457)
- A comment on the long-running "Unsloth On Mac" issue says Apple silicon now takes the MLX path by default for SFT/LoRA, but "Intel Macs and GRPO or DPO are still not covered". This is a secondary comment. — [unsloth issue #685](https://github.com/unslothai/unsloth/issues/685)
- mlx-tune is a separate community project with an Unsloth-like API, not official Unsloth. — [mlx-tune](https://github.com/ARahim3/mlx-tune)

**Axolotl / LLaMA-Factory**
- A Medium write-up covers fine-tuning Mistral-7B with Axolotl LoRA on Apple silicon, which suggests it is possible through PyTorch MPS. I did not read its details. — [Medium: Axolotl on Apple Silicon](https://medium.com/@plawanrath/fine-tuning-mistral-7b-on-apple-silicon-a-mac-users-journey-with-axolotl-lora-c6ff53858e7d)

**Apple Foundation Models Adapter Training Toolkit**
- Requirements and status:
  - Needs a Mac with Apple silicon and **at least 32 GB memory** (or Linux GPUs), plus Python 3.11+.
  - Version history: Beta 0.1.0, Beta 0.2.0 (added a tool-calling schema), then **26.0.0, the final release**, which "is not compatible with macOS, iOS, iPadOS, or visionOS 27 and later".
  - — [Apple developer: FM adapter](https://developer.apple.com/apple-intelligence/foundation-models-adapter/)
- How it works:
  - LoRA training on JSONL `messages`. Apple suggests 100–1,000 samples for basic tasks and 5,000+ for complex ones.
  - Example command: `--epochs 5 --learning-rate 1e-3 --batch-size 4`.
  - Each adapter is about **160 MB** and is tied to a single system-model version, so it must be retrained for each OS model update.
  - Training and local testing need no entitlement; deployment needs `com.apple.developer.foundation-model-adapter`.
  - Toolkit weights may be used only to train adapters.
  - — [Apple developer: FM adapter](https://developer.apple.com/apple-intelligence/foundation-models-adapter/)
- A third-party reference says the toolkit's LoRA rank is fixed at 32. It also says the `SystemLanguageModel.Adapter` API is deprecated in 26.4 and obsoleted in 27.0, with no adapter replacement in the 27 SDK. — [Axiom FM adapters reference](https://charleswiltgen.github.io/Axiom/reference/foundation-models-adapters-ref)
- At WWDC26, Apple introduced **Core AI** for deploying your own on-device models, including a Torch conversion package. Core AI models can be swapped into a Foundation Models `LanguageModelSession`; Apple's demo used a Qwen model. Session 339 describes public `LanguageModel` and `LanguageModelExecutor` protocols covering Apple models, Core AI, MLX and custom packages. — [WWDC26 324 Meet Core AI](https://developer.apple.com/videos/play/wwdc2026/324/); [WWDC26 382](https://developer.apple.com/videos/play/wwdc2026/382/); [WWDC26 326](https://developer.apple.com/videos/play/wwdc2026/326/); [wwdc.ai 339](https://wwdc.ai/2026/339)
- A blog claims iOS 27 ships an on-device "Foundation Models Adapter Trainer" for per-user adapters. I could not confirm this on Apple's own pages. — [ninetwothree](https://www.ninetwothree.co/blog/wwdc-2026-on-device-ai) (unverified)

### Inferences
- With 24 GB, the user cannot run Apple's toolkit on this Mac (32 GB minimum). The toolkit is also a dead end after OS 27. Apple's newer route (Core AI plus the `LanguageModel` protocol) is about serving custom models inside Swift apps, not about training. It could matter later if the style model ever needs to run inside a native macOS app, but it is unnecessary for a Claude Code tool.
- PyTorch MPS only makes sense at 3–4B in fp16/fp32 when the HF/TRL ecosystem is specifically needed. For 7B+ on 24 GB, MLX QLoRA is the practical option.
- Unsloth Studio may be a convenient GUI. Its Mac coverage is new and only partly documented, so mlx-lm or mlx-lm-lora is the lower-risk choice.

### Gaps
- I found no current official confirmation that Axolotl or LLaMA-Factory support MPS in late 2026, and no throughput figures for them on M-series Macs.
- I could not confirm whether Unsloth Studio's Mac path supports DPO/ORPO, which architectures it covers, or whether it exports GGUF.
- I found no PyTorch 2.x release-note confirmation of current bf16 status on MPS.

## Q4. Best open-weight base models (2025–2026) for English prose style imitation that fit 24 GB; base vs instruct starting point

### Takeaway
As of November 2026, the strongest candidates that train on 24 GB are:
- **Qwen3.5 4B / 9B** (March 2026, Apache 2.0, base checkpoints released)
- **Gemma 4 E4B / 12B** (March and June 2026, reportedly Apache 2.0)
- **Ministral 3 8B / 14B** (base, instruct and reasoning variants, Apache 2.0)
- **OLMo 3 7B** (fully open, base available)

Older but well-supported fallbacks are Gemma 3 4B/12B, Qwen3 4B/8B/14B and Llama 3.1 8B. For **pure style continuation on raw prose**, a **base** checkpoint fits naturally. For a **callable "rewrite/draft in my voice" tool**, starting from an **instruct** checkpoint with chat/completion data and `--mask-prompt` usually keeps instruction-following better. No controlled head-to-head comparison exists for this question.

### Cited Findings
**Qwen3.5 small models**
- Released March 1–2, 2026: four dense models (0.8B, 2B, 4B, 9B) under Apache 2.0, "along with their Base versions". Artificial Analysis scores the 9B at 32 and the 4B at 27 on its Intelligence Index, the highest in their size classes. — [Artificial Analysis](https://artificialanalysis.ai/es/articles/qwen3-5-small-models); [NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/qwen-3-5-small-models-9b-parameters-that-beat-120b)
- Qwen3.5-4B architecture: 32 layers, repeating 3× Gated DeltaNet + 1× gated attention. The card says the control tokens were trained so LoRA works with the official chat template. — [Qwen3.5-4B-Base README (mirror)](https://huggingface.co/devshiva/Qwen3.5-4B-Base/blob/main/README.md)
- MLX practical issues:
  - Qwen3.5 is natively multimodal; the 4B needed its vision weights stripped manually, or MLX LoRA training crashed. — [sciences44](https://github.com/sciences44/mlx-lora-finetune)
  - Its thinking template caused chat-template errors, which the author avoided by using text format. — [sciences44](https://github.com/sciences44/mlx-lora-finetune)
  - Unsloth's guidance (cited on a forum) says Qwen3.5 shows larger-than-normal quantization differences, so higher-precision LoRA is preferred where feasible. — [HF forum, Qwen3.5-4B-Base on novels](https://discuss.huggingface.co/t/how-should-i-fine-tune-qwen3-5-4b-base-on-raw-novel-text-without-a-chat-qa-format/179431)
- Larger Qwen 3.5 models exist (27B dense, 35B-A3B MoE, 122B-A10B MoE). On a 24 GB M4 Pro, 27B and 35B-A3B 4-bit are "tight"/"marginal" even for inference (~17–20 GB). — [willitrunai](https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide)

**Gemma**
- Release history:

  | Date | Release |
  |---|---|
  | Mar 10, 2025 | Gemma 3 (1B, 4B, 12B, 27B) |
  | Jun 26, 2025 | Gemma 3n (E2B, E4B) |
  | Mar 31, 2026 | Gemma 4 (E2B, E4B, 31B, 26B A4B) |
  | Apr 16, 2026 | Gemma 4 MTP variants |
  | Jun 3, 2026 | Gemma 4 12B "Unified" |

  The page lists nothing for November 2026. — [Gemma releases](https://ai.google.dev/gemma/docs/releases)
- Secondary sources report that Gemma 4 moved to **Apache 2.0**, replacing Gemma's custom license. E4B has 128K context and 31B has 256K. Listed HF IDs are `-it` (instruct). — [emelia.io](https://emelia.io/hub/gemma-4-open-source-guide); [Notebookcheck](https://www.notebookcheck.net/Gemma-4-on-Hugging-Face-Google-s-Easter-surprise-for-download.1265198.0.html)
- Unsloth's Gemma 4 guide recommends bf16 LoRA for the 26B-A4B MoE when memory allows and says QLoRA on the MoE isn't recommended. — [Unsloth Gemma 4 guide](https://unsloth.ai/docs/models/gemma-4/train)
- Gemma 4 E4B LoRA runs in MLX via `mlx_vlm.lora` at ~7.9 GB peak. — [HF card](https://huggingface.co/deadbydawn101/gemma-4-E4B-mlx-4bit)
- mlx-lm added Gemma 4 in v0.31.2. — [mlx-lm releases](https://github.com/ml-explore/mlx-lm/releases)

**Ministral 3 and OLMo 3**
- **Ministral 3** (Mistral AI): dense 3B, 8B and 14B, each released as a pretrained base, an instruct and a reasoning model, all Apache 2.0. — [arXiv 2601.08584](https://arxiv.org/abs/2601.08584); [eWeek](https://www.eweek.com/news/mistral-3-launch/)
- **OLMo 3 7B** base (`allenai/Olmo-3-1025-7B`): 5.93T training tokens, 32 layers, 65,536 context, Apache 2.0, with fully open data, code and checkpoints. A 32B sibling exists. — [HF: Olmo-3-1025-7B](https://huggingface.co/allenai/Olmo-3-1025-7B)
- LM Studio 0.3.33 added Ministral 3 support and Olmo-3 tool calling. — [LM Studio 0.3.33](https://lmstudio.ai/blog/lmstudio-v0.3.33)

**Base vs instruct**
- A forum thread treats raw novel text on Qwen3.5-4B-Base as plain causal LM with no chat template needed, and notes the Base card positions it for fine-tuning. — [HF forum](https://discuss.huggingface.co/t/how-should-i-fine-tune-qwen3-5-4b-base-on-raw-novel-text-without-a-chat-qa-format/179431)
- In an informal documentation-style experiment, the base model "mostly autocompleted raw corpus text", while instruction-tuned Qwen fine-tunes kept the target register better. — [passo.uno](https://passo.uno/fine-tuning-docs-llm/)
- In the text-to-SQL comparison, the instruct-tuned Mistral-Nemo-12B often ignored the LoRA format (43% plain-number answers) because "its instruction tuning competes with the LoRA format push". The 2B model did best, and validation loss was a misleading guide to quality. — [sciences44](https://github.com/sciences44/mlx-lora-finetune)
- A 2026 creative-writing roundup names Gemma 4 31B as a prose pick for 24 GB GPUs. That is inference on a GPU, not Mac training. The same roundup contains an unverifiable "Qwen3.8-27B" mention, so it is low reliability. — [PromptQuorum](https://www.promptquorum.com/power-local-llm/best-local-llm-creative-writing)

### Inferences
- **Primary pick for 24 GB:** a 7–9B dense model in QLoRA, either Qwen3.5-9B (base or instruct) or Ministral 3 8B. Training cost is moderate and inference is about 30–40 tok/s.
- **Fast-iteration pick:** Qwen3.5-4B or Gemma 4 E4B. They can use bf16 LoRA, which avoids the Qwen3.5 quantization-sensitivity issue.
- **Stretch:** Gemma 4 12B or Ministral 3 14B in QLoRA with short sequences.
- **Avoid** the hybrid-architecture and multimodal quirks (Qwen3.5 vision weights, Gemma 4 through mlx_vlm) if a smooth GGUF/Ollama path matters. Ministral 3 and older Llama/Mistral architectures follow the best-trodden export paths.
- **Base vs instruct by use case:**
  - The tool will mostly be called as "rewrite this / draft this in my voice", so the most practical recipe is an **instruct** checkpoint with `completions`/`chat` data (prompt = brief or neutral version, completion = my text) and `--mask-prompt`.
  - A **base** checkpoint trained on `text` format is better for pure voice capture and continuation. It is weaker at following instructions unless a second instruction stage is added.
  - Either way, judge results with held-out human or LLM evaluation, not val loss.

### Gaps
- I found no rigorous benchmark of style imitation or prose quality across these small models after LoRA.
- I could not confirm that Gemma 4 E4B, 12B or 31B **base** (pretrained) checkpoints are published; only `-it` IDs surfaced. Also unconfirmed: the Gemma 4 12B "Unified" architecture and how well mlx-lm's text-only path trains it.
- I did not re-verify SmolLM3, Phi-4/Phi-4-mini, Llama 3.x 8B or Mistral Small this session. They remain viable but older options, and no new 2026 data was found.
- I found no models released in October–November 2026 beyond those listed. The mlx-lm v0.32 notes mention "Muse Spark" (NVFP4) but give no details.

## Q5. Serving: mlx-lm server, LM Studio, Ollama, llama.cpp; LoRA support; latency for ~500 tokens on M4 Pro

### Takeaway
- **Simplest, adapter-native option:** `mlx_lm.server`. It is OpenAI-compatible on localhost:8080 and takes a **per-request `adapters` path**, so there is no fuse step. Its docs warn it is not production-grade.
- **For GGUF:** llama.cpp `llama-server` has the most mature LoRA hot-loading (`--lora`, `--lora-init-without-apply`, `POST /lora-adapters`, per-request `lora` scales).
- **Ollama** (v0.40.15, Nov 3, 2026) uses MLX on Apple silicon in some configurations. Its Modelfile `ADAPTER` is documented only for Llama, Mistral and Gemma 1/2 safetensors adapters, so importing a **fused** model is the reliable path.
- **LM Studio:** I found no official LoRA-adapter documentation; load a fused model.
- **Latency for 500 tokens on an M4 Pro:** roughly 7 s (4B 4-bit), 10–16 s (7–9B 4-bit) and 18–20 s (12–14B 4-bit), plus about 1 s of prefill for a short prompt.

### Cited Findings
**mlx-lm server**
- Start with `mlx_lm.server --model <path|hf_repo>` (default localhost:8080). Endpoints are `/v1/chat/completions` and `/v1/models`. Per-request options include `adapters` (a path relative to the server's start directory), `model` and `draft_model` for speculative decoding (`num_draft_tokens` defaults to 3). It supports streaming and KV-cache quantization (`--kv-bits`). It is "not recommended for production" because it only has basic security checks. — [SERVER.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md)
- Recent server changes: OpenAI-compatible `finish_reason` (v0.30.5); `chat_template_kwargs` and `top_logprobs` (v0.30.6); prompt-cache improvements (v0.31.0); `--allowed-origins` and a parallel tool-call fix (v0.31.2). — [mlx-lm releases](https://github.com/ml-explore/mlx-lm/releases)

**llama.cpp server**
- `--lora FNAME` (comma-separated for several adapters), `--lora-scaled FNAME:SCALE`, and `--lora-init-without-apply` (load at scale 0 and apply later). `GET /lora-adapters` lists adapters (id, path, scale). `POST /lora-adapters` takes `[{"id": 1, "scale": 0.5}]` to set global scales. A per-request `lora` field on `/completion` overrides the global scales.
- Caveat: "requests with different LoRA configurations will not be batched together". The README does not say whether `/v1/chat/completions` accepts the `lora` field.
- — [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- An older issue reported that hot-swapping was tied to a global scale, which blocked per-request switching. The per-request field above appears to address this. — [llama.cpp issue #10374](https://github.com/ggml-org/llama.cpp/issues/10374)

**Ollama**
- Ollama's March 30, 2026 blog announced Ollama 0.19 "powered by MLX on Apple Silicon in preview".
  - On Qwen3.5-35B-A3B NVFP4: prefill 1810 tok/s and decode 112 tok/s, versus 1154 and 58 on 0.18 (Apple hardware not specified in the summary).
  - It says "make sure you have a Mac with more than 32GB of unified memory".
  - It promises "an easier way to import" fine-tuned models.
  - — [Ollama blog: MLX](https://ollama.com/blog/mlx)
- The latest release is **v0.40.15 (Nov 3 [2026])**. Recent notes mention MLX updates and speedups: faster prompt processing on Apple silicon for Gemma 4, DFlash2 speculative decoding on MLX, and faster top-k sampling on MLX. They say nothing about adapters. — [Ollama releases](https://github.com/ollama/ollama/releases)
- Modelfile `ADAPTER` docs:
  - Safetensors adapters are supported for Llama (2/3/3.1), Mistral (1/2, Mixtral) and Gemma (1/2).
  - GGUF adapters use `ADAPTER /path/to/adapter.gguf`.
  - The `FROM` base must match the adapter's base, and non-QLoRA adapters are recommended because frameworks quantize differently.
  - The import page covers `FROM` safetensors directories and GGUF files (quantize GGUF beforehand with `llama-quantize`).
  - — [Ollama Modelfile docs](https://ollama.readthedocs.io/en/modelfile); [docs.ollama.com/import](https://docs.ollama.com/import.md)
- Third-party coverage reports that GGUF models run on llama.cpp and MLX/safetensors models run on MLX inside Ollama. — [yage.ai](https://yage.ai/share/mlx-apple-silicon-en-20260331.html); [gingter.org](https://gingter.org/2026/04/23/ollama-goes-mlx/)

**LM Studio**
- I found no official LM Studio document on loading LoRA adapters. A third-party April 2026 guide says LM Studio has no built-in LoRA training. — [PromptQuorum (KO)](https://www.promptquorum.com/ko/local-llms/lm-studio-advanced-features)
- A community export script fuses with `mlx_lm.fuse`, converts to GGUF and copies the result into LM Studio's models folder. — [export_to_lms.py](https://huggingface.co/Ex0bit/jit-lora/blob/main/src/export_to_lms.py)
- LM Studio ships both MLX and llama.cpp engines on Apple silicon. — [ExLLM LM Studio provider docs](https://hexdocs.pm/ex_llm/ExLLM.Providers.LMStudio.html)

**Speed figures**
- **Measured, llama.cpp, LLaMA 7B, M4 Pro 20-core (273 GB/s):**

  | Precision | Text generation (TG128) | Prompt processing (PP512) |
  |---|---|---|
  | Q4_0 | 50.74 tok/s | 439.78 tok/s |
  | Q8_0 | 30.69 tok/s | — |
  | F16 | 17.18 tok/s | — |

  The 16-core M4 Pro gets TG 49.64 and PP 364.06 at Q4_0. For comparison, the M4 Max 40-core gets TG 83.06 at Q4_0. — [llama.cpp discussion #4167](https://github.com/ggml-org/llama.cpp/discussions/4167)
- **Estimates ("triangulated", not measured), M4 Pro 24 GB with MLX:** Qwen 3.5 9B 4-bit ~32–42 tok/s at ~6 GB peak; 9B 8-bit ~30–40 tok/s at ~10.4 GB; 27B 4-bit ~15–22 tok/s at ~17–18 GB; 35B-A3B 4-bit ~18–25 tok/s at ~19.5–20.5 GB. — [willitrunai](https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide)
- **Measured, M4 Max:** Qwen3-4B decode ~145 tok/s and Gemma 3 4B ~141 tok/s with MLX/Core AI. — [apple-silicon-llm-bench](https://github.com/john-rocky/apple-silicon-llm-bench)
- **Estimate:** Qwen3 8B Q4_K_M on an M4 Pro via Ollama ~45 tok/s. — [llmcheck](https://llmcheck.net/models/qwen-3-8b-on-m4-pro/)

### Inferences
- **Time for ~500 generated tokens on an M4 Pro:**
  - **4B 4-bit:** ~70 tok/s, about 7 s. Estimated by halving the M4 Max 145 tok/s for half the bandwidth.
  - **7–9B 4-bit:** ~32–50 tok/s, about 10–16 s.
  - **7–9B 8-bit:** ~30 tok/s, about 16 s.
  - **12–14B 4-bit:** ~25–28 tok/s, about 18–20 s, scaled from 7B Q4_0 by weight size.
  - **Prefill:** a 500–1,000-token prompt adds about 1–2 s at ~440 tok/s.
  - Serving with an unfused adapter adds a small overhead. Fusing removes it.
- **Recommended serving path:**
  1. **Dev loop:** `mlx_lm.server --model <base-4bit-or-bf16>` with `"adapters": "adapters/style_v3"` per request. This makes A/B testing of adapter versions trivial.
  2. **Stable deploy:** `mlx_lm.fuse` (with `--dequantize`), then `mlx_lm.convert -q` back to 4-bit MLX, or GGUF via llama.cpp for Ollama or LM Studio.
  3. **llama-server:** use it if you want multiple adapters at runtime with scale blending, for example a style-strength knob via `scale`.
- **Ollama on 24 GB:** the MLX engine was officially pitched at 32 GB+ Macs, so on this machine Ollama may still run GGUF through llama.cpp. Performance would then be in line with the llama.cpp numbers above.

### Gaps
- I could not confirm whether Ollama ≥0.40 enables MLX on 24 GB Macs by default. Some third-party posts claim MLX became the default in v0.40.0 (Sept 2026) and that 16/24 GB Macs fall back to llama.cpp; I could not verify either claim.
- I could not confirm whether Ollama's MLX engine supports the `ADAPTER` directive, or whether Qwen3/3.5 and Gemma 3/4 safetensors adapters are accepted.
- I found no LM Studio documentation (version 0.3.x/0.4.x) on loading LoRA adapters on either engine.
- I found no measured MLX decode numbers specific to the M4 Pro for 4B, 12B or 14B models in 2026. The figures above are scaled estimates.
- I did not verify whether `mlx_lm.server` has a `--adapter-path` startup flag; SERVER.md documents only the per-request `adapters` field. Check with `mlx_lm.server --help`.

## Q6. Exposing the local model as a tool to Claude Code via MCP

### Takeaway
Build a small **stdio MCP server in Python** that exposes a tool such as `write_in_my_style(brief, length)`. The tool calls the local OpenAI-compatible endpoint (`mlx_lm.server` on :8080, `llama-server`, or Ollama's `/v1`) and returns the text. Register it with `claude mcp add --transport stdio <name> -- uv run server.py`. As of the 2026-07-28 MCP spec, the official Python SDK 2.x uses `from mcp.server import MCPServer`; older tutorials use FastMCP. Community "Ollama / OpenAI-compatible bridge" MCP servers exist, but none is a widely adopted reference implementation.

### Cited Findings
- **Official MCP Python quickstart (current docs, 2026-07-28 spec revision):**
  - Requires Python 3.10+ and "the Python MCP SDK 2.0.0 or higher". Install with `uv add "mcp[cli]"`.
  - Code: `from mcp.server import MCPServer`, `mcp = MCPServer("weather")`, tools declared with `@mcp.tool()` (type hints and docstrings generate the schemas), started with `mcp.run(transport="stdio")`.
  - The SDK depends on `httpx2`.
  - Warning: "Never write to stdout" in stdio servers. `print()` corrupts JSON-RPC, so log to stderr.
  - — [MCP: Build a server](https://modelcontextprotocol.io/docs/develop/build-server)
- **Registering with Claude Code:**
  - Syntax: `claude mcp add [options] <name> -- <command> [args...]`, for example `claude mcp add --env KEY=value --transport stdio myserver -- python server.py --port 8080`.
  - Scopes: `local` (the default, stored in `~/.claude.json` per project), `project` (`.mcp.json`, shareable) and `user`.
  - `.mcp.json` stdio entries use `command`, `args` and `env`, with `${VAR}` expansion.
  - — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- **Timeouts and limits in Claude Code:**
  - `MCP_TIMEOUT` sets the startup timeout.
  - The per-server `"timeout"` in ms overrides `MCP_TOOL_TIMEOUT` (which defaults to about 28 h when unset).
  - `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` defaults to 30 min for stdio.
  - `MAX_MCP_OUTPUT_TOKENS` defaults to 25,000, with a warning above 10,000 tokens.
  - — [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- **Existing community examples:**
  - A FastMCP server on Glama bridges to "any OpenAI-compatible LLM service" (a local service on port 5001, configured via `.env`, with a chat-completion tool over stdio). — [Glama: custom-mcp](https://glama.ai/mcp/servers/@Dev00355/custom-mcp)
  - Several Ollama MCP servers expose local models to Claude Code for "offload" tasks such as drafting and embeddings. — [mcpmarket: ollama-claude](https://mcpmarket.com/server/ollama-claude); [playbooks: Ollama MCP server](https://playbooks.com/mcp/newaiteesollama)
  - Treat all of these as third-party code to review before running.

### Inferences
- **Minimal design:**
  - An `MCPServer("style")` with one tool, `draft_in_my_voice(instructions: str, source_text: str | None, max_tokens: int = 600, temperature: float = 0.8)`.
  - The tool POSTs to `http://127.0.0.1:8080/v1/chat/completions` with `{"model": ..., "adapters": "adapters/style_vN", "messages": [...], "max_tokens": ...}` using an async HTTP client, and returns the text.
  - Optional parameters: `adapter_version` for A/B testing and `style_strength`, which maps to llama.cpp's per-request `lora` scale if that backend is used.
- **Timeouts:** at about 10–20 s per 500-token call on an M4 Pro, the defaults are fine. Set a per-server `"timeout"` of around 120,000 ms in `.mcp.json` as a guard.
- **Running the backend:** keep the model server as a separate long-running process (launchd or a terminal). Loading a model inside the MCP process would add model-load latency to Claude Code startup.
- **Tool description:** state when Claude should call the tool (final prose in the user's voice) and that its output should be lightly edited, not rewritten. That keeps Claude from paraphrasing the style away.

### Gaps
- I did not verify the exact current API of the standalone `fastmcp` package (jlowin/PrefectHQ), or whether `from mcp.server.fastmcp import FastMCP` still works as an alias in MCP Python SDK 2.x. Many 2025 tutorials use that import.
- I found no widely used, maintained reference MCP server that wraps `mlx_lm.server` specifically. The existing examples are small community projects targeting Ollama or generic OpenAI-compatible endpoints.
