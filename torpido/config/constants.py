import os

from torpido.config.config import Config

# file to save all the constants that are to be used
# ******************* CACHE PART *************************
# cache store dir
CACHE_DIR = "torpido_tmp/"

# cache file name
CACHE_NAME = "vea_cache.tmp"

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

# ******************* RANKS ****************************
# ranking for motion in video
RANK_MOTION = Config.read("RANK_MOTION", float)

# ranking for blur in video
RANK_BLUR = Config.read("RANK_BLUR", float)

# ranking for audio silence
RANK_AUDIO = Config.read("RANK_AUDIO", float)

# ranking for text in video
RANK_TEXT = Config.read("RANK_TEXT", float)

# output video min rank
MIN_RANK_OUT_VIDEO = Config.read("MIN_RANK_OUT_VIDEO", float)

# ******************* VIDEO PART *************************
# video width to keep while processing
VIDEO_WIDTH = 500

# threshold for video reading motion
MOTION_THRESHOLD = Config.read("MOTION_THRESHOLD", int)

# threshold for blur detection
BLUR_THRESHOLD = Config.read("BLUR_THRESHOLD", int)

# ******************* AUDIO PART *************************
# reading 10 percent of audio file at a time
AUDIO_BLOCK_PER = Config.read("AUDIO_BLOCK_PER", float)

# window level in the wavelet level
WAVELET_LEVEL = 1

# wavelet used to de noise/  Coiflet wavelet band
WAVELET = Config.read("WAVELET", str)

# decomposition and re composition mode
DEC_REC_MODE = "per"

# wave threshold method
WAVE_THRESH = "soft"

# silence threshold
SILENCE_THRESHOlD = Config.read("SILENCE_THRESHOlD", float)

# ********************** TEXTUAL PART ************************
# min confidence of the text being detected
TEXT_MIN_CONFIDENCE = Config.read("TEXT_MIN_CONFIDENCE", float)

# text detection is slow so some frames are skipped (sec)
TEXT_SKIP_FRAMES = Config.read("TEXT_SKIP_FRAMES", int)

# text detection model directory
TEXT_EAST_MODEL_PATH = os.environ['EAST_MODEL']

# ****************** FFMPEG *************************************
# output video file name extension
OUT_VIDEO_FILE = "_edited_by_torpido.mp4"

# input audio name to process
IN_AUDIO_FILE = "_audio.wav"

# output audio name processes and cleaned
OUT_AUDIO_FILE = "_audio_de_noised.wav"

# supported video file formats
SUPPORTED_VIDEO_FILES = [".mp4", ".webm", ".mkv", ".mov", ".flv", ".avi", ".ogg"]

# ********************* WATCHER ***********************************
# delay to check the CPU and MEM usage (in secs)
WATCHER_DELAY = Config.read("WATCHER_DELAY", int)

# ******************** UI ***************************************
# minimum height of window
WINDOW_HEIGHT = 630

# minimum width of window
WINDOW_WIDTH = 1000

# name of the window
WINDOW_TITLE = "Video Editing Automation (aka. Torpido)"

# ******************** LOG **************************
# log file
LOG_FILE = "torpido.log"
