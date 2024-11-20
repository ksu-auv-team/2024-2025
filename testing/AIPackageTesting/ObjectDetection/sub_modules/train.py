# train.py
from ultralytics import YOLO
from sub_modules.config import DATASET_PATH, EPOCHS, IMG_SIZE, BATCH_SIZE, MODEL_NAME

def train_model(model):
    """
    Train the YOLO model.
    """
    # Train the model
    model.train(
        data=f"{DATASET_PATH}/data.yaml",  # YOLO dataset configuration file
        task="train",
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        name=MODEL_NAME, 
    )
    print("Training completed!")

print("Training module loaded!")