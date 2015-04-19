__author__ = 'xuepeng'

import math
import time

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
    car1 = cars[0]
    car2 = cars[1]
    console.log("Demo1", "Car1 name:" + car1.name)
    # console.log("Demo1", "Car2 name:" + car2.name)
    car1.set_pos(100, 150, math.pi/2)
    car2.set_pos(100, 50, math.pi/2)
    car1.to_free()
    time.sleep(0.1)
    car2.to_follow()
    time.sleep(0.1)
    car2.set_follow_target(car1.name)
    console.log('Demo1', 'Working')
