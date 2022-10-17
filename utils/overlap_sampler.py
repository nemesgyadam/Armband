import numpy as np
from matplotlib import pyplot as plt

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
        X_pot = []
        y_pot = []

        shift = np.random.randint(0, step)
        # Collect all sessions
        for session_index in range(len(self.honey_pot_X)):
            session_X = self.honey_pot_X[session_index]
            session_y = self.honey_pot_y[session_index]
            for start in range(shift, session_X.shape[-1]-self.input_length, step):
                X_pot.append(session_X[:,start:start+self.input_length])
                if self.end_label:
                    sample_y = session_y[:,start+self.input_length]
                else:
                    sample_y = session_y[:,start:start+self.input_length]
                y_pot.append(sample_y)
        X_pot = np.array(X_pot)
        y_pot = np.array(y_pot)
        
 
        y_pot = self.get_targets(y_pot)

        X_pot, y_pot = self.shuffle(X_pot, y_pot)

        X_pot, y_pot = self.batch_data(X_pot, y_pot)
        
        

        # FORMAT DATA FOR GENERATOR
        y_pot_dict = []
        for i in range(y_pot.shape[0]):
            y_pot_dict.append({'distance': y_pot[i][:,0:1], 'degree': y_pot[i][:,1:2]})
        self.data = list(zip(X_pot, y_pot_dict))

        self.n_steps = X_pot.shape[0]


    def shuffle(self, X_pot, y_pot):
        # Shuffle
        indices = np.arange(X_pot.shape[0])
        np.random.shuffle(indices)
        X_pot = X_pot[indices]
        y_pot = y_pot[indices]
        return X_pot, y_pot

    def batch_data(self, X_pot, y_pot):
        orignal_length = X_pot.shape[0]

        # Drop remaining
        X_pot = X_pot[:-int(X_pot.shape[0]%self.batch_size)]
        y_pot = y_pot[:-int(y_pot.shape[0]%self.batch_size)]
        print(f'Dropped {orignal_length-X_pot.shape[0]} samples. {X_pot.shape[0]} samples remaining')
     

        X_pot = X_pot.reshape( int(X_pot.shape[0]/self.batch_size), self.batch_size, X_pot.shape[1], X_pot.shape[2])
        y_pot = y_pot.reshape( int(y_pot.shape[0]/self.batch_size), self.batch_size,y_pot.shape[1])
        return X_pot, y_pot

    def get_targets(self, result_y, classify = False):
           
        with plt.rc_context({'figure.facecolor':'white'}):
            distance = result_y[:,0:1]
            degree = result_y[:,1:2]
            fig, axs = plt.subplots(2, 2, figsize=(20, 10))
            axs[0,0].set_title('Distance Original')
            axs[0,0].hist(distance)
            axs[0,1].set_title('Degree Original')
            axs[0,1].hist(degree)
            if classify:
               

            

                distance[distance<0.5] = 0
                distance[distance>=0.5] = 1

                degree[(degree>=-0.5) & (degree<=0.5)] = 0
                degree[degree>0.5] = 1
                degree[degree< -0.5] = 2
                
                
                axs[1,0].set_title('Distance')
                axs[1,0].hist(distance)
                axs[1,1].set_title('Degree')
                axs[1,1].hist(degree)
        
                
                    

            result_y = np.concatenate((distance, degree), axis=1)
            plt.show()

        if 'distance' in self.targets and 'degree' not in self.targets:
            result_y = result_y[:,0:1]
        elif 'distance' not in self.targets and 'degree' in self.targets:
            result_y = result_y[:,1:2]
        return result_y

    
        
