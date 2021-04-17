from threading import Timer


class TrafficObject(object):

    def set_car_state(self, car_state):
        pass

    @staticmethod
    def is_close_by(obj, frame_height, min_height_pct=0.05):
        obj_height = obj.bounding_box[1][1]-obj.bounding_box[0][1]
        return obj_height / frame_height > min_height_pct


class RedTrafficLight(TrafficObject):

    def set_car_state(self, car_state):
        car_state['speed'] = 0


class GreenTrafficLight(TrafficObject):

    def set_car_state(self, car_state):
        pass


class Person(TrafficObject):

    def set_car_state(self, car_state):
        car_state['speed'] = 0


class SpeedLimit(TrafficObject):

    def __init__(self, speed_limit):
        self.speed_limit = speed_limit

    def set_car_state(self, car_state):
        car_state['speed_limit'] = self.speed_limit


class StopSign(TrafficObject):

    def __init__(self, wait_time_in_sec=3, min_no_stop_sign=20):
        self.in_wait_mode = False
        self.has_stopped = False
        self.wait_time_in_sec = wait_time_in_sec
        self.min_no_stop_sign = min_no_stop_sign
        self.no_stop_count = min_no_stop_sign
        self.timer = None

    def set_car_state(self, car_state):
        self.no_stop_count = self.min_no_stop_sign

        if self.in_wait_mode:
            car_state['speed'] = 0
            return

        if not self.has_stopped:
            car_state['speed'] = 0
            self.in_wait_mode = True
            self.has_stopped = True
            self.timer = Timer(self.wait_time_in_sec, self.wait_done)
            self.timer.start()
            return

    def wait_done(self):
        self.in_wait_mode = False

    def clear(self):
        if self.has_stopped:
            self.no_stop_count -= 1
            if self.no_stop_count == 0:
                self.has_stopped = False
                self.in_wait_mode = False
