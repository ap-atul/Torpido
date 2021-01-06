"""
This file defines the progress base from tqdm
and updates it according to the FFmpeg  logs based on
the time and duration in the logs
"""

from tqdm import tqdm

from torpido.progress.std_extractor import StdExtractor


class Progress:
    """
    Progress creation and initialization of the progress bar and extractor

    Attributes
    ----------
    __progress_bar : object
        tqdm progress bar
    __total_progress : int
        maintaining the current progress
    __extractor : object
        extractor object to read the stdout logs and parse them
    """

    def __init__(self):
        self.__progress_bar = tqdm(total=100)
        self.__total_progress = 0
        self.__extractor = StdExtractor()

    def display(self, log, displayLog=False):
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
        duration, time = self.__extractor.extract_time_duration(log)

        if time is not None:
            currentProgress = self.get_current_progress(duration, time)
            if currentProgress > self.__total_progress:
                self.__progress_bar.update(currentProgress - self.__total_progress)
                self.__total_progress = currentProgress

        # display log is true then it will print if errors
        elif displayLog:
            print(log)

    @staticmethod
    def get_current_progress(duration, time):
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
        durationInSec = duration.get_time_in_sec()
        if durationInSec == 0:
            return 100

        return int(time.get_time_in_sec() * 100 / durationInSec)

    def complete(self):
        """
        explicitly complete the progress bar
        """
        self.__progress_bar.update(100)

    def clear(self):
        """
        On occurrence of any error clear the progress bar
        """
        self.__progress_bar.clear()

    def __del__(self):
        """
        clean up
        """
        self.__progress_bar.close()
        del self.__progress_bar
        del self.__extractor
