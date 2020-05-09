from Road import Road
from TrafficLight import TrafficLight


def traffic_simulation():
    cycle_time_len = 180
    traffic_light_1 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_2 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_3 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_4 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    traffic_light_5 = TrafficLight(green_light_time_len=60, red_light_time_len=cycle_time_len-60)
    list_of_traffic_lights = [traffic_light_1, traffic_light_2, traffic_light_3, traffic_light_4, traffic_light_5]

    road_a = Road(name="A", num_cars=3, road_length=572)
    road_b = Road(name="B", num_cars=5, road_length=414)
    road_c = Road(name="C", num_cars=3, road_length=631, in_rate=0.9)
    road_d = Road(name="D", num_cars=2, road_length=572, in_rate=0.2)
    road_e = Road(name="E", num_cars=8, road_length=414)
    road_f = Road(name="F", num_cars=1, road_length=631)
    road_g = Road(name="G", num_cars=3, road_length=643)
    road_h = Road(name="H", num_cars=5, road_length=643, in_rate=0.3)
    list_of_roads = [road_a, road_b, road_c, road_d, road_e, road_f, road_g, road_h]

    list_of_end_roads = [road_a, road_f, road_g]  # cars will only leave the box freely on those roads; to calculate
                                                        # num cars leave
    road_b.set_next_roads([road_a, road_g])
    road_c.set_next_roads([road_b])
    road_d.set_next_roads([road_e, road_g])
    road_e.set_next_roads([road_f])
    road_h.set_next_roads([road_a, road_e])

    time_length = 1800  # 30 minutes = 1800 seconds
    for curr_time in range(1, time_length):
        # in a cycle: 1. tl3; 2. tl1; 3. tl1, tl2
        for traffic_light in list_of_traffic_lights:
            traffic_light.update_status(curr_time)

        for road in list_of_roads:
            road.advance()





def main():
    print("The beginning of traffic simulation")
    traffic_simulation()


main()