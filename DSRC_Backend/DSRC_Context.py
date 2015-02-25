__author__ = 'xuepengxu'

import sys,os
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Queue import Queue
from Event_Module.DSRC_Event import Event
from Event_Module import DSRC_Event
from DSRC_Messager_Module.DSRC_USRP_Connector import DsrcUSRPConnector, ConnectorInterface
from Event_Module.DSRC_Message_Coder import MessageCoder
from PyQt4 import QtGui, QtCore


class Context:
    def __init__(self):
        self.connector = DsrcUSRPConnector()
        self.event_generator = EventGenerator()
        self.event_generator.connect_to_event_signal(event_handler)
        self.connector.register_listener(self.event_generator)

    def event_handler(self, event):
        print "Not implemented"
        # raise NotImplementedError("Event handler not implemented!")

    def send_msg(self, msg):
        self.connector.send_to_USRP(msg)

    def stop_self(self):
        self.connector.stop_self()
        self.event_generator.stop_self()

class EventGenerator(QtCore.QObject, Thread, ConnectorInterface):
    event_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QObject.__init__(self)
        Thread.__init__(self)
        self.event_queue = Queue()
        self.running = True
        self.start()

    def msg_received(self, msg):
        self.event_queue.put(msg)

    def run(self):
        while self.running:
            event_msg = self.event_queue.get()
            if event_msg == "QUIT":
                break
            try:
                event_obj = MessageCoder.decode(event_msg)
                event = self.parse_event(event_obj)
                self.event_signal.emit(event)
            except ValueError, e:
                pass
        print "Event handler is stopped!"

    def connect_to_event_signal(self, function):
        self.event_signal.connect(function)

    def stop_self(self):
        self.event_queue.put_nowait("QUIT")
        self.running = False

    def parse_event(self, event_obj):
        """
        :rtype : Event
        :param event_obj: event object to parse
        :type event_obj: dict
        """
        event = None

        if event_obj["type"] == DSRC_Event.TYPE_CAR_CAR:
            event = DSRC_Event.Car_CarEvent()
            event.set_origin_msg(event_obj)
            event.self_parse()
        elif event_obj["type"] == DSRC_Event.TYPE_MONITOR_CAR:
            event = DSRC_Event.Monitor_CarEvent()
            event.set_origin_msg(event_obj)
            event.self_parse()
        elif event_obj["type"] == DSRC_Event.TYPE_CUSTOMIZED:
            if self.customized_event:
                # event = Plugin.customized_generate_event()
                # event.set_origin_msg(event_obj)
                # event.self_parse()
                pass

        if event:
            event.source = event_obj['source']
            event.destination = event_obj['destination']
            event.type = event_obj['type']

        return event

def event_handler(event):
    print event.source


def main():
    context = Context()
    while True:
        a = raw_input("Enter:")
        if a == 'quit':
            context.stop_self()
            exit()
        else:
            context.send_msg(a)

if __name__ == '__main__':
    main()


