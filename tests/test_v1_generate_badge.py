import pytest

from lambdas.v1.generate_badge import handler


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
    response = handler(
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
