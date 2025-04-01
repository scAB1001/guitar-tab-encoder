# cnn.py
"""
Defines the CNN architecture for detecting tab positions in guitar tab images.
"""
from keras import layers, models, Input

def build_cnn_model(input_shape=(128, 128, 1), num_classes=24):
    model = models.Sequential([
        Input(shape=input_shape),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(32, activation='relu'),  # Try 64 & 32 size
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

