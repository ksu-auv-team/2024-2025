import requests
import pygame
import json
import time
import os
import numpy as np
import requests
import logging
import argparse
import sys

def load_config():
    pass

def sendToDB(self, data : dict):
    url = f"{self.config['DB_Address']}:{self.config['DB_Port']}/inputs/"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending data to DB: {e}")

class CM:
    def __init__(self, mapping_choice : str = 'regular', args: list = sys.argv):
        self.joystick = None
        self.init_joystick()

        with open("config/controller_config.json") as f:
            self.config = json.load(f)
            # if args.P:
            #     self.baseurl = self.config['poolUrl']
            # else:
            #     self.baseurl = self.config['labUrl']
            self.config = self.config['FlightController']

        self.joy_data = []
        self.count = 0
        del self.config['_comment']

        # Each element in the map list is a list with three elements: element 0 is the button number, element 1 is the axis number, and element 2 is whether the axis is inverted.
        self.map = self.config

        self.out_data = {"Arm": 0, "X": 0.0, "Y": 0.0, "Z": 0.0}
        self.mapping_choice = mapping_choice
        self.convertedData = {"step_index": 0, "direction": "", "force": 0.0, "s1":127, "s2":127, "s3":127, "arm": False}
        # orin_ip = '192.168.1.246'
        orin_ip = '10.42.0.203'
        self.url = f"http://192.168.8.138:5000/inputs/"
        # Configure logging

        # step_index = db.Column(db.Integer, nullable=False)
        # direction = db.Column(db.String(50), nullable=False)
        # force = db.Column(db.Float, nullable=False)
        # M1 = db.Column(db.Float, nullable=False)
        # M2 = db.Column(db.Float, nullable=False)
        # M3 = db.Column(db.Float, nullable=False)
        # M4 = db.Column(db.Float, nullable=False)
        # M5 = db.Column(db.Float, nullable=False)
        # M6 = db.Column(db.Float, nullable=False)
        # M7 = db.Column(db.Float, nullable=False)
        # M8 = db.Column(db.Float, nullable=False)
        # S1 = db.Column(db.Float, nullable=False)
        # S2 = db.Column(db.Float, nullable=False)
        # S3 = db.Column(db.Float, nullable=False)
        # arm = db.Column(db.Boolean, nullable=False)
        self.remapped_to_motor_outputs = {
            "M1": 127,
            "M2": 127,
            "M3": 127,
            "M4": 127,
            "M5": 127,
            "M6": 127,
            "M7": 127,
            "M8": 127,
            "S1": 127,
            "S2": 127,
            "S3": 127,
            "Arm": False
        }

        

    def init_joystick(self):
        pygame.init()
        while True:
            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                print(f"{joystick_count} joystick(s) found. Using the first one.")
                break
            else:
                print("No joystick found. Connect the controller you bot!")
                pygame.time.wait(3000)
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def parse_mapping(self):
        pass

    def get_data(self):
        """
        Update the `data` array with the latest joystick values.
        
        ### Returns
        - `data`: The updated data array.

        ### Example
            Left Stick, Left-Right: 0.06
            Left Stick, Up-Down: -0.02
            Left Back Knob: -0.07
            Right Stick, Left-Right: -0.01
            Right Stick, Up-Down: 0.0
            Right Back Knob: -0.06
            Unknown: -1.0
            Top Knob: 0.93
            Left Button: 20th index
        - `data`: [0.06, -0.02, -0.07, -0.01, 0.0, -0.06, -1.0, 0.93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.joystick.init()

        self.joy_data = [round(self.joystick.get_axis(i), 2) for i in range(self.joystick.get_numaxes())]
        for i in range(self.joystick.get_numbuttons()):
            self.joy_data.append(self.joystick.get_button(i))
        for i in range(self.joystick.get_numhats()):
            self.joy_data.append(self.joystick.get_hat(i))
        return self.joy_data

    def map_data(self):
        """
        Maps joystick data to controller outputs based on the configured mapping.
        step_index = db.Column(db.Integer, nullable=False)
        direction = db.Column(db.String(50), nullable=False)
        force = db.Column(db.Float, nullable=False)
        s1 = db.Column(db.Float, nullable=False)
        s2 = db.Column(db.Float, nullable=False)
        s3 = db.Column(db.Float, nullable=False)
        arm = db.Column(db.Boolean, nullable=False)
        """
        for control, mapping in self.map.items():
            button_index, axis_index, invert = mapping

            # Check if there's a specific button press required for this control
            # if button_index is not None and not self.joy_data[button_index]:
            #     continue  # Skip this mapping if the required button is not pressed

            # Retrieve the axis value
            
            if axis_index is not None:
                value = self.joy_data[axis_index]
                if invert:
                    value = -value  # Invert the value if specified

                # Apply calibration or scaling if necessary
                # Example: value = scale(value, self.config[control])

                # Update the output data dictionary
                self.out_data[control] = value

            # For buttons (boolean values)
            elif 'torp' in control or 'claw' in control:
                self.out_data[control] = bool(self.joy_data[axis_index])

        # Log the mapped data for debugging
        logging.info(f"Mapped data: {self.out_data}")

    def remap_to_outputs(self, data : dict[str, int | float | bool]):
        if data['Arm']:
            if data['X'] > 0.2:
                self.remapped_to_motor_outputs['M1'] = 200
                self.remapped_to_motor_outputs['M2'] = 200
                self.remapped_to_motor_outputs['M3'] = 56
                self.remapped_to_motor_outputs['M4'] = 200
            elif data['X'] < -0.2:
                self.remapped_to_motor_outputs['M1'] = 56
                self.remapped_to_motor_outputs['M2'] = 56
                self.remapped_to_motor_outputs['M3'] = 200
                self.remapped_to_motor_outputs['M4'] = 56
            elif data['Y'] > 0.2:
                self.remapped_to_motor_outputs['M1'] = 56
                self.remapped_to_motor_outputs['M2'] = 200
                self.remapped_to_motor_outputs['M3'] = 200
                self.remapped_to_motor_outputs['M4'] = 200
            elif data['Y'] < -0.2:
                self.remapped_to_motor_outputs['M1'] = 200
                self.remapped_to_motor_outputs['M2'] = 56
                self.remapped_to_motor_outputs['M3'] = 56
                self.remapped_to_motor_outputs['M4'] = 56
            else:
                self.remapped_to_motor_outputs['M1'] = 127
                self.remapped_to_motor_outputs['M2'] = 127
                self.remapped_to_motor_outputs['M3'] = 127
                self.remapped_to_motor_outputs['M4'] = 127
            if data['Z'] > 0.2:
                self.remapped_to_motor_outputs['M5'] = 56
                self.remapped_to_motor_outputs['M6'] = 56
                self.remapped_to_motor_outputs['M7'] = 200
                self.remapped_to_motor_outputs['M8'] = 200
            elif data['Z'] < -0.2:
                self.remapped_to_motor_outputs['M5'] = 200
                self.remapped_to_motor_outputs['M6'] = 200
                self.remapped_to_motor_outputs['M7'] = 56
                self.remapped_to_motor_outputs['M8'] = 56
            else:
                self.remapped_to_motor_outputs['M5'] = 127
                self.remapped_to_motor_outputs['M6'] = 127
                self.remapped_to_motor_outputs['M7'] = 127
                self.remapped_to_motor_outputs['M8'] = 127
        else:
            self.remapped_to_motor_outputs['M1'] = 127
            self.remapped_to_motor_outputs['M2'] = 127
            self.remapped_to_motor_outputs['M3'] = 127
            self.remapped_to_motor_outputs['M4'] = 127
            self.remapped_to_motor_outputs['M5'] = 127
            self.remapped_to_motor_outputs['M6'] = 127
            self.remapped_to_motor_outputs['M7'] = 127
            self.remapped_to_motor_outputs['M8'] = 127

        # Send data to outputs table
        response = requests.post("http://192.168.8.138:5000/outputs/", json=self.remapped_to_motor_outputs)
        if response.status_code == 200:
            logging.info("Data successfully sent to the outputs table.")
        else:
            logging.error(f"Failed to send data to the outputs table: {response.text}")

    def post_data(self):
        """
        Sends the joystick data to the Flask server.
        """
        try:
            response = requests.post(self.url, json=self.convertedData)
            if response.status_code == 200:
                logging.info("Data successfully sent to the server.")
            else:
                logging.error(f"Failed to send data: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending data: {str(e)}")

    def log_output(self, version: int = 0):
        if version == 0:
            # logging.info(self.out_data)
            d = ''
            for key in self.out_data:
                d += f'{key}: {self.out_data[key]}     | '
            print(d)
        elif version == 1:
            temp = ""
            for i in range(len(self.joy_data)):
                temp += f'   {i}: {self.joy_data[i]}   |'
            logging.info(temp)
            print(temp)

    def run(self):
        while True:
            self.get_data()
            self.parse_mapping()
            self.map_data()
            # self.convertData()
            # self.post_data()
            self.remap_to_outputs(self.out_data)
            print("self.remapped_to_motor_outputs:", self.remapped_to_motor_outputs)
            pygame.time.wait(1)
    
    def convertData(self):
        if self.out_data["X"]>0.2:
            if "Forward" not in self.convertedData["direction"]:
                self.convertedData["direction"] += "Forward,"
            self.convertedData["force"] = self.out_data["X"]
        if self.out_data["X"]<-0.2:
            if "Backward" not in self.convertedData["direction"]:
                self.convertedData["direction"] += "Backward,"
            self.convertedData["force"] = self.out_data["X"]
        if self.out_data["Y"]>0.2:
            if "Up" not in self.convertedData["direction"]:
                self.convertedData["direction"] += "Up,"
            self.convertedData["force"] = self.out_data["Y"]
        if self.out_data["Y"]<-0.2:
            if "Down" not in self.convertedData["direction"]:
                self.convertedData["direction"] += "Down,"
            self.convertedData["force"] = self.out_data["Y"]
        if self.out_data["Z"]>0.2:
            if "Left" not in self.convertedData["direction"]:
                self.convertedData["direction"] += "Left,"
            self.convertedData["force"] = self.out_data["Z"]
        if self.out_data["Z"]<-0.2:
            if "Right" not in self.convertedData["direction"]:
                self.convertedData["direction"] += "Right,"
            self.convertedData["force"] = self.out_data["Z"]
        self.convertedData["step_index"] = self.count
        self.convertedData['arm'] = self.out_data["Arm"]
        self.count = self.count + 1

        
    def test_run(self):
        while True:
            axis = input('Enter axis (X, Y, Z, Pitch, Roll, Yaw): ')
            value = float(input('Enter value (-1.0 to 1.0): '))
            
            self.out_data[axis] = value
            
            self.post_data()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--P", help = "Use the pool IP address", action = "store_true")
    args.add_argument("--L", help = "Use the lab IP address", action = "store_true")
    arges = args.parse_args()
    cm = CM(args = arges)
    cm.run()
    # cm.test_run()
