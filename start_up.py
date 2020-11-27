import sys

from PyQt5.QtWidgets import QApplication

from ui.window import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    torpido = App()
    torpido.start()

    sys.exit(app.exec_())
