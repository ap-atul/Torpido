"""
This file will read the ranking for each section, parse it and
create timestamps in seconds that can be used to clip the video
using ffmpeg.

    1. Reading the ranks and parsing them to timestamps
    2. Padding the time ranks to generate the timestamps
    3. Validating the timestamps
    4. Returning a list of list containing (start -> end) time stamps

"""

from torpido.config.cache import Cache
from torpido.config.constants import (CACHE_RANK_MOTION, CACHE_RANK_TEXT,
                                      CACHE_RANK_BLUR, CACHE_RANK_AUDIO,
                                      MIN_RANK_OUT_VIDEO)
from torpido.exceptions.custom import RankingOfFeatureMissing


def add_padding(rankList: list, length):
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
    rankList.extend([sum(rankList) / len(rankList)] * int(length - len(rankList)))


def read_rankings():
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
    cache_rank = Cache()

    # loading the read files
    motionRank = cache_rank.read_data(CACHE_RANK_MOTION)
    blurRank = cache_rank.read_data(CACHE_RANK_BLUR)
    textRank = cache_rank.read_data(CACHE_RANK_TEXT)
    audioRank = cache_rank.read_data(CACHE_RANK_AUDIO)

    if not all([motionRank, blurRank, textRank, audioRank]):
        raise RankingOfFeatureMissing

    # max length for ranking
    # NOTE: FFmpeg does not get bothered by greater values, not lower though
    maxRank = int(max(len(motionRank), len(blurRank),
                      len(audioRank), len(textRank)))

    # padding the ranks of each feature
    add_padding(motionRank, maxRank)
    add_padding(blurRank, maxRank)
    add_padding(audioRank, maxRank)
    add_padding(textRank, maxRank)

    return [motionRank, blurRank,
            textRank, audioRank]


def trim_by_rank(ranks):
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


def get_timestamps(data):
    """
    Returns parsed timestamps from the ranking of all 4 processing

    Attributes
    -----------
    data: lol
        list of list of ranks

    Returns
    -------
    list of list
        timestamps list containing start and emd timestamps

    """
    motion, blur, text, audio = data
    ranks = [motion[i] + blur[i] + text[i] + audio[i] for i in range(len(motion))]

    if ranks is not None:
        timestamps = trim_by_rank(ranks)
    else:
        raise RankingOfFeatureMissing

    finalTimestamp = []

    # validating if there are 2 values in list
    for clip in timestamps:
        if len(clip) % 2 == 0:
            finalTimestamp.append(clip)

    return finalTimestamp


def get_output_video_length(timestamps: list):
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
