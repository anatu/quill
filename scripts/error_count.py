"""Count errors in passages written from held-out notes (explain task).

    uv run python scripts/error_count.py [system ...]      # default: tb-x1 bt-ex human

Claude Opus reads each passage blind, with the notes and the book's own passage as reference, and
lists errors by type and severity (configs/prompts/error_check.txt). The human passage is run
through the same check as a control: whatever it is charged with is the checker's false-alarm
rate. Annotations (with quotes) stay under ~/.quill/tb/eval/errors/; the report holds counts only.
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

from quill import config
from quill.eval import pool
from quill.gen.claude_cli import Claude, prompt

TYPES = ("logic", "misstatement", "unsupported", "vague", "repetition", "structure", "entity")
SUBSTANCE = ("logic", "misstatement", "unsupported", "entity")


def parse(reply: str) -> list[dict]:
    m = re.search(r"\{.*\}", reply, re.S)
    try:
        errs = json.loads(m.group(0)).get("errors", []) if m else None
    except json.JSONDecodeError:
        errs = None
    if errs is None:
        return [dict(type="unparsed", severity="minor", quote="", why=reply[:200])]
    return [e for e in errs if e.get("type") in TYPES]


def main(systems: list[str], part: str = "dev") -> None:
    cfg = config.load("configs/textbook.yaml")
    d = Path(cfg["paths"]["eval"]) / "outputs"
    human = {c["id"]: c["text"] for c in pool.author_chunks(cfg) if c["split"] == part}
    claude = Claude(cfg, "claude-opus-5-5", cfg.get("gen", {}).get("workers", 4))
    out_dir = Path(cfg["paths"]["eval"]) / "errors"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = {}
    for name in systems:
        items = [json.loads(x) for x in (d / name / f"{part}.jsonl").read_text().splitlines()]
        replies = claude.map([(prompt("error_check", notes=i["input"], reference=human[i["id"]], passage=i["text"]),) for i in items])
        ann = [dict(id=i["id"], words=len(i["text"].split()), errors=parse(r)) for i, r in zip(items, replies)]
        (out_dir / f"{name}-{part}.jsonl").write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a in ann))
        rows[name] = ann
    rep = dict(generated=time.strftime("%Y-%m-%dT%H:%M:%S"), split=part, checker=claude.model, cost_usd=round(claude.cost, 2), systems={})
    for name, ann in rows.items():
        errs = [e for a in ann for e in a["errors"]]
        major = [e for e in errs if e.get("severity") == "major"]
        words = sum(a["words"] for a in ann)
        rep["systems"][name] = dict(
            passages=len(ann), errors=len(errs), major=len(major),
            errors_per_passage=round(len(errs) / len(ann), 2), major_per_passage=round(len(major) / len(ann), 2),
            errors_per_1k_words=round(1000 * len(errs) / words, 2),
            passages_clean=sum(1 for a in ann if not a["errors"]),
            passages_no_major=sum(1 for a in ann if not any(e.get("severity") == "major" for e in a["errors"])),
            passages_with_major_substance=sum(1 for a in ann if any(e.get("severity") == "major" and e["type"] in SUBSTANCE for e in a["errors"])),
            by_type={t: dict(all=sum(e["type"] == t for e in errs), major=sum(e["type"] == t for e in major)) for t in TYPES},
            unparsed=sum(e["type"] == "unparsed" for a in ann for e in a["errors"]))
    r = config.reports_dir(config.REPO, cfg)
    (r / f"error-count-{part}.json").write_text(json.dumps(rep, indent=1))
    L = [f"# Error count on {part} ({rep['generated']})", "",
         f"Checker: {rep['checker']}, blind to the system, given the notes and the book's passage as reference. "
         "`human` is the book's own passage run through the same check: its counts are the checker's false-alarm rate.", "",
         "| System | Passages | Errors | Major | Errors / passage | Major / passage | Clean passages | No major error | Major error of substance |",
         "|---|---|---|---|---|---|---|---|---|"]
    for n, s in rep["systems"].items():
        L.append(f"| {n} | {s['passages']} | {s['errors']} | {s['major']} | {s['errors_per_passage']} | {s['major_per_passage']} | "
                 f"{s['passages_clean']} | {s['passages_no_major']} | {s['passages_with_major_substance']} |")
    L += ["", "Errors by type, all (major):", "", "| System | " + " | ".join(TYPES) + " |", "|---|" + "---|" * len(TYPES)]
    for n, s in rep["systems"].items():
        L.append(f"| {n} | " + " | ".join(f"{s['by_type'][t]['all']} ({s['by_type'][t]['major']})" for t in TYPES) + " |")
    L += ["", "Substance = logic, misstatement, unsupported, entity."]
    (r / f"error-count-{part}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L)); print(f"cost ${rep['cost_usd']}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["tb-x1", "bt-ex", "human"])
