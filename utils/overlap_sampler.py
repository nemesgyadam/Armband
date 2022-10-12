import numpy as np

class OverlapSampler:
    def __init__(self, honey_pot_X, honey_pot_y, settings, batch_size=64,  end_label = True):
        self.honey_pot_X = honey_pot_X
        self.honey_pot_y = honey_pot_y
        self.batch_size = batch_size
        self.end_label = end_label
        self.targets = settings['targets']
        self.input_length = settings['input_length']
        self.overlap = settings['overlap']
        self.targets = [target.lower() for target in self.targets]

       

        self.split_data()
   

    def split_data(self):
        step = self.input_length -self.overlap
        self.X_pot = []
        self.y_pot = []
        for session_index in range(len(self.honey_pot_X)):
            session_X = self.honey_pot_X[session_index]
            session_y = self.honey_pot_y[session_index]
            for start in range(0, session_X.shape[-1]-self.input_length, step):
                self.X_pot.append(session_X[:,start:start+self.input_length])
                if self.end_label:
                    sample_y = session_y[:,start+self.input_length]
                else:
                    sample_y = session_y[:,start:start+self.input_length]
                self.y_pot.append(sample_y)


        self.X_pot = np.array(self.X_pot)
        self.y_pot = np.array(self.y_pot)
        del self.honey_pot_X
        del self.honey_pot_y
 
        self.y_pot = self.get_targets(self.y_pot)

        self.shuffle()

        self.batch_data()
        
        self.n_steps = self.X_pot.shape[0]
      
        
        

        self.data = list(zip(self.X_pot, self.y_pot))
        print(self.data[0][0].shape)
        print(self.data[0][1].shape)

    def shuffle(self):
        # Shuffle
        indices = np.arange(self.X_pot.shape[0])
        np.random.shuffle(indices)
        self.X_pot = self.X_pot[indices]
        self.y_pot = self.y_pot[indices]

    def batch_data(self):
        # Drop remaining
        orignal_length = self.X_pot.shape[0]
        self.X_pot = self.X_pot[:-int(self.X_pot.shape[0]%self.batch_size)]
        self.y_pot = self.y_pot[:-int(self.y_pot.shape[0]%self.batch_size)]
        print(f'Dropped {orignal_length-self.X_pot.shape[0]} samples. {self.X_pot.shape[0]} samples remaining')
     

        self.X_pot = self.X_pot.reshape( int(self.X_pot.shape[0]/self.batch_size), self.batch_size, self.X_pot.shape[1], self.X_pot.shape[2])
        self.y_pot = self.y_pot.reshape( int(self.y_pot.shape[0]/self.batch_size), self.batch_size,self.y_pot.shape[1])


    def get_targets(self, result_y, classify = True):

        if classify:
            result_y[result_y<0.5] = 0
            result_y[result_y>=0.5] = 1


        if 'distance' in self.targets and 'degree' not in self.targets:
            result_y = result_y[:,0:1]
        elif 'distance' not in self.targets and 'degree' in self.targets:
            result_y = result_y[:,1:2]
        return result_y

  

    
        

        return result_X, result_y
        