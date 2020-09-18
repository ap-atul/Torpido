import gc
import os

from lib.progress.progress import Progress
from lib.util.constants import OUT_VIDEO_FILE, IN_AUDIO_FILE, OUT_AUDIO_FILE
from lib.util.ffmpegTools import split, merge
from lib.util.logger import Log

"""
This file contains function to separate out video and audio using ffmpeg.
It consists of two functions to split and merge video and audio
using ffmpeg.
"""


class FFMPEG:
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
        return file name that was used for processing
        :return: string, file path with name
        """
        if self.inputFileName is not None:
            return os.path.join(self.inputFilePath, self.inputFileName)
        return None

    def getOutputFileNamePath(self):
        """
        returns output file name generated from input
        file name
        :return: string, file path with name
        """
        if self.outputVideoFileName is not None:
            return os.path.join(self.outputFilePath, self.outputVideoFileName)
        return None

    def getInputAudioFileNamePath(self):
        """
        returns the output audio file name generated from input
        :return: string, audio file name with path
        """
        if self.inputAudioFileName is not None:
            return os.path.join(self.outputFilePath, self.inputAudioFileName)
        return None

    def getOutputAudioFileNamePath(self):
        """
        returns the output audio file name generated from input
        :return: string, audio file name with path
        """
        if self.outputAudioFileName is not None:
            return os.path.join(self.outputFilePath, self.outputAudioFileName)
        return None

    def splitVideoAudio(self, inputFile):
        """
        function to start the splitting video into audio and
        video.
        NOTE: there is no video created the input video is
        processed.
        :param inputFile: file path of input video to process
        :return: boolean, true if success, false if exception/error
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
        function to call the merging on video and audio streams
        and create an output file with generated name
        :param timestamps: list of timestamps containing list (start and end)
        :return: boolean, true for success
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
        delete the audio files generated
        :return: None
        """
        if os.path.isfile(os.path.join(self.outputFilePath, self.inputAudioFileName)):
            os.unlink(os.path.join(self.outputFilePath, self.inputAudioFileName))

        if os.path.isfile(os.path.join(self.outputFilePath, self.outputAudioFileName)):
            os.unlink(os.path.join(self.outputFilePath, self.outputAudioFileName))

        del self.progressBar
        Log.d(f"Garbage collected :: {gc.collect()}")
        Log.d("Clean up completed.")
