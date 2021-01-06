"""
Plotting of the ranks and the timestamps selected to trim, both
start and stop are displayed. All ranks are displayed as subplots
(line graphs)
"""

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from torpido.config.cache import Cache
from torpido.config.constants import CACHE_FPS, CACHE_FRAME_COUNT
from torpido.exceptions import RankingOfFeatureMissing
from torpido.tools.logger import Log
from torpido.util.timestamp import get_timestamps, get_output_video_length

# since, ui is using QTAgg, need to send the data to main gui thread
# or just use Tk ;)
matplotlib.use("TkAgg")


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
        self.__rank_length = None
        self.__ranks = None
        self.__data = None
        self.__timestamps = None
        self.__output_length = None
        self.__actual_length = None
        self.__cache = Cache()

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
            self.__timestamps = get_timestamps(data=data)
        except RankingOfFeatureMissing:
            Log.e(RankingOfFeatureMissing.cause)
            return

        self.__output_length = get_output_video_length(self.__timestamps)
        self.__actual_length = abs(self.__cache.read_data(CACHE_FRAME_COUNT) /
                                   self.__cache.read_data(CACHE_FPS))

        self.__plot_rank_line()
        self.__plot_sum_line()
        self.__analytics()

    def __plot_rank_line(self):
        """
        Plotting the ranks of each feature in the sub plot, with
        legends and color specified
        """
        numbers = [i for i in range(self.__rank_length)]
        fig = plt.figure()

        ax = fig.add_subplot(411)
        ax.plot(numbers, self.__motion, label="Motion", color='r')
        plt.legend(loc=2)

        ax = fig.add_subplot(412)
        ax.plot(numbers, self.__blur, label="Blur", color='g')
        plt.legend(loc=2)

        ax = fig.add_subplot(413)
        ax.plot(numbers, self.__audio, label="Audio", color='c')
        plt.legend(loc=2)

        ax = fig.add_subplot(414)
        ax.plot(numbers, self.__text, label="Text", color='m')
        plt.legend(loc=2)

        plt.tight_layout()
        plt.show()

    def __plot_sum_line(self):
        """
        Plotting the sub rank line graph, also adding the start and end timestamps
        dashed lines. The green
        """
        for start, end, in self.__timestamps:
            plt.plot([start, start], [0, 10], color='red', linestyle='dashed', linewidth=2)
            plt.plot([end, end], [0, 10], color='green', linestyle='dashed', linewidth=2)

        custom_lines = [Line2D([0], [0], color='red', lw=4),
                        Line2D([0], [0], color='green', lw=4)]

        plt.plot([i for i in range(self.__rank_length)], self.__ranks)
        plt.legend(custom_lines, ['Start time', 'End time'], loc=0)
        plt.title("Final summation of all ranks")
        plt.xlabel("Video duration (sec)")
        plt.ylabel("Summation of all rankings")
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
        Log.i(f"Output video length would be approx. :: {self.__output_length} s or {float(self.__output_length / 60)} m")
        Log.i(f"Percent of video trimmed :: {100 - ((self.__output_length * 100) / self.__actual_length)} %")
