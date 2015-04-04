__author__ = 'xuepengxu'

import warnings
import math

from PyQt4 import QtGui, QtCore
from Event_Module.DSRC_Message_Coder import MessageCoder, DSRC_Event
from CarController import CarController
from CarDialog import CarDialog


class Car(QtGui.QWidget):
    def __init__(self, context, parent, name, icon_path):
        QtGui.QWidget.__init__(self, parent=parent)
        self.context = context
        # x, y, radian
        self.setFixedSize(120, 140)
        self.coordinate = [0, 0, -1]
        self.name = name
        self.icon_path = icon_path
        self.icon = QtGui.QLabel()
        self.icon.setParent(self)
        self.icon.setGeometry(0, 20, 120, 120)
        self.original_image = None
        self.image = None
        self.load_icon()
        if self.original_image:
            self.icon.setPixmap(self.original_image)
        self.text = QtGui.QLabel()
        self.text.setParent(self)
        self.text.setText(self.name)
        self.text.setGeometry(0, 0, 120, 20)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.setToolTip(self.name + ":" + str(self.coordinate))
        self.action = None
        self.arg1 = None
        self.arg2 = None
        self.plugins = []
        self.setVisible(True)

    def add_plugin(self, plugin):
        if plugin not in self.plugins:
            self.plugins.append(plugin)

    def contextMenuEvent(self, e):
        menu = QtGui.QMenu(self)

        open_action = QtGui.QAction('Open', self)
        open_action.connect(open_action, QtCore.SIGNAL('triggered()'), self.open)
        menu.addAction(open_action)

        control_action = QtGui.QAction('Control', self)
        control_action.connect(control_action, QtCore.SIGNAL('triggered()'), self.control)
        menu.addAction(control_action)

        print_action = QtGui.QAction('Info', self)
        print_action.connect(print_action, QtCore.SIGNAL('triggered()'), self.print_info)
        menu.addAction(print_action)

        interval_action = QtGui.QAction('Set Mini Interval', self)
        interval_action.connect(interval_action, QtCore.SIGNAL('triggered()'), self.set_interval)
        menu.addAction(interval_action)

        free_action = QtGui.QAction('To Free Mode', self)
        free_action.connect(free_action, QtCore.SIGNAL('triggered()'), self.to_free)
        menu.addAction(free_action)

        lead_action = QtGui.QAction('To Lead Mode', self)
        lead_action.connect(lead_action, QtCore.SIGNAL('triggered()'), self.to_lead)
        menu.addAction(lead_action)

        customized_action = QtGui.QAction('To Customized Mode', self)
        customized_action.connect(customized_action, QtCore.SIGNAL('triggered()'), self.to_customized)
        menu.addAction(customized_action)

        follow_action = QtGui.QAction('To Follow Mode', self)
        follow_action.connect(follow_action, QtCore.SIGNAL('triggered()'), self.to_follow)
        menu.addAction(follow_action)

        set_follow_action = QtGui.QAction('Set follow target', self)
        set_follow_action.connect(set_follow_action, QtCore.SIGNAL('triggered()'), self.set_follow_target)
        menu.addAction(set_follow_action)

        safe_mode_action = QtGui.QAction('Set robot to safe mode', self)
        safe_mode_action.connect(safe_mode_action, QtCore.SIGNAL('triggered()'), self.to_safe_mode)
        menu.addAction(safe_mode_action)

        full_mode_action = QtGui.QAction('Set robot to full mode', self)
        full_mode_action.connect(full_mode_action, QtCore.SIGNAL('triggered()'), self.to_full_mode)
        menu.addAction(full_mode_action)

        set_pos_action = QtGui.QAction('Set pos', self)
        set_pos_action.connect(set_pos_action, QtCore.SIGNAL('triggered()'), self.set_pos)
        menu.addAction(set_pos_action)

        stop_action = QtGui.QAction('Stop', self)
        stop_action.connect(stop_action, QtCore.SIGNAL('triggered()'), self.stop)
        menu.addAction(stop_action)

        load_plugin_action = QtGui.QAction('Load Plugin', self)
        load_plugin_action.connect(load_plugin_action, QtCore.SIGNAL('triggered()'), self.ask_for_plugin)
        menu.addAction(load_plugin_action)

        disable_plugin_action = QtGui.QAction('Disable Plugin', self)
        disable_plugin_action.connect(disable_plugin_action, QtCore.SIGNAL('triggered()'), self.disable_plugin)
        menu.addAction(disable_plugin_action)

        menu.popup(QtGui.QCursor.pos())

    def open(self):
        dialog = CarDialog(self, self.context)
        dialog.show()

    def control(self):
        self.context.log(self.name, "Opening controller")
        controller = CarController(self, self.context)
        controller.show()

    def print_info(self):
        self.context.log(self.name, "Position: " + str(self.coordinate))

    def set_interval(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Set Interval',
                                              'Enter the mini interval:')
        if ok:
            try:
                value = float(text)
                msg = MessageCoder.generate_setting_message(source=self.context.source,
                                                            destination=self.name,
                                                            setting_name=DSRC_Event.SETTINGS_NAME_MINI_INTERVAL,
                                                            value=value)
                self.context.send_msg(msg)
                self.context.log(self.name, 'Set Minimal Interval, ' + text)
            except ValueError, e:
                QtGui.QMessageBox.warning(self, "Warning", "The input value is not float!")

    def to_lead(self):
        msg = MessageCoder.generate_setting_message(source=self.context.source,
                                                    destination=self.name,
                                                    setting_name=DSRC_Event.SETTINGS_NAME_STYLE,
                                                    value=DSRC_Event.SETTINGS_NAME_STYLE_LEAD)
        self.context.send_msg(msg)
        self.context.log(self.name, 'To Lead mode')

    # def set_follow_target(self):
    #     text, ok = QtGui.QInputDialog.getText(self, 'Target to follow',
    #                                           'Enter car name:')
    #     if ok:
    #         value = [text]
    #         msg = MessageCoder.generate_setting_message(source=self.context.source,
    #                                                     destination=self.name,
    #                                                     setting_name=DSRC_Event.SETTINGS_NAME_STYLE,
    #                                                     value=DSRC_Event.SETTINGS_NAME_STYLE_FOLLOW)
    #         self.context.send_msg(msg)
    #         msg = MessageCoder.generate_command_message(source=self.context.source,
    #                                                     destination=self.name,
    #                                                     cmd=DSRC_Event.COMMAND_NAME_FOLLOW,
    #                                                     args=value)
    #         self.context.send_msg(msg)
    #         self.context.log(self.name, 'To Follow mode, the target is ' + text)

    def to_follow(self):
        msg = MessageCoder.generate_setting_message(source=self.context.source,
                                                    destination=self.name,
                                                    setting_name=DSRC_Event.SETTINGS_NAME_STYLE,
                                                    value=DSRC_Event.SETTINGS_NAME_STYLE_FOLLOW)
        self.context.send_msg(msg)
        self.context.log(self.name, 'To Follow mode')

    def set_follow_target(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Target to follow',
                                              'Enter car name:')
        if ok:
            value = [str(text)]
            # msg = MessageCoder.generate_setting_message(source=self.context.source,
            #                                             destination=self.name,
            #                                             setting_name=DSRC_Event.SETTINGS_NAME_STYLE,
            #                                             value=DSRC_Event.SETTINGS_NAME_STYLE_FOLLOW)
            # self.context.send_msg(msg)
            msg = MessageCoder.generate_command_message(source=self.context.source,
                                                        destination=self.name,
                                                        cmd=DSRC_Event.COMMAND_NAME_FOLLOW,
                                                        args=value)
            self.context.send_msg(msg)
            self.context.log(self.name, 'To Follow mode, the target is ' + str(text))

    def to_free(self):
        msg = MessageCoder.generate_setting_message(source=self.context.source,
                                                    destination=self.name,
                                                    setting_name=DSRC_Event.SETTINGS_NAME_STYLE,
                                                    value=DSRC_Event.SETTINGS_NAME_STYLE_FREE)
        self.context.send_msg(msg)
        self.context.log(self.name, 'To Free mode')

    def to_customized(self):
        msg = MessageCoder.generate_setting_message(source=self.context.source,
                                                    destination=self.name,
                                                    setting_name=DSRC_Event.SETTINGS_NAME_STYLE,
                                                    value=DSRC_Event.SETTINGS_NAME_STYLE_CUSTOMIZED)
        self.context.send_msg(msg)
        self.context.log(self.name, 'To Customized mode')

    def to_safe_mode(self):
        msg = MessageCoder.generate_command_message(source=self.context.source,
                                                    destination=self.name,
                                                    cmd=DSRC_Event.COMMAND_NAME_SAFE_MODE,
                                                    args=None)
        self.context.send_msg(msg)
        self.context.log(self.name, 'To Safe Mode')

    def to_full_mode(self):
        msg = MessageCoder.generate_command_message(source=self.context.source,
                                                    destination=self.name,
                                                    cmd=DSRC_Event.COMMAND_NAME_FULL_MODE,
                                                    args=None)
        self.context.send_msg(msg)
        self.context.log(self.name, 'To Full Mode')

    def set_pos(self):
        text, ok = QtGui.QInputDialog.getText(self, "Set pos (separate by ',')",
                                              'Enter x,y,radian:')
        if ok:
            pos = text.split(',')
            if len(pos) < 3:
                return
            else:
                try:
                    x = int(pos[0])
                    y = int(pos[1])
                    degree = float(pos[2])
                    radian = degree/180 * math.pi
                    args = [x, y, radian]
                    msg = MessageCoder.generate_command_message(source=self.context.source,
                                                                destination=self.name,
                                                                cmd=DSRC_Event.COMMAND_NAME_SET_POS,
                                                                args=args)
                    self.context.send_msg(msg)
                    self.context.log(self.name, "Set pos " + text)
                except ValueError, e:
                    QtGui.QMessageBox.warning(self, "Warning", "The input value is incorrect, "
                                                               "separate x,y and degree by ',', "
                                                               "for instance, (15,20,30.0)")

    def stop(self):
        args = [0, 0]
        msg = MessageCoder.generate_command_message(self.context.source,
                                                    self.name,
                                                    DSRC_Event.COMMAND_NAME_GO,
                                                    args)
        self.context.send_msg(msg)
        self.context.log(self.name, 'Stop')

    def ask_for_plugin(self):
        msg = MessageCoder.generate_command_message(self.context.source,
                                                    self.name,
                                                    DSRC_Event.COMMAND_NAME_ASK_PLUGIN,
                                                    None)
        self.context.send_msg(msg)
        self.context.log(self.name, 'Ask for plugins')

    def disable_plugin(self):
        msg = MessageCoder.generate_command_message(self.context.source,
                                                    self.name,
                                                    DSRC_Event.COMMAND_NAME_DISABLE_PLUGIN,
                                                    None)
        self.context.send_msg(msg)
        self.context.log(self.name, 'Disable plugin')

    def go(self, x, y, radian):
        self.coordinate[0] = x
        self.coordinate[1] = y
        if self.coordinate[2] != radian:
            degree_to_rotate = - (radian/math.pi)*180
            transform = QtGui.QTransform()
            transform.rotate(degree_to_rotate)
            self.image = self.original_image.transformed(transform)
            self.coordinate[2] = radian
        x_center = x*self.context.FACTOR - self.icon.width()/2
        y_center = y*self.context.FACTOR + self.icon.height()/2
        self.move(x_center, self.context.map.height() - y_center)
        if self.image:
            self.icon.setPixmap(self.image)
        self.setToolTip(self.name + ":" + str(self.coordinate))

    def load_icon(self):
        try:
            self.original_image = QtGui.QPixmap(self.icon_path)
        except Exception, e:
            print e
            warnings.warn("Cannot load car icon!")

    def mouseDoubleClickEvent(self, e):
        self.control()

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            mime_data = QtCore.QMimeData()
            mime_data.setText('%d, %d' % (e.x(), e.y()))
            drag = QtGui.QDrag(self)
            drag.setMimeData(mime_data)
            if self.image:
                drag.setPixmap(self.image)
            elif self.original_image:
                drag.setPixmap(self.original_image)
            drag.setHotSpot(e.pos())
            if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
                x = (self.x() + self.icon.width()/2)/self.context.FACTOR
                y = (self.context.map.height() - self.y() - self.icon.height()/2)/self.context.FACTOR
                dy = y - self.coordinate[1]
                dx = x - self.coordinate[0]
                # issue
                d2 = dy*dy + dx*dx
                if d2:
                    radian = math.asin(float(dy)/math.sqrt(d2))
                else:
                    return
                if dx < 0:
                    radian = math.pi - radian
                self.go(x, y, radian)
                args = [x, y]
                msg = MessageCoder.generate_command_message(self.context.source,
                                                            self.name,
                                                            DSRC_Event.COMMAND_NAME_GO_TO,
                                                            args)
                self.context.send_msg(msg)
                self.context.log(self.name, "Drag and drop from (" + str(self.coordinate[0]) + "," +
                                 str(self.coordinate[1]) + ") to (" + str(x) + str(y) + ").")
