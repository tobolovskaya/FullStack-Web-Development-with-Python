import requests


def send_request(url):
    response = requests.get(url)
    return response.status_code


def test_send_request(mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    status_code = send_request('http://example.com')
    assert status_code == 200
    mock_get.assert_called_once_with('http://example.com')