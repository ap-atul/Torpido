from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class QLabelAlternate(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()
