"""M5 entity preservation: names, numbers, money, dates and links kept, none added.

Regex and capitalization rules find the entities. spaCy NER (en_core_web_sm) fixes their known
gap: a name seen only at the start of a sentence ("Buffett said...") counts when NER tags it as
a person, organisation or place and the word is not an ordinary one. The small NER model tags
ordinary sentence openers ("Luck", "Vanity") as names, so words seen in lower case in a
reference text (set_common) are never rescued.
"""
from __future__ import annotations

import re

URL = re.compile(r"https?://[^\s)>\]]+|www\.[^\s)>\]]+")
NUMBER = re.compile(r"(?<![\w.])[$€£]?\d[\d,]*(?:\.\d+)?%?(?:\s?(?:thousand|million|billion|trillion|bn|k|m)\b)?", re.I)
MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december"
DATE = re.compile(rf"\b(?:{MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s+\d{{4}})?|\b(?:{MONTHS})\s+\d{{4}}\b", re.I)
WORDNUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
           "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20", "thirty": "30", "forty": "40",
           "fifty": "50", "hundred": "100", "half": "0.5", "thirteen": "13", "fourteen": "14", "fifteen": "15",
           "sixteen": "16", "seventeen": "17", "eighteen": "18", "nineteen": "19", "sixty": "60", "seventy": "70",
           "eighty": "80", "ninety": "90"}
SCALE = {"thousand": 1e3, "k": 1e3, "million": 1e6, "m": 1e6, "billion": 1e9, "bn": 1e9, "trillion": 1e12}
CAP = r"(?:[A-Z]\.|[A-Z][\w’'&-]*)"      # "J." is an initial; any other full stop ends the name
LIST_MARK = re.compile(r"(?m)^\s*(?:[-*•]\s+)?(?:#+\s+)?(?:(?:(?:point|item|tip|lesson|section|rule|law|step|part|"
                       r"number|no\.?)\s+)?#?\d+(?:\s+in the list)?\s*[:.)]\s+)?", re.I)
NAME = re.compile(rf"\b{CAP}(?:\s+(?:(?:of|the|and|de|van|von|for)\s+)?{CAP})*")
SENT_START = re.compile(r"(?:^|[.!?:]\s+|\n\s*|[“\"(]\s*)$")
STOP = set("""a an the i i'm i've i'd i'll it it's its he she we they you this that these those there here but and or so
if in on at for to of as by with from not no yes when what why how who where which while then than also most many
some every each all both one two my your his her our their people nobody everyone someone something nothing
mr mrs ms dr ok okay""".split()) | set(MONTHS.split("|")) | {"monday", "tuesday", "wednesday", "thursday", "friday",
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
    The capitalized word that opens a sentence counts as part of a name only if it is known."""
    t = LIST_MARK.sub("", text.replace("’", "'")).replace("**", "")      # list numbers are not facts
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
        inner.update(x.lower().strip(".,'").removesuffix("'s") for x in (toks if not at_start else toks[1:]))
        while toks and toks[-1].lower() in STOP | {"of", "the", "and", "for", "de", "van", "von"}:
            toks = toks[:-1]
        if not toks:
            continue
        if at_start and (first in STOP or first.removesuffix("'s") not in known):
            toks = toks[1:]             # a capital that only marks the sentence start
            while toks and toks[0].lower() in STOP | {"of", "the", "and", "for"}:
                toks = toks[1:]
        name = " ".join(toks).strip(".,'").removesuffix("'s")
        if name and name.lower() not in STOP and not name.isdigit() and len(name) > 1:
            names.add(name.lower())
    return dict(names=names, numbers=numbers, dates=dates, urls=urls, _inner=inner)


LINK = {"of", "the", "and", "for", "de", "van", "von"}


def _covered(item: str, pool: set[str]) -> bool:
    """A name counts as kept when it matches, or when it is a part of a longer kept name
    ("Buffett" for "Warren Buffett") or the other way round."""
    if item in pool:
        return True
    a = set(item.split()) - LINK
    return any(a <= (b := set(p.split()) - LINK) or b <= a for p in pool if set(p.split()) - LINK)


NER_LABELS = {"PERSON", "ORG", "GPE", "LOC", "FAC", "NORP"}
_nlp = None
COMMON: set[str] = set()


def set_common(texts) -> None:
    """Words that occur in lower case in `texts` are ordinary words, not names."""
    for t in texts:
        COMMON.update(re.findall(r"\b[a-z]{2,}\b", t))


def ner_tokens(text: str) -> set[str]:
    """Lower-case tokens of the people, organisations and places spaCy finds."""
    global _nlp
    if _nlp is None:
        import spacy

        _nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
    return {t.lower().strip(".,'").removesuffix("'s") for e in _nlp(text.replace("’", "'")).ents
            if e.label_ in NER_LABELS for t in e.text.split()} - STOP - COMMON


def compare(input_text: str, output: str, ner: bool = True) -> dict:
    """Missing: in the input, not in the output. Added: in the output, not in the input."""
    known = extract(input_text)["_inner"] | extract(output)["_inner"]
    if ner:
        known |= ner_tokens(input_text) | ner_tokens(output)
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
