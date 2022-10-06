import os 
import numpy as np
from config.armband import *
from utils.signal import DCFilter, normalize
from tensorflow.keras.utils import to_categorical
import random
import pandas as pd

def load_set(session):
    data = pd.read_csv(session)
    X_store = data[["c0","c1","c2","c3","c4","c5","c6","c7"]].values.T
    y_store = data[["distance","degree"]].values.T
    return X_store, y_store

def load_continous_data(sessions):
    honey_pot_X = []
    honey_pot_y = []
    for session in sessions:
        X_store, y_store = load_set(session)
        honey_pot_X.append(X_store)
        honey_pot_y.append(y_store)
    honey_pot_X = np.squeeze(np.array(honey_pot_X))
    honey_pot_y = np.squeeze(np.array(honey_pot_y))
    return honey_pot_X, honey_pot_y

