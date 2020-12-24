""" UI Controller interaction between the UI and the core """

import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot

from torpido.controller import Controller as MainController


class Controller(QThread):
    """
    Middleware between the UI and the main core, all interactions reside here. with slots
    and signals, since, this a derived class of the QThread it can operate without any
    locking mechanism and does not affect the main gui thread.

    Attributes
    ----------

    Controller.percentComplete : pyqtSignal(float)
        signal for progress bar on the UI, progress value comes from torpido.Visual
    Controller.percentMem : pyqtSignal(float)
        signal for the percentage of the memory usage, value comes from torpido.Watcher
    Controller.percentCpu : pyqtSignal(float)
        signal for the percentage of the cpu usage, value comes from torpido.Watcher
    Controller.logger : pyqtSignal(str)
        signal for logs to the ui, all logs are redirected to the ui log window from torpido.Log
    Controller.videoFrame : pyqtSignal(np.ndarray)
        signal to send frames from the video processing, straight to gui thread for display, frames are coming
        from torpido.Visual
    Controller.videoClose : pyqtSignal()
        signal to close the video output
    controller : MainController
        object of the controller class in the core
    videoFile : str
        path of the input video file

    """
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
        """ Set the video file for processing """
        self.videoFile = videoFile

    def run(self):
        """ Start the processing on the input video file """
        self.controller.startProcessing(self, self.videoFile)

    def setVideoDisplay(self, value):
        """ Set up the video display request """
        self.controller.setVideoDisplay(value)

    def setSNRPlot(self, value):
        """ Set up the plotting for SNR audio """
        self.controller.setSNRPlot(value)

    def setRankingPlot(self, value):
        """ Set up the plotting of the analytics """
        self.controller.setRankingPlot(value)

    def setSaveLogs(self, value):
        """ Set up logging to use file to save logs"""
        self.controller.setSaveLogs(value)

    @pyqtSlot()
    def setPercentComplete(self, value):
        """ Emits the signal with the percent for the progress bar """
        self.percentComplete.emit(value)

    @pyqtSlot()
    def setCpuComplete(self, value: float):
        """ Emits the signal with the cpu usage value """
        self.percentCpu.emit(value)

    @pyqtSlot()
    def setMemComplete(self, value: float):
        """ Emits the signal with the memory usage value """
        self.percentMem.emit(value)

    @pyqtSlot()
    def setMessageLog(self, message):
        """ Emits the signal with the log to the ui """
        self.logger.emit(message)

    @pyqtSlot()
    def setVideoFrame(self, frame):
        """ Emits the signal with the video frame to display """
        self.videoFrame.emit(frame)

    @pyqtSlot()
    def setVideoClose(self):
        """ Emits the signal to end the video display """
        self.videoClose.emit()

    def terminate(self) -> None:
        """ Clean up """
        self.controller.clean()
        del Controller.percentComplete
        del Controller.percentMem
        del Controller.percentCpu
        del Controller.logger
