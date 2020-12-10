"""
File to load runtime config for the system. Integration for the
settings features the UI and for other functionality as well.
All constants are here defined in the file and can be loaded from there
on runtime and can be changed at runtime, similar to YMAL files
"""

import os

# text file storing all the configurations
CONFIG_FILE = "config.torpido"

# separator for the key & value in the text file
SEPARATOR = ":"

# ranking for motion in video
RANK_MOTION = 3

# ranking for blur in video
RANK_BLUR = 2

# ranking for audio silence
RANK_AUDIO = 3

# ranking for text in video
RANK_TEXT = 5

# output video min rank
MIN_RANK_OUT_VIDEO = 3

# ******************* VIDEO PART *************************
# threshold for video reading motion
MOTION_THRESHOLD = 50

# threshold for blur detection
BLUR_THRESHOLD = 500

# ******************* AUDIO PART *************************
# reading 10 percent of audio file at a time
AUDIO_BLOCK_PER = 0.2

# wavelet used to de noise/  Coiflet wavelet band
WAVELET = "coif1"

# silence threshold
SILENCE_THRESHOlD = 0.005

# ********************** TEXTUAL PART ************************
# min confidence of the text being detected
TEXT_MIN_CONFIDENCE = 0.5

# text detection is slow so some frames are skipped (sec)
TEXT_SKIP_FRAMES = 10

# delay to check the CPU and MEM usage (in secs)
WATCHER_DELAY = 3


class File:
    """
    All interactions with the config file would be handled by this class.
    Responsible to write, read and initialize the configs.
    """

    @staticmethod
    def init():
        """
        Creates the file and writes all initials values, constants
        to the initial following the file format.
        All changes will be rewritten on request from the ui component
        All constants bare same key aas their name mentioned
        """
        configs = [("RANK_MOTION" + SEPARATOR + str(RANK_MOTION) + "\n"),
                   ("RANK_BLUR" + SEPARATOR + str(RANK_BLUR) + "\n"),
                   ("RANK_TEXT" + SEPARATOR + str(RANK_TEXT) + "\n"),
                   ("RANK_AUDIO" + SEPARATOR + str(RANK_AUDIO) + "\n"),

                   ("MIN_RANK_OUT_VIDEO" + SEPARATOR + str(MIN_RANK_OUT_VIDEO) + "\n"),
                   ("MOTION_THRESHOLD" + SEPARATOR + str(MOTION_THRESHOLD) + "\n"),
                   ("BLUR_THRESHOLD" + SEPARATOR + str(BLUR_THRESHOLD) + "\n"),
                   ("SILENCE_THRESHOlD" + SEPARATOR + str(SILENCE_THRESHOlD) + "\n"),
                   ("TEXT_MIN_CONFIDENCE" + SEPARATOR + str(TEXT_MIN_CONFIDENCE) + "\n"),

                   ("AUDIO_BLOCK_PER" + SEPARATOR + str(AUDIO_BLOCK_PER) + "\n"),
                   ("TEXT_SKIP_FRAMES" + SEPARATOR + str(TEXT_SKIP_FRAMES) + "\n"),
                   ("WAVELET" + SEPARATOR + str(WAVELET) + "\n"),

                   ("WATCHER_DELAY" + SEPARATOR + str(WATCHER_DELAY)),
                   ]

        with open(CONFIG_FILE, "w") as config:
            config.writelines(configs)
            config.close()

    @staticmethod
    def write(configs):
        """
        Write the entire dictionary containing the updated values
        """
        with open(CONFIG_FILE, "w") as config:
            for key, value in configs:
                config.write(str(key) + SEPARATOR + str(value))
            config.close()

    @staticmethod
    def get():
        """
        Read the file, parse the data in dictionary

        Returns
        -------
        dict
            dictionary of all the constants and their values
        """
        configs = dict()

        with open(CONFIG_FILE, "r") as config:
            for line in config.readlines():
                key, value = line.split(SEPARATOR)
                configs[key] = value.replace("\n", "")

        return configs


class Config:
    """
    Manages the config for the system, interacts with the File
    class for read / write and init
    Make sures the config is present and update

    Attributes
    ----------
    Config.configs : dict
        dict that stores all the config for the system
    """

    if not os.path.isfile(CONFIG_FILE):
        File.init()

    # stores the configurations
    configs = File.get()

    @staticmethod
    def read(key, dtype):
        """
        Read the value for the key, since the api is internal their shouldn't
        be any key that is not present
        This function is called by the Constants file, so their is no
        incorrectness of the key

        Parameters
        ----------
        key : str
            the value for the key to return
        dtype : type
            conversion of the value to the correct format

        Returns
        -------
        val
            value for the key
        """
        return dtype(Config.configs.get(key, None))

    @staticmethod
    def write(key, value):
        """
        Update the config for the system. All values will be rewritten to
        the file, which will reflect in the system as in real-time
        Easy integration with the UI

        Parameters
        ----------
        key : str
            value of the key, identifier from the Constants file
        value : val
            some value to store

        """
        Config.configs[key] = value
        File.write(Config.configs)
