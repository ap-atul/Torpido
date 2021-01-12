class Sender:
    def __init__(self, channel):
        self._channel = channel

    def send(self, identifier, obj):
        data = dict()
        data[identifier] = obj

        self._channel.send(data)

    def close(self):
        self._channel.close()
