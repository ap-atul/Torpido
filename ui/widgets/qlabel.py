""" Custom QWidget label for connect signal and slots """

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class QLabelAlternate(QLabel):
    """
    Default pyQt label does not have a clicked event, nor does it calls a method on the
    interaction, so overriding the QLabel class to add a slot for mouse press event.

    Attributes
    ---------
    QLabelAlternate.clicked : pyqtSignal
        signal for the clicked event in the main ui
    """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        """ Initializing the parent class """
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        """" Overriding the mouse press event """
        self.clicked.emit()
