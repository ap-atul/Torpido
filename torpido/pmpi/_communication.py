from multiprocessing import Pipe
from threading import Thread

from ._sender import Sender


class Communication:
    def __init__(self):
        self._index = dict()
        self._receiver, self._channel = Pipe()
        self._sender = Sender(channel=self._channel)
        self._worker, self._stopped = None, False

    def sender(self):
        self._start_communication()
        return self._sender

    def register(self, identifier, func):
        if identifier not in self._index:
            self._index[identifier] = func

        else:
            raise Exception("The function or the identifier already exists.")

    def unregister(self, identifier):
        if identifier in self._index:
            self._index.pop(identifier)

        else:
            raise Exception("No such function or identifier exists.")

    def end(self):
        self._stopped = True

        self._sender.close()
        self._receiver.close()

    def _start_communication(self):
        self._start()

    def _start(self):
        self._worker = Thread(target=self._receive, args=())
        self._worker.start()

    def _receive(self):
        while not self._stopped:
            # this should be a single key dictionary
            if self._receiver.closed:
                break

            data_to_receive = None
            try:
                data_to_receive = self._receiver.recv()
            except EOFError and OSError as _:
                pass

            if not data_to_receive or not isinstance(data_to_receive, dict):
                print(f"[PMPI WARN] Unknown data of type :: {type(data_to_receive)} received from the sender. "
                      f"Requires data of the type dict.")
                continue

            key = list(data_to_receive.keys())[0]
            val = data_to_receive[key]

            if key in self._index:
                self._make_call(key, val)
            else:
                print(f"[PMPI WARN] Unknown data received from the receiver. Got :: {key} -> {val}")

    def _make_call(self, key, val):
        fun_for_call = self._index[key]
        data_arg = val

        fun_for_call(data_arg)

    def __del__(self):
        self._stopped = True
