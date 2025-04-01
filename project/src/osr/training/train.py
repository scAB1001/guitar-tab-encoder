# train.py
"""
Trains the CNN model on labeled tab images.
"""
import os
from datetime import datetime as dt
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from osr.models.cnn import build_cnn_model
from osr.data.loader import load_training_data
from osr.config import IMG_SIZE, ALL_VERSIONS_PATH, LATEST_MODEL_PATH, BEST_MODEL_PATH

def train():
    print("[INFO] Loading training data...")
    X_train, y_train, label_map, _ = load_training_data()
    print(f"[INFO] Classes found: {label_map}")

    print("[INFO] Building model...")
    model = build_cnn_model(input_shape=(IMG_SIZE, IMG_SIZE, 1), num_classes=len(label_map))

    print("[INFO] Training model...")
    history = model.fit(
        X_train, 
        y_train, 
        epochs=10, 
        batch_size=32, 
        validation_split=0.2, 
        verbose=1
    )

    # Generate timestamped filename
    timestamp = dt.now().strftime("%Y-%m-%d-%H%M")
    versioned_model_path = os.path.join(ALL_VERSIONS_PATH, f"cnn_model_{timestamp}.keras")

    # Save all 3 versions
    print(f"[INFO] Saving model to: {versioned_model_path}")
    model.save(versioned_model_path)

    print(f"[INFO] Saving model as latest: {LATEST_MODEL_PATH}")
    model.save(LATEST_MODEL_PATH)

    # Check if this is the best so far (based on val_accuracy)
    val_acc = history.history["val_accuracy"][-1]

    if not os.path.exists(BEST_MODEL_PATH):
        save_best = True
    else:
        from tensorflow.keras.models import load_model # type: ignore
        best_model = load_model(BEST_MODEL_PATH)
        best_val_acc = best_model.evaluate(X_train, y_train, verbose=0)[1]
        save_best = val_acc > best_val_acc

    if save_best:
        print(f"[INFO] New best model found (val_accuracy={val_acc:.4f}) → saved to: {BEST_MODEL_PATH}")
        model.save(BEST_MODEL_PATH)
    else:
        print(f"[INFO] Current model val_accuracy={val_acc:.4f} did not improve on best model.")

if __name__ == "__main__":
    train()
