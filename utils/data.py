import os 
import numpy as np
from config.armband import *
from utils.signal import DCFilter, normalize
from tensorflow.keras.utils import to_categorical
import random

def load_set(sessions):
    # Crate data structure

    # FORMAT:
    # One list of sessions to all classes
    data_set = {}
    for c in settings["classes"]:
        data_set[c] = []


    # Load 
    for session in sessions:
        for c in settings["classes"]:
            #print(f'Processing {os.path.join(session, c)}')
            data = np.load(os.path.join(session, c+'.npy'),allow_pickle=True)
            data_set[c].append(data)

    
  
    for c in data_set:
        data_set[c] = np.vstack(data_set[c])
        print(f'{c}: {data_set[c].shape}')
    
    return data_set

def pre_process_set(data):
    '''
    Input format:
    Dict (class_name -> samples)

    '''
    pre_processed = {}
    for c in settings["classes"]:
        pre_processed[c] = []

    for c in data:
        #print(f'PreProcessing {c}')
        for sample in data[c]:
            pre_processed[c].append(normalize(sample))

    for c in pre_processed:
        pre_processed[c] = np.array(pre_processed[c])
        print(f'{c}: {pre_processed[c].shape}')

    return pre_processed

def format2train(data):
    X = np.concatenate([data[x] for x in sorted(data)], 0)
    
    y = range(len(settings["classes"]))
    y = np.repeat(y, [data[x].shape[0] for x in sorted(data)])
    y = to_categorical(y)
    print('X shape:', X.shape)
    print('y shape:', y.shape)
    return X, y

def shuffle(X, y):
    # #SHUFFLE DATA
    c = list(zip(X, y))
    random.shuffle(c)
    X,y = zip(*c)
    X = np.array(X)
    y = np.array(y)
    return X, y