# data_preparation.py
import os
from torch.utils.data import DataLoader
from torchvision import transforms, datasets

from config import DATASET_PATH, IMAGE_SIZE, BATCH_SIZE

def get_data_loaders():
    # Data augmentation and normalization
    transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    
    # Load datasets
    dataset = datasets.ImageFolder(root=DATASET_PATH, transform=transform)
    data_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    return data_loader

print("Data preparation module loaded!")