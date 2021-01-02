""" Simple Compression method to zeroed the data that is below certain level """

import numpy as np


class Compressor:
    """
    The input magnitude, defines how to threshold the data. The range below the magnitude
    is made zero, which is then counted to determine the compression rate for the data and the
    algorithm

    Attributes
    ----------
    __magnitude: float
        magnitude to compare the data with
    __threshold: float
        threshold to compare the data with
    __substitute: float
        value to change with
    """

    def __init__(self):
        self.__magnitude = 0.
        self.__threshold = 1.
        self.__substitute = 0.

    def compress(self, data, magnitude):
        """
        Compress the data using the magnitude, make the elements zero which are lower the value
        Parameters
        ----------
        data: array_like
            input signal
        magnitude: float
            min magnitude to threshold

        Returns
        -------
        array_like
            thresholded values
        """
        self.__magnitude = magnitude
        con = np.less(data, (self.__magnitude * self.__threshold))
        return np.where(con, self.__substitute, data)

    def calculateCompressionRate(self, data):
        """
        Calculates the compression rate that is just the number of zeros
        in the signal

        Parameters
        ----------
        data: array_like
            input signal from the final step

        Returns
        -------
        float
            percentage value of the compression rate
        """
        data = np.asanyarray(data).flatten()
        noOfZeros = np.count_nonzero(data == 0)

        # avoiding division by zero
        if noOfZeros == 0:
            return noOfZeros

        return (noOfZeros / len(data)) * 100

    def getMagnitude(self):
        """
        Returns the magnitude calculated

        Returns
        -------
        float
            magnitude calculated
        """
        return self.__magnitude

    def getThreshold(self):
        """
        Returns the threshold

        Returns
        -------
        float
            default is 1
        """
        return self.__threshold
