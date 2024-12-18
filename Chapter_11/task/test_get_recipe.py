import pytest
from unittest.mock import patch, mock_open


def get_recipe(path, search_id):
    result = None
    with open(path, "r") as f:
        for line in f:
            (id, name, *recipes) = line.strip().split(",")
            if id == search_id:
                result = {"id": id, "name": name, "ingredients": recipes}
    return result


@pytest.fixture
def mock_recipes_data():
    return (
        "60b90c1c13067a15887e1ae1,Herbed Baked Salmon,4 lemons,1 large red onion,2 tablespoons chopped fresh basil\n"
        "60b90c2413067a15887e1ae2,Lemon Pancakes,2 tablespoons baking powder,1 cup vanilla-flavored almond milk,1 lemon\n"
        "60b90c2e13067a15887e1ae3,Chicken and Cold Noodles,6 ounces dry Chinese noodles,1 tablespoon sesame oil,3 tablespoons soy sauce"
    )


@pytest.fixture
def mock_file(mock_recipes_data):
    return mock_open(read_data=mock_recipes_data)


@pytest.mark.parametrize(
    "uuid,expected_name,expected_ingredients",
    [
        (
            "60b90c1c13067a15887e1ae1",
            "Herbed Baked Salmon",
            ["4 lemons", "1 large red onion", "2 tablespoons chopped fresh basil"],
        ),
        (
            "60b90c2413067a15887e1ae2",
            "Lemon Pancakes",
            [
                "2 tablespoons baking powder",
                "1 cup vanilla-flavored almond milk",
                "1 lemon",
            ],
        ),
    ],
)
def test_get_existing_recipe(uuid, expected_name, expected_ingredients, mock_file):
    filename = "fake.csv"
    with patch("builtins.open", mock_file):
        result = get_recipe(filename, uuid)
        assert result["id"] == uuid
        assert result["name"] == expected_name
        assert result["ingredients"] == expected_ingredients


def test_get_nonexistent_recipe(mock_file):
    uuid = "nonexistent_id"
    filename = "fake.csv"
    with patch("builtins.open", mock_file):
        result = get_recipe(filename, uuid)
        assert result is None


def test_empty_file():
    empty_mock = mock_open(read_data="")
    uuid = "60b90c1c13067a15887e1ae1"
    filename = "empty.csv"
    with patch("builtins.open", empty_mock):
        result = get_recipe(filename, uuid)
        assert result is None


def test_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            get_recipe("nonexistent_file.csv", "60b90c1c13067a15887e1ae1")