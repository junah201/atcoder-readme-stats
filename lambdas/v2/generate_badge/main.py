import utils
import fonts


COLORS: dict[str, dict] = {
    "King": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "Legend": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "10 Dan": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "9 Dan": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "8 Dan": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "7 Dan": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "6 Dan": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "5 Dan": {
        "color": "#FF7171",
        "gradient": ["#FF7171", "#D44141", "#870C0C"],
    },
    "4 Dan": {
        "color": "#FFB771",
        "gradient": ["#FFB771", "#CF853D", "#81470E"],
    },
    "3 Dan": {
        "color": "#FFB771",
        "gradient": ["#FFB771", "#CF853D", "#81470E"],
    },
    "2 Dan": {
        "color": "#DFDF80",
        "gradient": ["#DCDC56", "#C3C332", "#84840E"],
    },
    "1 Dan": {
        "color": "#DFDF80",
        "gradient": ["#DCDC56", "#C3C332", "#84840E"],
    },
    "1 Kyu": {
        "color": "#7171FF",
        "gradient": ["#7171FF", "#3B3BCF", "#1212A4"],
    },
    "2 Kyu": {
        "color": "#7171FF",
        "gradient": ["#7171FF", "#3B3BCF", "#1212A4"],
    },
    "3 Kyu": {
        "color": "#80DFDF",
        "gradient": ["#80DFDF", "#4DB7B7", "#206767"],
    },
    "4 Kyu": {
        "color": "#80DFDF",
        "gradient": ["#80DFDF", "#4DB7B7", "#206767"],
    },
    "5 Kyu": {
        "color": "#8AC48A",
        "gradient": ["#8AC48A", "#5EA15E", "#377E37"],
    },
    "6 Kyu": {
        "color": "#8AC48A",
        "gradient": ["#8AC48A", "#5EA15E", "#377E37"],
    },
    "7 Kyu": {
        "color": "#C4A78A",
        "gradient": ["#C4A78A", "#B28659", "#78512A"],
    },
    "8 Kyu": {
        "color": "#C4A78A",
        "gradient": ["#C4A78A", "#B28659", "#78512A"],
    },
    "9 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "10 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "11 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "12 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "13 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "14 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "15 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "16 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "17 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "18 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "19 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "20 Kyu": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
    },
    "Unrated": {
        "color": "#DDDDDD",
        "gradient": ["#DDDDDD", "#BBBBBB", "#828282"],
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
    gradient = colors["gradient"]

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
        @font-face {{
            font-family: 'Freehand';
            src: url(data:font/ttf;charset=utf-8;base64,{Freehand_font});
        }}

        @font-face {{
            font-family: 'Montserrat';
            src: url(data:font/ttf;charset=utf-8;base64,{Montserrat_font});
        }}

        @font-face {{
            font-family: 'Poppins';
            src: url(data:font/ttf;charset=utf-8;base64,{Poppins_font});
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
            font-family: 'Montserrat', sans-serif;
            font-size: 22px;
            font-weight: bold;
            fill: #FFFFFF;
            animation: fadeIn 0.8s ease-in-out forwards;
        }}

        .tier {{
            font-family: 'Freehand', cursive;
            font-size: 32px;
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
            stroke-dasharray: {percentage};
            stroke-dashoffset: {percentage};
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
        <text x="25" y="44" class="username">
            {username}
        </text>
        <text x="325" y="44" text-anchor="end" class="tier">
            {tier}
        </text>
    </g>
    <g>
        <text x="25" y="76" class="info">
            Rank
        </text>
        <text x="100" y="76" fill="#ffffff" class="info-value">
            {rank}
        </text>
    </g>
    <g>
        <text x="25" y="93" class="info">
            Rating
        </text>
        <text x="100" y="93" fill="#ffffff" class="info-value">
            {rating} (max: {highest_rating})
        </text>
    </g>
    <g>
        <text x="25" y="110" class="info">
            Matches
        </text>
        <text x="100" y="110" fill="#ffffff" class="info-value">
            {matches}
        </text>
    </g>
    <g>
        <line x1="25" y1="141" x2="325" y2="141" class="rate-bar-container"/>
    </g>
    <g>
        <line x1="25" y1="141" x2="{percentage}" y2="141" class="rate-bar"/>
    </g>
    <g>
        <text x="325" y="155" text-anchor="end" fill="#ffffff" class="detail">
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
        gradient=gradient,
        percentage=(rating + 200 - next_rating) / 200 * 300 + 25,
        Freehand_font=fonts.Freehand_font,
        Montserrat_font=fonts.Montserrat_font,
        Poppins_font=fonts.Poppins_font
    )

    return {
        'statusCode': 200,
        'body': svg,
        'headers': {
            'Content-Type': 'image/svg+xml',
            'Cache-Control': 'max-age=1800'
        }
    }
