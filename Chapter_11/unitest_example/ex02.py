import unittest

class MyTest(unittest.TestCase):
    def setUp(self):
        self.my_list = [1, 2, 3]

    def tearDown(self):
        del self.my_list

    def test_list_length(self):
        self.assertEqual(len(self.my_list), 3)

    def test_list_contents(self):
        self.assertListEqual(self.my_list, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()