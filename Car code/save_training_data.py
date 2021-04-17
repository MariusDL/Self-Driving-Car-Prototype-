import logging
import picar
import cv2
import pygame
import time


class Car(object):
    car_speed = 0
    img_width = 320
    img_height = 240

    def __init__(self):
        logging.info('Initialize components')
        picar.setup()
        self.image = cv2.VideoCapture(-1)
        self.image.set(3, self.img_width)
        self.image.set(4, self.img_height)

        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.forward()
        self.back_wheels.speed = 0

        self.front_wheels = picar.front_wheels.Front_Wheels()
        self.front_wheels.turn(90)

        # Initialize the joystick
        pygame.display.init()
        pygame.joystick.init()
        pygame.joystick.Joystick(0).init()

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        self.cleanup()

    def cleanup(self):
        self.back_wheels.speed = 0
        self.front_wheels.turn(90)
        self.image.release()
        cv2.destroyAllWindows()

    def start_drive(self, speed=car_speed):
        self.back_wheels.speed = speed
        i = 0
        while self.image.isOpened():
            _, captured_image = self.image.read()
            i += 1

            img_show('Display', captured_image)

            pygame.event.pump()

            # Get the value from the joystick
            axis_value = pygame.joystick.Joystick(0).get_axis(0)

            # round the value to two decimals
            rounded_axis_value = round(axis_value, 2)

            angle = (rounded_axis_value * 45) + 90

            rounded_angle = round(angle)

            self.front_wheels.turn(rounded_angle)

            time.sleep(0.1)
            cv2.imwrite("data/%s_%04d_%03d.png" % ("Image", i, rounded_angle), captured_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break


def img_show(title, frame):
    cv2.imshow(title, frame)


def main():
    with Car() as car:
        car.start_drive(45)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    main()
