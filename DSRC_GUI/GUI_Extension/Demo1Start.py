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
    console.log("Demo1", "Car number:" + str(len(cars)))
    if len(cars) < 2:
        console.log("Demo1", "At least two cars are needed!")
        return

    # job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 30, 0, 8)
    # msg = DSRC_Message_Coder.MessageCoder.generate_batch_processing(console.source, cars[0].name, job)
    # console.send_msg(msg)
    #
    # job = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 30, 0, 8)
    # msg = DSRC_Message_Coder.MessageCoder.generate_batch_processing(console.source, cars[1].name, job)
    # console.send_msg(msg)

    msg = generate_automove_message(console.source, cars[0].name, True)
    console.send_msg(msg)

    msg = generate_automove_message(console.source, cars[1].name, True)
    console.send_msg(msg)



def generate_automove_message(source, destination, automove):
    msg_obj = {}
    msg_obj[DSRC_Event.KEY_SOURCE] = source
    msg_obj[DSRC_Event.KEY_DESTINATION] = destination
    msg_obj[DSRC_Event.KEY_TYPE] = DSRC_Event.TYPE_CUSTOMIZED
    msg_obj[DSRC_Event.KEY_SUBTYPE] = 'automove'
    msg_obj["do"] = automove
    # msg = MessageCoder.encode(msg_obj)
    return msg_obj