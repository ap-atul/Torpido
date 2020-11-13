"""Fast Wavelet Transform calls the Base Transform based on the dimensions"""

import numpy as np
from torpido.wavelet.extension.base_transform import BaseTransform

from torpido.wavelet.util import isPowerOf2, decomposeArbitraryLength, scalb, getExponent


class FastWaveletTransform(BaseTransform):

    def __init__(self, waveletName):
        super().__init__(waveletName)

    def waverec(self, arrHilbert, level=None):
        # setting the max level
        if level is None:
            level = getExponent(len(arrHilbert))

        # checking if the data is not of arbitrary length
        # special cases only for 1D arrays
        if not isPowerOf2(len(arrHilbert)):
            # perform ancient egyptian decomposition
            return self.__waveRecAncientEgyptian(arrHilbert, level)

        else:
            return self.waveRec1(arrHilbert, level)

    def wavedec(self, arrTime, level=None):
        # setting the max level
        if level is None:
            level = getExponent(len(arrTime))

        # checking if the data is not of arbitrary length
        # special cases only for 1D arrays
        if not isPowerOf2(len(arrTime)):
            # perform ancient egyptian decomposition
            return self.__waveDecAncientEgyptian(arrTime, level)

        # data of length power of 2
        else:
            return self.waveDec1(arrTime, level)

    def __waveDecAncientEgyptian(self, arrTime, level):
        arrHilbert = list()
        powers = decomposeArbitraryLength(len(arrTime))
        offset = 0

        # running for each decomposed array by power
        for power in powers:
            sliceIndex = int(scalb(1., power))
            arrTimeSliced = arrTime[offset: (offset + sliceIndex)]

            # run the wavelet decomposition for the slice
            arrHilbert.extend(self.waveDec1(np.array(arrTimeSliced, dtype=np.float_), level))

            # incrementing the offset
            offset += sliceIndex

        return arrHilbert

    def __waveRecAncientEgyptian(self, arrHilbert, level):
        arrTime = list()
        powers = decomposeArbitraryLength(len(arrHilbert))
        offset = 0

        # running for each decomposed array by power
        for power in powers:
            sliceIndex = int(scalb(1., power))
            arrHilbertSliced = arrHilbert[offset: (offset + sliceIndex)]

            # run the wavelet decomposition for the slice
            arrTimeSliced = self.waveRec1(np.array(arrHilbertSliced, dtype=np.float_), level)
            arrTime.extend(arrTimeSliced)

            # incrementing the offset
            offset += sliceIndex

        return arrTime
