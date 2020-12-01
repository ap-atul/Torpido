import sys

from PyQt5.QtWidgets import QApplication

from ui.window import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    torpido = App()
    torpido.start()
    #
    # d1 = [10, 20, 30, 40]
    # d2 = [15, 25, 35, 45]
    #
    # bar = JoinBarPlot()
    # bar.plot(dataOne=d1,
    #          dataTwo=d2,
    #          dataOneTitle="Data one",
    #          dataTwoTitle="Data two")

    sys.exit(app.exec_())
