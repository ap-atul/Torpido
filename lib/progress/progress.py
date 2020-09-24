from tqdm import tqdm

from lib.progress.stdExtractor import StdExtractor

"""
This file defines the progress base from tqdm 
and updates it according to the FFmpeg  logs based on
the time and duration in the logs
"""


class Progress:
    """
    Progress creation and initialization of the progress bar and extractor

    Attributes
    ----------
    progressBar : object
        tqdm progress bar
    totalProgress : int
        maintaining the current progress
    extractor : object
        extractor object to read the stdout logs and parse them
    """

    def __init__(self):
        self.progressBar = tqdm(total=100)
        self.totalProgress = 0
        self.extractor = StdExtractor()

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
        duration, time = self.extractor.extractTimeDuration(log)

        if time is not None:
            currentProgress = self.getCurrentProgress(duration, time)
            if currentProgress > self.totalProgress:
                self.progressBar.update(currentProgress - self.totalProgress)
                self.totalProgress = currentProgress

        # display log is true then it will print if errors
        elif displayLog:
            print(log)

    @staticmethod
    def getCurrentProgress(duration, time):
        """
        Caluclates the progress percentage from duration and time object of the Time class

        Parameters
        ----------
        duration : Time
            Time object of total duration of original clip
        time : Time
            Time object of current duration of decoded clip

        Returns
        -------

        """
        durationInSec = duration.getTimeInSec()
        if durationInSec == 0:
            return 100

        return int(time.getTimeInSec() * 100 / durationInSec)

    def complete(self):
        """
        explicitly complete the progress bar
        """
        self.progressBar.update(100)

    def clear(self):
        """
        On occurrence of any error clear the progress bar
        """
        self.progressBar.clear()

    def __del__(self):
        """
        clean up
        """
        self.progressBar.close()
        del self.progressBar
        del self.extractor
