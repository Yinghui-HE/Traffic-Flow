import math
import numpy as np
import decimal

from TrafficLight import TrafficLight


class Road(object):
    U_MAX = 51.33  # speed limit: 35 miles per hours = 51.33 ft per seconds
    CAR_LENGTH = 20  # unit: ft
    CONST_C = 10000  # can change later
    P_MAX = 1 / CAR_LENGTH
    P_C = P_MAX * (math.exp(-1 * U_MAX / CONST_C))

    def __init__(self, name, num_cars, road_length, traffic_light, traffic_light_left=None, in_rate=0):
        self.name = name
        self.num_cars = num_cars
        self.road_length = road_length  # unit: ft
        self.traffic_light = traffic_light
        self.traffic_light_left = traffic_light_left
        self.in_rate = in_rate  # unit: number of cars per seconds

        self.NUM_CARS_MAX = road_length / Road.CAR_LENGTH
        self.p = num_cars / road_length  # density
        self.is_entrance = in_rate != 0
        self.u = 0
        self.num_cars_leaving = 0
        self.list_of_next_roads = []  # if 2 next roads, the order is: 1. next straight 2. turn
        if self.name == "H":
            # equal probability of turning left or turning right
            self.probability_first_next_road = 0.5
        else:
            # 90% cars will go straight, and the rest 10% will turn left or right
            self.probability_first_next_road = 0.9
        self.list_of_num_cars_out = []

    # return num of cars could still entering that road
    def calculate_spaces_for_more_cars(self):
        return self.NUM_CARS_MAX - self.num_cars

    def set_next_roads(self, list_of_next_roads):
        self.list_of_next_roads = list_of_next_roads

    def update_density_p(self):
        self.p = self.num_cars / self.road_length

    def get_velocity_u(self):
        return self.u

    def get_density_p(self):
        return self.p

    def calculate_velocity_u(self, next_road_density_p, next_road_p_c):
        if next_road_density_p < next_road_p_c:
            self.u = Road.U_MAX
        else:
            self.u = -1 * Road.CONST_C * np.log(next_road_density_p / Road.P_MAX)
        return self.u

    def cars_in(self, num_cars_in):
        self.num_cars = round(self.num_cars + num_cars_in, 2)
        self.update_density_p()

    def cars_out(self, num_cars_out):
        if num_cars_out > self.num_cars:  # error checking
            print("number cars leaving the road is larger than the number of cars originally on that road")
            return
        self.num_cars = round(self.num_cars - num_cars_out, 2)
        self.update_density_p()

    def calculate_num_cars_out(self, next_road, probability_choosing_road):
        next_road_velocity_u = Road.U_MAX
        next_road_spaces_for_more_cars = 100000
        if next_road is not None:
            next_road_velocity_u = self.calculate_velocity_u(next_road.get_density_p(), Road.P_C)
            next_road_spaces_for_more_cars = next_road.calculate_spaces_for_more_cars()

        num_cars_could_leave_per_second = (next_road_velocity_u / Road.CAR_LENGTH) * probability_choosing_road
        num_cars_out = round(min(next_road_spaces_for_more_cars, num_cars_could_leave_per_second, self.num_cars), 2)
        print(num_cars_out)
        return num_cars_out

    def advance(self):
        if not self.traffic_light.is_green:
            # certain cars entering the road with in_rate
            self.cars_in(self.in_rate)
            return

        if len(self.list_of_next_roads) == 0:
            # end road, cars freely go out of the system
            num_cars_out = self.calculate_num_cars_out(next_road=None, probability_choosing_road=1)
            self.cars_out(num_cars_out)
            self.list_of_num_cars_out.append(num_cars_out)
        elif len(self.list_of_next_roads) == 1:
            # if only one next road, probability = 1
            next_road = self.list_of_next_roads[0]
            num_cars_out = self.calculate_num_cars_out(next_road=next_road, probability_choosing_road=1)
            self.cars_out(num_cars_out)
            next_road.cars_in(num_cars_out)
        else:
            # have two next roads, probability
            if (self.traffic_light_left is None) \
                    or ((self.traffic_light_left is not None) and (self.traffic_light_left.is_green())):
                next_road_1 = self.list_of_next_roads[0]
                num_cars_out_1 = self.calculate_num_cars_out(
                    next_road=next_road_1, probability_choosing_road=self.probability_first_next_road)
                next_road_2 = self.list_of_next_roads[1]
                num_cars_out_2 = self.calculate_num_cars_out(
                    next_road=next_road_2, probability_choosing_road=1 - self.probability_first_next_road)
                self.cars_out(num_cars_out_1 + num_cars_out_2)
                next_road_1.cars_in(num_cars_out_1)
                next_road_2.cars_in(num_cars_out_2)
            else:
                # go straight only (turn left traffic light is red)
                next_road = self.list_of_next_roads[0]
                num_cars_out = self.calculate_num_cars_out(next_road=next_road,
                                                           probability_choosing_road=self.probability_first_next_road)
                self.cars_out(num_cars_out)
                next_road.cars_in(num_cars_out)

        self.cars_in(round(self.in_rate, 2))  # unit: num cars per second

    def __str__(self):
        msg = "Road " + self.name + "Info" \
              + "\n\tNum of Cars: " + str(self.num_cars)
        return msg
