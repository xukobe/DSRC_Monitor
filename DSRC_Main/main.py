__author__ = 'xuepeng'

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from multiprocessing import Process
from DSRC_Messager_Module import Test_Tube
from DSRC_GUI import Console
# from USRP_Communication_Module import DSRC_USRP_Transceiver
import time

import signal


def test_tube():
    Test_Tube.main()


# def transceiver():
#     DSRC_USRP_Transceiver.main()


def console():
    Console.main()

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print "Not enough arguments!"
        exit()
    if args[1] == "simulation":
        p1 = Process(target=test_tube, args=())
        p2 = Process(target=console, args=())
    elif args[1] == "stationary":
        # p1 = Process(target=transceiver, args=())
        p2 = Process(target=console, args=())
    else:
        exit()
    p1.start()
    p2.start()
    while p2.is_alive():
        time.sleep(0.5)
    # os.kill(p1.pid, signal.SIGTERM)
    os.kill(p1.pid, signal.SIGUSR1)
    time.sleep(0.5)
    os.kill(p1.pid, signal.SIGTERM)