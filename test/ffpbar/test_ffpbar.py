import unittest
from subprocess import Popen, PIPE

from torpido.ffpbar import *
from torpido import pympeg


class MyTestCase(unittest.TestCase):
    def test_parse(self):
        prg = Progress()

        for i in range(10):
            log = "time=%s:%s:%s  Duration: %02d:%02d:%02d" % (i * 6, i * 3, i * 5, i * 6, i * 3, i * 5)

        prg.complete()
        p = prg.progress

        self.assertEqual(int, type(prg.progress))
        self.assertEqual(100, p)

    def test_prg(self):
        prg = Progress()
        prg.complete()

        prg.clear()
        p = prg.progress

        self.assertEqual(0, p)
        self.assertEqual(int, type(prg.progress))
        self.assertIsNone(prg.clear())
        self.assertIsNone(prg.complete())

    def test_prg_on_cmd(self):
        progress = Progress()

        file = "/home/atul/Videos/example_02.mp4"
        audio = "/home/atul/Videos/example_02.wav"
        command = pympeg.input(name=file).output(name=audio).command()

        process = Popen(
            args=command,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            encoding='utf-8'
        )

        for out in process.stdout:
            progress.display(out)

        process.wait()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
