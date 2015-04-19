__author__ = 'xuepeng'


import math
import time
from Event_Module import DSRC_Event, DSRC_Message_Coder


# Must implement
def execute(console):
    cars = []
    for car_name in console.cars:
        car = console.cars[car_name]
        cars.append(car)
    console.log("Demo3", "Car number:" + str(len(cars)))
    if len(cars) < 2:
        console.log("Demo3", "At least two cars are needed!")
        return

    job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 30, 0, 8)
    msg = DSRC_Message_Coder.MessageCoder.generate_batch_processing(console.source, cars[0].name, job)
    console.send_msg(msg)

    job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 30, 0, 8)
    msg = DSRC_Message_Coder.MessageCoder.generate_batch_processing(console.source, cars[1].name, job)
    console.send_msg(msg)
