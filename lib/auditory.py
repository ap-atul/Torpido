"""
Audio de noising process: this class will read the audio file and using
wavelet transforms a threshold will be added to each window with certain level
"""

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


def mad(array):
    """
    Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variability of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation

    Parameters
    ----------
    array : numpy array
        input data from signal
    """
    array = np.ma.array(array).compressed()
    return np.median(np.abs(array - np.median(array)))


class Auditory:
    """
    Audio de noising is done using Wavelet Transform on the input audio signal. The functions read
    the input audio signal in small portions and append the de-noised signal to the output audio
    file that is later merged with the input video file

    Attributes
    ----------
    fileName : str
        input audio file
    rate : int
        sample rate of the audio signal in frequency
    plot : bool
        plot the signal
    info : object
        sound file object having the info of the audio file
    energy : list
        list of the ranks for the audio signal
    audioRankPath : str
        directory to store the rank of the audio
    silenceThreshold : int
        threshold value to determine the rank
    cache : Cache
        object of the cache to store the audio file info
    """
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
        Calculates the de noised signal based on the wavelets
        default wavelet is = db4, mode = per and thresh method = soft.

        The input audio is read in small portions de-noised and appended to the
        audio file in same manner. Also it supports multiple channels and the
        size of the input audio file and output audio files are same so no
        data loss.

        Prints some debug and info Logs

        Parameters
        ----------
        inputFile : str
            input audio file
        outputFile : str
            output audio file
        plot : bool
            True to plot the audio signal

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

        Parameters
        ----------
        block : array
            input signal block

        Returns
        -------
        int
            rank for the portion which is then set for all the portion of data
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
        """
        pass

    def getNoiseFromAudio(self):
        """
        Parsed the input audio signal all at once and generates an
        noise profile or the signal and saved to the file

        Writes the noise signal to the file names 'noise.wav'
        """
        data, rate = soundfile.read(self.fileName)
        filePath = os.path.dirname(self.fileName)

        noiseSignal = NoiseProfiler(data).getNoiseDataPredicted()
        soundfile.write(os.path.join(filePath, "noise.wav"), noiseSignal, rate)
        Log.i("Noise file generated.")

    def __del__(self):
        """
        clean up
        """
        del self.cache
        Log.d("Cleaning up.")
