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
    return cfg
