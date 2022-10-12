
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_model(end_label = True):
    inspected_chanels= 8
    input_length=     500
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    #x = layers.MaxPooling1D(pool_size= 1, data_format = 'channels_first')(input_layer)
    x = input_layer
    l2 =0.00002
    x = layers.Dense(20, activation='relu', kernel_regularizer=regularizers.l2(l2))(x)
    x  = layers.Dropout(.2)(x)

    x = layers.GlobalMaxPooling1D()(x)
    x = layers.Dense(20)(x)
    if end_label:
        distance_output = layers.Dense(1, activation = 'sigmoid', name = 'distance')(x)
        degree_output = layers.Dense(1, activation = 'tanh', name ='degree')(x)
    else:
        distance_output = layers.Dense(500, activation = 'sigmoid')(x)
        degree_output = layers.Dense(500, activation = 'tanh', name ='degree')(x)
    model = keras.Model(inputs=input_layer, outputs=[distance_output, degree_output])

    model.summary()
    return model