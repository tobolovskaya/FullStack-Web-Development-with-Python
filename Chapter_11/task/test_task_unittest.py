import unittest
from unittest.mock import patch, mock_open


def get_recipe(path, search_id):
    result = None
    with open(path, "r") as f:
        for line in f:
            (id, name, *recipes) = line.strip().split(",")
            if id == search_id:
                result = {"id": id, "name": name, "ingredients": recipes}
    return result


class TestGetRecipe(unittest.TestCase):
    mock_data = (
        "60b90c1c13067a15887e1ae1,Herbed Baked Salmon,4 lemons,1 large red onion,2 tablespoons chopped fresh basil\n"
        "60b90c2413067a15887e1ae2,Lemon Pancakes,2 tablespoons baking powder,1 cup vanilla-flavored almond milk,1 lemon\n"
        "60b90c2e13067a15887e1ae3,Chicken and Cold Noodles,6 ounces dry Chinese noodles,1 tablespoon sesame oil,3 tablespoons soy sauce"
    )

    @classmethod
    def setUpClass(cls):
        cls.mock_open_file = mock_open(read_data=cls.mock_data)

    @classmethod
    def tearDownClass(cls):
        cls.mock_open_file = None

    def test_get_first_recipe(self):
        uuid = "60b90c1c13067a15887e1ae1"
        filename = "fake.csv"
        with patch("builtins.open", self.mock_open_file):
            result = get_recipe(filename, uuid)
            self.assertEqual(uuid, result.get("id"))
            self.assertEqual("Herbed Baked Salmon", result.get("name"))
            self.assertEqual(
                ["4 lemons", "1 large red onion", "2 tablespoons chopped fresh basil"],
                result.get("ingredients"),
            )

    def test_get_second_recipe(self):
        uuid = "60b90c2413067a15887e1ae2"
        filename = "fake.csv"
        with patch("builtins.open", self.mock_open_file):
            result = get_recipe(filename, uuid)
            self.assertEqual(uuid, result.get("id"))
            self.assertEqual("Lemon Pancakes", result.get("name"))
            self.assertEqual(
                [
                    "2 tablespoons baking powder",
                    "1 cup vanilla-flavored almond milk",
                    "1 lemon",
                ],
                result.get("ingredients"),
            )

    def test_get_nonexistent_recipe(self):
        uuid = "nonexistent_id"
        filename = "fake.csv"
        with patch("builtins.open", self.mock_open_file):
            result = get_recipe(filename, uuid)
            self.assertIsNone(result)

    def test_empty_file(self):
        empty_mock = mock_open(read_data="")
        uuid = "60b90c1c13067a15887e1ae1"
        filename = "empty.csv"
        with patch("builtins.open", empty_mock):
            result = get_recipe(filename, uuid)
            self.assertIsNone(result)

    def test_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                get_recipe("nonexistent_file.csv", "60b90c1c13067a15887e1ae1")


if __name__ == "__main__":
    unittest.main()