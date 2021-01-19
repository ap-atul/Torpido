import unittest

from torpido.config.config import *


class ConfigTest(unittest.TestCase):
    def test_write(self):
        config = Config()
        d = config.read("WAVELET", str)

        self.assertEqual("coif1", d)

    def test_read(self):
        config = Config()
        config.write("MYD", 30)

        self.assertEqual("30", config.read("MYD", str))

    def test_read_dtype(self):
        config = Config()
        config.write("MYD", 30)

        self.assertEqual(30, config.read("MYD", int))

    def test_check_dtype(self):
        config = Config()
        config.write("MYD", 30)

        self.assertEqual(int, type(config.read("MYD", int)))

    def test_check_type(self):
        config = Config()
        config.write("Some", 30)

        try:
            config.read("Some", type(config))
        except TypeError:
            self.assertTrue(True)
        self.assertFalse(False)
        

if __name__ == '__main__':
    unittest.main()
