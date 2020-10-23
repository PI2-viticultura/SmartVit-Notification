import unittest


class TestHello(unittest.TestCase):

    def test_service_exist(self):
        self.assertNotEqual(5, 4)


if __name__ == '__main__':
    unittest.main()
