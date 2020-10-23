"""
This file defines the progress base from tqdm
and updates it according to the FFmpeg  logs based on
the time and duration in the logs
"""

from tqdm import tqdm

from lib.progress.std_extractor import StdExtractor


class Progress:
    """
    Progress creation and initialization of the progress bar and extractor

    Attributes
    ----------
    __progressBar : object
        tqdm progress bar
    __totalProgress : int
        maintaining the current progress
    __extractor : object
        extractor object to read the stdout logs and parse them
    """

    def __init__(self):
        self.__progressBar = tqdm(total=100)
        self.__totalProgress = 0
        self.__extractor = StdExtractor()

    def displayProgress(self, log, displayLog=False):
        """
        Gets extracted time and duration from stdExtractor and updates the progress bar

        Parameters
        ----------
        log : str
            current log from the subprocess stdout
        displayLog : bool
            if True then all logs will be flushed in the console

        Returns
        -------

        """
        duration, time = self.__extractor.extractTimeDuration(log)

        if time is not None:
            currentProgress = self.getCurrentProgress(duration, time)
            if currentProgress > self.__totalProgress:
                self.__progressBar.update(currentProgress - self.__totalProgress)
                self.__totalProgress = currentProgress

        # display log is true then it will print if errors
        elif displayLog:
            print(log)

    @staticmethod
    def getCurrentProgress(duration, time):
        """
        Calculates the progress percentage from duration and time object of the Time class

        Parameters
        ----------
        duration : Time
            Time object of total duration of original clip
        time : Time
            Time object of current duration of decoded clip

        Returns
        -------
        float
            Time in secs
        """
        durationInSec = duration.getTimeInSec()
        if durationInSec == 0:
            return 100

        return int(time.getTimeInSec() * 100 / durationInSec)

    def complete(self):
        """
        explicitly complete the progress bar
        """
        self.__progressBar.update(100)

    def clear(self):
        """
        On occurrence of any error clear the progress bar
        """
        self.__progressBar.clear()

    def __del__(self):
        """
        clean up
        """
        self.__progressBar.close()
        del self.__progressBar
        del self.__extractor
