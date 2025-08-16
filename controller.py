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

        self.out_data = {"Arm": 0, "X": 0.0, "Y": 0.0, "Z": 0.0, "Yaw": 0.0}
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
            "step_index": 0,
            "direction": "",
            "force": 0.0,
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
            "arm": False
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

    def last_resort(self, data : dict[str, int | float | bool]):
        self.remapped_to_motor_outputs['step_index'] += 1
        self.remapped_to_motor_outputs['arm'] = self.out_data['Arm']
        if data['Arm']:
            if data['X'] > 0.2:
                self.remapped_to_motor_outputs['M1'] = int(255)
                self.remapped_to_motor_outputs['M2'] = int(255)
                self.remapped_to_motor_outputs['M3'] = int(0)
                self.remapped_to_motor_outputs['M4'] = int(255)
            elif data['X'] < -0.2:
                self.remapped_to_motor_outputs['M1'] = int(0)
                self.remapped_to_motor_outputs['M2'] = int(0)
                self.remapped_to_motor_outputs['M3'] = int(255)
                self.remapped_to_motor_outputs['M4'] = int(0)
            elif data['Y'] > 0.2:
                self.remapped_to_motor_outputs['M1'] = int(0)
                self.remapped_to_motor_outputs['M2'] = int(255)
                self.remapped_to_motor_outputs['M3'] = int(255)
                self.remapped_to_motor_outputs['M4'] = int(255)
            elif data['Y'] < -0.2:
                self.remapped_to_motor_outputs['M1'] = int(255)
                self.remapped_to_motor_outputs['M2'] = int(0)
                self.remapped_to_motor_outputs['M3'] = int(0)
                self.remapped_to_motor_outputs['M4'] = int(0)
            elif data['Yaw'] > 0.2:
                self.remapped_to_motor_outputs['M1'] = 127
                self.remapped_to_motor_outputs['M2'] = 127
                self.remapped_to_motor_outputs['M3'] = 127
                self.remapped_to_motor_outputs['M4'] = 127
            elif data['Yaw'] < -0.2:
                self.remapped_to_motor_outputs['M1'] = 127
                self.remapped_to_motor_outputs['M2'] = 127
                self.remapped_to_motor_outputs['M3'] = 127
                self.remapped_to_motor_outputs['M4'] = 127
            else:
                self.remapped_to_motor_outputs['M1'] = int(127)
                self.remapped_to_motor_outputs['M2'] = int(127)
                self.remapped_to_motor_outputs['M3'] = int(127)
                self.remapped_to_motor_outputs['M4'] = int(127)
            if data['Z'] > 0.2:
                self.remapped_to_motor_outputs['M5'] = int(0)
                self.remapped_to_motor_outputs['M6'] = int(0)
                self.remapped_to_motor_outputs['M7'] = int(255)
                self.remapped_to_motor_outputs['M8'] = int(255)
            elif data['Z'] < -0.2:
                self.remapped_to_motor_outputs['M5'] = int(255)
                self.remapped_to_motor_outputs['M6'] = int(255)
                self.remapped_to_motor_outputs['M7'] = int(0)
                self.remapped_to_motor_outputs['M8'] = int(0)
            else:
                self.remapped_to_motor_outputs['M5'] = int(127)
                self.remapped_to_motor_outputs['M6'] = int(127)
                self.remapped_to_motor_outputs['M7'] = int(127)
                self.remapped_to_motor_outputs['M8'] = int(127)    
        else:
            self.remapped_to_motor_outputs['M1'] = int(127)
            self.remapped_to_motor_outputs['M2'] = int(127)
            self.remapped_to_motor_outputs['M3'] = int(127)
            self.remapped_to_motor_outputs['M4'] = int(127)
            self.remapped_to_motor_outputs['M5'] = int(127)
            self.remapped_to_motor_outputs['M6'] = int(127)
            self.remapped_to_motor_outputs['M7'] = int(127)
            self.remapped_to_motor_outputs['M8'] = int(127)

        # Send data to outputs table
        response = requests.post("http://192.168.8.138:5000/outputs/", json=self.remapped_to_motor_outputs)
        if response.status_code == 201:
            logging.info("Data successfully sent to the outputs table.")
        else:
            logging.error(f"Failed to send data to the outputs table: {response.text}")

    def run(self):
        while True:
            self.get_data()
            self.parse_mapping()
            self.map_data()
            # self.last_resort(self.out_data)
            self.send_data()
            print("self.remapped_to_motor_outputs:", self.remapped_to_motor_outputs)
            pygame.time.wait(1)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--P", help = "Use the pool IP address", action = "store_true")
    args.add_argument("--L", help = "Use the lab IP address", action = "store_true")
    arges = args.parse_args()
    cm = CM(args = arges)
    cm.run()
    # cm.test_run()
