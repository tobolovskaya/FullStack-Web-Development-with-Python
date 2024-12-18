import pytest


@pytest.fixture
def database_connection():
    print("\nВідкриття з'єднання з базою даних")
    db = {"connected": True}
    yield db
    print("\nЗакриття з'єднання з базою даних")
    db["connected"] = False


def test_database_operation(database_connection):
    assert database_connection["connected"] == True
    print("Виконання операції з базою даних")