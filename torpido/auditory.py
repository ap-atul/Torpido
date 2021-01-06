"""
Audio de noising process: this class will read the audio file and using
wavelet transforms a threshold will be added to each window with certain level
"""

import gc

import matplotlib
import numpy as np
import soundfile
from matplotlib import pyplot as plt

from torpido.config.cache import Cache
from torpido.config.constants import *
from torpido.tools.logger import Log
from torpido.wavelet import FastWaveletTransform, getExponent, VisuShrinkCompressor, snr

matplotlib.use("TkAgg")


class Auditory:
    """
    Audio de noising is done using Wavelet Transform on the input audio signal. The functions read
    the input audio signal in small portions and append the de-noised signal to the output audio
    file that is later merged with the input video file

    Attributes
    ----------
    __fileName : str
        input audio file
    __rate : int
        sample rate of the audio signal in frequency
    __plot : bool
        plot the signal
    __info : object
        sound file object having the info of the audio file
    __energy : list
        list of the ranks for the audio signal
    __snrBefore : list
        list to store the snr of the original audio
    __snrAfter : list
        list to store the snr of the de-noised audio
    __silenceThreshold : int
        threshold value to determine the rank
    __cache : Cache
        object of the cache to store the audio file info
    __fwt : FastWaveletTransform
        performs dwt & idwt on the data
    __compressor : VisuShrinkCompressor
        performs visu shrink thresholding on the coefficients
    """
    def __init__(self):
        self.__fileName = None
        self.__rate = None
        self.__data = None
        self.__plot = False
        self.__info = None
        self.__energy = None
        self.__snrBefore = list()
        self.__snrAfter = list()
        self.__silenceThreshold = SILENCE_THRESHOlD
        self.__cache = Cache()
        self.__fwt = FastWaveletTransform(WAVELET)
        self.__compressor = VisuShrinkCompressor()

    def __get_energy_rms(self, block):
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
        if np.sqrt(np.mean(block ** 2)) > self.__silenceThreshold:
            return RANK_AUDIO
        return 0

    def __set_audio_info(self):
        """ Storing audio info """
        self.__cache.write_data(CACHE_AUDIO_INFO, self.__info)

    def __plot_snr(self):
        """
        Plotting the snrs for the original and the de-noised signals, the snrs are collected
        during the processing, and the mean of the data is used to represent the final values
        The snr is very low (negative with raised to values) so abs of the mean is taken.
        Note: not to be mistaken with positive values

        this SNR is  the reciprocal of the coefficient of variation, i.e.,
        the ratio of mean to standard deviation of a signal, refer the snr function in wavelet/utility
        """

        width = 0.1
        x_orig = np.arange(len(self.__snrBefore))
        plt.bar(x_orig - width / 2, np.abs(self.__snrBefore), width=width, label='Original')
        plt.bar(x_orig + width / 2, np.abs(self.__snrAfter), width=width, label='De-noised')

        plt.title("Signal to noise ratios SNR(dB)")
        plt.legend(loc=0)
        plt.tight_layout()
        plt.show()

    def __del__(self):
        """
        clean up
        """
        del self.__cache
        del self.__fwt
        del self.__compressor

        Log.d("Cleaning up.")

    def start_processing(self, inputFile, outputFile, plot=False):
        """
        Calculates the de noised signal based on the wavelets
        default wavelet is = db4, mode = per and thresh method = soft.

        The input audio is read in small portions de-noised and appended to the
        audio file in same manner. Also it supports multiple channels and the
        size of the input audio file and output audio files are same so no
        data loss.

        Uses the VISU Shrink thresholding for the noise in the audio signal

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

        self.__fileName = inputFile
        self.__info = soundfile.info(self.__fileName)
        self.__set_audio_info()
        self.__rate = self.__info.samplerate
        self.__energy = []
        Log.i(f"Audio duration is {self.__info.duration}.")

        # creating and opening the output audio file
        with soundfile.SoundFile(outputFile, mode="w", samplerate=self.__rate, channels=1) as out:
            for block in soundfile.blocks(self.__fileName, int(self.__rate * self.__info.duration * AUDIO_BLOCK_PER)):
                # processing only single channel
                if block.ndim > 1:
                    block = block[:, 0]

                # cal all coefficients
                level = getExponent(len(block))

                # decomposition -> threshold -> reconstruction
                coefficients = self.__fwt.wavedec(block, level=level)
                coefficients = self.__compressor.compress(coefficients)
                cleaned = self.__fwt.waverec(coefficients, level=level)

                # recreating the audio signal in original form and writing to the output file
                cleaned = np.array(cleaned, dtype=np.float_)
                out.write(cleaned)

                # collecting the signal to noise ratios
                self.__snrBefore.append(snr(block))
                self.__snrAfter.append(snr(cleaned))

                # calculating the audio rank
                self.__energy.extend([self.__get_energy_rms(cleaned)] * max(1, int(len(cleaned) / self.__rate)))

            if plot:
                self.__plot_snr()

        self.__cache.write_data(CACHE_RANK_AUDIO, self.__energy)
        Log.i("Audio de noised successfully")
        Log.d(f"Audio ranking length {len(self.__energy)}")
        Log.i("Audio ranking saved .............")
        Log.d(f"Garbage collected :: {gc.collect()}")
