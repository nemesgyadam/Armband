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
from utils.record_utils import CollectData
from utils.visualize import showMe
from utils.signal import DCFilter

from config.armband import *


"""
This script records file for previously given classes and saves it as numpy files.
"""


clear = lambda: os.system("cls")


length_of_signal = 2  # seconds


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="SubjectID")
    parser.add_argument("--session", help="Number of Session", default="1")
    parser.add_argument("--n_commands", help="Number of commands", default=1)
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    save_location = os.path.join(
        settings["save_location"], args.subject, "session_" + args.session
    )
    if os.path.isdir(save_location):
        print("Session already exists!")
        return
    print("Saving data to {}".format(save_location))

    board = init()

    results, classes = CollectData(
        board,
        classes=settings["classes"],
        signal_length=settings["signal_length"],
        n_samples_per_class=int(args.n_commands),
    )

    pathlib.Path(save_location).mkdir(parents=True, exist_ok=False)

    for i, result in enumerate(results):
        result = np.asarray(result)
        np.save(os.path.join(save_location, classes[i]), result)

    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
