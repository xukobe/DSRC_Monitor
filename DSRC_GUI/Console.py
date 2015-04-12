__author__ = 'xuepengxu'

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import math
from Map import Map
from Car import Car
from Logger import Logger
from PyQt4 import QtGui, QtCore
from Event_Module import DSRC_Event
from DSRC_Backend.DSRC_Context import Context, EventListener
from DSRC_Resources import DSRC_Resources_Manager as Res_Manager
from Sider import Sider


class Console(QtGui.QMainWindow, Context, EventListener):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Context.__init__(self)
        EventListener.__init__(self)
        self.register_event_listener(self)
        self.v_layout = QtGui.QVBoxLayout()
        self.v_layout.addStretch(1)
        self.map = Map(context=self, parent=self, width=400, height=400)
        self.logger = Logger(parent=self, context=self, width=800, height=200)
        self.v_layout.addWidget(self.map)
        self.v_layout.addWidget(self.logger)
        self.v_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.sider = Sider(parent=self, context=self)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.addLayout(self.v_layout)
        self.main_layout.addWidget(self.sider)
        widget = QtGui.QWidget(self)
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.cars = {}
        self.current_car = None
        # self.cars['car1'] = Car(context=self, parent=self.map, name='car1', icon_path=Res_Manager.get_path("car.png"))
        # car = self.cars['car1']
        # print str(car.parent())
        # print str(car.width()) + ":" + str(car.height())
        # print str(car.name)
        # print str(car.baseSize().width()) + ":" + str(car.baseSize().height())
        # print str(car.thread())
        # car.go(100, 100, math.pi/2)
        # car.add_plugin("Lane_Change")
        # self.car1.add_plugin("Lead")
        # self.car1.add_plugin('Plugin1')
        # self.car1.add_plugin('Plugin2')
        # self.car1.add_plugin('Plugin3')
        # self.car1.add_plugin('plugin4')
        # self.car1.add_plugin('plugin5')
        # self.car1.add_plugin('plugin5')
        # self.car1.add_plugin('plugin5')

        # self.cars[self.car1.name] = self.car1
        # self.cars[self.car2.name] = self.car2

        self.setWindowTitle("Console")
        self.setWindowIcon(QtGui.QIcon(Res_Manager.get_path('icon.png')))
        self.setGeometry(300, 300, 1000, 1000)
        self.quick_tool = self.addToolBar('Tool')
        self.init_menu_and_tool_bar()
        self.show()
        # self.cars['car2'] = Car(context=self, parent=self.map, name='car2', icon_path=Res_Manager.get_path("car.png"))
        # car = self.cars['car2']
        # car.go(0, 0, math.pi/2)
        # car.add_plugin("Follow")
        # car.show()
        self.initialized = True

    def init_menu_and_tool_bar(self):
        menu = self.menuBar()

        file_menu = menu.addMenu('&File')
        help_menu = menu.addMenu('&Help')

        quit_action = QtGui.QAction('Quit', self)
        quit_action.connect(quit_action, QtCore.SIGNAL('triggered()'), self.close)

        save_action = QtGui.QAction('Save', self)
        save_action.connect(save_action, QtCore.SIGNAL('triggered()'), self.logger.save)

        file_menu.addAction(quit_action)
        file_menu.addAction(save_action)

        about_action = QtGui.QAction('About', self)
        about_action.connect(about_action, QtCore.SIGNAL('triggered()'), self.about)

        help_menu.addAction(about_action)

        self.quick_tool.addAction(quit_action)
        self.quick_tool.addAction(save_action)
        self.quick_tool.addAction(about_action)

    def about(self):
        QtGui.QMessageBox.about(self, 'Smart Vehicle', self.info())

    def info(self):
        msg = "Author: Xuepeng Xu\n" + \
              "Organization: CPSLAB@McGill"
        return msg

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit?"
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.stop_self()
            event.accept()
        else:
            event.ignore()

    def event_handler(self, event):
        if not self.initialized:
            return
        if not event:
            return
        if event.source == self.source:
            return
        else:
            if event.source in self.cars:
                # print "Find car"
                car = self.cars[event.source]
            else:
                # print "Add new Car: " + event.source
                self.cars[event.source] = Car(context=self,
                                              parent=self.map,
                                              name=event.source,
                                              icon_path=Res_Manager.get_path("car.png"))
                car = self.cars[event.source]
                self.sider.add_car(car)
                car.go(0, 0, 0)
            if event.type == DSRC_Event.TYPE_MONITOR_CAR:
                if event.sub_type == DSRC_Event.SUBTYPE_CMD:
                    if event.command.name == DSRC_Event.COMMAND_NAME_RESPONSE_PLUGIN:
                        args = event.command.args
                        plugin_name = args[0]
                        self.cars[event.source].add_plugin(plugin_name)
            elif event.type == DSRC_Event.TYPE_CAR_CAR:
                coord = event.coordinates
                action = event.action
                self.log(car.name, "Update coordinates: " + str(coord.x) + ":" + str(coord.y) + ":" + str(coord.radian))
                if car.coordinate[0] != coord.x or car.coordinate[1] != coord.y or car.coordinate[2] != coord.radian:
                    # print "Move"
                    car.go(coord.x, coord.y, coord.radian)
                    # car.go(100, 100, 0)
                car.action = action.name
                car.arg1 = action.arg1
                car.arg2 = action.arg2

    def mousePressEvent(self, e):
        pos = e.pos()
        ex = pos.x()
        ey = pos.y()
        selected = None
        for i in self.cars:
            car = self.cars[i]
            car_pos = car.pos()
            x = car_pos.x()
            y = car_pos.y()
            w = car.width()
            h = car.height()
            if x <= ex <= (x+w) and y <= ey <= (y+h):
                self.current_car = car
                selected = i
        if selected:
            self.sider.set_car(self.current_car)
            self.current_car.set_selected(True)
            for i in self.cars:
                if i != selected:
                    self.cars[i].set_selected(False)
            self.log('Console', self.current_car.name + " selected!")

    def write_to_log(self, content):
        self.logger.append(str(content))


def main():
    app = QtGui.QApplication(sys.argv)
    console = Console()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()