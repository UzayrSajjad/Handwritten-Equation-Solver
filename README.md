# Handwritten Math Equation Solver

![Project image](./image.png)

## Overview

This project detects and solves handwritten mathematical equations using deep learning models and exposes a simple Streamlit web app for interactive use. Users can draw an equation on a canvas or upload an image, and the app will output the interpreted equation and its solution.

## How it was made

- Data: A publicly available dataset of handwritten math symbols was used for training. Images were preprocessed (grayscale, thresholding, contour extraction, padding/resizing) and augmented to improve model robustness.
- Models: A CNN was trained for character recognition (per-character classification). An RNN was used to interpret sequences of characters and assemble full equations. The pipeline extracts character bounding boxes, classifies each symbol with the CNN, then passes the symbol sequence to the RNN to interpret and compute the result.
- Web app: A Streamlit frontend (`Web_app/app.py`) provides a drawing canvas and image upload, calls a `predict` function that loads the trained models (`Models/*.h5`) and returns the interpreted equation and solution.

## Tech stack / Libraries

- Python 3.12
- TensorFlow (2.x)
- Streamlit
- OpenCV
- Pillow
- NumPy, Pandas, scikit-learn, Matplotlib, Seaborn

See `requirements.txt` for exact versions used in the development environment.

## Model performance

These are the validation accuracies observed during training (your dataset & training recipe may cause variation):

- CNN (character recognition): 97.57%
- RNN (sequence interpretation): 76.32%

Note: The combined pipeline accuracy on end-to-end equation solving depends on symbol segmentation and the RNN interpretation; expect lower end-to-end accuracy than the raw per-character numbers.

## How to run locally

1. Create and activate a virtual environment (optional but recommended):

```bash
cd hwdr
python -m venv .venv
source .venv/bin/activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:

```bash
cd Web_app
streamlit run app.py
```

4. Open the URL shown in the terminal (e.g., http://localhost:8501).

## Files of interest

- `Models/` — trained models and notebooks used to train/evaluate them.
- `Web_app/` — Streamlit front-end and the `predict.py` script that wraps model inference.
