import pytest


@pytest.fixture(params=[1, 2, 3])
def numbers(request):
    return request.param


def test_multiplication(numbers):
    assert numbers * 2 < 7
