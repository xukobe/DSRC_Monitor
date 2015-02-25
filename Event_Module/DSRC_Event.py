__author__ = 'xuepeng'


################Destination##################
DESTINATION_ALL = "all"

####################Type#####################
TYPE_MONITOR_CAR = "monitor_car"
TYPE_CAR_CAR = "car_car"
TYPE_CUSTOMIZED = "customized"

################Monitor_Car##################
SETTINGS_NAME_STYLE = "style"
SETTINGS_NAME_STYLE_FOLLOW = "follow"
SETTINGS_NAME_STYLE_LEAD = "lead"
SETTINGS_NAME_STYLE_FREE = "free"

COMMAND_NAME_SAFE_MODE = "safe_mode"
COMMAND_NAME_FULL_MODE = "full_mode"
COMMAND_NAME_RESTART = "restart"
COMMAND_NAME_SHUT_DOWN = "shutdown"

BATCH_FLOW_START = "start"
BATCH_FLOW_JOB = "job"
BATCH_FLOW_END = "end"
BATCH_JOB_ACTION_NAME_GO = "go"
BATCH_JOB_ACTION_NAME_PAUSE = "pause"

#################Car_Car#####################
ACTION_NAME_GO = "go"
ACTION_NAME_PAUSE = "pause"

class EventAction:
    def __init__(self):
        self.name = None
        self.arg1 = None
        self.arg2 = None

    def set_name(self, name):
        self.name = name

    def set_arg1(self, arg1):
        self.arg1 = arg1

    def set_arg2(self, arg2):
        self.arg2 = arg2


class EventCoordinates:
    def __init__(self):
        self.x = None
        self.y = None
        self.radian = None

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_radian(self, radian):
        self.radian = radian


class EventJob:
    def __init__(self):
        self.action = None
        self.time = 0

    def set_action(self, action):
        """
        :param action: Event action
        :type action: EventAction
        """
        self.action = action

    def set_time(self, time):
        self.time = time


class Event:
    def __init__(self):
        self.source = None
        self.destination = None
        self.type = None
        self.msg_obj = None

    def set_origin_msg(self, msg_obj):
        self.msg_obj = msg_obj

    def set_source(self, source):
        self.source = source

    def set_destination(self, destination):
        self.destination = destination

    def set_type(self, type):
        self.type = type

    def self_parse(self):
        raise "Not implemented!"


class Car_CarEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.action = None
        self.coordinates = None

    def set_action(self, action):
        """
        :param action: car_car action
        """
        self.action = action

    def set_coor(self, coor):
        """
        :param coor: car_car coor
        """
        self.coordinates = coor

    def self_parse(self):
        if self.msg_obj:
            car_car_obj = self.msg_obj[TYPE_CAR_CAR]
            action_event = car_car_obj['action']
            coor_event = car_car_obj['coor']
            action = EventAction()
            coor = EventCoordinates()
            action.set_name(action_event['name'])
            action.set_arg1(action_event['arg1'])
            action.set_arg2(action_event['arg2'])
            coor.set_x(coor_event['x'])
            coor.set_y(coor_event['y'])
            coor.set_radian(coor_event['radian'])
            self.set_action(action)
            self.set_coor(coor)


class Monitor_CarEvent(Event):
    def __init__(self):
        Event.__init__(self)

    def self_parse(self):
        print "Monitor_car event parse!"

class EventGenerator:
    def __init__(self):
        self.listener = None

    def set_listener(self, listener):
        """
        :type listener: EventListener
        """
        self.listener = listener

class EventListener:
    def __init__(self):
        pass

    def usrp_event_received(self, event):
        raise NotImplementedError( "USRP event listener is not implemented." )

    def irobot_event_received(self,event):
        raise NotImplementedError("iRobot event listener is not implemented")
