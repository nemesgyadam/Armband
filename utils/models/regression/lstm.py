 
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import TimeDistributed, GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_model(end_label = True):
    inspected_chanels= 8
    input_length=     500
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    input_layer = tf.transpose(input_layer, perm=[0, 2, 1])
    input_layer = tf.reshape(input_layer, (-1, 50, 10* 8))
    x = input_layer
    #x = layers.AveragePooling1D(pool_size= 1)(input_layer)
    l2 =0.
    
    dense = keras.Sequential()
    dense.add(layers.Dense(2, activation='elu', kernel_regularizer=regularizers.l2(l2)))
    dense.add(layers.Dropout(.2))


    #x  = TimeDistributed(dense)(x)
   
    x     = tf.keras.layers.LSTM(20)(x)
    #x     = tf.keras.layers.LSTM(20)(x)

    #x     = layers.Flatten()(x)
    #x     = tf.keras.layers.GlobalAveragePooling2D()(x)
    x     = layers.Dense(2,kernel_regularizer=regularizers.l2(l2))(x)


    if end_label:
        distance_output = layers.Dense(1, activation = 'sigmoid')(x)
        degree_output = layers.Dense(1)(x)
    else:
        distance_output = layers.Dense(500, activation = 'sigmoid')(x)
        degree_output = layers.Dense(500)(x)
    model = keras.Model(inputs=input_layer, outputs=[distance_output])

    model.summary()
    return model