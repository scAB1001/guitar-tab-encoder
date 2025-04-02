# loader.py
"""
Data loading utilities for tab training images.
Each subfolder under DATA_DIR represents a class (e.g., c_major, g_major, etc.).
"""

import os
import numpy as np
from osr.utils.image_utils import load_image
from osr.config import DATA_DIR, IMG_SIZE

def load_training_data():
    """
    Loads grayscale image data and numerical labels from nested chord folders under tab_samples/.

    Expected layout:
        tab_samples/
        ├── major/
        │   ├── a_major/
        │   └── g_major/
        ├── minor/
        │   ├── e_minor/
        │   └── a_minor/
        └── sus/
            └── d_sus4/

    Returns:
        X (np.ndarray): Image tensors, shape (N, IMG_SIZE, IMG_SIZE, 1)
        y (np.ndarray): Integer labels
        label_map (dict): {label_name: index}
        reverse_label_map (dict): {index: label_name}
    """
    X, y = [], []
    chord_folders = []

    # Recursively find valid leaf folders (folders that contain image files)
    for root, dirs, files in os.walk(DATA_DIR):
        image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        if image_files:
            chord_folders.append(root)

    # Create label map using folder names only (e.g. "a_major")
    class_names = sorted([os.path.basename(path) for path in chord_folders])
    label_map = {name: idx for idx, name in enumerate(class_names)}
    reverse_label_map = {idx: name for name, idx in label_map.items()}

    for folder_path in chord_folders:
        label_name = os.path.basename(folder_path)
        label = label_map[label_name]
        
        for file in os.listdir(folder_path):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(folder_path, file)
                img = load_image(img_path, size=(IMG_SIZE, IMG_SIZE))
                X.append(img)
                y.append(label)

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y = np.array(y)
    
    return X, y, label_map, reverse_label_map
