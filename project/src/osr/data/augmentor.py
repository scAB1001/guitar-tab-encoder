import tensorflow as tf

def get_augmentation_pipeline():
    """
    Returns a sequential layer that performs data augmentation.
    """
    return tf.keras.Sequential([
        tf.keras.layers.RandomRotation(0.02),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1),
        tf.keras.layers.RandomTranslation(0.02, 0.02)
    ])
