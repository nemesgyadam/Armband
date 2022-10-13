import numpy as np
import keras
import os
from utils.continous_data import load_train_data
from utils.random_sampler import RandomSampler
from utils.overlap_sampler import OverlapSampler

class SamplerGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, settings, batch_size=32, n_steps = 1000, end_label = True, split = 'train'):
        'Initialization'
        self.data_path = settings["data_path"]
        self.batch_size = batch_size
        self.n_steps = n_steps
        self.settings = settings
        self.split = split
        self.load_sessions()
        

        if settings['sampler'] == 'random':
            self.sampler = RandomSampler(self.honey_pot_X, self.honey_pot_y, settings, self.batch_size, end_label = end_label)
        elif settings['sampler'] == 'overlap':
            self.sampler = OverlapSampler(self.honey_pot_X, self.honey_pot_y, settings, self.batch_size, end_label = end_label)
        #self.on_epoch_end()
    
    def load_sessions(self):
        sessions = []
        root_path = os.path.join(self.data_path, self.split)
        for subject in os.listdir(root_path):
            for session in os.listdir(os.path.join(root_path,subject)):
                sessions.append(os.path.join(root_path, subject,session))

        self.honey_pot_X, self.honey_pot_y = load_train_data(sessions)
        print("Loaded {} sessions".format(len(sessions)))

    def __len__(self):
        'Denotes the number of batches per epoch'
        if self.settings['sampler'] == 'random':
            return self.n_steps
        elif self.settings['sampler'] == 'overlap':
            return self.sampler.n_steps

    def __getitem__(self, index):
        'Generate one batch of data'
        if self.settings['sampler'] == 'random':
            return self.sampler.sample()
        elif self.settings['sampler'] == 'overlap':
            return self.sampler.data[index]
        else:
            raise ValueError("Unknown sampler type")

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        if self.sampler == 'overlap':
            self.sampler.split_data()
            

   