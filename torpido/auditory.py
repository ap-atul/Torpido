"""
Audio de noising process: this class will read the audio file and using
wavelet transforms a threshold will be added to each window with certain level
"""

import gc

import matplotlib
import numpy as np
import soundfile
from matplotlib import pyplot as plt

from .config.cache import Cache
from .config.config import Config
from .config.constants import *
from .tools.logger import Log
from .tools.ranking import Ranking
from .wavelet import FastWaveletTransform, VisuShrinkCompressor

matplotlib.use("TkAgg")
plt.rcParams["figure.figsize"] = (10, 4.5)


class Auditory:
    """
    Audio de noising is done using Wavelet Transform on the input audio signal. The functions read
    the input audio signal in small portions and append the de-noised signal to the output audio
    file that is later merged with the input video file

    Attributes
    ----------
    __file_name : str
        input audio file
    __rate : int
        sample rate of the audio signal in frequency
    __plot : bool
        plot the signal
    __info : object
        sound file object having the info of the audio file
    __energy : list
        list of the ranks for the audio signal
    __silence_threshold : int
        threshold value to determine the rank
    __cache : Cache
        object of the cache to store the audio file info
    __fwt : FastWaveletTransform
        performs dwt & idwt on the data
    __compressor : VisuShrinkCompressor
        performs visu shrink thresholding on the coefficients
    """
    def __init__(self):
        self.__file_name = self.__rate = self.__data = None
        self.__plot = self.__info = self.__energy = None
        self.__silence_threshold, self.__cache = Config.SILENCE_THRESHOLD, Cache()
        self.__fwt = FastWaveletTransform(Config.WAVELET)
        self.__compressor = VisuShrinkCompressor()

    def __get_energy_rms(self, block):
        """
        RMS = Root Mean Square to calculate the signal data to the dB, if signal
        satisfies some threshold the ranking can be affected and audio portion
        can be ranked
        RMS -> square root of mean of squared data

        Parameters
        ----------
        block : np-array
            input signal block

        Returns
        -------
        int
            rank for the portion which is then set for all the portion of data
        """
        if np.sqrt(np.mean(np.power(block, 2))) > self.__silence_threshold:
            return Config.RANK_AUDIO
        return 0

    def __set_audio_info(self):
        """ Storing audio info """
        self.__cache.write_data(CACHE_AUDIO_INFO, self.__info)

    def _specshow(self, original_signal, clean_signal, frame_rate):
        """
        Plotting the spectrogram for the original and the de-noised signals, the spectrogram are collected
        during the processing, and the mean of the data is used to represent the final values
        """
        original_signal, clean_signal = (
                                            list(filter(lambda x: x != 0, original_signal)),
                                            list(filter(lambda x: x != 0, clean_signal))
                                        )

        if len(original_signal) == 0 or len(clean_signal) == 0:
            return

        fig = plt.figure()

        # plot original signal
        ax = fig.add_subplot(211)
        ax.specgram(original_signal, Fs=frame_rate)
        ax.title.set_text("Original Signal")

        # plot clean signal
        ax = fig.add_subplot(212)
        ax.specgram(clean_signal, Fs=frame_rate)
        ax.title.set_text("Clean Signal")

        plt.tight_layout()
        plt.show()

    def __del__(self):
        """ clean up """
        del self.__cache, self.__fwt, self.__compressor
        Log.d("Cleaning up.")

    def start_processing(self, input_file, output_file, plot=False):
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
        input_file : str
            input audio file
        output_file : str
            output audio file
        plot : bool
            True to plot the audio signal

        """
        if os.path.isfile(input_file) is False:
            Log.e(f"File {input_file} does not exists")
            return

        self.__file_name, self.__energy = input_file, list()
        self.__info = soundfile.info(self.__file_name)
        self.__rate = self.__info.samplerate
        self.__set_audio_info()
        Log.i(f"Audio duration is {self.__info.duration}.")

        count, to_read = 0, int(self.__rate * self.__info.duration * Config.AUDIO_BLOCK_PER)
        # creating and opening the output audio file
        with soundfile.SoundFile(output_file, mode="w", samplerate=self.__rate, channels=1) as out:
            for block in soundfile.blocks(self.__file_name, to_read):

                # taking only the single channel
                # without losing any data
                if block.ndim > 1:
                    block = block.sum(axis=1) / 2

                # decomposition -> threshold -> reconstruction
                coefficients = self.__fwt.wavedec(block)
                coefficients = self.__compressor.compress(coefficients)
                cleaned = self.__fwt.waverec(coefficients)

                # recreating the audio signal in original form and writing to the output file
                cleaned = np.array(cleaned, dtype=np.float_)
                out.write(cleaned)

                # calculating the audio rank
                self.__energy.extend([self.__get_energy_rms(cleaned)] * max(1, int(len(cleaned) / self.__rate)))
                count += 1

                if plot and (count == 5 or count == 7):
                    self._specshow(block, cleaned, self.__info.samplerate)

        Ranking.add(CACHE_RANK_AUDIO, self.__energy)
        Log.i("Audio de noised successfully")
        Log.d(f"Audio ranking length {len(self.__energy)}")
        Log.i("Audio ranking saved .............")
        Log.d(f"Garbage collected :: {gc.collect()}")
