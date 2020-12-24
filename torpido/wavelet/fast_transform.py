"""Fast Wavelet Transform calls the Base Transform based on the dimensions"""

import numpy as np
from torpido.wavelet.extension.base_transform import BaseTransform

from torpido.wavelet.util import decomposeArbitraryLength, scalb, getExponent


class FastWaveletTransform(BaseTransform):
    """
    Reads the dimensions of the input signal and calls
    the respective functions of the Base Transform class
    """

    def __init__(self, waveletName):
        super().__init__(waveletName)

    def waverec(self, arrHilbert, level=None):
        """
        Wavelet Reconstruction

        Parameters
        ----------
        level: int
            level for reconstruction
        arrHilbert: array_like
            input array in the Hilbert domain

        Returns
        -------
        array_like
            Time domain
        """
        dimensions = np.ndim(arrHilbert)

        # setting the max level
        if level is None:
            level = getExponent(len(arrHilbert))

        # for single dim data
        if dimensions == 1:
            # perform ancient egyptian reconstruction
            return self.__waveRecAncientEgyptian(arrHilbert, level)

        # for two dim data
        if dimensions == 2:
            # perform ancient egyptian reconstruction
            return self.__waveRecAncientEgyptian2(arrHilbert)

    def wavedec(self, arrTime, level=None):
        """
        Wavelet Decomposition

        Parameters
        ----------
        level: int
            level for decomposition
        arrTime: array_like
            input array in the Time domain

        Returns
        -------
        array_like
            Hilbert domain
        """
        dimensions = np.ndim(arrTime)

        # setting the max level
        if level is None:
            level = getExponent(len(arrTime))

        # for two single data
        if dimensions == 1:
            # perform ancient egyptian decomposition
            return self.__waveDecAncientEgyptian(arrTime, level)

        # for two dim data
        if dimensions == 2:
            # perform ancient egyptian decomposition
            return self.__waveDecAncientEgyptian2(arrTime)

    def __waveDecAncientEgyptian(self, arrTime, level):
        """
        Wavelet decomposition for data of arbitrary length

        References
        ----------
        The array is distributed by the length of the power of 2
        and then wavelet decomposition is performed
        Look into the utility.decomposeArbitraryLength function

        for a data with length 42
        Ex: 42 = 2^5, 2^3, 2^1   i.e. 32, 8, 2 lengths partitions are made

        Parameters
        ----------
        arrTime: array_like
            input array in the time domain

        Returns
        -------
        array_like
            hilbert domain array
        """
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
        """
        Wavelet reconstruction for data of arbitrary length

        References
        ----------
        The array is distributed by the length of the power of 2
        and then wavelet decomposition is performed
        Look into the utility.decomposeArbitraryLength function

        for a data with length 42
        Ex: 42 = 2^5, 2^3, 2^1   i.e. 32, 8, 2 lengths partitions are made

        Parameters
        ----------
        arrHilbert: array_like
            input array in the hilbert domain

        Returns
        -------
        array_like
            hilbert time array
        """
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

    def __waveDecAncientEgyptian2(self, matTime):
        """
        Wavelet decomposition for data of arbitrary length (2D)

        References
        ----------
        The array is distributed by the length of the power of 2
        and then wavelet decomposition is performed
        Look into the utility.decomposeArbitraryLength function

        for a data with length 42
        Ex: 42 = 2^5, 2^3, 2^1   i.e. 32, 8, 2 lengths partitions are made

        Parameters
        ----------
        matTime: array_like
            input 2D array in the time domain

        Returns
        -------
        array_like
            hilbert domain array
        """
        # shape
        noOfRows = len(matTime)
        noOfCols = len(matTime[0])

        levelM = getExponent(noOfRows)
        levelN = getExponent(noOfCols)

        matHilbert = np.zeros(shape=(noOfRows, noOfCols))

        # rows
        for i in range(noOfRows):
            # run the decomposition
            matHilbert[i] = self.__waveDecAncientEgyptian(np.array(matTime[i], dtype=np.float_), levelN)

        # cols
        for j in range(noOfCols):
            # run the decomposition
            matHilbert[:, j] = self.__waveDecAncientEgyptian(np.array(matHilbert[:, j], dtype=np.float_), levelM)

        return matHilbert

    def __waveRecAncientEgyptian2(self, matHilbert):
        """
        Wavelet reconstruction for data of arbitrary length (2D)

        References
        ----------
        The array is distributed by the length of the power of 2
        and then wavelet decomposition is performed
        Look into the utility.decomposeArbitraryLength function

        for a data with length 42
        Ex: 42 = 2^5, 2^3, 2^1   i.e. 32, 8, 2 lengths partitions are made

        Parameters
        ----------
        matHilbert: array_like
            input 2D array in the hilbert domain

        Returns
        -------
        array_like
            hilbert time array
        """
        noOfRows = len(matHilbert)
        noOfCols = len(matHilbert[0])

        # getting the levels
        levelM = getExponent(noOfRows)
        levelN = getExponent(noOfCols)

        matTime = np.zeros(shape=(noOfRows, noOfCols))

        # rows
        for j in range(noOfCols):
            # run the reconstruction on the row
            matTime[:, j] = self.__waveRecAncientEgyptian(np.array(matHilbert[:, j], dtype=np.float_), levelM)

        # cols
        for i in range(noOfRows):
            # run the reconstruction on the column
            matTime[i] = self.__waveRecAncientEgyptian(np.array(matTime[i], dtype=np.float_), levelN)

        return matTime
