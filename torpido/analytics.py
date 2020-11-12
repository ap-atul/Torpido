from matplotlib import pyplot as plt

from torpido.util.timestamp import readTheRankings, getTimestamps


class Analytics:
    def __init__(self):
        self.__motion, self.__blur, self.__text, self.__audio = None, None, None, None
        self.__rankLength = None
        self.__ranks = None

    def analyze(self):
        self.__motion, self.__blur, self.__text, self.__audio = readTheRankings()
        self.__rankLength = len(self.__motion)

        self.__ranks = [self.__motion[i] + self.__blur[i] +
                        self.__text[i] + self.__audio[i] for i in range(self.__rankLength)]

        self.__plotRankLine()
        self.__plotSumLine()

    def __plotRankLine(self):
        numbers = [i for i in range(self.__rankLength)]
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

    def __plotSumLine(self):
        timestamps = getTimestamps()

        for start, end, in timestamps:
            plt.plot([start, start], [0, 10], color='red', linestyle='dashed', linewidth=2, label="start time")
            plt.plot([end, end], [0, 10], color='green', linestyle='dashed', linewidth=2, label="end time")

        plt.plot([i for i in range(self.__rankLength)], self.__ranks)
        plt.legend(loc=2)
        plt.title("Final summation of all ranks")
        plt.xlabel("Video duration (sec)")
        plt.ylabel("Summation of all rankings")
        plt.show()
