import pytest

from layers.util_layer.python.utils import get_user_data


@pytest.mark.parametrize(
    "username, is_valid",
    [
        (
            "tourist",
            True
        ),
        (
            "junah",
            True
        ),
        (
            "invalid_username_20240701",
            False
        )
    ]
)
def test_get_user_data(username, is_valid):
    user_data = get_user_data(username)
    assert (user_data is not None) == is_valid
    assert user_data == None or user_data.username == username
