"""
File to load runtime config for the system.
"""

import os

from torpido import yacp

# text file storing all the configurations
CONFIG_FILE = "config.torpido"

# syntax for parsing the config file
SYNTAX = "%s=%s"


class _TorpidoSettings:
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
    AUDIO_BLOCK_PER = 0.1

    # wavelet used to de noise/  Coiflet wavelet band
    WAVELET = "coif1"

    # silence threshold
    SILENCE_THRESHOLD = 0.005

    # ********************** TEXTUAL PART ************************
    # min confidence of the text being detected
    TEXT_MIN_CONFIDENCE = 0.5

    # text detection is slow so some frames are skipped (sec)
    TEXT_SKIP_FRAMES = 10

    # delay to check the CPU and MEM usage (in secs)
    WATCHER_DELAY = 5

    # theme for torpido
    THEME = "default"


def write_config(cls):
    yacp.dump(CONFIG_FILE, cls, syntax=SYNTAX)


if not os.path.isfile(CONFIG_FILE):
    yacp.dump(CONFIG_FILE, _TorpidoSettings, syntax=SYNTAX)

# simple object which is not a class
Config = yacp.load(CONFIG_FILE, _TorpidoSettings, override=True, syntax=SYNTAX)
