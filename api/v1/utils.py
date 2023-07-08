from dataclasses import dataclass
from typing import Optional
from enum import Enum, unique

import requests
from bs4 import BeautifulSoup


@unique
class Tier(Enum):
    UNRATED = "UNRATED"
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
    tier: Tier
    matches: int

    def __str__(self):
        return f"UserData(username={self.username} rank={self.rank} rating={self.rating} highest_rating={self.highest_rating} tier={self.tier.value} matches={self.matches})"

    def __repr__(self):
        return f"UserData(username={self.username} rank={self.rank} rating={self.rating} highest_rating={self.highest_rating} tier={self.tier.value} matches={self.matches})"


def rating_to_tier(rating: str) -> Tier:
    """Convert rating to tier"""
    if rating <= 0:
        return Tier.UNRATED
    elif rating < 400:
        return Tier._9_Kyu
    elif rating < 600:
        return Tier._8_Kyu
    elif rating < 800:
        return Tier._7_Kyu
    elif rating < 1000:
        return Tier._6_Kyu
    elif rating < 1200:
        return Tier._5_Kyu
    elif rating < 1400:
        return Tier._4_Kyu
    elif rating < 1600:
        return Tier._3_Kyu
    elif rating < 1800:
        return Tier._2_Kyu
    elif rating < 2000:
        return Tier._1_Kyu
    elif rating < 2200:
        return Tier._1_Dan
    elif rating < 2400:
        return Tier._2_Dan
    elif rating < 2600:
        return Tier._3_Dan
    elif rating < 2800:
        return Tier._4_Dan
    elif rating < 3000:
        return Tier._5_Dan
    elif rating < 3200:
        return Tier._6_Dan
    elif rating < 3400:
        return Tier._7_Dan
    elif rating < 3600:
        return Tier._8_Dan
    elif rating < 3800:
        return Tier._9_Dan
    elif rating < 4000:
        return Tier._10_Dan
    elif rating < 4200:
        return Tier.Legend
    else:
        return Tier.King


def get_user_data(username: str) -> Optional[UserData]:
    """Get user data from atcoder"""
    url = f"https://atcoder.jp/users/{username}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    # user not found
    if soup.select_one("div.alert.alert-danger"):
        return None

    user_data = soup.select("table.dl-table.mt-2 > tr")

    rank = user_data[0].select_one("td").text
    rating = int(user_data[1].select_one(
        "td > span.user-brown").text)
    highest_rating = int(user_data[2].select_one(
        "td > span.user-brown").text)
    matches = int(user_data[3].select_one("td").text)
    tier = rating_to_tier(rating)

    return UserData(username, rank, rating, highest_rating, tier, matches)
