# main.py
from sub_modules.model_utils import load_model
from sub_modules.train import train_model

if __name__ == "__main__":
    # Load or create model
    model = load_model()
    
    # Train model if not already trained
    if model.training:
        train_model(model)
    else:
        print("Model is already trained and loaded!")
