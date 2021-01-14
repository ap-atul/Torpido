import unittest

from torpido.wavelet import FastWaveletTransform, decomposeArbitraryLength, getExponent, scalb, isPowerOf2


class MyTestCase(unittest.TestCase):
    def test_wavelet(self):
        WAVELET_NAME = "db4"
        t = FastWaveletTransform(WAVELET_NAME)

        # original data
        data = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

        # decomposition --> reconstruction
        coefficients = t.wavedec(data)
        clean = t.waverec(coefficients)

        self.assertTrue(any([data, list(clean)]))

    def test_dec_rec(self):
        WAVELET = "coif1"
        t = FastWaveletTransform(WAVELET)
        data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        coeff = t.wavedec(data)
        clean = t.waverec(coeff)

        self.assertTrue(any([data, list(clean)]))

    def test_decomposition(self):
        self.assertEqual(decomposeArbitraryLength(13), [3, 2, 0])
        self.assertEqual(decomposeArbitraryLength(42), [5, 3, 1])
        self.assertEqual(decomposeArbitraryLength(43), [5, 3, 1, 0])
        self.assertEqual(decomposeArbitraryLength(1000000), [19, 18, 17, 16, 14, 9, 6])

    def test_exp(self):
        self.assertEqual(5, getExponent(32))
        self.assertEqual(6, getExponent(64))

    def test_scale(self):
        self.assertEqual(16.0, scalb(2, 3))

    def test_is_power(self):
        self.assertTrue(isPowerOf2(32))
        self.assertTrue(isPowerOf2(64))
        self.assertTrue(isPowerOf2(8))
        self.assertTrue(not isPowerOf2(10))


if __name__ == '__main__':
    unittest.main()
