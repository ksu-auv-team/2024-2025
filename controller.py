import requests
import pygame
import json
import time
import os


def load_config():
    pass

def sendToDB(self, data : dict):
    url = f"{self.config['DB_Address']}:{self.config['DB_Port']}/inputs/"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending data to DB: {e}")

class Controller:
    def __init__(self):
        pass