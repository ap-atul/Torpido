import sys
from time import time
from typing import Tuple

import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow


class OpenCVQImage(QtGui.QImage):
    def __init__(self, image: np.ndarray) -> None:
        if len(image.shape) == 3:
            height, width, n_channels = image.shape
            fmt = QtGui.QImage.Format_Grayscale8
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


class CameraDevice(QtCore.QObject):
    new_frame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_id=0, parent=None) -> None:
        super().__init__(parent)

        self._video_capture = cv2.VideoCapture(camera_id)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._query_frame)
        self._timer.setInterval(1000 // self.fps)
        self._timer.start()

    def _query_frame(self) -> None:
        _, frame = self._video_capture.read()
        frame = cv2.resize(frame, (500, 500))
        self.new_frame.emit(frame)

    @property
    def paused(self) -> bool:
        return not self._timer.isActive()

    @paused.setter
    def paused(self, pause: bool) -> None:
        if pause:
            self._timer.stop()
        else:
            self._timer.start()

    @property
    def frame_size(self) -> Tuple[int, int]:
        width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return int(width), int(height)

    @frame_size.setter
    def frame_size(self, size: Tuple[int, int]) -> None:
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def _calculate_fps(self) -> float:
        self._video_capture.read()  # Start up camera
        start_time = time()
        self._video_capture.read()
        return 1 / (time() - start_time)

    @property
    def fps(self) -> int:
        fps = int(self._video_capture.get(cv2.CAP_PROP_FPS))
        if fps <= 0:
            fps = self._calculate_fps()
        return fps


class CameraWidget(QtWidgets.QWidget):
    def __init__(self, camera_device: CameraDevice, parent=None) -> None:
        super().__init__(parent)

        self._camera_device = camera_device
        self._camera_device.new_frame.connect(self._on_new_frame)

        width, height = (500, 500)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

    def _on_new_frame(self, frame: np.ndarray):
        self._frame = frame
        self.update()

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


class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stream = CameraDevice()
        self.video = CameraWidget(self.stream)
        self.video.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoWindow()
    window.show()

    sys.exit(app.exec_())
