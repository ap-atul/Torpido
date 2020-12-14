import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout,
                             QGraphicsDropShadowEffect, QPushButton,
                             QCheckBox, QPlainTextEdit, QFileDialog, QGroupBox)

from torpido.config import *
from ui.controller import Controller
from ui.settings import SettingsDialog
from ui.widgets import QRoundProgressBar, QLabelAlternate, QVideoWindow


def getShadow():
    shadowEffect = QGraphicsDropShadowEffect()
    shadowEffect.setBlurRadius(20)
    shadowEffect.setOffset(-5)
    shadowEffect.setColor(QColor(72, 58, 78))

    return shadowEffect


class Donut:
    """ Custom progress bar """

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
        self.bar.setValue(0.1)

        return self.bar


class App(QWidget):
    REBOOT = 101

    videoFrame = pyqtSignal(np.ndarray)
    videoClose = pyqtSignal()
    reboot = pyqtSignal()

    def __init__(self):
        super().__init__()
        # middleware class object
        self.controller = Controller()

        # setting the theme
        theme = QtCore.QFile("./ui/theme/style.qss")
        theme.open(QtCore.QIODevice.ReadOnly)

        self.setStyleSheet(QtCore.QTextStream(theme).readAll())
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon('./ui/assets/logo.png'))

        self.videoPicNotSelected = QPixmap('./ui/assets/play-button-not-selected.png')
        self.videoPicNotSelected = self.videoPicNotSelected.scaledToWidth(120)

        self.videoPicSelected = QPixmap('./ui/assets/play-button.png')
        self.videoPicSelected = self.videoPicSelected.scaledToWidth(120)

        self.settingPic = QPixmap('./ui/assets/settings.png')
        self.settingPic = self.settingPic.scaledToWidth(35)

        self.videoImage = QLabelAlternate()
        self.introVideoImage = QLabelAlternate()
        self.extroVideoImage = QLabelAlternate()
        self.settings = QLabelAlternate()

        self.mainProgress = None
        self.cpuProgress = None
        self.memProgress = None
        self.logWindow = None
        self.inputVideoFile = None
        self.video = None
        self.videoDisplayCheckbox = None
        self.snrPlotDisplayCheckbox = None
        self.analyticsCheckbox = None
        self.saveLogsCheckbox = None

        self.buildLayouts()

        # resizing in min size
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.show()

    def buildLayouts(self):
        # base layout
        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(20, 20, 20, 10)
        mainLayout.setSpacing(10)

        # progress v layout
        progressLayout = QGridLayout()

        # file v layout
        fileLayout = QVBoxLayout()
        fileLayout.setSpacing(10)

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

        self.videoImage.setPixmap(self.videoPicNotSelected)
        self.videoImage.setAlignment(QtCore.Qt.AlignLeft)
        self.introVideoImage.setMaximumSize(120, 120)
        self.videoImage.clicked.connect(self.selectFile)
        self.videoImage.setToolTip("Input video file")

        videoLayout = QHBoxLayout()
        videoLayout.setAlignment(QtCore.Qt.AlignLeft)
        videoLayout.addWidget(self.videoImage)
        videoImageFrame = QGroupBox("Input Video")
        videoImageFrame.setLayout(videoLayout)
        fileLayout.addWidget(videoImageFrame)

        self.introVideoImage.setPixmap(self.videoPicNotSelected)
        self.introVideoImage.setMaximumSize(120, 120)
        self.introVideoImage.clicked.connect(self.selectFile)
        self.introVideoImage.setToolTip("Intro video will be placed at the start")
        extraLayout.addWidget(self.introVideoImage)

        self.extroVideoImage.setPixmap(self.videoPicNotSelected)
        self.extroVideoImage.setMaximumSize(120, 120)
        self.extroVideoImage.clicked.connect(self.selectFile)
        self.extroVideoImage.setToolTip("Extro video will be placed at the end")
        extraLayout.addWidget(self.extroVideoImage)

        extraLayout.setSpacing(20)
        extraLayout.setAlignment(QtCore.Qt.AlignLeft)

        extraFrame = QGroupBox("Extro and Intro Videos [Optional]")
        extraFrame.setFlat(True)
        extraFrame.setLayout(extraLayout)
        fileLayout.addWidget(extraFrame)

        self.videoDisplayCheckbox = QCheckBox("Display video output")
        self.videoDisplayCheckbox.setToolTip("Displays the video output while processing")
        self.videoDisplayCheckbox.stateChanged.connect(self.setVideoDisplay)

        self.snrPlotDisplayCheckbox = QCheckBox("Display SNR plot")
        self.snrPlotDisplayCheckbox.setToolTip("Displays the signal to noise ratio plot for audio de-noising")
        self.snrPlotDisplayCheckbox.stateChanged.connect(self.setSNRPlot)

        self.analyticsCheckbox = QCheckBox("Display ranking plot")
        self.analyticsCheckbox.setToolTip("Displays the line plot for ranking of the video and their timestamps")
        self.analyticsCheckbox.stateChanged.connect(self.setRankingPlot)

        self.saveLogsCheckbox = QCheckBox("Save logs to file")
        self.saveLogsCheckbox.setToolTip("Stores the logs in a text file along with some info on the processing")
        self.saveLogsCheckbox.stateChanged.connect(self.setSaveLogs)

        optionsLayout.addWidget(self.videoDisplayCheckbox, 1, 1)
        optionsLayout.addWidget(self.snrPlotDisplayCheckbox, 1, 2)
        optionsLayout.addWidget(self.analyticsCheckbox, 2, 1)
        optionsLayout.addWidget(self.saveLogsCheckbox, 2, 2)

        # frame for the options
        optionsFrame = QGroupBox("Options")
        optionsFrame.setLayout(optionsLayout)
        fileLayout.addWidget(optionsFrame)

        self.settings.setPixmap(self.settingPic)
        self.settings.setToolTip("Settings")
        self.settings.clicked.connect(self.startSettings)
        self.settings.setMaximumSize(40, 40)
        buttonLayout.addWidget(self.settings)

        startButton = QPushButton("Start")
        startButton.setToolTip("Start the processing for the input video given")
        startButton.clicked.connect(self.start)
        buttonLayout.addWidget(startButton)

        exitButton = QPushButton("Exit")
        exitButton.setToolTip("End the processing for the input video given")
        exitButton.clicked.connect(self.exit)
        buttonLayout.addWidget(exitButton)
        fileLayout.addLayout(buttonLayout)

        font = QFont()
        font.setPointSize(10)
        self.logWindow = QPlainTextEdit()
        self.logWindow.setCenterOnScroll(True)
        self.logWindow.setReadOnly(True)
        self.logWindow.setFont(font)
        self.logWindow.setLineWrapMode(QPlainTextEdit.NoWrap)

        # frame for the progress elements
        progressFrame = QGroupBox("Progress Metrics")
        progressFrame.setLayout(progressLayout)

        # frame for the log window
        logLayout = QHBoxLayout()
        logLayout.addWidget(self.logWindow)
        logLayout.setContentsMargins(5, 10, 5, 5)
        logFrame = QGroupBox("Logs")
        logFrame.setLayout(logLayout)
        logFrame.setMaximumHeight(120)

        # setting final layouts
        mainLayout.addWidget(progressFrame, 1, 1)
        mainLayout.addLayout(fileLayout, 1, 2)
        mainLayout.setColumnMinimumWidth(1, 620)
        mainLayout.addWidget(logFrame, 2, 1, 1, 2)

        self.setLayout(mainLayout)
        self.controller.percentComplete.connect(self.mainProgress.setValue)
        self.controller.percentMem.connect(self.memProgress.setValue)
        self.controller.percentCpu.connect(self.cpuProgress.setValue)
        self.controller.logger.connect(self.logWindow.appendPlainText)

        # creating the video window
        self.video = QVideoWindow(self.controller)
        self.controller.videoFrame.connect(self.videoFrame.emit)
        self.controller.videoClose.connect(self.videoClose.emit)
        self.reboot.connect(self.restart)

    def selectFile(self):
        """ Starts a file explorer to select video file """
        name = QFileDialog.getOpenFileName(None,
                                           "Open File",
                                           "~",
                                           "Video Files (*.mp4 *.flv *.avi *.mov *.mpg *.mxf)")

        # setting the data and ui image for video
        if len(name[0]) > 0:
            self.videoImage.setPixmap(self.videoPicSelected)
            self.videoImage.setToolTip(str(name[0]))
            self.inputVideoFile = str(name[0])

    def start(self):
        """ Starting the processing """

        if self.inputVideoFile is not None:
            self.controller.setVideo(self.inputVideoFile)
            self.controller.start()

    def setVideoDisplay(self):
        """ Display a video output """
        self.controller.setVideoDisplay(self.videoDisplayCheckbox.isChecked())

    def setSNRPlot(self):
        """ Display SNR plot for audio """
        self.controller.setSNRPlot(self.snrPlotDisplayCheckbox.isChecked())

    def setRankingPlot(self):
        """ Display analytics for the processing """
        self.controller.setRankingPlot(self.analyticsCheckbox.isChecked())

    def setSaveLogs(self):
        """ Save all logs to a file """
        self.controller.setSaveLogs(self.saveLogsCheckbox.isChecked())

    def startSettings(self):
        self.settings = SettingsDialog(self.reboot)

    def exit(self):
        self.controller.terminate()
        self.close()

    def restart(self):
        self.exit()
        # QtGui.QGuiApplication.exit(self.REBOOT)

    def __del__(self):
        print("Bye !")
