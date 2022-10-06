
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import Sequential
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import Conv1D, AveragePooling1D, TimeDistributed, GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def cnn_lstm(X_shape, y_shape):
    inspected_chanels= X_shape[1]
    input_length=     X_shape[2]
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    # x = layers.Reshape((inspected_chanels,input_length,1))(input_layer)
    # x = tf.transpose(x, perm=[0, 2, 1, 3])

    x = tf.transpose(input_layer, perm=[0, 2, 1])
    print(x.shape)


    l2 = 0.005
        
    cnn = Sequential()
    cnn.add(layers.Conv1D(32, kernel_size=(4), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2)))
    cnn.add(layers.BatchNormalization())
    cnn.add(layers.AveragePooling1D(pool_size=(4)))

    cnn.add(layers.Conv1D(64, kernel_size=(4), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2)))
    cnn.add(layers.BatchNormalization())
    cnn.add(layers.AveragePooling1D(pool_size=(2)))
    cnn.add(layers.BatchNormalization())
    cnn.add(layers.Flatten())

    dense = Sequential()
    dense.add(layers.Dense(128, activation='elu', kernel_regularizer=regularizers.l2(l2)))

    #x = TimeDistributed(cnn)(x)

    x  = TimeDistributed(dense)(x)
    print(x.shape)
    x     = tf.keras.layers.LSTM(20)(x)
    #x     = tf.keras.layers.LSTM(20)(x)

    #x     = layers.Flatten()(x)
    #x     = tf.keras.layers.GlobalAveragePooling2D()(x)
    x     = layers.Dense(20,kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.Dropout(.1)(x)

    output = layers.Dense(y_shape[-1], activation='softmax')(x)
    model = keras.Model(inputs=input_layer, outputs=output)

    model.summary()
    return model