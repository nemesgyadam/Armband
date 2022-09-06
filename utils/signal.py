import numpy as np
from config.armband import *
from scipy import signal


def DCFilter(data):
    new_data = []
    for d in data:
        new_data.append(d - np.mean(d))
    return np.array(new_data)


def normalize(data):
    range = settings["normalize_range"]
    data = signal.resample(data, settings["input_length"], axis=-1)
    data = np.clip(data, range[0], range[1])
    data /= range[1]
    return data
