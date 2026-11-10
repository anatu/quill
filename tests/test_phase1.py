"""Phase 1: extraction, cleaning, dedupe, chunking, lexicon, AI-text check, gate.

Cases 1-8 come from tests/cases/phase0_extraction.md. All text here is synthetic.
"""
import json
import os

import numpy as np
import pytest
import yaml

from quill import config
from quill.clean import ai_check, boilerplate, chunk, dedupe, pii_regex
from quill.clean.twins import find_twins, split_groups
from quill.corpus import build, gate, store
from quill.ingest.collabfund import read_page
from quill.scorers import contrast
from quill.scorers.lexicon import Lexicon, inflect

SENT = "This is one plain sentence of the essay body that says something. "


def page(body: str, title: str = "A Post", author: str = "Morgan Housel", date: str = "2019-05-01",
         intro: str = "") -> str:
    intro = f'<section class="post__intro longform container"><p>{intro}</p></section>' if intro else ""
    return f"""<html><head><title>{title} · Collaborative Fund</title>
<meta property="og:title" content="{title}" /><meta name="author" content="{author}" />
<meta property="og:url" content="https://collabfund.com/blog/x/" />
<meta property="article:published_time" content="{date}T09:00:00-05:00" /></head><body>
<header><nav><ul><li><a href="/">Home</a></li></ul></nav></header>
<article class="post post--blog"><div class="page-cover"><h1>{title}</h1></div>
<div class="post__meta"><time>May 1</time><h3>Share</h3><ul class="share"><li><div class="linkto">Copy Link</div></li></ul></div>
{intro}<section class="longform drop container">
<div class="post__sidebar"><section class="newsletter"><h3>Sign up for more Collab Fund content</h3>
<p>Subscribe to our newsletter</p></section></div>
{body}
</section><footer class="post__footer"><section class="newsletter"><p>Subscribe</p></section></footer></article>
<section class="more-posts"><h3 class="card__title">Another post</h3><p class="card__excerpt">Teaser text</p></section>
<footer class="footer"><p>© Collaborative Fund</p></footer></body></html>"""


def texts(body: str, **kw) -> list[str]:
    kept, _ = boilerplate.clean_post(read_page(page(body, **kw))["blocks"])
    return [b["text"] for b in kept]


def reasons(body: str) -> dict:
    _, dropped = boilerplate.clean_post(read_page(page(body))["blocks"])
    return {d["text"]: d["reason"] for d in dropped}


# ---------------------------------------------------------------- extraction and furniture

def test_metadata_and_title_suffix():
    p = read_page(page("<p>Body.</p>", title="Same as Ever"))
    assert (p["title"], p["date"], p["author"]) == ("Same as Ever", "2019-05-01", "Morgan Housel")
    assert p["url"] == "https://collabfund.com/blog/x/"


def test_chrome_outside_the_body_never_enters():
    out = texts("<p>First own paragraph.</p><p>Second own paragraph.</p>", intro="The intro line.")
    assert out == ["The intro line.", "First own paragraph.", "Second own paragraph."]


def test_blockquote_is_dropped_and_leaves_a_gap_mark():
    blocks = read_page(page("<p>He wrote:</p><blockquote><p>Someone else's words here.</p></blockquote>"
                            "<p>– Niall Ferguson</p><p>My view follows.</p>"))["blocks"]
    kept, dropped = boilerplate.clean_post(blocks)
    assert [b["text"] for b in kept] == ["He wrote:", "My view follows."]
    assert kept[0]["gaps"] == {"quote"}
    assert {d["reason"] for d in dropped} == {"blockquote", "quote_attribution"}


def test_epigraph_goes_with_its_attribution():
    short = "<p>“History never repeats. Man does.”</p><p>– Voltaire</p><p>My view follows.</p>"
    bare = "<p>We are all children of earth; grant us that simple knowledge.</p><p>– FDR, 1942</p><p>My view follows.</p>"
    for body in (short, bare):
        kept, dropped = boilerplate.clean_post(read_page(page(body))["blocks"])
        assert [b["text"] for b in kept] == ["My view follows."]
        assert [d["reason"] for d in dropped] == ["inline_quote", "quote_attribution"]
    one = "<p>It’s a rare person who wants to hear it. —Richard Cavett</p><p>My view follows.</p><p>For more:</p>"
    kept, dropped = boilerplate.clean_post(read_page(page(one))["blocks"])
    assert [b["text"] for b in kept] == ["My view follows."] and len(dropped) == 2
    later = "<p>Opening.</p><p>My own line that runs on.</p><p>– and then a dash aside</p>"
    assert len(boilerplate.clean_post(read_page(page(later))["blocks"])[0]) == 3


def test_spot_check_leftovers_are_dropped():
    body = ("<p>My own closing line.</p><p>Bezos once explained:</p><p>You have to go back in time to 1994.</p>"
            "<p>The recession was caused by [x].</p><p><em>Collaborative Fund team members own shares in companies "
            "mentioned in this article.</em></p><p>You can download the report <a href='/r.pdf'>here</a>, or click "
            "the image below.</p><p>More:</p><ul><li><a href='/blog/a/'>Another Post Title</a></li></ul>")
    kept, dropped = boilerplate.clean_post(read_page(page(body))["blocks"], quotes=["You have to go back"])
    assert [b["text"] for b in kept] == ["My own closing line.", "Bezos once explained:", "The recession was caused by [x]."]
    assert kept[1]["gaps"] == {"quote"}
    assert sorted(d["reason"] for d in dropped) == ["inline_quote", "promo", "promo", "related_links", "related_links"]


def test_embedded_tweet_leaves_a_quote_gap():
    body = "<p>Craig explained:</p><blockquote class='twitter-tweet'><p>Do not hold on.</p></blockquote><p>After.</p>"
    kept, _ = boilerplate.clean_post(read_page(page(body))["blocks"])
    assert [b["text"] for b in kept] == ["Craig explained:", "After."] and kept[0]["gaps"] == {"quote"}


def test_image_leaves_a_media_gap():
    kept, _ = boilerplate.clean_post(read_page(page("<p>Here is the chart:</p><img src='c.png'><p>After.</p>"))["blocks"])
    assert kept[0]["gaps"] == {"media"} and "gaps" not in kept[1]


def test_whole_paragraph_quotes_go_but_dialogue_stays():
    q = "“The first rule of compounding is to never interrupt it unnecessarily.” – Munger"
    multi1 = "“This is the first paragraph of a long quotation that runs on."
    multi2 = "“And this second paragraph finally closes the long quotation.”"
    dialogue = "“Sell everything,” he said to the broker that morning. “Do it now.”"
    r = reasons(f"<p>{q}</p><p>{multi1}</p><p>{multi2}</p><p>{dialogue}</p>")
    assert r == {q: "inline_quote", multi1: "inline_quote", multi2: "inline_quote"}
    assert boilerplate.is_pure_quote(dialogue) is False


def test_promo_lines_go_but_book_mentions_stay():
    mention = "I highlighted a similar story in my book, The Psychology of Money."
    out = texts("<p>My book, The Psychology of Money, is now out.</p>"
                "<p>(<a href='x.pdf'>PDF version here</a>)</p>"
                f"<p>{mention}</p><p>For more, check out my book The Psychology of Money.</p>")
    assert out == [mention]


def test_related_links_go_but_linked_sentences_stay():
    linked = "<p><a href='/a'>Growth is complicated and size can be both the driver and the trigger.</a></p>"
    out = texts(f"<p>Opening.</p>{linked}<p>Closing thought.</p><p>More on this topic:</p>"
                "<ul><li><a href='/b'>Five Lessons From History</a></li><li><a href='/c'>Useful Hacks</a></li></ul>")
    assert out == ["Opening.", "Growth is complicated and size can be both the driver and the trigger.",
                   "Closing thought."]


def test_separators_go_but_numeric_one_liners_and_footnotes_stay():
    note = "* Nothing, and yet everything, about this post is accurate."
    out = texts(f"<p>How much will you remember?</p><p>80%?</p><p>***</p><hr><p>Text[1] here.</p><p>{note}</p>")
    assert out == ["How much will you remember?", "80%?", "Text here.", note]


def test_lists_keep_numbers_and_bullets():
    blocks = read_page(page("<p>1. A typed number stays.</p><ol><li>First item</li><li><p>Second item</p></li></ol>"
                            "<ul><li>A bullet</li></ul>"))["blocks"]
    kept, _ = boilerplate.clean_post(blocks)
    assert [chunk.render(b) for b in kept] == ["1. A typed number stays.", "1. First item", "2. Second item",
                                                "- A bullet"]


def test_inline_code_becomes_a_token():
    assert texts("<p>Run <code>pip install x</code> first.</p>") == ["Run <CODE> first."]


def test_link_targets_are_recorded():
    p = read_page(page("<p>See <a href='https://e.org/a?utm_source=chatgpt.com'>this</a>.</p>"))
    assert p["hrefs"] == ["https://e.org/a?utm_source=chatgpt.com"]
    assert ai_check.LLM_LINK.search(p["hrefs"][0])


# ---------------------------------------------------------------- dedupe, twins, chunks, PII

def test_dedupe_keeps_the_earliest_copy_and_spares_one_liners():
    long = " ".join(f"w{i}" for i in range(40))
    posts = [dict(file="late", date="2020-01-01", dropped=[],
                  blocks=[dict(text=long + " extra"), dict(text="Same as ever."), dict(text="Only here.")]),
             dict(file="early", date="2018-01-01", dropped=[], blocks=[dict(text=long), dict(text="Same as ever.")])]
    assert dedupe.dedupe_posts(posts, min_words=20) == 1
    assert [b["text"] for b in posts[0]["blocks"]] == ["Same as ever.", "Only here."]
    assert posts[0]["dropped"][0]["kept_in"] == "early"
    assert len(posts[1]["blocks"]) == 2


def test_split_groups_pull_in_a_twin_that_borrows_from_several_posts():
    a, b, c = (" ".join(f"{k}{i}" for i in range(100)) for k in "abc")
    mix = " ".join(a.split()[:30] + b.split()[:30] + c.split()[:30])      # ~25% from each: no pair above 30%
    tw = find_twins({"a": a, "b": b, "c": c, "mix": mix, "z": " ".join(f"z{i}" for i in range(100))}, n=10, share=0.30)
    assert tw["groups"] == [] and tw["twin_posts"] == ["mix"]
    assert split_groups(tw, min_link=0.05) == [["a", "b", "c", "mix"]]


def _blocks(sizes, kind="p"):
    return [dict(text=" ".join(["w"] * n), kind=kind, n=None) for n in sizes]


def test_chunks_stay_in_bounds_and_cover_every_word():
    sizes = [60, 90, 40, 120, 30, 200, 80, 50, 70, 110, 45, 95, 300, 20, 60] * 3
    out = chunk.chunk_post(_blocks(sizes), key="post")
    assert sum(c["words"] for c in out) == sum(sizes)
    assert all(150 <= c["words"] <= 800 for c in out)
    assert {c["bucket"] for c in out} <= {"150-300", "300-500", "500-800"}
    assert chunk.chunk_post(_blocks(sizes), key="post") == out            # deterministic


def test_short_tail_merges_and_short_post_is_flagged():
    out = chunk.chunk_post(_blocks([200, 60, 40]), key="k", targets=[190])
    assert [c["words"] for c in out] == [300]
    short = chunk.chunk_post(_blocks([70, 60]), key="k")
    assert short[0]["flags"] == ["short"] and short[0]["bucket"] == "under-150"


def test_long_paragraph_splits_on_sentences():
    out = chunk.chunk_post([dict(text=SENT * 120, kind="p", n=None)], key="k")
    assert all(c["words"] <= 800 for c in out) and "split_para" in out[0]["flags"]
    assert sum(c["words"] for c in out) == len((SENT * 120).split())


def test_leadin_stays_with_what_it_introduces():
    blocks = _blocks([160]) + [dict(text="A few examples:", kind="p", n=None)] + _blocks([100, 100])
    out = chunk.chunk_post(blocks, key="k", targets=[170])
    assert not out[0]["text"].endswith("A few examples:")


def test_gap_flags_and_optional_markers():
    blocks = [dict(text="He wrote:", kind="p", n=None, gaps={"quote"})] + _blocks([200])
    plain = chunk.chunk_post(blocks, key="k")[0]
    assert {"quote_gap", "dangling_leadin"} <= set(plain["flags"]) and "text_marked" not in plain
    marked = chunk.chunk_post(blocks, key="k", markers={"quote": "<QUOTE>"})[0]
    assert marked["text_marked"].startswith("He wrote:\n\n<QUOTE>\n\n") and marked["text"] == plain["text"]


def test_pii_finds_emails_and_phones_only():
    hits = pii_regex.find("Write to a.b@example.com or call (206) 555-0100. In 2008 the S&P fell 37% to 903.25.")
    assert [(h["kind"], h["match"]) for h in hits] == [("email", "a.b@example.com"), ("phone", "(206) 555-0100")]
    assert pii_regex.find("It cost $1,200,000 in 1999-2000 and 555 people came.") == []


# ---------------------------------------------------------------- lexicon and AI-text check

def test_inflect():
    assert {"delves", "delved", "delving"} <= inflect("delve")
    assert "intricacies" in inflect("intricacy") and inflect("meticulously") == {"meticulously"}


def test_lexicon_families_and_whitelist():
    lex = Lexicon.load()
    text = ("Additionally, the city boasts a vibrant tapestry of culture, underscoring its enduring legacy. "
            "It serves as a testament to resilience. I hope this helps! As an AI language model, I cannot say.")
    s = lex.score(text)
    assert s["hits"]["vocabulary"] >= 5 and s["hits"]["structure"] >= 2 and s["hits"]["artifacts"] >= 2
    assert "structure:trailing_ing_significance" in s["items"] and "structure:copula_avoidance" in s["items"]
    lex.whitelist = {"word:vibrant", "word:tapestry"}
    assert lex.score(text)["hits"]["vocabulary"] == s["hits"]["vocabulary"] - 2
    plain = lex.score("Of course, markets fall. Sure, some people panic. He bought a house in 1999 and kept it.")
    assert plain["hits"]["artifacts"] == 0


def test_em_dashes_are_never_counted():
    lex = Lexicon.load()
    assert lex.score("Risk — real risk — is what you don’t see — ever.")["hits"] == {
        "vocabulary": 0, "structure": 0, "artifacts": 0}


def test_contrast_detector():
    assert contrast.count("It’s not a bug, but a feature of the whole system.") == 1
    assert contrast.count("The market isn't broken. It's working exactly as designed.") == 1
    assert contrast.count("He was not tall. She walked to the store and bought some bread.") == 0


def test_baseline_rows_are_scored_leave_one_out():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(60, 12))
    base = np.array([True] * 40 + [False] * 20)
    d = ai_check.distances(X, base)
    assert abs(d[base].mean() - d[~base].mean()) < 0.15       # same distribution: no built-in gap


def test_sustained_shift_is_found_only_when_it_lasts():
    rng = np.random.default_rng(1)
    dates = [f"20{10 + i // 12:02d}-{i % 12 + 1:02d}-01" for i in range(180)]       # 2010-01 .. 2024-12
    base = np.array([d < "2022-12-01" for d in dates])
    d = 1 + rng.normal(scale=0.05, size=180)
    assert ai_check.sustained_shifts(d, base, dates, after="2023-03-01") == []
    blip = d.copy()
    blip[170] += 1.0                                                                    # one odd post
    assert ai_check.sustained_shifts(blip, base, dates, after="2023-03-01") == []
    shifted = d.copy()
    shifted[168:] += 0.5                                                                # 2024 onwards
    out = ai_check.sustained_shifts(shifted, base, dates, after="2023-03-01")
    assert len(out) == 1 and out[0]["from_date"] == "2024-01-01"


# ---------------------------------------------------------------- end to end

WORDS = ("money time risk luck people market history story world growth patience habit value price profit "
         "saving spending work plan future past year decade company investor reader writer").split()


def essay(seed: int, paras: int = 8) -> str:
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(paras):
        sents = [" ".join(rng.choice(WORDS, size=int(rng.integers(6, 16)))).capitalize() + "." for _ in range(4)]
        out.append("<p>" + " ".join(sents) + "</p>")
    return "".join(out)


@pytest.fixture()
def cfg(tmp_path):
    raw = tmp_path / "raw" / "pages"
    raw.mkdir(parents=True)
    for i in range(12):
        date = f"{2016 + i}-03-01" if i < 6 else f"{2017 + i}-03-01"      # 2016-2021, then 2023-2028
        raw.joinpath(f"collabfund.com_blog_post-{i}_.html").write_text(page(essay(i), title=f"Post {i}", date=date))
    raw.joinpath("collabfund.com_blog_guest_.html").write_text(page(essay(50), author="Ted Lamade"))
    raw.joinpath("collabfund.com_blog_tiny_.html").write_text(page("<p>Just a link list.</p>"))
    raw.joinpath("collabfund.com_blog_promo_.html").write_text(page(essay(51), title="My New Book"))
    twin = essay(3) + "<p>And one new closing paragraph for the repost of this piece.</p>"
    raw.joinpath("collabfund.com_blog_repost_.html").write_text(page(twin, title="Repost", date="2024-06-01"))
    slop = essay(52) + ("<p>Additionally, this pivotal moment underscores a vibrant tapestry and serves as a "
                        "testament to the evolving landscape, fostering growth. Certainly! I hope this helps.</p>")
    raw.joinpath("collabfund.com_blog_slop_.html").write_text(page(slop, title="Slop", date="2025-02-01"))
    c = yaml.safe_load(open(config.DEFAULT))
    c["paths"] = {k: str(tmp_path / k) for k in ("home", "raw", "legal", "audit", "corpus", "lexicon")}
    c["corpus"]["drop_posts"] = {"promo": "book_promo"}
    c["corpus"]["post_tags"] = {"post-1": ["satire"]}
    c["expected"] = {"words": 1000}
    f = tmp_path / "quill.yaml"
    f.write_text(yaml.safe_dump(c))
    return config.load(f)


def test_build_end_to_end(cfg):
    r = build.build(cfg)
    assert r["pages"] == 17 and r["kept_posts"] == 13
    assert {p["slug"]: p["reason"] for p in r["dropped_posts"]} == {
        "guest": "other_author", "tiny": "under_min_words", "promo": "book_promo",
        "repost": "under_min_words_after_dedupe"}
    assert r["twins"]["groups"] == [["post-3", "repost"]] and r["duplicate_paragraphs"] == 8
    db = store.connect(store.db_path(cfg))
    posts = {p["slug"]: p for p in db.execute("SELECT * FROM posts")}
    assert posts["post-3"]["twin_group"] == posts["repost"]["twin_group"] == "t01"
    assert posts["repost"]["kept"] == 0 and posts["repost"]["drop_reason"] == "under_min_words_after_dedupe"
    assert posts["post-0"]["consent_ref"] and posts["post-0"]["fetched"]
    n = db.execute("SELECT COUNT(*), SUM(words) FROM usable_chunks").fetchone()
    assert n[1] == r["words"] and n[0] == r["chunks"]["n"]
    assert "satire" in json.loads(db.execute("SELECT flags FROM chunks WHERE id = 'post-1#00'").fetchone()[0])
    assert os.path.exists(r["_out"])


def test_aicheck_flags_review_and_gate(cfg):
    build.build(cfg)
    s = ai_check.run(cfg)
    assert s["baseline_posts"] == 6 and s["checked_posts"] == 7
    flags = {f["slug"]: f for f in ai_check.list_flags(cfg)}
    assert {"lexicon_vocabulary", "artifacts"} <= set(flags["slop"]["flags"])
    assert os.path.exists(s["lexicon"]) and os.path.exists(s["_out"])

    gate.spotcheck(cfg, n=5)
    st = {c["name"].split(":")[0]: c["ok"] for c in gate.status(cfg)}
    assert st["spot check"] is None and st["every AI-text flag reviewed and decided"] is None

    for slug in flags:
        assert ai_check.decide(cfg, slug, "drop" if slug == "slop" else "keep", note="test")
    gate.record(cfg, 0)
    assert all(c["ok"] for c in gate.status(cfg) if "tier" not in c["name"])
    db = store.connect(store.db_path(cfg))
    assert db.execute("SELECT COUNT(*) FROM usable_chunks WHERE post_file LIKE '%slop%'").fetchone()[0] == 0

    ai_check.run(cfg)                                    # a rerun keeps decisions whose reasons did not change
    assert {f["decision"] for f in ai_check.list_flags(cfg)} <= {"keep", "drop"}
    build.build(cfg)                                     # a rebuild keeps the flags table
    assert ai_check.list_flags(cfg)
