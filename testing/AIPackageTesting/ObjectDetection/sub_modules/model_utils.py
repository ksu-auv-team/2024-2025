# model_utils.py
import torch
import os
from torchvision.models.detection import fasterrcnn_resnet50_fpn  # Replace with YOLOv11 if available

from config import MODEL_SAVE_PATH, DEVICE, CLASS_NAMES

def create_model():
    # Replace with YOLOv11-specific model if you have it
    model = fasterrcnn_resnet50_fpn(pretrained=False, num_classes=len(CLASS_NAMES) + 1)
    model = model.to(DEVICE)
    return model

def load_model():
    if os.path.exists(MODEL_SAVE_PATH):
        print("Loading existing model...")
        model = create_model()
        model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
        return model
    else:
        print("No existing model found. Creating a new one...")
        return create_model()

def save_model(model):
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

print("Model utilities module loaded!")