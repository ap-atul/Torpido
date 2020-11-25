import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel

from torpido.config import *
from ui.widgets import QRoundProgressBar


class App(QWidget):
    def __init__(self):
        super().__init__()

        # setting the theme
        theme = QtCore.QFile("./theme/style.qss")
        theme.open(QtCore.QIODevice.ReadOnly)

        self.setStyleSheet(QtCore.QTextStream(theme).readAll())
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMaximumSize(1280, 720)
        self.setWindowTitle(WINDOW_TITLE)

        self.buildLayouts()
        self.placeWidgets()

    def buildLayouts(self):
        # base layout
        mainLayout = QHBoxLayout()
        mainLayout.setSpacing(0)

        # progress v layout
        progressLayout = QVBoxLayout()
        progressLayout.setSpacing(10)
        progressLayout.setContentsMargins(0, 0, 0, 0)

        # file v layout
        fileLayout = QVBoxLayout()
        fileLayout.setSpacing(1)
        fileLayout.setContentsMargins(120, 0, 0, 0)

        # main progress layout
        mainProgressLayout = QHBoxLayout()
        mainProgressLayout.setSpacing(10)
        progressLayout.addLayout(mainProgressLayout)

        # secondary progress layout
        secondaryProgressLayout = QHBoxLayout()
        secondaryProgressLayout.setSpacing(10)
        progressLayout.addLayout(secondaryProgressLayout)

        # cpu progress layout
        cpuProgressLayout = QVBoxLayout()
        cpuProgressLayout.setSpacing(10)
        secondaryProgressLayout.addLayout(cpuProgressLayout)

        # mem progress layout
        memProgressLayout = QVBoxLayout()
        memProgressLayout.setSpacing(10)
        secondaryProgressLayout.addLayout(memProgressLayout)

        self.RoundBar4 = QRoundProgressBar(self)
        self.RoundBar4.setObjectName("RoundBar4")

        p1 = QPalette()
        p1.setBrush(QPalette.AlternateBase, QtGui.QColor(42, 42, 50))
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

        progressLayout.addWidget(self.RoundBar4)

        label = QLabel("Heello")
        fileLayout.addWidget(label)

        mainLayout.addLayout(progressLayout)
        mainLayout.addLayout(fileLayout)
        self.setLayout(mainLayout)


def startApp():
    app = QApplication(sys.argv)
    torpido = App()
    torpido.show()
    sys.exit(app.exec_())


startApp()
