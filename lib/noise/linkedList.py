"""
A python linked list implementation
relying on http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/
"""


class Node:

    def __init__(self, data, prev=None, next=None):
        """
        Node the most unit part of the Tree (parsed data)

        Attributes
        ----------
        data : object
            audio signal data points
        prev : object, default=None
            pointer to previous data point
        next : object, default=None
            pointer to next data point
        """
        self.data = data
        self.prev = prev
        self.next = next

    def getNextWithValidData(self):
        """
        Next data point in the parsed tree

        Returns
        -------
        object
            data point if exists else None
        """
        current = self.next
        while current is not None:
            if current.data is not None:
                return current
            current = current.next

        return None

    def getPrevWithValidData(self):
        """
        Previous data point in the parsed tree

        Returns
        -------
        object
            data point if exists else None
        """
        current = self.prev
        while current is not None:
            if current.data is not None:
                return current
            current = current.prev

        return None


class LinkedList:

    def __init__(self):
        """
        Linked list custom implementation to avoid lock and priorities

        Attributes
        ----------
        first : object, default=None
            initial object
        last : object, default=None
            tail object
        _list : list
            all nodes
        """
        self.first = None  # head
        self.last = None  # tail
        self.__list = None

    def append(self, data):
        """
        add data to the node

        Parameters
        ----------
        data : object
            input data
        """
        new_node = Node(data, None, None)
        if self.first is None:
            self.first = self.last = new_node
            self.__list = list()
        else:
            new_node.prev = self.last
            new_node.next = None
            self.last.next = new_node
            self.last = new_node

        self.__list.append(new_node)

    def getAsList(self):
        """
        Returns the complete data as a list

        Returns
        -------
        list
            parsed data points
        """
        ret = list()
        current = self.first
        while current is not None:
            ret.append(current)
            current = current.next

        return ret
