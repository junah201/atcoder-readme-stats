import email.message
import http.client
import urllib.error

import pytest

from shared.utils import (
    REQUEST_TIMEOUT,
    USER_AGENT,
    AtCoderUnavailableError,
    get_user_data,
)

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


class FakeResponse:
    """Stands in for the object urllib.request.urlopen returns"""

    def __init__(
        self,
        body: bytes,
        status: int = 200,
        content_type: str = "text/html; charset=utf-8",
    ):
        self.status = status
        self.headers = email.message.Message()
        self.headers["Content-Type"] = content_type
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://atcoder.jp/users/x", code, "error", email.message.Message(), None
    )


def mock_urlopen(mocker, **kwargs):
    return mocker.patch("urllib.request.urlopen", **kwargs)


def test_get_user_data_success(mocker):
    mock = mock_urlopen(mocker, return_value=FakeResponse(HTML_VALID_USER.encode()))

    result = get_user_data("tourist")

    request = mock.call_args.args[0]
    assert request.full_url == "https://atcoder.jp/users/tourist?lang=en"
    assert request.get_header("User-agent") == USER_AGENT
    assert mock.call_args.kwargs["timeout"] == REQUEST_TIMEOUT
    assert result is not None
    assert result.username == "tourist"
    assert result.rank == "1st"
    assert result.rating == 3782
    assert result.highest_rating == 4229
    assert result.tier == "King"
    assert result.matches == 70


def test_get_user_data_inactive_user_without_rank(mocker):
    # AtCoder drops the Rank row for users inactive in rated contests
    html = HTML_VALID_USER.replace(
        '<tr><th class="no-break">Rank</th><td>1st</td></tr>', ""
    )
    mock_urlopen(mocker, return_value=FakeResponse(html.encode()))

    result = get_user_data("tourist")

    assert result is not None
    assert result.rank == "-"
    assert result.rating == 3782
    assert result.highest_rating == 4229
    assert result.tier == "King"
    assert result.matches == 70


def test_get_user_data_not_found(mocker):
    # urlopen raises HTTPError for 404 instead of returning a response
    mock_urlopen(mocker, side_effect=http_error(404))

    assert get_user_data("invalid_username") is None


def test_get_user_data_not_found_page(mocker):
    mock_urlopen(mocker, return_value=FakeResponse(HTML_NOT_FOUND.encode()))

    assert get_user_data("invalid_username") is None


def test_get_user_data_unrated(mocker):
    mock_urlopen(mocker, return_value=FakeResponse(HTML_UNRATED.encode()))

    result = get_user_data("new_user")

    assert result is not None
    assert result.username == "new_user"
    assert result.rank == "Unrated"
    assert result.rating == 0
    assert result.highest_rating == 0
    assert result.tier == "Unrated"
    assert result.matches == 0


@pytest.mark.parametrize(
    "error",
    [
        urllib.error.URLError("Name or service not known"),
        TimeoutError("timed out"),
        ConnectionResetError("connection reset"),
        http.client.IncompleteRead(b""),
    ],
)
def test_get_user_data_network_error(mocker, error):
    mock_urlopen(mocker, side_effect=error)

    with pytest.raises(AtCoderUnavailableError):
        get_user_data("tourist")


@pytest.mark.parametrize("status_code", [429, 500, 503])
def test_get_user_data_error_status(mocker, status_code):
    mock_urlopen(mocker, side_effect=http_error(status_code))

    with pytest.raises(AtCoderUnavailableError):
        get_user_data("tourist")


def test_get_user_data_unexpected_success_status(mocker):
    mock_urlopen(mocker, return_value=FakeResponse(HTML_UNRATED.encode(), status=203))

    with pytest.raises(AtCoderUnavailableError):
        get_user_data("tourist")


@pytest.mark.parametrize(
    ("content_type", "encoding"),
    [
        ("text/html; charset=utf-8", "utf-8"),
        ("text/html; charset=Shift_JIS", "shift_jis"),
        ("text/html; charset=EUC-JP", "euc_jp"),
        # no charset or an unknown one falls back to UTF-8
        ("text/html", "utf-8"),
        ("text/html; charset=not-a-charset", "utf-8"),
    ],
)
def test_get_user_data_decodes_with_response_charset(mocker, content_type, encoding):
    html = HTML_VALID_USER.replace("King", "初段").replace("1st", "１位")
    mock_urlopen(
        mocker,
        return_value=FakeResponse(html.encode(encoding), content_type=content_type),
    )

    result = get_user_data("tourist")

    assert result is not None
    assert result.tier == "初段"
    assert result.rank == "１位"
