__author__ = 'xuepengxu'

import warnings
import math

from PyQt4 import QtGui, QtCore

GRID_SPAN = 20

class Map(QtGui.QWidget):
    def __init__(self, context, parent, width, height):
        QtGui.QWidget.__init__(self, parent)
        # factor
        factor = 1
        self.w = width
        self.h = height
        self.context = context
        self.resize(width*factor, height*factor)

    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.paint_grid(qp)
        qp.end()

    def paint_grid(self, qp):
        color = QtGui.QColor(0, 0, 0)
        qp.setPen(color)
        # Vertical
        v_size = self.w/GRID_SPAN
        for i in range(v_size+1):
            factor = 1
            x = i*GRID_SPAN*factor
            qp.drawLine(x, 0, x, self.height())

        # Horizontal
        h_size = self.h/GRID_SPAN
        for i in range(h_size+1):
            factor = 1
            y = i*GRID_SPAN*factor
            qp.drawLine(0, y, self.width(), y)