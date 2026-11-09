"""Light PII pass: email addresses and phone numbers only. Hits are reviewed, never auto-removed."""
from __future__ import annotations

import re

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
# North American and international forms; needs separators or a + so plain numbers (years, dollars) pass
PHONE = re.compile(r"(?<![\d$.,])(?:\+\d{1,3}[\s.-]?)?(?:\(\d{3}\)\s?|\d{3}[\s.-])\d{3}[\s.-]\d{4}(?![\d,])"
                   r"|(?<![\d$.,])\+\d{1,3}(?:[\s.-]?\d{2,4}){2,4}(?![\d,])")


def find(text: str) -> list[dict]:
    hits = [dict(kind="email", match=m.group(0), start=m.start()) for m in EMAIL.finditer(text)]
    hits += [dict(kind="phone", match=m.group(0), start=m.start()) for m in PHONE.finditer(text)]
    return sorted(hits, key=lambda h: h["start"])
