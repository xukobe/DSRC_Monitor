__author__ = 'xuepeng'

import threading
import socket
import sys, os
import math
import random
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from DSRC_Messenger import SocketClient
from DSRC_Messenger import SocketServer
from Event_Module import DSRC_Message_Coder

client = None

def test_server():
    tss = SocketServer(_server_callback)
    tss.start()
    #threading._start_new_thread(tss.run,())
    while True:
        msg = raw_input("Please type some words:")
        client.send(msg)


def _server_callback(coming_socket):
    global client
    client_socket = coming_socket
    client = SocketClient(_recv_callback,client_socket)
    client.run()

def _recv_callback(msg):
    message = msg.replace("\n", "")
    print message

def test_client():
    client = SocketClient(_recv_callback)
    client.connect('127.0.0.1',10123)
    threading._start_new_thread(client.run,())
    while True:
        msg = raw_input("Please type some words:")
        client.send(msg)

def test_monitor():
    tss = SocketServer(_server_callback)
    tss.start()
    #threading._start_new_thread(tss.run,())
    radian = 0
    while True:
        a = raw_input("Enter:")
        if a == 'quit':
            tss.stop_self()
            break
        x = random.randint(0, 800)
        y = random.randint(0, 800)
        radian = random.random() * math.pi*2
        # radian = radian + math.pi/2
        msg = DSRC_Message_Coder.MessageCoder.generate_car_car_message("car1", "monitor", "go", 20, 30, x, y, radian)
        client.send(msg)

if __name__ =="__main__":
    if len(sys.argv) < 2:
        print "Usage: test_trafficsocket client/server"
        quit()
    choice = sys.argv[1]
    if choice == 'client':
        test_client()
    elif choice == 'server':
        test_server()
    elif choice == 'monitor':
        test_monitor()