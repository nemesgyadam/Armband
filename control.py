
import os
import time
import numpy as np
import argparse
import pathlib
import tensorflow as tf

import datetime
from scipy import signal

#from time import perf_counter_ns
import mindrove
from mindrove.data_filter import DataFilter, FilterTypes, AggOperations
from mindrove.board_shim import (
    BoardShim,
    MindRoveInputParams,
    BoardIds,
    MindRoveError,
)



from utils.armband import init
from utils.visualize import showMe, showHistory
from utils.signal import DCFilter, normalize
from utils.augment import apply_augment

from utils.ros import connect, commands
from utils.control import *

from config.armband import *


"""

This script records file for previously given classes and saves it as numpy files.
"""


clear = lambda: os.system("cls")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model")
    parser.add_argument("--target", default = '', help= "Device to control:(None, ros-continous, ros-step, keyboard)")
    return parser.parse_args(args)


def decode(pred):
    time.sleep(0.1)
    gas_pred = pred[0][0][0]
    direction_pred = pred[1][0][0]
    print (pred[0][0])
    print (pred[1][0])
    
    # én így szoktam kasztolni ;)
    gas = 1 if gas_pred > settings["thresholds"]["gas"] else 0

    if direction_pred < settings["thresholds"]["left"]:
        direction = 2
    elif direction_pred > settings["thresholds"]["right"]:
        direction = 1
    else:
        direction = 0
        

    return gas, direction, gas_pred, direction_pred
  

def print_info(gas, direction, gas_pred, direction_pred):
    clear()
    gases = ["Stop", "Go"]
    directions = ["Middle", "Right", "Left"]
    gas_text = gases[gas]
    direction_text = directions[direction]
    print("Value:")
    print(f"Gas: {gas_pred} Direction: {direction_pred}")
    print("Command:")
    print(f"Gas: {gas_text}, Direction: {direction_text}")
    

def run(board, model, target, signal_length=1):
    controller = Controller(target)
        
    board_id = BoardIds.MINDROVE_WIFI_BOARD.value 
    sample_rate = board.get_sampling_rate(board_id)
    board.start_stream(450000)
    data_window = 2  # sec
    time.sleep(3)
    

    times = []
    while True:
        #start = perf_counter_ns()
        data = board.get_current_board_data(
            sample_rate * (data_window + 1)
        )  # 10 seconds for DC filter

        sos = signal.butter(4, 10, "hp", fs=500, output="sos")
        data = signal.sosfilt(sos, data)
        data = DCFilter(data)
        data = data[:8, -sample_rate * data_window :]
        #print(data.shape)
        data = normalize(data, False)
        #print(data.shape)
        data = np.expand_dims(data, axis=0)
        
        #pre_start = perf_counter_ns()
        pred = model(data)
        #pre_end = perf_counter_ns()
        print (pred)
        
        
        gas, direction, gas_pred, direction_pred = decode(pred)
        print_info(gas, direction, gas_pred, direction_pred)
        
        if target == 'keyboard':
            controller.keyboard_control(gas, direction)
        elif target == 'ros-step':
            controller.ros_step_control(gas, direction)
        elif target == 'ros-continous':
            controller.ros_continous_control(gas_pred, direction_pred)
            
      
            
           

       
       
        #end = perf_counter_ns()
        #times.append(end - start)
        #print(f"Average time: {np.mean(times)/1e6} ms")
        #print(f"Prediction time: {(pre_end-pre_start)/1e6} ms")


def main(args=None):
    args = parse_args(args)
    model_path = os.path.join("models", args.model)

    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)
   
    board = init()

    # model = configure(board, model=model)
    run(board, model=model, target = args.target, signal_length=settings["signal_length"])

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
