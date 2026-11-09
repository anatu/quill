from quill.clean.twins import find_twins
from quill.ingest import textlib as T
from quill.ingest.collabfund import dedupe_boiler

BASE = " ".join(f"word{i}" for i in range(60))


def test_twins_group_reposts_and_skip_unrelated():
    docs = {
        "a": BASE,
        "b": BASE + " " + " ".join(f"extra{i}" for i in range(20)),
        "c": " ".join(f"other{i}" for i in range(80)),
    }
    out = find_twins(docs, n=10, share=0.30)
    assert out["groups"] == [["a", "b"]]
    assert set(out["twin_posts"]) == {"a", "b"}


def test_dedupe_boiler_drops_paragraph_repeated_across_posts():
    posts = [{"paras": [f"essay {i} text", "More on this topic"]} for i in range(5)]
    removed = dedupe_boiler(posts)
    assert removed == ["more on this topic"]
    assert all(p["paras"] == [f"essay {i} text"] for i, p in enumerate(posts))


def test_extract_drops_blockquotes_and_chrome():
    html = (
        "<html><head><title>T · Collaborative Fund</title></head><body>"
        "<nav><p>Menu</p></nav><article>"
        "<p>His own sentence one is here and it is long enough.</p>"
        "<blockquote><p>A quoted passage from someone else.</p></blockquote>"
        "<p>His own sentence two follows the quote.</p>"
        "</article><footer><p>Copyright</p></footer></body></html>"
    )
    title, paras = T.extract_html(html)
    assert title == "T · Collaborative Fund"
    assert any(p["bq"] for p in paras)
    kept = T.clean_paras(paras)
    assert kept == ["His own sentence one is here and it is long enough.", "His own sentence two follows the quote."]
