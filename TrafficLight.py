
class TrafficLight(object):
    def __init__(self, name, green_light_time_len, start_green_time_in_cycle, is_green=False):
        self.name = name
        self.green_light_time_len = green_light_time_len # unit: second
        self.start_green_time_in_cycle = start_green_time_in_cycle
        self.end_green_time_in_cycle = start_green_time_in_cycle + green_light_time_len
        self.is_green = is_green

    def get_status(self):
        if self.is_green:
            return self.name + ": green"
        else:
            return self.name + ": red"

    def turn_green(self):
        self.is_green = True

    def turn_red(self):
        self.is_green = False

    def update_status(self, curr_time_in_cycle):
        if self.is_green and curr_time_in_cycle > self.start_green_time_in_cycle:
            self.turn_red()
            print("Traffic Light " + self.name + " Turns Red.")
        elif (not self.is_green) and curr_time_in_cycle < self.end_green_time_in_cycle:
            self.turn_green()
            print("Traffic Light " + self.name + " Turns Green.")


