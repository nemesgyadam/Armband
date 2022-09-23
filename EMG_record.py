import os
import time
import pandas as pd
import numpy as np
from scipy import signal
from scipy.fftpack import fft
from scipy.signal import butter,filtfilt
import argparse

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
    parser.add_argument("subject", help="Name or ID of the subject")
    return parser.parse_args(args)

def main(args=None):
    args = parse_args(args)
    save_name = os.path.join('timestamped_data','EMG',args.subject,datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.csv')
    if not os.path.exists(os.path.dirname(save_name)):
        os.makedirs(os.path.dirname(save_name))


    board = init()
    sample_rate = board.get_sampling_rate(16)
    board.start_stream(450000) 


    df = pd.DataFrame(columns = ['timestamp', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'])
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

        # GENERATE TIME STAMPS
        time_stamps = np.zeros(data.shape[-1], dtype='datetime64[ms]')
        for i, d in enumerate(range(data.shape[-1])):
            time_between_two_samples = 1000/sample_rate
            delay = time_between_two_samples * (len(data[-1])-i)
            time_stamps[i] = timestamp - datetime.timedelta(milliseconds=delay)
        
        # CREATE DATAFRAME OF THE LAST 2 seconds
        new_data = pd.DataFrame({'timestamp': time_stamps, 'c0': data[0], 'c1': data[1],'c2': data[2], 'c3':data[3], 'c4':data[4],'c5': data[5], 'c6':data[6], 'c7':data[7] } )
        
        if len(df) == 0:
            df = new_data
        else:
            last_stored = df.iloc[-1]['timestamp']
            new_data = new_data[new_data['timestamp'] > last_stored]
            df = pd.concat([df, new_data])


        if iterator%20 == 0:
            df.to_csv(save_name, index = False)
            print(f'Data saved to {save_name}')

        vis.showEMG(data, sleep = 5) 


if __name__ == "__main__":
    main()
