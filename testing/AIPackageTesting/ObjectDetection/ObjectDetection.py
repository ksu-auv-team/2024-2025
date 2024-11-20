# main.py
from sub_modules.model_utils import load_model
from sub_modules.train import train_model

from datetime import datetime

if __name__ == "__main__":
    start_time = datetime.now()
    # Load or create model
    model = load_model()
    
    # Train model if not already trained
    if model.training:
        train_model(model)
    else:
        print("Model is already trained and loaded!")
    
    end_time = datetime.now()
    print("Time Started:", start_time)
    print("Time Ended:", end_time)
    print("Total Time Elapsed:", end_time - start_time)
