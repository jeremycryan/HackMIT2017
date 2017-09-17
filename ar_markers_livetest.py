#!/usr/bin/env python

import cv2
import numpy as np
import math

from detect import detect_markers

CAM_HEIGHT = 0.1
CAM_ANGLE = -math.pi/6
#   Transforms the room frame into the camera frame.
CAM_ROTATION = np.asarray([[1, 0, 0],
                          [0, math.cos(CAM_ANGLE), -math.sin(CAM_ANGLE)],
                          [0, math.sin(CAM_ANGLE), math.cos(CAM_ANGLE)]])
CAM_VECTOR = np.matmul(CAM_ROTATION, np.asarray([[0], [1], [0]]))
CAM_RATIO = 0.559/480.0
CAM_VERT_ANGLE_RANGE = 480.0*CAM_RATIO # range of camera in radians, vertical
CAM_HORIZ_ANGLE_RANGE = 640.0*CAM_RATIO

def pixel_to_angle_transform(y_pixel):
    vert_ratio = (480 - y_pixel)/240.0 - 1
    angle = vert_ratio * CAM_VERT_ANGLE_RANGE / 2.0
    transform = np.asarray([[1, 0, 0],
                              [0, math.cos(angle), -math.sin(angle)],
                              [0, math.sin(angle), math.cos(angle)]])
    return transform

def x_pixel_to_angle_transform(x_pixel):
    horiz_ratio = (x_pixel)/320.0 - 1
    angle = horiz_ratio * CAM_HORIZ_ANGLE_RANGE / 2.0
    transform = np.asarray([[math.cos(angle), math.sin(angle), 0],
                              [-math.sin(angle), math.cos(angle), 0],
                              [0, 0, 1]])
    return transform

def inverse_matrix(matrix):
    pass

def mats_to_eulers(list_of_mats):
    eulers = []
    for matrix in list_of_mats:
        eulers.append(rotationMatrixToEulerAngles(matrix))

def angle_diff(a, b):
    """ Calculates the difference between angle a and angle b (both should be in radians)
        the difference is always based on the closest rotation from angle a to angle b
        examples:
            angle_diff(.1,.2) -> -.1
            angle_diff(.1, 2*math.pi - .1) -> .2
            angle_diff(.1, .2+2*math.pi) -> -.1
    """

    d1 = a-b
    d2 = 2.0*math.pi - math.fabs(d1)
    if d1 > 0:
        d2 *= -1.0
    if math.fabs(d1) < math.fabs(d2):
        return d1
    else:
        return d2

if __name__ == '__main__':
    capture = cv2.VideoCapture(1)

    if capture.isOpened(): # try to get the first frame
        frame_captured, frame = capture.read()
    else:
        frame_captured = False
    while frame_captured:
        markers = detect_markers(frame)

        diagonal_vectors = []
        angles = []
        positions = []
        ids = []
        for m in markers:

            diff_vec = m.contours[3] - m.contours[1]
            norm_diff = diff_vec/np.linalg.norm(diff_vec)
            diagonal_vectors.append(norm_diff)
            abs_angle = math.atan2(norm_diff[0][1], norm_diff[0][0])
            rel_angle = angle_diff(math.pi/4.0, abs_angle)
            angles.append(rel_angle)

            transform = pixel_to_angle_transform(m.center[1])
            direction_vec = np.matmul(transform, CAM_VECTOR)
            slope = direction_vec[2]/direction_vec[1]
            y_coord = -CAM_HEIGHT/slope

            transform = x_pixel_to_angle_transform(m.center[0])
            direction_vec = np.matmul(transform, np.asarray([[0], [1], [0]]))
            x_coord = direction_vec[0] * y_coord
            positions.append([x_coord, y_coord, 0])

            ids.append(m.id)

        for marker in markers:
            marker.highlite_marker(frame)
        cv2.imshow('Test Frame', frame)
        frame_captured, frame = capture.read()
