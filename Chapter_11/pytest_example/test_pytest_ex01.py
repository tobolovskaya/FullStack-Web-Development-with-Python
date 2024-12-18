import pytest


def test_basic_assertions():
    # Перевірка рівності
    assert 1 == 1

    # Перевірка нерівності
    assert 1 != 2

    # Перевірка істинності
    assert 3 > 2

    # Перевірка хибності
    assert not 2 > 3

    # Перевірка наявності в колекції
    assert "h" in "hello"

    # Перевірка типу
    assert isinstance(1, int)

    # Перевірка виключення
    with pytest.raises(ZeroDivisionError):
        1 / 0

    # Перевірка наближеної рівності для чисел з плаваючою комою
    assert pytest.approx(0.1 + 0.2) == 0.3

    # Перевірка частини рядка
    assert "hello" in "hello world"

    # Перевірка довжини колекції
    assert len([1, 2, 3]) == 3


# Приклад використання assert для порівняння складних об'єктів
def test_complex_assertions():
    person1 = {"name": "Alice", "age": 30}
    person2 = {"name": "Alice", "age": 30}
    assert person1 == person2


# Приклад використання assert для перевірки виключень з контекстом
def test_exception_message():
    with pytest.raises(ValueError) as exc_info:
		    # щось дає виключення
        raise ValueError("Неправильне значення")
    assert str(exc_info.value) == "Неправильне значення"