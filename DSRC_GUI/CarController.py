__author__ = 'xuepeng'

from PyQt4 import QtCore
from PyQt4 import QtGui
from DSRC_Resources import DSRC_Resources_Manager as Res_Manager
from Event_Module.DSRC_Message_Coder import MessageCoder, DSRC_Event

SIDE_SIZE = 300


class CarController(QtGui.QWidget):
    def __init__(self, parent, context):
        QtGui.QWidget.__init__(self, parent)
        self.context = context
        self.car = parent
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.WindowTitleHint | QtCore.Qt.Tool | QtCore.Qt.WindowCloseButtonHint)
        self.setGeometry(500, 500, SIDE_SIZE, SIDE_SIZE)
        self.setWindowTitle(self.car.name + ' Control')

        self.left_button = QtGui.QPushButton(self)
        self.right_button = QtGui.QPushButton(self)
        self.up_button = QtGui.QPushButton(self)
        self.down_button = QtGui.QPushButton(self)
        self.stop_button = QtGui.QPushButton(self)

        self.left_icon = QtGui.QIcon(Res_Manager.get_path('left.png'))
        self.right_icon = QtGui.QIcon(Res_Manager.get_path('right.png'))
        self.up_icon = QtGui.QIcon(Res_Manager.get_path('up.png'))
        self.down_icon = QtGui.QIcon(Res_Manager.get_path('down.png'))
        self.stop_icon = QtGui.QIcon(Res_Manager.get_path('stop.png'))

        self.left_active_icon = QtGui.QIcon(Res_Manager.get_path('left_triggered.png'))
        self.right_active_icon = QtGui.QIcon(Res_Manager.get_path('right_triggered.png'))
        self.up_active_icon = QtGui.QIcon(Res_Manager.get_path('up_triggered.png'))
        self.down_active_icon = QtGui.QIcon(Res_Manager.get_path('down_triggered.png'))
        self.stop_active_icon = QtGui.QIcon(Res_Manager.get_path('stop_triggered.png'))

        self.left_button.setIconSize(QtCore.QSize(SIDE_SIZE/3, SIDE_SIZE/3))
        self.right_button.setIconSize(QtCore.QSize(SIDE_SIZE/3, SIDE_SIZE/3))
        self.up_button.setIconSize(QtCore.QSize(SIDE_SIZE/3, SIDE_SIZE/3))
        self.down_button.setIconSize(QtCore.QSize(SIDE_SIZE/3, SIDE_SIZE/3))
        self.stop_button.setIconSize(QtCore.QSize(SIDE_SIZE/3, SIDE_SIZE/3))

        self.left_button.setIcon(self.left_icon)
        self.right_button.setIcon(self.right_icon)
        self.up_button.setIcon(self.up_icon)
        self.down_button.setIcon(self.down_icon)
        self.stop_button.setIcon(self.stop_icon)

        self.left_button.connect(self.left_button, QtCore.SIGNAL('pressed()'), lambda: self.press_handler('left'))
        self.right_button.connect(self.right_button, QtCore.SIGNAL('pressed()'), lambda: self.press_handler('right'))
        self.up_button.connect(self.up_button, QtCore.SIGNAL('pressed()'), lambda: self.press_handler('up'))
        self.down_button.connect(self.down_button, QtCore.SIGNAL('pressed()'), lambda: self.press_handler('down'))
        self.stop_button.connect(self.stop_button, QtCore.SIGNAL('pressed()'), lambda: self.press_handler('stop'))

        self.left_button.connect(self.left_button, QtCore.SIGNAL('released()'), lambda: self.release_handler('left'))
        self.right_button.connect(self.right_button, QtCore.SIGNAL('released()'), lambda: self.release_handler('right'))
        self.up_button.connect(self.up_button, QtCore.SIGNAL('released()'), lambda: self.release_handler('up'))
        self.down_button.connect(self.down_button, QtCore.SIGNAL('released()'), lambda: self.release_handler('down'))
        self.stop_button.connect(self.stop_button, QtCore.SIGNAL('released()'), lambda: self.release_handler('stop'))

        self.left_button.setGeometry(0, SIDE_SIZE/3, SIDE_SIZE/3, SIDE_SIZE/3)
        self.right_button.setGeometry(200, SIDE_SIZE/3, SIDE_SIZE/3, SIDE_SIZE/3)
        self.up_button.setGeometry(SIDE_SIZE/3, 0, SIDE_SIZE/3, SIDE_SIZE/3)
        self.down_button.setGeometry(SIDE_SIZE/3, 200, SIDE_SIZE/3, SIDE_SIZE/3)
        self.stop_button.setGeometry(SIDE_SIZE/3, SIDE_SIZE/3, SIDE_SIZE/3, SIDE_SIZE/3)

    def press_handler(self, direction):
        if direction == 'left':
            self.left_button.setIcon(self.left_active_icon)
        elif direction == 'right':
            self.right_button.setIcon(self.right_active_icon)
        elif direction == 'up':
            self.up_button.setIcon(self.up_active_icon)
        elif direction == 'down':
            self.down_button.setIcon(self.down_active_icon)
        elif direction == 'stop':
            self.stop_button.setIcon(self.stop_active_icon)

    def release_handler(self, direction):
        args = None
        if direction == 'left':
            self.left_button.setIcon(self.left_icon)
            args = [0, 90]
            self.context.log(self.car.name, "Turn left")
        elif direction == 'right':
            self.right_button.setIcon(self.right_icon)
            args = [0, -90]
            self.context.log(self.car.name, "Turn right")
        elif direction == 'up':
            self.up_button.setIcon(self.up_icon)
            args = [30, 0]
            self.context.log(self.car.name, "Go forward")
        elif direction == 'down':
            self.down_button.setIcon(self.down_icon)
            args = [-30, 0]
            self.context.log(self.car.name, "Go backward")
        elif direction == 'stop':
            self.stop_button.setIcon(self.stop_icon)
            args = [0, 0]
            self.context.log(self.car.name, "Stop")
        if args:
            msg = MessageCoder.generate_command_message(self.context.source,
                                                        self.car.name,
                                                        DSRC_Event.COMMAND_NAME_GO,
                                                        args)
            self.context.send_msg(msg)

    def keyPressEvent(self, e):
        key = e.key()
        print "Press " + str(key)
        if key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_A:
            self.press_handler('left')
        elif key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_D:
            self.press_handler('right')
        elif key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_W:
            self.press_handler('up')
        elif key == QtCore.Qt.Key_Down or key == QtCore.Qt.Key_S:
            self.press_handler('down')
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_P:
            self.press_handler('stop')

    def keyReleaseEvent(self, e):
        key = e.key()
        print "Release " + str(key)
        if key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_A:
            self.release_handler('left')
        elif key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_D:
            self.release_handler('right')
        elif key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_W:
            self.release_handler('up')
        elif key == QtCore.Qt.Key_Down or key == QtCore.Qt.Key_S:
            self.release_handler('down')
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_P:
            self.release_handler('stop')







