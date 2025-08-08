# custom_objects.py

import tensorflow.keras.backend as K
from keras.saving import register_keras_serializable

@register_keras_serializable()
def sum_over_time(x):
    return K.sum(x, axis=1)

@register_keras_serializable()
def sum_shape(input_shape):
    return (input_shape[0], input_shape[2])
