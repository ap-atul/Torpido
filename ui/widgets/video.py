""" QWidget for Open cv im show alternative with Qt """

import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow


class OpenCVQImage(QtGui.QImage):
    """ Conversion of open cv image to QImage """

    def __init__(self, image: np.ndarray) -> None:
        if len(image.shape) == 3:
            height, width, n_channels = image.shape
            fmt = QtGui.QImage.Format_BGR30
        else:
            height, width = image.shape
            n_channels = 1
            fmt = QtGui.QImage.Format_Grayscale8
        super().__init__(
            image.tostring(),
            width,
            height,
            n_channels * width,
            fmt
        )


class QVideoWidget(QtWidgets.QWidget):
    """ Widget with paint events and communication slot for frame retrieval and display """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        width, height = 500, 500
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        self._frame = None

    def setFrame(self, frame: np.ndarray):
        """ Set the frame to the window """
        self._frame = frame
        cv2.imshow("Video Output", self._frame)

    def end(self):
        """ Close all the windows """
        cv2.destroyAllWindows()

    def changeEvent(self, event: QtCore.QEvent) -> None:
        if event.type() == QtCore.QEvent.EnabledChange:
            if self.isEnabled():
                self._camera_device.new_frame.connect(self._on_new_frame)
            else:
                self._camera_device.new_frame.disconnect(self._on_new_frame)
        super().changeEvent(event)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), OpenCVQImage(self._frame))
        super().paintEvent(event)


class QVideoWindow(QMainWindow):
    """ Separate window for video display """

    def __init__(self, window):
        super().__init__()

        self.window = window

        self.setWindowTitle("Video Output")
        self.setMaximumSize(600, 500)
        self.setMinimumSize(600, 500)

        self.video = QVideoWidget(self)
        self.setCentralWidget(self.video)

        self.window.videoFrame.connect(self.video.setFrame)
        self.window.videoClose.connect(self.video.end)
