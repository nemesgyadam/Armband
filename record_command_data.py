import os
import time
import numpy as np
import argparse
import pathlib

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
from utils.signal import DCFilter
from config.armband import *

clear = lambda: os.system("cls")


length_of_signal = 2  # seconds


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="SubjectID")
    parser.add_argument("--session", help="Number of Session", default="1")
    return parser.parse_args(args)


def GenerateOrder(n_classes, n_samples_per_class=1):
    lists = []
    for i in range(n_classes):
        tmp = np.empty([n_samples_per_class])
        tmp.fill(i)
        lists.append(tmp)
    order = np.vstack(lists).ravel().astype(np.int32)
    np.random.shuffle(order)
    return order


def CollectData(
    board, classes=["Left", "Right", "Fist"], signal_length=1, n_samples_per_class=1
):
    sample_rate = board.get_sampling_rate(16)
    classes = ["Rest"] + classes
    results = [[] for i in range(len(classes))]
    tasks = GenerateOrder(len(classes), n_samples_per_class)

    board.start_stream(450000)
    i = 0
    for task in tasks:
        clear()
        print("Stand By! ({}/{})".format(i + 1, len(tasks)))
        time.sleep(1)
        print("Perform |{:^10s}|".format(classes[task]))
        # board.get_board_data() # clear buffer
        time.sleep(
            signal_length * 1.1
        )  # record longer to make sure there is enough data
        data = board.get_board_data()
        data = DCFilter(data)
        data = data[
            :6, -sample_rate * signal_length :
        ]  # keep the data of the eeg channels only, and remove data over the trial length
        results[task].append(data)
        i += 1
    return results, classes


def main(args=None):
    args = parse_args(args)
    save_location = os.path.join(
        settings["save_location"], args.subject, "session_" + args.session
    )
    print("Saving data to {}".format(save_location))

    board = init()

    results, classes = CollectData(
        board, signal_length=settings["signal_length"], n_samples_per_class=1
    )

    pathlib.Path(save_location).mkdir(parents=True, exist_ok=False)

    i = 0
    for result in tqdm(results):
        result = np.asarray(result)
        np.save(os.path.join(save_location, classes[i]), result)
        i += 1

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
