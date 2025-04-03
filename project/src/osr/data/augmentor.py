import tensorflow as tf
from keras import layers as l

def get_augmentation_pipeline():
    """
    Returns a sequential layer that performs data augmentation.
    """
    return tf.keras.Sequential([
        l.RandomRotation(0.02),
        l.RandomZoom(0.1),
        l.RandomContrast(0.1),
        l.RandomTranslation(0.02, 0.02)
    ])
