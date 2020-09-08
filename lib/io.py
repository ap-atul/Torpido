import os

from lib.util.constants import OUT_VIDEO_FILE, IN_AUDIO_FILE
from lib.util.ffmpegTools import split, merge

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
        self.outputAudioFileName = None
        self.outputFilePath = None

    def getInputFileNamePath(self):
        """
        return file name that was used for processing
        :return: string, file path with name
        """
        return os.path.join(self.inputFilePath, self.inputFileName)

    def getOutputFileNamePath(self):
        """
        returns output file name generated from input
        file name
        :return: string, file path with name
        """
        return os.path.join(self.outputFilePath, self.outputVideoFileName)

    def getOutputAudioFileNamePath(self):
        """
        returns the output audio file name generated from input
        :return: string, audio file name with path
        """
        return os.path.join(self.outputFilePath, self.outputAudioFileName)

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
            print("[ERROR] File does not exists")
            return False

        self.inputFilePath = os.path.dirname(inputFile)
        self.outputFilePath = self.inputFilePath
        self.inputFileName = os.path.basename(inputFile)
        self.outputVideoFileName = os.path.splitext(self.inputFileName)[0] + OUT_VIDEO_FILE
        self.outputAudioFileName = os.path.splitext(self.inputFileName)[0] + IN_AUDIO_FILE

        # call ffmpeg tool to do the splitting
        try:
            for _ in split(inputFile,
                           os.path.join(self.outputFilePath, self.outputAudioFileName)):
                pass
        except ChildProcessError:
            print("[ERROR] Splitting the input file has caused an error.")
            return False
        return True

    def mergeAudioVideo(self):
        """
        function to call the merging on video and audio streams
        and create an output file with generated name
        :return: boolean, true for success
        """
        print(self.inputFileName , self.outputAudioFileName)
        if self.inputFileName is None or self.outputAudioFileName is None:
            print("[ERROR] Files not found for merging")
            return False

        # call ffmpeg tool to merge the files
        try:
            for _ in merge(os.path.join(self.outputFilePath, self.inputFileName),
                           os.path.join(self.outputFilePath, self.outputAudioFileName),
                           os.path.join(self.outputFilePath, self.outputVideoFileName)):
                pass
        except ChildProcessError:
            print("[ERROR] Merging the files has caused an error.")
            return False
        return True
