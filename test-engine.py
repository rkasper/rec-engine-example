import unittest

from engine import get_recommendations


class EngineTestCase(unittest.TestCase):
    def test_get_recommendations(self):
        products = get_recommendations(3)
        print(products)
        self.assertTrue(len(products) > 0)


if __name__ == '__main__':
    unittest.main()
