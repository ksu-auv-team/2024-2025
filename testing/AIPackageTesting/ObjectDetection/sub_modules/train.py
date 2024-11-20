# train.py
from ultralytics import YOLO
from config import DATASET_PATH, EPOCHS, IMG_SIZE, BATCH_SIZE, OUTPUT_PATH, MODEL_NAME

def train_model(model):
    """
    Train the YOLO model.
    """
    # Train the model
    model.train(
        data=f"{DATASET_PATH}/data.yaml",  # YOLO dataset configuration file
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        project=OUTPUT_PATH,  # Custom outputs folder
        name=MODEL_NAME, 
        task="detect",  # Explicitly set the task
    )
    print("Training completed!")

print("Training module loaded!")