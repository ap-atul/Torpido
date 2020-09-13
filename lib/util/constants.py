# file to save all the constants that are to be used
# ******************* CACHE PART *************************
# cache store dir
CACHE_DIR = "model/"

# cache file name
CACHE_NAME = "vea_cache.joblib"

# cache keys
# video fps key
CACHE_FPS = "FPS"

# video frame count
CACHE_FRAME_COUNT = "FRAME_COUNT"

# audio info object
CACHE_AUDIO_INFO = "CACHE_AUDIO_INFO"

# ******************* RANKS ****************************
# ranking for motion in video
RANK_MOTION = 5

# ranking for blur in video
RANK_BLUR = 1

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

# ranking dir
RANK_DIR = "model/"

# output folder to save the rankings dumps
RANK_OUT_MOTION = 'motion_ranking.joblib'
RANK_OUT_BLUR = "blur_ranking.joblib"


# ******************* AUDIO PART *************************
# reading 5 percent of audio file at a time
AUDIO_BLOCK_PER = 0.5

# window level in the wavelet level
WAVELET_LEVEL = 1

# wavelet used to de noise/  Daubechies wavelet band
WAVELET = "db4"

# decomposition and re composition mode
DEC_REC_MODE = "per"

# wave threshold method
WAVE_THRESH = "soft"

# output folder to save the ranking dumps
RANK_OUT_AUDIO = 'audio_ranking.joblib'

# silence threshold
SILENCE_THRESHOlD = 0.005

# ********************** TEXTUAL PART ************************
# min confidence of the text being detected
TEXT_MIN_CONFIDENCE = 0.5

# text detection is slow so some frames are skipped (sec)
TEXT_SKIP_FRAMES = 20

# text detection model directory
TEXT_EAST_MODEL_PATH = "model/frozen_east_text_detection.pb"

# name of the ranking file
RANK_OUT_TEXT = "text_ranking.joblib"

# ******************* ANALYTICS PART *************************
MODEL_DIR = "model/"

# model name
MODEL_NAME = "views_predict_model.joblib"

# ****************** FFMPEG *************************************
# output video file name extension
OUT_VIDEO_FILE = "_edited_by_torpido.mp4"

# input audio name to process and later to merge
IN_AUDIO_FILE = "_audio.wav"

# supported video file formats
SUPPORTED_VIDEO_FILES = [".mp4", ".webm", ".mkv", ".mov", ".flv", ".avi", ".ogg"]
