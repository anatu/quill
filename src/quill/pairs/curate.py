"""Curation of training pairs (plan.md Phase 3). A pair is dropped when:

  closure  the target holds a name, number, date or link the input lacks (teaches invention)
  markers  the input's <QUOTE>/<IMAGE> lines differ from the target's
  meaning  MIS(input, target) is under the floor
  copy     the input is a near-copy of the target (word-level similarity over the cap)
  length   the input is outside 0.5-2x the target's length
  tokens   the rendered example is over the training sequence length
The target is never edited.
"""
from __future__ import annotations

import difflib
import json
import re
import time
from pathlib import Path

from .. import template
from ..scorers import entities, meaning
from . import generate as G

FORMS = dict(A="paraphrase", B="draft")
MIS_MIN, COPY_MAX, LEN_LO, LEN_HI, MAX_TOKENS = 0.7, 0.85, 0.5, 2.0, 2048
REPO = Path(__file__).resolve().parents[3]


def plain(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", G.MARKER.sub("", text)).strip()


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower().split(), b.lower().split(), autojunk=False).ratio()


ONES = dict(zip("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
                "seventeen eighteen nineteen".split(), range(20)))
TENS = dict(zip("twenty thirty forty fifty sixty seventy eighty ninety".split(), range(20, 100, 10)))
ORD = dict(first=1, second=2, third=3, fifth=5, eighth=8, ninth=9, twelfth=12)
MULT = dict(hundred=100, thousand=10 ** 3, million=10 ** 6, billion=10 ** 9, trillion=10 ** 12)
IDIOM = re.compile(r"\b(?:9/11|20/20|24/7|401\(k\)|(?:a|full|complete)\s+(?:180|360))(?![\w/])", re.I)
ENUM = re.compile(r"(?:(?<=\s)|^)\(?\d{1,2}[.)](?=\s)", re.M)
ALIAS = [{"america", "american", "americans", "united states", "u.s", "us", "usa"}, {"britain", "british", "uk", "united kingdom"}]
LINK = {"of", "the", "and", "for", "a", "an", "in"}


def _word_value(w: str):
    w = w.lower()
    if w in ONES or w in TENS or w in ORD or w in MULT:
        return ONES.get(w, TENS.get(w, ORD.get(w, MULT.get(w))))
    for suf in ("ieth", "th", "s"):                       # twentieth, sixteenth, hundreds
        base = w[:-len(suf)] + ("y" if suf == "ieth" else "") if w.endswith(suf) else None
        if base and (base in ONES or base in TENS or base in MULT):
            return ONES.get(base, TENS.get(base, MULT.get(base)))
    return None


def spelled_numbers(text: str) -> set[str]:
    """Numbers written as words: "thirty-six" -> 36, "two hundred" -> 200, "sixteenth" -> 16. Each
    part and each total counts, so a loose match is possible; this is a filter against false alarms."""
    out, run = set(), []

    def flush():
        if run:
            total = cur = 0
            for v in run:
                out.add(f"{v:g}")
                if v >= 1000:
                    total, cur = total + max(cur, 1) * v, 0
                elif v == 100:
                    cur = max(cur, 1) * 100
                else:
                    cur += v
            out.add(f"{total + cur:g}")
            run.clear()

    for w in re.findall(r"[A-Za-z]+|[^A-Za-z\s-]", text):
        v = _word_value(w)
        if v is not None:
            run.append(v)
        elif w.lower() != "and" or not run:
            flush()
    flush()
    return out


def _core(n: str) -> str:
    return re.sub(r"[$€£%]", "", n)


def _initials_match(acr: str, words: list[str]) -> bool:
    ws = [w for w in words if w not in LINK]
    k = len(acr)
    return any("".join(w[0] for w in ws[i:i + k]) == acr for i in range(len(ws) - k + 1)) or \
        any(w[0] == acr[0] and re.search(".*".join(map(re.escape, acr)), w) for w in ws if len(w) > len(acr) + 2)


def _name_in_input(name: str, low: str, words: list[str], wordset: set[str], entity_tokens: set[str]) -> bool:
    toks = [t for t in re.findall(r"[a-z0-9]+", name) if t not in LINK]
    if all(t in wordset for t in toks):                   # present in lower case: a word, not a new fact
        return True
    for group in ALIAS:
        if name in group and any(re.search(rf"(?<![a-z]){re.escape(a)}(?![a-z])", low) for a in group):
            return True
    if len(toks) > 1:                                     # a spelling variant: Allan / Allen
        n = len(name.split())
        ws = low.split()
        if any(difflib.SequenceMatcher(None, name, " ".join(ws[i:i + n]).strip(".,;:'\"()")).ratio() >= 0.85
               for i in range(len(ws) - n + 1)):
            return True
    for t in toks:
        if t in wordset or (len(toks) == 1 and t in entities.COMMON):   # an ordinary word that opens a sentence
            continue
        base = t[:-1] if t.endswith("s") and len(t) > 3 else t
        if len(base) <= 5 and _initials_match(base, words):
            continue                                      # JFK for John F. Kennedy, TV for television
        if len(base) <= 5 and " " not in name and t not in entity_tokens:
            continue                                      # a short capitalized word spaCy does not call an entity
        if any((len(base) >= 3 and w.startswith(base)) or (len(w) >= 4 and base[:4] == w[:4]) for w in wordset):
            continue                                      # Fed / Federal, German / Germany
        return False
    return True


def closure(inp: str, target: str) -> dict:
    """What the target holds and the input lacks, after allowing for form: numbers as words, percent
    signs, list numbers, idioms ("a 180", "9/11"), acronyms and capitalized ordinary words."""
    inp, target = plain(inp), IDIOM.sub(" ", ENUM.sub(" ", plain(target)))
    added = entities.compare(inp, target)["added"]
    low = inp.lower().replace("’", "'")
    words = re.findall(r"[a-z0-9]+", low)
    wordset = set(words)
    have = {_core(n) for n in entities.extract(inp)["numbers"]} | spelled_numbers(inp) | set(re.findall(r"\d+", low))
    miss = {}
    nums = [n for n in added.get("numbers", []) if _core(n) not in have]
    ent = entities.ner_tokens(target) if added.get("names") else set()
    names = [n for n in added.get("names", []) if not _name_in_input(n, low, words, wordset, ent)]
    for k, v in (("numbers", nums), ("names", names), ("dates", added.get("dates", [])), ("urls", added.get("urls", []))):
        if v:
            miss[k] = v
    return miss


def lost_items(inp: str, target: str) -> list[str]:
    """The missing items as they stand in the target, each with a few words around it."""
    t = plain(target).replace("\n", " ")
    out = []
    for kind, items in closure(inp, target).items():
        for x in items:
            pat = r"(?<![\d.,])" + re.escape(_core(x)) if kind == "numbers" else re.escape(x).replace("\\ ", r"\s+")
            if kind == "numbers" and "e+" in x:           # a scaled figure: 8e+07 stands for "80 million"
                v = float(_core(x))
                pat = "|".join(rf"{v / m:g}\s?{w}" for w, m in entities.SCALE.items() if v / m >= 1)
                pat = f"(?:{pat})"
            m = re.search(r"((?:\S+\s+){0,3})(\S*" + pat + r"\S*)((?:\s+\S+){0,3})", t.replace("’", "'"), re.I)
            out.append("".join(m.groups()).strip() if m else x)
    return list(dict.fromkeys(out))


def token_counter(cfg: dict):
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(str(Path(cfg["gen"]["base_model"]).expanduser()))
    return lambda msgs: len(tok(tok.apply_chat_template(msgs, tokenize=False))["input_ids"])


def check(inp: str, target: str, mis: float, tokens: int) -> list[str]:
    fails = []
    if closure(inp, target):
        fails.append("closure")
    if G.markers(inp) != G.markers(target):
        fails.append("markers")
    if mis < MIS_MIN:
        fails.append("meaning")
    if similarity(plain(inp), plain(target)) > COPY_MAX:
        fails.append("copy")
    if not LEN_LO <= len(inp.split()) / max(1, len(target.split())) <= LEN_HI:
        fails.append("length")
    if tokens > MAX_TOKENS:
        fails.append("tokens")
    return fails


def messages(row: dict, form: str) -> list[dict]:
    return template.messages("restyle", FORMS[form], template.bucket(row["words"]), row[FORMS[form]], row["target"])


def score(cfg: dict, rows: list[dict], count=None, mis=None, forms=tuple(FORMS)) -> list[dict]:
    """Add row['checks'][form] = dict(fails, mis, tokens, similarity)."""
    count = count or token_counter(cfg)
    mis = mis or meaning.MIS(Path(cfg["paths"]["eval"]) / "cache")
    entities.set_common(r["target"] for r in rows)
    for form in forms:
        key = FORMS[form]
        a, b = [plain(r[key]) for r in rows], [plain(r["target"]) for r in rows]
        ms = [max(x, y) for x, y in zip(mis.score(a, b), mis.score(b, a))]   # window misalignment only lowers a score
        for r, m in zip(rows, ms):
            n = count(messages(r, form))
            r.setdefault("checks", {})[form] = dict(fails=check(r[key], r["target"], m, n), mis=round(m, 4), tokens=n,
                                                    similarity=round(similarity(plain(r[key]), plain(r["target"])), 3))
    return rows


def summary(rows: list[dict]) -> dict:
    out = {}
    for part in sorted({r["split"] for r in rows}):
        rs = [r for r in rows if r["split"] == part]
        s = dict(chunks=len(rs), both=sum(not r["checks"]["A"]["fails"] and not r["checks"]["B"]["fails"] for r in rs))
        s["both_share"] = round(s["both"] / max(1, len(rs)), 4)
        for f in FORMS:
            fails = [x for r in rs for x in r["checks"][f]["fails"]]
            s[f] = dict(kept=sum(not r["checks"][f]["fails"] for r in rs), fails={k: fails.count(k) for k in sorted(set(fails))},
                        mis_median=round(sorted(r["checks"][f]["mis"] for r in rs)[len(rs) // 2], 3),
                        input_to_target_words=round(sum(len(r[FORMS[f]].split()) for r in rs) / max(1, sum(len(r["target"].split()) for r in rs)), 3),
                        max_tokens=max(r["checks"][f]["tokens"] for r in rs))
        out[part] = s
    return out


def report(cfg: dict, rows: list[dict], extra: dict | None = None) -> dict:
    s = summary(rows)
    rep = dict(version=G.VERSION, generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
               thresholds=dict(mis_min=MIS_MIN, copy_max=COPY_MAX, length=[LEN_LO, LEN_HI], max_tokens=MAX_TOKENS),
               splits=s, gate=dict(need=0.85, got=s.get("train", {}).get("both_share"),
                                   passed=s.get("train", {}).get("both_share", 0) >= 0.85), **(extra or {}))
    L = [f"# Training pairs {G.VERSION}: curation ({rep['generated']})", "",
         "Form A is a neutral paraphrase; form B is a generic draft from the fact list. The target is the author's chunk, verbatim. "
         f"A pair is kept when the target adds no name, number, date or link, the markers match, MIS is at least {MIS_MIN}, "
         f"word similarity is at most {COPY_MAX}, the input is {LEN_LO}-{LEN_HI}x the target and the example fits {MAX_TOKENS} tokens.", "",
         "| Split | Chunks | Form | Kept | Median MIS | Input/target words | Max tokens | Fails |", "|---|---|---|---|---|---|---|---|"]
    for part, v in s.items():
        for f in FORMS:
            x = v[f]
            L.append(f"| {part} | {v['chunks']} | {f} | {x['kept']} ({x['kept'] / max(1, v['chunks']):.1%}) | {x['mis_median']} | "
                     f"{x['input_to_target_words']} | {x['max_tokens']} | " + (", ".join(f"{k} {n}" for k, n in x["fails"].items()) or "none") + " |")
    t = s.get("train", {})
    L += ["", f"Train chunks that keep both forms: {t.get('both')} of {t.get('chunks')} ({t.get('both_share', 0):.1%}). "
              f"The gate is 85%: {'passes' if rep['gate']['passed'] else 'fails'}."]
    for k, v in (extra or {}).items():
        L += ["", f"{k}: {json.dumps(v)}"]
    d = REPO / "eval_reports"
    (d / f"pairs-{G.VERSION}.json").write_text(json.dumps(rep, indent=1))
    (d / f"pairs-{G.VERSION}.md").write_text("\n".join(L) + "\n")
    return rep
