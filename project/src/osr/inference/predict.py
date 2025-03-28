# predict.py
"""
Loads a trained CNN model and predicts the class of a guitar tab image.
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import sys
import numpy as np
from tensorflow.keras.models import load_model
from osr.utils.image_utils import load_image
from osr.config import MODEL_PATH, IMG_SIZE
from osr.data.loader import load_training_data


def predict(image_path: str):
    # Load trained model
    print("[INFO] Loading model...")
    model = load_model(MODEL_PATH)

    # Load and preprocess input image
    print(f"[INFO] Loading image from {image_path}...")
    image = load_image(image_path, size=(IMG_SIZE, IMG_SIZE))
    image = image.reshape(1, IMG_SIZE, IMG_SIZE, 1)  # Add batch and channel dims

    # Get class name mapping
    _, _, _, reverse_label_map = load_training_data()

    # Predict
    print("[INFO] Predicting...")
    predictions = model.predict(image)
    predicted_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_index])
    label_name = reverse_label_map[predicted_index]

    print(f"[RESULT] Predicted class: {label_name} (confidence: {confidence:.2f})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m osr.inference.predict <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    predict(image_path)
