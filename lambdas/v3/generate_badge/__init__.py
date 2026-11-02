from shared.badge import Badge, handle_badge_request

# accent colors lifted so they stay readable on the dark background
ACCENTS: dict[str, str] = {
    "red": "#FF6464",
    "orange": "#FF9F45",
    "yellow": "#DDD54E",
    "blue": "#8199FF",
    "cyan": "#3AD7D7",
    "green": "#4CC46A",
    "brown": "#D0915F",
    "gray": "#B1B5BB",
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# number of cells in the progress bar toward the next 200 rating step
CELLS = 24


def handler(event, _context):
    return handle_badge_request(event, render_svg)


def render_svg(badge: Badge) -> str:
    accent = ACCENTS[badge.tier_group]
    unrated = badge.tier == "Unrated"
    filled = 0 if unrated else round(badge.rating % 200 / 200 * CELLS)

    prompt = f"atcoder stats {badge.username}"
    # monospace advance is ~0.6em; only used to park the cursor after the prompt
    cursor_x = 38 + len(prompt) * 6.6 + 4

    rating_text = (
        "-"
        if unrated
        else f'{badge.rating}<tspan fill="#7D8590"> (max {badge.highest_rating})</tspan>'
    )
    rows = [
        ("tier", f'<tspan fill="{accent}" font-weight="700">{badge.tier}</tspan>'),
        ("rating", rating_text),
        ("rank", badge.rank),
        ("matches", str(badge.matches)),
    ]
    rows_svg = "\n".join(
        f"""\
    <g class="line" style="animation-delay:{0.15 + i * 0.12:.2f}s">
        <text x="24" y="{58 + i * 18}" class="mono" fill="#7D8590">{label}</text>
        <text x="96" y="{58 + i * 18}" class="mono" fill="#E6EDF3">{value}</text>
    </g>"""
        for i, (label, value) in enumerate(rows)
    )

    cells_svg = "\n".join(
        f'    <rect x="{24 + i * 9}" y="136" width="7" height="10" fill="{accent}" class="cell" style="animation-delay:{0.8 + i * 0.03:.2f}s"/>'
        if i < filled
        else f'    <rect x="{24 + i * 9}" y="136" width="7" height="10" fill="#21262D"/>'
        for i in range(CELLS)
    )

    progress = "no rated contest" if unrated else f"{badge.rating}/{badge.next_rating}"

    return f"""\
<?xml version="1.0" encoding="UTF-8"?>
<svg
    width="350"
    height="170"
    viewBox="0 0 350 170"
    fill="none"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
>
    <style type="text/css">
        .mono {{
            font-family: {MONO};
            font-size: 11.5px;
        }}

        .line, .cell {{
            opacity: 0;
            animation: show 0.01s steps(1) forwards;
        }}

        .cursor {{
            animation: blink 1s steps(1) infinite;
        }}

        @keyframes show {{
            to {{
                opacity: 1;
            }}
        }}

        @keyframes blink {{
            50% {{
                opacity: 0;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .line, .cell {{
                animation: none;
                opacity: 1;
            }}

            .cursor {{
                animation: none;
            }}
        }}
    </style>
    <clipPath id="card">
        <rect width="350" height="170" rx="6"/>
    </clipPath>
    <g clip-path="url(#card)">
    <rect width="350" height="170" fill="#0D1117"/>
    <rect width="3" height="170" fill="{accent}"/>
    <rect x="0.5" y="0.5" width="349" height="169" rx="6" fill="none" stroke="#30363D"/>
    <text x="24" y="30" class="mono"><tspan fill="{accent}">$</tspan><tspan fill="#E6EDF3"> {prompt}</tspan></text>
    <rect x="{cursor_x:.1f}" y="20" width="7" height="13" fill="#E6EDF3" class="cursor"/>
    <text x="326" y="30" class="mono" fill="#7D8590" text-anchor="end" font-size="10">atcoder.jp</text>
    <line x1="24" y1="40" x2="326" y2="40" stroke="#21262D"/>
{rows_svg}
{cells_svg}
    <text x="326" y="145" class="mono" fill="#7D8590" text-anchor="end" font-size="10">{progress}</text>
    </g>
</svg>
"""
