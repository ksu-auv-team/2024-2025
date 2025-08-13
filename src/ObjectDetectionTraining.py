import requests
import numpy as np
import json
import time
from modules.SupportAll.DebugHandler import DebugHandler
import argparse
from ultralytics import YOLO

# Initialize DebugHandler for logging
##self.debug_handler = DebugHandler("ObjectDetection", ip, port)
if __name__ == "__main__":
    model = YOLO("yolo11n.yaml") ##should load an untrained model
    results = model.train(data="dataset.yaml", epochs=100, imgsz=640) ##will use dataset in Yolo11 format
    ##to train on. Dataset downloaded from RoboFlow after annotation is finished.
    metrics = model.val() ##validates model using validation images.
    path = model.export(format="onnx") ##converts model into onnx format for ZED camera.
