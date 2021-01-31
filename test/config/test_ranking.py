import unittest

from torpido.tools.ranking import Ranking


class CacheTest(unittest.TestCase):
    def test_add(self):
        Ranking.add("MOTION", [1, 2, 3])
        self.assertEqual(list, type(Ranking.get("MOTION")))

    def test_get(self):
        self.assertEqual(None, Ranking.get("NO_SUCH"))
        self.assertEqual(list, type(Ranking.get("MOTION")))

    def test_ranks(self):
        self.assertEqual(4, len(Ranking.ranks()))

    def test_timestamps(self):
        self.assertEqual(list, type(Ranking.get_timestamps()))

    def test_get_vid_len(self):
        self.assertEqual(int, type(Ranking.get_video_length()))
        self.assertEqual(30, Ranking.get_video_length())

    def test_get_thumbnail_sec(self):
        self.assertEqual(int, type(Ranking.get_thumbnail_sec()))


if __name__ == '__main__':
    unittest.main()
