import http.client
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum, unique

from bs4 import BeautifulSoup

# AtCoder usernames: 3-16 characters of alphanumerics and underscores
USERNAME_PATTERN = re.compile(r"[A-Za-z0-9_]{3,16}")

# seconds; must stay under the Lambda timeout (10s)
REQUEST_TIMEOUT = 8

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


def is_valid_username(username: str) -> bool:
    return USERNAME_PATTERN.fullmatch(username) is not None


@unique
class Tier(Enum):
    Unrated = "Unrated"
    _20_Kyu = "20 Kyu"
    _19_Kyu = "19 Kyu"
    _18_Kyu = "18 Kyu"
    _17_Kyu = "17 Kyu"
    _16_Kyu = "16 Kyu"
    _15_Kyu = "15 Kyu"
    _14_Kyu = "14 Kyu"
    _13_Kyu = "13 Kyu"
    _12_Kyu = "12 Kyu"
    _11_Kyu = "11 Kyu"
    _10_Kyu = "10 Kyu"
    _9_Kyu = "9 Kyu"
    _8_Kyu = "8 Kyu"
    _7_Kyu = "7 Kyu"
    _6_Kyu = "6 Kyu"
    _5_Kyu = "5 Kyu"
    _4_Kyu = "4 Kyu"
    _3_Kyu = "3 Kyu"
    _2_Kyu = "2 Kyu"
    _1_Kyu = "1 Kyu"
    _1_Dan = "1 Dan"
    _2_Dan = "2 Dan"
    _3_Dan = "3 Dan"
    _4_Dan = "4 Dan"
    _5_Dan = "5 Dan"
    _6_Dan = "6 Dan"
    _7_Dan = "7 Dan"
    _8_Dan = "8 Dan"
    _9_Dan = "9 Dan"
    _10_Dan = "10 Dan"
    Legend = "Legend"
    King = "King"


@dataclass
class UserData:
    username: str
    rank: str
    rating: int
    highest_rating: int
    tier: str
    matches: int


class AtCoderUnavailableError(Exception):
    """Raised when AtCoder cannot be reached or responds with an unexpected status"""


def fetch_html(url: str) -> str | None:
    """Fetch a page as text, or None when it does not exist (404)"""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            if response.status != 200:
                raise AtCoderUnavailableError(f"{url} responded with {response.status}")
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise AtCoderUnavailableError(f"{url} responded with {e.code}") from e
    # URLError, timeouts and dropped connections are all OSError subclasses
    except (OSError, http.client.HTTPException) as e:
        raise AtCoderUnavailableError(f"request to {url} failed") from e

    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        # unknown charset in Content-Type; AtCoder serves UTF-8
        return body.decode("utf-8", errors="replace")


def get_user_data(username: str) -> UserData | None:
    """Get user data from atcoder"""
    # lang=en pins the row labels parsed below to English
    html = fetch_html(f"https://atcoder.jp/users/{username}?lang=en")

    # user not found
    if html is None:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # user not found
    if soup.select_one("div.alert.alert-danger"):
        return None

    # map each row by its label; rows come and go (e.g. Rank is dropped for inactive users)
    rows = {
        th.get_text(strip=True): tr.select_one("td")
        for tr in soup.select("table.dl-table.mt-2 > tr")
        if (th := tr.select_one("th"))
    }

    # user is unrated
    if "Rating" not in rows:
        return UserData(username, "Unrated", 0, 0, "Unrated", 0)

    rank_cell = rows.get("Rank")
    rank = rank_cell.get_text(" ", strip=True) if rank_cell else "-"
    rating = int(rows["Rating"].select_one("span").get_text(strip=True))
    highest_rating = int(rows["Highest Rating"].select_one("span").get_text(strip=True))
    tier = rows["Highest Rating"].select_one("span.bold").get_text(strip=True)
    matches = int(rows["Rated Matches"].get_text(strip=True))

    return UserData(username, rank, rating, highest_rating, tier, matches)
