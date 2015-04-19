__author__ = 'xuepeng'

from PyQt4 import QtGui, QtCore
from Event_Module.DSRC_Message_Coder import DSRC_Event, MessageCoder
import Car
import math


class SiderCallback:
    def __init__(self):
        pass

    def car_set(self, car):
        print "Not implemented"

class Sider(QtGui.QWidget):
    def __init__(self, parent, context):
        QtGui.QWidget.__init__(self, parent)
        self.context = context
        self.setFixedSize(200, 1000)
        self.v_layout = QtGui.QVBoxLayout()
        self.display = Display(self)
        self.car_sider = CarSider(self)
        self.function_sider = FunctionSider(self)
        self.v_layout.addWidget(self.display)
        self.v_layout.addWidget(self.car_sider)
        self.v_layout.addWidget(self.function_sider)
        self.setLayout(self.v_layout)
        self.current_car = None
        self.setVisible(True)
        self.callback = None

    def set_car(self, car):
        self.display.dispaly_car(car)
        self.function_sider.remove_all()
        for plugin in car.plugins:
            function_widget = FunctionWidget(self.function_sider, plugin, self.context, car)
            self.function_sider.add_function(function_widget)
        if self.callback:
            self.callback.car_set(car)

    def add_car(self, car):
        self.car_sider.add_car(car)


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
        mode = "Mode:\t"
        follow_target = ""
        if car.mode == Car.MODE_FOLLOW and car.follow_target:
            follow_target = "Target:" + car.follow_target
        interval = "Interval:"
        if car.action != None:
            action = action + str(car.action)

        if car.arg1 != None:
            arg1 = arg1 + str(car.arg1)

        if car.arg2 != None:
            arg2 = arg2 + str(car.arg2)

        if car.mode != None:
            mode = mode + str(car.mode)

        if car.interval != None:
            interval = interval + str(car.interval)

        self.display_content = name + '\n' + \
                               pos_x + '\n' + \
                               pos_y + '\n' + \
                               pos_radian + '\n' + \
                               action + '\n' + \
                               arg1 + '\n' + \
                               arg2 + '\n' + \
                               mode + '\n' + \
                               follow_target + '\n' + \
                               interval

        self.setText(self.display_content)


class CarItem(QtGui.QWidget):
    def __init__(self, parent, car, sider):
        QtGui.QWidget.__init__(self, parent=parent)
        self.car = car
        self.sider = sider
        self.icon = QtGui.QLabel()
        self.icon.setParent(self)
        if self.car.original_image:
            degree_to_rotate = -90
            transform = QtGui.QTransform()
            transform.rotate(degree_to_rotate)
            image = self.car.original_image.transformed(transform)
            self.icon.setPixmap(image)
        self.icon.setGeometry(0, 0, 120, 120)
        self.text = QtGui.QLabel()
        self.text.setParent(self)
        self.text.setText(self.car.name)
        self.text.setGeometry(0, 120, 120, 20)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(120, 140)
        self.setToolTip(self.car.name + ":" + str(self.car.coordinate))

    def contextMenuEvent(self, e):
        self.car.contextMenuEvent(e)

    def mousePressEvent(self, e):
        self.sider.set_car(self.car)
        self.sider.car_sider.set_selected(self.car.name)



class CarSider(QtGui.QScrollArea):
    def __init__(self, parent):
        QtGui.QScrollArea.__init__(self, parent)
        self.sider = parent
        self.car_list = {}
        self.v_layout = QtGui.QVBoxLayout()
        self.setFixedSize(190, 220)
        self.inner_widget = QtGui.QWidget()
        self.inner_widget.setLayout(self.v_layout)
        self.setWidget(self.inner_widget)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    def add_car(self, car):
        if car.name in self.car_list:
            pass
        else:
            car_item = CarItem(self, car, self.sider)
            self.car_list[car.name] = car_item
            self.v_layout.addWidget(car_item)

    def remove_car(self, car):
        car_item = self.car_list.pop(car.name)
        if car_item:
            car_item.setParent(None)
            # self.v_layout.removeWidget(car_item)

    def set_selected(self, car_name):
        for i in self.car_list:
            if i != car_name:
                self.car_list[i].car.set_selected(False)
        self.car_list[car_name].car.set_selected(True)


class FunctionSider(QtGui.QScrollArea):
    def __init__(self, parent):
        QtGui.QScrollArea.__init__(self, parent)
        self.v_layout = QtGui.QVBoxLayout()
        self.setFixedSize(190, 550)
        # self.v_layout.addSpacing()
        # self.setLayout(self.v_layout)
        self.inner_widget = QtGui.QWidget()
        self.inner_widget.setLayout(self.v_layout)
        self.setWidget(self.inner_widget)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.function_list = {}

    def add_function(self, function_widget):
        if function_widget.name in self.function_list:
            pass
        else:
            self.function_list[function_widget.name] = function_widget
            function_widget.setParent(self)
            self.v_layout.addWidget(function_widget)

    def remove_all(self):
        size = self.v_layout.count()
        for i in range(size):
            self.v_layout.itemAt(0).widget().setParent(None)
        self.function_list.clear()


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
        self.car.use_plugin(self.name)
