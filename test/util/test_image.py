import unittest

from torpido.util.image import *


class MyTestCase(unittest.TestCase):
    def test_image_resize(self):
        white_image = np.full(
            (1920, 720, 3),
            255,
            dtype=np.uint8
        )
        resized_image = resize(white_image, 500)
        output_shape = (1333, 500, 3)
        self.assertEqual(output_shape, resized_image.shape)

    def test_image_resize_gray(self):
        white_image = np.full(
            (500, 500),
            255,
            dtype=np.uint8
        )
        resized_image = resize(white_image, 500)
        output_shape = (500, 500)
        self.assertEqual(output_shape, resized_image.shape)


if __name__ == '__main__':
    unittest.main()
