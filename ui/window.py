import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout,
                             QHBoxLayout, QLabel, QGridLayout,
                             QGraphicsDropShadowEffect, QPushButton,
                             QCheckBox, QFrame)

from torpido.config import *
from ui.widgets import QRoundProgressBar, QLabelAlternate

layoutStyle = '''
                border-color: #775157;
                border-width: 1px;
                border-style: solid;
                border-radius: 10px;
              '''


def getShadow():
    shadowEffect = QGraphicsDropShadowEffect()
    shadowEffect.setBlurRadius(5)
    shadowEffect.setOffset(5)
    shadowEffect.setColor(QColor(72, 58, 78))

    return shadowEffect


class Donut:
    def __init__(self, name, widget: QWidget):
        self.bar = QRoundProgressBar(widget)
        self.bar.setObjectName(name)

    def get(self, text):
        palette = QPalette()
        palette.setBrush(QPalette.AlternateBase, QtGui.QColor(42, 42, 50))
        palette.setColor(QPalette.Text, QtGui.QColor(224, 224, 224))
        self.bar.setPalette(palette)
        self.bar.setNullPosition(QRoundProgressBar.PositionLeft)
        self.bar.setDecimals(1)
        self.bar.setFormat(text)

        # progress bar gradient
        gradientPoints = [(0, QtGui.QColor(72, 58, 78)),
                          (0.4, QtGui.QColor(177, 123, 129)),
                          (0.8, QtGui.QColor(191, 141, 124)),
                          (0.9, QtGui.QColor(179, 132, 103))]
        self.bar.setDataColors(gradientPoints)
        self.bar.setValue(99)

        return self.bar


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

        self.videoPicNotSelected = QPixmap('./assets/play-button-not-selected.png')
        self.videoPicNotSelected = self.videoPicNotSelected.scaledToWidth(140)

        self.videoPicSelected = QPixmap('./assets/play-button.png')
        self.videoPicSelected = self.videoPicSelected.scaledToWidth(140)
        self.buildLayouts()

    def buildLayouts(self):
        # base layout
        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)

        # progress v layout
        progressLayout = QGridLayout()

        # file v layout
        fileLayout = QVBoxLayout()
        fileLayout.setSpacing(5)

        # extro and intro layout
        extraLayout = QHBoxLayout()
        extraLayout.setSpacing(10)

        # button layout
        buttonLayout = QHBoxLayout()

        # options layout
        optionsLayout = QGridLayout()

        # WIDGETS
        mainProgress = Donut("mainProgress", self).get('%p%')
        progressLayout.addWidget(mainProgress, 1, 1, 1, 2)

        cpuProgress = Donut("cpuProgress", self).get('%p% \n CPU')
        cpuProgress.setMaximumSize(150, 150)
        progressLayout.addWidget(cpuProgress, 2, 1)

        memProgress = Donut("memProgress", self).get('%p% \n MEM')
        memProgress.setMaximumSize(150, 150)
        progressLayout.addWidget(memProgress, 2, 2)

        select = QLabel("Drag or select a video file")
        select.setAlignment(QtCore.Qt.AlignLeft)
        select.setMaximumHeight(20)
        fileLayout.addWidget(select)

        videoImage = QLabelAlternate()
        videoImage.setPixmap(self.videoPicNotSelected)
        videoImage.setGraphicsEffect(getShadow())
        videoImage.setAlignment(QtCore.Qt.AlignLeft)
        videoImage.setMaximumSize(140, 130)
        videoImage.clicked.connect(self.selectFile)
        fileLayout.addWidget(videoImage)

        optional = QLabel("Select intro and extro video files (optional)")
        optional.setContentsMargins(0, 30, 0, 0)
        optional.setAlignment(QtCore.Qt.AlignLeft)
        fileLayout.addWidget(optional)

        introVideoImage = QLabelAlternate()
        introVideoImage.setPixmap(self.videoPicNotSelected)
        introVideoImage.setGraphicsEffect(getShadow())
        introVideoImage.setMaximumSize(140, 130)
        introVideoImage.clicked.connect(self.selectFile)
        extraLayout.addWidget(introVideoImage)

        extroVideoImage = QLabelAlternate()
        extroVideoImage.setPixmap(self.videoPicNotSelected)
        extroVideoImage.setGraphicsEffect(getShadow())
        extroVideoImage.setMaximumSize(140, 130)
        extroVideoImage.clicked.connect(self.selectFile)

        extraLayout.addWidget(extroVideoImage)
        extraLayout.setSpacing(20)
        extraLayout.setAlignment(QtCore.Qt.AlignLeft)
        fileLayout.addLayout(extraLayout)

        optionLabel = QLabel("Choose below options")
        optionLabel.setContentsMargins(0, 30, 0, 0)
        optionLabel.setAlignment(QtCore.Qt.AlignLeft)
        fileLayout.addWidget(optionLabel)

        option1Label = QCheckBox("Option")
        option2Label = QCheckBox("Option")
        option3Label = QCheckBox("Option")
        option4Label = QCheckBox("Option")

        optionsLayout.addWidget(option1Label, 1, 1)
        optionsLayout.addWidget(option2Label, 1, 2)
        optionsLayout.addWidget(option3Label, 2, 1)
        optionsLayout.addWidget(option4Label, 2, 2)
        optionsLayout.setRowStretch(3, 5)

        fileLayout.addLayout(optionsLayout)

        startButton = QPushButton("Start")
        buttonLayout.addWidget(startButton)

        stopButton = QPushButton("Stop")
        buttonLayout.addWidget(stopButton)
        fileLayout.addLayout(buttonLayout)

        progressFrame = QFrame()
        progressFrame.setLayout(progressLayout)
        progressFrame.setStyleSheet(layoutStyle)

        # setting final layouts
        mainLayout.addWidget(progressFrame, 1, 1)
        mainLayout.addLayout(fileLayout, 1, 2)
        mainLayout.setColumnMinimumWidth(1, 600)
        self.setLayout(mainLayout)

    def selectFile(self):
        print("Yes")


def startApp():
    app = QApplication(sys.argv)
    torpido = App()
    torpido.show()
    sys.exit(app.exec_())


startApp()
