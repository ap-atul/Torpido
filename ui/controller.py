import time

from PyQt5.QtCore import pyqtSignal, QThread, QObject


class Signal(QObject):
    percentComplete = pyqtSignal(float)
    percentMem = pyqtSignal(float)
    percentCpu = pyqtSignal(float)
    message = pyqtSignal(str)


class Controller(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.signal = Signal(self)

    def startProcess(self):
        self.start()

    def run(self):
        for i in range(101):
            time.sleep(0.1)
            self.signal.percentComplete.emit(i)
            self.signal.percentCpu.emit(i)
            self.signal.percentMem.emit(i)

    def setPercentComplete(self, value: float):
        self.signal.percentComplete.emit(value)

    def setCpuComplete(self, value: float):
        self.signal.percentCpu.emit(value)

    def setMemComplete(self, value: float):
        self.signal.percentMem.emit(value)

    def setMessage(self, msg: str):
        self.signal.message.emit(msg)

    def terminate(self) -> None:
        print("Exiting from the controller")
