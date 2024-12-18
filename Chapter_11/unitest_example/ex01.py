import unittest

def multiply_numbers(x, y):
    return x * y

class TestMultiplication(unittest.TestCase):
    def test_multiply_two_positive_numbers(self):
        result = multiply_numbers(2, 3)
        self.assertEqual(result, 6)

    def test_multiply_positive_and_negative_numbers(self):
        result = multiply_numbers(2, -3)
        self.assertEqual(result, -6)

    def test_multiply_two_negative_numbers(self):
        result = multiply_numbers(-2, -3)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()