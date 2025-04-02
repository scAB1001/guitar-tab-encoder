import os
import random
from typing import Optional
from PIL import Image, ImageDraw
from osr.config import DATA_DIR

# Define standard string labels (high E to low E)
STRING_LABELS = ['e', 'B', 'G', 'D', 'A', 'E']
STRING_TO_INDEX = {s: i for i, s in enumerate(STRING_LABELS)}


def interpret_chord(chord: str) -> list[tuple[int, str]]:
    """
    Parses a chord string into a list of (fret, string) tuples.
    - Supports multi-digit frets (e.g. '10A')
    - Allows delimiters (space, comma, etc.)
    - Interprets 'E' alone as (0, 'E')
    """
    result = []
    buffer = ""  # collect characters between delimiters

    for char in chord:
        
        # Add the fret/string to buffer
        if char.isalnum():
            buffer += char
            
        # Encountered whitespace, must be end of note    
        else:
            if buffer:
                result.append(parse_fret_string(buffer))
                buffer = ""  # Reset the buffer
    
    # If there's anything left in the buffer, parse and append it
    if buffer:
        result.append(parse_fret_string(buffer))

    return result


def parse_fret_string(token: str) -> tuple[int, str]:
    """
    Converts a string like '2B' or '10A' to (2, 'B').
    If the token is just a string letter (e.g., 'E'), it's treated as open string (0 fret).
    """
    if token.isalpha() and len(token) == 1:
        return (0, token())

    # Find first letter index
    for i, ch in enumerate(token):
        if ch.isalpha():
            fret = int(token[:i]) if i > 0 else 0
            string = token[i:]
            return (fret, string)

    raise ValueError(f"Invalid token: '{token}'")



def create_synthetic_tab_image(
    fret_positions: Optional[list[tuple[int, int]]] = None,
    width: int = 320,
    height: int = 120,
    frets: int = 5
) -> Image.Image:
    """
    Creates a synthetic fretboard tab image with strings, frets, and optional finger positions.

    Args:
        fret_positions: List of (fret, string_label) tuples, e.g. (1, 'B')
        width: Total image width
        height: Total image height
        frets: Number of vertical frets to draw
    """
    margin = 20
    fret_spacing = (width - 2 * margin) // frets
    string_spacing = (height - 2 * margin) // 5

    img = Image.new("L", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Draw frets (vertical lines)
    for i in range(frets + 1):
        x = margin + i * fret_spacing
        draw.line([(x, margin), (x, height - margin)], fill=0, width=1)

    # Draw strings (horizontal lines)
    for i in range(6):
        y = margin + i * string_spacing
        draw.line([(margin, y), (width - margin, y)], fill=0, width=2)

    # Draw finger positions (circles)
    if fret_positions is None:
        fret_positions = [
            (random.randint(1, frets), random.choice(STRING_LABELS))
            for _ in range(random.randint(2, 4))
        ]

    for fret_num, string_label in fret_positions:
        string_idx = STRING_TO_INDEX[string_label]
        y = margin + string_idx * string_spacing
        x = margin + fret_num * fret_spacing - fret_spacing // 2
        r = 6
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=0)

    return img


def is_leaf_dir(path: str) -> bool:
    """Returns True if the directory has no subdirectories (i.e., it's a chord folder)."""
    return all(not os.path.isdir(os.path.join(path, entry)) for entry in os.listdir(path))


def populate_synthetic_tabs(target_count_per_class=20):
    """
    For each chord folder in tab_samples/, generate synthetic tab images
    until the folder contains at least target_count_per_class total.
    """
    print(f"[INFO] Populating synthetic tabs in: {DATA_DIR}")

    for root, dirs, _ in os.walk(DATA_DIR):
        for chord_dir in dirs:
            full_path = os.path.join(root, chord_dir)

            if not is_leaf_dir(full_path):
                continue

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


def preview_chord_image(interactive_frets: list[tuple[int, str]]):
    """
    Quick preview: generates and shows an image for a specified chord shape.
    Tuple format: (fret_number, string_label), e.g. (1, 'B')
    """
    img = create_synthetic_tab_image(fret_positions=interactive_frets)
    # img.show()
    
    # img.close()


if __name__ == "__main__":
    # populate_synthetic_tabs(target_count_per_class=20)

    # Interactive preview example
    # Example: C major = 1st fret on B, 2nd fret on D, 3rd fret on A
    preview_chord_image([(1, 'B'), (1, 'G'), (2, 'D'), (3, 'A')])
    
    # interpret_chord("1B 2D 3A")
    interpret_chord("1BG, 2D, 3A, 4eE")