import pytest

from lambdas.v3.generate_badge import ACCENTS, CELLS, handler
from shared.utils import UserData


def render(mocker, user_data: UserData) -> str:
    mocker.patch("shared.badge.get_user_data", return_value=user_data)
    response = handler({"queryStringParameters": {"name": user_data.username}}, {})
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "image/svg+xml"
    assert response["headers"]["Cache-Control"] == "max-age=1800"
    return response["body"]


@pytest.mark.parametrize(
    ("rating", "filled"),
    [(3782, round(182 / 200 * CELLS)), (1000, 0), (1100, CELLS // 2), (1199, CELLS)],
)
def test_v3_progress_cells(mocker, rating, filled):
    body = render(mocker, UserData("tourist", "1st", rating, 4229, "King", 70))

    assert body.count('class="cell"') == filled
    assert body.count('fill="#21262D"/>') == CELLS - filled


def test_v3_rated_user(mocker):
    body = render(mocker, UserData("tourist", "1st", 3782, 4229, "King", 70))

    assert "atcoder stats tourist" in body
    assert "(max 4229)" in body
    assert "3782/3800" in body
    assert ACCENTS["red"] in body


def test_v3_unrated_user(mocker):
    body = render(mocker, UserData("new_user", "Unrated", 0, 0, "Unrated", 0))

    assert "no rated contest" in body
    assert "(max" not in body
    assert 'class="cell"' not in body
    assert ACCENTS["gray"] in body
