# Whats its all about
The purpose of the repository is to record:
- EMG data
- The corresponding labels

# Generate label from video stream
The labels are 2 time series for the following values:
- Degree of the Palm (AKA degree)
- Distance of palm and pinky finger (AKA distance)



# EMG Data
The project works with the Mindrove ArmBand device:\
[Mindrove Official Site](https://mindrove.com/product/armband_8_ch/)

The device uses the mindrove-brainflow package:
>pip install mindrove-brainflow

# Hand tracking Data

The project works with the Leap Motion hand tracker:\
[Leap Motion Site](https://www.ultraleap.com/)

Requirements: 
Install Leap Motion SDK [Leap Motion developer archive](https://developer-archive.leapmotion.com/get-started?id=v3-developer-beta&platform=windows&version=3.2.1.45911)



# Data Recording

In order to record a dataset, run the following 2 commands simultaneously:
>CAM_record.py [subject]

### Note: Leap motion SDK at the time of coding only suppoert python v2.7 so use the env27 virtual env:
> env27\Script\activate.bat

and starrt recording by:
>LEAP_record.py [subject]

These scripts will output 2 csv-s with the EMG data and labels.

# Show CSV

In order to inspect the recorded data use the following script:

>show_csvs.py [subject] [LEAP_timestamp] [EMG_timestamp]

subject         -> Name of subject\
LEAP_timestamp  -> name of LEAP recording file (without extension)\
EMG_timestamp   -> name of LEAP recording file (without extension)

The script will show a CAM and an EMG csv.\
Cut out the timespan when data available for both dataset.\
Resample both for 500 Hz,\
and Visualize the result.

# Merge CSV
You have to merge labels and EMG recordings to a single CSV\
for the generator to understand.


>merge_csvs.py [subject] [LEAP_timestamp] [EMG_timestamp]

subject         -> Name of subject\
LEAP_timestamp  -> name of LEAP recording file (without extension)\
EMG_timestamp   -> name of LEAP recording file (without extension)

The script will load a CAM and an EMG csv.\
Cut out the timespan when data available for both dataset.\
Resample both for 500 Hz,\
and Visualize the result.

# Generator

The SamplerGenerator usees the outout of merge_csvs as input.
It expolore every file in the data folder defined in settings.
Than creates a "honey_pot" of all available data.\
It uses a sampler to get random part of the data in every batch.

## End label

The sampler has two workinng methods:
* if End label is True:
    - It returns only the labels of the final time point.\
      Output shape: 
      [batch_size, 2]
* if End label is False:
    - It return every label.\
        Output shape:
        [batch_size, num_samples, 2]

# Train

For training use the train_continous.ipynb notebook

# Complete Recording Process:

* Explain the paradigm to the subject
* Activate "env27" virtualenv in terminal A
* Start the leap motion Visulaizer in order to validate hand postion during recording(Optional)


* Apply NaCl solution to the Mindrove Armband electrodes
* Put on Armband to subject, placement:\
    - right hand
    - 2/3 of lower arm 
    - sensor look outwards
    - lights on top
![Armband Position](/resources/position.jpg "Text to show on mouseover").

* Turn on Mindrove Armband
* Connect to Mindrove WiFi
* Start LEAP_record.py to start the hand position recording\
* Start EMG_record.py
* Run show_csvs.py to check the data quaility (optional)
* Run merge_csvs.py to create train data format