
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers as layers
from tensorflow.keras.layers import GlobalMaxPooling2D, Activation, Dense, Conv1D, Conv2D, Dropout, Flatten, MaxPooling2D, BatchNormalization, GlobalMaxPooling1D
from tensorflow.keras import regularizers

def get_hyper_conv_classifier(hp):
    X_shape = (1,8,1000)
    y_shape = (4,)
    inspected_chanels= X_shape[1]
    input_length=     X_shape[2]

    resample = hp.Choice('resample', [1, 2, 5, 10])
    l2 =  hp.Choice('l2', [0.005, 0.0005, 0.000005, 0.])
    pool_1 = hp.Choice('pool_1', [10, 20, 50, 100])
    conv_1 = hp.Choice('conv_1', [10, 20, 50, 100])
    pool_2 = hp.Choice('pool_2', [1, 3, 4, 8])
    conv_2 = hp.Choice('conv_2', [10, 20, 50, 100])

    dense = hp.Choice('dense', [10, 20, 50, 100])
    dropout = hp.Choice('droupout', [0.1, 0.2, 0.3, 0.4, 0.5])

    flatten = hp.Choice('flatten', [True, False])

    input_layer = keras.Input(shape = (inspected_chanels,input_length), name='input')
    x = layers.Reshape((inspected_chanels,input_length,1))(input_layer)
    x     = layers.AveragePooling2D(pool_size=(1,resample))(x) # resample to 500

    

        
   
    x     = layers.Conv2D(conv_1, kernel_size=(1,pool_1), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    x     = layers.AveragePooling2D(pool_size=(1,pool_1))(x)

    x     = layers.Conv2D(conv_2, kernel_size=(pool_2,1), padding='same', activation='elu', kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.BatchNormalization()(x)
    x     = layers.AveragePooling2D(pool_size=(pool_2,1))(x)
    x     = layers.BatchNormalization()(x)
    if flatten:
        x     = layers.Flatten()(x)
    else:
        x     = tf.keras.layers.GlobalAveragePooling2D()(x)
    x     = layers.Dense(dense,kernel_regularizer=regularizers.l2(l2))(x)
    x     = layers.Dropout(dropout)(x)

    output = layers.Dense(y_shape[-1], activation='softmax')(x)
    model = keras.Model(inputs=input_layer, outputs=output)

    lr_schedule = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log"),
        decay_steps=10,
        decay_rate=hp.Choice('decay',[0.1,0.9]))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr_schedule),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model