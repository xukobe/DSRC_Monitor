__author__ = 'xuepengxu'

import warnings
import math

from PyQt4 import QtGui, QtCore


class Car(QtGui.QLabel):
    def __init__(self, context, parent, icon_path):
        QtGui.QLabel.__init__(self, parent=parent)
        self.context = context
        # x, y, radian
        self.coordinate = [0, 0, 0]
        self.icon_path = icon_path
        self.icon = None
        self.load_icon()
        self.setPixmap(self.icon)

    def contextMenuEvent(self, QContextMenuEvent):
        pass

    def go(self, x, y, radian):
        self.coordinate[0] = x
        self.coordinate[1] = y
        if self.coordinate[2] != radian:
            degree_to_rotate = ((radian-self.coordinate[2])/math.pi)*180
            self.icon = self.icon.transformed(QtGui.QTransform().rotate(degree_to_rotate))
            self.coordinate[2] = radian
        # factor
        factor = 1.0
        self.move(x*factor, self.context.map.height() - y*factor)
        self.setPixmap(self.icon)

    def load_icon(self):
        try:
            self.icon = QtGui.QPixmap(self.icon_path)
        except Exception, e:
            print e
            warnings.warn("Cannot load car icon!")

