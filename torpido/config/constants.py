import os
from sys import platform

# file to save all the constants that are to be used
# os type
LINUX = platform.startswith("linux")

# process priority ((20 − nice)/(20 − 0) = %)
NICE = 15

# max priority for the entire app (max * np = < 19)
NICE_MAX = 5

# ******************* CACHE PART *************************
# cache store dir
CACHE_DIR = "torpido_tmp/"

# cache file name
CACHE_NAME = ".vea_cache.tmp"

# cache keys
# video fps key
CACHE_FPS = "FPS"

# video frame count
CACHE_FRAME_COUNT = "FRAME_COUNT"

# audio info object
CACHE_AUDIO_INFO = "CACHE_AUDIO_INFO"

# ranking for audio
CACHE_RANK_AUDIO = "CACHE_AUDIO_RANK"

# ranking for motion
CACHE_RANK_MOTION = "CACHE_RANK_MOTION"

# ranking for blur
CACHE_RANK_BLUR = "CACHE_RANK_BLUR"

# ranking for text
CACHE_RANK_TEXT = "CACHE_RANK_TEXT"

# video width
CACHE_VIDEO_WIDTH = "CACHE_VIDEO_WIDTH"

# video height
CACHE_VIDEO_HEIGHT = "CACHE_VIDEO_HEIGHT"

# ******************* VIDEO PART *************************
# video width to keep while processing
VIDEO_WIDTH = 500

# window level in the wavelet level
WAVELET_LEVEL = 1

# decomposition and re composition mode
DEC_REC_MODE = "per"

# wave threshold method
WAVE_THRESH = "soft"

# ********************** TEXTUAL PART ************************

# text detection model directory
TEXT_EAST_MODEL_PATH = os.environ['EAST_MODEL']

# ****************** FFMPEG *************************************
# output video file name extension
OUT_VIDEO_FILE = "_edited_by_torpido"

# input audio name to process
IN_AUDIO_FILE = "_audio.wav"

# output audio name processes and cleaned
OUT_AUDIO_FILE = "_audio_de_noised.wav"

# thumbnail file name
THUMBNAIL_FILE = "_thumbnail.jpg"

# supported video file formats
SUPPORTED_VIDEO_FILES = [".mp4", ".webm", ".mkv", ".mov", ".flv", ".avi", ".ogg"]

# fade in effect duration in seconds
FADE_IN = 3

# fade out effect duration in seconds
FADE_OUT = 3

# ******************** UI ***************************************
# minimum height of window
WINDOW_HEIGHT = 630

# minimum width of window
WINDOW_WIDTH = 850

# name of the window
WINDOW_TITLE = "Video Editing Automation (aka. Torpido)"

# ******************** LOG **************************
# log file
LOG_FILE = "torpido.log"

# ******************* IDENTIFIER COMM *****************
ID_COM_LOGGER = "logger_communication_channel"
ID_COM_PROGRESS = "progress_communication_channel"
ID_COM_VIDEO = "video_communication_channel"

REBOOT = 101


def rinit():
    """
    This function can replace all the values with new ones, but takes a very bad approach,
    currently not using it but it can be used any way.

    The thing it does it whatever variables are defined here, it will update in the global
    scope which will be accessible instantly without restart.
    """
    globals().update(locals())
