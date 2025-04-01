import os
from typing import Optional
import matplotlib.pyplot as plt
from datetime import datetime


def plot_training_curves(history, output_dir: Optional[str] = "project/reports", prefix: str = "training") -> None:
    """
    Plots and saves training and validation accuracy and loss curves.

    Args:
        history: Keras History object returned by model.fit().
        output_dir: Directory to save the plot image.
        prefix: Filename prefix (timestamp will be added automatically).
    """
    if not hasattr(history, "history"):
        raise ValueError("Expected a Keras History object with a `.history` attribute.")

    history_data = history.history
    acc = history_data.get("accuracy", [])
    val_acc = history_data.get("val_accuracy", [])
    loss = history_data.get("loss", [])
    val_loss = history_data.get("val_loss", [])
    epochs = range(1, len(acc) + 1)

    # Start plotting
    plt.figure(figsize=(14, 6))
    plt.suptitle("Model Training Summary", fontsize=16, fontweight="bold")

    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, label="Train Accuracy", color="#1f77b4", linewidth=2)
    if val_acc:
        plt.plot(epochs, val_acc, label="Val Accuracy", color="#ff7f0e", linestyle="--", linewidth=2)
    plt.title("Accuracy per Epoch", fontsize=13)
    plt.xlabel("Epoch", fontsize=11)
    plt.ylabel("Accuracy", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend(loc="lower right")
    plt.xticks(epochs)
    plt.ylim(0, 1.05)

    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label="Train Loss", color="#2ca02c", linewidth=2)
    if val_loss:
        plt.plot(epochs, val_loss, label="Val Loss", color="#d62728", linestyle="--", linewidth=2)
    plt.title("Loss per Epoch", fontsize=13)
    plt.xlabel("Epoch", fontsize=11)
    plt.ylabel("Loss", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend(loc="upper right")
    plt.xticks(epochs)

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for suptitle

    # Save figure
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{prefix}_curves_{timestamp}.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"[INFO] Training curves saved to: {save_path}")
