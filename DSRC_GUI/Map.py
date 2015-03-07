__author__ = 'xuepengxu'

import warnings
import math

from PyQt4 import QtGui, QtCore

GRID_SPAN = 20

class Map(QtGui.QWidget):
    def __init__(self, context, parent, width, height):
        QtGui.QWidget.__init__(self, parent)
        self.w = width
        self.h = height
        self.context = context
        self.setFixedSize(width*self.context.FACTOR + 1, height*self.context.FACTOR + 1)
        self.setAcceptDrops(True)
        self.setVisible(True)

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
            x = i*GRID_SPAN*self.context.FACTOR
            qp.drawLine(x, 0, x, self.height())

        # Horizontal
        h_size = self.h/GRID_SPAN
        for i in range(h_size+1):
            y = i*GRID_SPAN*self.context.FACTOR
            qp.drawLine(0, y, self.width(), y)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))
        e.source().move(e.pos() - QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
