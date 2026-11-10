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


def test_entities_ignore_list_marks_and_stop_at_full_stops():
    src = "- Sam Bankman-Fried was admired.\n- Thirteen people said so.\n- Say it plainly."
    out = "1. People admired Sam Bankman-Fried. Nobody doubted him.\n2. Say I asked 13 of them."
    assert entities.compare(src, out)["ok"], entities.compare(src, out)


def test_entities_ignore_item_labels_openers_and_word_order():
    src = ("- Point 9: Lloyd Blankfein, former Goldman Sachs CEO, is worth $1 billion.\n- 14: Steve Jobs kept working.\n"
           "- Item 3 in the list: Covid changed habits after Bryson wrote about it.")
    out = ("Lloyd Blankfein, the former CEO of Goldman Sachs, is worth $1 billion. Same for Steve Jobs, who kept working. "
           "After the Covid years, habits changed. Per Bryson, that was expected.")
    assert entities.compare(src, out)["ok"], entities.compare(src, out)
    assert not entities.compare(src, out + " Same for Elon Musk.")["ok"]
    assert not entities.compare(src, out.replace("$1 billion", "$9 billion"))["ok"]


def test_entities_ignore_sentence_initial_capitals():
    assert entities.compare("the market fell. people panicked.", "The market fell. People panicked. Nobody knew.")["ok"]


# ---------------------------------------------------------------- generation, baselines

def _cfg(tmp_path, claude_api=True):
    legal = tmp_path / "legal"
    legal.mkdir(exist_ok=True)
    (legal / "scope.yaml").write_text(f"scope:\n  claude_api: {'yes' if claude_api else 'unknown'}\n")
    return dict(paths=dict(legal=legal, eval=tmp_path / "eval"), author=dict(name="The Author"))


def test_claude_calls_are_cached_per_sample_and_blocked_without_consent(tmp_path):
    import pytest
    from quill.gen.claude_cli import Claude, prompt

    seen = []
    c = Claude(_cfg(tmp_path), "m", workers=2, runner=lambda t, s: (seen.append(t) or f"out:{t}", 0.01))
    assert c.map([("a",), ("b",), ("a",)]) == ["out:a", "out:b", "out:a"] and sorted(seen) == ["a", "b"]
    assert c.ask("a", sample=1) == "out:a" and len(seen) == 3          # a new sample is a new draw
    assert Claude(_cfg(tmp_path), "m", runner=lambda t, s: ("x", 0)).ask("a") == "out:a"   # cache survives
    with pytest.raises(SystemExit):
        Claude(_cfg(tmp_path, claude_api=False), "m")
    assert "{text}" not in prompt("facts", text="a {brace} stays") and "{brace}" in prompt("facts", text="a {brace} stays")


class _Ctx:
    use_embeddings = True

    def __init__(self):
        from quill.scorers.lexicon import Lexicon
        self.memo = memo.Memo(n=8)
        self.memo.add("the highest returns tend to be one-off hits that cannot be repeated by anyone at all")
        self.lexicon = Lexicon(dict(vocabulary=dict(words=[], phrases={}), structure={},
                                    artifacts={"chat_opener": r"^Certainly!"}), set())

    def spans(self, text, given, chunk_id=None):
        return self.memo.longest(text, given)["span"], 0

    def style_delta(self, texts):
        return np.array([t.count("—") for t in texts], dtype=float)


def test_rerank_gates_first_then_style():
    from quill.eval import baselines

    ctx = _Ctx()
    given = "In 1987 Warren Buffett paid $1.2 billion for a stake in the bank and it worked out well for him."
    good = "Buffett paid $1.2 billion in 1987 for a piece of the bank — and it worked out well for him, mostly."
    plain = "In 1987 Buffett paid $1.2 billion for part of the bank and it worked out well for him in the end."
    wrong = "Buffett paid $2.1 billion in 1987 — for the bank — and it — worked out well — for him, mostly, yes."
    copied = good + " The highest returns tend to be one-off hits that cannot be repeated by anyone."
    r = baselines.rerank(ctx, [plain, wrong, good, copied], given, words=20)
    assert r["choice"] == 2 and not r["fallback"]
    assert r["checks"][1]["fails"] == ["entities"] and "memorization" in r["checks"][3]["fails"]
    r = baselines.rerank(ctx, [wrong, "Certainly! " + wrong], given, words=20)
    assert r["fallback"] and r["choice"] == 0


def test_exemplars_and_openings_are_stable():
    from quill.eval import baselines

    train = [dict(id=f"t{i}", bucket="150-300" if i % 2 else "300-500", words=200, text=f"text {i}") for i in range(40)]
    row = dict(id="x#00", bucket="150-300")
    a, b = baselines.exemplars(train, row), baselines.exemplars(train, row)
    assert a == b and len(a) == 5 and all(c["bucket"] == "150-300" for c in a)
    assert baselines.first_sentences("Short one. This second sentence makes it long enough to stand as an opening. Third.") \
        == "Short one. This second sentence makes it long enough to stand as an opening."


def test_content_mask_keeps_function_words_and_punctuation():
    from quill.scorers import av

    keep = av.frequent_words(["the cat and the dog. the end, and so on"], 3)
    assert keep == {"the", "and", "cat"} or {"the", "and"} <= keep
    assert av.mask("The Buffett rule — and 1,200 dollars, the end.", frozenset({"the", "and"})) == "The * * — and 0 *, the *."


def test_entities_ner_keeps_sentence_initial_name_and_mutations_fail():
    from quill.scorers import entities

    src = "Buffett bought the stock in 1988. He paid $1 billion. Coca-Cola then tripled."
    assert entities.compare(src, "In 1988 the stock was bought by Buffett for $1 billion. Coca-Cola then tripled.")["ok"]
    r = entities.compare(src, "Soros bought the stock in 1988. He paid $1 billion. Coca-Cola then tripled.")
    assert not r["ok"] and "buffett" in r["missing"]["names"]
    assert not entities.compare(src, src.replace("1988", "1989"))["ok"]
    assert not entities.compare(src, src.replace("$1 billion", "$2 billion"))["ok"]
    assert not entities.compare(src, src + " Read more at https://example.com/x")["ok"]


def test_blind_kit_matches_length_records_answers_and_reports(tmp_path):
    from quill.eval import blind

    cfg = {"paths": {"eval": str(tmp_path)}}
    para = "One short sentence here. Another one follows it now. A third closes the paragraph."
    chunks = [dict(id=f"t{i}", split="test", post=f"p{i}", text="\n\n".join([para] * 6)) for i in range(5)]
    chunks += [dict(id="r0", split="train", post="q", text=para)]
    outs = {"sys": {f"t{i}": "\n\n".join(["It’s  “fine”. Really it is."] * 4) for i in range(5)}}
    kit = blind.make(cfg, "A", "sys", "test", n=4, chunks=chunks, outputs=outs)
    assert kit["n"] == 4 and blind.make(cfg, "A", "sys", "test", n=9)["n"] == 4      # frozen once built
    it = kit["items"][0]
    assert abs(len(it["first"].split()) - len(it["second"].split())) <= 14 and "“" not in it["first"] + it["second"]
    said = iter([str(i["truth"]) if k < 3 else str(3 - i["truth"]) for k, i in enumerate(kit["items"]) for _ in (0,)])
    script = iter(x for i in kit["items"] for x in (next(said), "rhythm", "n"))
    blind.session(cfg, kit, ask=lambda _: next(script), show=lambda *_: None)
    r = blind.report(cfg, kit)
    assert (r["answered"], r["hits"], r["recognized"]) == (4, 3, 0) and r["p_one_sided"] == 0.3125
    assert blind.binom_p(26, 40) < 0.05 < blind.binom_p(25, 40)


def test_judge_counts_only_consistent_picks():
    from quill.eval import judge

    class Fake:
        def map(self, jobs):
            return ["A", "B", "A", "A", "B", "A"]

    assert judge.ask(Fake(), [("r", "x", "y")] * 3) == [1, 0, -1]


def test_composite_applies_gate_and_paired_bootstrap():
    from quill.eval import harness

    good = [dict(id=f"c{i}", gate=True, m1=0.8, m15=0.8, m4=0.8) for i in range(20)]
    bad = [dict(r, gate=i % 2 == 0, m1=0.2) for i, r in enumerate(good)]
    assert abs(harness.composite(good) - 0.8) < 1e-9
    assert abs(harness.composite(bad) - 0.5 * (0.2 * 0.8 * 0.8) ** (1 / 3)) < 1e-9
    d = harness.bootstrap(good, bad, n=200)
    assert d["ci95"][0] > 0 and d["chunks"] == 20


def test_entities_common_word_at_sentence_start_is_not_a_name():
    from quill.scorers import entities

    entities.set_common(["a bit of luck and vanity"])
    assert entities.compare("People get lucky. It matters a lot.", "Luck matters. Vanity does not help people.")["ok"]
