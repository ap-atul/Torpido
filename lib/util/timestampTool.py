"""
This file will read the ranking for each section, parse it and
create timestamps in seconds that can be used to clip the video
using ffmpeg.

    1. Reading the ranks and parsing them to timestamps
    2. Padding the __time ranks to generate the timestamps
    3. Validating the timestamps

"""

import os

from joblib import load

from lib.util.constants import *
from lib.util.logger import Log


def readTheRankings():
    """
    Reads the ranking using the joblib files and calculate
    the final sum ranks
    TODO: padding if required

    Returns
    -------
    list
        list of the sum of all ranks
    """
    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_MOTION)) is False:
        Log.e("Motion Ranking does not exists")
        return

    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_BLUR)) is False:
        Log.e("Blur Ranking does not exists")
        return

    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_TEXT)) is False:
        Log.e("Text Ranking does not exists")
        return

    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_AUDIO)) is False:
        Log.e("Audio Ranking does not exists")
        return

    motionFile = os.path.join(RANK_DIR, RANK_OUT_MOTION)
    blurFile = os.path.join(RANK_DIR, RANK_OUT_BLUR)
    textFile = os.path.join(RANK_DIR, RANK_OUT_TEXT)
    audioFile = os.path.join(RANK_DIR, RANK_OUT_AUDIO)
    motionRank = load(motionFile)
    blurRank = load(blurFile)
    textRank = load(textFile)
    audioRank = load(audioFile)

    minRank = min(len(motionRank), len(blurRank),
                  len(audioRank), len(textRank))

    return [motionRank[i] + blurRank[i] +
            textRank[i] + audioRank[i]
            for i in range(minRank)]


def trimByRank(ranks):
    """
    Parse the ranks to generate timestamps. Ranks are per sec so the start rank will be start
    timestamp for trimming

    Parameters
    ----------
    ranks : iterable
        ranks of the video

    Returns
    --------
    timestamps : list
        timestamps parsed from the ranks
    """
    timestamps = []
    start = None
    end = None
    prev_end = 0
    for i in range(0, len(ranks)):
        if ranks[i] > MIN_RANK_OUT_VIDEO:
            if start is None:
                start = i
            prev_end += 1

        else:
            if end is None and start is not None:
                end = start + prev_end - 1
                if start == end:
                    end = None

        if start is not None and end is not None:
            start = start
            end = end
            timestamps.append([start, end])
            end = None
            start = None
            prev_end = 0
    if start is not None and end is None:
        end = len(ranks)
        timestamps.append([start, end])

    return timestamps


def getTimestamps():
    """
    Returns parsed timestamps from the ranking of all 4 processing

    Returns
    -------
    list of list
        timestamps list containing start and emd timestamps

    """
    timestamps = trimByRank(readTheRankings())

    finalTimestamp = []
    for clip in timestamps:
        if len(clip) % 2 == 0:
            finalTimestamp.append(clip)

    return finalTimestamp
