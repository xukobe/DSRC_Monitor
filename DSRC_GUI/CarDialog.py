__author__ = 'xuepeng'

from PyQt4 import QtCore, QtGui
from Event_Module import DSRC_Event
from DSRC_Resources import DSRC_Resources_Manager as Res_Manager

SIDE_SIZE = 560

QTYPE_FORWARD = 'forward'
FORWARD_ARG1 = 30
FORWARD_ARG2 = 0

QTYPE_BACKWARD = 'backward'
BACKWARD_ARG1 = -30
BACKWARD_ARG2 = 0

QTYPE_LEFT = 'left'
LEFT_ARG1 = 0
LEFT_ARG2 = 90

QTYPE_RIGHT = 'right'
RIGHT_ARG1 = 0
RIGHT_ARG2 = -90

QTYPE_STOP = 'stop'
STOP_ARG1 = 0
STOP_ARG2 = 0

QTYPE_CUSTOMIZED = 'customized'
CUSTOMIZED_ARG1 = 0
CUSTOMIZED_ARG2 = 0


class CarDialog(QtGui.QWidget):
    def __init__(self, car, context):
        QtGui.QWidget.__init__(self, car)
        self.context = context
        self.car = car
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.WindowTitleHint | QtCore.Qt.Tool | QtCore.Qt.WindowCloseButtonHint)
        self.setGeometry(500, 500, SIDE_SIZE, SIDE_SIZE)
        self.template_box = TemplateBoxWidget(self, self.context)
        self.template_box.setGeometry(10, 10, 330, 400)

        # template
        self.up_job = TemplateWidget(self.template_box, QTYPE_FORWARD)
        self.down_job = TemplateWidget(self.template_box, QTYPE_BACKWARD)
        self.left_job = TemplateWidget(self.template_box, QTYPE_LEFT)
        self.right_job = TemplateWidget(self.template_box, QTYPE_RIGHT)
        self.stop_job = TemplateWidget(self.template_box, QTYPE_STOP)
        self.customized_job = TemplateWidget(self.template_box, QTYPE_CUSTOMIZED)

        self.template_box.add_template(self.up_job)
        self.template_box.add_template(self.down_job)
        self.template_box.add_template(self.left_job)
        self.template_box.add_template(self.right_job)
        self.template_box.add_template(self.stop_job)
        self.template_box.add_template(self.customized_job)

        self.job_list = JobCollectionWidget(self, self.car, self.context)
        self.job_list.setGeometry(350, 10, 200, 450)

        self.submit_button = QtGui.QPushButton("Submit", self)
        self.cancel_button = QtGui.QPushButton("Cancel", self)

        self.submit_button.setGeometry(470, 480, 80, 60)
        self.cancel_button.setGeometry(370, 480, 80, 60)

        self.submit_button.connect(self.submit_button, QtCore.SIGNAL('clicked()'), self.submit)
        self.cancel_button.connect(self.cancel_button, QtCore.SIGNAL('clicked()'), self.cancel)

        self.setAcceptDrops(True)

        self.setWindowTitle(self.car.name)

    def submit(self):
        job_list = []
        size = self.job_list.list_widget.count()
        for i in range(size):
            job = self.job_list.list_widget.item(i).job
            job_list.append(job)
        self.context.send_batch(self.context.source, self.car.name, job_list)
        self.context.log(self.car.name, "Jobs are submitted!")
        self.close()

    def cancel(self):
        self.context.log(self.car.name, "Jobs are cancelled!")
        self.close()


class TemplateBoxWidget(QtGui.QFrame):
    def __init__(self, parent, context):
        QtGui.QWidget.__init__(self, parent)
        self.context = context
        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.setAlignment(QtCore.Qt.AlignTop)
        self.col_num = 3
        self.total_num = 0
        self.setLayout(self.grid_layout)
        self.setFrameShape(QtGui.QFrame.Box)
        self.setAcceptDrops(True)

    def add_template(self, template):
        i = self.total_num / self.col_num
        j = self.total_num % self.col_num
        self.total_num += 1
        self.grid_layout.addWidget(template, i, j)

    def dragEnterEvent(self, e):
        if e.dropAction() == QtCore.Qt.CopyAction:
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        if e.dropAction() == QtCore.Qt.CopyAction:
            e.acceptProposedAction()

    def dropEvent(self, e):
        e.ignore()


class JobCollectionWidget(QtGui.QFrame):
    def __init__(self, parent, car, context):
        QtGui.QWidget.__init__(self, parent)
        self.car = car
        self.context = context
        self.list_widget = JobListWidget(self, car, context)
        self.list_widget.setGeometry(0, 0, 200, 400)

        self.up_button = QtGui.QPushButton("+", self)
        self.down_button = QtGui.QPushButton("-", self)
        self.up_button.setGeometry(140, 400, 30, 30)
        self.down_button.setGeometry(170, 400, 30, 30)
        self.up_button.connect(self.up_button, QtCore.SIGNAL('clicked()'), self.move_item_up)
        self.down_button.connect(self.down_button, QtCore.SIGNAL('clicked()'), self.move_item_down)

    def move_item_up(self):
        items = self.list_widget.selectedItems()
        if len(items) > 0:
            current_row = self.list_widget.row(items[0])
            if current_row == 0:
                return
            else:
                pre_row = current_row - 1
                item = self.list_widget.takeItem(current_row)
                self.list_widget.insertItem(pre_row, item)
                self.list_widget.setCurrentRow(pre_row)

    def move_item_down(self):
        items = self.list_widget.selectedItems()
        if len(items) > 0:
            current_row = self.list_widget.row(items[0])
            if current_row == self.list_widget.count() - 1:
                return
            else:
                next_row = current_row + 1
                item = self.list_widget.takeItem(current_row)
                self.list_widget.insertItem(next_row, item)
                self.list_widget.setCurrentRow(next_row)


class JobListWidget(QtGui.QListWidget):
    def __init__(self, parent, car, context):
        QtGui.QListWidget.__init__(self, parent)
        self.context = context
        self.car = car
        self.setAcceptDrops(True)
        self.total_num = 0
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

    def add_job(self, job_item):
        self.addItem(job_item)

    def remove_job(self, job_item):
        self.takeItem(self.row(job_item))

    def dragEnterEvent(self, e):
        if e.dropAction() == QtCore.Qt.CopyAction:
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        if e.dropAction() == QtCore.Qt.CopyAction:
            e.acceptProposedAction()

    def dropEvent(self, e):
        if e.dropAction() == QtCore.Qt.CopyAction:
            quick_type = e.mimeData().text()
            job_item = JobItem(None, self.car)
            job_item.init_item(quick_type)
            ok = job_item.dialog_for_parameters()
            if ok:
                e.acceptProposedAction()
                self.add_job(job_item)
                self.context.log(self.car.name, "Add a job, " + quick_type + ", action: " + job_item.job.action.name +
                                 ", arg1: " + str(job_item.job.action.arg1) + ", arg2: " +
                                 str(job_item.job.action.arg2) + ", time: " + str(job_item.job.time))

    def contextMenuEvent(self, e):
        if len(self.selectedItems()) > 0:
            menu = QtGui.QMenu(self)

            delete_action = QtGui.QAction('Delete', self)
            delete_action.connect(delete_action, QtCore.SIGNAL('triggered()'), self.delete_job)
            menu.addAction(delete_action)

            edit_action = QtGui.QAction('Edit', self)
            edit_action.connect(edit_action, QtCore.SIGNAL('triggered()'), self.edit_job)
            menu.addAction(edit_action)

            info_action = QtGui.QAction('Info', self)
            info_action.connect(info_action, QtCore.SIGNAL('triggered()'), self.info)
            menu.addAction(info_action)

            menu.popup(QtGui.QCursor.pos())

    def delete_job(self):
        if len(self.selectedItems()) > 0:
            self.remove_job(self.selectedItems()[0])

    def edit_job(self):
        if len(self.selectedItems()) > 0:
            self.selectedItems()[0].dialog_for_parameters()

    def info(self):
        if len(self.selectedItems()) > 0:
            msg = self.selectedItems()[0].info()
            self.context.log(self.car.name, msg)


class TemplateWidget(QtGui.QLabel):
    def __init__(self, parent, quick_type=None):
        QtGui.QLabel.__init__(self, parent=parent)
        self.p = parent
        self.is_instance = False
        self.quick_type = quick_type
        self.job = None
        self.icon = None
        self.init_job()

    def init_job(self):
        self.setFixedSize(100, 100)

        self.setScaledContents(True)

        if self.quick_type == QTYPE_FORWARD:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, FORWARD_ARG1, FORWARD_ARG2, 0)
            self.setText('Up')
            self.setPixmap(QtGui.QPixmap(Res_Manager.get_path('up.png')))
        elif self.quick_type == QTYPE_BACKWARD:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, BACKWARD_ARG1, BACKWARD_ARG2, 0)
            self.setText('Down')
            self.setPixmap(QtGui.QPixmap(Res_Manager.get_path('down.png')))
        elif self.quick_type == QTYPE_LEFT:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, LEFT_ARG1, LEFT_ARG2, 0)
            self.setText('Left')
            self.setPixmap(QtGui.QPixmap(Res_Manager.get_path('left.png')))
        elif self.quick_type == QTYPE_RIGHT:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, RIGHT_ARG1, RIGHT_ARG2, 0)
            self.setText('Right')
            self.setPixmap(QtGui.QPixmap(Res_Manager.get_path('right.png')))
        elif self.quick_type == QTYPE_STOP:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, STOP_ARG1, STOP_ARG2, 0)
            self.setText('Stop')
            self.setPixmap(QtGui.QPixmap(Res_Manager.get_path('stop.png')))
        else:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, STOP_ARG1, STOP_ARG2, 0)
            self.setText('Customized')
            self.setPixmap(QtGui.QPixmap(Res_Manager.get_path('customized.png')))

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            mime_data = QtCore.QMimeData()
            mime_data.setText(self.quick_type)
            drag = QtGui.QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(e.pos())
            drag.exec_(QtCore.Qt.CopyAction)

    def contextMenuEvent(self, e):
        menu = QtGui.QMenu(self)
        if self.is_instance:
            delete_action = QtGui.QAction('Delete', self)
            delete_action.connect(delete_action, QtCore.SIGNAL('triggered()'), self.delete_self)
            menu.addAction(delete_action)

        menu.popup(QtGui.QCursor.pos())

    def set_time(self, time):
        self.job.time = time


class JobItem(QtGui.QListWidgetItem):
    def __init__(self, parent, car):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.p = parent
        self.car = car
        self.quick_type = None
        self.job = None

    def init_item(self, quick_type):
        self.quick_type = quick_type

        if self.quick_type == QTYPE_FORWARD:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, FORWARD_ARG1, FORWARD_ARG2, 0)
            self.setIcon(QtGui.QIcon(Res_Manager.get_path('up.png')))
        elif self.quick_type == QTYPE_BACKWARD:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, BACKWARD_ARG1, BACKWARD_ARG2, 0)
            self.setIcon(QtGui.QIcon(Res_Manager.get_path('down.png')))
        elif self.quick_type == QTYPE_LEFT:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, LEFT_ARG1, LEFT_ARG2, 0)
            self.setIcon(QtGui.QIcon(Res_Manager.get_path('left.png')))
        elif self.quick_type == QTYPE_RIGHT:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, RIGHT_ARG1, RIGHT_ARG2, 0)
            self.setIcon(QtGui.QIcon(Res_Manager.get_path('right.png')))
        elif self.quick_type == QTYPE_STOP:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, STOP_ARG1, STOP_ARG2, 0)
            self.setIcon(QtGui.QIcon(Res_Manager.get_path('stop.png')))
        else:
            self.job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 0, 0, 0)
            self.setIcon(QtGui.QIcon(Res_Manager.get_path('customized.png')))

        if self.quick_type:
            self.setText(self.quick_type)
        else:
            self.setText("customized")

    def info(self):
        info_str = "Batch Job info--" + \
                   "Action: " + self.job.action.name +\
                   ", Arg1: " + str(self.job.action.arg1) + \
                   ", Arg2: " + str(self.job.action.arg2) + \
                   ", Time: " + str(self.job.time)
        return info_str

    def dialog_for_parameters(self):
        if self.quick_type == QTYPE_FORWARD or self.quick_type == QTYPE_BACKWARD or self.quick_type == QTYPE_LEFT or \
                        self.quick_type == QTYPE_RIGHT or self.quick_type == QTYPE_STOP:
            time = JobDialog(self.p).get_time()
            if not time:
                return False
            else:
                self.job.time = float(time)
                self.setToolTip(self.info())
                return True
        else:
            result = JobDialog(self.p).get_time_and_action()
            if result:
                self.job.time = float(result[0])
                self.job.action.arg1 = int(result[1])
                self.job.action.arg2 = int(result[2])
                self.setToolTip(self.info())
                return True
            else:
                return False


class JobDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.WindowTitleHint | QtCore.Qt.Tool | QtCore.Qt.WindowCloseButtonHint)

        self.time_label = None
        self.time_text = None
        self.time_layout = None

        self.arg1_label = None
        self.arg1_text = None
        self.arg1_layout = None

        self.arg2_label = None
        self.arg2_text = None
        self.arg2_layout = None

        self.buttons = None
        self.cancel_button = None
        self.ok_button = None
        self.button_layout = None

        self.dialog_layout = QtGui.QVBoxLayout()
        self.setLayout(self.dialog_layout)

        self.time = None
        self.arg1 = None
        self.arg2 = None

        self.move(500, 500)

    def accept(self):
        feedback = True
        if self.time_text:
            self.time = self.time_text.text()
            if self.time == "":
                feedback = False
        if self.arg1_text:
            self.arg1 = self.arg1_text.text()
            if self.arg1 == "":
                feedback = False
        if self.arg2_text:
            self.arg2 = self.arg2_text.text()
            if self.arg2 == "":
                feedback = False
        if not feedback:
            QtGui.QDialog.reject(self)
        else:
            QtGui.QDialog.accept(self)

    def init_time(self):
        self.time_label = QtGui.QLabel('Time(s):', self)
        self.time_text = QtGui.QLineEdit(self)
        self.time_text.setValidator(QtGui.QDoubleValidator(self.time_text))
        self.time_layout = QtGui.QHBoxLayout()
        self.time_layout.addWidget(self.time_label)
        self.time_layout.addWidget(self.time_text)

    def init_action(self):
        self.arg1_label = QtGui.QLabel('Velocity(cm/s):', self)
        self.arg1_text = QtGui.QLineEdit(self)
        self.arg1_text.setValidator(QtGui.QIntValidator(self.arg1_text))
        self.arg1_layout = QtGui.QHBoxLayout()
        self.arg1_layout.addWidget(self.arg1_label)
        self.arg1_layout.addWidget(self.arg1_text)

        self.arg2_label = QtGui.QLabel('Angular Velocity(degree/s):', self)
        self.arg2_text = QtGui.QLineEdit(self)
        self.arg2_text.setValidator(QtGui.QIntValidator(self.arg2_text))
        self.arg2_layout = QtGui.QHBoxLayout()
        self.arg2_layout.addWidget(self.arg2_label)
        self.arg2_layout.addWidget(self.arg2_text)

    def init_button(self):
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_time(self):
        self.init_time()
        self.init_button()
        self.dialog_layout.addLayout(self.time_layout)
        self.dialog_layout.addWidget(self.buttons)
        if self.exec_():
            return self.time
        else:
            return None
        # return self.time
        # else:
        # return None

    def get_time_and_action(self):
        self.init_time()
        self.init_action()
        self.init_button()
        self.dialog_layout.addLayout(self.time_layout)
        self.dialog_layout.addLayout(self.arg1_layout)
        self.dialog_layout.addLayout(self.arg2_layout)
        self.dialog_layout.addWidget(self.buttons)
        if self.exec_():
            return [self.time, self.arg1, self.arg2]
        else:
            return None











