
class TrafficLight(object):
    def __init__(self, name, green_light_time_len, start_green_time_in_cycle=0, is_green=False, red_light_time_len=0):
        self.name = name
        self.green_light_time_len = green_light_time_len # unit: second
        self.start_green_time_in_cycle = start_green_time_in_cycle
        self.end_green_time_in_cycle = start_green_time_in_cycle + green_light_time_len
        self.is_green = is_green
        self.red_light_time_len = red_light_time_len
        self.last_green_time = 0
        self.last_red_time = 0

    def get_status(self):
        if self.is_green:
            return self.name + ": green"
        else:
            return self.name + ": red"

    def turn_green(self):
        self.is_green = True
        # print("Traffic Light " + self.name + " Turns Green.")

    def turn_red(self):
        self.is_green = False
        # print("Traffic Light " + self.name + " Turns Red.")

    def update_status_independent(self, curr_time):
        if self.is_green and (curr_time - self.last_green_time >= self.green_light_time_len):
            self.turn_red()
            self.last_red_time = curr_time
        elif (not self.is_green) and (curr_time - self.last_red_time >= self.red_light_time_len):
            self.turn_green()
            self.last_green_time = curr_time

    def update_status_in_cycle(self, curr_time_in_cycle):
        if self.is_green and curr_time_in_cycle > self.end_green_time_in_cycle:
            self.turn_red()
        elif (not self.is_green) and self.start_green_time_in_cycle <= curr_time_in_cycle <= self.end_green_time_in_cycle:
            self.turn_green()