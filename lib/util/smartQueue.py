"""
Smart queue: A simple queue to store the frames read from the
VideoCapture open cv'
This one has no blocking writes and reads which makes it more
faster and since list is used as a queue. The time complexity
is linear O(n)
"""


class SmartQueue:
    def __init__(self):
        """
        initializing the list for bigger video may
        need to create a max size default
        """
        self.Q = list()

    def put(self, data):
        """
        insert data to the queue/ list
        :param data: any object
        :return: none
        """
        self.Q.append(data)

    def get(self, index=0):
        """
        return the index 0 data from
        queue, if remove was used the queue
        becomes reversed
        :param index:
        :return:
        """
        return self.Q.pop(index)

    def empty(self):
        """
        empty check
        :return: bool
        """
        if self.Q.__len__() == 0:
            return True
        return False

    def qsize(self):
        """
        :return: lengths of the size of queue
        """
        return self.Q.__len__()

    def full(self):
        """
        currently no size is defined, so the queue
        is always not full
        :return: bool
        """
        return False
