from tqdm import tqdm

from lib.progress.stdExtractor import StdExtractor

"""
This file defines the progress base from tqdm 
and updates it according to the FFmpeg  logs based on
the time and duration in the logs
"""


class Progress:
    def __init__(self):
        """
        initializes the progress bar and extractor
        """
        self.progressBar = tqdm(total=100)
        self.totalProgress = 0
        self.extractor = StdExtractor()

    def displayProgress(self, log, displayLog=False):
        """
        extracts time and duration to update the progress
        bar.
        :param log: string, stdout log
        :param displayLog: bool, to print the log
        :return: None
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
        current progress is calculated with duration and current
        time
        :param duration: Time object, original time
        :param time: Time object, current time
        :return: int, percent completed
        """
        durationInSec = duration.getTimeInSec()
        if durationInSec == 0:
            return 100

        return int(time.getTimeInSec() * 100 / durationInSec)

    def complete(self):
        """
        explicitly complete the bar
        :return: none
        """
        self.progressBar.update(100)

    def clear(self):
        """
        on error clear the percent on the progress bar
        :return: None
        """
        self.progressBar.clear()

    def __del__(self):
        """
        clean up
        :return: None
        """
        self.progressBar.close()
        del self.progressBar
        del self.extractor
