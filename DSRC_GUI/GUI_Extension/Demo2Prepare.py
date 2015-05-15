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
    console.log("Demo2", "Car number:" + str(len(cars)))
    if len(cars) < 2:
        console.log("Demo2", "At least two cars are needed!")
        return
    # car1 = cars[0]
    # car2 = cars[1]
    # console.log("Demo1", "Car1 name:" + car1.name)
    # # console.log("Demo1", "Car2 name:" + car2.name)
    # car1.set_pos(100, 150, math.pi/2)
    # car2.set_pos(50, 50, math.pi/2)
    # car1.to_free()
    # time.sleep(0.1)
    # car2.to_customized()
    # time.sleep(0.1)
    # car2.use_plugin('lane')
    # time.sleep(0.1)
    # console.log('Demo1', 'Working')

    # args0 = [100, 120, 90]
    # args1 = [50, 20, 90]
    #
    # msg0 = generate_auto_set_up_message(console.source, cars[0].name, args0)
    # console.send_msg(msg0)
    #
    # msg1 = generate_auto_set_up_message(console.source, cars[1].name, args1)
    # console.send_msg(msg1)

    # time.sleep(0.5)
    #
    # diff = (math.pi/2 - cars[0].coordinate[2])%(2*math.pi)
    # rotate_speed = 90
    # if diff > math.pi:
    #     diff = 360 - diff
    #     rotate_speed = -90
    #
    # time = abs(diff/float(rotate_speed))
    #
    # job0 = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 0, rotate_speed, time)
    # msg = DSRC_Message_Coder.MessageCoder.generate_batch_processing(console.source, cars[0].name, job0)
    # console.send_msg(msg)
    #
    # diff = (math.pi/2 - cars[1].coordinate[2])%(2*math.pi)
    # rotate_speed = 90
    # if diff > math.pi:
    #     diff = 360 - diff
    #     rotate_speed = -90
    #
    # time = abs(diff/float(rotate_speed))
    #
    # job0 = DSRC_Event.EventJob(DSRC_Event.ACTION_NAME_GO, 0, rotate_speed, time)
    # msg = DSRC_Message_Coder.MessageCoder.generate_batch_processing(console.source, cars[0].name, job0)
    # console.send_msg(msg)


    # cars[0].set_pos(100, 120, math.pi/2)
    # cars[1].set_pos(50, 20, math.pi/2)

    cars[0].to_customized()
    cars[0].use_plugin('snakemove')

    cars[1].to_customized()
    cars[1].use_plugin('lane')

    args0 = [120, 50, 0]
    args1 = [20, 100, 0]

    msg0 = generate_auto_set_up_message(console.source, cars[0].name, args0)
    console.send_msg(msg0)

    msg1 = generate_auto_set_up_message(console.source, cars[1].name, args1)
    console.send_msg(msg1)

    # msg = generate_snakemove_message(console.source, cars[0].name, True)
    # console.send_msg(msg)


def generate_snakemove_message(source, destination, snakemove):
    msg_obj = {}
    msg_obj[DSRC_Event.KEY_SOURCE] = source
    msg_obj[DSRC_Event.KEY_DESTINATION] = destination
    msg_obj[DSRC_Event.KEY_TYPE] = DSRC_Event.TYPE_CUSTOMIZED
    msg_obj[DSRC_Event.KEY_SUBTYPE] = 'snakemove'
    msg_obj["do"] = snakemove
    # msg = MessageCoder.encode(msg_obj)
    return msg_obj


def generate_auto_set_up_message(source, destination, args):
    msg_obj = {}
    msg_obj[DSRC_Event.KEY_SOURCE] = source
    msg_obj[DSRC_Event.KEY_DESTINATION] = destination
    msg_obj[DSRC_Event.KEY_TYPE] = DSRC_Event.TYPE_CUSTOMIZED
    msg_obj[DSRC_Event.KEY_SUBTYPE] = "auto_setup"
    msg_obj["x"] = args[0]
    msg_obj["y"] = args[1]
    msg_obj["r"] = args[2]
    # msg = MessageCoder.encode(msg_obj)
    return msg_obj
