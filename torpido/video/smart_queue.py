class SmartQueue:
    def __init__(self, maxSize=1024):
        self.maxSize, self.Q = maxSize, list()

    def put(self, data):
        self.Q.append(data)

    def get(self, index=0):
        return self.Q.pop(index)

    def empty(self):
        return True if self.Q.__len__() == 0 else False

    def qsize(self):
        return self.Q.__len__()

    def full(self):
        return True if self.Q.__len__() == self.maxSize else False
