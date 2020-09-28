"""
Smart queue: A simple queue to store the frames read from the
VideoCapture open cv'
This one has no blocking writes and reads which makes it more
faster and since list is used as a queue. The __time complexity
is linear O(n)
"""


class SmartQueue:
    """
    List to use as a Queue to store the frames from the video read by the thread
    waiting to be processed. Using custom queue implementation to increase the computation
    speed and to get around the locks of the default queue

    Attributes
    ----------
    Q : list
        list is used to create a queue
    maxSize : int
        size of the queue

    Examples
    --------
    Similar to Queue functions are named same way
    """
    def __init__(self, maxSize=1024):
        self.maxSize = maxSize
        self.Q = list()

    def put(self, data):
        """
        Insert data in the queue

        Parameters
        ----------
        data : object
            any object can be inserted

        """
        self.Q.append(data)

    def get(self, index=0):
        """
        Removes and returns the first inserted data

        Parameters
        ----------
        index : optional, default=0
            since the list works in LIFO manner so removing from index 0

        Returns
        -------
        object
            return item at index
        """
        return self.Q.pop(index)

    def empty(self):
        """
        If the queue is empty

        Returns
        -------
        bool
            True if empty
        """
        if self.Q.__len__() == 0:
            return True
        return False

    def qsize(self):
        """
        Check the size of the queue

        Returns
        -------
        int
            size of the queue

        """
        return self.Q.__len__()

    def full(self):
        """
        If the queue is full

        Returns
        -------
        bool
            True if full
        """
        if self.Q.__len__() == self.maxSize:
            return True
        return False
