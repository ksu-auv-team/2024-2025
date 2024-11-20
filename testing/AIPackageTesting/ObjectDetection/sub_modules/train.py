# train.py
import torch
import torch.optim as optim
from torch.nn.functional import cross_entropy

from sub_modules.config import EPOCHS, DEVICE, LEARNING_RATE
from sub_modules.data_preparations import get_data_loaders
from sub_modules.model_utils import save_model

def train_model(model):
    data_loader = get_data_loaders()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    model.train()
    for epoch in range(EPOCHS):
        epoch_loss = 0
        for images, targets in data_loader:
            images, targets = images.to(DEVICE), targets.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = cross_entropy(outputs, targets)  # Replace with YOLO-specific loss if applicable
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        print(f"Epoch [{epoch+1}/{EPOCHS}] Loss: {epoch_loss:.4f}")
    
    save_model(model)
    print("Training complete!")

print("Training module loaded!")