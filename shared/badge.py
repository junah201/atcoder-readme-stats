from collections.abc import Callable
from dataclasses import dataclass
from html import escape

from shared.utils import AtCoderUnavailableError, get_user_data, is_valid_username

TIER_GROUPS: dict[str, list[str]] = {
    "red": ["King", "Legend", *(f"{n} Dan" for n in range(5, 11))],
    "orange": ["3 Dan", "4 Dan"],
    "yellow": ["1 Dan", "2 Dan"],
    "blue": ["1 Kyu", "2 Kyu"],
    "cyan": ["3 Kyu", "4 Kyu"],
    "green": ["5 Kyu", "6 Kyu"],
    "brown": ["7 Kyu", "8 Kyu"],
    "gray": ["Unrated", *(f"{n} Kyu" for n in range(9, 21))],
}

TIER_TO_GROUP: dict[str, str] = {
    tier: group for group, tiers in TIER_GROUPS.items() for tier in tiers
}


@dataclass
class Badge:
    """Values to render in a badge; string fields are already HTML-escaped"""

    username: str
    rank: str
    rating: int
    highest_rating: int
    tier: str
    tier_group: str
    matches: int
    next_rating: int
    # x coordinate where the rating progress bar ends (bar spans 25..325)
    bar_end: float


def handle_badge_request(event, render_svg: Callable[[Badge], str]) -> dict:
    query_string_parameters = event.get("queryStringParameters") or {}
    username = query_string_parameters.get("name")

    if not username:
        return {"statusCode": 400, "body": "name parameter is required"}

    if not is_valid_username(username):
        return {"statusCode": 400, "body": "invalid name parameter"}

    try:
        user_data = get_user_data(username)
    except AtCoderUnavailableError:
        return {
            "statusCode": 502,
            "body": "failed to fetch data from AtCoder",
            "headers": {"Cache-Control": "no-store"},
        }

    if not user_data:
        return {"statusCode": 404, "body": f"user({username}) not found"}

    rating = user_data.rating
    badge = Badge(
        username=escape(username),
        rank=escape(user_data.rank),
        rating=rating,
        highest_rating=user_data.highest_rating,
        tier=escape(user_data.tier),
        tier_group=TIER_TO_GROUP.get(user_data.tier, "gray"),
        matches=user_data.matches,
        next_rating=rating - rating % 200 + 200,
        bar_end=rating % 200 / 200 * 300 + 25,
    )

    return {
        "statusCode": 200,
        "body": render_svg(badge),
        "headers": {"Content-Type": "image/svg+xml", "Cache-Control": "max-age=1800"},
    }
