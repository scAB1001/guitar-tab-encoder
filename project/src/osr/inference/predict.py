# predict.py
"""
Loads a trained CNN model and predicts the chord class of a guitar tab image.
"""

import os
import sys
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
from osr.utils.image_utils import load_image
from osr.config import LATEST_MODEL_PATH, IMG_SIZE
from osr.data.loader import load_training_data

def predict(image_path: str, model_path: str = LATEST_MODEL_PATH):
    """Loads model, preprocesses image, predicts class label."""
    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        sys.exit(1)

    print("[INFO] Loading model...")
    model = load_model(model_path)

    print(f"[INFO] Loading image from: {image_path}")
    image = load_image(image_path, size=(IMG_SIZE, IMG_SIZE))
    image = image.reshape(1, IMG_SIZE, IMG_SIZE, 1)  # Batch dimension

    print("[INFO] Loading label map...")
    _, _, _, reverse_label_map = load_training_data()

    print("[INFO] Predicting...")
    predictions = model.predict(image)
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_index])
    predicted_label = reverse_label_map.get(predicted_index, "Unknown")

    print(f"[RESULT] Predicted chord: {predicted_label} (confidence: {confidence:.2f})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m osr.inference.predict <image_path>")
        sys.exit(1)

    predict(sys.argv[1])
