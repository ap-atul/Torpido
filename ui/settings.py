from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QWidget,
                             QFormLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QVBoxLayout)

from torpido.config.constants import *

WAVELETS_NAMES = ['Daubechies2',
                  'Daubechies3',
                  'Daubechies4',
                  'Daubechies5',
                  'Daubechies6',
                  'Daubechies7',
                  'Daubechies8',
                  'Daubechies9',
                  'Daubechies10',
                  'Daubechies11',
                  'Daubechies12',
                  'Daubechies13',
                  'Daubechies14',
                  'Daubechies15',
                  'Daubechies16',
                  'Daubechies17',
                  'Daubechies18',
                  'Daubechies20',
                  'Symlet2',
                  'Symlet3',
                  'Symlet4',
                  'Symlet5',
                  'Symlet6',
                  'Symlet7',
                  'Symlet8',
                  'Symlet9',
                  'Symlet10',
                  'Symlet11',
                  'Symlet12',
                  'Symlet13',
                  'Symlet14',
                  'Symlet15',
                  'Symlet16',
                  'Symlet17',
                  'Symlet18',
                  'Symlet19',
                  'Symlet20',
                  'Haar',
                  'Coiflet1',
                  'Coiflet2',
                  'Coiflet3',
                  'Coiflet4',
                  'Coiflet5',
                  'Biorthogonal11',
                  'Biorthogonal13',
                  'Biorthogonal15',
                  'Biorthogonal22',
                  'Biorthogonal24',
                  'Biorthogonal26',
                  'Biorthogonal28',
                  'Biorthogonal31',
                  'Biorthogonal33',
                  'Biorthogonal35',
                  'Biorthogonal37',
                  'Biorthogonal39',
                  'Biorthogonal44',
                  'Biorthogonal55',
                  'Biorthogonal68',
                  'Meyer']
WAVELETS_VALUES = ['db2',
                   'db3',
                   'db4',
                   'db5',
                   'db6',
                   'db7',
                   'db8',
                   'db9',
                   'db10',
                   'db11',
                   'db12',
                   'db13',
                   'db14',
                   'db15',
                   'db16',
                   'db17',
                   'db18',
                   'db19',
                   'db20',
                   'sym2',
                   'sym3',
                   'sym4',
                   'sym5',
                   'sym6',
                   'sym7',
                   'sym8',
                   'sym9',
                   'sym10',
                   'sym11',
                   'sym12'
                   'sym13',
                   'sym14',
                   'sym15',
                   'sym16',
                   'sym17',
                   'sym18',
                   'sym19',
                   'sym20',
                   'haar',
                   'coif1',
                   'coif2',
                   'coif3',
                   'coif4',
                   'coif5',
                   'bior1.1',
                   'bior1.3',
                   'bior1.5',
                   'bior2.2',
                   'bior2.4',
                   'bior2.6',
                   'bior2.8',
                   'bior3.1',
                   'bior3.3',
                   'bior3.5',
                   'bior3.7',
                   'bior3.9',
                   'bior4.4',
                   'bior5.5',
                   'bior6.8',
                   'meyer']


class SettingsDialog(QWidget):

    def __init__(self, reboot):
        super().__init__()

        self.reboot = reboot

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
        self.waveletInput.addItems(WAVELETS_NAMES)
        self.waveletInput.setCurrentIndex(WAVELETS_VALUES.index(WAVELET))

        self.watcherDelayInput = QLineEdit()
        self.watcherDelayInput.setText(str(WATCHER_DELAY))

        formLayout.addRow(QLabel("The rank of motion:"), self.rankMotionInput)
        formLayout.addRow(QLabel("The rank of blur:"), self.rankBlurInput)
        formLayout.addRow(QLabel("The rank of audio:"), self.rankAudioInput)
        formLayout.addRow(QLabel("The rank of text:"), self.rankTextInput)
        formLayout.addRow(QLabel("Min rank for the output:"), self.minRankInput)
        formLayout.addRow(QLabel("Motion detection threshold:"), self.motionThresholdInput)
        formLayout.addRow(QLabel("Blur detection threshold:"), self.blurThresholdInput)
        formLayout.addRow(QLabel("Audio detection threshold:"), self.silenceThresholdInput)
        formLayout.addRow(QLabel("Text detection threshold:"), self.textThresholdInput)
        formLayout.addRow(QLabel("Audio block to read (%):"), self.audioBlockInput)
        formLayout.addRow(QLabel("Text detection skip frames:"), self.textSkipFramesInput)
        formLayout.addRow(QLabel("Wavelet name:"), self.waveletInput)
        formLayout.addRow(QLabel("Watcher delay (s):"), self.watcherDelayInput)

        formFrame = QGroupBox("Configuration")
        formFrame.setLayout(formLayout)

        self.save = QPushButton("Save")
        self.save.setToolTip("Requires restart")
        self.save.clicked.connect(self.saveSettings)

        self.exit = QPushButton("Close")
        self.exit.clicked.connect(self.close)

        buttonLayout.addWidget(self.save)
        buttonLayout.addWidget(self.exit)

        mainLayout.addWidget(formFrame)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def saveSettings(self):
        config = {'RANK_MOTION': self.rankMotionInput.text(),
                  'RANK_BLUR': self.rankBlurInput.text(),
                  'RANK_TEXT': self.rankTextInput.text(),
                  'RANK_AUDIO': self.rankAudioInput.text(),
                  'MIN_RANK_OUT_VIDEO': self.minRankInput.text(),
                  'MOTION_THRESHOLD': self.motionThresholdInput.text(),
                  'BLUR_THRESHOLD': self.blurThresholdInput.text(),
                  'SILENCE_THRESHOlD': self.silenceThresholdInput.text(),
                  'TEXT_MIN_CONFIDENCE': self.textThresholdInput.text(),
                  'AUDIO_BLOCK_PER': self.audioBlockInput.text(),
                  'TEXT_SKIP_FRAMES': self.textSkipFramesInput.text(),
                  'WAVELET': WAVELETS_VALUES[self.waveletInput.currentIndex()],
                  'WATCHER_DELAY': self.watcherDelayInput.text()
                  }

        Config.writeAll(config)
        self.reboot.emit()
        self.close()
