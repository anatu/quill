"""Shared text extraction, passage splitting and stylometrics (stdlib only).

Ported unchanged from the 2026-11-08 similarity pass
(~/.quill/research/2026-11-08/simpass/scripts/textlib.py) so Phase 0 counts
reproduce. Phase 1 replaces the extraction rules with tested ones.
"""
import re, html, math, statistics, collections
from html.parser import HTMLParser

# ---------------------------------------------------------------- HTML extraction
SKIP_TAGS = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'noscript', 'svg',
             'button', 'select', 'textarea', 'iframe', 'figure', 'figcaption', 'table', 'code', 'pre'}
SKIP_ATTR = re.compile(
    r'(^|[\s_-])(comments?|commentlist|respond|sidebar|widgets?|related|share|sharing|social|footer|'
    r'newsletter|subscribe|subscription|signup|sign-up|optin|opt-in|byline|author-?bio|author-box|'
    r'about-author|post-?meta|entry-?meta|meta-bottom-row|breadcrumbs?|menu|navigation|navbar|popup|modal|cookie|'
    r'disclaimer|disclosure|tags|categories|pagination|nav-links|post-footer|card|supascribe|'
    r'jp-relatedposts|sharedaddy|wp-block-buttons|cta|promo|advert|ads?|sponsor|toc|'
    r'table-of-contents|wp-caption|caption|footnotes?|post-navigation|yarpp|mc4wp|convertkit|ck_form|'
    r'beehiiv-embed|subscribe-widget|share-bar|post__sidebar|post__share|article-info-bar|tooltip)($|[\s_-])',
    re.I)
LAYOUT = re.compile(r'^(content|site|main|page|wrap|inner|container|layout|body)', re.I)
VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'wbr', 'area', 'base', 'col', 'embed', 'param', 'track'}
PTAGS = ('p', 'li')
CONTAINERS = {'div', 'section', 'article', 'main', 'body', 'td', 'ul', 'ol'}


class Extractor(HTMLParser):
    """Collect p/li paragraphs with: in-blockquote flag, link-text share, container path."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, skip, cid)
        self.skip = 0
        self.bq = 0
        self.pdepth = 0
        self.buf = []
        self.abuf = []
        self.in_a = 0
        self.paras = []  # dict(text, bq, link_share, path)
        self.cid = 0
        self.title = ''
        self._in_title = False

    def _path(self):
        return tuple(x[2] for x in self.stack if x[0] in CONTAINERS)

    def handle_starttag(self, t, attrs):
        if t == 'title':
            self._in_title = True
        if t in VOID:
            if t == 'br' and self.pdepth:
                self.buf.append('\n')
            return
        a = dict(attrs)
        cls = (a.get('class') or '') + ' ' + (a.get('id') or '')
        sk = (t in SKIP_TAGS) or a.get('aria-hidden') == 'true' or (t not in ('html', 'body', 'main', 'article') and any(
            SKIP_ATTR.search(tok) for tok in cls.split()) and not any(LAYOUT.match(tok) for tok in cls.split()))
        if t == 'p' and self.pdepth:  # implicit close of an unclosed <p>
            self._flush()
        self.cid += 1
        self.stack.append((t, sk, self.cid, cls.strip()[:100]))
        if sk:
            self.skip += 1
        if t == 'blockquote':
            self.bq += 1
        if t in PTAGS:
            if self.pdepth and t == 'li':
                self._flush()
            self.pdepth += 1
            self.buf, self.abuf = [], []
        if t == 'a':
            self.in_a += 1

    def _flush(self):
        txt = re.sub(r'[ \t\r\f\v]+', ' ', ''.join(self.buf))
        txt = re.sub(r'\s*\n\s*', ' ', txt).strip()
        if txt and not self.skip:
            atxt = re.sub(r'\s+', ' ', ''.join(self.abuf)).strip()
            self.paras.append(dict(text=txt, bq=self.bq > 0, link_share=len(atxt) / max(1, len(txt)),
                                   path=self._path()))
        self.buf, self.abuf = [], []

    def handle_endtag(self, t):
        if t == 'title':
            self._in_title = False
        if t in VOID:
            return
        if not any(x[0] == t for x in self.stack):
            return
        while self.stack:
            tag, sk, c, _cls = self.stack.pop()
            if tag in PTAGS and self.pdepth:
                self._flush()
                self.pdepth -= 1
            if sk:
                self.skip -= 1
            if tag == 'blockquote':
                self.bq -= 1
            if tag == 'a':
                self.in_a = max(0, self.in_a - 1)
            if tag == t:
                break

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self.pdepth and not self.skip:
            self.buf.append(d)
            if self.in_a:
                self.abuf.append(d)


BOILER = re.compile(
    r'^(further reading|related|subscribe|sign up|share this|follow (me|us)|listen|watch|source[s]?:|'
    r'disclosure|disclaimer|this content|comments?\b|leave a|copyright|©|all rights reserved|posted in|'
    r'filed under|tags?:|read more|click here|image:|photo:|chart:|via |h/t|hat tip|note:|footnotes?|'
    r'image credit|photo credit|thanks for reading|if you enjoyed|join \d|get the|download|register|'
    r'order (my|the) book|buy (my|the) book|my new book|pre-?order|reply|share$|tweet|email|print|'
    r'you may also like|recommended|sponsored|advertisement|previous post|next post|older post|newer post|'
    r'the post .* appeared first|this post was originally|originally published|this article was originally|'
    r'\*\*?disclaimer|the compound|animal spirits|ritholtz wealth|nothing on this blog)', re.I)


def clean_paras(paras, min_words=1):
    out = []
    for p in paras:
        t = p['text']
        t = re.sub(r'\[\d+\]|\[\w\]', '', t)          # footnote markers
        t = re.sub(r'\s+', ' ', t).strip()
        if not t:
            continue
        w = len(t.split())
        if p.get('bq'):
            continue
        if p.get('link_share', 0) > 0.6 and w < 40:
            continue
        if BOILER.search(t) and w < 40:
            continue
        if re.match(r'^(source|sources|chart|data|image)\b', t, re.I):
            continue
        if w < min_words or not re.search(r'[A-Za-z]', t):
            continue
        out.append(t)
    return out


def main_container(paras):
    """Return paras inside the deepest container that holds >=70% of all paragraph words."""
    if not paras:
        return paras
    tot = sum(len(p['text'].split()) for p in paras)
    cw = collections.Counter()
    for p in paras:
        w = len(p['text'].split())
        for i in range(len(p['path'])):
            cw[p['path'][:i + 1]] += w
    best = ()
    for path, w in cw.items():
        if w >= 0.7 * tot and len(path) > len(best):
            best = path
    return [p for p in paras if p['path'][:len(best)] == best]


def extract_html(h):
    e = Extractor()
    try:
        e.feed(h)
        e.close()
    except Exception:
        pass
    paras = [p for p in e.paras]
    paras = main_container(paras)
    return html.unescape(e.title).strip(), paras


def meta_year(h, url=''):
    for pat in [r'article:published_time"\s+content="(\d{4})', r'"datePublished"\s*:\s*"(\d{4})',
                r'<time[^>]+datetime="(\d{4})', r'"published_at"\s*:\s*"(\d{4})', r'"publish_date"\s*:\s*"(\d{4})']:
        m = re.search(pat, h)
        if m:
            return int(m.group(1))
    m = re.search(r'/(20\d\d|19\d\d)/', url)
    if m:
        return int(m.group(1))
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)'
                  r'\s+\d{1,2},\s+((?:19|20)\d\d)', h)
    return int(m.group(2)) if m else None


def meta_author(h):
    for pat in [r'<meta\s+name="author"\s+content="([^"]+)"', r'"author"\s*:\s*\{\s*"@type"\s*:\s*"Person"\s*,\s*"name"\s*:\s*"([^"]+)"',
                r'"author"\s*:\s*\[\s*\{[^}]*?"name"\s*:\s*"([^"]+)"', r'<meta\s+name="twitter:data1"\s+content="([^"]+)"',
                r'rel="author"[^>]*>([^<]+)<']:
        m = re.search(pat, h)
        if m:
            return html.unescape(m.group(1)).strip()
    return None


# ---------------------------------------------------------------- plain-text (pre / pdf) paragraphs
def text_paragraphs(txt):
    """Split plain text into paragraphs on blank lines; join wrapped lines; drop tables/headers."""
    txt = txt.replace('\r', '').replace('\f', '\n\n')
    blocks = re.split(r'\n\s*\n', txt)
    out = []
    for b in blocks:
        lines = [l for l in b.split('\n')]
        # drop table-like lines: many runs of 2+ spaces, or mostly digits/punctuation
        keep = []
        for l in lines:
            s = l.strip()
            if not s:
                continue
            alpha = sum(ch.isalpha() for ch in s)
            if alpha < 0.55 * len(s):
                continue
            if len(re.findall(r'\S {3,}\S', l)) >= 2:
                continue
            if re.search(r'\.{4,}', s):
                continue
            keep.append(s)
        if not keep:
            continue
        p = ' '.join(keep)
        p = re.sub(r'(\w)- (\w)', r'\1\2', p)  # de-hyphenate line breaks
        p = re.sub(r'\s+', ' ', p).strip()
        if len(p.split()) < 4:
            continue
        if not re.search(r'[.!?:;"\')]$', p) and len(p.split()) < 12:   # headings
            continue
        out.append(p)
    return out


# ---------------------------------------------------------------- passages
def make_passages(posts, lo=250, hi=350, hard=450, carry=True):
    """posts: list of dict(id, paras). Returns list of dict(group, text, paras).
    Paragraph boundaries are kept. A paragraph longer than `hard` words is split at sentence boundaries.
    Post remainders < lo words are carried into the next post's buffer when carry=True."""
    out = []
    buf, bufw, group = [], 0, None

    def emit():
        nonlocal buf, bufw, group
        if buf:
            out.append(dict(group=group, paras=list(buf), text='\n\n'.join(buf), words=bufw))
        buf, bufw, group = [], 0, None

    for post in posts:
        paras = []
        for p in post['paras']:
            w = len(p.split())
            if w > hard:
                sents = split_sentences(p)
                cur, cw = [], 0
                for s in sents:
                    sw = len(s.split())
                    if cw + sw > hi and cw >= lo * 0.6:
                        paras.append(' '.join(cur)); cur, cw = [], 0
                    cur.append(s); cw += sw
                if cur:
                    paras.append(' '.join(cur))
            else:
                paras.append(p)
        if not carry:
            emit()
        for p in paras:
            w = len(p.split())
            if group is None:
                group = post['id']
            if bufw >= lo and bufw + w > hi:
                emit()
                group = post['id']
            buf.append(p); bufw += w
            if bufw >= hi:
                emit()
        if bufw >= lo:
            emit()
        elif not carry:
            if bufw >= 150:
                emit()
            else:
                buf, bufw, group = [], 0, None
    if bufw >= 150:
        emit()
    return out


# ---------------------------------------------------------------- stylometrics
ABBR = r'(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e|U\.S|U\.K|Inc|Co|Corp|Ltd|No|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|Gen|Gov|Sen|Rep|Mt|approx|cf|al)'
_SENT = re.compile(r'(?<=[.!?])["\'”’)\]]*\s+(?=["\'“‘(\[]*[A-Z0-9])')


def split_sentences(p):
    p = p.strip()
    if not p:
        return []
    prot = re.sub(r'\b(' + ABBR + r')\.', lambda m: m.group(1) + '<DOT>', p)
    prot = re.sub(r'\b([A-Z])\.(?=\s?[A-Z]\.?)', r'\1<DOT>', prot)  # initials
    prot = re.sub(r'(\d)\.(\d)', r'\1<DOT>\2', prot)
    parts = _SENT.split(prot)
    return [x.replace('<DOT>', '.').strip() for x in parts if x.strip()]


WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")


def words(t):
    return [w.lower().replace('’', "'") for w in WORD.findall(t)]


FPS = {'i', 'me', 'my', 'mine', 'myself', "i'm", "i've", "i'd", "i'll"}
SP = {'you', 'your', 'yours', 'yourself', 'yourselves', "you're", "you've", "you'd", "you'll", "y'all"}


def stylometrics(paragraphs_lists):
    """paragraphs_lists: list of passages, each a list of paragraph strings."""
    sent_lens, para_words, one_sent, n_paras = [], [], 0, 0
    q = ex = 0
    toks = []
    text_all = []
    for paras in paragraphs_lists:
        for p in paras:
            ss = split_sentences(p)
            if not ss:
                continue
            n_paras += 1
            pw = len(words(p))
            para_words.append(pw)
            if len(ss) == 1:
                one_sent += 1
            for s in ss:
                sl = len(words(s))
                if sl == 0:
                    continue
                sent_lens.append(sl)
                s2 = s.rstrip('"\'”’)] ')
                if s2.endswith('?'):
                    q += 1
                elif s2.endswith('!'):
                    ex += 1
            toks += words(p)
            text_all.append(p)
    T = '\n'.join(text_all)
    nw = max(1, len(toks))
    ns = max(1, len(sent_lens))
    k = 1000.0 / nw
    emd = T.count('—') + len(re.findall(r'(?<=\w) ?-- ?(?=\w)', T)) + len(re.findall(r' – ', T))
    colons = len(re.findall(r':(?!\d)', T)) - len(re.findall(r'https?:', T))
    return dict(
        n_words=len(toks), n_sents=len(sent_lens), n_paras=n_paras,
        sent_len_mean=statistics.mean(sent_lens) if sent_lens else float('nan'),
        sent_len_sd=statistics.pstdev(sent_lens) if len(sent_lens) > 1 else float('nan'),
        words_per_para=statistics.mean(para_words) if para_words else float('nan'),
        one_sent_para_share=one_sent / max(1, n_paras),
        question_per_100s=100.0 * q / ns, exclam_per_100s=100.0 * ex / ns,
        fps_per_1k=k * sum(1 for w in toks if w in FPS),
        sp_per_1k=k * sum(1 for w in toks if w in SP),
        emdash_per_1k=k * emd, semicolon_per_1k=k * T.count(';'),
        colon_per_1k=k * max(0, colons), paren_per_1k=k * T.count('('),
        mattr500=mattr(toks, 500),
    )


def mattr(toks, w=500):
    n = len(toks)
    if n < w:
        return len(set(toks)) / max(1, n)
    c = collections.Counter(toks[:w])
    tot = len(c)
    s = tot
    for i in range(w, n):
        out_t, in_t = toks[i - w], toks[i]
        c[out_t] -= 1
        if c[out_t] == 0:
            del c[out_t]
        c[in_t] += 1
        s += len(c)
    return s / (n - w + 1) / w   # mean type/token ratio over all windows of w tokens


def rel_freqs(passage_texts, vocab):
    c = collections.Counter()
    n = 0
    for t in passage_texts:
        ws = words(t)
        c.update(ws)
        n += len(ws)
    return [c[v] / max(1, n) for v in vocab], n
