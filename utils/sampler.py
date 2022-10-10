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
        n_sessions = len(self.honey_pot_X)
        for i in range(self.batch_size):
            # Handle multiple sessions
            session_id = np.random.randint(0, n_sessions)
            session_X = self.honey_pot_X[session_id]
            session_y = self.honey_pot_y[session_id]
            
            start = np.random.randint(0, session_X.shape[-1]-500)
            sample_X = session_X[:,start:start+500]
            if self.end_label:
                sample_y = session_y[:,start+500]
            else:
                sample_y = session_y[:,start:start+500]
            result_X.append(sample_X)
            result_y.append(sample_y)
        return np.array(result_X), np.array(result_y)
        