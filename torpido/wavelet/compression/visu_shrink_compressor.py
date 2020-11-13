""" Compression using Universal Threhold """

import numpy as np

from torpido.wavelet.compression.compressor import Compressor
from torpido.wavelet.util.utility import threshold, mad


class VisuShrinkCompressor:
    """
    Compressor class to the threshold by using VISU method

    Attributes
    ----------
    __compressor: Compressor
        object to call the compress function
    __threshold: float
        threshold for the signal

    References
    ------
    Can be used to reduce noise from a audio signal. Better noise
    threshold calculation
    """

    def __init__(self):
        self.__compressor = Compressor()
        self.__threshold = None

    def compress(self, coefficients):
        """
        Thresholding by generated the threshold value

        Parameters
        ----------
        coefficients: array_like
            input coefficients,  output of the decompose method

        Returns
        -------
        array_like
            thresholded coefficients
        """
        # calculating the threshold only once
        if self.__threshold is None:
            sigma = mad(coefficients)
            self.__threshold = sigma * np.sqrt(2 * np.log(len(coefficients)))

        return threshold(coefficients, self.__threshold)

    def getCompressionRate(self, data):
        """
        Returns the compression rate for the input data. Check the Compression
        class for the implementation

        Parameters
        ----------
        data: array_like
            final data

        Returns
        -------
        int, float
            output in percentage
        """
        return self.__compressor.calculateCompressionRate(data)

    def getThreshold(self):
        """
        Returns the calculated threshold for the signal

        Returns
        -------
        float
            threshold value
        """
        return self.__threshold
