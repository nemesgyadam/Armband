import os
import cv2
import time
import numpy as np
import argparse
import pathlib
import tensorflow as tf
from tensorflow import keras
from keras import backend as K
from tqdm.notebook import tqdm
import datetime
from matplotlib import pyplot as plt
from scipy import signal
import pyautogui
from time import perf_counter_ns
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
from utils.record_utils import CollectData
from utils.augment import apply_augment

from config.armband import *


"""

This script records file for previously given classes and saves it as numpy files.
"""


clear = lambda: os.system("cls")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model")
    return parser.parse_args(args)


def decode(pred, key_control=False):
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

    if key_control:
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

    gas_text = gases[gas]
    direction_text = directions[direction]
    print("Value:")
    print(f"Gas: {gas_pred} Direction: {direction_pred}")
    print("Command:")
    print(f"Gas: {gas_text}, Direction: {direction_text}")


def run(board, model, signal_length=1):
    sample_rate = board.get_sampling_rate(16)
    board.start_stream(450000)
    data_window = 2  # sec
    time.sleep(2)
    # board.start_stream(450000)

    # print("Waiting because DC filter...")
    time.sleep(2)

    times = []
    while True:
        start = perf_counter_ns()
        data = board.get_current_board_data(
            sample_rate * (data_window + 1)
        )  # 10 seconds for DC filter

        sos = signal.butter(4, 10, "hp", fs=500, output="sos")
        data = signal.sosfilt(sos, data)
        data = DCFilter(data)
        data = data[:8, -sample_rate * data_window :]
        data = normalize(data, False)
        data = np.expand_dims(data, axis=0)
        pre_start = perf_counter_ns()
        pred = model(data)
        pre_end = perf_counter_ns()

        clear()
        decode(pred)
        print()
        print()
        end = perf_counter_ns()
        times.append(end - start)
        print(f"Average time: {np.mean(times)/1e6} ms")
        print(f"Prediction time: {(pre_end-pre_start)/1e6} ms")


def main(args=None):
    args = parse_args(args)
    model_path = os.path.join("models", args.model)

    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)

    board = init()

    # model = configure(board, model=model)
    run(board, model=model, signal_length=settings["signal_length"])

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
