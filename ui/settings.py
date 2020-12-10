from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QWidget,
                             QFormLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QVBoxLayout)

from torpido.config.constants import *

wavelet = {
    "Daubechies2": "db2",
    "Daubechies3": "db3",
    "Daubechies4": "db4",
    "Daubechies5": "db5",
    "Daubechies6": "db6",
    "Daubechies7": "db7",
    "Daubechies8": "db8",
    "Daubechies9": "db9",
    "Daubechies10": "db10",
    "Daubechies11": "db11",
    "Daubechies12": "db12",
    "Daubechies13": "db13",
    "Daubechies14": "db14",
    "Daubechies15": "db15",
    "Daubechies16": "db16",
    "Daubechies17": "db17",
    "Daubechies18": "db18",
    "Daubechies19": "db19",
    "Daubechies20": "db20",
    "Symlet2": "sym2",
    "Symlet3": "sym3",
    "Symlet4": "sym4",
    "Symlet5": "sym5",
    "Symlet6": "sym6",
    "Symlet7": "sym7",
    "Symlet8": "sym8",
    "Symlet9": "sym9",
    "Symlet10": "sym10",
    "Symlet11": "sym11",
    "Symlet12": "sym12",
    "Symlet13": "sym13",
    "Symlet14": "sym14",
    "Symlet15": "sym15",
    "Symlet16": "sym16",
    "Symlet17": "sym17",
    "Symlet18": "sym18",
    "Symlet19": "sym19",
    "Symlet20": "sym20",
    "Haar": "haar",
    "Coiflet1": "coif1",
    "Coiflet2": "coif2",
    "Coiflet3": "coif3",
    "Coiflet4": "coif4",
    "Coiflet5": "coif5",
    "Biorthogonal11": "bior1.1",
    "Biorthogonal13": "bior1.3",
    "Biorthogonal15": "bior1.5",
    "Biorthogonal22": "bior2.2",
    "Biorthogonal24": "bior2.4",
    "Biorthogonal26": "bior2.6",
    "Biorthogonal28": "bior2.8",
    "Biorthogonal31": "bior3.1",
    "Biorthogonal33": "bior3.3",
    "Biorthogonal35": "bior3.5",
    "Biorthogonal37": "bior3.7",
    "Biorthogonal39": "bior3.9",
    "Biorthogonal44": "bior4.4",
    "Biorthogonal55": "bior5.5",
    "Biorthogonal68": "bior6.8",
    "Meyer": "meyer"
}

waveletKeys = list(wavelet.keys())
waveletValues = list(wavelet.values())


class SettingsDialog(QWidget):

    def __init__(self):
        super().__init__()

        # setting the theme
        theme = QtCore.QFile("./ui/theme/style.qss")
        theme.open(QtCore.QIODevice.ReadOnly)

        self.setStyleSheet(QtCore.QTextStream(theme).readAll())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon('./ui/assets/logo.png'))

        self.rankMotionInput = None
        self.rankBlurInput = None
        self.rankTextInput = None
        self.rankAudioInput = None
        self.minRankInput = None
        self.motionThresholdInput = None
        self.blurThresholdInput = None
        self.silenceThresholdInput = None
        self.textThresholdInput = None
        self.audioBlockInput = None
        self.textSkipFramesInput = None
        self.waveletInput = None
        self.watcherDelayInput = None

        self.save = None
        self.exit = None

        self.buildLayouts()
        self.show()

    def buildLayouts(self):
        # main layout
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        mainLayout.setContentsMargins(15, 10, 15, 10)

        # form layout
        formLayout = QFormLayout()
        formLayout.setSpacing(10)
        formLayout.setContentsMargins(10, 10, 10, 10)

        # button layout
        buttonLayout = QHBoxLayout()

        # WIDGETS
        self.rankMotionInput = QLineEdit()
        self.rankMotionInput.setText(str(RANK_MOTION))

        self.rankBlurInput = QLineEdit()
        self.rankBlurInput.setText(str(RANK_BLUR))

        self.rankTextInput = QLineEdit()
        self.rankTextInput.setText(str(RANK_TEXT))

        self.rankAudioInput = QLineEdit()
        self.rankAudioInput.setText(str(RANK_MOTION))

        self.minRankInput = QLineEdit()
        self.minRankInput.setText(str(MIN_RANK_OUT_VIDEO))

        self.motionThresholdInput = QLineEdit()
        self.motionThresholdInput.setText(str(MOTION_THRESHOLD))

        self.blurThresholdInput = QLineEdit()
        self.blurThresholdInput.setText(str(BLUR_THRESHOLD))

        self.silenceThresholdInput = QLineEdit()
        self.silenceThresholdInput.setText(str(SILENCE_THRESHOlD))

        self.textThresholdInput = QLineEdit()
        self.textThresholdInput.setText(str(TEXT_MIN_CONFIDENCE))

        self.audioBlockInput = QLineEdit()
        self.audioBlockInput.setText(str(AUDIO_BLOCK_PER))

        self.textSkipFramesInput = QLineEdit()
        self.textSkipFramesInput.setText(str(TEXT_SKIP_FRAMES))

        self.waveletInput = QComboBox()
        self.waveletInput.addItems(waveletKeys)
        self.waveletInput.setCurrentIndex(waveletValues.index(WAVELET))

        self.watcherDelayInput = QLineEdit()
        self.watcherDelayInput.setText(str(WATCHER_DELAY))

        formLayout.addRow(QLabel("The rank of motion"), self.rankMotionInput)
        formLayout.addRow(QLabel("The rank of blur"), self.rankBlurInput)
        formLayout.addRow(QLabel("The rank of audio"), self.rankAudioInput)
        formLayout.addRow(QLabel("The rank of text"), self.rankTextInput)
        formLayout.addRow(QLabel("Min rank for the output"), self.minRankInput)
        formLayout.addRow(QLabel("Motion detection threshold"), self.motionThresholdInput)
        formLayout.addRow(QLabel("Blur detection threshold"), self.blurThresholdInput)
        formLayout.addRow(QLabel("Audio detection threshold"), self.silenceThresholdInput)
        formLayout.addRow(QLabel("Text detection threshold"), self.textThresholdInput)
        formLayout.addRow(QLabel("Audio block to read (%)"), self.audioBlockInput)
        formLayout.addRow(QLabel("Text detection skip frames"), self.textSkipFramesInput)
        formLayout.addRow(QLabel("Wavelet name"), self.waveletInput)
        formLayout.addRow(QLabel("Watcher delay (s) "), self.watcherDelayInput)

        formFrame = QGroupBox("Configuration")
        formFrame.setLayout(formLayout)

        self.save = QPushButton("Save")
        self.save.clicked.connect(self.close)

        self.exit = QPushButton("Close")
        self.exit.clicked.connect(self.close)

        buttonLayout.addWidget(self.save)
        buttonLayout.addWidget(self.exit)

        mainLayout.addWidget(formFrame)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
