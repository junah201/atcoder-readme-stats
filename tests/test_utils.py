import requests

from shared.utils import get_user_data

HTML_VALID_USER = """
<html>
<body>
    <table class="dl-table mt-2">
        <tr><th class="no-break">Rank</th><td>1st</td></tr>
        <tr><th class="no-break">Rating</th><td><span class='user-red'>3782</span></td></tr>
        <tr>
            <th class="no-break">Highest Rating</th>
            <td>
                <span class='user-red'>4229</span>
                <span class="gray">―</span>
                <span class="bold">King</span>
                <span class="gray">(+171 to promote)</span>
            </td>
        </tr>
        <tr><th class="no-break">Rated Matches</th><td>70</td></tr>
        <tr><th class="no-break">Last Competed</th><td>2025/12/28</td></tr>
    </table>
</body>
</html>
"""

HTML_NOT_FOUND = """
<html>
<body>
    <div class="alert alert-danger alert-dismissible col-sm-12 fade in" role="alert">
        <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span> User not found.
    </div>
</body>
</html>
"""

HTML_UNRATED = """
<html>
<body>
    <div class="col-md-9 col-sm-12">
        <h3>Contest Status</h3>
    </div>
</body>
</html>
"""


def test_get_user_data_success(mocker):
    mock_get = mocker.patch("requests.get")

    mock_response = mocker.Mock()
    mock_response.text = HTML_VALID_USER
    mock_get.return_value = mock_response

    result = get_user_data("tourist")

    assert result is not None
    assert result.username == "tourist"
    assert result.rank == "1st"
    assert result.rating == 3782
    assert result.highest_rating == 4229
    assert result.tier == "King"
    assert result.matches == 70


def test_get_user_data_not_found(mocker):
    mock_get = mocker.patch("requests.get")

    mock_response = mocker.Mock()
    mock_response.text = HTML_NOT_FOUND
    mock_get.return_value = mock_response

    result = get_user_data("invalid_username")

    assert result is None


def test_get_user_data_unrated(mocker):
    mock_get = mocker.patch("requests.get")

    mock_response = mocker.Mock()
    mock_response.text = HTML_UNRATED
    mock_get.return_value = mock_response

    result = get_user_data("new_user")

    assert result is not None
    assert result.username == "new_user"
    assert result.rank == "Unrated"
    assert result.rating == 0
    assert result.highest_rating == 0
    assert result.tier == "Unrated"
    assert result.matches == 0


def test_get_user_data_network_error(mocker):
    mock_get = mocker.patch("requests.get")

    mock_get.side_effect = requests.RequestException("Timeout or Connection Error")

    result = get_user_data("tourist")

    assert result is None
