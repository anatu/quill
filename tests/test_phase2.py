"""Phase 2: splits and scorers. Synthetic text only; no model downloads."""
import numpy as np

from quill.corpus import split
from quill.eval import pool
from quill.scorers import av, entities, memo, stylometry


# ---------------------------------------------------------------- splits

def test_pick_clusters_hits_the_target_and_respects_exclusions():
    words = {0: 500, 1: 100, 2: 60, 3: 40, 4: 300}
    assert split.pick_clusters(words, 0.10, 1000) == (2, 3)          # 100 words; ties go to more clusters
    assert split.pick_clusters(words, 0.10, 1000, exclude={2, 3}) == (1,)


def test_assign_keeps_twin_groups_together_and_clusters_whole():
    rows = [dict(file=f"p{i}", words=100, twin_group=None) for i in range(20)]
    rows[0]["twin_group"] = rows[19]["twin_group"] = "t01"            # one twin pair across two clusters
    rows[0]["words"] = 300
    labels = [i // 2 for i in range(20)]                               # 10 clusters of 2 posts
    posts, info = split.assign(rows, labels, test_share=0.10, dev_share=0.10)
    assert posts["p0"] == posts["p19"] and info["straddling_twin_groups"] == ["t01"]
    by_cluster = {}
    for i, r in enumerate(rows):
        if r["twin_group"] is None:
            by_cluster.setdefault(labels[i], set()).add(posts[r["file"]])
    assert all(len(v) == 1 for v in by_cluster.values())              # no cluster is cut in two
    assert set(posts.values()) == {"train", "dev", "test"}
    assert split.assignment_hash(posts) == split.assignment_hash(dict(reversed(list(posts.items()))))
    assert split.assignment_hash(posts) != split.assignment_hash({**posts, "p5": "test" if posts["p5"] != "test" else "dev"})


def test_segments_cut_long_text_and_return_short_text_whole():
    para = " ".join(["word"] * 100)
    segs = pool.segments("\n\n".join([para] * 9))
    assert len(segs) == 3 and all(250 <= len(s.split()) <= 450 for s in segs)
    assert pool.segments("A short text.") == ["A short text."]
    assert pool.part_of("a:1") == pool.part_of("a:1") and pool.part_of("a:1") in ("train", "dev", "test")


# ---------------------------------------------------------------- M1, M15

def _voice(rng, words, n, tic):
    out = []
    for _ in range(n):
        sents = [" ".join(rng.choice(words, size=int(rng.integers(5, 14)))).capitalize() + tic for _ in range(20)]
        out.append(" ".join(sents))
    return out


def test_verifier_and_attributor_separate_two_voices():
    rng = np.random.default_rng(0)
    vocab = "money time risk luck people market history story world growth patience habit value price".split()
    a = _voice(rng, vocab, 40, " — you know.")
    b = _voice(rng, vocab, 40, "; moreover, indeed.")
    g = [f"g{i // 2}" for i in range(30)]
    v = av.Verifier().fit(a[:30], g, b[:30], g)
    assert v.accept(a[30:]).mean() >= 0.9 and v.accept(b[30:]).mean() <= 0.1
    at = av.Attributor().fit(a[:30] + b[:30], ["author"] * 30 + ["llm"] * 30)
    assert at.shares(a[30:])["author"] >= 0.9 and at.shares(b[30:])["llm"] >= 0.9


# ---------------------------------------------------------------- M6

def _essay(rng, n_paras, sent_len, dash):
    paras = []
    for _ in range(n_paras):
        sents = []
        for _ in range(int(rng.integers(1, 5))):
            k = max(3, int(rng.normal(sent_len, 4)))
            s = " ".join(rng.choice(["you", "money", "people", "time", "risk", "is", "the", "of", "and"], size=k))
            sents.append(s.capitalize() + (" — it is." if rng.random() < dash else "."))
        paras.append(" ".join(sents))
    return "\n\n".join(paras)


def test_tic_profile_passes_the_same_voice_and_flags_a_caricature():
    rng = np.random.default_rng(1)
    train = [_essay(rng, 12, 14, 0.2) for _ in range(120)]
    same = [_essay(rng, 12, 14, 0.2) for _ in range(40)]
    caricature = [_essay(rng, 12, 8, 0.0) for _ in range(40)]        # short sentences, no dashes
    tp = stylometry.TicProfile().fit(train, groups=[i % 4 for i in range(120)])
    assert tp.score(same)["max_abs_z"] <= 2
    bad = tp.score(caricature)
    assert bad["max_abs_z"] > 2 and bad["features"]["emdash_per_1k"]["z"] < -2
    assert bad["features"]["sent_len_mean"]["z"] < -2


def test_delta_is_smaller_for_the_same_author():
    rng = np.random.default_rng(2)
    wa, wb = ["the", "of", "and", "you", "money"], ["the", "of", "but", "we", "market"]
    mk = lambda w, n: [" ".join(rng.choice(w, size=400)) for _ in range(n)]     # noqa: E731
    a1, a2, b = mk(wa, 30), mk(wa, 30), mk(wb, 30)
    d = stylometry.Delta.build({"a": a1, "b": b, "c": mk(["the", "a", "in"], 10)}).fit(a1)
    assert d.score(a2)["delta"] < d.score(b)["delta"]


# ---------------------------------------------------------------- M8, M9

def test_memo_finds_copied_spans_and_exempts_the_input():
    m = memo.Memo(n=8)
    m.add("Good investing is not about earning the highest returns because the highest returns tend to be one-off hits.")
    copied = "As one writer put it, investing is not about earning the highest returns because the highest returns fade."
    r = m.longest(copied)
    assert r["span"] == 12 and r["text"].startswith("investing is not about earning")
    assert m.longest("Totally fresh words that share nothing at all with the indexed corpus text here.")["span"] == 0
    assert m.longest(copied, input_text=copied)["span"] == 0          # the draft already said it
    assert m.longest("Investing is not about earning the highest.")["span"] == 0   # 7 words: under the gate


def test_signature_picks_the_author_phrases():
    author = ["the point is that risk is what you do not see and " + f"topic{i} matters" for i in range(30)]
    others = ["in this letter we report that earnings grew and " + f"topic{i} matters" for i in range(30)]
    s = memo.Signature(k=10, min_count=5, min_docs=5).fit(author, others)
    assert "the point" in s.phrases and not any("report" in p for p in s.phrases)
    assert s.rate(author[:5]) > 10 * max(s.rate(others[:5]), 0.01)


# ---------------------------------------------------------------- M5

SRC = ("In 1987 Warren Buffett paid $1.2 billion for 12% of Salomon Brothers. On October 19, 1987 the market fell "
       "22.6%. See https://example.com/letter for the letter.")


def test_entities_pass_on_a_faithful_restyle():
    out = ("Buffett bought 12% of Salomon Brothers in 1987. He paid $1.2 billion. Then, on October 19, 1987, the "
           "market fell 22.6%. The letter is at https://example.com/letter.")
    r = entities.compare(SRC, out)
    assert r["ok"], r


def test_entities_catch_each_kind_of_mutation():
    base = ("Buffett bought 12% of Salomon Brothers in 1987 for $1.2 billion. On October 19, 1987 the market fell "
            "22.6%. The letter is at https://example.com/letter.")
    cases = {
        "dropped number": (base.replace(" for $1.2 billion", ""), "missing", "numbers"),
        "changed number": (base.replace("22.6%", "26.2%"), "added", "numbers"),
        "shifted date": (base.replace("October 19", "October 20"), "added", "dates"),
        "new name": (base.replace("the market fell", "Charlie Munger said the market fell"), "added", "names"),
        "dropped name": (base.replace("Salomon Brothers", "a bank"), "missing", "names"),
        "changed link": (base.replace("/letter", "/other"), "added", "urls"),
    }
    for name, (out, side, kind) in cases.items():
        r = entities.compare(SRC, out)
        assert not r["ok"] and kind in r[side], (name, r)


def test_entities_ignore_sentence_initial_capitals():
    assert entities.compare("the market fell. people panicked.", "The market fell. People panicked. Nobody knew.")["ok"]
