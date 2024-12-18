import pytest


@pytest.fixture
def add_fixture():
    return lambda x, y: x + y


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (3, 4, 7),
        (-2, 5, 3),
    ],
)
def test_addition(add_fixture, a, b, expected):
    assert add_fixture(a, b) == expected