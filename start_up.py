import sys

from PyQt5.QtWidgets import QApplication

from ui.window import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    torpido = App()
    currentCode = app.exec_()
    sys.exit(currentCode)