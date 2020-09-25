"""
This file contains function to separate out video and audio using ffmpeg.
It consists of two functions to split and merge video and audio
using ffmpeg.
"""

import gc
import os

from lib.progress.progress import Progress
from lib.util.constants import OUT_VIDEO_FILE, IN_AUDIO_FILE, OUT_AUDIO_FILE
from lib.util.ffmpegTools import split, merge
from lib.util.logger import Log


class FFMPEG:
    """
    FFMPEG helper function to make use of the subprocess module to run command
    to trim and split video files. The std out logs are parsed to generate a progress
    bar to show the progress of the command that is being executed.

    Attributes
    ----------
    inputFileName : str
        input video file name
    inputFilePath : str
        input video file name
    outputVideoFileName : str
        output video file name
    inputAudioFileName : str
        original splitted audio file name
    outputAudioFileName : str
        de-noised audio file name
    outputFilePath : str
        same as the input file path
    progressBar : tqdm
        object of tqdm to display a progress bar
    """
    def __init__(self):
        self.inputFileName = None
        self.inputFilePath = None
        self.outputVideoFileName = None
        self.inputAudioFileName = None
        self.outputAudioFileName = None
        self.outputFilePath = None
        self.progressBar = None

    def getInputFileNamePath(self):
        """
        Returns file name that was used for processing

        Returns
        --------
        str
            final name and path of the input video file
        """
        if self.inputFileName is not None:
            return os.path.join(self.inputFilePath, self.inputFileName)
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
        if self.outputVideoFileName is not None:
            return os.path.join(self.outputFilePath, self.outputVideoFileName)
        return None

    def getInputAudioFileNamePath(self):
        """
        Returns name and path of the input audio file that is split from the input video file

        Returns
        -------
        str
            input audio file name and path ready to de-noise
        """
        if self.inputAudioFileName is not None:
            return os.path.join(self.outputFilePath, self.inputAudioFileName)
        return None

    def getOutputAudioFileNamePath(self):
        """
        Returns the output audio file name and path that is de-noised

        Returns
        -------
        str
            returns the output audio file
        """
        if self.outputAudioFileName is not None:
            return os.path.join(self.outputFilePath, self.outputAudioFileName)
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

        self.inputFilePath = os.path.dirname(inputFile)
        self.outputFilePath = self.inputFilePath
        self.inputFileName = os.path.basename(inputFile)
        self.outputVideoFileName = os.path.splitext(self.inputFileName)[0] + OUT_VIDEO_FILE
        self.inputAudioFileName = os.path.splitext(self.inputFileName)[0] + IN_AUDIO_FILE
        self.outputAudioFileName = os.path.splitext(self.inputFileName)[0] + OUT_AUDIO_FILE

        # call ffmpeg tool to do the splitting
        try:
            Log.i("Splitting the video file.")
            self.progressBar = Progress()
            for log in split(inputFile,
                             os.path.join(self.outputFilePath, self.inputAudioFileName)):
                self.progressBar.displayProgress(log)

        except ChildProcessError:
            Log.e("Splitting the input file has caused an error.")
            self.progressBar.clear()
            return False

        finally:
            self.progressBar.complete()
            print("----------------------------------------------------------")
            return True

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
        if self.inputFileName is None or self.outputAudioFileName is None:
            Log.e("Files not found for merging")
            return False

        # call ffmpeg tool to merge the files
        try:
            self.progressBar = Progress()
            Log.i("Writing the output video file.")
            for log in merge(os.path.join(self.outputFilePath, self.inputFileName),
                             os.path.join(self.outputFilePath, self.outputAudioFileName),
                             os.path.join(self.outputFilePath, self.outputVideoFileName), timestamps):
                self.progressBar.displayProgress(log)

        except ChildProcessError:
            Log.e("Merging the files has caused an error.")
            self.progressBar.clear()
            return False

        finally:
            self.progressBar.complete()
            print("----------------------------------------------------------")
            return True

    def cleanUp(self):
        """
        Deleted the audio files created while audio processing.
        Minor clean ups.
        """
        if os.path.isfile(os.path.join(self.outputFilePath, self.inputAudioFileName)):
            os.unlink(os.path.join(self.outputFilePath, self.inputAudioFileName))

        if os.path.isfile(os.path.join(self.outputFilePath, self.outputAudioFileName)):
            os.unlink(os.path.join(self.outputFilePath, self.outputAudioFileName))

        del self.progressBar
        Log.d(f"Garbage collected :: {gc.collect()}")
        Log.d("Clean up completed.")
