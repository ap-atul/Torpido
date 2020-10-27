"""
This file will read the ranking for each section, parse it and
create timestamps in seconds that can be used to clip the video
using ffmpeg.

    1. Reading the ranks and parsing them to timestamps
    2. Padding the time ranks to generate the timestamps
    3. Validating the timestamps
    4. Returning a list of list containing (start -> end) time stamps

"""

import numpy as np

from torpido.config import *
from torpido.exceptions import RankingOfFeatureMissing


def addPadding(rankList: list, length):
    """
    Function to add padding to the ranks if there length is lower than that of the
    required length
    Average of the rank is added as the padding data, mostly data is below 1

    Parameters
    ----------
    rankList : list
        feature rank list
    length : int
        required length
    """
    rankList.extend([np.average(rankList)] * int(length - len(rankList)))


def readTheRankings():
    """
    Reads the ranking using the joblib files and calculate
    the final sum ranks

    Getting the ranking length for the ranks for the features from max
    of all the ranks length

    Padding the ranks, so that every feature has equal range

    Returns
    -------
    list
        list of the sum of all ranks
    """
    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_MOTION)) is False:
        Log.e("Motion Ranking does not exists")
        return None

    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_BLUR)) is False:
        Log.e("Blur Ranking does not exists")
        return None

    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_TEXT)) is False:
        Log.e("Text Ranking does not exists")
        return None

    if os.path.isfile(os.path.join(RANK_DIR, RANK_OUT_AUDIO)) is False:
        Log.e("Audio Ranking does not exists")
        return None

    # reading the saved ranking from the joblib files
    motionFile = os.path.join(RANK_DIR, RANK_OUT_MOTION)
    blurFile = os.path.join(RANK_DIR, RANK_OUT_BLUR)
    textFile = os.path.join(RANK_DIR, RANK_OUT_TEXT)
    audioFile = os.path.join(RANK_DIR, RANK_OUT_AUDIO)

    # loading the read files
    motionRank = load(motionFile)
    blurRank = load(blurFile)
    textRank = load(textFile)
    audioRank = load(audioFile)

    # max length for ranking
    # NOTE: FFmpeg does not get bothered by greater values, not lower though
    maxRank = int(max(len(motionRank), len(blurRank),
                      len(audioRank), len(textRank)))

    # padding the ranks of each feature
    addPadding(motionRank, maxRank)
    addPadding(blurRank, maxRank)
    addPadding(audioRank, maxRank)
    addPadding(textRank, maxRank)

    return [motionRank[i] + blurRank[i] +
            textRank[i] + audioRank[i]
            for i in range(maxRank)]


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
    ranks = readTheRankings()
    if ranks is not None:
        timestamps = trimByRank(ranks)
    else:
        raise RankingOfFeatureMissing

    finalTimestamp = []

    # validating if there are 2 values in list
    for clip in timestamps:
        if len(clip) % 2 == 0:
            finalTimestamp.append(clip)

    return finalTimestamp


def getOutputVideoLength(timestamps: list):
    """
    Calculates the output video length from the timestamps, each portion
    length would be end - start

    Parameters
    ----------
    timestamps : list
        timestamps for the video to edit

    Returns
    -------
    int
        final video length

    References
    ----------

    timestamps has list of start and end like :

        [[start, end], [start, end]]

    to get a length of each portion
        end - start

    to get final length
        finalLength += end[i] - start[i] ; i: 0 -> len(timestamps)
    """
    videoLength = 0
    if len(timestamps) < 0:
        return 0

    for start, end in timestamps:
        videoLength += abs(end - start)

    return videoLength
