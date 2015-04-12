__author__ = 'xuepengxu'

import sys,os
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time

from Queue import Queue
from Event_Module.DSRC_Event import Event
from Event_Module import DSRC_Event
from DSRC_Messager_Module.DSRC_USRP_Connector import DsrcUSRPConnector, ConnectorInterface
from Event_Module.DSRC_Message_Coder import MessageCoder
from PyQt4 import QtGui, QtCore

RETX_TIMES = 5
SENDING_INTERVAL = 0.1

class Context(QtCore.QObject):

    def __init__(self):
        super(Context, self).__init__()
        self.connector = DsrcUSRPConnector()
        self.msg_handler = MessageHandler()
        self.sender = SendingHandler(self)
        self.connect(self.sender, self.sender.signal, self.message_received_by_vehicle)
        self.sender.start()
        self.connect(self.msg_handler, self.msg_handler.signal, self.event_handler)
        self.connect(self.msg_handler, self.msg_handler.signal, self.sender.remove_ack)
        self.msg_handler.start()
        self.connector.register_listener(self.msg_handler)
        self.log_signal = QtCore.SIGNAL('log(PyQt_PyObject)')
        self.connect(self, self.log_signal, self.write_to_log)
        self.map_height = 0
        self.map_width = 0
        self.FACTOR = 2
        self.source = 'monitor'
        self.batch_senders = []
        self.batch_sender = None

    def event_handler(self, event):
        # print event.type
        print "Not implemented"
        # raise NotImplementedError("Event handler not implemented!")

    def message_received_by_vehicle(self, message):
        print "Not implemented"

    def write_to_log(self, content):
        print "Not implement"

    def log(self, who, content):
        self.emit(self.log_signal, who + ": " + content)

    def send_msg(self, msg):
        # m = MessageCoder.encode(msg)
        # self.connector.send_to_USRP(m)
        self.sender.send(msg)

    def send_batch(self, source, destination, job_list):
        is_start = False
        size = len(self.batch_senders)
        for i in range(size):
            if not self.batch_senders[i].isRunning():
                self.batch_senders[i] = JobBatchSender(self, job_list, source, destination)
                self.batch_senders[i].start()
                is_start = True
                break
        if not is_start:
            self.batch_sender = JobBatchSender(self, job_list, source, destination)
            self.batch_senders.append(self.batch_sender)
            self.batch_sender.start()

    def stop_self(self):
        self.sender.stop_self()
        self.connector.stop_self()
        self.msg_handler.stop_self()

    def register_event_listener(self, listener):
        self.msg_handler.register_event_listener(listener)


class MessageItem:
    def __init__(self, message, max_times, seq):
        self.sequence = seq
        self.message = message
        self.times = 0
        self.max_times = max_times


class SendingHandler(QtCore.QThread):
    def __init__(self, context):
        QtCore.QThread.__init__(self)
        self.signal = QtCore.SIGNAL('ack_event(PyQt_PyObject)')
        self.sending_queue = Queue()
        self.seq_to_remove = []
        self.running = True
        self.context = context
        self.seq = 0

    def send(self, msg_obj):
        msg_obj['seq'] = self.seq
        m_item = MessageItem(msg_obj, RETX_TIMES, self.seq)
        self.seq += 2
        self.sending_queue.put(m_item)

    def remove_ack(self, event):
        if event.type == DSRC_Event.TYPE_MONITOR_CAR:
            if event.sub_type == DSRC_Event.SUBTYPE_ACK:
                seq = event.seq - 1
                self.seq_to_remove.append(seq)

    def run(self):
        while self.running:
            m_item = self.sending_queue.get()
            if m_item.sequence == -1:
                break
            elif m_item.sequence in self.seq_to_remove:
                self.emit(self.signal, m_item.message)
                continue
            try:
                msg = MessageCoder.encode(m_item.message)
                self.context.connector.send_to_USRP(msg)
                m_item.times += 1
                if m_item.times >= m_item.max_times:
                    self.seq_to_remove.append(m_item.sequence)
                self.sending_queue.put(m_item)
            except Exception, e:
                self.context.log("Context", e.message)
            time.sleep(SENDING_INTERVAL)


    def stop_self(self):
        self.sending_queue.put_nowait(MessageItem(None, 0, -1))


class EventListener:

    def __init__(self):
        pass

    def event_handler(self, event):
        raise NotImplementedError('Not implemented!')


class MessageHandler(QtCore.QThread, ConnectorInterface):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.signal = QtCore.SIGNAL('hand_event(PyQt_PyObject)')
        self.event_queue = Queue()
        self.event_handler = None
        self.running = True

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
                self.emit(self.signal, event)
            except ValueError, e:
                pass
            except KeyError, e:
                pass
        print "Event handler is stopped!"

    def register_event_listener(self, listener):
        self.event_handler = listener

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
            # event = Plugin.customized_generate_event()
            # event.set_origin_msg(event_obj)
            # event.self_parse()
            pass

        if event:
            event.source = event_obj['source']
            event.destination = event_obj['destination']
            event.type = event_obj['type']
        return event


class EventSimpleHandler(EventListener):

    def __init__(self):
        pass

    def event_handler(self, event):
        print "Not implement"


class JobBatchSender(QtCore.QThread):
    def __init__(self, context, job_list, source, destination):
        QtCore.QThread.__init__(self)
        self.job_list = job_list
        self.context = context
        self.source = source
        self.destination = destination

    def run(self):
        for job in self.job_list:
            msg = MessageCoder.generate_batch_processing(self.source, self.destination, job)
            self.context.send_msg(msg)
            time.sleep(0.1)


def main():
    context = Context()
    # context.register_event_listener(EventSimpleHandler())
    # context.event_generator.connect_to_event_signal(event_handler)
    while True:
        a = raw_input("Enter:")
        if a == 'quit':
            context.stop_self()
            exit()
        else:
            context.send_msg(a)

if __name__ == '__main__':
    main()


