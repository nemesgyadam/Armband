
import os
import time
import numpy as np
import argparse
import pathlib
import tensorflow as tf
from tensorflow import keras
from keras import backend as K
import datetime
from scipy import signal

#from time import perf_counter_ns
import mindrove_brainflow
from mindrove_brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from mindrove_brainflow.board_shim import (
    BoardShim,
    BrainFlowInputParams,
    BoardIds,
    BrainFlowError,
)



from utils.armband import init
from utils.visualize import showMe, showHistory
from utils.signal import DCFilter, normalize
from utils.augment import apply_augment

from utils.ros import connect, commands


from config.armband import *


"""

This script records file for previously given classes and saves it as numpy files.
"""


clear = lambda: os.system("cls")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model")
    parser.add_argument("--target", help= "Device to control:(None, ros-continous, ros-step, keyboard)")
    return parser.parse_args(args)


def decode(pred, target):
    gas_pred = pred[0][0][0]
    direction_pred = pred[1][0]
    gases = ["Stop", "Go"]
    directions = ["Middle", "Right", "Left"]

    gas = gas_pred > settings["thresholds"]["gas"]

    if direction_pred < settings["thresholds"]["left"]:
        direction = 2
    elif direction_pred > settings["thresholds"]["right"]:
        direction = 1
    else:
        direction = 0
    # direction = np.argmax(direction_pred)

    if target == 'keyboard':
        if gas == 0:
            pyautogui.keyUp("up")
        elif gas == 1:
            pyautogui.keyDown("up")
        if direction == 1:
            pyautogui.keyDown("right")
            pyautogui.keyUp("left")
        elif direction == 2:
            pyautogui.keyDown("left")
            pyautogui.keyUp("right")
        else:
            pyautogui.keyUp("right")
            pyautogui.keyUp("left")
    elif target == 'ros-continous':
        speed = commands['forward']
        speed = speed.replace('speed', str(gas_pred))
        talker.publish(commands['forward'])
        direction = commands['turn']
        direction = direction.replace('direction', str(direction_pred))
        talker.publish(commands['turn'])
    elif target == 'ros-step':
        if gas == 1:
                talker.publish(commands['forward'])
            
        if direction == 1:
            talker.publish(commands['right'])
        elif direction == 2:
            talker.publish(commands['left'])
    else:
        print("invalid target")
        quit()
        

    gas_text = gases[gas]
    direction_text = directions[direction]
    print("Value:")
    print(f"Gas: {gas_pred} Direction: {direction_pred}")
    print("Command:")
    print(f"Gas: {gas_text}, Direction: {direction_text}")


def run(board, model, target, signal_length=1):
    if 'ros' in target:
        from utils.ros import connect, commands
        ros, talker = connect()
    if target == 'keyboard':
        import pyautogui
    sample_rate = board.get_sampling_rate(16)
    board.start_stream(450000)
    data_window = 2  # sec
    time.sleep(2)

    command_buffer = np.zeros((2, 100))
    buffer_index = 0
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
        data = normalize(data, False)
        data = np.expand_dims(data, axis=0)
        input(data.shape)
        #pre_start = perf_counter_ns()
        pred = model(data)
        #pre_end = perf_counter_ns()

        clear()
        if target != 'ros-continous':
            decode(pred, target)
        else:
            gas_pred = pred[0][0][0]
            direction_pred = pred[1][0]
          
            gas = gas_pred > settings["thresholds"]["gas"]

            if direction_pred < settings["thresholds"]["left"]:
                direction = 2
            elif direction_pred > settings["thresholds"]["right"]:
                direction = 1
            else:
                direction = 0
            command_buffer[0, buffer_index] = gas
            command_buffer[1, buffer_index] = direction
            buffer_index += 1
            if buffer_index == 100:
                print("calculating average")
                gas_summ = np.sum(command_buffer[0, :])
                unique, counts = numpy.unique(command_buffer[0, :], return_counts=True)
                res = dict(zip(unique, counts))
                left_summ = res[2]
                right_summ = res[1]
                print(f"gas: {gas_summ}, left: {left_summ}, right: {right_summ}")
                command_buffer = np.zeros((2, 100))
                buffer_index = 0
        print()
        print()
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
