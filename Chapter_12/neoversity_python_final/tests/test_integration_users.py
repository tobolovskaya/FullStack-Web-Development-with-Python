from unittest.mock import patch

from conftest import test_user


def test_get_me(client, get_token):
    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("api/users/me", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "avatar" in data


@patch("src.services.upload_file.UploadFileService.upload_file")
def test_update_avatar_user(mock_upload_file, client, get_token):
    # Мокаємо відповідь від сервісу завантаження файлів
    fake_url = "http://example.com/avatar.jpg"
    mock_upload_file.return_value = fake_url

    # Токен для авторизації
    headers = {"Authorization": f"Bearer {get_token}"}

    # Файл, який буде відправлено
    file_data = {"file": ("avatar.jpg", b"fake image content", "image/jpeg")}

    # Відправка PATCH-запиту
    response = client.patch("/api/users/avatar", headers=headers, files=file_data)

    # Перевірка, що запит був успішним
    assert response.status_code == 200, response.text

    # Перевірка відповіді
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert data["avatar"] == fake_url

    # Перевірка виклику функції upload_file з об'єктом UploadFile
    mock_upload_file.assert_called_once()
