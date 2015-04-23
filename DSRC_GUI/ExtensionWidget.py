__author__ = 'xuepeng'

from PyQt4 import QtCore, QtGui


class ExtensionWindow(QtGui.QScrollArea):
    def __init__(self, parent):
        QtGui.QScrollArea.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.WindowTitleHint | QtCore.Qt.Tool | QtCore.Qt.WindowCloseButtonHint)
        self.v_layout = QtGui.QVBoxLayout()
        self.setFixedSize(200, 550)
        self.inner_widget = QtGui.QWidget()
        self.inner_widget.setLayout(self.v_layout)
        self.setWidget(self.inner_widget)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.v_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.extension_list = {}
        self.hiding = True

    def add_extension(self, extension_widget):
        if extension_widget.name in self.extension_list:
            pass
        else:
            self.extension_list[extension_widget.name] = extension_widget
            extension_widget.setParent(self)
            self.v_layout.addWidget(extension_widget)

    def closeEvent(self, e):
        if self.hiding:
            self.hide()
        else:
            super(ExtensionWindow, self).closeEvent(e)
            e.accept()

    def stop_self(self):
        self.deleteLater()
        self.hiding = False
        self.close()


class ExtensionItem(QtGui.QPushButton):
    def __init__(self, parent, name, function, args):
        QtGui.QPushButton.__init__(self, parent)
        self.name = name
        self.function = function
        self.args = args
        self.setText(self.name)
        self.setFixedSize(100, 100)
        self.connect(self, QtCore.SIGNAL('clicked()'), self.fire_function)

    def fire_function(self):
        self.function(*self.args)