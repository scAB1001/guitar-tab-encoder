# cnn.py
"""
Defines the CNN architecture for detecting tab positions in guitar tab images.
"""

from keras import l as l, models, Input
from osr.data.augmentor import get_augmentation_pipeline

def build_cnn_model(input_shape=(128, 128, 1), num_classes=24):
    """
    Builds and returns a refined CNN model with:
    - BatchNorm + Dropout (better generalization)
    - 3 conv l (deeper feature extraction)
    - Wider dense layer (more expressive)
    """
    data_augmentation = get_augmentation_pipeline()
    
    model = models.Sequential([
        Input(shape=input_shape),
        data_augmentation,  # Only applies during training
        
        # Block 1
        l.Conv2D(32, (3, 3), padding='same', activation='relu'),
        l.BatchNormalization(),
        l.MaxPooling2D((2, 2)),
        l.Dropout(0.2),

        # Block 2
        l.Conv2D(64, (3, 3), padding='same', activation='relu'),
        l.BatchNormalization(),
        l.MaxPooling2D((2, 2)),
        l.Dropout(0.25),

        # Block 3
        l.Conv2D(128, (3, 3), padding='same', activation='relu'),
        l.BatchNormalization(),
        l.MaxPooling2D((2, 2)),
        l.Dropout(0.3),

        # Fully Connected
        l.Flatten(),
        l.Dense(128, activation='relu'),
        l.Dropout(0.4),
        l.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam', 
        loss='sparse_categorical_crossentropy', 
        metrics=['accuracy'])
    
    return model

