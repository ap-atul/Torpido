"""
Class to create a noise profile from an audio input
"""
import math

import matplotlib.pyplot as plt
import numpy

from lib.noise import windowBundle, waveletHelper
from lib.noise.linkedList import LinkedList


class NoiseProfiler:
    """
    Basic de noise wrapper for keeping store of the settings

    Attributes
    ----------
    timeWindow : float
        max __time window
    sampleRate : int, default=44100
        sample rate of audio in frequency
    percentileLevel : int, default=95
        percent satisfies
    wlevels : int, default=4
        max wavelet levels
    dbName : str, default='db8'
        name of wavelet to use
    """

    def __init__(self, x, timeWindow=0.1, sampleRate=44100, percentileLevel=95, wlevels=4, dbName='db8'):
        self.x = x
        self.timeWindow = timeWindow
        self.windowSamples = int(timeWindow * sampleRate)
        self.wlevels = wlevels
        self.dbName = dbName

        self.windows = list()
        self.sortedWindows = list()

        self.noiseWindows = None
        self.noiseLinked = LinkedList()
        self.signalWindows = None
        self.signalLinked = LinkedList()

        self.percentileLevel = percentileLevel
        self.noiseData = None
        self.noiseWavelets = list()
        self.threshold = None

        self.extractWindows()
        print("Noise profiler finished")

    def cleanUp(self):
        """
        cleaning up
        """
        self.windows = None
        self.sortedWindows = None
        self.noiseData = None
        self.noiseLinked = None
        self.signalLinked = None
        self.signalWindows = None
        self.noiseWavelets = None

    @staticmethod
    def __getNodesWindowData(nodes):
        """
        window data based on the nodes

        Parameters
        ----------
        nodes : Node
            input nodes

        Returns
        -------
        object
            data from the nodes

        """
        data = []
        for node in nodes:
            window = node.data
            data.extend(window.data)

        return data

    def __getNodeCircularPrediction(self, node, n):
        """
        Returns predicted value for the node

        Parameters
        ----------
        node : Node
            data point
        n : int
            index of data point

        Returns
        -------
        object
            links of nodes
        """
        prevNode = node.getPrevWithValidData()
        nextNode = node.getNextWithValidData()
        if prevNode is None:
            # work with current->future period of silence
            return self.__getFutureCircularNodes(nextNode, n)
        # working with the previous period of silence
        return self.__getPastCircularNodes(prevNode, n)

    @staticmethod
    def __getFutureCircularNodes(initialNode, n):
        """
        Returns predicted values for the nodes

        Parameters
        ----------
        initialNode : object
            current node
        n : int
            index of the node

        Returns
        -------
        object
            links of the nodes

        """
        ret = []
        count = 0
        current = initialNode
        while True:
            ret.append(current)
            count += 1
            if count == n:
                return ret

            if current.next and current.next.data:
                current = current.next
            else:
                current = initialNode

    @staticmethod
    def __getPastCircularNodes(initialNode, n):
        """
        Returns previous nodes

        Parameters
        ----------
        initialNode : object
            initial node
        n : int
            index of the node

        Returns
        -------
        list
            list of nodes

        """
        ret = []
        count = 0
        current = initialNode
        while True:
            ret.append(current)
            count += 1
            if count == n:
                return ret

            if current.prev and current.prev.data:
                current = current.prev
            else:
                current = initialNode

    def getNoiseDataPredicted(self):
        """
        Calculates noise profile by parsing the input signal

        Returns
        -------
        object
            noise signal extracted
        """
        self.threshold = self.extractRMSthresholdFromWindows(
            self.percentileLevel)
        self.extractSignalAndNoiseWindows(self.threshold)

        noiseDataPredicted = []

        consecutiveEmptyNodes = 0
        lastValidNode = None
        for node in self.noiseLinked.getAsList():
            if node.data is None:
                consecutiveEmptyNodes += 1
            else:
                lastValidNode = node

                if consecutiveEmptyNodes != 0:
                    predictedNodes = self.__getNodeCircularPrediction(
                        node, consecutiveEmptyNodes)
                    noiseDataPredicted.extend(self.__getNodesWindowData(predictedNodes))
                    consecutiveEmptyNodes = 0

                window = node.data
                noiseDataPredicted.extend(window.data)

        # in case we had empty data on the end
        if consecutiveEmptyNodes != 0:
            predictedNodes = self.__getNodeCircularPrediction(
                lastValidNode, consecutiveEmptyNodes)
            noiseDataPredicted.extend(self.__getNodesWindowData(predictedNodes))

        self.cleanUp()
        return noiseDataPredicted

    def extractRMSthresholdFromWindows(self, percentileLevel):
        """
        Get threshold for the Energy of the signal

        Parameters
        ----------
        percentileLevel : float
            threshold satisfying value

        Returns
        -------
        float
            updated threshold

        """
        if self.threshold is not None:
            return self.threshold

        sortedWindows = sorted(
            self.windows, key=lambda x: x.getRMS(), reverse=True)
        # now the are arranged with the max DESC
        nWindows = len(sortedWindows)
        thresholdIndex = math.floor(percentileLevel / 100 * nWindows)
        self.threshold = sortedWindows[thresholdIndex].getRMS()

        return self.threshold

    def getWindowsRMSasEnvelope(self):
        """
        Returns the energy for the signal

        Returns
        -------
        list
            energy list

        """
        envelope = numpy.array([])
        for window in self.windows:
            windowEnvelope = window.getRMS() * numpy.ones(len(window.data))
            envelope = numpy.concatenate([envelope, windowEnvelope])

        return envelope

    def extractWindows(self):
        """
        Get windows from the parsed signals
        """
        xLength = len(self.x)
        nWindows = math.ceil(xLength / self.windowSamples)
        for i in range(0, nWindows):
            windowBeginning = i * self.windowSamples
            windowEnd = windowBeginning + self.windowSamples
            windowData = self.x[windowBeginning:windowEnd]

            if i == nWindows - 1 and windowEnd - windowBeginning < self.windowSamples:
                paddingLength = windowEnd - windowBeginning - self.windowSamples
                paddingArray = numpy.zeros(paddingLength)
                windowData = numpy.concatenate(windowData, paddingArray)
            window = windowBundle.WindowBundle(windowData, i)
            self.windows.append(window)

    def extractSignalAndNoiseWindows(self, rmsThreshold):
        """
        parse the signal and generate windows

        Parameters
        ----------
        rmsThreshold : float
            threshold
        """
        if self.noiseWindows is not None and self.signalWindows is not None:
            return

        self.noiseWindows = list()
        self.signalWindows = list()
        for window in self.windows:
            # giving a +5% grace on the rms threshold comparison
            if window.getRMS() < (rmsThreshold + 0.05 * rmsThreshold):
                self.noiseWindows.append(window)
                self.noiseLinked.append(window)
                self.signalLinked.append(None)
            else:
                self.signalWindows.append(window)
                self.signalLinked.append(window)
                self.noiseLinked.append(None)

    def plotWavelets(self):
        """
        plot the wavelets
        """
        wtBandsLength = 0
        for window in self.windows:
            windowWaveletData = list()

            windowDataLength = 0
            wt = window.extractWaveletPacket(self.dbName, self.wlevels)
            leafNodes = [node.path for node in wt.get_level(
                self.wlevels, 'freq')]

            for node in leafNodes:
                bandData = wt[node].data
                windowWaveletData.extend(bandData)
                wtBandsLength += len(bandData)
                windowDataLength += len(bandData)

            print("window # " + str(window.id) +
                  " of " + str(len(self.windows)))
            plt.figure(window.id)
            plt.subplot(211)
            plt.plot(window.data)
            plt.subplot(212)
            plt.plot(waveletHelper.waveletLeafData(window.waveletPacket))
            plt.show()
