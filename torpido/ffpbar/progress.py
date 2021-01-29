"""
This file defines the progress bar from tqdm and updates it according to the FFmpeg
logs based on the time and duration in the logs. Command that have dynamic lengths like
multiple trims and concatenation the progress cannot be predicted so the progress bar does not
accurately detects the progress.
"""

from tqdm import tqdm

from .parser import Parser


class Progress:
    def __init__(self):
        self._bar, self._percent, self._parser = tqdm(total=100), 0, Parser()

    @property
    def progress(self):
        return self._percent

    def display(self, log: str, display_log=False):  # parse the log and update the progress
        duration, time = self._parser.extract_time_duration(log)

        if time is not None:
            current_progress = self.__get_progress(duration, time)
            if current_progress > self._percent:
                self._bar.update(current_progress - self._percent)
                self._percent = current_progress

        # display log is true then it will print if errors
        elif display_log:
            print(log)

    def complete(self):  # completes the progress bar
        self._bar.update(100)
        self._percent = 100

    def __get_progress(self, duration, time): # returns the percentage of the progress
        duration_in_sec = duration.get_time_in_sec()
        if duration_in_sec == 0:
            return 100

        return int(time.get_time_in_sec() * 100 / duration_in_sec)

    def clear(self):  # sets the progress to 0
        self._bar.clear()
        self._percent = 0

    def __del__(self):
        self._bar.close()
