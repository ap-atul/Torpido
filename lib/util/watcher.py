"""
Module to watch the CPU and RAM usage as a part of showing the
current usage by the product.
Not using any modules... But running some commands on the linux
machine to retrieve the CPU and RAM usage manually

May upgrade later to use `psutil`
"""
import subprocess
import time
from threading import Thread

from lib.util.logger import Log


class Watcher:
    """
    Class the watch the current usage and display on the UI as well
    as push on the console for debugging purposes.

    Creating subprocess calls with some command line only specific
    to Linux

    Commands
    ---------
    CPU Usage

    $ grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }'

        - using grep and awk to parse the output string output of the stat command

    RAM Usage

    $ grep -m 3 ':' /proc/meminfo | awk '{print $2}'

        - reading first 3 lines to get the available, free and total memory usage

    """

    def __init__(self):
        self.__cpuCommandLine = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($5)} END {print usage }'"
        self.__memCommandLine = "grep -m 3 ':' /proc/meminfo | awk '{print $2}'"
        self.__cpuThread = None
        self.__memThread = None
        self.__stopped = False
        self.__delay = 3

    def start(self):
        """
        Starting 2 threads that run the commands using suprocess and reads the output to the UI and Logs
        """
        self.__cpuThread = Thread(target=self.__runCpu, args=())
        self.__memThread = Thread(target=self.__runMem, args=())
        self.__cpuThread.start()
        self.__memThread.start()

    def __runCpu(self):
        """
        Run the CPU check command till the process is explicitly told to stop using the Watcher.stop()
        function
        """
        while not self.__stopped:
            run = subprocess.Popen(args=self.__cpuCommandLine,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True,
                                   shell=True)

            for stdout in iter(run.stdout.readline, ""):
                stdout = stdout.replace("\n", "")
                Log.i(f"[ CPU :: {stdout}% ]")

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

            Log.i(f"[ RAM :: {round((lines[0] - lines[2]) * 100 / lines[0])}% ]")
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
