__author__ = 'xuepeng'

from PyQt4 import QtCore, QtGui
from threading import Thread
import pyqtgraph as pg
import array
import numpy as np
import time
import sys
from random import randint

class Data:
    def __init__(self, max_size):
        self.max_size = max_size
        self.size = 0
        self.x = None
        self.y = array.array('l')

    def addY(self, y):
        if self.size < self.max_size:
            self.size += 1
            self.x = np.arange(self.size)
            self.y.append(y)
        else:
            self.y.pop(0)
            self.y.append(y)

    def getXY(self):
        return self.x, self.y


class ChartListener:
    def __init__(self):
        pass

    def chartClosed(self, chart):
        print "Not implemented!"


class Chart(QtGui.QWidget, Thread):
    def __init__(self, parent, name, update_interval=1, listener=None, max_size=20):
        QtGui.QWidget.__init__(self, parent=parent)
        Thread.__init__(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.name = name
        self.setWindowTitle(self.name)
        self.signal = QtCore.SIGNAL('plot()')
        self.connect(self, self.signal, self.plot_chart)
        self.parent = parent
        self.interval = update_interval
        self.listener = listener
        self.max_size = max_size
        self.running = True
        title = self.name + " Chart"
        self.plot = pg.PlotWidget(title=title, background=None)
        self.plot.setParent(self)
        self.plot.addLegend(offset=(5,5), size=(150,75))
        self.setGeometry(500, 300, 700, 500)
        self.data = {}
        self.dataItem = {}
        self.start()

    def addData(self, name):
        if name not in self.data:
            self.data[name] = Data(self.max_size)
            self.dataItem[name] = pg.PlotDataItem(pen=pg.mkPen(randint(0,255), randint(0,255), randint(0,255)),
                                                  name=name, symbol='+')
            self.plot.addItem(self.dataItem[name])

    def addEntry(self, name, y):
        if name in self.data:
            self.data[name].addY(y)
        else:
            self.addData(name)
            self.data[name].addY(y)

    def plot_chart(self):
        i = 1
        l = len(self.data)
        for data_key in self.data:
            data = self.data[data_key]
            plotItem = self.dataItem[data_key]
            x, y = data.getXY()
            plotItem.setData(x, y)
        self.plot.plot()

    def run(self):
        while self.running:
            self.emit(self.signal)
            time.sleep(self.interval)
        print self.name + " chart Thread end!"

    def closeEvent(self, event):
        self.running = False
        super(Chart, self).closeEvent(event)
        if self.listener:
            self.listener.chartClosed(chart=self)
        event.accept()

    def stop_self(self):
        self.deleteLater()
        self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    charts = Chart(parent=None)

    charts.addData("car1")
    charts.addData("car2")

    charts.addEntry('car1', 20)
    charts.addEntry('car1', 50)
    charts.addEntry('car1', 40)
    charts.addEntry('car1', 80)
    charts.addEntry('car1', 50)
    charts.addEntry('car1', 90)
    charts.addEntry('car1', 40)
    charts.addEntry('car1', 70)
    charts.addEntry('car1', 30)
    charts.addEntry('car1', 80)
    charts.addEntry('car1', 10)

    charts.addEntry('car2', 60)
    charts.addEntry('car2', 30)
    charts.addEntry('car2', 80)
    charts.addEntry('car2', 50)
    charts.addEntry('car2', 0)
    charts.addEntry('car2', 20)
    charts.addEntry('car2', 70)
    charts.addEntry('car2', 10)
    charts.addEntry('car2', 60)
    charts.addEntry('car2', 30)
    charts.addEntry('car2', 40)

    charts.start()

    charts.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
