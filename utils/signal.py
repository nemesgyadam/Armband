import numpy as np

def DCFilter(data):
    new_data = []
    for d in data:
        new_data.append(d - np.mean(d))
    return np.array(new_data)
