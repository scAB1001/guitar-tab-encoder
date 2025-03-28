# config.py
"""
Project-wide configuration constants.
"""

IMG_SIZE = 128  # Resize input images to 128x128

# Note: Expected to contain category subfolders (e.g., major/, minor/) each containing class folders
DATA_DIR = "project/data/tab_samples"

MODEL_DIR = "saved_models"
ALL_VERSIONS_PATH = "saved_models/all_versions"
LATEST_MODEL_PATH = f"{MODEL_DIR}/cnn_model_latest.keras"
BEST_MODEL_PATH = f"{MODEL_DIR}/cnn_model_best.keras"