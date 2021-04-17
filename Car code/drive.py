import picar
import cv2
from compute_steering import CalculateSteering
from detect_objects import DetectObjectsOnRoad


class Car(object):

    car_speed = 0
    img_width = 320
    img_height = 240

    def __init__(self):
        picar.setup()

        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3, self.img_width)
        self.camera.set(4, self.img_height)

        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.forward()
        self.back_wheels.speed = 0

        self.front_wheels = picar.front_wheels.Front_Wheels()
        self.front_wheels.turn(90)

        self.detect_traffic_objects = DetectObjectsOnRoad(self)

        self.calculate_steering_angle = CalculateSteering(self)

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):

        self.cleanup()

    def cleanup(self):
        self.back_wheels.speed = 0
        self.front_wheels.turn(90)
        self.camera.release()
        cv2.destroyAllWindows()

    def start_drive(self, speed=car_speed):

        self.back_wheels.speed = speed

        while self.camera.isOpened():
            _, captured_image = self.camera.read()
            objects_img = captured_image.copy()

            captured_image = self.calculate_steering(captured_image)
            img_show('Steering Line', captured_image)

            objects_img = self.process_objects_on_road(objects_img)
            img_show('Traffic objects', objects_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break

    def process_objects_on_road(self, image):
        image = self.detect_traffic_objects.process_objects_on_road(image)
        return image

    def calculate_steering(self, image):
        image = self.calculate_steering_angle.compute_the_steering(image)
        return image


def img_show(text, frame):
    cv2.imshow(text, frame)


def main():
    with Car() as car:
        car.start_drive(45)


if __name__ == '__main__':
    main()
