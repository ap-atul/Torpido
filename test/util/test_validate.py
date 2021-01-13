import unittest
from torpido.util.validate import *


class MyTestCase(unittest.TestCase):
    def test_check_video(self):
        fil = "sample.json"

        # file not exists
        self.assertFalse(check_type_video(fil))

    def test_check_video_exits(self):
        file = "/home/atul/Videos/example_02.mp4"

        self.assertTrue(check_type_video(file))

    def test_check_not_video(self):
        file = "/home/atul/Videos/audios/10min_cut_720_60.wav"

        self.assertFalse(check_type_video(file))

    def test_check_video_rename(self):
        file = "/home/atul/Videos/example_.mp4"

        # file not found, even if it is a video
        self.assertFalse(check_type_video(file))


if __name__ == '__main__':
    unittest.main()
