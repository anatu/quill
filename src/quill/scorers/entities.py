"""M5 entity preservation: names, numbers, money, dates and links kept, none added.

Regex and capitalization rules only. spaCy NER is planned on top (plan.md M5) and is not
wired in yet. Known gap: a new one-word name that appears only at the start of a sentence
is not seen.
"""
from __future__ import annotations

import re

URL = re.compile(r"https?://[^\s)>\]]+|www\.[^\s)>\]]+")
NUMBER = re.compile(r"(?<![\w.])[$€£]?\d[\d,]*(?:\.\d+)?%?(?:\s?(?:thousand|million|billion|trillion|bn|k|m)\b)?", re.I)
MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december"
DATE = re.compile(rf"\b(?:{MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s+\d{{4}})?|\b(?:{MONTHS})\s+\d{{4}}\b", re.I)
WORDNUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
           "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20", "thirty": "30", "forty": "40",
           "fifty": "50", "hundred": "100", "half": "0.5"}
SCALE = {"thousand": 1e3, "k": 1e3, "million": 1e6, "m": 1e6, "billion": 1e9, "bn": 1e9, "trillion": 1e12}
CAP = r"[A-Z][\w’'.&-]*"
NAME = re.compile(rf"\b{CAP}(?:\s+(?:(?:of|the|and|de|van|von|for)\s+)?{CAP})*")
SENT_START = re.compile(r"(?:^|[.!?:]\s+|\n\s*|[“\"(]\s*)$")
STOP = set("""a an the i i'm i've i'd i'll it it's its he she we they you this that these those there here but and or so
if in on at for to of as by with from not no yes when what why how who where which while then than also most many
some every each all both one two my your his her our their people nobody everyone someone something nothing
mr mrs ms dr""".split()) | set(MONTHS.split("|")) | {"monday", "tuesday", "wednesday", "thursday", "friday",
                                                       "saturday", "sunday"}


def _num(tok: str) -> str:
    t = tok.lower().replace(",", "").strip()
    m = re.match(r"([$€£]?)(\d+(?:\.\d+)?)(%?)\s?([a-z]+)?", t)
    if not m:
        return t
    val = float(m.group(2)) * SCALE.get(m.group(4) or "", 1)
    return f"{m.group(1)}{val:g}{m.group(3)}"


def extract(text: str, known: set[str] = frozenset()) -> dict[str, set[str]]:
    """known: lower-case name tokens seen away from a sentence start (in this or the paired text).
    A lone capitalized word that opens a sentence is a name only if it is known."""
    t = text.replace("’", "'")
    urls = {u.rstrip(".,;") for u in URL.findall(t)}
    no_url = URL.sub(" ", t)
    dates = {re.sub(r"(st|nd|rd|th)\b|[.,]", "", d.lower()).strip() for d in DATE.findall(no_url)}
    numbers = {_num(n) for n in NUMBER.findall(no_url)}
    words = re.findall(r"[a-z]+", no_url.lower())
    numbers |= {WORDNUM[w] for w in words if w in WORDNUM and w not in ("one", "half")}
    names = set()
    inner = set()
    for m in NAME.finditer(no_url):
        toks = m.group(0).split()
        first = toks[0].lower().strip(".'")
        at_start = bool(SENT_START.search(no_url[:m.start()]))
        if not at_start:
            inner.update(x.lower().strip(".,'").removesuffix("'s") for x in toks)
        if at_start and (first in STOP or (len(toks) == 1 and first.removesuffix("'s") not in known)):
            toks = toks[1:]             # a capital that only marks the sentence start
            while toks and toks[0].lower() in STOP | {"of", "the", "and", "for"}:
                toks = toks[1:]
        while toks and toks[-1].lower() in ("of", "the", "and", "for", "de", "van", "von"):
            toks = toks[:-1]
        name = " ".join(toks).strip(".,'").removesuffix("'s")
        if name and name.lower() not in STOP and not name.isdigit() and len(name) > 1:
            names.add(name.lower())
    return dict(names=names, numbers=numbers, dates=dates, urls=urls, _inner=inner)


def _covered(item: str, pool: set[str]) -> bool:
    """A name counts as kept when it matches, or when it is a part of a longer kept name
    ("Buffett" for "Warren Buffett") or the other way round."""
    return item in pool or any(re.search(rf"\b{re.escape(item)}\b", p) or re.search(rf"\b{re.escape(p)}\b", item)
                               for p in pool)


def compare(input_text: str, output: str) -> dict:
    """Missing: in the input, not in the output. Added: in the output, not in the input."""
    known = extract(input_text)["_inner"] | extract(output)["_inner"]
    a, b = extract(input_text, known), extract(output, known)
    missing, added = {}, {}
    for k in ("names", "numbers", "dates", "urls"):
        soft = k == "names"
        miss = sorted(x for x in a[k] if not (_covered(x, b[k]) if soft else x in b[k]))
        add = sorted(x for x in b[k] if not (_covered(x, a[k]) if soft else x in a[k]))
        if miss:
            missing[k] = miss
        if add:
            added[k] = add
    return dict(ok=not missing and not added, missing=missing, added=added)
