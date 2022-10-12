
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_model():
    inspected_chanels= 8
    input_length=     500
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    x  = layers.Dense(100)(input_layer)
    #x  = layers.Dropout(.1)(x)
   
    distance_output = layers.Dense(1, activation = 'sigmoid')(x)
    
    model = keras.Model(inputs=input_layer, outputs=[distance_output])

    model.summary()
    return model