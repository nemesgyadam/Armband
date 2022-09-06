import os
import cv2
import time
import numpy as np
import argparse
import pathlib
import tensorflow as tf
import brainflow
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import (
    BoardShim,
    BrainFlowInputParams,
    BoardIds,
    BrainFlowError,
)

from tqdm.notebook import tqdm
import datetime
from matplotlib import pyplot as plt

from utils.armband import init
from utils.visualize import showMe
from utils.signal import DCFilter, normalize
from config.armband import *


"""
This script records file for previously given classes and saves it as numpy files.
"""


clear = lambda: os.system("cls")


length_of_signal = 2  # seconds


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model")
    return parser.parse_args(args)


def Run(board, model, signal_length=1):
    sample_rate = board.get_sampling_rate(16)
    board.start_stream(450000)

    print("Waiting because DC filter...")
    time.sleep(5)

    while True:
        print("Stand By!")
        time.sleep(1)
        print("Perform")
        time.sleep(
            signal_length * 1.1
        )  # record longer to make sure there is enough data
        data = board.get_board_data()
        data = DCFilter(data)
        data = data[
            :8, -sample_rate * signal_length :
        ]  # keep the data of the emg channels only, and remove data over the trial length
        pre_processed = normalize(data)
        showMe(pre_processed, [-1, 1])
        result = model(np.array([pre_processed]))[0]
        pred_class = np.argmax(result)
        clear()
        print(pred_class)
        print(settings["classes"][pred_class])

        k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
        if k == ord("q"):
            break


def main(args=None):
    args = parse_args(args)

    model_path = os.path.join("models", args.model)
    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)

    board = init()

    Run(board, model=model, signal_length=settings["signal_length"])

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
