import os

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
# video width to keep while processing
VIDEO_WIDTH = 500

# threshold for video reading motion
MOTION_THRESHOLD = 50

# threshold for blur detection
BLUR_THRESHOLD = 500

# ******************* AUDIO PART *************************
# reading 10 percent of audio file at a time
AUDIO_BLOCK_PER = 0.2

# window level in the wavelet level
WAVELET_LEVEL = 1

# wavelet used to de noise/  Coiflet wavelet band
WAVELET = "coif1"

# decomposition and re composition mode
DEC_REC_MODE = "per"

# wave threshold method
WAVE_THRESH = "soft"

# silence threshold
SILENCE_THRESHOlD = 0.005

# ********************** TEXTUAL PART ************************
# min confidence of the text being detected
TEXT_MIN_CONFIDENCE = 0.5

# text detection is slow so some frames are skipped (sec)
TEXT_SKIP_FRAMES = 10

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
WATCHER_DELAY = 3

# ******************** UI ***************************************
# minimum height of window
WINDOW_HEIGHT = 500

# minimum width of window
WINDOW_WIDTH = 900

# name of the window
WINDOW_TITLE = "Video Editing Automation (aka. Torpido)"
