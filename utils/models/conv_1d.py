
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import LSTM, MaxPooling1D, GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def conv_1d(X_shape, y_shape):
    inspected_chanels= X_shape[1]
    input_length=     X_shape[2]
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    x = tf.transpose(input_layer, perm=[0, 2, 1])
    print(x.shape)


    l2 = 0.005
        
   
    x     = layers.Conv1D(8, kernel_size=(4), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    #x     = layers.MaxPooling1D(pool_size=(5))(x)

    x     = layers.Conv1D(16, kernel_size=(4), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    #x     = layers.MaxPooling1D(pool_size=(5))(x)

    #x     = layers.Flatten()(x)
    x     = layers.Dropout(.1)(x)

    x     = LSTM(20, return_sequences=True)(x)
    x     = layers.MaxPooling1D(pool_size=(5))(x)
    x     = LSTM(20, return_sequences=True)(x)

    x     = tf.keras.layers.AveragePooling1D(4)(x)
    #x     = layers.Dense(5,kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.Flatten()(x)

    x     = layers.Dropout(.2)(x)

    output = layers.Dense(y_shape[-1], activation='softmax')(x)
    model = keras.Model(inputs=input_layer, outputs=output)

    model.summary()
    return model