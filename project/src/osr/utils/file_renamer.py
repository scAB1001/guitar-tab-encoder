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
    Rename all files in the specified chord directory with a standardized naming pattern.
    """
    dir_path = BASE_PATH / category / chord_name
    base_file_name = f"{chord_name}_tab_"

    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Directory not found: {dir_path}")
        return

    for i, file in enumerate(sorted(dir_path.iterdir())):
        if file.is_file():
            new_name = f"{base_file_name}{i + 1}.png"
            new_path = dir_path / new_name
            
            if file.name == new_name:
                print(f"Files for {chord_name}/ have already been converted.")
                return

            try:
                file.rename(new_path)
                print(f"Renamed: {file.name} -> {new_name}")
            except PermissionError:
                print(f"Permission denied: {file}")
            except OSError as error:
                print(f"Error renaming {file}: {error}")


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