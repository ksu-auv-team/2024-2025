# config.py
import os
import torch

# Dataset and Model Configuration
DATASET_PATH = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets'), "RoboSub24_At_Comp") # This should be the path to your dataset
MODEL_SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
CLASS_NAMES = ["object1", "object2", "object3", "object4"]  # Update with actual objects
IMAGE_SIZE = (640, 640)
BATCH_SIZE = 16
LEARNING_RATE = 0.001
EPOCHS = 100
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("Configuration loaded!")
# print("Dataset Path:", DATASET_PATH)
# print("Model Save Path:", MODEL_SAVE_PATH)
# print("Class Names:", CLASS_NAMES)
# print("Image Size:", IMAGE_SIZE)
# print("Batch Size:", BATCH_SIZE)
# print("Learning Rate:", LEARNING_RATE)
# print("Epochs:", EPOCHS)
# print("Device:", DEVICE)