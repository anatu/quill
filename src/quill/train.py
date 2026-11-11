"""Run one SFT stage with mlx-lm (plan.md Phases 4-5).

The shared config is configs/train/sft.yaml. This fills in the model, the data, the adapter
path, the iteration count (passes x rows) and a cosine schedule with warmup, writes the
resolved config beside the adapter, and runs `mlx_lm.lora` under caffeinate with a log.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]


def adapter_dir(cfg: dict, name: str) -> Path:
    return Path(cfg["paths"]["home"]) / "adapters" / name


def resolve(cfg: dict, name: str, data: Path, passes: float = 1.0, overrides: dict | None = None,
            resume: str | None = None) -> dict:
    c = yaml.safe_load((REPO / "configs" / "train" / "sft.yaml").read_text())
    c.update(overrides or {})
    rows = sum(1 for x in (data / "train.jsonl").read_text().splitlines() if x.strip())
    iters = int(round(rows * passes / c["batch_size"]))
    updates = max(1, iters // c["grad_accumulation_steps"])
    warmup = min(10, max(1, updates // 5))
    lr = float(c["learning_rate"])
    c.update(model=str(Path(cfg["gen"]["base_model"]).expanduser()), data=str(data), adapter_path=str(adapter_dir(cfg, name)),
             iters=iters, learning_rate=lr,
             lr_schedule=dict(name="cosine_decay", warmup=warmup, warmup_init=1e-7,
                              arguments=[lr, max(1, updates - warmup), 1e-6]))
    if resume:
        c["resume_adapter_file"] = str(adapter_dir(cfg, resume) / "adapters.safetensors")
    return c


def parse_log(text: str) -> dict:
    """Val losses, the last train loss, tokens per second and peak memory from an mlx-lm log."""
    t = re.sub(r"\x1b\[[0-9;]*m", "", text)
    val = [(int(i), float(v)) for i, v in re.findall(r"^\s*(\d+)\s+val\s+([\d.]+)", t, re.M)]
    train = [(int(i), float(v), float(s)) for i, v, s in re.findall(r"^\s*(\d+)\s+([\d.]+)\s*[▲▼–-]?\s+([\d.]+)\s+[\d.]+k", t, re.M)]
    peak = re.search(r"(\d+)\s+peak memory footprint", t)       # from /usr/bin/time -l, in bytes
    return dict(val=val, train_last=train[-1][1] if train else None,
                loss_tok_per_s=round(sum(x[2] for x in train) / len(train), 1) if train else None,
                peak_gb=round(int(peak.group(1)) / 1e9, 2) if peak else None)


def run(cfg: dict, name: str, stage: str = "s1", passes: float = 1.0, overrides: dict | None = None,
        resume: str | None = None, data: Path | None = None, iters: int | None = None) -> dict:
    data = data or Path(cfg["paths"]["home"]) / "data" / "mlx" / f"sft-v1-{stage}"
    c = resolve(cfg, name, data, passes, overrides, resume)
    if iters:
        c["iters"] = iters
    d = adapter_dir(cfg, name)
    d.mkdir(parents=True, exist_ok=True)
    (d / "train_config.yaml").write_text(yaml.safe_dump(c, sort_keys=False))
    log = Path(cfg["paths"]["home"]) / "logs" / f"train-{name}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with log.open("w") as f:
        r = subprocess.run(["caffeinate", "-i", "-s", "/usr/bin/time", "-l", sys.executable, "-m", "mlx_lm", "lora", "-c", str(d / "train_config.yaml")],
                           stdout=f, stderr=subprocess.STDOUT, cwd=str(d))
    out = dict(name=name, base=Path(c["model"]).name, data=str(data), iters=c["iters"], passes=passes, exit=r.returncode,
               minutes=round((time.time() - t0) / 60, 1), log=str(log), **parse_log(log.read_text(errors="replace")))
    (d / "train_result.json").write_text(json.dumps(out, indent=1))
    return out
