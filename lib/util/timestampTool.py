import os

from joblib import load

from lib.util.constants import *

"""
This file will read the ranking for each section, parse it and
create timestamps in seconds that can be used to clip the video
using ffmpeg.
1. Reading the ranks and parsing them to timestamps
2. Padding the time ranks to generate the timestamps
3. Validating the timestamps
"""


def readTheRankings():
    """
    read the ranking using the joblib files and calculate
    the final sum ranks
    TODO: padding if required

    :return: list, sum of all ranks
    """
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
    convert the ranks of each sec to timestamp in the video
    formula : sec / fps = duration (sec)
    :param ranks: input ranks for all the secs in the video
    :return:
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
    sumRank = readTheRankings()
    timestamps = trimByRank(sumRank)

    finalTimestamp = []
    for clip in timestamps:
        if len(clip) % 2 == 0:
            finalTimestamp.append(clip)

    return finalTimestamp
