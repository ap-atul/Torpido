import os

import numpy as np
import pywt
import soundfile
from joblib import dump
from matplotlib import pyplot as plt
from statsmodels.robust import mad

from lib.util.constants import *
from lib.util.noiseProfiler import NoiseProfiler

"""
Audio de noising process: this class will read the audio file and using
wavelet transforms a threshold will be added to each window with certain level
"""


def getEnergyRMS(block):
    """
    RMS = Root Mean Square to calculate the signal data to the dB, if signal
    satisfies some threshold the ranking can be affected and audio portion
    can be ranked
    RMS -> square root of mean of squared data
    :param block: array, input signal
    :return: float, energy in dB
    """
    if np.sqrt(np.mean(block ** 2)) > SILENCE_THRESHOlD:
        return RANK_AUDIO
    return 0


class Auditory:
    def __init__(self):
        self.fileName = None
        self.rate = None
        self.data = None
        self.plot = False
        self.clean = None
        self.info = None
        self.energy = None
        self.audioRankPath = os.path.join(RANK_DIR, RANK_OUT_AUDIO)

    def startProcessing(self, inputFile, outputFile, plot=False):
        """
        this function calculates the de noised signal based on the wavelets
        default wavelet is = db4, mode = per and thresh method = soft
        :param inputFile: (str) name of the file
        :param outputFile: (str) destination file name
        :param plot: (bool) to plot the signal
        :return: None
        """
        if os.path.isfile(inputFile) is False:
            print(f"[ERROR] File {inputFile} does not exists")
            return

        self.fileName = inputFile

        self.info = soundfile.info(self.fileName)
        self.rate = self.info.samplerate
        self.clean = np.array([])
        self.energy = []

        for block in soundfile.blocks(self.fileName, int(self.rate * AUDIO_BLOCK_SEC)):
            if len(block.shape) > 1:
                block = block.T[0]

            # cal all coefficients
            coefficients = pywt.wavedec(block, WAVELET, DEC_REC_MODE)
            sigma = mad(coefficients[- WAVELET_LEVEL])

            thresh = sigma * np.sqrt(2 * np.log(len(block)))
            coefficients[1:] = (pywt.threshold(i, value=thresh, mode=WAVE_THRESH) for i in coefficients[1:])

            self.clean = np.concatenate([self.clean, pywt.waverec(coefficients, WAVELET, mode=DEC_REC_MODE)])
            self.energy.extend([getEnergyRMS(block) * AUDIO_BLOCK_SEC])  # calculate the audio energy

        soundfile.write(outputFile, np.array(self.clean, dtype=float), self.rate)
        dump(self.energy, self.audioRankPath)
        print("[INFO] Audio de noised successfully")
        print(f"[INFO] Audio ranking length {len(self.energy)}")
        print("[INFO] Audio ranking saved .............")

        if plot:
            self.plotSignals()

    def getAudioInfo(self):
        return self.info

    def plotSignals(self):
        """
        plotting the cleaned and original signals
        :return:
        """
        plt.plot(self.data)
        plt.title("Original Signal")
        plt.show()

        plt.plot(self.clean)
        plt.title("Cleaned Signal")
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
        print("[INFO] Noise file generated.")
