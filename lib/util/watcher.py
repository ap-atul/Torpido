"""
Module to watch the CPU and RAM usage as a part of showing the
current usage by the product.
Not using any modules... But running some commands on the linux
machine to retrieve the CPU and RAM usage manually

May upgrade later to use `psutil`
"""
import gc
import re
import subprocess
import time
from threading import Thread

from lib.util.constants import WATCHER_DELAY
from lib.util.logger import Log


def getIdleTotal(stdout):
    """
    Reads the stdout logs, calculates the various cpu times and creates a dictionary
    of idle time and the total time

    Parameters
    ----------
    stdout : str
        output of the command from the std out logs

    Returns
    -------
    dict
        idle and total time of the cpu
    """
    stdout = stdout.replace('cpu  ', '').split(" ")
    cpuLine = [float(i) for i in stdout[0:]]

    user, nice, system, idle, io, irq, soft, steal, _, _ = cpuLine

    idle = idle + io
    nonIdle = user + nice + system + irq + soft + steal
    total = idle + nonIdle

    return {'total': total, 'idle': idle}


class Watcher:
    """
    Class the watch the current usage and display on the UI as well
    as push on the console for debugging purposes.

    Creating subprocess calls with some command line only specific
    to Linux

    Commands
    ---------
    CPU Usage

    $ grep 'cpu ' /proc/stat

        - using grep and awk to parse the output string output of the stat command

    RAM Usage

    $ grep -m 3 ':' /proc/meminfo | awk '{print $2}'

        - reading first 3 lines to get the available, free and total memory usage

    """

    def __init__(self):
        self.__cpuCommandLine = "grep 'cpu ' /proc/stat"
        self.__memCommandLine = "grep -m 3 ':' /proc/meminfo | awk '{print $2}'"
        self.__cpuThread = None
        self.__memThread = None
        self.__stopped = False
        self.__delay = WATCHER_DELAY
        self.__exp = re.compile(r'(\d)')
        self.__enable = True

    def enable(self, enable=True):
        """
        Utility function to enable and disable the watcher

        Parameters
        ----------
        enable : bool, default=True
            enables the watcher
        """
        self.__enable = enable

    def start(self):
        """
        Starting 2 threads that run the commands using suprocess and reads the output to the UI and Logs
        """
        if self.__enable:
            self.__cpuThread = Thread(target=self.__runCpu, args=())
            self.__memThread = Thread(target=self.__runMem, args=())
            self.__cpuThread.start()
            self.__memThread.start()

    def __runCpu(self):
        """
        Run the CPU check command till the process is explicitly told to stop using the Watcher.stop()
        function
        """
        cpuInfo = {}
        percent = 0

        while not self.__stopped:
            run = subprocess.Popen(args=self.__cpuCommandLine,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True,
                                   shell=True)

            for stdout in iter(run.stdout.readline, ""):
                if len(cpuInfo) == 0:
                    cpuInfo.update(getIdleTotal(stdout))

                else:
                    current = getIdleTotal(stdout)
                    total = current['total']
                    prevTotal = cpuInfo['total']

                    idle = current['idle']
                    prevIdle = cpuInfo['idle']

                    percent = ((total - prevTotal) - (idle - prevIdle)) / (total - prevTotal) * 100
                    cpuInfo.update(current)

                Log.i(f"[ CPU :: {round(percent)} % ]")

            run.stdout.close()
            if run.wait():
                Log.e("Can't initiate Watcher for CPU")
                self.__stopped = True

            time.sleep(self.__delay)

    def __runMem(self):
        """
        Run the RAM check command till the process is explicitly told to stop using the Watcher.stop()
        function
        """
        while not self.__stopped:
            run = subprocess.Popen(args=self.__memCommandLine,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True,
                                   shell=True)

            lines = []
            for stdout in iter(run.stdout.readline, ""):
                lines.append(int(stdout))

            Log.i(f"[ RAM :: {round((lines[0] - lines[2]) * 100 / lines[0])} % ]")
            run.stdout.close()
            if run.wait():
                Log.e("Can't initiate Watcher for RAM")
                self.__stopped = True

            time.sleep(self.__delay)

    def end(self):
        """
        End both the processes
        """
        self.__stopped = True
        Log.d("Stopping the watcher................")

    def __del__(self):
        """
        clean up
        """
        if self.__memThread is not None:
            del self.__memThread
        if self.__cpuThread is not None:
            del self.__cpuThread

        Log.d(f"Garbage Collected :: {gc.collect()}")
