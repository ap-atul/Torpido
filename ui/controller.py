from PyQt5.QtCore import pyqtSignal, QThread

from controller import Controller as MainController


class Controller(QThread):
    percentComplete = pyqtSignal(float)
    percentMem = pyqtSignal(float)
    percentCpu = pyqtSignal(float)
    logger = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.controller = MainController()
        self.controller.addLogsToUi(self)
        self.videoFile = None

    def setVideo(self, videoFile):
        self.videoFile = videoFile

    def run(self):
        self.controller.startProcessing(self, self.videoFile, False)

    def setPercentComplete(self, value):
        self.percentComplete.emit(value)

    def setCpuComplete(self, value: float):
        self.percentCpu.emit(value)

    def setMemComplete(self, value: float):
        self.percentMem.emit(value)

    def terminate(self) -> None:
        print("Exiting from the controller")

    def setMessageLog(self, message):
        self.logger.emit(message)

    def __del__(self):
        del self.controller
        del Controller.percentComplete
        del Controller.percentMem
        del Controller.percentCpu
        del Controller.logger
