from lambdas.v2.generate_badge import fonts
from shared.badge import Badge, handle_badge_request

GRADIENTS: dict[str, list[str]] = {
    "red": ["#FF7171", "#D44141", "#870C0C"],
    "orange": ["#FFB771", "#CF853D", "#81470E"],
    "yellow": ["#DCDC56", "#C3C332", "#84840E"],
    "blue": ["#7171FF", "#3B3BCF", "#1212A4"],
    "cyan": ["#80DFDF", "#4DB7B7", "#206767"],
    "green": ["#8AC48A", "#5EA15E", "#377E37"],
    "brown": ["#C4A78A", "#B28659", "#78512A"],
    "gray": ["#DDDDDD", "#BBBBBB", "#828282"],
}


def handler(event, _context):
    return handle_badge_request(event, render_svg)


def render_svg(badge: Badge) -> str:
    gradient = GRADIENTS[badge.tier_group]

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
        @font-face {{
            font-family: 'Freehand';
            src: url(data:font/ttf;charset=utf-8;base64,{fonts.Freehand_font});
        }}

        @font-face {{
            font-family: 'Montserrat';
            src: url(data:font/ttf;charset=utf-8;base64,{fonts.Montserrat_font});
        }}

        @font-face {{
            font-family: 'Poppins';
            src: url(data:font/ttf;charset=utf-8;base64,{fonts.Poppins_font});
        }}

        @keyframes delayFadeIn {{
            0% {{
                opacity: 0;
            }}
            60% {{
                opacity: 0;
            }}
            100% {{
                opacity: 1;
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
            font-family: 'Montserrat', sans-serif;
            font-size: 22px;
            font-weight: bold;
            fill: #FFFFFF;
            animation: fadeIn 0.8s ease-in-out forwards;
        }}

        .tier {{
            font-family: 'Freehand', cursive;
            font-size: 40px;
            font-weight: regular;
            fill: #FFFFFF;
            animation: fadeIn 0.8s ease-in-out forwards;
            filter: drop-shadow(2px 2px 2px rgb(0 0 0 / 0.5));
        }}

        .info {{
            font-family: 'Poppins', sans-serif;
            font-size: 12px;
            font-weight: bold;
            fill : rgba(255, 255, 255, 0.75);
            animation: delayFadeIn 1s ease-in-out forwards;
        }}

        .info-value {{
            font-family: 'Poppins', sans-serif;
            font-size: 11px;
            font-weight: bold;
            animation: delayFadeIn 1s ease-in-out forwards;
        }}

        .detail {{
            font-family: 'Poppins', sans-serif;
            font-size: 8px;
            font-weight: regular;
            animation: delayFadeIn 1s ease-in-out forwards;
        }}

        .rate-bar {{
            stroke-dasharray: {badge.bar_end};
            stroke-dashoffset: {badge.bar_end};
            animation: rateBarAnimation 3s forwards ease-in-out;
            animation-delay: 1s;
            border-radius: 3px;
            stroke: #FFFFFF;
            stroke-width: 4;
            stroke-linecap: round;
        }}

        .rate-bar-container {{
            animation: delayFadeIn 1s ease-in-out forwards;
            stroke: #FFFFFF;
            stroke-opacity: 0.5;
            stroke-width: 4;
            stroke-linecap: round;
            filter: drop-shadow(2px 2px 2px rgb(0 0 0 / 0.5));
        }}
    </style>
    <defs>
        <linearGradient id="gradient" x1="224.027" y1="42.8829" x2="353.626" y2="154.755" gradientUnits="userSpaceOnUse">
            <stop stop-color="{gradient[0]}"/>
            <stop offset="0.34375" stop-color="{gradient[1]}"/>
            <stop offset="0.963964" stop-color="{gradient[2]}"/>
        </linearGradient>
    </defs>
    <rect width="350" height="170" fill="url(#gradient)" rx="6"/>
    <g>
        <text x="25" y="44" class="username">{badge.username}</text>
        <text x="325" y="48" text-anchor="end" class="tier">{badge.tier}</text>
    </g>
    <g>
        <text x="25" y="76" class="info">Rank</text>
        <text x="100" y="76" fill="#ffffff" class="info-value">{badge.rank}</text>
    </g>
    <g>
        <text x="25" y="93" class="info">Rating</text>
        <text x="100" y="93" fill="#ffffff" class="info-value">{badge.rating} (max: {badge.highest_rating})</text>
    </g>
    <g>
        <text x="25" y="110" class="info">Matches</text>
        <text x="100" y="110" fill="#ffffff" class="info-value">{badge.matches}</text>
    </g>
    <g>
        <line x1="25" y1="141" x2="325" y2="141" class="rate-bar-container"/>
    </g>
    <g>
        <line x1="25" y1="141" x2="{badge.bar_end}" y2="141" class="rate-bar"/>
    </g>
    <g>
        <text x="325" y="155" text-anchor="end" fill="#ffffff" class="detail">{badge.rating} / {badge.next_rating}</text>
    </g>
</svg>
    """
