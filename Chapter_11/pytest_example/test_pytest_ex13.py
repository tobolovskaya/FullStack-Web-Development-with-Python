class Config:
    @property
    def api_key(self):
        return "real_api_key"


def get_api_key(config):
    return config.api_key


def test_get_api_key(mocker):
    config = Config()

    # Мокаємо властивість api_key
    mocker.patch.object(
        Config,
        "api_key",
        new_callable=mocker.PropertyMock,
        return_value="mocked_api_key",
    )

    result = get_api_key(config)

    assert result == "mocked_api_key"