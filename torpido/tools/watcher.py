"""
Module to watch the CPU and RAM usage as a part of showing the
current usage by the product.
Not using any modules... But running some commands on the linux
machine to retrieve the CPU and RAM usage manually

May upgrade later to use `psutil`
"""

import os
from threading import Thread
from time import sleep

from torpido.config.constants import WATCHER_DELAY
from torpido.exceptions.custom import WatcherFileMissing
from torpido.tools.logger import Log


def times(values):
    """
    Reads the stdout logs, calculates the various cpu times and creates a dictionary
    of idle time and the total time

    Parameters
    ----------
    values : list
        output of the command from the std out logs

    Returns
    -------
    tuple
        idle and total time of the cpu
    """
    user, nice, system, idle, io, irq, soft, steal, _, _ = values

    idle = idle + io
    nonIdle = user + nice + system + irq + soft + steal
    total = idle + nonIdle

    return total, idle


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

    Attributes
    ----------
    Watcher.CPU : str
        name of the file for the cpu stats
    Watcher.MEM : str
        name of the file for the mem stats
    Watcher.CLOCK : int
        clocks of the system
    __cpu : thread
        thread for reading the cpu stats
    __mem : thread
        thread for reading the mem stats
    __delay : float
        ms to sleep the thread, stopping the thread from consuming resources
    _app : controller
        object of the controller to redirect the percent value to the UI
    __enable : bool
        to enable the Watcher for the stat reading
    __stop : bool
        to end the threads and reading of the stats
    """

    # cpu stats file in Linux, default location
    CPU = "/proc/stat"

    # memory stats file in Linux, default location
    MEM = "/proc/meminfo"

    # clock ticks
    CLOCK = os.sysconf("SC_CLK_TCK")

    def __init__(self):
        self.__cpu = None
        self.__mem = None

        # delay for the thread
        self.__delay = WATCHER_DELAY

        # ui controller
        self._app = None
        self.__enable = False
        self.__stop = False

    def _start_cpu(self):
		"""
		Starting the monitoring of the cpu usage. The cpu usage is not connected to the
		current process but the entire system so the percent may vary. Hance, we are reading
		the "proc" files of the system
		"""

		total, idle = None, None

		try:
			stat = self.__read_cpu()
			total, idle = times(stat)
        except WatcherFileMissing:
            self.__stop = True
            Log.e(WatcherFileMissing.cause)

        while not self.__stop:

            try:
				nstat = self.__read_cpu()
				ntotal, nidle = times(nstat)

                percent = ((ntotal - total) - (nidle - idle)) / (ntotal - total) * 100

            # cases when initial values are zero
            except ZeroDivisionError:
                percent = 0

            # if anything happened, chances are very low
            except WatcherFileMissing:
                Log.e(WatcherFileMissing.cause)
                percent = 0

            # sanity checks
            if percent < 0:
                percent = 0
            elif percent > 100:
                percent = 100

            Log.i(f"[CPU] :: {percent}")

            # send to the UI
            if self._app is not None:
				self._app.set_cpu_complete(percent)

            # sleeping the thread
            sleep(self.__delay)

	def _start_mem(self):
		"""
		Starting the monitoring of the ram usage. This determines the ram used
		by the entire system not only the current process. The ram usage may vary
		by small units depends on the Watcher.__delay or the Config.delay
		"""

		while not self.__stop:
			try:
				stat = self.__read_mem()
				percent = ((stat[0] - stat[2]) * 100) / stat[0]

            except ZeroDivisionError or WatcherFileMissing:
                percent = 0
                Log.e(WatcherFileMissing.cause)

            Log.i(f"[RAM] :: {percent}")

            # send to the UI
            if self._app is not None:
				self._app.set_mem_complete(percent)

            # sleeping the thread
            sleep(self.__delay)

	def __read_cpu(self):
		""" Reads the file and returns the list of the values of the times of the cpu """
		try:
			with open(Watcher.CPU) as f:
				values = f.readline().split()[1:]
			values = [float(value) / Watcher.CLOCK for value in values]

			return values

		except FileNotFoundError:
			self.__stop = False
            raise WatcherFileMissing

	def __read_mem(self):
		""" Reads the files and returns 3 values representing the available, total and free memory"""
		values = list()

		try:
			with open(Watcher.MEM) as f:
				lines = f.readlines()[0: 3]
				for line in lines:
					values.append(int(line.split()[1]))

			return values

        except FileNotFoundError:
            self.__stop = False
            raise WatcherFileMissing

    def enable(self, app, enable=True):
        """ Enables the watcher and the controller object is connected to receives the readings """
        self._app = app
        self.__enable = enable

    def start(self):
        """
        Starts the watcher, which starts 2 threads for the monitoring, if the cpu
        usage is going high then try changing the delay value
        """
		if self.__enable:
			self.__cpu = Thread(target=self._start_cpu, args=())
			self.__mem = Thread(target=self._start_mem, args=())

			self.__cpu.start()
			self.__mem.start()

    def stop(self):
        """ End the monitoring """
        self.__stop = True

    def __del__(self):
        """ Clean up """
        if self.__mem is not None:
            del self.__mem
        if self.__cpu is not None:
            del self.__cpu
