# Whats its all about
The purpose of the repository is to record:
- EMG data
- The corresponding labels

# Generate label from video stream
The labels are 2 time series for the following values:
- Degree of the Palm
- Distance of palm and pinky finger (AKA isFist)


Stream.py process a video or live stream from the following setup!:\
![alt text](resources/demo.jpg)

## Algoritm
The script finds the contour of biggest black object(AKA palm)
- Calculate the degree of the palm
- Apply 1D kalman filter to the degree
- Normalize it -1, 1 

The script finds the contour of biggest green object(AKA finger)
- Calculate the distance of the finger and palm



# EMG Data
The project works with the Mindrove ArmBand device:\
[Mindrove Official Site](https://mindrove.com/product/armband_8_ch/)

The device uses the mindrove-brainflow package:
>pip install mindrove-brainflow


# Data Recording

In order to record a dataset, ran the following 2 commands simultaneously:
>CAM_record.py [subject]

>EMG_record.py [subject]

These scripts will output 2 csv-s with the EMG data and labels.

# Load CSV

>load_csvs.py

The script will load a CAM and an EMG csv.

Cut out the timespan when data available for both dataset.

Resample both for 500 Hz,

and Visualize the result.



