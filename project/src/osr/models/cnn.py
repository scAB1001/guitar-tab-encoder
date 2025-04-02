# cnn.py
"""
Defines the CNN architecture for detecting tab positions in guitar tab images.
"""

from keras import layers, models, Input
from osr.data.augmentor import get_augmentation_pipeline

def build_cnn_model(input_shape=(128, 128, 1), num_classes=24):
    """
    Builds and returns a refined CNN model with:
    - BatchNorm + Dropout (better generalization)
    - 3 conv layers (deeper feature extraction)
    - Wider dense layer (more expressive)
    """
    data_augmentation = get_augmentation_pipeline()
    
    model = models.Sequential([
        Input(shape=input_shape),
        data_augmentation,  # Only applies during training
        
        # Block 1
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),

        # Block 2
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Block 3
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),

        # Fully Connected
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam', 
        loss='sparse_categorical_crossentropy', 
        metrics=['accuracy'])
    
    return model

