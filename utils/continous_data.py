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

def load_train_data(sessions):
    honey_pot_X = []
    honey_pot_y = []

    print(f"Loading {len(sessions)} sessions...")
    for session in sessions:
        X_store, y_store = load_set(session)
        # print(f"X_store shape: {X_store.shape}")
        # print(f"y_store shape: {y_store.shape}")
        honey_pot_X.append(X_store)
        honey_pot_y.append(y_store)
    return honey_pot_X, honey_pot_y

