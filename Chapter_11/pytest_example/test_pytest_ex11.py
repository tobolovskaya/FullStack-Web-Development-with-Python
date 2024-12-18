import requests


def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()


def test_get_user_data(mocker):
    # Створюємо мок для requests.get
    mock_get = mocker.patch('requests.get')

    # Налаштовуємо поведінку мока
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_get.return_value = mock_response

    # Викликаємо функцію, яку тестуємо
    result = get_user_data(1)

    # Перевіряємо, чи був викликаний requests.get з правильним URL
    mock_get.assert_called_once_with("https://api.example.com/users/1")

    # Перевіряємо результат
    assert result == {"id": 1, "name": "John Doe"}