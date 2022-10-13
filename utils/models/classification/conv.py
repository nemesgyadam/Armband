
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_model(end_label = True, targets = ['Distance', 'Degree']):
    inspected_chanels= 8
    input_length=     500
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    x = layers.Reshape((inspected_chanels,input_length,1))(input_layer)
    #x = layers.MaxPooling1D(pool_size= 1, data_format = 'channels_first')(input_layer)
   
    l2 =0.0001

    x = layers.Conv2D(200, kernel_size=(8,10), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)

    
    x = layers.Dropout(.2)(x)
    x = layers.GlobalMaxPooling2D()(x)
    
    # distance = layers.Dense(50, activation='relu', kernel_regularizer=regularizers.l2(l2))(x)
    # distance = layers.Dropout(.2)(distance)
    # distance= layers.GlobalMaxPooling1D()(distance)
    distance = layers.Dense(50, kernel_regularizer=regularizers.l2(l2))(x)
    distance = layers.Dense(10, kernel_regularizer=regularizers.l2(l2))(distance)


    # degree = layers.Dense(20, activation='relu', kernel_regularizer=regularizers.l2(l2))(x)
    # degree = layers.Dropout(.2)(degree)
    # degree= layers.GlobalMaxPooling1D()(degree)
    degree = layers.Dense(50, kernel_regularizer=regularizers.l2(l2))(x)
    degree = layers.Dense(10, kernel_regularizer=regularizers.l2(l2))(degree)



    if end_label:
        distance_output = layers.Dense(1, activation = 'sigmoid', name = 'distance')(distance)
        degree_output = layers.Dense(3,activation = 'softmax', name = 'degree')(degree)
        #degree_output = layers.Dense(3, activation = 'tanh', name ='degree')(degree)
        #degree_output = layers.Dense(1, activation = 'sigmoid', name ='degree')(degree)
    else:
        distance_output = layers.Dense(500, activation = 'sigmoid')(distance)
        degree_output = layers.Dense(500,activation = 'softmax', name = 'degree')(degree)
        #degree_output = layers.Dense(500, activation = 'tanh', name ='degree')(degree)
        #degree_output = layers.Dense(500, activation = 'sigmoid', name ='degree')(degree)
        
    outputs = []
    if 'Distance' in targets:
        outputs.append(distance_output)
    if 'Degree' in targets:
        outputs.append(degree_output)
    model = keras.Model(inputs=input_layer, outputs=outputs)

    model.summary()
    return model