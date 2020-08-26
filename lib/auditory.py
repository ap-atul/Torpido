import os

import numpy as np
import pywt
import soundfile
from matplotlib import pyplot as plt
from statsmodels.robust import mad
from tqdm import tqdm

from lib.util.constants import *
from lib.util.noiseProfiler import NoiseProfiler

"""
Audio de noising process: this class will read the audio file and using
wavelet transforms a threshold will be added to each window with certain level
"""


class Auditory:
    def __init__(self):
        self.fileName = None
        self.rate = None
        self.data = None
        self.plot = False
        self.clean = None
        self.info = None

    def startProcessing(self, inputFile, plot=False):
        """
        this function calculates the de noised signal based on the wavelets
        default wavelet is = db4, mode = per and thresh method = soft
        :param inputFile: (str) name of the file
        :param plot: (bool) to plot the signal
        :return: None
        """
        if os.path.isfile(inputFile) is False:
            raise Exception(f"File {inputFile} does not exists")

        self.fileName = inputFile

        self.info = soundfile.info(self.fileName)
        self.rate = self.info.samplerate
        self.clean = np.array([])

        for block in tqdm(soundfile.blocks(self.fileName, int(self.rate * self.info.duration * AUDIO_BLOCK))):
            if len(block.shape) > 1:
                block = block.T[0]

            # cal all coefficients
            coefficients = pywt.wavedec(block, WAVELET, DEC_REC_MODE)
            sigma = mad(coefficients[- WAVELET_LEVEL])

            thresh = sigma * np.sqrt(2 * np.log(len(block)))
            coefficients[1:] = (pywt.threshold(i, value=thresh, mode=WAVE_THRESH) for i in coefficients[1:])

            self.clean = np.concatenate([self.clean, pywt.waverec(coefficients, WAVELET, mode=DEC_REC_MODE)])
        soundfile.write(inputFile, np.array(self.clean, dtype=float), self.rate)
        print("Audio de noised successfully")

        if plot:
            self.plotSignals()

    def getAudioInfo(self):
        return self.info

    def plotSignals(self):
        """
        plotting the cleaned and original data
        :return:
        """
        plt.plot(self.data)
        plt.title("Original Data")
        plt.show()

        plt.plot(self.clean)
        plt.title("Cleaned Data")
        plt.show()

    def getNoiseFromAudio(self):
        """
        this method is not completely related, all it does it
        using wavelet transform remove the noise signals and
        save to a file name: noise.wav
        Note :: It is very heavy on the memory
        :return: None
        """
        data, rate = soundfile.read(self.fileName)
        filePath = os.path.dirname(self.fileName)

        noiseSignal = NoiseProfiler(data).getNoiseDataPredicted()
        soundfile.write(os.path.join(filePath, "noise.wav"), noiseSignal, rate)
        print("Noise file generated.")
