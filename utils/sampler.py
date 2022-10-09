import numpy as np

class Sampler:
    def __init__(self, honey_pot_X, honey_pot_y, batch_size=64, end_label = True):
        self.honey_pot_X = honey_pot_X
        self.honey_pot_y = honey_pot_y
        self.batch_size = batch_size
        self.end_label = end_label
        
    def sample(self):
        result_X = []
        result_y = []
        for i in range(self.batch_size):
            start = np.random.randint(0, self.honey_pot_X.shape[-1]-500)
            sample_X = self.honey_pot_X[:,start:start+500]
            if self.end_label:
                sample_y = self.honey_pot_y[:,start+500]
            else:
                sample_y = self.honey_pot_y[:,start:start+500]
            result_X.append(sample_X)
            result_y.append(sample_y)
        return np.array(result_X), np.array(result_y)
        