import unittest

from torpido.config.config import *


class ConfigTest(unittest.TestCase):
    def test_write(self):
        d = Config.WAVELET

        self.assertEqual("coif1", d)

    def test_read(self):
        Config.THEME = "Crank"

        self.assertEqual("Crank", Config.THEME)

    def test_check_dtype(self):
        Config.THEME = "Crank"

        self.assertEqual("Crank", Config.THEME)
        self.assertEqual(str, type(Config.THEME))
        

if __name__ == '__main__':
    unittest.main()
