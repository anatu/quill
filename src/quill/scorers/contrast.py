""""Not X, but Y" contrast detector.

Port of the ten stage-1 surface regexes from slop-score (js/regexes-stage1.js,
Copyright (c) 2025 Sam Paech, MIT License, https://github.com/sam-paech/slop-score).
The 35 POS-tagged stage-2 patterns are not ported: they need a tagger and target fiction dialogue.
Overlapping matches merge into one hit, as in the original contrast-detector.js.
"""
from __future__ import annotations

import re

MAXG = 160
PRON = r"(?:it|they|this|that)"
BE = r"(?:is|are|was|were)"
BE_NEG = r"(?:is\s+not|are\s+not|was\s+not|were\s+not|isn't|aren't|wasn't|weren't|ain't)"
START = r"(?:(?<=^)|(?<=[.?!]\s))"
Q = "[\"“”']?"

_RAW = {
    "not_but": (
        rf"\b(?:(?:{BE_NEG})|not(?!\s+(?:that|only)\b))\s+(?:(?!\bbut\b|[.?!]).){{1,100}}?[,;:]\s*but\s+"
        r"(?!when\b|while\b|which\b|who\b|whom\b|whose\b|where\b|if\b|that\b|as\b|because\b|although\b|though\b|"
        r"till\b|until\b|unless\b|here\b|there\b|then\b|my\b|we\b|I\b|you\b|it\s+seems\b|it\s+appears\b|"
        r"it\s+felt\b|it\s+looks?\b|anything\b)"),
    "not_dash": (
        rf"\b(?:\w+n't|not)\s+(?:just|only|merely)?\s+(?:(?![.?!]).){{1,{MAXG}}}?(?:-|\s-\s|[—–])\s*"
        rf"{PRON}\s+(?:(?:'re|are|'s|is|were|was)\b|(?!'re|are|'s|is|were|was)[*_~]*[a-z]\w*)"),
    "pron_be_not_sep_be": (
        rf"{START}\s*{Q}(?:(?:{PRON}\s+{BE}\s+not)|(?:{PRON}\s+{BE}n't)|(?:it's|they're|that's)\s+not)\b"
        rf"[^.?!]{{0,{MAXG}}}[.;:?!]\s*{Q}{PRON}\s+(?:{BE}|(?:'s|'re))\b(?!\s+not\b)"),
    "np_be_not_sep_they_be": (
        rf"{START}\s*(?![^.?!]{{0,80}}\b(?:knew|know|thought|think|said|says|told|heard|learned)\b[^.?!]{{0,40}}?"
        rf"\bthat\b)(?!\s*not\s+without\b)(?![^.?!]{{0,50}}\bnot\s+put\b)[^.?!]{{0,{MAXG}}}?\b(?:{BE_NEG})\b"
        rf"[^.?!]{{0,{MAXG}}}[.;:?!]\s*{Q}{PRON}\b(?:'re|\s+(?:are|were|is|was))\b(?!\s+not\b)"),
    "no_longer": (
        rf"{START}\s*[^.?!]{{0,{MAXG}}}\bno\s+longer\b[^.;:?!]{{0,{MAXG}}}[.;:?!]\s*(?:it|they|this|that)\s+"
        r"(?:is|are|was|were)\b(?!\s+not\b)"),
    "not_just_sep": (
        rf"{START}\s*{Q}{PRON}\b(?:'s|'re|\s+(?:is|are|was|were))?\s+not\s+just\b[^.?!]{{0,{MAXG}}}[.?!]\s*{Q}"
        rf"{PRON}\b(?:'s|'re|\s+(?:is|are|was|were))\b(?!\s+not\b)"),
    "not_period_sameverb": (
        rf"{START}[^.?!]*?\b(?:do|does|did)n't\b\s+(?:(?:\w+\s+){{0,2}})([a-z]{{3,}})\b[^.?!]*[.?!]\s*"
        rf"{PRON}\s+\1(?:ed|es|s|ing)?\b"),
    "simple_be_not_it_be": (
        rf"{START}\s*{Q}(?!he\b|she\b|i\b|you\b|we\b)(?![^.?!]{{0,80}}\b(?:knew|know|thought|think|said|says|told|"
        rf"heard|learned)\b[^.?!]{{0,40}}?\bthat\b)[^.?!]{{0,{MAXG}}}?\b{BE_NEG}\b[^.?!]{{0,{MAXG}}}[.;:?!]\s*"
        rf"{Q}it(?:'s|\s+(?:is|are|was|were))\b"),
    "embedded_not_just_sep": (
        rf"{START}[^.?!]{{0,80}}?\b(?:(?:it|they)\s+(?:is|are)|(?:it's|they're))\s+not\s+just\b"
        rf"[^.?!]{{0,{MAXG}}}[.?!]\s*(?:(?:it|they)\s+(?:is|are)|(?:it's|they're))\b"),
    "dialogue_not_just": (
        rf"{Q}{PRON}(?:'re|'s|\s+(?:are|is|was|were))\s+not\s+just\b[^\"“”']{{0,{MAXG}}}{Q}\s*"
        r"(?:[^.?!]{0,80}\b(?:said|asked|whispered|muttered|replied|added|shouted|cried)\b[^.?!]{0,80}[.?!]\s*)?"
        rf"{Q}{PRON}(?:'re|'s|\s+(?:are|is|was|were))\s+[*_~]?[a-z]\w*"),
}
REGEXES = {k: re.compile(v, re.I | re.M) for k, v in _RAW.items()}


def find(text: str) -> list[tuple[int, int]]:
    """Merged (start, end) spans of contrast constructions."""
    t = text.replace("’", "'")
    spans = sorted((m.start(), m.end()) for rx in REGEXES.values() for m in rx.finditer(t))
    out: list[list[int]] = []
    for lo, hi in spans:
        if out and lo <= out[-1][1]:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return [(a, b) for a, b in out]


def count(text: str) -> int:
    return len(find(text))
