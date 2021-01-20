from torpido.exceptions.custom import RankingOfFeatureMissing
from torpido.config.cache import Cache
from torpido.config.config import Config
from torpido.config.constants import CACHE_FRAME_COUNT, CACHE_FPS


class Ranking:

    _ranks = dict()

    @staticmethod
    def _add_padding(val):
        _max_length = int(Cache().read_data(CACHE_FRAME_COUNT) / Cache().read_data(CACHE_FPS))
        _min_rank = Config.MIN_RANK_OUT_VIDEO
        if len(val) < _max_length:
            val.extend([sum(val) / len(val)] * int(_max_length - len(val)))
            return val
        return val[0: _max_length]

    @staticmethod
    def _trim_by_rank(ranks):
        _max_length = int(Cache().read_data(CACHE_FRAME_COUNT) / Cache().read_data(CACHE_FPS))
        _min_rank = Config.MIN_RANK_OUT_VIDEO

        timestamps = list()
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
        _max_length = int(Cache().read_data(CACHE_FRAME_COUNT) / Cache().read_data(CACHE_FPS))
        _min_rank = Config.MIN_RANK_OUT_VIDEO

        rank = Ranking._add_padding(rank)
        Ranking._ranks[key] = rank

    @staticmethod
    def get(key):
        return None if key not in Ranking._ranks else Ranking._ranks[key]

    @staticmethod
    def ranks():
        return Ranking._ranks

    @staticmethod
    def get_timestamps():
        sum_ranks = [sum(rank_list) for rank_list in zip(* Ranking._ranks.values())]

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
