import cv2
import numpy as np
from argparse import ArgumentParser
from april_python import *
import april_python as apriltag


class CameraRead():
    def __init__(self):
        self.cap = cv2.VideoCapture(1)

    def run(self):
        self.detect_tags()
        # while True:
        #     img = self.get_gsc_image()
        #     self.display_image(img)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # self.cap.release()
        # cv2.destroyAllWindows()

    def get_gsc_image(self, grayscale = True):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if grayscale:
            return gray
        else:
            return frame

    def detect_tags(self):
        parser = ArgumentParser(
            description='test apriltag Python bindings')
        parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                            help=1)
        apriltag.add_arguments(parser)
        options = parser.parse_args()
        cap = cv2.VideoCapture(int(options.device_or_movie))
        window = 'Camera'
        cv2.namedWindow(window)
        detector = apriltag.Detector(options)



    def display_image(self, image):
        cv2.imshow('frame',image)


cam = CameraRead()
cam.run()

# When everything done, release the capture
