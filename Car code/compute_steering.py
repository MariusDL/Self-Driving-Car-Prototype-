import cv2
import numpy as np
import logging
import math
from keras.models import load_model


class CalculateSteering(object):

    def __init__(self, car=None):
        self.car = car
        self.wheels_angle = 90
        self.model = load_model('/home/pi/Desktop/CarProject/models/compute_steering_model.h5')

    def compute_the_steering(self, frame):
        # img_show("orig", frame)

        self.wheels_angle = self.model_predict_angle(frame)

        if self.car is not None:
            self.car.front_wheels.turn(self.wheels_angle)
        p_frame = show_prediction_line(frame, self.wheels_angle)

        return p_frame

    def model_predict_angle(self, frame):
        preprocessed = preprocess_image(frame)
        X = np.asarray([preprocessed])
        steering_angle = self.model.predict(X)[0]

        return int(steering_angle + 0.5)


def preprocess_image(frame):
    height, _, _ = frame.shape
    frame = frame[int(height / 2):, :, :]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.resize(frame, (200, 66))
    frame = frame / 255
    return frame


def show_prediction_line(frame, wh_angle, line_color=(0, 0, 255), line_width=5, ):
    img = np.zeros_like(frame)
    height, width, _ = frame.shape

    steering_angle_radian = wh_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(img, (x1, y1), (x2, y2), line_color, line_width)
    img = cv2.addWeighted(frame, 0.8, img, 1, 1)

    return img


def img_show(title, frame):
    cv2.imshow(title, frame)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
