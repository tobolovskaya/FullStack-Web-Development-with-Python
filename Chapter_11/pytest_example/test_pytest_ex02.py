import pytest

@pytest.fixture
def some_data():
    return {"a": 1, "b": 2, "c": 3}

def test_addition(some_data):
    assert some_data["a"] + some_data["b"] == 3

def test_subtraction(some_data):
    assert some_data["c"] - some_data["b"] == 1
