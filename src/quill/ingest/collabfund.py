"""Read Collab Fund blog pages into posts.

Raw pages are untrusted input. They are parsed with the stdlib HTML parser only.

Two readers live here:
  load_posts  the Phase 0 reader (generic textlib rules). `quill audit` uses it to
              reproduce the 2026-11-08 figures. Do not change it.
  read_page / read_posts  the Phase 1 reader, built for the Collab Fund page layout.
"""
from __future__ import annotations

import html as htmllib
import re
import time
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from . import textlib as T

# ------------------------------------------------------------------ Phase 0 (frozen)


def _norm(t: str) -> str:
    return re.sub(r"\W+", " ", t.lower()).strip()


def dedupe_boiler(posts: list[dict]) -> list[str]:
    """Drop paragraphs repeated across >= max(3, 10%) of posts. Returns removed paragraphs."""
    cnt = Counter()
    for p in posts:
        for t in {_norm(x) for x in p["paras"]}:
            cnt[t] += 1
    thr = max(3, int(0.1 * len(posts)))
    rep = {t for t, c in cnt.items() if c >= thr and t}
    for p in posts:
        p["paras"] = [x for x in p["paras"] if _norm(x) not in rep]
    return sorted(rep)


def load_posts(raw_dir: Path) -> tuple[list[dict], list[str]]:
    """Return (posts, removed_boilerplate). Each post: file, title, year, paras, words, quote_words."""
    pages = sorted((raw_dir / "pages").glob("*.html"))
    posts = []
    for f in pages:
        h = f.read_text(encoding="utf-8", errors="replace")
        title, paras = T.extract_html(h)
        quote_words = sum(len(p["text"].split()) for p in paras if p.get("bq"))
        posts.append(dict(file=f.name, title=title, year=T.meta_year(h), author=T.meta_author(h),
                          paras=T.clean_paras(paras), quote_words=quote_words))
    removed = dedupe_boiler(posts)
    for p in posts:
        p["words"] = sum(len(x.split()) for x in p["paras"])
    return posts, removed


# ------------------------------------------------------------------ Phase 1 reader

TITLE_SUFFIX = re.compile(r"\s*·\s*Collaborative Fund\s*$")
BODY_CLASS = re.compile(r"(^|\s)longform(\s|$)")          # section.longform and section.post__intro.longform
SKIP_CLASS = re.compile(
    r"(^|[\s_-])(post__sidebar|sidebar|newsletter|subscribe|share|share-bar|share-container|"
    r"article-info-bar|tooltip|caption|byline|post__meta|footnotes?|related|more-posts|"
    r"twitter-tweet|instagram-media|promo|cta)($|[\s_-])", re.I)
SKIP_TAGS = {"script", "style", "noscript", "svg", "button", "select", "textarea", "iframe", "video", "audio",
             "figure", "figcaption", "table", "form", "nav", "header", "footer", "aside"}
VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr", "area", "base", "col", "embed", "param",
        "track"}
MEDIA = {"img", "figure", "iframe", "video", "table"}       # leave a marker so chunks can flag the gap
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "pre"}
BREAKERS = {"div", "section", "article", "ul", "ol", "blockquote", "hr"}   # end any open implicit block
CODE_TOKEN = "<CODE>"


class PageParser(HTMLParser):
    """Collect body blocks of one Collab Fund post.

    Each block: text, kind (p | li | oli | h | code | media), n (ordered-list number), bq (inside a
    block quote), link_share (share of characters inside links).
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool, bool]] = []   # (tag, opens_skip, opens_body)
        self.body = 0
        self.skip = 0
        self.bq = 0
        self.in_a = 0
        self.code = 0
        self.lists: list[list] = []        # [tag, counter]
        self.open: dict | None = None      # block being filled
        self.blocks: list[dict] = []
        self.hrefs: list[str] = []         # every link target in the body, block quotes included
        self.title = ""
        self._in_title = False

    # -- block handling
    def _start(self, kind: str, n: int | None = None):
        self._flush()
        self.open = dict(kind=kind, n=n, buf=[], abuf=[])

    def _flush(self):
        b, self.open = self.open, None
        if not b:
            return
        txt = re.sub(r"\s+", " ", "".join(b["buf"])).strip()
        if not txt:
            return
        atxt = re.sub(r"\s+", " ", "".join(b["abuf"])).strip()
        self.blocks.append(dict(text=txt, kind=b["kind"], n=b["n"], bq=self.bq > 0,
                                link_share=len(atxt) / max(1, len(txt))))

    def _media(self):
        self._flush()
        self.blocks.append(dict(text="", kind="media", n=None, bq=self.bq > 0, link_share=0.0))

    # -- parser events
    def handle_starttag(self, t, attrs):
        if t == "title":
            self._in_title = True
        a = dict(attrs)
        if t in VOID:
            if self.body and not self.skip:
                if t == "br" and self.open:
                    self.open["buf"].append(" ")
                elif t == "hr":
                    self._flush()
                elif t == "img":
                    self._media()
            return
        cls = (a.get("class") or "") + " " + (a.get("id") or "")
        opens_body = t == "section" and bool(BODY_CLASS.search(a.get("class") or ""))
        sk = t in SKIP_TAGS or a.get("aria-hidden") == "true" or bool(SKIP_CLASS.search(cls))
        self.stack.append((t, sk, opens_body))
        if opens_body:
            self.body += 1
        if sk:
            if self.body and not self.skip:
                if t in MEDIA:
                    self._media()
                elif re.search(r"twitter-tweet|instagram-media", cls):
                    self._media()                       # an embedded post: someone else's words
                    self.blocks[-1]["bq"] = True
                else:
                    self._flush()
            self.skip += 1
        if not self.body or self.skip:
            return
        if t == "blockquote":
            self._flush()
            self.bq += 1
        elif t in ("ul", "ol"):
            self._flush()
            self.lists.append([t, 0])
        elif t in BREAKERS:
            self._flush()
        elif t == "li":
            n = None
            if self.lists:
                self.lists[-1][1] += 1
                if self.lists[-1][0] == "ol":
                    n = self.lists[-1][1]
            self._start("oli" if n else "li", n)
        elif t == "p":
            # a <p> inside an open <li> continues the item; otherwise it starts a paragraph
            if self.open and self.open["kind"] in ("li", "oli") and any(x[0] == "li" for x in self.stack[:-1]):
                self.open["buf"].append(" ")
            else:
                self._start("p")
        elif t == "pre":
            self._start("code")
        elif t in BLOCK:
            self._start("h")
        elif t == "code":
            self.code += 1
            if self.open and self.open["kind"] != "code":
                self.open["buf"].append(CODE_TOKEN)
        elif t == "a":
            self.in_a += 1
            if a.get("href"):
                self.hrefs.append(a["href"])

    def handle_endtag(self, t):
        if t == "title":
            self._in_title = False
        if t in VOID or not any(x[0] == t for x in self.stack):
            return
        while self.stack:
            tag, sk, opens_body = self.stack.pop()
            live = self.body and not self.skip
            if live:
                if tag in BLOCK or tag in BREAKERS:
                    if not (tag == "p" and self.open and self.open["kind"] in ("li", "oli")):
                        self._flush()
                if tag == "blockquote":
                    self.bq = max(0, self.bq - 1)
                elif tag in ("ul", "ol") and self.lists:
                    self.lists.pop()
                elif tag == "code":
                    self.code = max(0, self.code - 1)
                elif tag == "a":
                    self.in_a = max(0, self.in_a - 1)
            if sk:
                self.skip -= 1
            if opens_body:
                self._flush()
                self.body -= 1
            if tag == t:
                break

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if not self.body or self.skip:
            return
        if self.open is None:
            if not d.strip():
                return
            self._start("p")            # bare text outside any block
        if self.open["kind"] == "code":
            self.open["buf"] = [CODE_TOKEN]
            return
        if self.code:
            return                      # inline code already replaced by the token
        self.open["buf"].append(d)
        if self.in_a:
            self.open["abuf"].append(d)


def _meta(h: str, key: str) -> str | None:
    m = re.search(r'<meta[^>]+(?:property|name)="%s"[^>]+content="([^"]*)"' % re.escape(key), h)
    return htmllib.unescape(m.group(1)).strip() if m else None


def read_page(h: str) -> dict:
    """Parse one page. Returns title, url, date (ISO day or None), author, blocks, hrefs."""
    p = PageParser()
    try:
        p.feed(h)
        p.close()
        p._flush()
    except Exception:       # malformed page: keep what was parsed
        pass
    date = _meta(h, "article:published_time")
    if not date:
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', h)
        date = m.group(1) if m else None
    title = _meta(h, "og:title") or TITLE_SUFFIX.sub("", htmllib.unescape(p.title).strip())
    return dict(title=TITLE_SUFFIX.sub("", title).strip(), url=_meta(h, "og:url"),
                date=date[:10] if date else None, author=_meta(h, "author") or T.meta_author(h),
                blocks=p.blocks, hrefs=p.hrefs)


def read_posts(raw_dir: Path) -> list[dict]:
    """Read every page under raw_dir/pages. Adds file and fetched (file mtime, ISO day)."""
    posts = []
    for f in sorted((Path(raw_dir) / "pages").glob("*.html")):
        post = read_page(f.read_text(encoding="utf-8", errors="replace"))
        post["file"] = f.name
        post["fetched"] = time.strftime("%Y-%m-%d", time.localtime(f.stat().st_mtime))
        posts.append(post)
    return posts
