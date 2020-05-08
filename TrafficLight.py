
class TrafficLight(object):
    def __init__(self, green_light_time_len, red_light_time_len):
        self.green_light_time_len = green_light_time_len
        self.red_light_time_len = red_light_time_len
        self.last_green_time = 0
        self.last_red_time = 0
        self.is_green = False

    def turn_green(self, curr_time):
        self.is_green = True
        self.last_green_time = curr_time

    def turn_red(self, curr_time):
        self.is_green = False
        self.last_red_time = curr_time

    def update_status(self, curr_time):
        if self.is_green and (curr_time - self.last_green_time >= self.green_light_time_len):
            self.turn_red(curr_time)
        elif (not self.is_green) and (curr_time - self.last_red_time >= self.red_light_time_len):
            self.turn_green(curr_time)


