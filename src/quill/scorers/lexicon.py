"""Lexicon v0: AI-writing tells in three families (vocabulary, structure, artifacts).

Rates are hits per 1,000 words. An item the author used before the cutoff at or above a
human baseline is whitelisted: it is still counted and reported, but it leaves the
family score. Word baselines come from wordfreq (its sources end in 2021). Phrase and
structure baselines come from a human impostor corpus when one is configured.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import yaml

from ..ingest import textlib as T
from . import contrast

REPO = Path(__file__).resolve().parents[3]
SEED = REPO / "configs" / "lexicon" / "seed_v0.yaml"
KOBAK = REPO / "configs" / "lexicon" / "kobak_excess_words.csv"
FLAGS = re.I | re.M
FAMILY = {"word": "vocabulary", "kobak": "vocabulary", "phrase": "vocabulary", "structure": "structure",
          "artifact": "artifacts"}


def inflect(lemma: str) -> set[str]:
    """Surface forms of a seed lemma. Over-generates; a form that is not a word never matches."""
    w = lemma.lower()
    out = {w}
    if w.endswith("ly") or w.endswith("s"):
        return out
    if w.endswith("y") and w[-2] not in "aeiou":
        out |= {w[:-1] + "ies", w[:-1] + "ied", w + "ing"}
    elif w.endswith("e"):
        out |= {w + "s", w + "d", w[:-1] + "ing"}
    else:
        out |= {w + "s", w + "es", w + "ed", w + "ing"}
    return out


def kobak_style_words(path: Path = KOBAK, max_general_per_1k: float | None = None) -> set[str]:
    """Kobak's style words. Drops words more common in general English than the cap (function words)."""
    with open(path, newline="") as f:
        words = {r["word"].lower() for r in csv.DictReader(f) if "style" in r["type"]}
    if max_general_per_1k is not None:
        from wordfreq import word_frequency
        words = {w for w in words if 1000 * word_frequency(w, "en") <= max_general_per_1k}
    return words


class Lexicon:
    def __init__(self, seed: dict, kobak: set[str], whitelist: set[str] | None = None):
        self.forms: dict[str, str] = {}
        for lemma in seed["vocabulary"]["words"]:
            for f in inflect(lemma):
                self.forms.setdefault(f, lemma)
        self.kobak = {w for w in kobak if w not in self.forms}
        self.phrases = {k: re.compile(v, FLAGS) for k, v in seed["vocabulary"]["phrases"].items()}
        self.structure = {k: re.compile(v, FLAGS) for k, v in seed["structure"].items()}
        self.artifacts = {k: re.compile(v, FLAGS) for k, v in seed["artifacts"].items()}
        self.rate_only = {f"structure:{k}" for k in seed.get("rate_only", [])}
        self.whitelist = set(whitelist or ())

    @classmethod
    def load(cls, v0: Path | None = None) -> "Lexicon":
        """Seed lexicon, plus the whitelist from a built v0.json when given."""
        seed = yaml.safe_load(SEED.read_text())
        wl = set(json.loads(Path(v0).read_text())["whitelist"]) if v0 and Path(v0).exists() else set()
        return cls(seed, kobak_style_words(max_general_per_1k=seed.get("kobak_max_general_per_1k")), wl)

    def count(self, text: str) -> tuple[Counter, int]:
        """Return (hits per item, word count). Item keys: word:x, kobak:x, phrase:x, structure:x, artifact:x."""
        t = text.replace("’", "'")
        toks = T.words(t)
        c: Counter = Counter()
        for w in toks:
            if w in self.forms:
                c[f"word:{self.forms[w]}"] += 1
            elif w in self.kobak:
                c[f"kobak:{w}"] += 1
        for k, rx in self.phrases.items():
            n = sum(1 for _ in rx.finditer(t))
            if n:
                c[f"phrase:{k}"] = n
        for k, rx in self.structure.items():
            n = sum(1 for _ in rx.finditer(t))
            if n:
                c[f"structure:{k}"] = n
        n = contrast.count(t)
        if n:
            c["structure:contrast"] = n
        for k, rx in self.artifacts.items():
            n = sum(1 for _ in rx.finditer(t))
            if n:
                c[f"artifact:{k}"] = n
        return c, len(toks)

    @staticmethod
    def family(item: str) -> str:
        return FAMILY[item.split(":", 1)[0]]

    def score(self, text: str) -> dict:
        """Family rates per 1k words (whitelisted and rate-only items excluded), raw hits and items."""
        c, n = self.count(text)
        hits = Counter()
        for item, k in c.items():
            if item not in self.whitelist and item not in self.rate_only:
                hits[self.family(item)] += k
        per = 1000.0 / max(1, n)
        fams = ("vocabulary", "structure", "artifacts")
        return dict(words=n, hits={f: hits[f] for f in fams}, rates={f: hits[f] * per for f in fams},
                    items={k: v for k, v in c.most_common()})


def read_baseline(dirpath: Path | None, before_year: int = 2022) -> list[str]:
    """Human impostor passages dated up to `before_year` (simpass corpus layout). Empty if absent."""
    if not dirpath or not Path(dirpath).is_dir():
        return []
    out = []
    for meta in sorted(Path(dirpath).glob("*_posts.json")):
        name = meta.name[:-len("_posts.json")]
        if name.startswith(("housel", "claude")):
            continue
        posts = json.loads(meta.read_text())
        posts = posts.get("posts", posts) if isinstance(posts, dict) else posts
        ok = {p["id"] for p in posts if p.get("year") and p["year"] <= before_year}
        jl = meta.with_name(name + ".jsonl")
        if not jl.exists():
            continue
        for line in jl.read_text().splitlines():
            r = json.loads(line)
            if r.get("group") in ok:
                out.append("\n\n".join(r["paras"]))
    return out


def tell_rates(texts: list[str]) -> dict:
    """The author's own rates for habits a lexicon must not punish (plan.md Phase 1 step 8)."""
    s = T.stylometrics([t.split("\n\n") for t in texts])
    joined = "\n\n".join(texts)
    k = 1000.0 / max(1, s["n_words"])
    rx = yaml.safe_load(SEED.read_text())["structure"]
    n = lambda key: sum(1 for _ in re.finditer(rx[key], joined, FLAGS))   # noqa: E731
    return {
        "words": s["n_words"],
        "em_dash_per_1k": round(s["emdash_per_1k"], 3),
        "colon_per_1k": round(s["colon_per_1k"], 3),
        "semicolon_per_1k": round(s["semicolon_per_1k"], 3),
        "parenthetical_per_1k": round(s["paren_per_1k"], 3),
        "contrast_per_1k": round(k * contrast.count(joined), 3),
        "not_just_but_per_1k": round(k * n("not_just_but"), 3),
        "rather_than_per_1k": round(k * n("rather_than"), 3),
        "tricolon_per_1k": round(k * n("tricolon"), 3),
        "questions_per_100_sentences": round(s["question_per_100s"], 3),
        "sentence_len_mean": round(s["sent_len_mean"], 2),
        "sentence_len_sd": round(s["sent_len_sd"], 2),
        "one_sentence_para_share": round(s["one_sent_para_share"], 3),
        "you_per_1k": round(s["sp_per_1k"], 3),
    }


def build_v0(author_pre: list[str], baseline: list[str], out: Path | None = None, margin: float = 1.0) -> dict:
    """Build lexicon v0 from the seed: count the author's pre-cutoff text, whitelist his habits.

    Whitelist rule: the author's rate >= margin x the baseline rate, and he uses the item at all.
    """
    from wordfreq import word_frequency

    seed = yaml.safe_load(SEED.read_text())
    lex = Lexicon(seed, kobak_style_words(max_general_per_1k=seed.get("kobak_max_general_per_1k")))
    a_c, a_n = lex.count("\n\n".join(author_pre))
    b_c, b_n = lex.count("\n\n".join(baseline)) if baseline else (Counter(), 0)
    forms_of: dict[str, list[str]] = {}
    for f, lemma in lex.forms.items():
        forms_of.setdefault(lemma, []).append(f)

    def general(item: str) -> tuple[float | None, str]:
        kind, key = item.split(":", 1)
        if kind == "word":
            return 1000 * sum(word_frequency(f, "en") for f in forms_of[key]), "wordfreq"
        if kind == "kobak":
            return 1000 * word_frequency(key, "en"), "wordfreq"
        if b_n:
            return 1000 * b_c[item] / b_n, "impostor corpus"
        return None, "none"

    items = ([f"word:{w}" for w in seed["vocabulary"]["words"]] + [f"kobak:{w}" for w in sorted(lex.kobak)]
             + [f"phrase:{k}" for k in lex.phrases] + [f"structure:{k}" for k in lex.structure]
             + ["structure:contrast"] + [f"artifact:{k}" for k in lex.artifacts])
    table, whitelist = {}, []
    for item in items:
        a = 1000 * a_c[item] / max(1, a_n)
        g, src = general(item)
        wl = bool(a > 0 and g is not None and a >= margin * g and not item.startswith("artifact:"))
        if wl:
            whitelist.append(item)
        table[item] = dict(author_per_1k=round(a, 4), baseline_per_1k=None if g is None else round(g, 4),
                           baseline=src, whitelisted=wl, rate_only=item in lex.rate_only)
    v0 = {
        "version": "v0",
        "seed": str(SEED.relative_to(REPO)),
        "author_words": a_n,
        "baseline_words": b_n,
        "margin": margin,
        "whitelist": sorted(whitelist),
        "exempt": seed.get("exempt", []),
        "author_rates": tell_rates(author_pre),
        "items": table,
    }
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(v0, indent=1))
    return v0
