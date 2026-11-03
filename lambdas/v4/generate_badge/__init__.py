import re

from lambdas.v4.generate_badge.kanji import KANJI, KANJI_UPM
from shared.badge import Badge, handle_badge_request

# same gradients as v2 so v4 reads as part of the family
GRADIENTS: dict[str, list[str]] = {
    "red": ["#FF7171", "#D44141", "#870C0C"],
    "orange": ["#FFB771", "#CF853D", "#81470E"],
    "yellow": ["#DCDC56", "#C3C332", "#84840E"],
    "blue": ["#7171FF", "#3B3BCF", "#1212A4"],
    "cyan": ["#80DFDF", "#4DB7B7", "#206767"],
    "green": ["#8AC48A", "#5EA15E", "#377E37"],
    "brown": ["#C4A78A", "#B28659", "#78512A"],
    "gray": ["#BBBBBB", "#8E8E8E", "#4F4F4F"],
}

# deep tier colors for the characters carved into the seal
SEAL_INK: dict[str, str] = {
    "red": "#7A1010",
    "orange": "#6E3405",
    "yellow": "#5A5206",
    "blue": "#1A2280",
    "cyan": "#0B4C52",
    "green": "#174A22",
    "brown": "#55361A",
    "gray": "#3A3A3A",
}

SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

KANJI_DIGITS = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]

TIER_PATTERN = re.compile(r"(\d+) (Kyu|Dan)")

# seal box position and size
SEAL_X, SEAL_Y, SEAL_W, SEAL_H = 32, 24, 68, 114


def handler(event, _context):
    return handle_badge_request(event, render_svg)


def kanji_number(n: int) -> str:
    if n < 10:
        return KANJI_DIGITS[n]
    tens = n // 10
    return f"{KANJI_DIGITS[tens] if tens > 1 else ''}十{KANJI_DIGITS[n % 10]}"


def seal_text(tier: str) -> str:
    """Characters stamped on the seal, read top to bottom.

    Dan and 極伝 (King) follow AtCoder's Japanese pages; 皆伝 (Legend) and
    未定 (Unrated) are not confirmed yet.
    """
    if match := TIER_PATTERN.fullmatch(tier):
        n, unit = int(match[1]), match[2]
        if unit == "Kyu":
            return f"{kanji_number(n)}級"
        return "初段" if n == 1 else f"{kanji_number(n)}段"
    if tier == "Legend":
        return "皆伝"
    if tier == "King":
        return "極伝"
    return "未定"


def next_tier_name(tier: str) -> str | None:
    """Kyu counts down to 1 Kyu, then Dan counts up to 10 Dan, then Legend, King"""
    if match := TIER_PATTERN.fullmatch(tier):
        n, unit = int(match[1]), match[2]
        if unit == "Kyu":
            return f"{n - 1} Kyu" if n > 1 else "1 Dan"
        return f"{n + 1} Dan" if n < 10 else "Legend"
    if tier == "Legend":
        return "King"
    return None


def render_seal(badge: Badge) -> str:
    chars = seal_text(badge.tier)
    size = 36 if len(chars) <= 2 else 28 if len(chars) == 3 else 22
    step = (SEAL_H - 16) / len(chars)
    scale = size / KANJI_UPM
    ink = SEAL_INK[badge.tier_group]

    paths = []
    for i, char in enumerate(chars):
        d, advance = KANJI[char]
        x = SEAL_X + SEAL_W / 2 - advance * scale / 2
        # ideographs sit in an em box from -0.12em to 0.88em, so its middle is 0.38em above the baseline
        baseline = SEAL_Y + 8 + step * i + step / 2 + size * 0.38
        paths.append(
            f'<path d="{d}" transform="translate({x:.2f} {baseline:.2f}) scale({scale:.4f})" fill="{ink}"/>'
        )
    chars_svg = "\n        ".join(paths)

    return f"""\
    <g class="stamp">
        <g filter="url(#ink)">
        <rect x="{SEAL_X}" y="{SEAL_Y}" width="{SEAL_W}" height="{SEAL_H}" rx="5" fill="#FFF7EC"/>
        <rect x="{SEAL_X + 5}" y="{SEAL_Y + 5}" width="{SEAL_W - 10}" height="{SEAL_H - 10}" rx="2" fill="none" stroke="{ink}" stroke-width="1.2"/>
        {chars_svg}
        </g>
    </g>"""


def render_svg(badge: Badge) -> str:
    gradient = GRADIENTS[badge.tier_group]
    unrated = badge.tier == "Unrated"

    if match := TIER_PATTERN.fullmatch(badge.tier):
        headline = f'<tspan font-size="38" font-weight="800">{match[1]}</tspan><tspan font-size="19" font-weight="700" dx="5" letter-spacing="2">{match[2].upper()}</tspan>'
    else:
        # Legend, King and Unrated are shown in caps; an unknown tier is shown as AtCoder wrote it
        word = (
            badge.tier.upper()
            if badge.tier in ("Legend", "King", "Unrated")
            else badge.tier
        )
        headline = f'<tspan font-size="28" font-weight="800" letter-spacing="1.5">{word}</tspan>'

    rating_text = (
        "-"
        if unrated
        else f'{badge.rating} <tspan fill-opacity=".7">(max {badge.highest_rating})</tspan>'
    )
    rows = [
        ("rating", rating_text),
        ("rank", badge.rank),
        ("matches", str(badge.matches)),
    ]
    rows_svg = "\n".join(
        f"""\
    <g class="item" style="animation-delay:{0.25 + i * 0.15:.2f}s">
        <text x="124" y="{94 + i * 17}" class="label">{label}</text>
        <text x="190" y="{94 + i * 17}" class="value">{value}</text>
    </g>"""
        for i, (label, value) in enumerate(rows)
    )

    # tiers move every 200 points of *highest* rating, so promotion is measured on it
    if unrated:
        percentage = 0
        promotion = "first rated contest"
    else:
        next_step = badge.highest_rating - badge.highest_rating % 200 + 200
        # (x % 200) / 200 * 100 rounded half up; round() would round 52.5 down to 52
        percentage = (badge.highest_rating % 200 + 1) // 2
        promotion = f"+{next_step - badge.highest_rating} to {next_tier_name(badge.tier) or 'promote'}"

    bar_end = 35 + (290 - 35) * percentage / 100
    bar_fill = (
        f'<line x1="35" y1="150" x2="{bar_end:.1f}" y2="150" class="rate-bar" pathLength="1"/>'
        if percentage > 0
        else ""
    )

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
        text {{
            fill: #FFFFFF;
            font-family: {SANS};
        }}

        .username {{
            font-size: 15px;
            font-weight: 700;
        }}

        .label {{
            font-size: 12.5px;
            font-weight: 600;
            fill-opacity: 0.78;
        }}

        .value {{
            font-size: 12.5px;
            font-variant-numeric: tabular-nums;
        }}

        .small {{
            font-size: 9.5px;
            fill-opacity: 0.9;
            font-variant-numeric: tabular-nums;
        }}

        .item {{
            animation: fadeIn 0.6s ease-in-out both;
        }}

        .tier {{
            animation: fadeIn 0.6s ease-in-out 0.35s both;
        }}

        .stamp {{
            transform-box: fill-box;
            transform-origin: center;
            transform: rotate(-3deg);
            animation: stamp 0.45s cubic-bezier(0.2, 0.9, 0.3, 1.2) 0.15s both;
        }}

        .rate-bar-container {{
            stroke: #FFFAF0;
            stroke-opacity: 0.38;
            stroke-width: 4;
            stroke-linecap: round;
        }}

        .rate-bar {{
            stroke: #FFFAF0;
            stroke-width: 4;
            stroke-linecap: round;
            stroke-dasharray: 1;
            stroke-dashoffset: 1;
            animation: rateBarAnimation 1.2s ease-in-out 0.7s forwards;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
        }}

        @keyframes stamp {{
            from {{
                opacity: 0;
                transform: rotate(-3deg) scale(1.5);
            }}
        }}

        @keyframes rateBarAnimation {{
            to {{
                stroke-dashoffset: 0;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation: none !important;
            }}

            .rate-bar {{
                stroke-dashoffset: 0;
            }}
        }}
    </style>
    <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="35%">
            <stop offset="10%" stop-color="{gradient[0]}">
                <animate attributeName="stop-opacity" values="0.75;1;0.75" dur="4s" repeatCount="indefinite"/>
            </stop>
            <stop offset="55%" stop-color="{gradient[1]}"/>
            <stop offset="100%" stop-color="{gradient[2]}">
                <animate attributeName="stop-opacity" values="1;0.82;1" dur="4s" repeatCount="indefinite"/>
            </stop>
        </linearGradient>
        <!-- uneven ink: wobble the edges, then knock out a few specks -->
        <filter id="ink" x="-6%" y="-6%" width="112%" height="112%">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="wobble"/>
            <feDisplacementMap in="SourceGraphic" in2="wobble" scale="2.4" xChannelSelector="R" yChannelSelector="G" result="inked"/>
            <feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="9" result="grain"/>
            <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -24 0 0 0 17" result="specks"/>
            <feComposite in="inked" in2="specks" operator="in"/>
        </filter>
    </defs>
    <rect width="350" height="170" rx="10" fill="#1A1A1A"/>
    <rect width="350" height="170" rx="10" fill="url(#gradient)"/>
    <rect width="350" height="170" rx="10" fill="#000000" fill-opacity="0.14"/>
{render_seal(badge)}
    <text x="124" y="36" class="username item">{badge.username}</text>
    <text x="122" y="73" class="tier">{headline}</text>
{rows_svg}
    <line x1="35" y1="150" x2="290" y2="150" class="rate-bar-container"/>
    {bar_fill}
    <text x="297" y="153.5" class="small">{percentage}%</text>
    <text x="290" y="164" text-anchor="end" class="small">{promotion}</text>
</svg>
"""
