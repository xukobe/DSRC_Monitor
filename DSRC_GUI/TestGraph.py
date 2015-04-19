__author__ = 'xuepeng'
from PyQt4 import QtGui, QtCore
import sys

import pyqtgraph as pg
import array
import numpy as np


class Console(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # self.main_layout = QtGui.QHBoxLayout()
        widget = QtGui.QWidget(self)
        # widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("Console")
        #
        x = np.arange(13)
        # x = array.array('l', [1,2,3,4,5,7,4,85,34,6,3,64,6])
        # y = np.random.normal(size=(1, 1000))
        # y = [1,5,3,7,22,7,4,85,34,6,3,64,6]
        y = array.array('l', [1,5,3,7,22,7,4,85,34,6,3,64,6])
        # plotWidget = pg.PlotWidget(widget,background=None)
        # plotWidget.setGeometry(300,300,400,400)
        # pen = pg.mkPen(color=pg.mkColor(255,255,255))
        # plotWidget.plot(x, y, pen)  ## setting pen=(i,3) automaticaly creates three different-colored pens
        #
        # self.setGeometry(300, 300, 1000, 1000)

        plot = pg.PlotWidget(background=None, title="Title")

        ## Create a grid layout to manage the widgets size and position
        layout = QtGui.QGridLayout()
        widget.setLayout(layout)

        ## Add widgets to the layout in their proper positions

        layout.addWidget(plot)  # plot goes on right side, spanning 3 rows
        plot.plot(x,y,pen=(1,2))
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    console = Console()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()