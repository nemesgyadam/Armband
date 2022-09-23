import os
import cv2
import time
import math
import warnings
import datetime
import argparse
import pandas as pd
from scipy.spatial.distance import euclidean

import numpy as np

from utils.KalmanFilter1D import KalmanFilter1D
from utils.KalmanFilter2D import KalmanFilter2D
from utils.image_utils import *
from config.video import settings
from utils.calibrate_hand import Calibrator
from utils.visualizer import Visualizer
from utils.img_utils import format_frame

clear = lambda: os.system("cls")
warnings.filterwarnings("ignore")

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="Name or ID of the subject")
    return parser.parse_args(args)

def main(args=None):
    # Initialize parameters
    fist_vis = Visualizer(name = 'fist')
    degree_vis = Visualizer(name = 'degree')

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

    # Place both for the center of image for start
    black_center = (settings["process_shape"][0] // 2, settings["process_shape"][1] // 2)

    green_center = (settings["process_shape"][0] // 2, settings["process_shape"][1] // 2)

    kalman_value = None
    distance = None


  

    distance_buffer = np.zeros(500)
    degree_buffer = np.zeros(500)
    date_buffer = np.zeros(500, dtype='datetime64[ms]')
    df = pd.DataFrame(columns = ['timestamp', 'distance', 'degree'])


    calibrator = Calibrator()

    args = parse_args(args)
    save_name = os.path.join('timestamped_data','CAM',args.subject,datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.csv')
    if not os.path.exists(os.path.dirname(save_name)):
        os.makedirs(os.path.dirname(save_name))
    cap = cv2.VideoCapture(settings["stream_url"])

    # Start streaming
    iterator =0
    while True:
        iterator += 1
        timestamp = np.datetime64(datetime.datetime.now())

        ret, frame = cap.read()
        frame = format_frame(frame,settings["process_shape"],settings["image_rotation"] )
        


        black_cnt = get_black_contour(frame, settings)
        green_cnt = get_green_contour(frame, settings)

        # HAND ANGLE
        if black_cnt is not None:
            angle = countour2angle(black_cnt, frame, settings)
            kalman_angle = angle_kalman.step(angle)

            # NORMALIZE TO -1 1
            value = (angle / 90) - 1
            kalman_value = (kalman_angle / 90) - 1

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

        # PINKY DISTANCE
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
        
        # MAIN LOOP
        if calibrator.done:
            # Calculate relative values
            rel_distance = abs(float(distance - calibrator.fist_min)) / float(calibrator.fist_max - calibrator.fist_min)
            rel_distance = min(1.,rel_distance)
        
            if kalman_value < calibrator.degree_center:
                rel_degree = abs(float(kalman_value - calibrator.degree_center)) / float(calibrator.degree_center - calibrator.degree_min)
                rel_degree *= -1
                rel_degree = max(-1.,rel_degree)

            else:
                rel_degree = abs(float(kalman_value - calibrator.degree_center)) / float(calibrator.degree_max - calibrator.degree_center)
                rel_degree = min(1.,rel_degree)

            # STORE VALUES
            distance_buffer = np.roll(distance_buffer, -1)
            distance_buffer[-1] = rel_distance
            degree_buffer = np.roll(degree_buffer, -1)
            degree_buffer[-1] = rel_degree
            date_buffer = np.roll(date_buffer, -1)
            date_buffer[-1] = timestamp

            new_data = pd.DataFrame({'timestamp': date_buffer,'distance' :distance_buffer, 'degree':degree_buffer } )
            
            if len(df) == 0:
                df = new_data[new_data['timestamp'] >pd.to_datetime(datetime.date(1971,1,1)) ]
            else:
                last_stored = df.iloc[-1]['timestamp']
                new_data = new_data[new_data['timestamp'] > last_stored]
                df = pd.concat([df, new_data])

            if iterator%100 == 0:
                df.to_csv(save_name, index = False)
                print(f'Data saved to {save_name}')
        

            cv2.putText(
                frame,
                str(np.round(rel_distance))[:-2],
                (100, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (100, 255, 0),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                str(rel_degree),
                (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0,100),
                1,
                cv2.LINE_AA,
            )
            fist_vis.show(distance_buffer)
            degree_vis.show(degree_buffer)



        cv2.imshow("video", frame)
        k = cv2.waitKey(1)
        if k == 27:  # press 'ESC' to quit
            break
        
        # CALLED IN EACH ITERATION WHILE NOT DONE
        if not calibrator.done and not kalman_value is None and  not  distance is None:
            calibrator.step(kalman_value, distance, k)
       
      
        

if __name__ == "__main__":
    main()
