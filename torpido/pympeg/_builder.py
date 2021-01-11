""" Builder to build the node chain """


class Stream:
    """
    Simple list manager, adds nodes and returns the chain
    of graph call. Also keeps track of labelling the input
    nodes.

    Attributes
    ----------
    _stream : list
            chain of the nodes
    count : int
            tracks the index of the InputNode
    """

    def __init__(self):
        self._stream = list()
        self.count = 0

    def add(self, node):
        """ Add a node type to the chain """
        self._stream.append(node)
        return self

    def graph(self):
        """ Returns the chain of the nodes """
        return self._stream
