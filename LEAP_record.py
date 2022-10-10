import os, sys, inspect, thread, time
import sys
sys.path.insert(0, "../lib")
sys.path.insert(1, "../lib/x86")

import time
import datetime
import argparse

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

sys.path.insert(0, 'utils/leap')
import Leap



clear = lambda: os.system("cls")

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="Name or ID of the subject")
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    save_name = os.path.join('raw_data','LEAP',args.subject,datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.csv')
    if not os.path.exists(os.path.dirname(save_name)):
        os.makedirs(os.path.dirname(save_name))
        
    controller = Leap.Controller()
  
    last_frame = -1
    iteration = 0
    started = False
    with open(save_name, mode="a") as csv_file:
        csv_file.write('timestamp,distance,degree\n')

        while 1:
            iteration += 1
            frame = controller.frame()
            if frame.id != last_frame:
                last_frame = frame.id
                timestamp = datetime.datetime.now()
                if len(frame.hands) == 0:
                    clear()
                    print("No hands detected")
                    if started:
                        print("Hand lost, stopping recording")
                        break
                elif len(frame.hands) == 1:
                  
                    started = True
                    hand = frame.hands[0]

                    grab = hand.grab_strength
                    yaw = hand.direction.yaw
                    yaw = min(max(yaw, -1.0), 1.0)
     
                    line = str(timestamp) + "," + str(grab) +"," + str(yaw)
                    clear()
                    print(line)
                    csv_file.write(line+'\n')
                elif len(frame.hands) > 1:
                    print("Too many hands detected")
                        
                time.sleep(0.0001)


if __name__ == "__main__":
    main()
