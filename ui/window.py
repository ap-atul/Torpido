import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPalette, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QPushButton, QCheckBox,
                             QPlainTextEdit, QFileDialog, QGroupBox)

from torpido.config.config import Config
from torpido.config.constants import *
from ui.controller import Controller
from ui.settings import SettingsDialog
from ui.style.theme import Color, Type, get_theme, get_style_sheet
from ui.widgets import QRoundProgressBar, QLabelAlternate, QVideoWindow

SYS_THEME = get_theme(Config.THEME)
BGR = SYS_THEME[Color.BGR][Type.RGB]
PRI = SYS_THEME[Color.PRI][Type.RGB]
SEC = SYS_THEME[Color.SEC][Type.RGB]
TEX = SYS_THEME[Color.TEX][Type.RGB]

SYS_STYLESHEET = get_style_sheet(Config.THEME)

NOT_SELECTED = ("QLabel { "
                "background-color:" + SYS_THEME[Color.PRI][Type.HEX] + ";"
                                                                       "border-radius: 5px;"
                                                                       "border-style: dashed;"
                                                                       "border-color: #8B8C8D;"
                                                                       "border-width: 1.5px;"
                                                                       "}")

SELECTED = ("QLabel {"
            "background-color:" + SYS_THEME[Color.PRI][Type.HEX] + ";"
                                                                   "border-style: solid;"
                                                                   "border-color: #BEBFC0;"
                                                                   "border-radius: 5px;"
                                                                   "border-width: 1.5px;"
                                                                   "}")


class Donut:
    """ Custom progress bar """

    def __init__(self, name, widget: QWidget):
        self.bar = QRoundProgressBar(widget)
        self.bar.setBackground(BGR)
        self.bar.setObjectName(name)

    def get(self, text):
        palette = QPalette()
        palette.setBrush(QPalette.AlternateBase, QtGui.QColor(BGR))

        if "Light" in Config.THEME:
            palette.setColor(QPalette.Text, QtGui.QColor(18, 18, 18))
        else:
            palette.setColor(QPalette.Text, QtGui.QColor(210, 210, 210))

        self.bar.setPalette(palette)
        self.bar.setNullPosition(QRoundProgressBar.PositionLeft)
        self.bar.setDecimals(1)
        self.bar.setFormat(text)

        # progress bar gradient
        gradientPoints = [(0, TEX),
                          (0.40, SEC),
                          (0.98, PRI)]
        self.bar.setDataColors(gradientPoints)
        self.bar.setValue(100)

        return self.bar


class App(QWidget):
    videoFrame = pyqtSignal(np.ndarray)
    videoClose = pyqtSignal()
    reboot = pyqtSignal()

    def __init__(self):
        super().__init__()

        # middleware class object
        self.controller = Controller()

        # setting the theme
        theme = QtCore.QFile(SYS_STYLESHEET)
        theme.open(QtCore.QIODevice.ReadOnly)

        self.setStyleSheet(QtCore.QTextStream(theme).readAll())
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon('./ui/assets/logo.png'))

        self.videoPicNotSelected = QPixmap('./ui/assets/no-video.png')
        self.videoPicNotSelected = self.videoPicNotSelected.scaledToWidth(120)

        self.videoPicSelected = QPixmap('./ui/assets/video.png')
        self.videoPicSelected = self.videoPicSelected.scaledToWidth(120)

        self.settingPic = QPixmap('./ui/assets/settings.png')
        self.settingPic = self.settingPic.scaledToWidth(35)

        self.videoImage = QLabelAlternate()
        self.introVideoImage = QLabelAlternate()
        self.exitVideoImage = QLabelAlternate()
        self.settings = QLabelAlternate()

        self.mainProgress = None
        self.cpuProgress = None
        self.memProgress = None
        self.logWindow = None
        self.inputVideoFile = None
        self.intro = None
        self.extro = None
        self.video = None
        self.videoDisplayCheckbox = None
        self.specPlotDisplayCheckbox = None
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
        self.videoImage.setMinimumSize(120, 120)
        self.videoImage.clicked.connect(self.selectFile)
        self.videoImage.setToolTip("Input video file")
        self.videoImage.setStyleSheet(NOT_SELECTED)

        videoLayout = QHBoxLayout()
        videoLayout.setAlignment(QtCore.Qt.AlignLeft)
        videoLayout.addWidget(self.videoImage)
        videoImageFrame = QGroupBox("Input Video")
        videoImageFrame.setLayout(videoLayout)
        fileLayout.addWidget(videoImageFrame)

        self.introVideoImage.setPixmap(self.videoPicNotSelected)
        self.introVideoImage.setMaximumSize(120, 120)
        self.introVideoImage.clicked.connect(self.selectIntroFile)
        self.introVideoImage.setToolTip("Intro video will be placed at the start")
        self.introVideoImage.setStyleSheet(NOT_SELECTED)
        extraLayout.addWidget(self.introVideoImage)

        self.exitVideoImage.setPixmap(self.videoPicNotSelected)
        self.exitVideoImage.setMaximumSize(120, 120)
        self.exitVideoImage.clicked.connect(self.selectExtroFile)
        self.exitVideoImage.setToolTip("Exit video will be placed at the end")
        self.exitVideoImage.setStyleSheet(NOT_SELECTED)
        extraLayout.addWidget(self.exitVideoImage)

        extraLayout.setSpacing(20)
        extraLayout.setAlignment(QtCore.Qt.AlignLeft)

        extraFrame = QGroupBox("Exit and Intro Videos [Optional]")
        extraFrame.setFlat(True)
        extraFrame.setLayout(extraLayout)
        fileLayout.addWidget(extraFrame)

        self.videoDisplayCheckbox = QCheckBox("Display video output")
        self.videoDisplayCheckbox.setToolTip("Displays the video output while processing")
        self.videoDisplayCheckbox.stateChanged.connect(self.setVideoDisplay)

        self.specPlotDisplayCheckbox = QCheckBox("Display Spectrogram plot")
        self.specPlotDisplayCheckbox.setToolTip("Displays the spectrogram plot for audio de-noising")
        self.specPlotDisplayCheckbox.stateChanged.connect(self.setSNRPlot)

        self.analyticsCheckbox = QCheckBox("Display ranking plot")
        self.analyticsCheckbox.setToolTip("Displays the line plot for ranking of the video and their timestamps")
        self.analyticsCheckbox.stateChanged.connect(self.setRankingPlot)

        self.saveLogsCheckbox = QCheckBox("Save logs to file")
        self.saveLogsCheckbox.setToolTip("Stores the logs in a text file along with some info on the processing")
        self.saveLogsCheckbox.stateChanged.connect(self.setSaveLogs)

        optionsLayout.addWidget(self.videoDisplayCheckbox, 1, 1)
        optionsLayout.addWidget(self.specPlotDisplayCheckbox, 1, 2)
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
            self.videoImage.setStyleSheet(SELECTED)
            self.videoImage.setToolTip(str(name[0]))
            self.inputVideoFile = str(name[0])

    def selectExtroFile(self):
        """ Starts a file explorer to select video file """
        name = QFileDialog.getOpenFileName(None,
                                           "Open File",
                                           "~",
                                           "Video Files (*.mp4 *.flv *.avi *.mov *.mpg *.mxf)")

        # setting the data and ui image for video
        if len(name[0]) > 0:
            self.exitVideoImage.setPixmap(self.videoPicSelected)
            self.exitVideoImage.setStyleSheet(SELECTED)
            self.exitVideoImage.setToolTip(str(name[0]))
            self.extro = str(name[0])

    def selectIntroFile(self):
        """ Starts a file explorer to select video file """
        name = QFileDialog.getOpenFileName(None,
                                           "Open File",
                                           "~",
                                           "Video Files (*.mp4 *.flv *.avi *.mov *.mpg *.mxf)")

        # setting the data and ui image for video
        if len(name[0]) > 0:
            self.introVideoImage.setPixmap(self.videoPicSelected)
            self.introVideoImage.setStyleSheet(SELECTED)
            self.introVideoImage.setToolTip(str(name[0]))
            self.intro = str(name[0])

    def start(self):
        """ Starting the processing """
        if self.inputVideoFile is not None:
            self.controller.set_video(self.inputVideoFile, self.intro, self.extro)
            self.controller.start()

    def setVideoDisplay(self):
        """ Display a video output """
        self.controller.set_video_display(self.videoDisplayCheckbox.isChecked())

    def setSNRPlot(self):
        """ Display SNR plot for audio """
        self.controller.set_spec_plot(self.specPlotDisplayCheckbox.isChecked())

    def setRankingPlot(self):
        """ Display analytics for the processing """
        self.controller.set_ranking_plot(self.analyticsCheckbox.isChecked())

    def setSaveLogs(self):
        """ Save all logs to a file """
        self.controller.set_save_logs(self.saveLogsCheckbox.isChecked())

    def startSettings(self):
        self.settings = SettingsDialog(self.reboot)

    def exit(self):
        self.controller.terminate()
        self.close()

    def restart(self):
        self.exit()
        # QtGui.QGuiApplication.exit(REBOOT)
