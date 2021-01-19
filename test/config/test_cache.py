import unittest

from torpido.config.cache import *


class CacheTest(unittest.TestCase):
    def test_read_write_dtype(self):
        cache = Cache()
        cache.write_data("data", {"str": "String", "int": 3})

        self.assertEqual(cache.read_data("data"), {"str": "String", "int": 3})

    def test_read_write_list(self):
        cache = Cache()
        cache.write_data("d", [1, 2, 3, 4])
        ls = cache.read_data("d")

        self.assertListEqual(ls, [1, 2, 3, 4])

    def test_read_write_obj(self):
        cache = Cache()
        cache.write_data("d", cache)
        obg = cache.read_data("d")

        self.assertEqual(type(obg), type(cache))


if __name__ == '__main__':
    unittest.main()
