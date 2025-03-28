# OSR: Optical String Reader for Guitar Tablature

A computer vision project that detects and converts guitar tab images into a custom structured notation. The system leverages image classification and machine learning to recognize chord positions from tab diagrams and translate them into fret-string or note-based representations.

---

## 🎯 Project Goal

Translate guitar tab images into a symbolic format like:

- Input: Image showing a **C major chord**
- Output: `1B`, `2D/E`, `3A/C`
  - Meaning: 1st fret on B string = C note, 2nd fret on D string = E, 3rd fret on A string = C

The system is designed to support **any valid guitar tab**, including:

- Alternate tunings (e.g., Drop D, DADGAD)
- Full fretboard range (not limited to the first 3 frets)
- Capo use and transpositions

---

## 🌐 Scope and Vision

OSR is not limited to any single notation or tuning. The project is intended to be:

- Tuning-agnostic
- Fret-range agnostic
- Capo-aware

### ♻️ Upcoming Enhancements

- ✅ Dynamic tuning support
- ✅ Capo-aware position translation
- ✅ Smart tab-to-notation mapping (e.g., from shape to musical context)

---

## 📁 Project Structure

| Path                            | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| `src/osr/`                      | Main Python package                                                        |
| `config.py`                    | Project-wide constants and paths                                           |
| `app.py`                       | CLI or main entry point (future use)                                       |
| `data/loader.py`              | Loads and labels training image data                                       |
| `models/cnn.py`               | Defines the CNN architecture using TensorFlow/Keras                        |
| `training/train.py`           | Trains the model and saves it                                              |
| `training/metrics.py`         | Metrics and performance evaluation (TBD)                                   |
| `inference/predict.py`        | Loads model and predicts from new images                                   |
| `utils/image_utils.py`        | OpenCV and Pillow helpers for preprocessing                                |
| `notebooks/`                  | Prototyping, exploratory analysis                                           |
| `data/tab_samples/`           | Labeled training data (e.g., c_major/, g_major/, etc.)                     |
| `data/raw/`                   | Unprocessed tab image samples                                              |
| `data/processed/`             | Preprocessed tab images (resized, binarized, etc.)                         |
| `pyproject.toml`              | Poetry configuration (dependencies, interpreter, paths)                   |

---

## ✅ Getting Started

### 1. Build File Structure

```powershell
mkdir -Force project/src/osr
mkdir -Force project/src/osr/{data,models,training,inference,utils}
mkdir -Force project/notebooks
mkdir -Force project/data/{raw,processed,tab_samples}
```

### 2. Create Module Files

```powershell
New-Item project/src/osr/__init__.py -ItemType File
New-Item project/src/osr/config.py -ItemType File
New-Item project/src/osr/app.py -ItemType File
New-Item project/src/osr/data/loader.py -ItemType File
New-Item project/src/osr/models/cnn.py -ItemType File
New-Item project/src/osr/training/train.py -ItemType File
New-Item project/src/osr/training/metrics.py -ItemType File
New-Item project/src/osr/inference/predict.py -ItemType File
New-Item project/src/osr/utils/image_utils.py -ItemType File
New-Item project/notebooks/experimentation.ipynb -ItemType File
New-Item project/README.md -ItemType File
New-Item project/.gitignore -ItemType File
```

### 3. Poetry Environment Setup

```powershell
# From OSR/ root
poetry lock --no-cache --regenerate   # Create a lock file

# Remove all self-installed plugins (clean reset)
poetry self clear-cache
poetry self remove poetry-plugin-shell
poetry self show plugins

poetry self add poetry-plugin-shell   # (Optional) adds `poetry shell`
poetry env use python3.9              # Select Python 3.9 for this project
poetry install                        # Install all dependencies
```

Add your packages in `pyproject.toml`:

```toml
dependencies = [
  "tensorflow>=2.19.0,<3.0.0",
  "opencv-python>=4.11.0.86,<5.0.0.0",
  "pillow>=11.1.0,<12.0.0",
  "numpy>=1.26.0,<2.2.0",
  "matplotlib>=3.5,<3.7",
  "rich>=13.7.0,<14.0.0",
  "python-dotenv>=1.0.1,<2.0.0"
]
```

---

## ⚖️ Running Training

Run training from the OSR root directory:

```powershell
$env:PYTHONPATH="project/src"
python -m osr.training.train
```

This uses the correct `src/` layout and keeps your imports clean and modular.

---

## 🔮 Running Prediction

To predict from a new image:

```powershell
$env:PYTHONPATH="project/src"
python -m osr.inference.predict project/data/tab_samples/c_major/sample1.jpg
```

You’ll see something like:

```powershell
[INFO] Loading model...
[INFO] Loading image from ...
[INFO] Predicting...
[RESULT] Predicted class: c_major (confidence: 0.92)
```

---

## 🚀 Tech Stack

- **TensorFlow** – Deep learning framework
- **OpenCV** – Image preprocessing and transformation
- **Pillow** – Image loading and resizing
- **Poetry** – Dependency and environment management
- **VS Code** – IDE with Pylance for linting/type checking

---

## 📊 Future Improvements

- Add data augmentation to avoid overfitting
- Support multi-label classification for individual finger/string/fret detection
- Export to various formats (MIDI, MusicXML, tab notation)
- Web frontend (Streamlit or FastAPI)

---

## 📆 Last Verified

> ✅ Last verified working on **Windows 11 + Python 3.9 + Poetry 1.8.2 + TensorFlow 2.19.0**
