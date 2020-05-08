import math
import numpy as np


class Road(object):
    U_MAX = 35 # speed limit is 35 mph
    CAR_LENGTH = 20 # unit: ft
    CONST_C = 1 # can change later

    def __init__(self, name, num_cars, road_length, in_rate=0):
        self.name = name
        self.road_length = road_length # unit: ft
        self.p = num_cars / road_length # density
        self.num_cars = num_cars
        self.is_entrance = in_rate != 0
        self.in_rate = in_rate # unit: number of cars per minute
        self.u = 0
        self.p_max = road_length / Road.CAR_LENGTH
        self.p_c = self.p_max * (math.exp(-1 * Road.U_MAX / Road.CONST_C))
        self.num_cars_leaving = 0

    def update_density_p(self):
        self.p = self.num_cars / self.road_length
        self.calculate_velocity_u()

    def calculate_velocity_u(self):
        if self.p < self.p_c:
            self.u = Road.U_MAX
        else:
            self.u = -1 * Road.CONST_C * np.log(self.p / self.p_max)

    def cars_in(self, num_cars_in):
        self.num_cars += num_cars_in
        self.update_density_p()

    def cars_out(self, num_cars_out):
        if num_cars_out > self.num_cars: # error checking
            print("number cars leaving the road is larger than the number of cars originally on that road")
            return
        self.num_cars -= num_cars_out
        self.update_density_p()

    def __str__(self):
        msg = "Road " + self.name
        return msg
