import os
import time
import numpy as np
from scipy import signal
from scipy.fftpack import fft
from scipy.signal import butter,filtfilt

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



board = init()
sample_rate = board.get_sampling_rate(16)


board.start_stream(450000) 

vis = Visualizer()
time.sleep(2)
data_window = 2 #sec
while(True):
   
    data = board.get_current_board_data(sample_rate*20) # 10 seconds for DC filter
    data = DCFilter(data)
    data = data[
        :8, -sample_rate * data_window :
    ] 
    sos = signal.butter(10, 15, 'hp', fs=500, output='sos')
    data= signal.sosfilt(sos, data)
    data = normalize(data, False)
    vis.showEMG(data, sleep = 5) 