import sys

from PyQt5.QtWidgets import QApplication

from ui import App

current = 101


def start():
    app = QApplication(sys.argv)
    torpido = App()

    c = app.exec_()
    del torpido
    return c


if __name__ == '__main__':

    while current == 101:
        current = start()

    sys.exit(current)
