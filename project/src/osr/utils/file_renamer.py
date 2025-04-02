import os
from pathlib import Path
from typing import List

BASE_PATH = Path(r"C:\Users\abazigos001\source\repos\self\OSR\project\data\tab_samples")

def print_folder_sizes(base_path: Path) -> None:
    """
    Walk through the directory tree and print the size of each folder.
    """
    for root, _, files in os.walk(base_path, followlinks=True):
        root_path = Path(root)
        total_size = sum((root_path / f).stat().st_size for f in files)
        relative_path = root_path.relative_to(base_path)
        print(f"{relative_path} consumes {total_size} bytes in {len(files)} non-directory files")


def collect_chord_dirs(only_non_empty: bool = False) -> List[Path]:
    """
    Collect all chord label folders (leaf directories).
    If only_non_empty is True, skip folders without files.
    """
    chord_folders = []
    for root, dirs, _ in os.walk(BASE_PATH):
        for d in dirs:
            full_path = Path(root) / d
            if not only_non_empty or any(full_path.iterdir()):
                chord_folders.append(full_path)

    for folder in chord_folders:
        print(folder.relative_to(BASE_PATH))
    
    return chord_folders


def rename_screenshots_in_dir(category: str, chord_name: str) -> None:
    """
    Renames files in the given chord folder using basic string slicing,
    ensuring consistent numeric suffixes without gaps or duplicates.
    """
    dir_path = BASE_PATH / category / chord_name
    base_file_name = f"{chord_name}_tab_"

    if not dir_path.exists() or not dir_path.is_dir():
        print(f"[SKIP] Directory not found: {dir_path}")
        return

    def extract_number(filename: str) -> int:
        """
        Extracts the numeric suffix from a filename assuming format:
        <chord_name>_tab_<number>.png
        """
        try:
            stem = filename.rsplit(".", 1)[0]              # Remove extension
            num_part = stem.rsplit("_", 1)[-1]             # Get number after last '_'
            return int(num_part)
        except (ValueError, IndexError):
            return float('inf')  # Push unmatchables to the end

    # Get sorted list of files by suffix number
    files = sorted(
        [f for f in dir_path.iterdir() if f.is_file() and f.suffix == ".png"],
        key=lambda f: extract_number(f.name)
    )

    for i, file in enumerate(files, start=1):
        new_name = f"{base_file_name}{i}.png"
        new_path = dir_path / new_name

        if file.name != new_name:
            try:
                file.rename(new_path)
                print(f"[RENAME] {file.name} → {new_name}")
            except PermissionError:
                print(f"[ERROR] Permission denied: {file}")
            except OSError as e:
                print(f"[ERROR] Failed to rename {file}: {e}")
        else:
            print(f"[SKIP] Already correct: {file.name}")


def rename_entire_chord_type(chord_type: str) -> None:
    chord_type_path = BASE_PATH / chord_type
    
    if not chord_type_path.exists() or not chord_type_path.is_dir():
        print(f"Directory not found: {chord_type_path}")
        return
    
    for chord in chord_type_path.iterdir():
        if chord.is_dir():
            rename_screenshots_in_dir(chord_type, chord.name)
    

def rename_chords() -> None:
    for dir in BASE_PATH.iterdir():
        if dir.is_dir():
            rename_entire_chord_type(dir.name)

if __name__ == "__main__":
    # print_folder_sizes(BASE_PATH)
    # print(collect_chord_dirs(only_non_empty=True))
    # rename_screenshots_in_dir("add", "d_add9")
    # rename_entire_chord_type("add")
    rename_chords()