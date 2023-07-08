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
}


def lambda_handler(event, context):
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
    next_rating = user_data.rating + user_data.rating % 200

    colors = COLORS[tier]
    color = colors["color"]
    darker = colors["darker"]
    lighter = colors["lighter"]

    svg = '''\
    <svg width="350" height="170" viewBox="0 0 350 170" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter');

                .username {{
                    font-family: 'Inter', sans-serif;
                    font-size: 20px;
                    font-weight: bold;
                }}
                .tier {{
                    font-family: 'Inter', sans-serif;
                    font-size: 40px;
                    font-weight: bold;
                    color: {lighter};
                }}
                .info {{
                    font-family: 'Inter', sans-serif;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .detail {{
                    font-family: 'Inter', sans-serif;
                    font-size: 8px;
                    font-weight: bold;
                }}
            </style>
        </defs>
        <linearGradient id="gradient" x1="0" y1="0" x2="286.703" y2="200.752" gradientUnits="userSpaceOnUse">
            <stop stop-color="{darker}"/>
            <stop offset="0.8" stop-color="{darker}"/>
            <stop offset="1" stop-color="{color}"/>
        </linearGradient>
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
                rank
            </text>
            <text x="100" y="76" fill="#ffffff" class = "info">
                {rank}
            </text>
        </g>
        <g>
            <text x="25" y="93" fill="#ffffff" class = "info">
                rating
            </text>
            <text x="100" y="93" fill="#ffffff" class = "info">
                {rating} (max: {highest_rating})
            </text>
        </g>
        <g>
            <text x="25" y="110" fill="#ffffff" class = "info">
                matches
            </text>
            <text x="100" y="110" fill="#ffffff" class = "info">
                {matches}
            </text>
        </g>
        <rect x="25" y="133" width="300" height="12" rx="3" fill="{lighter}"/>
        <rect x="25" y="133" width="91" height="12" rx="3" fill="white"/>
        <g>
            <text x="285" y="155" fill="#ffffff" class = "detail">
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
        lighter=lighter
    )

    return {
        'statusCode': 200,
        'body': svg,
        'headers': {
            'Content-Type': 'image/svg+xml',
        }
    }
