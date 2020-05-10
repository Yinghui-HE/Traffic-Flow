from Road import Road
from TrafficLight import TrafficLight
import numpy as np

np.set_printoptions(linewidth=200)
graph_list = []


def advance_all_roads(list_of_roads):
    for road in list_of_roads:
        road.advance()

def traffic_simulation():
    all_red_time_len = 30
    traffic_light_3 = TrafficLight(name="3", green_light_time_len=30, start_green_time_in_cycle=0)
    traffic_light_1 = TrafficLight(name="1", green_light_time_len=60, start_green_time_in_cycle=traffic_light_3.end_green_time_in_cycle)
    traffic_light_1_left = TrafficLight(name="1 Left", green_light_time_len=30, start_green_time_in_cycle=traffic_light_3.end_green_time_in_cycle)
    traffic_light_2 = TrafficLight(name="2", green_light_time_len=30, start_green_time_in_cycle=traffic_light_1_left.end_green_time_in_cycle)
    cycle_time_len = traffic_light_2.end_green_time_in_cycle + all_red_time_len

    traffic_light_4 = TrafficLight(name="4", green_light_time_len=60, start_green_time_in_cycle=0)
    traffic_light_5 = TrafficLight(name="5", green_light_time_len=60, start_green_time_in_cycle=0)

    traffic_light_always_green = TrafficLight(name="always green", green_light_time_len=cycle_time_len, start_green_time_in_cycle=0, is_green=True)
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

    time_length = 120  # 30 minutes = 1800 seconds
    cycle = [[traffic_light_3],
             [traffic_light_1, traffic_light_1_left],
             [traffic_light_1, traffic_light_2]]
    print_graph_list(list_of_traffic_lights, list_of_roads)
    for time in range(1, time_length, cycle_time_len):
        # in a cycle: 1. tl3; 2. tl1 & tl1_left; 3. tl1, tl2
        # time for turning green for tl4 & tl5 can be changed
        curr_time = time
        for curr_time in range(0, cycle_time_len):
            for traffic_light in list_of_traffic_lights:
                traffic_light.update_status(curr_time)
            advance_all_roads(list_of_roads)
            print_graph_list(list_of_traffic_lights, list_of_roads)
            print()


def print_graph_list(list_of_traffic_lights=None, list_roads=None):
    list_roads_str = ["    A   ", "    B   ", "    C   ", "   D    ", "    E   ", "    F   ", "|        |        |"]
    list_traffic_lights_str = ["1: red".ljust(8), "2: red".ljust(8), "3: red".ljust(8), "4: red".ljust(8), "5: red".ljust(8)]
    if list_roads is not None:
        list_roads_str = []
        for i in range(len(list_roads)-2):
            list_roads_str.append((list_roads[i].name + ": " + str(list_roads[i].num_cars)).ljust(8))
        list_roads_str.append(("| " + str(list_roads[6].num_cars).ljust(6) + " | " + str(list_roads[7].num_cars).ljust(6) + " |"))

    if list_of_traffic_lights is not None:
        list_traffic_lights_str = []
        for traffic_light in list_of_traffic_lights:
            list_traffic_lights_str.append(traffic_light.get_status().ljust(8))

    global graph_list
    box_8 = "—" * 8
    box_19 = "—" * 19

    spaces_2 = " " * 2
    spaces_7 = " " * 7
    spaces_8 = " " * 8
    spaces_9 = " " * 9
    spaces_19 = " " * 19

    middle_8 = "-" * 8
    light3 = "|        |" + list_traffic_lights_str[2] + "|"

    left_arrow = "<-"
    right_arrow = "->"
    graph_list = np.array([[spaces_2, box_8, box_8, box_19, box_8, box_8, box_8, box_8, spaces_2],
                  [left_arrow, list_roads_str[0], spaces_8, spaces_19, list_traffic_lights_str[0], list_roads_str[1], list_traffic_lights_str[3], list_roads_str[2], left_arrow],
                  [spaces_2, middle_8, middle_8, spaces_19, middle_8, middle_8, middle_8, middle_8, spaces_2],
                  [right_arrow, list_roads_str[3], list_traffic_lights_str[1], spaces_19, spaces_8, list_roads_str[4], list_traffic_lights_str[4], list_roads_str[5], right_arrow],
                  [spaces_2, box_8, box_8, light3, box_8, box_8, box_8, box_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|" + spaces_8 + "|" + spaces_8 + "|", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|" + spaces_8 + "|" + spaces_8 + "|", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|   G    |   H    |", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, list_roads_str[6],spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|" + spaces_8 + "|" + spaces_8 + "|", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8,  "|" + spaces_8 + "|" + spaces_8 + "|", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|   |    |   ^    |", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|   v    |   |    |", spaces_8, spaces_8, spaces_8, spaces_8, spaces_2],])

    print(graph_list)

def main():
    print("The beginning of traffic simulation")
    # print_graph_list()
    traffic_simulation()


main()