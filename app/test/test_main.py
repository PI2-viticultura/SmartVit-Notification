# Importamos a biblioteca de testes
import unittest


class TestHello(unittest.TestCase):
    def test_service_exist(self):
        test = ['item']
        self.assertNotEqual(None, test)


if __name__ == '__main__':
    unittest.main()
