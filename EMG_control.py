import os
import time
import pandas as pd
import numpy as np
from scipy import signal
from scipy.fftpack import fft
from scipy.signal import butter,filtfilt
import argparse
import tensorflow as tf
from tensorflow import keras

import mindrove_brainflow
from mindrove_brainflow.data_filter import FilterTypes, AggOperations
from mindrove_brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError

from tqdm.notebook import tqdm
import datetime
from matplotlib import pyplot as plt

from utils.armband import init
from utils.visualize import showMe
from utils.signal import DCFilter, normalize
from config.armband import *
from utils.visualizer import Visualizer


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model name")
    return parser.parse_args(args)

def main(args=None):
    args = parse_args(args)
    model = keras.models.load_model(os.path.join('models',args.model))

  


    board = init()
    sample_rate = board.get_sampling_rate(16)
    board.start_stream(450000) 


   
    vis = Visualizer()
    time.sleep(2)
    data_window = 2 #sec

    iterator = 0
    while(True):
        iterator+=1
        
        data = board.get_current_board_data(sample_rate*(data_window+1)) # 10 seconds for DC filter
        timestamp = datetime.datetime.now()

        sos = signal.butter(4, 10, 'hp', fs=500, output='sos')
        data= signal.sosfilt(sos, data)
        data = DCFilter(data)
        data = data[
            :8, -sample_rate * data_window :
        ] 
        data = normalize(data, False)

        print(data.shape)
        print(model.predict(data))

        vis.showEMG(data, sleep = 5) 


if __name__ == "__main__":
    main()
