from Road import Road
from TrafficLight import TrafficLight
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)
graph_list = []


def advance_all_roads(list_of_roads):
    for road in list_of_roads:
        road.advance()


def plot_list_of_density_graphs(list_of_density_lists, time_list, label_list, traffic_condition):
    fig, ax = plt.subplots()

    for density_list in list_of_density_lists:
        ax.plot(time_list, density_list)

    plt.legend(label_list)
    ax.set(xlabel='time (s)', ylabel='density (num cars / ft)',
           title="Density of roads over time" + " (" + traffic_condition + " traffic)")

    ax.grid()
    plt.show()


def plot_graph(y_list, time_list, plot_title, y_label, traffic_condition):
    fig, ax = plt.subplots()
    ax.plot(time_list, y_list)

    ax.set(xlabel='time (s)', ylabel=y_label,
           title=plot_title + " (" + traffic_condition + " traffic)")
    ax.grid()
    plt.show()


def print_graph_list(list_of_traffic_lights=None, list_roads=None):
    list_roads_str = ["    A   ", "    B   ", "    C   ", "   D    ", "    E   ", "    F   ", "|        |        |"]
    list_traffic_lights_str = ["1: red & 1L: red".ljust(18), "2: red".ljust(8), "3: red".ljust(8), "4: red".ljust(8), "5: red".ljust(8)]
    if list_roads is not None:
        list_roads_str = []
        for i in range(len(list_roads)-2):
            list_roads_str.append((list_roads[i].name + ": " + str(list_roads[i].num_cars)).ljust(8))
        list_roads_str.append(("| " + str(list_roads[6].num_cars).ljust(6) + " | " + str(list_roads[7].num_cars).ljust(6) + " |"))

    if list_of_traffic_lights is not None:
        list_traffic_lights_str = []
        first = list_of_traffic_lights[0].get_status() + " & " + list_of_traffic_lights[1].get_status()
        list_traffic_lights_str.append(first.ljust(18))
        for i in range(2, len(list_of_traffic_lights)):
            list_traffic_lights_str.append(list_of_traffic_lights[i].get_status().ljust(8))

    global graph_list
    box_8 = "—" * 8
    box_19 = "—" * 19
    box_18 = "—"*18

    spaces_2 = " " * 2
    spaces_8 = " " * 8
    spaces_19 = " " * 19
    spaces_18 = " " * 18

    middle_8 = "-" * 8
    middle18 = "-" * 18
    light3 = "|        |" + list_traffic_lights_str[2] + "|"

    left_arrow = "<-"
    right_arrow = "->"
    graph_list = np.array([[spaces_2, box_8, box_8, box_19, box_18, box_8, box_8, box_8, spaces_2],
                  [left_arrow, list_roads_str[0], spaces_8, spaces_19, list_traffic_lights_str[0], list_roads_str[1], list_traffic_lights_str[3], list_roads_str[2], left_arrow],
                  [spaces_2, middle_8, middle_8, spaces_19, middle18, middle_8, middle_8, middle_8, spaces_2],
                  [right_arrow, list_roads_str[3], list_traffic_lights_str[1], spaces_19, spaces_18, list_roads_str[4], list_traffic_lights_str[4], list_roads_str[5], right_arrow],
                  [spaces_2, box_8, box_8, light3, box_18, box_8, box_8, box_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|" + spaces_8 + "|" + spaces_8 + "|", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|" + spaces_8 + "|" + spaces_8 + "|", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|   G    |   H    |", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, list_roads_str[6],spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|" + spaces_8 + "|" + spaces_8 + "|", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8,  "|" + spaces_8 + "|" + spaces_8 + "|", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|   |    |   ^    |", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],
                  [spaces_2, spaces_8, spaces_8, "|   v    |   |    |", spaces_18, spaces_8, spaces_8, spaces_8, spaces_2],])

    print(graph_list)


# individual simulation with graphs
def traffic_simulation_with_plots(traffic_condition, dict_traffic_coef, step_1_len=30, step_2_len=30, step_3_len=30, step_4_len=30):
    print("step_1_length=" + str(step_1_len) + ", step_2_length=" + str(step_2_len) + ", step_3_length=" + str(step_3_len) + ", step_4_length=" + str(step_4_len))
    in_rate_max = Road.U_MAX / Road.CAR_LENGTH
    traffic_coef_list = dict_traffic_coef[traffic_condition]
    c_coef = traffic_coef_list[0]
    d_coef = traffic_coef_list[1]
    h_coef = traffic_coef_list[2]

    TIME_LENGTH = 1200  # 20 minutes = 1200 seconds
    LENGTH_45_GREEN = 180
    LENGTH_45_RED = 20

    all_red_time_len = step_4_len
    length_3 = step_1_len
    length_1_left = step_2_len
    length_1_straight = step_3_len
    length_1 = length_1_left + length_1_straight
    length_2 = length_1_straight

    traffic_light_3 = TrafficLight(name="3", green_light_time_len=length_3, start_green_time_in_cycle=0)
    traffic_light_1 = TrafficLight(name="1", green_light_time_len=length_1,
                                   start_green_time_in_cycle=traffic_light_3.end_green_time_in_cycle)
    traffic_light_1_left = TrafficLight(name="1L", green_light_time_len=length_1_left,
                                        start_green_time_in_cycle=traffic_light_3.end_green_time_in_cycle)
    traffic_light_2 = TrafficLight(name="2", green_light_time_len=length_2,
                                   start_green_time_in_cycle=traffic_light_1_left.end_green_time_in_cycle)
    cycle_time_len = traffic_light_2.end_green_time_in_cycle + all_red_time_len
    print("cycle_time_len=" + str(cycle_time_len))
    list_of_dependent_traffic_lights = [traffic_light_1, traffic_light_1_left, traffic_light_2, traffic_light_3]

    traffic_light_4 = TrafficLight(name="4", green_light_time_len=LENGTH_45_GREEN, red_light_time_len=LENGTH_45_RED)
    traffic_light_5 = TrafficLight(name="5", green_light_time_len=LENGTH_45_GREEN, red_light_time_len=LENGTH_45_RED)

    traffic_light_always_green = TrafficLight(name="always green", green_light_time_len=cycle_time_len,
                                              start_green_time_in_cycle=0, is_green=True)
    list_of_traffic_lights = [traffic_light_1, traffic_light_1_left, traffic_light_2, traffic_light_3, traffic_light_4,
                              traffic_light_5]

    road_a = Road(name="A", num_cars=0, road_length=572, traffic_light=traffic_light_always_green)
    road_b = Road(name="B", num_cars=0, road_length=414, traffic_light=traffic_light_1,
                  traffic_light_left=traffic_light_1_left)
    road_c = Road(name="C", num_cars=0, road_length=631, traffic_light=traffic_light_4, in_rate=in_rate_max * c_coef)
    road_d = Road(name="D", num_cars=0, road_length=572, traffic_light=traffic_light_2, in_rate=in_rate_max * d_coef)
    road_e = Road(name="E", num_cars=0, road_length=414, traffic_light=traffic_light_5)
    road_f = Road(name="F", num_cars=0, road_length=631, traffic_light=traffic_light_always_green)
    road_g = Road(name="G", num_cars=0, road_length=643, traffic_light=traffic_light_always_green)
    road_h = Road(name="H", num_cars=0, road_length=643, in_rate=in_rate_max * h_coef, traffic_light=traffic_light_3)
    list_of_roads = [road_a, road_b, road_c, road_d, road_e, road_f, road_g, road_h]

    list_of_end_roads = [road_a, road_f, road_g]  # cars will only leave the box freely on those roads; to calculate
    # num cars leave
    road_b.set_next_roads([road_a, road_g])
    road_c.set_next_roads([road_b])
    road_d.set_next_roads([road_e, road_g])
    road_e.set_next_roads([road_f])
    road_h.set_next_roads([road_a, road_e])

    print_graph_list(list_of_traffic_lights, list_of_roads)
    for time in range(1, TIME_LENGTH, cycle_time_len):
        # in a cycle: 1. tl3; 2. tl1 & tl1_left; 3. tl1, tl2
        for curr_time_in_cycle in range(0, min(cycle_time_len, TIME_LENGTH-time+1)):
            curr_time = time + curr_time_in_cycle
            print("curr_time=" + str(curr_time))

            # update the status of light 4 and light 5 (independent of cycle)
            traffic_light_4.update_status_independent(curr_time)
            traffic_light_5.update_status_independent(curr_time)

            # update status of light 1, 1L, 2, 3 in the cycle
            print("curr_time_in_cycle=" + str(curr_time_in_cycle))
            for traffic_light in list_of_dependent_traffic_lights:
                traffic_light.update_status_in_cycle(curr_time_in_cycle)

            advance_all_roads(list_of_roads)
            print_graph_list(list_of_traffic_lights, list_of_roads)
            print()
    time_list = range(0, TIME_LENGTH)

    # plot traffic outflow (num of cars out of system) over time
    for end_road in list_of_end_roads:
        print(end_road.list_of_num_cars_out)
    road_outflow = np.array([road_a.list_of_num_cars_out, road_f.list_of_num_cars_out, road_g.list_of_num_cars_out])
    sum_outflow = road_outflow.sum(axis=0)
    print(sum_outflow)
    plot_graph(sum_outflow, time_list, plot_title="Traffic outflow over time", y_label="total traffic (num cars)", traffic_condition=traffic_condition)
    total_outflow = sum_outflow.sum()
    print(total_outflow)

    # plot densities of roads over time
    START = 0
    END = 300
    TIME = range(START, END)
    list_of_density_lists = []
    road_name_list = []
    for road in list_of_roads:
        list_of_density_lists.append(road.density_list[START:END])
        road_name_list.append(road.name)
        # if need to print the plots seperately for each road, uncomment the next line
        # plot_graph(road.density_list, time_list, plot_title="Density of road " + road.name + " over time", y_label='density (num cars / ft)')

    plot_list_of_density_graphs(list_of_density_lists, TIME, road_name_list, traffic_condition)


# called in optimization method (each simulation, without plots)
def one_simple_simulation(traffic_condition, dict_traffic_coef, step_1_len=30, step_2_len=30, step_3_len=30, step_4_len=30):
    print("step_1_length=" + str(step_1_len) + ", step_2_length=" + str(step_2_len) + ", step_3_length=" + str(step_3_len) + ", step_4_length=" + str(step_4_len))
    in_rate_max = Road.U_MAX / Road.CAR_LENGTH
    traffic_coef_list = dict_traffic_coef[traffic_condition]
    c_coef = traffic_coef_list[0]
    d_coef = traffic_coef_list[1]
    h_coef = traffic_coef_list[2]

    TIME_LENGTH = 1200  # 20 minutes = 1200 seconds
    LENGTH_45_GREEN = 180
    LENGTH_45_RED = 20

    all_red_time_len = step_4_len
    length_3 = step_1_len
    length_1_left = step_2_len
    length_1_straight = step_3_len
    length_1 = length_1_left + length_1_straight
    length_2 = length_1_straight

    traffic_light_3 = TrafficLight(name="3", green_light_time_len=length_3, start_green_time_in_cycle=0)
    traffic_light_1 = TrafficLight(name="1", green_light_time_len=length_1,
                                   start_green_time_in_cycle=traffic_light_3.end_green_time_in_cycle)
    traffic_light_1_left = TrafficLight(name="1L", green_light_time_len=length_1_left,
                                        start_green_time_in_cycle=traffic_light_3.end_green_time_in_cycle)
    traffic_light_2 = TrafficLight(name="2", green_light_time_len=length_2,
                                   start_green_time_in_cycle=traffic_light_1_left.end_green_time_in_cycle)
    cycle_time_len = traffic_light_2.end_green_time_in_cycle + all_red_time_len
    print("cycle_time_len=" + str(cycle_time_len))
    list_of_dependent_traffic_lights = [traffic_light_1, traffic_light_1_left, traffic_light_2, traffic_light_3]

    traffic_light_4 = TrafficLight(name="4", green_light_time_len=LENGTH_45_GREEN, red_light_time_len=LENGTH_45_RED)
    traffic_light_5 = TrafficLight(name="5", green_light_time_len=LENGTH_45_GREEN, red_light_time_len=LENGTH_45_RED)

    traffic_light_always_green = TrafficLight(name="always green", green_light_time_len=cycle_time_len,
                                              start_green_time_in_cycle=0, is_green=True)
    list_of_traffic_lights = [traffic_light_1, traffic_light_1_left, traffic_light_2, traffic_light_3, traffic_light_4,
                              traffic_light_5]

    road_a = Road(name="A", num_cars=0, road_length=572, traffic_light=traffic_light_always_green)
    road_b = Road(name="B", num_cars=0, road_length=414, traffic_light=traffic_light_1,
                  traffic_light_left=traffic_light_1_left)
    road_c = Road(name="C", num_cars=0, road_length=631, traffic_light=traffic_light_4, in_rate=in_rate_max * c_coef)
    road_d = Road(name="D", num_cars=0, road_length=572, traffic_light=traffic_light_2, in_rate=in_rate_max * d_coef)
    road_e = Road(name="E", num_cars=0, road_length=414, traffic_light=traffic_light_5)
    road_f = Road(name="F", num_cars=0, road_length=631, traffic_light=traffic_light_always_green)
    road_g = Road(name="G", num_cars=0, road_length=643, traffic_light=traffic_light_always_green)
    road_h = Road(name="H", num_cars=0, road_length=643, in_rate=in_rate_max * h_coef, traffic_light=traffic_light_3)
    list_of_roads = [road_a, road_b, road_c, road_d, road_e, road_f, road_g, road_h]

    list_of_end_roads = [road_a, road_f, road_g]  # cars will only leave the box freely on those roads; to calculate
    # num cars leave
    road_b.set_next_roads([road_a, road_g])
    road_c.set_next_roads([road_b])
    road_d.set_next_roads([road_e, road_g])
    road_e.set_next_roads([road_f])
    road_h.set_next_roads([road_a, road_e])

    for time in range(1, TIME_LENGTH, cycle_time_len):
        # in a cycle: 1. tl3; 2. tl1 & tl1_left; 3. tl1, tl2
        for curr_time_in_cycle in range(0, min(cycle_time_len, TIME_LENGTH-time+1)):
            curr_time = time + curr_time_in_cycle
            # update the status of light 4 and light 5 (independent of cycle)
            traffic_light_4.update_status_independent(curr_time)
            traffic_light_5.update_status_independent(curr_time)

            # update status of light 1, 1L, 2, 3 in the cycle
            for traffic_light in list_of_dependent_traffic_lights:
                traffic_light.update_status_in_cycle(curr_time_in_cycle)
            advance_all_roads(list_of_roads)
    # plot traffic outflow (num of cars out of system) over time
    road_outflow = np.array([road_a.list_of_num_cars_out, road_f.list_of_num_cars_out, road_g.list_of_num_cars_out])
    sum_outflow = road_outflow.sum(axis=0)
    total_outflow = sum_outflow.sum()
    print(total_outflow)

    time_list = range(0, TIME_LENGTH)
    # plot_graph(sum_outflow, time_list, plot_title="Traffic outflow over time", y_label="total traffic (num cars)", traffic_condition=traffic_condition)

    # print_graph_list(list_of_traffic_lights, list_of_roads)

    return total_outflow


def optimization(traffic_condition, dict_traffic_coef):
    max_total_outflow_value = -1
    max_total_outflow_tuple = (-1, -1, -1)

    for step_1_len in range(10, 121, 10):
        for step_2_len in range(10, 121, 10):
            for step_3_len in range(10, 121, 10):
                total_outflow = one_simple_simulation(traffic_condition, dict_traffic_coef, step_1_len, step_2_len, step_3_len)
                if total_outflow > max_total_outflow_value:
                    max_total_outflow_value = total_outflow
                    max_total_outflow_tuple = (step_1_len, step_2_len, step_3_len)
    print()
    print(max_total_outflow_tuple)
    print(max_total_outflow_value)
    return max_total_outflow_tuple


def optimization_fixed_cycle_length(traffic_condition, dict_traffic_coef):
    max_total_outflow_value = -1
    max_total_outflow_tuple = (-1, -1, -1)
    step_4_len = 30
    FIXED_CYCLE_LENGTH = 360
    for step_1_len in range(10, 121, 10):
        for step_2_len in range(10, 121, 10):
            step_3_len = FIXED_CYCLE_LENGTH - step_1_len - step_2_len - step_4_len
            if step_3_len > 0:
                total_outflow = one_simple_simulation(traffic_condition, dict_traffic_coef, step_1_len, step_2_len, step_3_len)
                if total_outflow > max_total_outflow_value:
                    max_total_outflow_value = total_outflow
                    max_total_outflow_tuple = (step_1_len, step_2_len, step_3_len)
    print()
    print(max_total_outflow_tuple)
    print(max_total_outflow_value)
    return max_total_outflow_tuple


def optimization_same_length_123(traffic_condition, dict_traffic_coef):
    list_of_total_outflow = []
    time_range = range(10, 500, 2)
    for step_1_len in time_range:
        step_2_len = step_1_len
        step_3_len = step_1_len
        total_outflow = one_simple_simulation(traffic_condition, dict_traffic_coef, step_1_len, step_2_len, step_3_len)
        list_of_total_outflow.append(total_outflow)

    print()
    plot_graph(list_of_total_outflow, time_range, plot_title="Total outflow over different step length", y_label="Total outflow (num of cars)", traffic_condition=traffic_condition)


def main():
    print_graph_list()
    print("The beginning of traffic simulation")

    # coefficient order: c, d, h
    DICT_TRAFFIC_COEF = {
        "light": [0.1, 0.3, 0.1],
        # "medium": [0.3, 0.5, 0.6],
        "medium": [0.3, 0.6, 0.5],
        "heavy": [1, 1, 1]
    }
    TRAFFIC_CONDITION = "light"
    # traffic_simulation_with_plots(traffic_condition=TRAFFIC_CONDITION, dict_traffic_coef=DICT_TRAFFIC_COEF)
    # one_simple_simulation(traffic_condition=TRAFFIC_CONDITION, dict_traffic_coef=DICT_TRAFFIC_COEF)
    # optimization(traffic_condition=TRAFFIC_CONDITION, dict_traffic_coef=DICT_TRAFFIC_COEF)
    optimization_same_length_123(traffic_condition=TRAFFIC_CONDITION, dict_traffic_coef=DICT_TRAFFIC_COEF)
    # optimization_fixed_cycle_length(traffic_condition=TRAFFIC_CONDITION, dict_traffic_coef=DICT_TRAFFIC_COEF)


main()