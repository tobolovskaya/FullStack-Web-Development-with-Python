import requests
from unittest.mock import Mock, patch


def send_request(url):
    response = requests.get(url)
    return response.status_code


def test_send_request():
    mock_get = Mock(return_value=Mock(status_code=200))
    with patch("requests.get", mock_get):
        status_code = send_request("http://example.com")
        assert status_code == 200
        mock_get.assert_called_once_with("http://example.com")