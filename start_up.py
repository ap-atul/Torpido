import sys

from PyQt5.QtWidgets import QApplication

# reboot code
current = 101


def start():
    from ui import App
    app = QApplication(sys.argv)
    torpido = App()

    c = app.exec_()
    del torpido
    return c


if __name__ == '__main__':

    while current == 101:
        current = start()

    sys.exit(current)
