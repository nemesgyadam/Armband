import numpy as np
from config.armband import *
from scipy import signal


def DCFilter(data):
    return data -np.mean(data, axis=-1, keepdims=True)
    new_data = []
    for d in data:
        new_data.append(d - np.mean(d))
    return np.array(new_data)


def normalize(data, resample =True):
    range = settings["normalize_range"]
    if resample:
        data = signal.resample(data, settings["input_length"], axis=-1)
    data = np.clip(data, range[0], range[1])
    data /= range[1]
    return data
