"""Draw the README charts from the aggregate reports in eval_reports/.

    uv run python scripts/readme_charts.py

Writes assets/{ladder,fingerprint}-{light,dark}.svg. Numbers only; no corpus text is read.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REPORTS = REPO / "eval_reports"
QUILL = "sft-v1-s2m-ptag-n4"         # the best system scored on dev
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEME = dict(
    light=dict(ink="#0b0b0b", ink2="#52514e", muted="#898781", grid="#e1e0d9", axis="#c3c2b7", surface="#ffffff",
               quill="#2a78d6", opus="#eb6834", draft="#1baf7a", neutral="#c3c2b7", author="#52514e"),
    dark=dict(ink="#f0efec", ink2="#c3c2b7", muted="#898781", grid="#2c2c2a", axis="#383835", surface="#0d1117",
              quill="#3987e5", opus="#d95926", draft="#199e70", neutral="#55544f", author="#c3c2b7"),
)


def scores(name: str) -> dict:
    return json.loads((REPORTS / f"{name}-dev.json").read_text())["scores"]


def svg(w: int, h: int, body: list[str], title: str, desc: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'font-family="{FONT}"><title>{title}</title><desc>{desc}</desc>\n' + "\n".join(body) + "\n</svg>\n")


def bar(x: float, y: float, w: float, h: float, fill: str, r: float = 4) -> str:
    """A horizontal bar anchored at the baseline (square left), rounded at the data end."""
    w = max(w, 0.0)
    if w <= r:
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 1.5):.1f}" height="{h}" fill="{fill}"/>'
    return (f'<path d="M{x:.1f},{y:.1f} h{w - r:.1f} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r:.1f} '
            f'a{r},{r} 0 0 1 -{r},{r} h-{w - r:.1f} z" fill="{fill}"/>')


def ladder(mode: str) -> str:
    c = THEME[mode]
    base = json.loads((REPORTS / "baseline-v2.json").read_text())["sanity"]["M1"]
    rows = [("The author's own held-out essays", base["ceiling_accept"], c["author"], "the ceiling"),
            ("quill: fine-tuned 8B, on a laptop", scores(QUILL)["M1_av"]["accept_rate"], c["quill"], ""),
            ("Claude Opus + style guide + 5 real passages", scores("b0")["M1_av"]["accept_rate"], c["neutral"], ""),
            ("Same 8B model, not fine-tuned", scores("b1")["M1_av"]["accept_rate"], c["neutral"], ""),
            ("Other human essayists", base["impostor_accept"], c["neutral"], ""),
            ("A plain assistant draft", scores("b2")["M1_av"]["accept_rate"], c["neutral"], "")]
    w, left, right, top, rh, bh = 860, 318, 96, 54, 40, 20
    plot = w - left - right
    h = top + rh * len(rows) + 34
    out = [f'<text x="0" y="20" font-size="16" font-weight="600" fill="{c["ink"]}">How often does an authorship check say '
           f'"that is the author"?</text>',
           f'<text x="0" y="40" font-size="12.5" fill="{c["ink2"]}">Share of passages accepted, on topics the check never saw. '
           f'Dev split.</text>']
    for t in (0, 25, 50, 75, 100):
        x = left + plot * t / 100
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + rh * len(rows)}" stroke="{c["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{x:.1f}" y="{top + rh * len(rows) + 18}" font-size="11.5" fill="{c["muted"]}" text-anchor="middle">{t}%</text>')
    for i, (label, v, fill, note) in enumerate(rows):
        y = top + i * rh + (rh - bh) / 2
        strong = fill == c["quill"]
        out.append(f'<text x="{left - 12}" y="{y + bh / 2 + 4.5:.1f}" font-size="13" text-anchor="end" '
                   f'fill="{c["ink"] if strong else c["ink2"]}" font-weight="{600 if strong else 400}">{label}</text>')
        out.append(bar(left, y, plot * v, bh, fill))
        out.append(f'<text x="{left + plot * v + 8:.1f}" y="{y + bh / 2 + 4.5:.1f}" font-size="13" font-weight="600" '
                   f'fill="{c["ink"]}">{v:.1%}</text>')
    out.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + rh * len(rows)}" stroke="{c["axis"]}" stroke-width="1"/>')
    return svg(w, h, out, "Authorship check accept rate by system",
               "Horizontal bars: " + "; ".join(f"{r[0]} {r[1]:.1%}" for r in rows))


FEATURES = [("one_sent_para_share", "One-sentence paragraphs", lambda v: f"{v:.0%}"),
            ("words_per_para", "Words per paragraph", lambda v: f"{v:.0f}"),
            ("emdash_per_1k", "Em dashes per 1,000 words", lambda v: f"{v:.1f}"),
            ("sent_len_mean", "Words per sentence", lambda v: f"{v:.1f}"),
            ("sent_len_sd", "Spread of sentence length", lambda v: f"{v:.1f}"),
            ("question_per_100s", "Questions per 100 sentences", lambda v: f"{v:.1f}")]


def marker(kind: str, x: float, y: float, fill: str, ring: str) -> str:
    if kind == "circle":
        return f'<circle cx="{x:.1f}" cy="{y}" r="6.5" fill="{fill}" stroke="{ring}" stroke-width="2"/>'
    if kind == "diamond":
        return (f'<path d="M{x:.1f},{y - 7.5} l7.5,7.5 l-7.5,7.5 l-7.5,-7.5 z" fill="{fill}" stroke="{ring}" '
                f'stroke-width="2"/>')
    return f'<rect x="{x - 5.5:.1f}" y="{y - 5.5}" width="11" height="11" rx="1.5" fill="{fill}" stroke="{ring}" stroke-width="2"/>'


def fingerprint(mode: str) -> str:
    c = THEME[mode]
    series = [("A plain assistant draft", "b2", c["draft"], "square"),
              ("Claude Opus + style guide", "b0", c["opus"], "diamond"),
              ("quill", QUILL, c["quill"], "circle")]
    tics = {name: scores(name)["M6_tic_profile"]["features"] for _, name, _, _ in series}
    w, left, right, top, rh = 860, 232, 150, 96, 52
    plot, hi = w - left - right, 2.25
    h = top + rh * len(FEATURES) + 40
    sx = lambda r: left + plot * min(r, hi) / hi
    out = [f'<text x="0" y="20" font-size="16" font-weight="600" fill="{c["ink"]}">A voice has a shape. '
           f'How close does each system get?</text>',
           f'<text x="0" y="40" font-size="12.5" fill="{c["ink2"]}">Each habit as a multiple of the author&#39;s own rate. '
           f'On the line is a match. Dev split.</text>']
    lx = 0.0
    for label, _, fill, kind in series:                      # legend, always present for 3 series
        out.append(marker(kind, lx + 8, 66, fill, c["surface"]))
        out.append(f'<text x="{lx + 22:.1f}" y="70.5" font-size="12.5" fill="{c["ink2"]}">{label}</text>')
        lx += 40 + 6.6 * len(label)
    for t in (0, 0.5, 1.5, 2.0):
        out.append(f'<line x1="{sx(t):.1f}" y1="{top}" x2="{sx(t):.1f}" y2="{top + rh * len(FEATURES)}" stroke="{c["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{sx(t):.1f}" y="{top + rh * len(FEATURES) + 18}" font-size="11.5" fill="{c["muted"]}" text-anchor="middle">{t:g}×</text>')
    out.append(f'<line x1="{sx(1):.1f}" y1="{top - 6}" x2="{sx(1):.1f}" y2="{top + rh * len(FEATURES)}" stroke="{c["author"]}" stroke-width="2"/>')
    out.append(f'<text x="{sx(1):.1f}" y="{top + rh * len(FEATURES) + 18}" font-size="11.5" font-weight="600" fill="{c["ink"]}" text-anchor="middle">the author</text>')
    for i, (key, label, fmt) in enumerate(FEATURES):
        y = top + i * rh + rh / 2
        ref = tics[QUILL][key]["reference"]
        out.append(f'<text x="{left - 14}" y="{y + 4.5}" font-size="13" text-anchor="end" fill="{c["ink"]}">{label}</text>')
        if i:
            out.append(f'<line x1="{left}" y1="{y - rh / 2}" x2="{left + plot}" y2="{y - rh / 2}" stroke="{c["grid"]}" stroke-width="1"/>')
        for k, (_, name, fill, kind) in enumerate(series):     # one lane per series, so close values stay visible
            out.append(marker(kind, sx(tics[name][key]["value"] / ref), y + (k - 1) * 11, fill, c["surface"]))
        q = tics[QUILL][key]["value"]
        out.append(f'<text x="{left + plot + 14}" y="{y + 4.5}" font-size="12" fill="{c["ink2"]}">'
                   f'<tspan fill="{c["ink"]}" font-weight="600">{fmt(q)}</tspan> vs {fmt(ref)}</text>')
    out.append(f'<text x="{left + plot + 14}" y="{top - 10}" font-size="11.5" fill="{c["muted"]}">quill vs author</text>')
    desc = "; ".join(f"{label}: " + ", ".join(f"{s[0]} {tics[s[1]][key]['value'] / tics[QUILL][key]['reference']:.2f}x" for s in series)
                     for key, label, _ in FEATURES)
    return svg(w, h, out, "Style habits as a multiple of the author's rate", desc)


def main() -> None:
    d = REPO / "assets"
    d.mkdir(exist_ok=True)
    for mode in THEME:
        (d / f"ladder-{mode}.svg").write_text(ladder(mode))
        (d / f"fingerprint-{mode}.svg").write_text(fingerprint(mode))
    print("wrote", sorted(p.name for p in d.glob("*.svg")))


if __name__ == "__main__":
    main()
