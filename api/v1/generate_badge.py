import utils

COLORS: dict[str, dict] = {
    "King": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "Legend": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "10 Dan": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "9 Dan": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "8 Dan": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "7 Dan": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "6 Dan": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "5 Dan": {
        "lighter": "#ffa4a4",
        "color": "#FF7171",
        "darker": "#FF5E5E"
    },
    "4 Dan": {
        "lighter": "#FFD1A4",
        "color": "#FFB771",
        "darker": "#FFAD5E"
    },
    "3 Dan": {
        "lighter": "#FFD1A4",
        "color": "#FFB771",
        "darker": "#FFAD5E"
    },
    "2 Dan": {
        "lighter": "#F6F6DB",
        "color": "#DFDF80",
        "darker": "#DBDB71"
    },
    "1 Dan": {
        "lighter": "#F6F6DB",
        "color": "#DFDF80",
        "darker": "#DBDB71"
    },
    "1 Kyu": {
        "lighter": "#a4a4ff",
        "color": "#7171FF",
        "darker": "#5E5EFF"
    },
    "2 Kyu": {
        "lighter": "#a4a4ff",
        "color": "#7171FF",
        "darker": "#5E5EFF"
    },
    "3 Kyu": {
        "lighter": "#a9e9e9",
        "color": "#80DFDF",
        "darker": "#71DBDB"
    },
    "4 Kyu": {
        "lighter": "#a9e9e9",
        "color": "#80DFDF",
        "darker": "#71DBDB"
    },
    "5 Kyu": {
        "lighter": "#D4E9D4",
        "color": "#8AC48A",
        "darker": "#7EBE7E"
    },
    "6 Kyu": {
        "lighter": "#D4E9D4",
        "color": "#8AC48A",
        "darker": "#7EBE7E"
    },
    "7 Kyu": {
        "lighter": "#d5c1ac",
        "color": "#C4A78A",
        "darker": "#BE9E7E"
    },
    "8 Kyu": {
        "lighter": "#d5c1ac",
        "color": "#C4A78A",
        "darker": "#BE9E7E"
    },
    "9 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "10 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "11 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "12 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "13 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "14 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "15 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "16 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "17 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "18 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "19 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "20 Kyu": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    },
    "Unrated": {
        "lighter": "#e9e9e9",
        "color": "#DDDDDD",
        "darker": "#D1D1D1"
    }
}


def lambda_handler(event, context):
    query_string_parameters = event.get("queryStringParameters", {})

    if not query_string_parameters:
        return {
            'statusCode': 400,
            'body': "name parameter is required"
        }

    username = event.get("queryStringParameters", {}).get("name", None)

    if not username:
        return {
            'statusCode': 400,
            'body': "name parameter is required"
        }

    user_data = utils.get_user_data(username)

    if not user_data:
        return {
            'statusCode': 404,
            'body': f"user({username}) not found"
        }

    tier = user_data.tier
    rank = user_data.rank
    rating = user_data.rating
    highest_rating = user_data.highest_rating
    matches = user_data.matches
    next_rating = user_data.rating - user_data.rating % 200 + 200

    colors = COLORS[tier]
    color = colors["color"]
    darker = colors["darker"]
    lighter = colors["lighter"]

    svg = '''\
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
                stroke-dashoffset: {percentage};
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
            stroke-dasharray: {percentage};
            stroke-dashoffset: {percentage};
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
        <text x="25" y="44" fill="#ffffff" class = "username">
            {username}
        </text>
        <text x="325" y="55"  fill="#F6F6DB" text-anchor="end" class = "tier">
            {tier}
        </text>
    </g>
    <g>
        <text x="25" y="76" fill="#ffffff" class = "info">
            Rank
        </text>
        <text x="100" y="76" fill="#ffffff" class = "info-value">
            {rank}
        </text>
    </g>
    <g>
        <text x="25" y="93" fill="#ffffff" class = "info">
            Rating
        </text>
        <text x="100" y="93" fill="#ffffff" class = "info-value">
            {rating} (max: {highest_rating})
        </text>
    </g>
    <g>
        <text x="25" y="110" fill="#ffffff" class = "info">
            Matches
        </text>
        <text x="100" y="110" fill="#ffffff" class = "info-value">
            {matches}
        </text>
    </g>
    <g>
        <line x1="25" y1="135" x2="325" y2="135" stroke="{lighter}" stroke-width="8" rx="3" class="rate-bar-container" />
    </g>
    <g>
        <line x1="25" y1="135" x2="{percentage}" y2="135" stroke="#ffffff" stroke-width="8" rx="3" class="rate-bar" />
    </g>
    <g>
        <text x="325" y="155" text-anchor="end" fill="#ffffff" class = "detail">
            {rating} / {next_rating}
        </text>
    </g>
</svg>
    '''.format(
        username=username,
        tier=tier,
        rank=rank,
        rating=rating,
        highest_rating=highest_rating,
        next_rating=next_rating,
        matches=matches,
        color=color,
        darker=darker,
        lighter=lighter,
        percentage=(rating + 200 - next_rating) / 200 * 300 + 25
    )

    return {
        'statusCode': 200,
        'body': svg,
        'headers': {
            'Content-Type': 'image/svg+xml',
            'Cache-Control': 'max-age=1800'
        }
    }
