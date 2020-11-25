import sys

from PyQt5.QtWidgets import QWidget, QApplication

from torpido.config import *


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(WINDOW_HEIGHT)
        self.setMinimumWidth(WINDOW_WIDTH)
        self.setWindowTitle(WINDOW_TITLE)

        self.buildLayouts()

    def buildLayouts(self):


def startApp():
    app = QApplication(sys.argv)
    torpido = App()
    torpido.show()
    sys.exit(app.exec_())


startApp()
