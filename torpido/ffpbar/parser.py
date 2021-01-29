""" This file extracts the time and duration from the FFmpeg logs on command execution """
import re


class Time:
    def __init__(self):
        self.hour, self.minute, self.second = None, None, None

    def get_time_in_sec(self):
        return (self.hour * 60 * 60) + (self.minute * 60) + self.second

    def __del__(self):
        del self.hour, self.minute, self.second


class Parser:
    def __init__(self):
        self.duration, self.time, self.time_re, self.duration_re = None, None, re.compile(r'time=(\d+):(\d+):(\d+)'), re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2})')

    def extract_time_duration(self, line):
        return self.extract_duration(line), self.extract_time(line)

    def extract_time(self, line):
        exp = self.time_re.search(line)
        if exp:
            self.time = Time()
            self.time.hour = int(exp.group(1))
            self.time.minute = int(exp.group(2))
            self.time.second = int(exp.group(3))

        return self.time

    def extract_duration(self, line):
        if self.duration is not None:
            return self.duration

        exp = self.duration_re.search(line)
        if exp:
            self.duration = Time()
            self.duration.hour = int(exp.group(1))
            self.duration.minute = int(exp.group(2))
            self.duration.second = int(exp.group(3))

        return self.duration

    def __del__(self):
        del self.duration, self.time
