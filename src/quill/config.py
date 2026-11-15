"""Load configs/quill.yaml and expand paths."""
from __future__ import annotations

import os
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DEFAULT = REPO / "configs" / "quill.yaml"


def load(path: str | os.PathLike | None = None) -> dict:
    p = Path(path or os.environ.get("QUILL_CONFIG") or DEFAULT)
    cfg = yaml.safe_load(p.read_text())
    cfg["paths"] = {k: Path(os.path.expanduser(v)) for k, v in cfg.get("paths", {}).items()}
    cfg["_file"] = str(p)
    global VOICE
    VOICE = cfg.get("voice", "")
    return cfg


VOICE = ""       # the voice of the config loaded last; reports of a named voice go in their own folder


def reports_dir(repo: Path, cfg: dict | None = None) -> Path:
    """eval_reports/ for the first corpus; eval_reports/<voice>/ for a config that names a voice."""
    d = Path(repo) / "eval_reports" / (cfg.get("voice", "") if cfg is not None else VOICE)
    d.mkdir(parents=True, exist_ok=True)
    return d
