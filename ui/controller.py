from multiprocessing import Lock

from PyQt5.QtCore import pyqtSignal, QObject, QRunnable

from controller import Controller as MainController


class Signal(QObject):
    percentComplete = pyqtSignal(float)
    percentMem = pyqtSignal(float)
    percentCpu = pyqtSignal(float)
    message = pyqtSignal(str)
    logger = pyqtSignal(str)


class Controller(QRunnable):
    def __init__(self):
        super().__init__()
        self.signal = Signal()
        self.controller = MainController()
        self.controller.addLogsToUi(self)
        self.videoFile = None

    def setVideo(self, videoFile):
        self.videoFile = videoFile

    def run(self):
        lock = Lock()
        self.controller.startProcessing(lock, self.videoFile, True)

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

    def setMessageLog(self, message):
        self.signal.logger.emit(message)
