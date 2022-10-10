import numpy as np
import keras
import os
from utils.continous_data import load_train_data
from utils.sampler import Sampler

class SamplerGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, settings, batch_size=32, n_steps = 1000, end_label = True):
        'Initialization'
        self.data_path = settings["data_path"]
        self.batch_size = batch_size
        self.n_steps = n_steps

        self.load_sessions()
        self.sampler = Sampler(self.honey_pot_X, self.honey_pot_y, end_label = end_label)
        #self.on_epoch_end()
    
    def load_sessions(self):
        sessions = []
        for subject in os.listdir(self.data_path):
            for session in os.listdir(os.path.join(self.data_path,subject)):
                sessions.append(os.path.join(self.data_path, subject,session))

        self.honey_pot_X, self.honey_pot_y = load_train_data(sessions)
        print("Loaded {} sessions".format(len(sessions)))

    def __len__(self):
        'Denotes the number of batches per epoch'
        return self.n_steps

    def __getitem__(self, index):
        'Generate one batch of data'
        return self.sampler.sample()

    def on_epoch_end(self):
       'Updates indexes after each epoch'
       ...

   