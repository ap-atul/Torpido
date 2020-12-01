import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot

from controller import Controller as MainController


class Controller(QThread):
    percentComplete = pyqtSignal(float)
    percentMem = pyqtSignal(float)
    percentCpu = pyqtSignal(float)
    logger = pyqtSignal(str)
    videoFrame = pyqtSignal(np.ndarray)
    videoClose = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.controller = MainController()

        self.videoFile = None

    def setVideo(self, videoFile):
        self.videoFile = videoFile

    def run(self):
        self.controller.startProcessing(self, self.videoFile, False)

    @pyqtSlot()
    def setPercentComplete(self, value):
        self.percentComplete.emit(value)

    @pyqtSlot()
    def setCpuComplete(self, value: float):
        self.percentCpu.emit(value)

    @pyqtSlot()
    def setMemComplete(self, value: float):
        self.percentMem.emit(value)

    @pyqtSlot()
    def setMessageLog(self, message):
        self.logger.emit(message)

    @pyqtSlot()
    def setVideoFrame(self, frame):
        self.videoFrame.emit(frame)

    @pyqtSlot()
    def setVideoClose(self):
        self.videoClose.emit()

    def __del__(self):
        del self.controller
        del Controller.percentComplete
        del Controller.percentMem
        del Controller.percentCpu
        del Controller.logger
