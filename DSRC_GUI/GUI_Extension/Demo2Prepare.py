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
    cars[0].set_pos(100, 100, math.pi/2)
    cars[1].set_pos(50, 20, math.pi/2)

    cars[0].to_customized()
    cars[0].use_plugin('snakemove')

    cars[1].to_customized()
    cars[1].use_plugin('lane')

    # msg = generate_snakemove_message(console.source, cars[0].name, True)
    # console.send_msg(msg)


def generate_snakemove_message(source, destination, snakemove):
    msg_obj = {}
    msg_obj[DSRC_Event.KEY_SOURCE] = source
    msg_obj[DSRC_Event.KEY_DESTINATION] = destination
    msg_obj[DSRC_Event.KEY_TYPE] = DSRC_Event.TYPE_CUSTOMIZED
    msg_obj["do"] = snakemove
    # msg = MessageCoder.encode(msg_obj)
    return msg_obj

