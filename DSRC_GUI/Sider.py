__author__ = 'xuepeng'

from PyQt4 import QtGui, QtCore
from Event_Module.DSRC_Message_Coder import DSRC_Event, MessageCoder


class Sider(QtGui.QWidget):
    def __init__(self, parent, context):
        QtGui.QWidget.__init__(self, parent)
        self.context = context
        self.setFixedSize(200, 1000)
        self.v_layout = QtGui.QVBoxLayout()
        self.display = Display(self)
        self.function_sider = FunctionSider(self)
        self.v_layout.addWidget(self.display)
        self.v_layout.addWidget(self.function_sider)
        self.setLayout(self.v_layout)
        self.current_car = None
        self.setVisible(True)

    def set_car(self, car):
        self.display.dispaly_car(car)
        self.function_sider.remove_all()
        for plugin in car.plugins:
            function_widget = FunctionWidget(self.function_sider, plugin, self.context, car)
            self.function_sider.add_function(function_widget)


class Display(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        self.display_content = None
        self.setFixedSize(190, 220)

    def dispaly_car(self, car):
        name = "Name:\t" + car.name
        pos_x = "X:\t" + str(car.coordinate[0])
        pos_y = "Y:\t" + str(car.coordinate[1])
        pos_radian = "Radian: \t" + str("{:10.2f}".format(car.coordinate[2]))
        action = "Action:\t"
        arg1 = "Velocity:\t"
        arg2 = "Angular rate:\t"
        if car.action:
            action = action + car.action
        if car.arg1:
            arg1 = arg1 + str(car.arg1)
        if car.arg2:
            arg2 = arg2 + str(car.arg2)
        self.display_content = name + '\n' + \
                               pos_x + '\n' + \
                               pos_y + '\n' + \
                               pos_radian + '\n' + \
                               action + '\n' + \
                               arg1 + '\n' + arg2

        self.setText(self.display_content)


class FunctionSider(QtGui.QScrollArea):
    def __init__(self, parent):
        QtGui.QScrollArea.__init__(self, parent)
        self.v_layout = QtGui.QVBoxLayout()
        self.setFixedSize(190, 770)
        # self.v_layout.addSpacing()
        # self.setLayout(self.v_layout)
        self.inner_widget = QtGui.QWidget()
        self.inner_widget.setLayout(self.v_layout)
        self.setWidget(self.inner_widget)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    def add_function(self, function_widget):
        function_widget.setParent(self)
        self.v_layout.addWidget(function_widget)

    def remove_all(self):
        size = self.v_layout.count()
        for i in range(size):
            self.v_layout.itemAt(0).widget().setParent(None)


class FunctionWidget(QtGui.QPushButton):
    def __init__(self, parent, function_name, context, car):
        QtGui.QPushButton.__init__(self, parent)
        self.name = function_name
        self.context = context
        self.car = car
        self.setText(self.name)
        self.setFixedSize(150, 150)
        self.connect(self, QtCore.SIGNAL('clicked()'), self.send_function)

    def send_function(self):
        args = [self.name]
        msg = MessageCoder.generate_command_message(self.context.source,
                                                    self.car.name,
                                                    DSRC_Event.COMMAND_NAME_PLUGIN,
                                                    args)
        self.context.send_msg(msg)
        self.context.log(self.car.name, "Send Plugin " + self.name)
