import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout

from torpido.config import *
from ui.widgets import QRoundProgressBar


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(WINDOW_HEIGHT)
        self.setMinimumWidth(WINDOW_WIDTH)
        self.setWindowTitle(WINDOW_TITLE)

        self.buildLayouts()

    def buildLayouts(self):
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)

        self.RoundBar4 = QRoundProgressBar(self)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 100, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        self.RoundBar4.setPalette(palette)
        self.RoundBar4.setObjectName("RoundBar4")

        p1 = QPalette()
        p1.setBrush(QPalette.AlternateBase, QtGui.QColor(63, 60, 65))
        p1.setColor(QPalette.Text, QtGui.QColor(224, 224, 224))
        self.RoundBar4.setPalette(p1)
        self.RoundBar4.setNullPosition(QRoundProgressBar.PositionLeft)
        self.RoundBar4.setDecimals(0)

        # progress bar gradient
        gradientPoints = [(0, QtGui.QColor(224, 56, 79)),
                          (0.5, QtGui.QColor(225, 117, 145)),
                          (0.7, QtGui.QColor(247, 219, 212)),
                          (0.9, QtGui.QColor(255, 216, 97))]
        self.RoundBar4.setDataColors(gradientPoints)
        self.RoundBar4.setValue(99)

        mainLayout.addWidget(self.RoundBar4)
        self.setLayout(mainLayout)


def startApp():
    app = QApplication(sys.argv)
    torpido = App()
    torpido.show()
    sys.exit(app.exec_())


startApp()
