import os 
import numpy as np
import pandas as pd
import argparse
import time
from utils.visualizer import Visualizer


def get_timespan(df):
    return df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]

def load_data(args):
    LEAP_df = pd.read_csv(os.path.join('raw_data','LEAP',args.subject,args.LEAP_timestamp+'.csv'))
    EMG_df = pd.read_csv(os.path.join('raw_data','EMG',args.subject,args.EMG_timestamp+'.csv'))
    LEAP_df[['distance', 'degree']] = LEAP_df[['distance', 'degree']].astype(float)
    EMG_df[['c0','c1','c2','c3','c4','c5','c6','c7']] = EMG_df[['c0','c1','c2','c3','c4','c5','c6','c7']].astype(float)

    LEAP_df['timestamp'] = pd.to_datetime(LEAP_df['timestamp'])
    EMG_df['timestamp'] = pd.to_datetime(EMG_df['timestamp'])


    # FIND COMMON TIME INTERVAL
    LEAP_start = LEAP_df['timestamp'].iloc[0]
    LEAP_end = LEAP_df['timestamp'].iloc[-1]
    EMG_start = EMG_df['timestamp'].iloc[0]
    EMG_end = EMG_df['timestamp'].iloc[-1]
    print("LEAP start: ", LEAP_start)
    print("LEAP end: ", LEAP_end)
    print("EMG start: ", EMG_start)
    print("EMG end: ", EMG_end)
    start = max(LEAP_start, EMG_start)
    end = min(LEAP_end, EMG_end)
 
    LEAP_df = LEAP_df[(LEAP_df['timestamp'] >= start) & (LEAP_df['timestamp'] <= end)]
    EMG_df = EMG_df[(EMG_df['timestamp'] >= start) & (EMG_df['timestamp'] <= end)]




    print("Resampling...")
    #Resample LEAP data to 500Hz
    LEAP_df = LEAP_df.set_index('timestamp')
    LEAP_df = LEAP_df.resample('2ms').mean()
    LEAP_df = LEAP_df.interpolate(method='linear')
    LEAP_df = LEAP_df.reset_index()

    # Resample EMG data to 500Hz
    EMG_df = EMG_df.set_index('timestamp')
    EMG_df = EMG_df.resample('2ms').mean()
    EMG_df = EMG_df.interpolate(method='linear')
    EMG_df = EMG_df.reset_index()
    
    if len(LEAP_df) > len(EMG_df):
        LEAP_df = LEAP_df.iloc[:len(EMG_df)]
    else:
        EMG_df = EMG_df.iloc[:len(LEAP_df)]
   
    return LEAP_df, EMG_df

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="Name or ID of the subject")
    parser.add_argument("LEAP_timestamp", help="Name or ID of the LEAP session")
    parser.add_argument("EMG_timestamp", help="Name or ID of the LEAP session")
    return parser.parse_args(args)

def main(args=None):
    args = parse_args(args)
    LEAP_df, EMG_df = load_data(args)
  
    df = pd.concat([LEAP_df.set_index('timestamp'), EMG_df.set_index('timestamp')], axis=1, join = 'inner').reset_index()
    if len(df)==0:
        print("No common section found")
        return
    timestamp = df['timestamp'].iloc[0].strftime("%Y-%m-%d_%H-%M")
    if not os.path.isdir(os.path.join('train_data','train',args.subject)):
        os.mkdir(path=os.path.join('train_data','train',args.subject))
    #df.to_csv(os.path.join('train_data',args.subject,timestamp+'.csv'), index=False)

    features = df[["c0","c1","c2","c3","c4","c5","c6","c7"]].values.T
    labels   = df[["distance","degree"]].values.T
    data = np.concatenate((features, labels), axis=0)

    np.save(os.path.join('train_data','train',args.subject,timestamp+'.npy'), data)
    print("Merged csv saved to train_data/train"+args.subject+"/"+timestamp+".npy")
    
   

if __name__ == "__main__":
    main()