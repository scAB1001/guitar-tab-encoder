# image_utils.py
"""
Image preprocessing utilities using Pillow and OpenCV.
"""

from PIL import Image
import numpy as np
import cv2

def load_image(filepath: str, size=(128, 128)) -> np.ndarray:
    """
    Loads and resizes an image as grayscale.
    """
    image = Image.open(filepath).convert("L").resize(size)
    return np.array(image) / 255.0

def binarize_image(image: np.ndarray, threshold=127) -> np.ndarray:
    """
    Applies binary thresholding to enhance lines and dots (tab markers).
    """
    _, binary = cv2.threshold((image * 255).astype("uint8"), threshold, 255, cv2.THRESH_BINARY)
    return binary

def show_image(image: np.ndarray, title="Image"):
    """
    Displays image using OpenCV.
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
