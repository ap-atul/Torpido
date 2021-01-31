import os

from joblib import load, dump

from .. import Log
from ..exceptions.custom import RankingOfFeatureMissing
from ..config.cache import Cache
from ..config.config import Config
from ..config.constants import CACHE_FRAME_COUNT, CACHE_FPS, CACHE_DIR, CACHE_NAME


class _RankCache:
    RANK_KEY = "rank"  # key val for the rank cache dict

    def __init__(self):
        if not os.path.isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        self._filename = os.path.join(CACHE_DIR, CACHE_NAME)

    def write(self, key, val):
        if os.path.isfile(self._filename):
            data = load(self._filename)
        else:
            data = dict()

        if _RankCache.RANK_KEY not in data:
            rank = dict()
            rank[key] = val
            data[_RankCache.RANK_KEY] = rank
        else:
            data[_RankCache.RANK_KEY][key] = val

        dump(data, self._filename)
        Log.d(f"[RANK CACHE] {key} stored")

    def read(self, key):
        if os.path.isfile(self._filename):
            data = load(self._filename)
            if _RankCache.RANK_KEY in data:
                if key in data[_RankCache.RANK_KEY]:
                    return data[_RankCache.RANK_KEY][key]
                return None
        return None

    def all_ranks(self):
        if os.path.isfile(self._filename):
            data = load(self._filename)
            return list(data[_RankCache.RANK_KEY].values())


class Ranking:

    # _ranks = dict()

    @staticmethod
    def _add_padding(val):
        _max_length = int(Cache().read_data(CACHE_FRAME_COUNT) / Cache().read_data(CACHE_FPS))
        if len(val) < _max_length:
            val.extend([sum(val) / len(val)] * int(_max_length - len(val)))
            return val
        return val[0: _max_length]

    @staticmethod
    def _trim_by_rank(ranks):
        timestamps = list()
        _min_rank = Config.MIN_RANK_OUT_VIDEO
        start, end, prev_end, i = None, None, 0, 0

        for i in range(len(ranks)):
            if start is None and ranks[i] > _min_rank:
                start = i

            if start is not None and end is None and ranks[i] <= _min_rank:
                end = i - 1

            if start is not None and end is not None:
                timestamps.append([start, end])
                start, end = None, None

        if end is None and start is not None:
            timestamps.append([start, i + 1])

        return timestamps

    @staticmethod
    def add(key, rank: list):
        rank = Ranking._add_padding(rank)
        _RankCache().write(key, rank)

    @staticmethod
    def get(key):
        return _RankCache().read(key)

    @staticmethod
    def ranks():
        return _RankCache().all_ranks()

    @staticmethod
    def get_timestamps():
        sum_ranks = [sum(rank_list) for rank_list in zip(* _RankCache().all_ranks())]

        if sum_ranks is None:
            raise RankingOfFeatureMissing

        timestamps = Ranking._trim_by_rank(sum_ranks)
        final = list()

        for clip in timestamps:
            if len(clip) % 2 == 0:
                final.append(clip)

        return final

    @staticmethod
    def get_video_length():
        timestamps = Ranking.get_timestamps()
        video_length = 0

        if len(timestamps) < 0:
            return 0

        for start, end in timestamps:
            video_length += abs(end - start)

        return video_length

    @staticmethod
    def get_thumbnail_sec():
        from random import randint

        timestamps = Ranking.get_timestamps()
        if len(timestamps) == 0:
            raise TypeError("There are no timestamps.")

        first = timestamps[0]
        start, end = first[0], first[1]

        return randint(start, end)
