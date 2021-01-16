"""
This file will read the ranking for each section, parse it and
create timestamps in seconds that can be used to clip the video
using ffmpeg.

    1. Reading the ranks and parsing them to timestamps
    2. Padding the time ranks to generate the timestamps
    3. Validating the timestamps
    4. Returning a list of list containing (start -> end) time stamps

"""
from random import randint

from torpido.config.cache import Cache
from torpido.config.constants import (CACHE_RANK_MOTION, CACHE_RANK_TEXT,
                                      CACHE_RANK_BLUR, CACHE_RANK_AUDIO,
                                      MIN_RANK_OUT_VIDEO)
from torpido.exceptions.custom import RankingOfFeatureMissing


def add_padding(rank_list: list, length):
    """
    Function to add padding to the ranks if there length is lower than that of the
    required length
    Average of the rank is added as the padding data, mostly data is below 1

    Parameters
    ----------
    rank_list : list
        feature rank list
    length : int
        required length
    """
    rank_list.extend([sum(rank_list) / len(rank_list)] * int(length - len(rank_list)))


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
    motion = cache_rank.read_data(CACHE_RANK_MOTION)
    blur = cache_rank.read_data(CACHE_RANK_BLUR)
    text = cache_rank.read_data(CACHE_RANK_TEXT)
    audio = cache_rank.read_data(CACHE_RANK_AUDIO)

    if not all([motion, blur, text, audio]):
        raise RankingOfFeatureMissing

    # max length for ranking
    # NOTE: FFmpeg does not get bothered by greater values, not lower though
    maxRank = int(max(len(motion), len(blur),
                      len(audio), len(text)))

    # padding the ranks of each feature
    add_padding(motion, maxRank)
    add_padding(blur, maxRank)
    add_padding(audio, maxRank)
    add_padding(text, maxRank)

    return [motion, blur,
            text, audio]


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
    timestamps : list-any
        timestamps parsed from the ranks
    """
    timestamps = list()
    start, end, prev_end, i = None, None, 0, 0
    min_rank_out = MIN_RANK_OUT_VIDEO

    for i in range(len(ranks)):
        if start is None and ranks[i] > min_rank_out:
            start = i

        if start is not None and end is None and ranks[i] <= min_rank_out:
            end = i - 1

        if start is not None and end is not None:
            timestamps.append([start, end])
            start, end = None, None

    if end is None and start is not None:
        timestamps.append([start, i])

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

    final_timestamp = []

    # validating if there are 2 values in list
    for clip in timestamps:
        if len(clip) % 2 == 0:
            final_timestamp.append(clip)

    return final_timestamp


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
    video_length = 0
    if len(timestamps) < 0:
        return 0

    for start, end in timestamps:
        video_length += abs(end - start)

    return video_length


def get_thumbnail_sec(timestamps: list):
    """ Returns the sec for the thumnbail to generate """
    if len(timestamps) == 0:
        raise TypeError("There are no timestamps.")

    first = timestamps[0]
    start, end = first[0], first[1]

    return randint(start, end)
