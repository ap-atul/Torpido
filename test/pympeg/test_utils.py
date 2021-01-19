import unittest

from torpido.pympeg._util import *
from torpido.pympeg._node import *


class UtilTest(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(str, type(gen_labels()))

    def test_mul_labels(self):
        self.assertEqual(list, type(gen_labels(10)))
        self.assertEqual(5, len(gen_labels(5)))

    def test_param_str(self):
        params = {
            "start": 10,
            "duration": 5
        }
        out = "start=10:duration=5"

        self.assertEqual(out, get_str_from_params(params))

    def test_filter_str(self):
        params = {
            "start": 10,
            "duration": 5
        }
        filter = FilterNode(filter_name="trim", params=params, inputs=[Label()])
        str = get_str_from_filter(filter)

        if 'trim=start=10:duration=5' in str:
            out = True
        else:
            out = False

        self.assertEqual(True, out)

    def test_global_str(self):
        global_node = GlobalNode(inputs=[Label()], args="split=2", outputs=[Label()])
        str = get_str_from_global(global_node)

        if 'split=2' in str:
            out = True
        else:
            out = False

        self.assertEqual(True, out)


if __name__ == '__main__':
    unittest.main()
