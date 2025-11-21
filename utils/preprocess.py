import cv2
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
import streamlit as st
from pathlib import Path
import traceback

labels = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '+', 11: '/', 12: '*', 13: '-'}

# Resolve model path for new structure
project_root = Path(__file__).resolve().parents[1]  # HandyMath/
model_path = project_root / 'model' / 'cnn_model.h5'

model = None
try:
    if model_path.exists():
        model = load_model(str(model_path))
    else:
        st.error(f"Model file not found at {model_path}")
except Exception as e:
    st.error(f"Failed to load model from {model_path}: {e}")
    st.text(traceback.format_exc())

if model is None:
    st.error("Model not found or failed to load. Expected at: Models/cnn_model.h5")


def predict(image_path):
    # Early guard: ensure model was loaded
    if model is None:
        st.error("Model is not loaded. Prediction cannot proceed.")
        return "Error", "Model not loaded"

    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")

        _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            return "No symbols detected", "Error: No symbols found"

        bounding_boxes = [cv2.boundingRect(contour) for contour in contours]
        sorted_indices = sorted(range(len(bounding_boxes)), key=lambda i: bounding_boxes[i][0])
        sorted_contours = [contours[i] for i in sorted_indices]

        rois = []
        padding = 10  

        for contour in sorted_contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_start = max(0, x - padding)
            y_start = max(0, y - padding)
            x_end = min(image.shape[1], x + w + padding)
            y_end = min(image.shape[0], y + h + padding)
            
            roi = image[y_start:y_end, x_start:x_end]
            roi = cv2.resize(roi, (32, 32))
            rois.append(roi)

        rois = np.array(rois)
        rois = rois / 255.0
        rois = np.expand_dims(rois, axis=-1)

        predictions = model.predict(rois)
        predicted_labels = np.argmax(predictions, axis=1)

        image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        for i, contour in enumerate(sorted_contours):
            x, y, w, h = cv2.boundingRect(contour)
            label = labels[predicted_labels[i]]
            cv2.rectangle(image_color, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image_color, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        st.image(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))
        equation = ''.join(labels[predicted_labels[i]] for i in range(len(predicted_labels)))
        
        try:
            result = eval(equation)
        except:
            result = "Invalid equation"
        
        return equation.replace('*','x'), result

    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
        return "Error", "Could not process image"



