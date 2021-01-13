import unittest
from torpido.util.timestamp import *


class MyTestCase(unittest.TestCase):
    def test_list_padding(self):
        list_test = [1, 2, 3, 4, 5]
        new_list = list_test
        add_padding(new_list, 10)
        self.assertListEqual(new_list, [1, 2, 3, 4, 5, 3.0, 3.0, 3.0, 3.0, 3.0])

    def test_list_pad(self):
        list_test = [1, 2, 3, 4, 5]
        self.assertIsNone(add_padding(list_test, 20))

    def test_trim(self):
        ranks = [0, 0, 0, 10, 20, 30, 0, 0]
        self.assertListEqual([[3, 5]], trim_by_rank(ranks))

    def test_trim_2(self):
        ranks = [0, 10, 20, 0, 0, 0, 50, 60]
        # returns the index

        self.assertListEqual([[1, 2], [6, 8]], trim_by_rank(ranks))

    def test_timestamps(self):
        ranks = [
            [0, 0, 0, 0, 0],
            [1, 2, 3, 4, 5],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        self.assertListEqual([[3, 5]], get_timestamps(ranks))

    def test_timestamps_2(self):
        ranks = [
            [10, 0.1, 10, 10, 10],
            [11, 21, 13, 41, 51],
            [10, 0.1, 10, 10, 10],
            [10, 10, 10, 10, 0.1]
        ]

        self.assertListEqual([[0, 5]], get_timestamps(ranks))

    def test_video_length(self):
        timestamps = [
            [1, 3],
            [10, 50]
        ]

        self.assertEqual(42, get_output_video_length(timestamps))

    def test_get_ranking(self):
        try:
            # since ranking are missing before start
            read_rankings()

        except RankingOfFeatureMissing as _:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
