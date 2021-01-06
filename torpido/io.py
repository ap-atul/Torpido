"""
This file contains function to separate out video and audio using ffmpeg.
It consists of two functions to split and merge video and audio
using ffmpeg.
"""
import os

from torpido.config.constants import CACHE_DIR, CACHE_NAME, IN_AUDIO_FILE, OUT_AUDIO_FILE, OUT_VIDEO_FILE
from torpido.exceptions import AudioStreamMissingException, FFmpegProcessException
from torpido.progress import Progress
from torpido.tools.ffmpeg import split, merge
from torpido.tools.logger import Log


class FFMPEG:
    """
    FFMPEG helper function to make use of the subprocess module to run command
    to trim and split video files. The std out logs are parsed to generate a progress
    bar to show the progress of the command that is being executed.

    Attributes
    ----------
    __input_file_name : str
        input video file name
    __input_file_path : str
        input video file name
    __output_video_file_name : str
        output video file name
    __input_audio_file_name : str
        original splatted audio file name
    __output_audio_file_name : str
        de-noised audio file name
    __output_file_path : str
        same as the input file path
    __intro : str
        name of the intro video file
    __extro : str
        name of the extro video file
    __extension : str
        name of the extension of the input file
    __progress_bar : tqdm
        object of tqdm to display a progress bar
    """
    def __init__(self):
        self.__input_file_name = None
        self.__input_file_path = None
        self.__output_video_file_name = None
        self.__input_audio_file_name = None
        self.__output_audio_file_name = None
        self.__output_file_path = None
        self.__intro = None
        self.__extro = None
        self.__extension = None
        self.__progress_bar = None

    def set_intro_video(self, intro):
        """ Sets the intro video file """
        self.__intro = intro

    def set_outro_video(self, extro):
        """ Sets the extro video file """
        self.__extro = extro

    def get_input_file_name_path(self):
        """
        Returns file name that was used for processing

        Returns
        --------
        str
            final name and path of the input video file
        """
        if self.__input_file_name is not None:
            return os.path.join(self.__input_file_path, self.__input_file_name)
        return None

    def get_output_file_name_path(self):
        """
        Returns output file name generated from input
        file name

        Returns
        -------
        str
            output file name and path of the video file
        """
        if self.__output_video_file_name is not None:
            return os.path.join(self.__output_file_path, self.__output_video_file_name)
        return None

    def get_input_audio_file_name_path(self):
        """
        Returns name and path of the input audio file that is split from the input video file

        Returns
        -------
        str
            input audio file name and path ready to de-noise
        """
        if self.__input_audio_file_name is not None:
            return os.path.join(self.__output_file_path, self.__input_audio_file_name)
        return None

    def get_output_audio_file_name_path(self):
        """
        Returns the output audio file name and path that is de-noised

        Returns
        -------
        str
            returns the output audio file
        """
        if self.__output_audio_file_name is not None:
            return os.path.join(self.__output_file_path, self.__output_audio_file_name)
        return None

    def split_video_audio(self, input_file):
        """
        Function to split the input video file into audio file using FFmpeg. Progress bar is
        updated as the command is run

        Note : No new video file is created, only audio file is created

        Parameters
        ----------
        input_file : str
            input video file

        Returns
        -------
        bool
            returns True if success else Error

        """
        if os.path.isfile(input_file) is False:
            Log.e("File does not exists")
            return False

        # storing all the references
        self.__input_file_path = os.path.dirname(input_file)
        self.__output_file_path = self.__input_file_path
        self.__input_file_name = os.path.basename(input_file)

        _, self.__extension = os.path.splitext(self.__input_file_name)
        self.__output_video_file_name = "".join([self.__input_file_name, OUT_VIDEO_FILE, self.__extension])

        self.__input_audio_file_name = self.__input_file_name + IN_AUDIO_FILE
        self.__output_audio_file_name = self.__input_file_name + OUT_AUDIO_FILE

        # call ffmpeg tool to do the splitting
        try:
            Log.i("Splitting the video file.")
            self.__progress_bar = Progress()
            for log in split(input_file,
                             os.path.join(self.__output_file_path, self.__input_audio_file_name)):
                self.__progress_bar.display(log)

            if not os.path.isfile(os.path.join(self.__output_file_path, self.__input_audio_file_name)):
                raise AudioStreamMissingException

            self.__progress_bar.complete()
            print("----------------------------------------------------------")
            return True

        # no audio in the video
        except AudioStreamMissingException:
            Log.e(AudioStreamMissingException.cause)
            self.__progress_bar.clear()
            return False

    def merge_video_audio(self, timestamps):
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
        if self.__input_file_name is None or self.__output_audio_file_name is None:
            Log.e("Files not found for merging")
            return False

        # call ffmpeg tool to merge the files
        try:
            self.__progress_bar = Progress()
            Log.i("Writing the output video file.")
            for log in merge(os.path.join(self.__output_file_path, self.__input_file_name),
                             os.path.join(self.__output_file_path, self.__output_audio_file_name),
                             os.path.join(self.__output_file_path, self.__output_video_file_name),
                             timestamps,
                             intro=self.__intro,
                             extro=self.__extro):
                self.__progress_bar.display(log)

            if not os.path.isfile(os.path.join(self.__output_file_path, self.__output_video_file_name)):
                raise FFmpegProcessException

            self.__progress_bar.complete()
            print("----------------------------------------------------------")
            return True

        except FFmpegProcessException:
            Log.e(FFmpegProcessException.cause)
            self.__progress_bar.clear()
            return False

    def clean_up(self):
        """
        Deletes extra files created while processing, deletes the ranking files
        cache, etc.
        """

        # processing is not yet started for something went wrong
        if self.__input_file_name is not None:

            # original audio split from the video file
            if os.path.isfile(os.path.join(self.__output_file_path, self.__input_audio_file_name)):
                os.unlink(os.path.join(self.__output_file_path, self.__input_audio_file_name))

            # de-noised audio file output of Auditory
            if os.path.isfile(os.path.join(self.__output_file_path, self.__output_audio_file_name)):
                os.unlink(os.path.join(self.__output_file_path, self.__output_audio_file_name))

        # cache storage file
        if os.path.isfile(os.path.join(CACHE_DIR, CACHE_NAME)):
            os.unlink(os.path.join(CACHE_DIR, CACHE_NAME))

        if self.__progress_bar is not None:
            del self.__progress_bar

        Log.d("Clean up completed.")
