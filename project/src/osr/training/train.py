"""
Trains the CNN model on labeled tab images.
"""
import os, json
from datetime import datetime as dt
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from osr.models.cnn import build_cnn_model
from osr.data.loader import load_training_data
from osr.training.metrics import plot_training_curves
from osr.config import IMG_SIZE, ALL_VERSIONS_PATH, LATEST_MODEL_PATH, BEST_MODEL_PATH


def save_label_map(label_map: dict, path: str):
    with open(path, "w") as f:
        json.dump(label_map, f, indent=2)


def train():

    def save_model_instance(model_path: str):
        model.save(model_path)
        label_path = model_path.replace(".keras", "_labels.json")
        save_label_map(label_map, label_path)
        return model_path
    
    print("[INFO] Loading training data...")
    X_train, y_train, label_map, _ = load_training_data()
    print(f"[INFO] Classes found: {json.dumps(label_map, indent=2)}")

    print("\n[INFO] Building model...")
    model = build_cnn_model(input_shape=(IMG_SIZE, IMG_SIZE, 1), num_classes=len(label_map))

    print("[INFO] Training model...")
    history = model.fit(
        X_train, 
        y_train, 
        epochs=10, 
        batch_size=32, 
        validation_split=0.1, 
        verbose=1
    )

    # Generate timestamped filename
    timestamp = dt.now().strftime("%Y-%m-%d-%H%M")
    versioned_model_path = os.path.join(ALL_VERSIONS_PATH, f"cnn_model_{timestamp}.keras")

    # Save all 3 versions
    print(f"\n[INFO] Saving model to: {save_model_instance(versioned_model_path)}")

    print(f"[INFO] Saving model as latest: {save_model_instance(LATEST_MODEL_PATH)}")

    # Check if this is the best so far (based on val_accuracy)
    val_acc = history.history["val_accuracy"][-1]
    save_best = False

    if not os.path.exists(BEST_MODEL_PATH):
        save_best = True
    else:
        from tensorflow.keras.models import load_model  # type: ignore
        try:
            best_model = load_model(BEST_MODEL_PATH)
            if best_model.output_shape[-1] != len(label_map):
                print("[WARN] Best model class count doesn't match current label map — removing old best model.")
                os.remove(BEST_MODEL_PATH)
                save_best = True
            else:
                best_val_acc = best_model.evaluate(X_train, y_train, verbose=0)[1]
                save_best = val_acc > best_val_acc
        except Exception as e:
            print(f"[ERROR] Failed to load best model: {e}")
            os.remove(BEST_MODEL_PATH)
            save_best = True

    if save_best:
        print(f"[INFO] New best model found (val_accuracy={val_acc:.4f}) → saved to: {save_model_instance(BEST_MODEL_PATH)}")
    else:
        print(f"[INFO] Current model val_accuracy={val_acc:.4f} did not improve on best model.")
    
    print(f"\n[INFO] Generating training metrics...")
    plot_training_curves(history)
    

if __name__ == "__main__":
    train()
