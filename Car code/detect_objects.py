import cv2
import time
import edgetpu.detection.engine
from PIL import Image
from traffic_objects import *


class DetectObjectsOnRoad(object):

    def __init__(self,
                 car=None,
                 speed_limit=40,
                 model='/home/pi/Desktop/CarProject/models/detect_traffic_objects_quantized_edgetpu.tflite',
                 label='/home/pi/Desktop/CarProject/models/traffic_objects_labels.txt',
                 width=320,
                 height=240):
        self.width = width
        self.height = height

        self.car = car
        self.speed_limit = speed_limit
        self.speed = speed_limit

        with open(label, 'r') as f:
            pairs = (l.strip().split(maxsplit=1) for l in f.readlines())
            self.labels = dict((int(k), v) for k, v in pairs)

        self.engine = edgetpu.detection.engine.DetectionEngine(model)
        self.min_confidence = 0.30
        self.num_of_objects = 3

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10, height - 10)
        self.fontScale = 1
        self.fontColor = (255, 255, 255)
        self.boxColor = (0, 0, 255)
        self.boxLineWidth = 1
        self.lineType = 2
        self.annotate_text = ""
        self.annotate_text_time = time.time()
        self.time_to_show_prediction = 1.0

        self.traffic_objects = {0: GreenTrafficLight(),
                                1: Person(),
                                2: RedTrafficLight(),
                                3: SpeedLimit(0),
                                4: SpeedLimit(0),
                                5: StopSign()}

    def process_objects_on_road(self, frame):
        objects, final_frame = self.detect_objects(frame)
        self.control_car(objects)

        return final_frame

    def control_car(self, objects):
        car_state = {"speed": self.speed_limit, "speed_limit": self.speed_limit}

        contain_stop_sign = False
        for obj in objects:
            obj_label = self.labels[obj.label_id]
            processor = self.traffic_objects[obj.label_id]
            if processor.is_close_by(obj, self.height):
                processor.set_car_state(car_state)

            if obj_label == 'Stop':
                contain_stop_sign = True

        if not contain_stop_sign:
            self.traffic_objects[5].clear()

        self.resume_driving(car_state)

    def resume_driving(self, car_state):
        old_speed = self.speed
        self.speed_limit = car_state['speed_limit']
        self.speed = car_state['speed']

        if self.speed == 0:
            self.set_speed(0)
        else:
            self.set_speed(self.speed_limit)

        if self.speed == 0:
            time.sleep(1)

    def set_speed(self, speed):

        self.speed = speed
        if self.car is not None:
            self.car.back_wheels.speed = speed

    def detect_objects(self, frame):

        start_ms = time.time()
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_RGB)
        objects = self.engine.DetectWithImage(img_pil, threshold=self.min_confidence, keep_aspect_ratio=True,
                                              relative_coord=False, top_k=self.num_of_objects)

        if objects:
            for obj in objects:
                height = obj.bounding_box[1][1] - obj.bounding_box[0][1]
                width = obj.bounding_box[1][0] - obj.bounding_box[0][0]
                box = obj.bounding_box
                coord_top_left = (int(box[0][0]), int(box[0][1]))
                coord_bottom_right = (int(box[1][0]), int(box[1][1]))
                cv2.rectangle(frame, coord_top_left, coord_bottom_right, self.boxColor, self.boxLineWidth)
                annotate_text = "%s %.0f%%" % (self.labels[obj.label_id], obj.score * 100)
                coord_top_left = (coord_top_left[0], coord_top_left[1] + 15)
                cv2.putText(frame, annotate_text, coord_top_left, self.font, self.fontScale, self.boxColor,
                            self.lineType)

        elapsed_ms = time.time() - start_ms

        annotate_summary = "%.1f FPS" % (1.0 / elapsed_ms)

        cv2.putText(frame, annotate_summary, self.bottomLeftCornerOfText, self.font, self.fontScale, self.fontColor,
                    self.lineType)
        # cv2.imshow('Detected Objects', frame)

        return objects, frame


def show_image(title, frame):
    cv2.imshow(title, frame)


if __name__ == '__main__':
    pass
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
