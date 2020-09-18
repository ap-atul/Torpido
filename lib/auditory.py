import gc
import os

import numpy as np
import pywt
import soundfile
from joblib import dump

from lib.noise.noiseProfiler import NoiseProfiler
from lib.util.cache import Cache
from lib.util.constants import *
from lib.util.logger import Log

"""
Audio de noising process: this class will read the audio file and using
wavelet transforms a threshold will be added to each window with certain level
"""


def mad(array):
    """
    Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variability of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation

    :param array : input data from signal
    """
    array = np.ma.array(array).compressed()
    return np.median(np.abs(array - np.median(array)))


class Auditory:
    def __init__(self):
        self.fileName = None
        self.rate = None
        self.data = None
        self.plot = False
        self.info = None
        self.energy = None
        self.audioRankPath = os.path.join(os.getcwd(), RANK_DIR, RANK_OUT_AUDIO)
        self.silenceThreshold = SILENCE_THRESHOlD
        self.cache = Cache()

    def startProcessing(self, inputFile, outputFile, plot=False):
        """
        this function calculates the de noised signal based on the wavelets
        default wavelet is = db4, mode = per and thresh method = soft
        :param outputFile: (str) de noised file name
        :param inputFile: (str) name of the file
        :param plot: (bool) to plot the signal
        :return: None
        """
        if os.path.isfile(inputFile) is False:
            Log.e(f"File {inputFile} does not exists")
            return

        self.fileName = inputFile

        self.info = soundfile.info(self.fileName)
        self.setAudioInfo()
        self.rate = self.info.samplerate
        self.energy = []
        Log.i(f"Audio duration is {self.info.duration}.")

        with soundfile.SoundFile(outputFile, mode="w", samplerate=self.rate, channels=self.info.channels) as out:
            for block in soundfile.blocks(self.fileName, int(self.rate * self.info.duration * AUDIO_BLOCK_PER)):
                # cal all coefficients
                coefficients = pywt.wavedec(block, WAVELET, DEC_REC_MODE)
                sigma = mad(coefficients[- WAVELET_LEVEL])

                thresh = sigma * np.sqrt(2 * np.log(len(block)))
                coefficients[1:] = (pywt.threshold(i, value=thresh, mode=WAVE_THRESH) for i in coefficients[1:])

                # writing to the output file
                out.write(pywt.waverec(coefficients, WAVELET, mode=DEC_REC_MODE))

                # calculating the audio rank
                self.energy.extend([self.getEnergyRMS(block)] * max(1, int(len(block) / self.rate)))

        dump(self.energy, self.audioRankPath)
        Log.i("Audio de noised successfully")
        Log.d(f"Audio ranking length {len(self.energy)}")
        Log.i("Audio ranking saved .............")

        if plot:
            self.plotSignals()

        Log.d(f"Garbage collected :: {gc.collect()}")

    def getEnergyRMS(self, block):
        """
        RMS = Root Mean Square to calculate the signal data to the dB, if signal
        satisfies some threshold the ranking can be affected and audio portion
        can be ranked
        RMS -> square root of mean of squared data
        :param block: array, input signal
        :return: float, energy in dB
        """
        if np.sqrt(np.mean(block ** 2)) > self.silenceThreshold:
            return RANK_AUDIO
        return 0

    def setAudioInfo(self):
        self.cache.writeDataToCache(CACHE_AUDIO_INFO, self.info)

    def plotSignals(self):
        """
        plotting the cleaned and original signals
        TODO: Plotting the audio signal efficiently
        :return:
        """
        pass

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
        Log.i("Noise file generated.")

    def __del__(self):
        del self.cache
        Log.d("Cleaning up.")
