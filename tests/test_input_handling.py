import pytest

import lambdas.v1.generate_badge as v1
import lambdas.v2.generate_badge as v2
from shared.utils import AtCoderUnavailableError, UserData, is_valid_username

MODULES = [v1, v2]


@pytest.mark.parametrize("username", ["abc", "tourist", "junah", "A_b_9", "a" * 16])
def test_is_valid_username_accepts(username):
    assert is_valid_username(username)


@pytest.mark.parametrize(
    "username",
    [
        "",
        "ab",
        "a" * 17,
        "tourist/history",
        "tourist#<script>",
        "tourist?x=1",
        "<svg>",
        "한글이름",
    ],
)
def test_is_valid_username_rejects(username):
    assert not is_valid_username(username)


@pytest.mark.parametrize("module", MODULES)
@pytest.mark.parametrize(
    "username", ["tourist#<script>alert(1)</script>", "tourist/history", "ab"]
)
def test_handler_rejects_invalid_username(mocker, module, username):
    mock_get_user_data = mocker.patch.object(module, "get_user_data")

    response = module.handler({"queryStringParameters": {"name": username}}, {})

    assert response["statusCode"] == 400
    mock_get_user_data.assert_not_called()


@pytest.mark.parametrize("module", MODULES)
def test_handler_escapes_scraped_values(mocker, module):
    mocker.patch.object(
        module,
        "get_user_data",
        return_value=UserData("tourist", "<b>1st</b>", 3782, 4229, "King", 70),
    )

    response = module.handler({"queryStringParameters": {"name": "tourist"}}, {})

    assert response["statusCode"] == 200
    assert "<b>1st</b>" not in response["body"]
    assert "&lt;b&gt;1st&lt;/b&gt;" in response["body"]


@pytest.mark.parametrize("module", MODULES)
def test_handler_returns_uncached_502_when_atcoder_unavailable(mocker, module):
    mocker.patch.object(module, "get_user_data", side_effect=AtCoderUnavailableError())

    response = module.handler({"queryStringParameters": {"name": "tourist"}}, {})

    assert response["statusCode"] == 502
    assert response["headers"]["Cache-Control"] == "no-store"
