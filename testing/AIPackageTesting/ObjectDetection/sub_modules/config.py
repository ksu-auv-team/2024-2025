# config.py
import os
import torch

# Dataset and Model Configuration
DATASET_PATH = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets'), "RoboSub24_At_Comp") # This should be the path to your dataset
MODEL_SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
MODEL_NAME = "RoboSub24_At_Comp.pt"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EPOCHS = 50
IMG_SIZE = 640
BATCH_SIZE = 16

print("Configuration loaded!")
# print("Dataset Path:", DATASET_PATH)
# print("Model Save Path:", MODEL_SAVE_PATH)
# print("Model Name:", MODEL_NAME)
# print("Device:", DEVICE)
# print("Epochs:", EPOCHS)
# print("Image Size:", IMG_SIZE)
# print("Batch Size:", BATCH_SIZE)
