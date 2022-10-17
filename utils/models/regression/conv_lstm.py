
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_model(end_label = True, targets = ['Distance', 'Degree']):
    inspected_chanels= 8
    input_length=     1000
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')

    x = tf.transpose(input_layer, perm=[0, 2, 1])
    x = layers.Reshape((input_length,inspected_chanels,1))(x)


    l2 =0.0001
    conv_params = 200  
    x = layers.Conv2D(conv_params, kernel_size=(8,10), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x = layers.MaxPooling2D(pool_size=(1,10), data_format = 'channels_first')(x)
    x = layers.Reshape((100, 10 * 8*20))(x)
    x  = tf.keras.layers.LSTM(200, kernel_regularizer=regularizers.l2(l2), dropout = 0.1, recurrent_dropout = 0.)(x)


    

    distance = layers.Dense(50, kernel_regularizer=regularizers.l2(l2))(x)
    distance = layers.Dense(10, kernel_regularizer=regularizers.l2(l2))(distance)



    degree = layers.Dense(50, kernel_regularizer=regularizers.l2(l2))(x)
    degree = layers.Dense(10, kernel_regularizer=regularizers.l2(l2))(degree)



    if end_label:
        distance_output = layers.Dense(1, activation = 'sigmoid', name = 'distance')(distance)
        degree_output = layers.Dense(1,activation = 'tanh', name = 'degree')(degree)
    else:
        distance_output = layers.Dense(500, activation = 'sigmoid')(distance)
        degree_output = layers.Dense(500,activation = 'tanh', name = 'degree')(degree)
       
    outputs = []
    if 'Distance' in targets:
        outputs.append(distance_output)
    if 'Degree' in targets:
        outputs.append(degree_output)
    model = keras.Model(inputs=input_layer, outputs=outputs)

    #model.summary()
    return model