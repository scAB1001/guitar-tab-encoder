# OSR: Optical String Reader for Guitar Tablature

A computer vision pipeline that detects and converts guitar tab images into a structured symbolic notation. The system uses convolutional neural networks (CNNs) and image classification to recognize chord positions and translate them into a concise representation like `1B`, `2D/E`, `3A/C`.

---

## 🎯 Project Goals

- Recognize fretted positions from guitar chord diagrams
- Translate those positions into notation like `1B` (1st fret, B string)
- Support **any valid tab**, not just standard tuning or first-position chords

### Supported Notation Examples

- `1BD` → 1st fret, B and D string
- `3A/C` → 3rd fret on A string producing note C
- `0E` or `E` → Open E string

### Intelligent Design Goals

- ✅ Alternate tuning and capo handling
- ✅ Full fretboard support
- ✅ Encoding for output such as string-note or string-fret

---

## 📦 Current Achievements

- ✅ Functional CNN model using Keras + TensorFlow
- ✅ Augmentation pipeline for more robust learning
- ✅ Synthetic tab generator with fretboard + finger positions
- ✅ CLI-based trainer and predictor
- ✅ Modular project layout using Poetry
- ✅ Automatic best model tracking + visual metric plots

---

## 📁 Project Structure

```plaintext
osr/
├── pyproject.toml              # Poetry setup and dependency management
└── project/
    ├── src/osr/
    │   ├── app.py              # CLI entry point
    │   ├── config.py           # Global constants
    │   ├── data/
    │   │   ├── loader.py       # Data loading for training
    │   │   └── generator.py    # Synthetic image generator
    │   ├── models/
    │   │   └── cnn.py          # CNN model definition
    │   ├── training/
    │   │   ├── train.py        # Training logic
    │   │   └── metrics.py      # Metric plotting
    │   ├── inference/
    │   │   └── predict.py      # Inference script
    │   ├── utils/
    │   │   └── image_utils.py  # Preprocessing helpers (OpenCV + Pillow)
    ├── data/
    │   ├── tab_samples/        # Chord-labeled image folders
    │   ├── raw/                # Raw input samples
    │   └── processed/          # Preprocessed image output
    ├── saved_models/           # Trained model versions
    ├── reports/                # Training visualizations (plots)
    └── notebooks/              # Prototyping + exploration
```

---

## 🚀 Quick Start

### Poetry Setup

```powershell
# From OSR/ root directory
poetry self add poetry-plugin-shell   # (Optional)
poetry lock --no-cache --regenerate   # Create a lock file
poetry self show plugins

poetry env use python3.9
poetry install                        # Install dependencies
```

### Running the program

```powershell
# Trainer
python -m osr.training.train

# Generator
python -m osr.data.generator

# Predict from an image
python -m osr.inference.predict project/data/raw/sample1.png
```

Output:

```powershell
[INFO] Loading model...
[INFO] Predicting...
[RESULT] Predicted class: c_major (confidence: 0.92)
```

---

## 🧪 Poetry Dependencies

Inside `pyproject.toml`:

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

## Tech Stack

- **TensorFlow / Keras** – Deep learning
- **OpenCV** – Image preprocessing
- **Pillow** – Image loading and augmentation
- **Poetry** – Python dependency management
- **Matplotlib** – Plotting training curves
- **VS Code** – Development and debugging

---

## Future Directions

- Multi-label prediction: detect multiple fingers/strings
- Output to MIDI, MusicXML or ASCII tabs
- Real-time prediction web app (Streamlit / FastAPI)
- Pretrained base model integration
- Export best metrics for leaderboard comparisons

---

## ✅ Last Verified

> **Windows 11 + Python 3.9 + Poetry 1.8.2 + TensorFlow 2.19.0**

---

## Git Setup

### Ignore Unnecessary Files

`.gitignore` at the root (OSR/):

```plaintext
__pycache__/
*.py[cod]
.vscode/
.env/
.venv/
poetry.lock
project/data/raw/
project/data/processed/
project/saved_models/
project/reports/
```

### First Commit

```powershell
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git checkout -b main
git add .
git commit -m "Initial commit: Guitar tab recognition framework"
git push -u origin main
```

---

## 📈 How to Evaluate

- Use `training/metrics.py` to save loss/accuracy curves
- Saved as timestamped `.png` plots under `project/reports/`
- Models saved in:
  - `saved_models/all_versions/`
  - `cnn_model_latest.keras`
  - `cnn_model_best.keras`

---

## Contributing

If you have ideas for better tab rendering, fret logic, dataset improvements, or model refinements — PRs are welcome!
