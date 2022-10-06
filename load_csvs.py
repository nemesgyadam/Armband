import os 
import numpy as np
import pandas as pd
import argparse
import time
from utils.visualizer import Visualizer


def get_timespan(df):
    return df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]

def load_data(args):
    CAM_df = pd.read_csv(os.path.join('timestamped_data','CAM',args.subject,args.CAM_timestamp+'.csv'))
    EMG_df = pd.read_csv(os.path.join('timestamped_data','EMG',args.subject,args.EMG_timestamp+'.csv'))
    CAM_df[['distance', 'degree']] = CAM_df[['distance', 'degree']].astype(float)
    EMG_df[['c0','c1','c2','c3','c4','c5','c6','c7']] = EMG_df[['c0','c1','c2','c3','c4','c5','c6','c7']].astype(float)

    CAM_df['timestamp'] = pd.to_datetime(CAM_df['timestamp'])
    EMG_df['timestamp'] = pd.to_datetime(EMG_df['timestamp'])


    # FIND COMMON TIME INTERVAL
    CAM_start = CAM_df['timestamp'].iloc[0]
    CAM_end = CAM_df['timestamp'].iloc[-1]
    EMG_start = EMG_df['timestamp'].iloc[0]
    EMG_end = EMG_df['timestamp'].iloc[-1]
    start = max(CAM_start, EMG_start)
    end = min(CAM_end, EMG_end)
    print(start)
    print(end)
    CAM_df = CAM_df[(CAM_df['timestamp'] >= start) & (CAM_df['timestamp'] <= end)]
    EMG_df = EMG_df[(EMG_df['timestamp'] >= start) & (EMG_df['timestamp'] <= end)]

    print(len(CAM_df))
    print(len(EMG_df))



    print("Resampling...")
    #Resample CAM data to 500Hz
    CAM_df = CAM_df.set_index('timestamp')
    CAM_df = CAM_df.resample('2ms').mean()
    CAM_df = CAM_df.interpolate(method='linear')
    CAM_df = CAM_df.reset_index()

    # Resample EMG data to 500Hz
    EMG_df = EMG_df.set_index('timestamp')
    EMG_df = EMG_df.resample('2ms').mean()
    EMG_df = EMG_df.interpolate(method='linear')
    EMG_df = EMG_df.reset_index()
    
    if len(CAM_df) > len(EMG_df):
        CAM_df = CAM_df.iloc[:len(EMG_df)]
    else:
        EMG_df = EMG_df.iloc[:len(CAM_df)]
   
    return CAM_df, EMG_df

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="Name or ID of the subject")
    parser.add_argument("CAM_timestamp", help="Name or ID of the CAM session")
    parser.add_argument("EMG_timestamp", help="Name or ID of the CAM session")
    return parser.parse_args(args)

def main(args=None):
    args = parse_args(args)
    CAM_df, EMG_df = load_data(args)
    vis = Visualizer()

    for i in range(0, len(CAM_df)):  
        relevant = EMG_df.iloc[i*1000:(i+1)*1000] # First 2 seconds
        EMG_data = relevant[['c0','c1','c2','c3','c4','c5','c6','c7']].values.T
    

        relevant = CAM_df.iloc[i*1000:(i+1)*1000] # First 2 seconds
        distance_data = relevant['distance'].values
        degree_data = relevant['degree'].values


        all_data = np.concatenate((EMG_data, distance_data.reshape(1,-1), degree_data.reshape(1,-1)), axis=0)
        
        if all_data.shape[-1] == 1000:
            vis.showAll(all_data,sleep=50)
        else:
            break
            
   

if __name__ == "__main__":
    main()