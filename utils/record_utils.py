from genericpath import isdir
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

def GenerateOrder(n_classes, n_samples_per_class=1):
    lists = []
    for i in range(n_classes):
        tmp = np.empty([n_samples_per_class])
        tmp.fill(i)
        lists.append(tmp)
    order = np.vstack(lists).ravel().astype(np.int32)
    #np.random.shuffle(order)
    return order


def CollectData(
    board, classes, signal_length=1, n_samples_per_class=1
):
    sample_rate = board.get_sampling_rate(16)
    
    results = [[] for i in range(len(classes))]
    tasks = GenerateOrder(len(classes), n_samples_per_class)

    board.start_stream(450000)
    i = 0
    print("Waiting because DC filter...")
    time.sleep(5)
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
            :8, -sample_rate * signal_length :
        ]  # keep the data of the eeg channels only, and remove data over the trial length
        results[task].append(data)
        i += 1
    return results, classes
