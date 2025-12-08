import pytest

from unittest.mock import patch, MagicMock
from src.slack_api import SlackAPI


def test_api_success():
    slack = SlackAPI("token")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"ok": True, "data": 123}

    with patch("requests.get", return_value=mock_resp):
        res = slack.request("test")
        assert res["data"] == 123


def test_api_retry_then_success():
    slack = SlackAPI("token")
    responses = [
        MagicMock(status_code=500),
        MagicMock(status_code=500),
        MagicMock(status_code=200, json=lambda: {"ok": True})
    ]

    with patch("requests.get", side_effect=responses):
        res = slack.request("test")
        assert res["ok"] is True
