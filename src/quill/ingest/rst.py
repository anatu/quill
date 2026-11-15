"""Read a textbook kept as reStructuredText (Sphinx) into the block form the cleaner expects.

One .rst file under a chapter directory is one "post" (a section). Blocks carry text, kind
(p | li | oli | h | media), n, bq and link_share, as ingest/collabfund.py produces. Figures, tables,
code and display maths become `media` blocks, so the chunker can leave a gap marker where one was.
Sidebars and admonitions are asides in another voice and are skipped.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

UNDERLINE = re.compile(r"^([=\-~^\"'`#*+:.])\1{2,}\s*$")
DIRECTIVE = re.compile(r"^\.\.\s+([A-Za-z][\w:-]*)::\s*(.*)$")
LABEL = re.compile(r"^\.\.\s+_([^:]+):\s*$")
BULLET = re.compile(r"^([-*+•])\s+(.*)$")
ENUM = re.compile(r"^(\d+|#)[.)]\s+(.*)$")
MEDIA = {"figure", "image", "code-block", "code", "sourcecode", "literalinclude", "math", "table", "csv-table",
         "list-table", "parsed-literal", "graphviz", "raw"}
ASIDE = {"sidebar", "admonition", "note", "warning", "tip", "important", "topic", "epigraph", "pull-quote",
         "highlights", "container", "only", "toctree", "contents", "include", "index", "rubric", "role", "todo"}
ROLE_TEXT = re.compile(r":[a-zA-Z][\w:-]*:`([^`<]*?)\s*(?:<[^`>]*>)?`")     # :ref:`text <label>` -> text
NUMREF = re.compile(r":numref:`(\w+)\s+%s\s*<([^`>]+)>`")                   # :numref:`Figure %s <fig-x>`
LINK = re.compile(r"`([^`<]+?)\s*<[^`>]+>`__?")
SUBST = re.compile(r"\|[A-Za-z][\w -]*\|")


def inline(text: str, numbers: dict[str, int]) -> str:
    """Strip inline markup. Figure and table references get a number, stable within the section."""
    def ref(m):
        return f"{m.group(1)} {numbers.setdefault(m.group(2).strip().lower(), len(numbers) + 1)}"

    t = NUMREF.sub(ref, text)
    t = ROLE_TEXT.sub(lambda m: m.group(1).strip() or "", t)
    t = LINK.sub(r"\1", t)
    t = re.sub(r"``([^`]+)``", r"\1", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"\1", t)
    t = re.sub(r"`([^`]+)`_*", r"\1", t)
    t = SUBST.sub("", t)
    t = re.sub(r"\[#?\w*\]_", "", t)                    # footnote and citation marks
    return re.sub(r"\s+", " ", t.replace("\\ ", "")).strip()


def read_section(text: str) -> dict:
    """Parse one section file. Returns title and blocks."""
    lines = text.replace("\t", "    ").split("\n")
    blocks, numbers, title = [], {}, ""
    i, n = 0, len(lines)

    def add(kind, txt="", num=None):
        if kind == "media":
            if blocks and blocks[-1]["kind"] == "media":
                return                                   # one gap for a run of figures or code
            blocks.append(dict(text="", kind="media", n=None, bq=False, link_share=0.0))
            return
        txt = inline(txt, numbers)
        if txt:
            blocks.append(dict(text=txt, kind=kind, n=num, bq=False, link_share=0.0))

    def skip_indented(j):
        while j < n and (not lines[j].strip() or lines[j].startswith(" ")):
            j += 1
        return j

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if LABEL.match(line):
            i += 1
            continue
        d = DIRECTIVE.match(line)
        if d:
            name = d.group(1).lower()
            if name in MEDIA or name.startswith("_"):
                add("media")
            i = skip_indented(i + 1)
            continue
        if line.startswith(".. "):                       # comment or unknown explicit markup
            i = skip_indented(i + 1)
            continue
        if UNDERLINE.match(line):                        # overline or stray rule
            i += 1
            continue
        if i + 1 < n and UNDERLINE.match(lines[i + 1]) and not line.startswith(" "):
            head = inline(re.sub(r"^\d+(\.\d+)*\s+", "", line.strip()), numbers)
            title = title or head
            add("h", head)
            i += 2
            continue
        if line.startswith(("+-", "|")) or re.match(r"^=+(\s+=+)+\s*$", line):      # table or line block
            add("media")
            while i < n and lines[i].strip():
                i += 1
            continue
        m = BULLET.match(line) or ENUM.match(line)
        if m:
            kind = "li" if BULLET.match(line) else "oli"
            num = int(m.group(1)) if kind == "oli" and m.group(1).isdigit() else None
            buf = [m.group(2)]
            i += 1
            while i < n and lines[i].strip() and lines[i].startswith(" "):
                buf.append(lines[i].strip())
                i += 1
            add(kind, " ".join(buf), num)
            continue
        if line.startswith(" "):                         # indented block outside a directive: literal or quote
            add("media")
            i = skip_indented(i)
            continue
        buf = []
        while i < n and lines[i].strip() and not lines[i].startswith((" ", ".. ")) \
                and not (i + 1 < n and UNDERLINE.match(lines[i + 1])):      # a wrapped line may begin "- 300 Hz"
            buf.append(lines[i].strip())
            i += 1
        para = " ".join(buf)
        literal = para.endswith("::")
        if para != "::":
            add("p", re.sub(r"\s*::$", ":", para) if literal else para)
        if literal:
            add("media")
            i = skip_indented(i)
    return dict(title=title, blocks=blocks)


def read_posts(raw_dir: Path, author: str, url: str = "") -> list[dict]:
    """Every section file one level down (chapter/section.rst). Top-level files are front matter."""
    root = Path(raw_dir)
    posts = []
    for f in sorted(root.glob("*/*.rst")):
        if f.parent.name.startswith((".", "_")):
            continue
        sec = read_section(f.read_text(encoding="utf-8", errors="replace"))
        rel = f.relative_to(root).as_posix()
        posts.append(dict(title=sec["title"], url=f"{url.rstrip('/')}/{rel}" if url else rel, date=None, author=author,
                          blocks=sec["blocks"], hrefs=[], file=rel,
                          fetched=time.strftime("%Y-%m-%d", time.localtime(f.stat().st_mtime))))
    return posts
