""" Set limit on the processes using the process ids """

from os import setpriority, PRIO_PROCESS

from torpido.config.constants import NICE
from torpido.exceptions.custom import ProcessDoesNotExists
from torpido.tools.logger import Log


class Manager:
    """
    Process with a nice value determines the priority for the process
    on the operating system. If correct enough value is set then the process
    won't lock the performance of the system and other applications

    NOTE: Only for Linux and Unix

    Priorities
    ----------
        -19 (highest) to 19 (lowest), default 0 (any process)
        Priority below 0 requires super user privileges (sudo)

    Attributes
    ----------
    _nice : int
        priority for the process range from -20 to 19
    _unnice: int
        re setting the priority, default is 0
    """

    def __init__(self):
        self._nice = NICE
        self._unnice = 0

    def register(self, pid, nice=None):
        """
        Register the process for the niceness, i.e. set the priority
        defines by the nice variable and change the priority of the process.

        May raise process look up error when such process does not exists
        or is terminated. Mostly register processes which takes longer time for
        the execution

        Parameters
        ----------
        pid : int
            process id important
        nice : int
            default None, nice (priority) for the process with pid

        Raises
        ------
        ProcessDoesNotExists : Exception
            process does not exists on the system or is terminated
        """
        if nice is not None:
            self._nice = nice

        try:
            setpriority(PRIO_PROCESS, pid, self._nice)

        except ProcessLookupError:
            Log.e(ProcessDoesNotExists(pid).cause)
            raise ProcessDoesNotExists

    def unregister(self, pid, nice=None):
        """
        Unregisters the process from the Manager, i.e. set priority for the process
        to the default value i.e. 0 (Unix).

        After unregistering the priority of the process will be default which means
        that the process will run at a full potential, useful when load on the
        system is reduced.

        Parameters
        ----------
        pid : int
            process id important
        nice : int
            default None, nice (priority) for the process with pid

        Raises
        ------
        ProcessDoesNotExists : Exception
            process does not exists on the system or is terminated

        """
        if nice is not None:
            self._unnice = nice

        try:
            setpriority(PRIO_PROCESS, pid, self._unnice)

        except ProcessLookupError:
            Log.e(ProcessDoesNotExists(pid).cause)
            raise ProcessDoesNotExists


class ManagerPool:
    """
    Keeps track of all processes and their niceness. Used to handle multiple
    requests to the processes and also to distribute the amount of priority
    over to all the processes.
    TODO: distribution

    Attributes
    ----------
    __manager : Manager
        Manager object that registers and unregisters the process
    __pool : dict
        dict to store the niceness and the processes ids
    """

    def __init__(self):
        self.__manager = Manager()
        self.__pool = dict()

    def add(self, pid, nice=None):
        """
        Adds new process to the pool and set its niceness depending on the
        argument. Also used to distribute the priority among the processes.
        To equally use the system performance a accurate amount of value
        needs to be decided.

        Parameters
        ----------
        pid : int
            process id
        nice : int
            nice value

        Raises
        ------
        ProcessDoesNotExists : Exception
            process not found
        """
        if pid not in self.__pool:
            self.__pool[pid] = nice

        self.__manager.register(pid, nice)

    def remove(self, pid, nice=None):
        """
        Removes the process from the pool and also unregisters from the
        Manager, if the process is already terminated this function will
        raise ProcessDoesNotExists exception.

        Useful in scenarios when other heavy process is finished, and the
        current process needs more resources.

        Parameters
        ----------
        pid : int
            process id
        nice : int
            nice value

        Raises
        -------
        ProcessDoesNotExists : Exception
            process not found
        """
        if pid in self.__pool:
            self.__manager.unregister(pid, nice)
            self.__pool.pop(pid)

    def get(self):
        """
        Returns the dictionary of all the processes and their niceness
        values from the pool. Is no process is yet added then empty.

        Returns
        -------
        dict
            process and their niceness values
        """
        return self.__pool

    def reset(self, nice=None):
        """
        Re assigns niceness based on the argument to all the processes
        present in the pool. Nice value is absent then all processes
        will have same nice values.

        Useful when the processes have a distributed nice value and the
        new value is to be set to all the processes at once.

        Parameters
        ----------
        nice : int
            nice value
        """
        for pid, _ in self.__pool:
            self.__manager.register(pid, nice)

    def clean(self):
        """
        Removing all processes from the pool and reassigning the default nice
        value to all the processes.

        Useful while testing or for some other purposes.
        """
        for pid, _ in self.__pool:
            self.__manager.unregister(pid)

        # re creating empty dictionary
        self.__pool = dict()
