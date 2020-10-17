"""
This file contains function to separate out video and audio using ffmpeg.
It consists of two functions to split and merge video and audio
using ffmpeg.
"""

import gc
import os

from lib.exceptions.custom import AudioStreamMissingException, FFmpegProcessException
from lib.progress.progress import Progress
from lib.util.constants import *
from lib.util.ffmpegTools import split, merge
from lib.util.logger import Log


class FFMPEG:
    """
    FFMPEG helper function to make use of the subprocess module to run command
    to trim and split video files. The std out logs are parsed to generate a progress
    bar to show the progress of the command that is being executed.

    Attributes
    ----------
    __inputFileName : str
        input video file name
    __inputFilePath : str
        input video file name
    __outputVideoFileName : str
        output video file name
    __inputAudioFileName : str
        original splatted audio file name
    __outputAudioFileName : str
        de-noised audio file name
    __outputFilePath : str
        same as the input file path
    __progressBar : tqdm
        object of tqdm to display a progress bar
    """
    def __init__(self):
        self.__inputFileName = None
        self.__inputFilePath = None
        self.__outputVideoFileName = None
        self.__inputAudioFileName = None
        self.__outputAudioFileName = None
        self.__outputFilePath = None
        self.__progressBar = None

    def getInputFileNamePath(self):
        """
        Returns file name that was used for processing

        Returns
        --------
        str
            final name and path of the input video file
        """
        if self.__inputFileName is not None:
            return os.path.join(self.__inputFilePath, self.__inputFileName)
        return None

    def getOutputFileNamePath(self):
        """
        Returns output file name generated from input
        file name

        Returns
        -------
        str
            output file name and path of the video file
        """
        if self.__outputVideoFileName is not None:
            Log.e(self.__outputVideoFileName)
            Log.e(self.__outputFilePath)
            return os.path.join(self.__outputFilePath, self.__outputVideoFileName)
        return None

    def getInputAudioFileNamePath(self):
        """
        Returns name and path of the input audio file that is split from the input video file

        Returns
        -------
        str
            input audio file name and path ready to de-noise
        """
        if self.__inputAudioFileName is not None:
            return os.path.join(self.__outputFilePath, self.__inputAudioFileName)
        return None

    def getOutputAudioFileNamePath(self):
        """
        Returns the output audio file name and path that is de-noised

        Returns
        -------
        str
            returns the output audio file
        """
        if self.__outputAudioFileName is not None:
            return os.path.join(self.__outputFilePath, self.__outputAudioFileName)
        return None

    def splitVideoAudio(self, inputFile):
        """
        Function to split the input video file into audio file using FFmpeg. Progress bar is
        updated as the command is run

        Note : No new video file is created, only audio file is created

        Parameters
        ----------
        inputFile : str
            input video file

        Returns
        -------
        bool
            returns True if success else Error

        """
        if os.path.isfile(inputFile) is False:
            Log.e("File does not exists")
            return False

        # storing all the references
        self.__inputFilePath = os.path.dirname(inputFile)
        self.__outputFilePath = self.__inputFilePath
        self.__inputFileName = os.path.basename(inputFile)
        self.__outputVideoFileName = os.path.splitext(self.__inputFileName)[0] + OUT_VIDEO_FILE
        self.__inputAudioFileName = os.path.splitext(self.__inputFileName)[0] + IN_AUDIO_FILE
        self.__outputAudioFileName = os.path.splitext(self.__inputFileName)[0] + OUT_AUDIO_FILE

        # call ffmpeg tool to do the splitting
        try:
            Log.i("Splitting the video file.")
            self.__progressBar = Progress()
            for log in split(inputFile,
                             os.path.join(self.__outputFilePath, self.__inputAudioFileName)):
                self.__progressBar.displayProgress(log)

            if not os.path.isfile(os.path.join(self.__outputFilePath, self.__inputAudioFileName)):
                raise AudioStreamMissingException

            self.__progressBar.complete()
            print("----------------------------------------------------------")
            return True

        # no audio in the video
        except AudioStreamMissingException:
            Log.e(AudioStreamMissingException.cause)
            self.__progressBar.clear()
            return False

    def mergeAudioVideo(self, timestamps):
        """
        Function to merge the processed files using FFmpeg. The timestamps are used the trim
        the original video file and the audio stream is replaced with the de-noised audio
        file created by `Auditory`

        Parameters
        ----------
        timestamps : list
            list of start and end timestamps

        Returns
        -------
        bool
            True id success else error is raised
        """
        if self.__inputFileName is None or self.__outputAudioFileName is None:
            Log.e("Files not found for merging")
            return False

        # call ffmpeg tool to merge the files
        try:
            self.__progressBar = Progress()
            Log.i("Writing the output video file.")
            for log in merge(os.path.join(self.__outputFilePath, self.__inputFileName),
                             os.path.join(self.__outputFilePath, self.__outputAudioFileName),
                             os.path.join(self.__outputFilePath, self.__outputVideoFileName),
                             timestamps):
                self.__progressBar.displayProgress(log)

            if not os.path.isfile(os.path.join(self.__outputFilePath, self.__outputVideoFileName)):
                raise FFmpegProcessException

            self.__progressBar.complete()
            print("----------------------------------------------------------")
            return True

        except FFmpegProcessException:
            Log.e(FFmpegProcessException.cause)
            self.__progressBar.clear()
            return False

    def cleanUp(self):
        """
        Deleted the audio files created while audio processing.
        Minor clean ups.
        """
        # original audio split from the video file
        if os.path.isfile(os.path.join(self.__outputFilePath, self.__inputAudioFileName)):
            os.unlink(os.path.join(self.__outputFilePath, self.__inputAudioFileName))

        # de-noised audio file output of Auditory
        if os.path.isfile(os.path.join(self.__outputFilePath, self.__outputAudioFileName)):
            os.unlink(os.path.join(self.__outputFilePath, self.__outputAudioFileName))

        # motion ranking file
        if os.path.isfile(os.path.join(MODEL_DIR, RANK_OUT_MOTION)):
            os.unlink(os.path.join(MODEL_DIR, RANK_OUT_MOTION))

        # blur ranking file
        if os.path.isfile(os.path.join(MODEL_DIR, RANK_OUT_BLUR)):
            os.unlink(os.path.join(MODEL_DIR, RANK_OUT_BLUR))

        # audio ranking file
        if os.path.isfile(os.path.join(MODEL_DIR, RANK_OUT_AUDIO)):
            os.unlink(os.path.join(MODEL_DIR, RANK_OUT_AUDIO))

        # text ranking file
        if os.path.isfile(os.path.join(MODEL_DIR, RANK_OUT_TEXT)):
            os.unlink(os.path.join(MODEL_DIR, RANK_OUT_TEXT))

        # cache storage file
        if os.path.isfile(os.path.join(CACHE_DIR, CACHE_NAME)):
            os.unlink(os.path.join(CACHE_DIR, CACHE_NAME))

        del self.__progressBar
        Log.d(f"Garbage collected :: {gc.collect()}")
        Log.d("Clean up completed.")
