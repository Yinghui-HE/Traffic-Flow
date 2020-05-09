from Road import Road
from TrafficLight import TrafficLight
import numpy as np

np.set_printoptions(precision=5)
graph_list = []


def advance_all_roads(list_of_roads):
    for road in list_of_roads:
        road.advance()

def traffic_simulation():
    cycle_time_len = 180
    traffic_light_1 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_1_left = TrafficLight(green_light_time_len=30, red_light_time_len=cycle_time_len-60)
    traffic_light_2 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_3 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_4 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_5 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_always_green =  TrafficLight(green_light_time_len=cycle_time_len, red_light_time_len=0, is_green=True)
    list_of_traffic_lights = [traffic_light_1, traffic_light_2, traffic_light_3, traffic_light_4, traffic_light_5]

    road_a = Road(name="A", num_cars=20, road_length=572, traffic_light=traffic_light_always_green)
    road_b = Road(name="B", num_cars=10, road_length=414, traffic_light=traffic_light_1,
                  traffic_light_left=traffic_light_1_left)
    road_c = Road(name="C", num_cars=4, road_length=631, traffic_light=traffic_light_4, in_rate=0.9)
    road_d = Road(name="D", num_cars=15, road_length=572, traffic_light=traffic_light_2, in_rate=0.2)
    road_e = Road(name="E", num_cars=8, road_length=414, traffic_light=traffic_light_5)
    road_f = Road(name="F", num_cars=18, road_length=631, traffic_light=traffic_light_always_green)
    road_g = Road(name="G", num_cars=13, road_length=643, traffic_light=traffic_light_always_green)
    road_h = Road(name="H", num_cars=6, road_length=643, in_rate=0.3, traffic_light=traffic_light_3)
    list_of_roads = [road_a, road_b, road_c, road_d, road_e, road_f, road_g, road_h]

    list_of_end_roads = [road_a, road_f, road_g]  # cars will only leave the box freely on those roads; to calculate
                                                        # num cars leave
    road_b.set_next_roads([road_a, road_g])
    road_c.set_next_roads([road_b])
    road_d.set_next_roads([road_e, road_g])
    road_e.set_next_roads([road_f])
    road_h.set_next_roads([road_a, road_e])

    time_length = 80  # 30 minutes = 1800 seconds
    cycle = [[traffic_light_3],
             [traffic_light_1, traffic_light_1_left],
             [traffic_light_1, traffic_light_2]]
    for time in range(1, time_length, cycle_time_len):
        # in a cycle: 1. tl3; 2. tl1 & tl1_left; 3. tl1, tl2
        # time for turning green for tl4 & tl5 can be changed
        curr_time = time
        # 1.
        traffic_light_3.turn_green()
        for time_step in range(curr_time, curr_time+traffic_light_3.green_light_time_len):
            advance_all_roads(list_of_roads)
            print_graph_list(road_a.num_cars, road_b.num_cars, road_c.num_cars, road_d.num_cars, road_e.num_cars,
                             road_f.num_cars, "| " + str(road_g.num_cars)+" | " + str(road_h.num_cars) + " |")
            print()




def print_graph_list(a="   A  ", b="   B  ", c="   C  ", d="  D   ", e="   E  ", f="   F  ", gh = "|  G  |  H  |"):
    global graph_list
    graph_list = np.array([["——————", "—————————————", "——————", "——————", "——————"],
                  [a, "             ", b, "      ", c],
                  ["------", "             ", "------", "------", "------"],
                  [d, "             ", e, "      ", f],
                  ["——————", "             ", "——————", "——————", "——————"],
                  ["      ", "|     |     |", "      ", "      ", "      "],
                  ["      ", "|     |     |", "      ", "      ", "      "],
                  ["      ", "|     |     |", "      ", "      ", "      "],
                  ["      ", gh, "      ", "      ", "      "],
                  ["      ", "|     |     |", "      ", "      ", "      "],
                  ["      ", "|     |     |", "      ", "      ", "      "],
                  ["      ", "|     |     |", "      ", "      ", "      "],])
    print(graph_list)

def main():
    print("The beginning of traffic simulation")
    print_graph_list()
    traffic_simulation()


main()