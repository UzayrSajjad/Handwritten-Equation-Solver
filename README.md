# Handy Math - Handwritten Equation Solver

A modern web application that uses deep learning to recognize handwritten mathematical equations and solve them in real-time.

## Features

- 🖌️ **Draw Equations**: Interactive canvas for writing equations
- 📷 **Upload Images**: Support for image uploads
- 🤖 **AI-Powered**: Uses CNN and RNN models for accurate recognition
- 🎨 **Modern UI**: Beautiful gradient design with dark/light mode
- ⚡ **Real-time**: Instant equation recognition and solving

## Tech Stack

- **Frontend**: Streamlit
- **ML Models**: TensorFlow/Keras (CNN + RNN)
- **Image Processing**: OpenCV, PIL
- **Canvas**: streamlit-drawable-canvas

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd HandyMath
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
HandyMath/
│
├── app.py                # Main Streamlit application
│
├── model/
│   ├── cnn_model.h5     # CNN model for digit recognition
│   └── rnn_model.h5     # RNN model for sequence processing
│
├── utils/
│   └── preprocess.py    # Helper functions for preprocessing and prediction
│
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore         # Git ignore rules
```

## How It Works

1. **Draw or Upload**: User draws an equation on the canvas or uploads an image
2. **Preprocessing**: Image is processed and segmented into individual characters
3. **Recognition**: CNN model recognizes digits and operators
4. **Sequence Processing**: RNN model processes the sequence
5. **Evaluation**: Mathematical expression is evaluated and result is displayed

## Models

- **CNN Model**: Trained on MNIST dataset for digit recognition (0-9) and operators (+, -, ×, ÷)
- **RNN Model**: Processes sequences of recognized characters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Streamlit
- Deep Learning models powered by TensorFlow
- UI inspired by modern design principles

---

Made with ❤️ using Deep Learning
