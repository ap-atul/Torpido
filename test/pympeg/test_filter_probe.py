import unittest

from torpido import pympeg


class FFprobeTest(unittest.TestCase):
    def test_probe(self):
        json_dict = pympeg.probe("/home/atul/Videos/example_02.mp4")

        self.assertEqual(dict, type(json_dict))

    def test_probe_no_file(self):
        try:
            json_dict = pympeg.probe(filename="/home/atul/some.txt")

        except FileExistsError:
            self.assertTrue(True)

    def test_command_gen(self):
        pympeg.init()
        command = pympeg.input(name="/home/atul/Videos/example_02.mp4").output(name="my_output.mp4", map_cmd="").command()

        if "ffmpeg -y -i /home/atul/Videos/example_02.mp4" in command:
            out = True
        else:
            out = False

        self.assertTrue(out)

    def test_filter_outputs(self):
        pympeg.init()
        splits = pympeg.input(name="/home/atul/Videos/example_02.mp4").filter(filter_name="split", outputs=2)

        self.assertEqual(2, len(splits.outputs))

    def test_filter_inputs(self):
        pympeg.init()
        in_file = pympeg.input(name="/home/atul/Videos/example_02.mp4")
        concat = in_file.arg(inputs=[in_file, in_file], args="concat=2", outputs=2)

        self.assertEqual(2, len(concat.inputs))
        self.assertEqual(2, len(concat.outputs))

    def test_options(self):
        pympeg.init()
        command = pympeg.option(tag="-f", name='ffmetadata', output='out').command()
        str = "ffmpeg -y -f ffmetadata "

        self.assertEqual(str, command)


if __name__ == '__main__':
    unittest.main()
