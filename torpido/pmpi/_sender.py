class Sender:
    def __init__(self, channel):
        self._channel = channel

    def send(self, identifier, obj):
        self._channel.send({identifier: obj})

    def close(self):
        self._channel.close()
