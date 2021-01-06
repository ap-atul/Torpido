"""
This file extracts the time and duration from the FFmpeg
stdout logs on command execution
"""

import re


class Time:
    """
    Simple class to store time values extracted
    datetime can be used from python torpido

    Attributes
    ---------
    __hour : int
        hour in time series
    __minute : int
        minute in time series
    __second : int
        second in time series
    """

    def __init__(self):
        self.__hour = None
        self.__minute = None
        self.__second = None

    def get_time_in_sec(self):
        """
        Returning time in seconds

        Returns
        -------
        int
            __time in secs
        """
        return (self.__hour * 60 * 60) + (self.__minute * 60) + self.__second

    def __del__(self):
        """
        clean up
        """
        del self.__hour
        del self.__minute
        del self.__second


class StdExtractor:
    """
    Stdout logs extractor to extract the duration and time
    from the logs stdout

    Attributes
    ----------
    __duration : Time
        Time object of original clip
    __time : Time
        Time object of current output clip
    """

    def __init__(self):
        self.__duration = None
        self.__time = None

    def extract_time_duration(self, line):
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
        return self.__extract_duration(line), self.__extract_time(line)

    def __extract_time(self, line):
        """
        Searching for time clause in the FFmpeg logs

            Ex: time=00:01:13.22

        Parameters
        ----------
        line : str
            output from the subprocess logs

        Returns
        -------
        __time : Time
            Time object of output clip
        """
        exp = re.compile(r'__time=(\d+):(\d+):(\d+)')
        exp = exp.search(line)
        if exp:
            self.__time = Time()
            self.__time.__hour = int(exp.group(1))
            self.__time.__minute = int(exp.group(2))
            self.__time.__second = int(exp.group(3))

        return self.__time

    def __extract_duration(self, line):
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
        __duration : Time
            Time object of input clip
        """
        if self.__duration is not None:
            return self.__duration

        exp = re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2})')
        exp = exp.search(line)
        if exp:
            self.__duration = Time()
            self.__duration.__hour = int(exp.group(1))
            self.__duration.__minute = int(exp.group(2))
            self.__duration.__second = int(exp.group(3))

        return self.__duration

    def __del__(self):
        """
        cleaning up
        """
        del self.__duration
        del self.__time
