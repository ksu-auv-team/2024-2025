from modules.SupportAll.DebugHandler import DebugHandler

import json
import requests
import argparse
import time
import pyautogui
class VirtualHardwareInterface:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = "http://" + self.ip + ":" + self.port
        self.debug = DebugHandler("VirtualHardwareInterface", ip, port)
        self.debug.set_data("VirtualHardwareInterface", "Initialized")

        #               M1 , M2,  M3,  M4,  M5,  M6,  M7,  M8, T1, T2, Claw
        self.outputs = [127, 127, 127, 127, 127, 127, 127, 127, 0, 0, 127]
        self.keys = ["w", "a", "s", "d", "q", "e", "z", "x", "c", "v", "t", "space"]
        #             X,  -Y,  -X,   Y,   Rz, -Rz, -Y,   C,   Y.  -C, +Cam,  Reset

    def get_data(self):
        response = requests.get(self.url + "/outputs")
        data = response.json()
        self.debug.set_data("VirtualHardwareInterface", "get_data")
        return data

    def actuate(self, data : list):
        pass

    def run(self):
        while True:
            data = self.get_data()
            self.actuate(data)
            time.sleep(0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost")
    parser.add_argument("--port", type=str, default="5000")
    args = parser.parse_args()
    VirtualHardwareInterface(args.ip, args.port).run()
