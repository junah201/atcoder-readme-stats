from shared.badge import Badge, handle_badge_request

COLORS: dict[str, dict[str, str]] = {
    "red": {"lighter": "#ffa4a4", "color": "#FF7171", "darker": "#FF5E5E"},
    "orange": {"lighter": "#FFD1A4", "color": "#FFB771", "darker": "#FFAD5E"},
    "yellow": {"lighter": "#F6F6DB", "color": "#DFDF80", "darker": "#DBDB71"},
    "blue": {"lighter": "#a4a4ff", "color": "#7171FF", "darker": "#5E5EFF"},
    "cyan": {"lighter": "#a9e9e9", "color": "#80DFDF", "darker": "#71DBDB"},
    "green": {"lighter": "#D4E9D4", "color": "#8AC48A", "darker": "#7EBE7E"},
    "brown": {"lighter": "#d5c1ac", "color": "#C4A78A", "darker": "#BE9E7E"},
    "gray": {"lighter": "#e9e9e9", "color": "#DDDDDD", "darker": "#D1D1D1"},
}


def handler(event, _context):
    return handle_badge_request(event, render_svg)


def render_svg(badge: Badge) -> str:
    colors = COLORS[badge.tier_group]
    color = colors["color"]
    darker = colors["darker"]
    lighter = colors["lighter"]

    return f"""\
<?xml version="1.0" encoding="UTF-8"?>
<svg
    width="350"
    height="170"
    viewBox="0 0 350 170"
    fill="none"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xml:space="preserve"
>
    <style type="text/css">
        @import url('https://fonts.googleapis.com/css2?family=Inter');

        @keyframes delayFadeIn {{
            0%{{
                opacity:0
            }}
            60%{{
                opacity:0
            }}
            100%{{
                opacity:1
            }}
        }}
        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
        @keyframes rateBarAnimation {{
            0% {{
                stroke-dashoffset: {badge.bar_end};
            }}
            75% {{
                stroke-dashoffset: 25;
            }}
            100% {{
                stroke-dashoffset: 25;
            }}
        }}

        .username {{
            font-family: 'Inter', sans-serif;
            font-size: 24px;
            font-weight: bold;
            animation: fadeIn 0.8s ease-in-out forwards;
        }}
        .tier {{
            font-family: 'Inter', sans-serif;
            font-size: 40px;
            font-weight: bold;
            color: {lighter};
            animation: fadeIn 0.8s ease-in-out forwards;
        }}
        .info {{
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            animation: delayFadeIn 1s ease-in-out forwards;
        }}
        .info-value {{
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            animation: delayFadeIn 1s ease-in-out forwards;
        }}
        .detail {{
            font-family: 'Inter', sans-serif;
            font-size: 10px;
            animation: delayFadeIn 1s ease-in-out forwards;
        }}
        .rate-bar {{
            stroke-dasharray: {badge.bar_end};
            stroke-dashoffset: {badge.bar_end};
            animation: rateBarAnimation 3s forwards ease-in-out;
            animation-delay: 1s;
        }}
        .rate-bar-container {{
            animation: delayFadeIn 1s ease-in-out forwards;
        }}
    </style>
    <defs>
        <linearGradient id="gradient" x1="0" y1="0" x2="286.703" y2="200.752" gradientUnits="userSpaceOnUse">
            <stop stop-color="{darker}"/>
            <stop offset="0.8" stop-color="{darker}"/>
            <stop offset="1" stop-color="{color}"/>
        </linearGradient>
    </defs>
    <rect width="350" height="170" fill="url(#gradient)" rx = "6"/>
    <g>
        <text x="25" y="44" fill="#ffffff" class = "username">{badge.username}</text>
        <text x="325" y="55"  fill="#F6F6DB" text-anchor="end" class = "tier">{badge.tier}</text>
    </g>
    <g>
        <text x="25" y="76" fill="#ffffff" class = "info">Rank</text>
        <text x="100" y="76" fill="#ffffff" class = "info-value">{badge.rank}</text>
    </g>
    <g>
        <text x="25" y="93" fill="#ffffff" class = "info">Rating</text>
        <text x="100" y="93" fill="#ffffff" class = "info-value">{badge.rating} (max: {badge.highest_rating})</text>
    </g>
    <g>
        <text x="25" y="110" fill="#ffffff" class = "info">Matches</text>
        <text x="100" y="110" fill="#ffffff" class = "info-value">{badge.matches}</text>
    </g>
    <g>
        <line x1="25" y1="135" x2="325" y2="135" stroke="{lighter}" stroke-width="8" rx="3" class="rate-bar-container" />
    </g>
    <g>
        <line x1="25" y1="135" x2="{badge.bar_end}" y2="135" stroke="#ffffff" stroke-width="8" rx="3" class="rate-bar" />
    </g>
    <g>
        <text x="325" y="155" text-anchor="end" fill="#ffffff" class = "detail">{badge.rating} / {badge.next_rating}</text>
    </g>
</svg>
    """
