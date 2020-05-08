from Road import Road
from TrafficLight import TrafficLight


def traffic_simulation():
    traffic_light_1 = TrafficLight(green_light_time_len=60, red_light_time_len=120)
    traffic_light_2 = TrafficLight(green_light_time_len=60, red_light_time_len=120)
    traffic_light_3 = TrafficLight(green_light_time_len=60, red_light_time_len=120)
    road_a = Road(name="A", num_cars=3, road_length=572)
    road_b = Road(name="B", num_cars=5, road_length=414)
    road_c = Road(name="C", num_cars=3, road_length=631, in_rate=10)
    road_d = Road(name="D", num_cars=2, road_length=572, in_rate=8)
    road_e = Road(name="E", num_cars=8, road_length=414)
    road_f = Road(name="F", num_cars=1, road_length=631)
    road_g = Road(name="G", num_cars=3, road_length=643)
    road_h = Road(name="H", num_cars=5, road_length=643, in_rate=5)

    list_end_roads = [road_a, road_f, road_g]  # cars will only leave the box freely on those roads

    time_length = 1800  # 30 minutes = 1800 seconds
    for curr_time in range(1, time_length):





def main():
    print("The beginning of traffic simulation")
    traffic_simulation()


main()