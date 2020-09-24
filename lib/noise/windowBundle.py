"""
A class to keep:
1) the window's raw data
2) the window's max(abs(data))

To be utilized to later extract the level that was surpassed the x% of the time
"""
import math

import numpy
import pywt


class WindowBundle:
    def __init__(self, data: numpy, id):
        """
        Handles the smallest component of the parsed signal

        Parameters
        ----------
        data : array
            input data
        id : int
            index
        """
        self.id = id
        self.data = data
        self.rms = None
        self.waveletPacket = None
        self.noiseWindow = None
        self.denoisedData = []

        self.dbName = None
        self.wlevels = None

    def extractWaveletPacket(self, dbName, wlevels):
        """
        Extract wavelet coefficient using Wavelet and levels

        Parameters
        ----------
        dbName : str
            wavelet name
        wlevels : int
            wavelet levels

        Returns
        -------
        object
            final wavelet packet
        """
        if self.waveletPacket is not None:
            return self.waveletPacket

        self.dbName = dbName
        self.wlevels = wlevels
        self.waveletPacket = pywt.WaveletPacket(
            self.data, dbName, 'symmetric', wlevels)

        return self.waveletPacket

    def getRMS(self):
        """
        Calculate the RMS for input signal

        Returns
        -------
        float
            RMS value
        """
        if self.rms is not None:
            return self.rms

        squaredSum = numpy.sum(numpy.power(self.data, 2))
        self.rms = math.sqrt(squaredSum / len(self.data))

        return self.rms
