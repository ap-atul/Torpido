"""
This file extracts the time and duration from the FFmpeg
stdout logs on command execution
"""

import re


class Time:
    def __init__(self):
        """
        Simple class to store time values extracted
        datetime can be used from python lib
        """
        self.hour = None
        self.minute = None
        self.second = None

    def get_time_in_sec(self):
        """ Returns the time in seconds """
        return (self.hour * 60 * 60) + (self.minute * 60) + self.second

    def __del__(self):
        del self.hour
        del self.minute
        del self.second


class Parser:
    def __init__(self):
        """
        Stdout logs parser to extract the duration and time
        from the logs stdout
        """
        self.duration = None
        self.time = None

    def extract_time_duration(self, line):
        """ Extracts the time and duration from the log """
        return self.extract_duration(line), self.extract_time(line)

    def extract_time(self, line):
        """ Extracts the time from the log """
        exp = re.compile(r'time=(\d+):(\d+):(\d+)')
        exp = exp.search(line)
        if exp:
            self.time = Time()
            self.time.hour = int(exp.group(1))
            self.time.minute = int(exp.group(2))
            self.time.second = int(exp.group(3))

        return self.time

    def extract_duration(self, line):
        """ Extracts the duration from the log """
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
        del self.duration
        del self.time
