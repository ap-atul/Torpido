"""
This file defines the progress bar from tqdm
and updates it according to the FFmpeg  logs based on
the time and duration in the logs
"""

from tqdm import tqdm

from .parser import Parser


class Progress:
    def __init__(self):
        """ Initializes the percent bar object """
        self._bar = tqdm(total=100)
        self._parser = Parser()
        self._percent = 0

    @property
    def progress(self):
        return self._percent

    def display(self, log: str, display_log=False):
        """ Extracts the time and duration from log and update the percent bar"""
        duration, time = self._parser.extract_time_duration(log)

        if time is not None:
            current_progress = self.__get_progress(duration, time)
            if current_progress > self._percent:
                self._bar.update(current_progress - self._percent)
                self._percent = current_progress

        # display log is true then it will print if errors
        elif display_log:
            print(log)

    def complete(self):
        """ Completes the progress bar """
        self._bar.update(100)
        self._percent = 100

    def __get_progress(self, duration, time):
        """ Returns the percent as percentage from duration and time """
        duration_in_sec = duration.get_time_in_sec()
        if duration_in_sec == 0:
            return 100

        return int(time.get_time_in_sec() * 100 / duration_in_sec)

    def clear(self):
        """ Clears the percent bar """
        self._bar.clear()
        self._percent = 0

    def __del__(self):
        self._bar.close()
