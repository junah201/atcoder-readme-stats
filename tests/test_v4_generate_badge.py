import pytest

from lambdas.v4.generate_badge import KANJI, handler, next_tier_name, seal_text
from shared.utils import UserData


def render(mocker, user_data: UserData) -> str:
    mocker.patch("shared.badge.get_user_data", return_value=user_data)
    response = handler({"queryStringParameters": {"name": user_data.username}}, {})
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "image/svg+xml"
    assert response["headers"]["Cache-Control"] == "max-age=1800"
    return response["body"]


@pytest.mark.parametrize(
    ("tier", "text"),
    [
        ("20 Kyu", "二十級"),
        ("10 Kyu", "十級"),
        ("5 Kyu", "五級"),
        ("1 Kyu", "一級"),
        ("1 Dan", "初段"),
        ("4 Dan", "四段"),
        ("10 Dan", "十段"),
        ("Legend", "皆伝"),
        ("King", "極伝"),
        ("Unrated", "未定"),
    ],
)
def test_seal_text(tier, text):
    assert seal_text(tier) == text
    # every character must have an outline, since the seal does not rely on fonts
    assert all(char in KANJI for char in text)


@pytest.mark.parametrize(
    ("tier", "name"),
    [
        ("5 Kyu", "4 Kyu"),
        ("1 Kyu", "1 Dan"),
        ("4 Dan", "5 Dan"),
        ("10 Dan", "Legend"),
        ("Legend", "King"),
        ("King", None),
    ],
)
def test_next_tier_name(tier, name):
    assert next_tier_name(tier) == name


def test_v4_king(mocker):
    body = render(mocker, UserData("tourist", "1st", 3782, 4229, "King", 70))

    # same numbers AtCoder shows: "+171 to promote" from the highest rating 4229
    assert "+171 to promote" in body
    assert ">15%<" in body  # 29 / 200 = 14.5%, rounded half up
    assert ">KING<" in body
    assert "(max 4229)" in body
    assert body.count("<path ") == 2


def test_v4_dan(mocker):
    body = render(mocker, UserData("orange_fox", "512th", 2633, 2710, "4 Dan", 97))

    assert "+90 to 5 Dan" in body
    assert ">4</tspan>" in body
    assert ">DAN</tspan>" in body


def test_v4_unrated(mocker):
    body = render(mocker, UserData("new_user", "Unrated", 0, 0, "Unrated", 0))

    assert "first rated contest" in body
    assert ">0%<" in body
    assert 'class="rate-bar"' not in body
    assert "(max" not in body


def test_v4_percentage_rounds_half_up(mocker):
    body = render(mocker, UserData("legend_dp", "3rd", 3950, 4105, "Legend", 120))

    assert ">53%<" in body
    assert "+95 to King" in body
