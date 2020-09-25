"""
This file extracts the time and duration from the FFmpeg
stdout logs on command execution
"""

import re


class Time:
    """
    Simple class to store time values extracted
    datetime can be used from python lib

    Attributes
    ---------
    hour : int
        hour in time series
    minute : int
        minute in time series
    second : int
        second in time series
    """

    def __init__(self):
        self.hour = None
        self.minute = None
        self.second = None

    def getTimeInSec(self):
        """
        Returning time in seconds

        Returns
        -------
        int
            time in secs
        """
        return (self.hour * 60 * 60) + (self.minute * 60) + self.second

    def __del__(self):
        """
        clean up
        """
        del self.hour
        del self.minute
        del self.second


class StdExtractor:
    """
    Stdout logs extractor to extract the duration and time
    from the logs stdout

    Attributes
    ----------
    duration : Time
        Time object of original clip
    time : Time
        Time object of current output clip
    """

    def __init__(self):
        self.duration = None
        self.time = None

    def extractTimeDuration(self, line):
        """
        Extracts time and duration from the stdout log from the sub process

        Parameters
        ----------
        line : str
            output from the subprocess logs

        Returns
        -------
        tuple
            Time object of duration and time
        """
        return self.extractDuration(line), self.extractTime(line)

    def extractTime(self, line):
        """
        Searching for time clause in the FFmpeg logs

            Ex: time=00:01:13.22

        Parameters
        ----------
        line : str
            output from the subprocess logs

        Returns
        -------
        time : Time
            Time object of output clip
        """
        exp = re.compile(r'time=(\d+):(\d+):(\d+)')
        exp = exp.search(line)
        if exp:
            self.time = Time()
            self.time.hour = int(exp.group(1))
            self.time.minute = int(exp.group(2))
            self.time.second = int(exp.group(3))

        return self.time

    def extractDuration(self, line):
        """
        Searching for duration clause in FFmpeg logs
        since duration is displayed only once it is set
        only once and later returned the same value

        Parameters
        ----------
        line : str
            output from the subprocess logs

        Returns
        -------
        duration : Time
            Time object of input clip
        """
        if self.duration is not None:
            return self.duration

        exp = re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2})')
        exp = exp.search(line)
        if exp:
            self.duration = Time()
            self.duration.hour = int(exp.group(1))
            self.duration.minute = int(exp.group(2))
            self.duration.second = int(exp.group(3))

        return self.duration

    def __del__(self):
        """
        cleaning up
        """
        del self.duration
        del self.time
