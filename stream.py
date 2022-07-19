import os
import cv2
import time
import math
import warnings
from scipy.spatial.distance import euclidean

import numpy as np

from utils.KalmanFilter1D import KalmanFilter1D
from utils.KalmanFilter2D import KalmanFilter2D
from utils.image_utils import *
from config.default import settings

clear = lambda: os.system("cls")
warnings.filterwarnings("ignore")


# KALMAN FILTER FOR PALM ANGLE
angle_kalman = KalmanFilter1D(
    settings["angle_dt"],
    settings["angle_u"],
    settings["angle_std_acc"],
    settings["angle_std_meas"],
)

# KALMAN FILTER FOR FINGER POSITION
green_kalman = KalmanFilter2D(
    settings["dt"],
    settings["u_x"],
    settings["u_y"],
    settings["std_acc"],
    settings["x_std_meas"],
    settings["y_std_meas"],
)

# KALMAN FILTER FOR PALM POSITION
black_kalman = KalmanFilter2D(
    settings["dt"],
    settings["u_x"],
    settings["u_y"],
    settings["std_acc"],
    settings["x_std_meas"],
    settings["y_std_meas"],
)

black_center = (settings["process_shape"][0] // 2, settings["process_shape"][1] // 2)
green_center = (settings["process_shape"][0] // 2, settings["process_shape"][1] // 2)


cap = cv2.VideoCapture(settings["stream_url"])
while True:
    new_frame_time = time.time()
    ret, frame = cap.read()

    frame = cv2.resize(frame, settings["process_shape"])
    if settings["image_rotation"] == 90:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    if settings["image_rotation"] == 180:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_180)
    if settings["image_rotation"] == 270:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

    black_cnt = get_black_contour(frame, settings)
    green_cnt = get_green_contour(frame, settings)

    # HAND ANGLE
    if black_cnt is not None:
        angle = countour2angle(black_cnt, frame, settings)
        kalman_angle = angle_kalman.step(angle)

        # NORMALIZE TO -1 1
        value = (angle / 90) - 1
        kalman_value = (kalman_angle / 90) - 1

        # SHOW NORMALIZED ANGLE
        # cv2.putText(frame, str(np.round(value,1)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(
            frame,
            str(np.round(kalman_value, 1)),
            (20, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1,
            cv2.LINE_AA,
        )
    ###########################################################

    # FINDER DISTANCE
    green_temp = center(green_cnt)
    black_temp = center(black_cnt)
    green_center = green_temp if green_temp is not None else green_center
    black_center = black_temp if black_temp is not None else black_center

    # draw_center(frame, green_center)
    # draw_center(frame, black_center, (255,0,0))

    kalman_green_center = green_kalman.step(green_center)
    kalman_black_center = black_kalman.step(black_center)

    draw_center_kalman(frame, kalman_green_center)
    draw_center_kalman(frame, kalman_black_center, (255, 0, 0))

    distance = euclidean(green_center, black_center)

    # SHOW DISTANCE
    cv2.putText(
        frame,
        str(np.round(distance))[:-2],
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
        cv2.LINE_AA,
    )
    ###########################################################

    cv2.imshow("video", frame)
    k = cv2.waitKey(int(1000 / 25)) & 0xFF
    if k == 27:  # press 'ESC' to quit
        break
