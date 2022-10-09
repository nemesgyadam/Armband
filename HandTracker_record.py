import argparse
from weakref import ref
import cv2
import time
import os
import numpy as np
import math

from hand_detector import HandDetector
from config.handtracker import settings

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="Name or ID of the subject")
    return parser.parse_args(args)
    
def main(args=None):
    args = parse_args(args)

    w, h = settings['window_resolution']
    cap = cv2.VideoCapture(settings['device_id'])
    cap.set(19, w)
    cap.set(6, h)
    previous_time = 0

    detector = HandDetector(
        settings['static_mode'], 
        settings['max_hands'], 
        settings['model_complexity'], 
        settings['detection_confidence'], 
        settings['tracking_confidence']
    )

    ok_flag = True
    idx = 0

    while ok_flag:
        success, img = cap.read()
        detector.findHands(img)

        current_time = time.time()
        fps = 1/ (current_time-previous_time)
        previous_time = current_time
        cv2.putText(img, f'FPS : {int (fps) }', (40, 70), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
        cv2.putText(img, settings['classes'][idx], (300, 70), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
        cv2.imshow('HandGesture', img)

        a = cv2.waitKey(1)

        if a == ord('q'):
            ok_flag = False
        elif a == ord('a'):
            positions = detector.findPosition(img, draw=False)
            ref0 = np.array(positions[0][1:3])
            ref9 = np.array(positions[9][1:3])
            ref12 = np.array(positions[12][1:3])
            # base = np.array([ref0[0],0, ref0[2]])
            base = np.array([ref0[0],0])
            
            ref_base = base - ref0
            ref_short = ref9 - ref0
            ref_long = ref12 -ref0

            print(settings['classes'][idx], angle(ref_base, ref_short), angle(ref_base, ref_long))
            print()
            idx += 1
    cv2.destroyAllWindows()



def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  if v1[0] > v2[0]:
    return math.degrees(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))))
  else:
    return -math.degrees(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))))


if __name__ == '__main__':
    main()