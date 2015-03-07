__author__ = 'xuepeng'

import warnings
import math
import os

from PyQt4 import QtGui, QtCore


class Logger(QtGui.QTextEdit):
    def __init__(self, parent, context, width, height):
        super(Logger, self).__init__(parent)
        self.context = context
        self.w = width
        self.h = height
        self.setFixedSize(width, height)
        self.setReadOnly(True)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        # self.pal = self.palette()
        # self.pal.setColor(QtGui.QPalette.Background, QtGui.QColor(0, 0, 0))
        # self.setPalette(self.pal)
        # self.autoFillBackground()
        self.setStyleSheet("QTextEdit{background-color: black}")
        self.setTextColor(QtGui.QColor(255, 255, 255))
        self.setVisible(True)

    def contextMenuEvent(self, QContextMenuEvent):
        menu = QtGui.QMenu(self)
        save_ation = QtGui.QAction(self)
        save_ation.setText('Save')
        save_ation.connect(save_ation, QtCore.SIGNAL('triggered()'), self.save)
        menu.addAction(save_ation)
        menu.popup(QtGui.QCursor.pos())

    def save(self):
        data = self.toPlainText()
        try:
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Save as', os.path.expanduser("~"))
            if filename:
                f = QtCore.QFile(filename)
                f.open(QtCore.QIODevice.WriteOnly)
                f.writeData(data)
                f.close()
            else:
                self.context.log('Logger', 'No file selected!')
        except Exception, e:
            QtGui.QMessageBox.warning(self, 'Warning', 'IO Exception!')

    def log(self, string):
        self.append(string)