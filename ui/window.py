from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QGridLayout,
                             QGraphicsDropShadowEffect, QPushButton,
                             QCheckBox, QFrame, QPlainTextEdit, QFileDialog)

from torpido.config import *
from ui.controller import Controller
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
        gradientPoints = [(0, QtGui.QColor(179, 132, 103)),
                          (0.2, QtGui.QColor(191, 141, 124)),
                          (0.40, QtGui.QColor(177, 123, 129)),
                          (0.95, QtGui.QColor(72, 58, 78))]
        self.bar.setDataColors(gradientPoints)
        self.bar.setValue(100)

        return self.bar


class App(QWidget):
    def __init__(self):
        super().__init__()

        # middleware class object
        self.controller = Controller()

        # setting the theme
        theme = QtCore.QFile("./ui/theme/style.qss")
        theme.open(QtCore.QIODevice.ReadOnly)

        self.setStyleSheet(QtCore.QTextStream(theme).readAll())
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMaximumSize(1280, 720)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon('./ui/assets/logo.png'))

        self.videoPicNotSelected = QPixmap('./ui/assets/play-button-not-selected.png')
        self.videoPicNotSelected = self.videoPicNotSelected.scaledToWidth(140)

        self.videoPicSelected = QPixmap('./ui/assets/play-button.png')
        self.videoPicSelected = self.videoPicSelected.scaledToWidth(140)

        self.videoImage = QLabelAlternate()
        self.introVideoImage = QLabelAlternate()
        self.extroVideoImage = QLabelAlternate()

        self.mainProgress = None
        self.cpuProgress = None
        self.memProgress = None
        self.logWindow = None
        self.inputVideoFile = None
        self.threadPool = QThreadPool()

        self.buildLayouts()

    def buildLayouts(self):
        # base layout
        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(20, 20, 20, 10)
        mainLayout.setSpacing(10)

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
        self.mainProgress = Donut("mainProgress", self).get('%p%')
        self.mainProgress.setToolTip("Progress bar to represent the percentage completion of the video editing")
        progressLayout.addWidget(self.mainProgress, 1, 1, 1, 2)

        self.cpuProgress = Donut("cpuProgress", self).get('%p% \n CPU')
        self.cpuProgress.setToolTip("Progress bar to represent the percentage usage of CPU by VEA")
        self.cpuProgress.setMaximumSize(120, 120)
        progressLayout.addWidget(self.cpuProgress, 2, 1)

        self.memProgress = Donut("memProgress", self).get('%p% \n MEM')
        self.memProgress.setToolTip("Progress bar to represent the percentage usage of Memory/RAM by VEA")
        self.memProgress.setMaximumSize(120, 120)
        progressLayout.addWidget(self.memProgress, 2, 2)

        select = QLabel("Drag or select a video file")
        select.setAlignment(QtCore.Qt.AlignLeft)
        select.setMaximumHeight(20)
        fileLayout.addWidget(select)

        self.videoImage.setPixmap(self.videoPicNotSelected)
        self.videoImage.setGraphicsEffect(getShadow())
        self.videoImage.setAlignment(QtCore.Qt.AlignLeft)
        self.videoImage.setMaximumSize(140, 130)
        self.videoImage.clicked.connect(self.selectFile)
        self.videoImage.setToolTip("Input video file")
        fileLayout.addWidget(self.videoImage)

        optional = QLabel("Select intro and extro video files (optional)")
        optional.setContentsMargins(0, 30, 0, 0)
        optional.setAlignment(QtCore.Qt.AlignLeft)
        fileLayout.addWidget(optional)

        self.introVideoImage.setPixmap(self.videoPicNotSelected)
        self.introVideoImage.setGraphicsEffect(getShadow())
        self.introVideoImage.setMaximumSize(140, 130)
        self.introVideoImage.clicked.connect(self.selectFile)
        self.introVideoImage.setToolTip("Intro video will be placed at the start")
        extraLayout.addWidget(self.introVideoImage)

        self.extroVideoImage.setPixmap(self.videoPicNotSelected)
        self.extroVideoImage.setGraphicsEffect(getShadow())
        self.extroVideoImage.setMaximumSize(140, 130)
        self.extroVideoImage.clicked.connect(self.selectFile)
        self.extroVideoImage.setToolTip("Extro video will be placed at the end")
        extraLayout.addWidget(self.extroVideoImage)

        extraLayout.setSpacing(20)
        extraLayout.setAlignment(QtCore.Qt.AlignLeft)
        fileLayout.addLayout(extraLayout)

        optionLabel = QLabel("Choose below options")
        optionLabel.setContentsMargins(0, 30, 0, 0)
        optionLabel.setAlignment(QtCore.Qt.AlignLeft)
        fileLayout.addWidget(optionLabel)

        displayVideo = QCheckBox("Display video output")
        displayVideo.setToolTip("Displays the video output while processing")

        snrDisplay = QCheckBox("Display SNR plot")
        snrDisplay.setToolTip("Displays the signal to noise ratio plot for audio de-noising")

        rankingPlot = QCheckBox("Display ranking plot")
        rankingPlot.setToolTip("Displays the line plot for ranking of the video and their timestamps")

        logOption = QCheckBox("Keep logs")
        logOption.setToolTip("Stores the logs in a text file along with some info on the processing")

        optionsLayout.addWidget(displayVideo, 1, 1)
        optionsLayout.addWidget(snrDisplay, 1, 2)
        optionsLayout.addWidget(rankingPlot, 2, 1)
        optionsLayout.addWidget(logOption, 2, 2)
        optionsLayout.setRowStretch(3, 5)
        fileLayout.addLayout(optionsLayout)

        startButton = QPushButton("Start")
        startButton.setToolTip("Start the processing for the input video given")
        startButton.clicked.connect(self.start)
        buttonLayout.addWidget(startButton)

        stopButton = QPushButton("Stop")
        stopButton.setToolTip("End the processing for the input video given")
        stopButton.clicked.connect(self.close)
        buttonLayout.addWidget(stopButton)
        fileLayout.addLayout(buttonLayout)

        font = QFont()
        font.setPointSize(10)
        self.logWindow = QPlainTextEdit()
        self.logWindow.setMaximumHeight(80)
        self.logWindow.setCenterOnScroll(True)
        self.logWindow.setReadOnly(True)
        self.logWindow.setFont(font)
        self.logWindow.setLineWrapMode(QPlainTextEdit.NoWrap)

        progressFrame = QFrame()
        progressFrame.setLayout(progressLayout)
        progressFrame.setStyleSheet(layoutStyle)

        # setting final layouts
        mainLayout.addWidget(progressFrame, 1, 1)
        mainLayout.addLayout(fileLayout, 1, 2)
        mainLayout.setColumnMinimumWidth(1, 600)
        mainLayout.addWidget(self.logWindow, 2, 1, 1, 2)

        self.setLayout(mainLayout)
        self.controller.signal.percentComplete.connect(self.setProgress)
        self.controller.signal.percentMem.connect(self.setMem)
        self.controller.signal.percentCpu.connect(self.setCpu)
        self.controller.signal.logger.connect(self.setLog)

    def selectFile(self):
        name = QFileDialog.getOpenFileName(None, "Open File", "~",
                                           "Video Files (*.mp4 *.flv *.avi *.mov *.mpg *.mxf)")

        if len(name[0]) > 0:
            # self.videoImage.setPixmap(self.videoPicSelected)
            self.videoImage.setToolTip(str(name[0]))
            self.inputVideoFile = str(name[0])

    def setProgress(self, value):
        self.mainProgress.setValue(value)

    def setCpu(self, value):
        self.cpuProgress.setValue(value)

    def setMem(self, value):
        self.memProgress.setValue(value)

    def setLog(self, message):
        self.logWindow.appendPlainText(message)

    def start(self):
        if self.inputVideoFile is not None:
            self.controller.setVideo(self.inputVideoFile)
            self.threadPool.start(self.controller)

    def __del__(self):
        if self.controller is not None:
            self.controller.terminate()

        del self.controller
