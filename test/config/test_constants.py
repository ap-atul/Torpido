import unittest

from torpido.config import constants


class MyTestCase(unittest.TestCase):
    def test_rinit(self):
        val = constants.ID_COM_VIDEO
        val += constants.ID_COM_VIDEO + "new_change"
        constants.ID_COM_VIDEO = val

        # updating
        constants.rinit()

        self.assertEqual(val, constants.ID_COM_VIDEO)


if __name__ == '__main__':
    unittest.main()
