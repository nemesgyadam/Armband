import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_dense_classifier(X_shape, y_shape):
    inspected_chanels= X_shape[1]
    input_length=     X_shape[2]
    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    x = layers.Flatten()(input_layer)

    l2 = 0.001
    x     = layers.Dense(5,kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    x     = layers.Dropout(.3)(x)


    output = layers.Dense(y_shape[-1], activation='softmax')(x)
    model = keras.Model(inputs=input_layer, outputs=output)

    model.summary()
    return model