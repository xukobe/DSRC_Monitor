__author__ = 'xuepengxu'

from PyQt4 import QtGui, QtCore


class Car(QtGui.QLabel):
    def __init__(self):
        super(Car, self).__init__()
        self.coordinate = (0, 0, 0)
        