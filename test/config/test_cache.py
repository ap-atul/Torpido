import unittest

from torpido.config.cache import *
from torpido.tools.ranking import Ranking


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

    def test_ranking(self):
        Cache().write_data(CACHE_FPS, 20)
        Cache().write_data(CACHE_FRAME_COUNT, 600)
        Ranking.add("CACHE_RANK_MOTION", [1, 1, 1, 1, 1])
        Ranking.add("CACHE_RANK_BLUR", [1, 1, 1, 6, 7])
        Ranking.add("CACHE_RANK_AUDIO", [1, 1, 4, 5, 1])
        Ranking.add("CACHE_RANK_TEXT", [1, 2, 3, 1, 1])

        self.assertEqual(4, len(Ranking.ranks()))


if __name__ == '__main__':
    unittest.main()
