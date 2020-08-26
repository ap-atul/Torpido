# file to save all the constants that are to be used

# ******************* VIDEO PART *************************
# video width to keep while processing
VIDEO_WIDTH = 500

# threshold for video reading motion
MOTION_THRESHOLD = 50

# threshold for blur detection
BLUR_THRESHOLD = 200

# ranking dir
RANK_DIR = "model/"

# output folder to save the rankings dumps
RANK_OUT_MOTION = 'motion_ranking.joblib'
RANK_OUT_BLUR = "blur_ranking.joblib"


# ******************* AUDIO PART *************************
# reading 10% of audio file at a time
AUDIO_BLOCK = 0.02

# window level in the wavelet level
WAVELET_LEVEL = 1

# wavelet used to de noise/  Daubechies wavelet band
WAVELET = "db4"

# decomposition and re composition mode
DEC_REC_MODE = "per"

# wave threshold method
WAVE_THRESH = "soft"

# ******************* ANALYTICS PART *************************
MODEL_DIR = "model/"

# model name
MODEL_NAME = "views_predict_model.joblib"
