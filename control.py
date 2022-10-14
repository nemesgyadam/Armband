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


def configure(board, model, n_commands=5):
    print("Running configureation...")

    # Collect tune data
    results, _ = CollectData(
        board,
        classes=settings["classes"],
        signal_length=settings["signal_length"],
        n_samples_per_class=n_commands,
    )

    # Preprocess data
    pre_processed = []
    for result in np.vstack(results):
        pre_processed.append(np.array(normalize(result)))

    # Formating
    X = np.array(pre_processed)
    y = range(len(settings["classes"]))
    y = np.repeat(y, n_commands)
    y = tf.keras.utils.to_categorical(y, len(settings["classes"]))
    print("X shape: ", X.shape)
    print("y shape: ", y.shape)
    X, y = apply_augment(X, y)

    # TRAINING
    opt = keras.optimizers.Adam(learning_rate=0.01)
    loss = tf.keras.losses.CategoricalCrossentropy(
        from_logits=False, label_smoothing=0.0, name="categorical_crossentropy"
    )
    model.compile(optimizer=opt, loss=loss, metrics=["accuracy"])
    history = model.fit(
        X,
        y,
        batch_size=len(settings["classes"]) * n_commands,
        epochs=10,
        shuffle=True,
    )
    showHistory(history)
    return model

def decode(pred, threshold = 0.5):
    gas_pred = pred[0][0][0]
    direction_pred = pred[1][0]
    gases = ["Stop","Go"]
    directions = ["Middle", "Right", "Left"]

    if gas_pred> threshold:
         gas_text = gases[1]
         pyautogui.keyDown('up')
    else:
        gas_text = gases[0]
        pyautogui.keyUp('up')

    direction = np.argmax(direction_pred)
    direction_text = directions[direction]
    if direction == 1:
        pyautogui.keyDown('right')
        pyautogui.keyUp('left')
    elif direction == 2:
        pyautogui.keyDown('left')
        pyautogui.keyUp('right')
    else:
        pyautogui.keyUp('right')
        pyautogui.keyUp('left')
    clear()
    print(f"Gas: {gas_text}, Direction: {direction_text}")


def run(board, model, signal_length=1):
    sample_rate = board.get_sampling_rate(16)
    board.start_stream(450000)
    data_window = 2 #sec
    time.sleep(2)
    # board.start_stream(450000)

    # print("Waiting because DC filter...")
    time.sleep(2)

    times = []
    while True:
        start = perf_counter_ns()
        data = board.get_current_board_data(sample_rate*(data_window+1)) # 10 seconds for DC filter


        sos = signal.butter(4, 10, 'hp', fs=500, output='sos')
        data= signal.sosfilt(sos, data)
        data = DCFilter(data)
        data = data[
            :8, -sample_rate * data_window :
        ] 
        data = normalize(data, False)
        data = np.expand_dims(data, axis=0)
        pred = model(data)
        #print(pred)
        decode(pred)
        end = perf_counter_ns()
        times.append(end-start)
        print(f"Average time: {np.mean(times)/1e6} ms")




def main(args=None):
    args = parse_args(args)
    model_path = os.path.join("models", args.model)

    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)

    board = init()

    #model = configure(board, model=model)
    run(board, model=model, signal_length=settings["signal_length"])

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
