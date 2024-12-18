import pytest


@pytest.fixture(scope="module")
def module_fixture():
    print("\nСтворення module_fixture")
    yield "module_data"
    print("\nЗнищення module_fixture")


@pytest.fixture(scope="function")
def function_fixture():
    print("\nСтворення function_fixture")
    yield "function_data"
    print("\nЗнищення function_fixture")


def test_1(module_fixture, function_fixture):
    print(f"Виконання test_1 з {module_fixture} та {function_fixture}")


def test_2(module_fixture, function_fixture):
    print(f"Виконання test_2 з {module_fixture} та {function_fixture}")