import os
import random
from PIL import Image, ImageDraw
from osr.config import DATA_DIR

def create_synthetic_tab_image(width=300, height=100) -> Image.Image:
    """
    Creates a basic synthetic guitar tab image with lines and randomly placed fret dots.
    """
    img = Image.new("L", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Draw 6 horizontal lines (strings)
    for i in range(6):
        y = 20 + i * 12
        draw.line((10, y, width - 10, y), fill=0)

    # Add 2–4 random dots for fretted notes
    for _ in range(random.randint(2, 4)):
        string = random.randint(0, 5)
        fret = random.randint(1, 4)
        y = 20 + string * 12
        x = 20 + fret * 40
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=0)

    return img


def is_leaf_dir(path: str) -> bool:
    """Returns True if the directory has no subdirectories (i.e., it's a chord folder)."""
    return all(not os.path.isdir(os.path.join(path, entry)) for entry in os.listdir(path))


def populate_synthetic_tabs(target_count_per_class=20):
    """
    For each chord folder in tab_samples/, generate synthetic tab images
    until the folder contains at least `target_count_per_class` total.
    """
    print(f"[INFO] Populating synthetic tabs in: {DATA_DIR}")

    for root, dirs, _ in os.walk(DATA_DIR):
        for chord_dir in dirs:
            full_path = os.path.join(root, chord_dir)

            if not is_leaf_dir(full_path):
                continue  # skip intermediate folders like 'add/', 'sus/', etc.

            existing = [f for f in os.listdir(full_path) if f.lower().endswith((".png", ".jpg"))]
            n_existing = len(existing)

            if n_existing >= target_count_per_class:
                print(f"[SKIP] {chord_dir} already has {n_existing} images")
                continue

            needed = target_count_per_class - n_existing
            print(f"[GEN] {chord_dir} → {needed} synthetic samples")

            for i in range(needed):
                filename = f"{chord_dir}_tab_{n_existing + i + 1}.png"
                save_path = os.path.join(full_path, filename)

                img = create_synthetic_tab_image()
                img.save(save_path)

if __name__ == "__main__":
    populate_synthetic_tabs(target_count_per_class=20)
