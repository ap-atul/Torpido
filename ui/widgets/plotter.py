import numpy as np
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    """
    Integration of UI and the matplot lib with Qt
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class JoinBarPlot(QtWidgets.QMainWindow):
    """
    Plotting in the main UI Thread, a separate window with integrated Matplot plots.
    Window of same size, only the data need to be collected from the processes
    via pipes, since the data from different process would not reflect on the
    ui at any cost
    """

    def __init__(self, *args, **kwargs):
        super(JoinBarPlot, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object
        self.sc = MplCanvas(self, width=7, height=5, dpi=100)
        self.setCentralWidget(self.sc)

    def plot(self, dataOne, dataTwo, dataOneTitle, dataTwoTitle):
        width = 0.1
        x_orig = np.arange(len(dataOne))
        self.sc.axes.bar(x_orig - width / 2, np.abs(dataOne), width=width, label=dataOneTitle)
        self.sc.axes.bar(x_orig + width / 2, np.abs(dataTwo), width=width, label=dataTwoTitle)

        self.setWindowTitle("Signal to noise ratios SNR(dB)")
        self.sc.axes.legend(loc=0)
        self.sc.figure.tight_layout()
        print("Plotting the snr")
        self.show()
