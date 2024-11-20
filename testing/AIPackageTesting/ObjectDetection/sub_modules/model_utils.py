# model_utils.py
from ultralytics import YOLO
from sub_modules.config import MODEL_SAVE_PATH, MODEL_NAME

import os

def load_model():
    """
    Loads an existing YOLO model or creates a new one.
    """
    try:
        # Check if the model file exists
        model = YOLO(os.path.join(MODEL_SAVE_PATH, MODEL_NAME))  # Load from disk
        print("Loaded existing YOLO model.")
    except FileNotFoundError:
        print("No existing model found. Creating a new one...")
        model = YOLO("yolov11x.pt")  # Start with a pre-trained YOLO model (nano version)
    
    return model

def save_model(model):
    """
    Save the model to disk.
    """
    model.export(format="torchscript", save_dir=MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

print("Model utilities module loaded!")