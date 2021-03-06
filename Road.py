import math
import numpy as np
import decimal
from TrafficLight import TrafficLight


# Road class
class Road(object):
    U_MAX = 51.33  # speed limit: 35 miles per hours = 51.33 ft per seconds
    CAR_LENGTH = 20  # unit: ft
    CONST_C = 10  # can change later
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
            # 70% cars will go straight, and the rest 30% will turn left or right
            self.probability_first_next_road = 0.7
        self.list_of_num_cars_out = []
        self.density_list = []
        self.velocity_list = []

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

    def linear_acceleration(self, curr_time, traffic_light_green_time):
        time = curr_time - traffic_light_green_time
        # 11.48 ft per seconds = 3.5 m/s^2. Citation: https://hypertextbook.com/facts/2001/MeredithBarricella.shtml
        return time * 11.48

    def calculate_curr_velocity(self, curr_time, traffic_light_green_time, next_road_density_p, next_road_p_c):
        curr_acceleration = self.linear_acceleration(curr_time, traffic_light_green_time)
        possible_max = self.calculate_velocity_u(next_road_density_p, next_road_p_c)
        if self.u + curr_acceleration < possible_max:
            self.u += curr_acceleration
        else:
            self.u = possible_max

    def cars_in(self, num_cars_in):
        self.num_cars = min(round(self.num_cars + num_cars_in, 2), self.NUM_CARS_MAX)
        self.update_density_p()

    def cars_out(self, num_cars_out):
        if num_cars_out > self.num_cars:  # error checking
            num_cars_out = self.num_cars
        self.num_cars = round(self.num_cars - num_cars_out, 2)
        self.update_density_p()

    def calculate_num_cars_out(self, next_road, probability_choosing_road):
        next_road_velocity_u = Road.U_MAX
        next_road_spaces_for_more_cars = 1000000000
        if next_road is not None:
            next_road_velocity_u = self.calculate_velocity_u(next_road.get_density_p(), Road.P_C)
            next_road_spaces_for_more_cars = next_road.calculate_spaces_for_more_cars()

        num_cars_could_leave_per_second = (next_road_velocity_u / Road.CAR_LENGTH) * probability_choosing_road
        num_cars_out = round(min(next_road_spaces_for_more_cars, num_cars_could_leave_per_second, self.num_cars), 2)
        return num_cars_out

    def advance(self):
        if self.traffic_light.is_green:
            if len(self.list_of_next_roads) == 0:
                # end road, cars freely go out of the system
                self.density_list.append(self.p)
                self.velocity_list.append(self.u)
                num_cars_out = self.calculate_num_cars_out(next_road=None, probability_choosing_road=1)
                self.cars_out(num_cars_out)
                self.list_of_num_cars_out.append(num_cars_out)
                return
            elif len(self.list_of_next_roads) == 1:
                # if only one next road, probability = 1
                next_road = self.list_of_next_roads[0]
                num_cars_out = self.calculate_num_cars_out(next_road=next_road, probability_choosing_road=1)
                self.cars_out(num_cars_out)
                next_road.cars_in(num_cars_out)
            else:
                # have two next roads, probability
                if (self.traffic_light_left is None) \
                        or ((self.traffic_light_left is not None) and (self.traffic_light_left.is_green)):
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
        self.density_list.append(self.p)
        self.velocity_list.append(self.u)

    def __str__(self):
        msg = "Road " + self.name + "Info" \
              + "\n\tNum of Cars: " + str(self.num_cars)
        return msg
