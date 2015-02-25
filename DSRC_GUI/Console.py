__author__ = 'xuepengxu'

import sys, os
import math
from Map import Map
from Car import Car
from PyQt4 import QtGui, QtCore

RES_PATh = os.path.join(os.path.dirname(__file__), '../Resources/')


class Console(QtGui.QWidget):
    def __init__(self):
        super(Console, self).__init__()
        self.map = Map(context=self, parent=self, width=800, height=800)
        self.map.move(0, 0)
        print RES_PATh+"car.png"
        self.car = Car(context=self, parent=self.map, icon_path=(RES_PATh+"car.png"))
        self.car.go(100, 100, math.pi)
        self.setWindowTitle("Console")
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    console = Console()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()