"""Phase 3: template, pair generation, curation, mlx data. Synthetic text only; no models, no Claude."""
import json

import pytest
import yaml

from quill import template
from quill.gen.claude_cli import Claude
from quill.pairs import curate as C
from quill.pairs import generate as G
from quill.pairs import to_mlx
from quill.scorers import meaning


def _cfg(tmp_path):
    (tmp_path / "legal").mkdir(exist_ok=True)
    (tmp_path / "legal" / "scope.yaml").write_text(yaml.safe_dump(dict(scope=dict(claude_api=True))))
    return dict(paths=dict(home=str(tmp_path), legal=str(tmp_path / "legal"), eval=str(tmp_path / "eval")),
                gen=dict(draft_model="drafter"))


TARGET = ("Warren Buffett bought his first stock in 1942. He was 11 years old.\n\n<QUOTE>\n\n"
          "It took him 60 years to make most of his money. Patience did the work.")
PARA = ("Warren Buffett purchased his first share in 1942, when he was 11.\n\n<QUOTE>\n\n"
        "Most of his wealth arrived over the following 60 years. The cause was patience.")


def _row(**kw):
    return dict(dict(id="p#00", split="train", post="p", words=28, bucket="150-300", target=TARGET, facts="- x",
                     paraphrase=PARA, draft=PARA), **kw)


# ---------------------------------------------------------------- template

def test_template_is_stable_and_rejects_unknown_fields():
    assert template.system("restyle", "draft", "300-500") == "quill v2\nop: restyle\ninput: draft\nlength: 300-500\nvoice: v0"
    m = template.messages("restyle", "paraphrase", "150-300", " in \n", " out\n")
    assert [x["role"] for x in m] == ["system", "user", "assistant"] and m[1]["content"] == "in" and m[2]["content"] == "out"
    assert len(template.messages("restyle", "draft", "150-300", "in")) == 2          # inference: no assistant turn
    assert m[0] == template.messages("restyle", "paraphrase", "150-300", "other")[0]  # same prompt at train and run time
    for bad in (("write", "draft", "300-500"), ("restyle", "brief", "300-500"), ("restyle", "draft", "400")):
        with pytest.raises(ValueError):
            template.system(*bad)
    assert [template.bucket(n) for n in (150, 299, 300, 499, 500, 800)] == ["150-300"] * 2 + ["300-500"] * 2 + ["500-800"] * 2


# ---------------------------------------------------------------- markers

def test_markers_are_found_only_on_their_own_line():
    assert G.markers(TARGET) == ["<QUOTE>"]
    assert G.markers("a\n\n<IMAGE>\n\nb\n\n<QUOTE>") == ["<IMAGE>", "<QUOTE>"]
    assert G.markers("he wrote <QUOTE> inline") == []


def test_insert_markers_places_each_marker_and_keeps_the_words():
    draft = "One.\n\nTwo.\n\nThree."
    assert G.insert_markers(draft, ["<QUOTE>"], [2]) == "One.\n\nTwo.\n\n<QUOTE>\n\nThree."
    assert G.insert_markers(draft, ["<IMAGE>", "<QUOTE>"], [0, 3]) == "<IMAGE>\n\nOne.\n\nTwo.\n\nThree.\n\n<QUOTE>"
    assert G.insert_markers(draft, ["<QUOTE>", "<QUOTE>"], [1, 1]).count("<QUOTE>") == 2
    out = G.insert_markers(draft, ["<QUOTE>"], [99])                     # past the end: goes last
    assert out.endswith("Three.\n\n<QUOTE>") and C.plain(out) == draft


def test_place_markers_uses_the_reply_and_survives_a_bad_one(tmp_path):
    rows = [dict(marked="a\n\n<QUOTE>\n\nb"), dict(marked="no gaps here"), dict(marked="a\n\n<QUOTE>\n\nb\n\n<IMAGE>")]
    drafts = ["P1.\n\nP2.", "Q1.", "R1.\n\nR2."]
    replies = iter(["1", "nonsense"])                                    # only the two marked rows are sent
    seen = []
    c = Claude(_cfg(tmp_path), "m", workers=1, runner=lambda t, s: (seen.append(t) or next(replies), 0.0))
    out = G.place_markers(_cfg(tmp_path), rows, drafts, c)
    assert out[0] == "P1.\n\n<QUOTE>\n\nP2." and out[1] == "Q1."
    assert out[2] == "R1.\n\nR2.\n\n<QUOTE>\n\n<IMAGE>"                  # unparsed reply: markers at the end, in order
    assert len(seen) == 2 and "[1] P1." in seen[0] and "[2] P2." in seen[0]
    assert all(C.plain(o) == d for o, d in zip(out, drafts))             # the draft's words never change


# ---------------------------------------------------------------- curation

def test_plain_strips_markers_and_similarity_is_word_level():
    assert C.plain(TARGET) == TARGET.replace("\n\n<QUOTE>", "")
    assert C.similarity("a b c d", "A B C D") == 1.0 and C.similarity("a b c d", "w x y z") == 0.0


def test_check_passes_a_faithful_pair():
    assert C.check(PARA, TARGET, mis=0.9, tokens=100) == []


def test_check_names_each_failure():
    def fails(inp=PARA, target=TARGET, mis=0.9, tokens=100):
        return C.check(inp, target, mis, tokens)

    assert fails(inp=PARA.replace("1942", "the 1940s")) == ["closure"]              # a number only the target holds
    assert fails(inp=PARA.replace("Warren Buffett", "An investor")) == ["closure"]  # a name only the target holds
    assert fails(inp=PARA.replace("\n\n<QUOTE>", "")) == ["markers"]
    assert fails(inp=PARA + "\n\n<IMAGE>") == ["markers"]
    assert fails(mis=0.69) == ["meaning"]
    assert fails(inp=TARGET) == ["copy"]
    assert "length" in fails(inp=" ".join([PARA] * 3)) and "length" in fails(inp="Warren Buffett, 1942, 11, 60.\n\n<QUOTE>")
    assert fails(tokens=C.MAX_TOKENS + 1) == ["tokens"] and fails(tokens=C.MAX_TOKENS) == []


def test_check_lets_the_input_hold_more_than_the_target():
    assert C.check(PARA + " Charlie Munger agreed in 1990.", TARGET, mis=0.9, tokens=100) == []


class _FakeMIS:
    """Scores 0.9, or 0.2 when either side says BAD."""

    def score(self, a, b):
        return [0.2 if "BAD" in x + y else 0.9 for x, y in zip(a, b)]


def _scored():
    rows = [_row(), _row(id="p#01", paraphrase=PARA.replace("1942", "that year")),
            _row(id="p#02", draft=PARA + " BAD"), _row(id="q#00", split="dev", post="q")]
    return C.score({}, rows, count=lambda msgs: 50, mis=_FakeMIS())


def test_score_and_summary_count_kept_pairs_per_form_and_split():
    rows = _scored()
    assert [r["checks"]["A"]["fails"] for r in rows] == [[], ["closure"], [], []]
    assert [r["checks"]["B"]["fails"] for r in rows] == [[], [], ["meaning"], []]
    s = C.summary(rows)
    assert s["train"]["chunks"] == 3 and s["train"]["both"] == 1 and s["train"]["both_share"] == round(1 / 3, 4)
    assert s["train"]["A"]["kept"] == 2 and s["train"]["A"]["fails"] == {"closure": 1}
    assert s["train"]["B"]["fails"] == {"meaning": 1} and s["dev"]["both_share"] == 1.0


def test_score_sends_marker_free_text_to_the_meaning_scorer():
    seen = []

    class Spy(_FakeMIS):
        def score(self, a, b):
            seen.extend(a + b)
            return super().score(a, b)

    C.score({}, [_row()], count=lambda m: 1, mis=Spy())
    assert seen and not any("<QUOTE>" in t for t in seen)


def test_messages_keep_the_target_verbatim_with_its_markers():
    m = C.messages(_row(), "B")
    assert m[0]["content"].splitlines()[2] == "input: draft" and m[2]["content"] == TARGET
    assert C.messages(_row(), "A")[0]["content"].splitlines()[2] == "input: paraphrase"


def test_report_holds_numbers_only(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "REPO", tmp_path)
    (tmp_path / "eval_reports").mkdir()
    rep = C.report({}, _scored())
    assert rep["gate"]["passed"] is False and rep["gate"]["got"] == round(1 / 3, 4)
    for f in (tmp_path / "eval_reports").iterdir():
        t = f.read_text()
        assert "Buffett" not in t and "Patience" not in t


# ---------------------------------------------------------------- mlx data

def test_to_mlx_writes_kept_pairs_only_and_dev_as_valid(tmp_path):
    cfg = _cfg(tmp_path)
    out = to_mlx.write(cfg, _scored())
    assert out["s1"]["rows"] == dict(train=2, valid=1) and out["s2"]["rows"] == dict(train=2, valid=1)
    d = to_mlx.data_dir(cfg, "s1")
    lines = [json.loads(x) for x in (d / "train.jsonl").read_text().splitlines()]
    assert all(set(x) == {"messages"} and x["messages"][2]["content"] == TARGET for x in lines)
    assert all("input: paraphrase" in x["messages"][0]["content"] for x in lines)
    s2 = [json.loads(x) for x in (to_mlx.data_dir(cfg, "s2") / "train.jsonl").read_text().splitlines()]
    assert all("input: draft" in x["messages"][0]["content"] and "BAD" not in x["messages"][1]["content"] for x in s2)
    assert out["s1"]["hash"] == to_mlx.write(cfg, _scored())["s1"]["hash"]            # deterministic


# ---------------------------------------------------------------- meaning windows

def test_candidates_fall_back_to_the_nearest_starts_not_the_whole_text():
    long = " ".join(["word"] * 60) + "."
    text = " ".join([long] * 4)                         # sentence starts at 0, .25, .5, .75
    c = meaning.candidates(text, 0.37, 0.63)            # no start within the slack of 0.37
    assert c and text not in c and all(len(x.split()) <= 180 for x in c)
    assert meaning.candidates(text, 0.0, 0.25)[0] == long


# ---------------------------------------------------------------- closure, form-tolerant

def test_spelled_numbers_reads_compounds_ordinals_and_plurals():
    got = C.spelled_numbers("thirty-six hours, two hundred years, the sixteenth century, hundreds of them")
    assert {"36", "200", "16", "100"} <= got
    assert C.spelled_numbers("no numbers here") == set()


@pytest.mark.parametrize("inp, target", [
    ("He waited thirty-six hours.", "He waited 36 hours."),
    ("Debt was 100 percent of income.", "Debt was 100% of income."),
    ("It began in the sixteenth century.", "It began in the 16th century."),
    ("There are two reasons. The market reversed completely.", "Two reasons. 1) The market did a full 180."),
    ("After the September 11 attacks, markets fell.", "After 9/11, markets fell."),
    ("John F. Kennedy watched television.", "JFK watched TV."),
    ("The Federal Reserve cut rates.", "The Fed cut rates."),
    ("People in the United States saved more.", "Americans saved more."),
    ("It is the next big thing.", "It is the next Big Thing."),
    ("He cited Frederick Lewis Allen in 1931.", "He cited Frederick Lewis Allan in 1931."),
])
def test_closure_allows_a_change_of_form(inp, target):
    assert C.closure(inp, target) == {}


@pytest.mark.parametrize("inp, target, kind", [
    ("He waited for days.", "He waited 36 hours.", "numbers"),
    ("He waited thirty-five hours.", "He waited 36 hours.", "numbers"),
    ("An investor said so.", "Charlie Munger said so.", "names"),
    ("He saw a famous monument.", "He saw the Taj Mahal.", "names"),
    ("It happened that spring.", "It happened on March 4, 1933.", "dates"),
])
def test_closure_still_catches_a_missing_fact(inp, target, kind):
    assert kind in C.closure(inp, target)
