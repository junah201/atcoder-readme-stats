import pytest

from lambdas.v1.generate_badge.main import lambda_handler


@pytest.mark.parametrize(
    "username",
    [
        (
            "tourist"
        ),
        (
            "junah"
        )
    ]
)
def test_v1_generate_badge(username):
    response = lambda_handler(
        {
            "queryStringParameters": {
                "name": username
            }
        },
        {}
    )
    assert response["statusCode"] == 200
    assert response["body"] is not None
    assert response["headers"]["Content-Type"] == "image/svg+xml"
    assert response["headers"]["Cache-Control"] == "max-age=1800"
