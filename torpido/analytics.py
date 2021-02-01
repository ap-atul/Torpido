"""
Plotting of the ranks and the timestamps selected to trim, both
start and stop are displayed. All ranks are displayed as subplots
(line graphs)
"""

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from .config.cache import Cache
from .config.constants import CACHE_FPS, CACHE_FRAME_COUNT
from .exceptions import RankingOfFeatureMissing
from .tools.ranking import Ranking
from .tools.logger import Log

# since, ui is using QTAgg, need to send the data to main gui thread
# or just use Tk ;)
matplotlib.use("TkAgg")
plt.rcParams["figure.figsize"] = (10, 4.5)


class Analytics:
    """
    Class to plot based on the ranks and the timestamps
    selected to trim

    Attributes
    ----------
    __motion : list
        rank list for the motion feature
    __blur : list
        rank list for the blur feature
    __text : list
        rank list for the text feature
    __audio : list
        rank list for the audio feature
    __rank_length : int
        max length of the ranks
    __ranks : list
        sum of all the ranks
    __data : lol
        list of list of all ranks
    __timestamps : lol
        list of list of two timestamps (start & end0
    """

    def __init__(self):
        self.__motion, self.__blur, self.__text, self.__audio = None, None, None, None
        self.__rank_length, self.__ranks, self.__data, self.__timestamps = None, None, None, None
        self.__output_length, self.__actual_length, self.__cache = None, None, Cache()

    def analyze(self, data):
        """
        Calculating the sum of all ranks, calling plotting
        functions on the data stored

        Parameters
        ----------
        data : lol
            list of list of all feature ranks
        """
        self.__data = data
        self.__motion, self.__blur, self.__text, self.__audio = self.__data
        self.__rank_length = len(self.__motion)

        self.__ranks = [self.__motion[i] + self.__blur[i] +
                        self.__text[i] + self.__audio[i] for i in range(self.__rank_length)]

        try:
            self.__timestamps = Ranking.get_timestamps()
        except RankingOfFeatureMissing:
            Log.e(RankingOfFeatureMissing.cause)
            return

        self.__output_length = Ranking.get_video_length()
        self.__actual_length = abs(self.__cache.read_data(CACHE_FRAME_COUNT) /
                                   self.__cache.read_data(CACHE_FPS))

        self.__plot_rank_line()
        self.__analytics()

    def __plot_rank_line(self):
        """
        Plotting the ranks of each feature in the sub plot, with
        legends and color specified
        """
        numbers = [i for i in range(self.__rank_length)]
        fig = plt.figure()

        print(len(self.__motion), len(self.__blur), len(self.__audio), len(self.__text))

        ax = fig.add_subplot(211)
        ax.plot(numbers, self.__motion, label="Motion", color='r')
        ax.plot(numbers, self.__blur, label="Blur", color='g')
        ax.plot(numbers, self.__audio, label="Audio", color='c')
        ax.plot(numbers, self.__text, label="Text", color='m')
        ax.set_title("rankings for all features")
        ax.set_ylim(-1)
        plt.legend(loc=2).set_draggable(True)

        ax = fig.add_subplot(212)
        for start, end, in self.__timestamps:
            ax.plot([start, start], [0, 10], color='red', linestyle='dashed', linewidth=1.5)
            ax.plot([end, end], [0, 10], color='green', linestyle='dashed', linewidth=1.5)

        custom_lines = [Line2D([0], [0], color='red', linestyle='dashed', linewidth=1.5),
                        Line2D([0], [0], color='green', linestyle='dashed', linewidth=1.5)]

        ax.plot([i for i in range(self.__rank_length)], self.__ranks)
        ax.set_ylim(0)
        ax.set_title("sum of all rankings")
        ax.legend(custom_lines, ['start time', 'end time'], loc=0).set_draggable(True)

        plt.tight_layout()
        plt.show()

    def __analytics(self):
        """ Basic analytics on the data """

        # timestamps is not found
        if self.__timestamps is None:
            return

        if len(self.__timestamps) == 0:
            Log.w("There are not good enough portions to cut. Try changing the configurations.")
            return

        Log.i(f"Clipping a total of {len(self.__timestamps)} sub portion(s).")
        Log.i(f"Output video length would be approx. :: {self.__output_length}s or {float(self.__output_length / 60)}m")
        Log.i(f"Percent of video trimmed :: {100 - ((self.__output_length * 100) / self.__actual_length)}%")
