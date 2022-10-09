
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_model(end_label = True):
    inspected_chanels= 8
    input_length=     500
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    x = layers.Reshape((inspected_chanels,input_length,1))(input_layer)
    x  = layers.AveragePooling2D(pool_size=(1,2))(x) # resample to 500

    l2 = 0.005
        
   
    x     = layers.Conv2D(100, kernel_size=(1,100), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    x     = layers.AveragePooling2D(pool_size=(1,100))(x)

    x     = layers.Conv2D(100, kernel_size=(1,1), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    x     = layers.AveragePooling2D(pool_size=(1,1))(x)
    x     = layers.BatchNormalization()(x)
    x     = layers.Flatten()(x)
    #x     = tf.keras.layers.GlobalAveragePooling2D()(x)
    x     = layers.Dense(20,kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.Dropout(.1)(x)

    
    if end_label:
        distance_output = layers.Dense(1, activation = 'sigmoid')(x)
        degree_output = layers.Dense(1)(x)
    else:
        distance_output = layers.Dense(500, activation = 'sigmoid')(x)
        degree_output = layers.Dense(500)(x)
    model = keras.Model(inputs=input_layer, outputs=[distance_output, degree_output])

    model.summary()
    return model