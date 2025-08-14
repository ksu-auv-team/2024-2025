from .logic import fetch_data, post_data, get_latest_data
from .config_loader import load_config
from .pid import PIDController

import numpy as np
import logging
import os


class MovementPackage:
    def __init__(self, package_name: str = "movement_package"):
        self.package_name = package_name
        self.config = load_config(package_name)
        self.logger = logging.getLogger(package_name)

        self.parsed_inputs = {
            "id": 0,
            "step_index": 0,
            "direction": "",
            "force": 0,
            "X": 0,
            "Y": 0,
            "Z": 0,
            "Yaw": 0,
            "S1": 0,
            "S2": 0,
            "S3": 0,
            "Arm": 0
        }
        motor_data = {
            f"M{i}": 127 for i in range(1, 9)
        }
        servo_data = {
            f"S{i}": 127 for i in range(1, 4)
        }
        self.combined_output = {**motor_data, **servo_data}
        self.logger.info(f"Combined output: {self.combined_output}")

        self.PID = PIDController()

        self.config = load_config(self.package_name)

    def _parse_inputs(self, input_data: dict):
        """
        @brief Generate output data based on the input data
        @param input_data The input data to process
        @return A dictionary containing the output data
        """
        if not input_data:
            self.logger.warning("No input data provided.")
            return {"data": []}

        # Process the input data and generate output
        # id = db.Column(db.Integer, primary_key=True)
        # step_index = db.Column(db.Integer, nullable=False)
        # direction = db.Column(db.String(50), nullable=False)
        # force = db.Column(db.Float, nullable=False)
        # s1 = db.Column(db.Float, nullable=False)
        # s2 = db.Column(db.Float, nullable=False)
        # s3 = db.Column(db.Float, nullable=False)
        # arm = db.Column(db.Boolean, nullable=False)

        if input_data['arm']:
            self.parsed_inputs['id'] = input_data['id']
            self.parsed_inputs['step_index'] = input_data['step_index']
            self.parsed_inputs['direction'] = input_data['direction']
            self.parsed_inputs['force'] = input_data['force']
            match self.parsed_inputs['direction']:
                case "up":
                    self.logger.info("Moving up.")
                    self.parsed_inputs['Z'] = input_data['force']
                case "down":
                    self.logger.info("Moving down.")
                    self.parsed_inputs['Z'] = -input_data['force']
                case "left":
                    self.logger.info("Moving left.")
                    self.parsed_inputs['Y'] = -input_data['force']
                case "right":
                    self.logger.info("Moving right.")
                    self.parsed_inputs['Y'] = input_data['force']
                case "forward":
                    self.logger.info("Moving forward.")
                    self.parsed_inputs['X'] = input_data['force']
                case "backward":
                    self.logger.info("Moving backward.")
                    self.parsed_inputs['X'] = -input_data['force']
                case "yaw_right":
                    self.logger.info("Yawing right.")
                    self.parsed_inputs['Y'] = input_data['force']
                case "yaw_left":
                    self.logger.info("Yawing left.")
                    self.parsed_inputs['Y'] = -input_data['force']
                case _:
                    self.logger.warning(f"Unknown direction: {dir}")
            self.parsed_inputs['S1'] = input_data['s1']
            self.parsed_inputs['S2'] = input_data['s2']
            self.parsed_inputs['S3'] = input_data['s3']
            self.parsed_inputs['Arm'] = input_data['arm']

    def _parse_outputs(self, data : dict) -> dict:
        """
        @brief Generate output data based on the parsed inputs
        @return A dictionary containing the output data
        """
        if not self.parsed_inputs:
            self.logger.warning("No parsed inputs available.")
            return {"data": []}
    
        if data:
            self.logger.info(f"Latest IMU data: {data}")
            self.PID.update_motors(**data)
            output = {
                "id": self.parsed_inputs["id"],
                "step_index": self.parsed_inputs["step_index"],
                "direction": self.parsed_inputs["direction"],
                "force": self.parsed_inputs["force"],
                "M1": int(self.PID.horizontal_motors[0]) if len(self.PID.horizontal_motors) > 0 else 0,
                "M2": int(self.PID.horizontal_motors[1]) if len(self.PID.horizontal_motors) > 1 else 0,
                "M3": int(self.PID.horizontal_motors[2]) if len(self.PID.horizontal_motors) > 2 else 0,
                "M4": int(self.PID.horizontal_motors[3]) if len(self.PID.horizontal_motors) > 3 else 0,
                "M5": int(self.PID.vertical_motors[0]) if len(self.PID.vertical_motors) > 0 else 0,
                "M6": int(self.PID.vertical_motors[1]) if len(self.PID.vertical_motors) > 1 else 0,
                "M7": int(self.PID.vertical_motors[2]) if len(self.PID.vertical_motors) > 2 else 0,
                "M8": int(self.PID.vertical_motors[3]) if len(self.PID.vertical_motors) > 3 else 0,
                "S1": int(self.PID.servos[0]) if len(self.PID.servos) > 0 else 0,
                "S2": int(self.PID.servos[1]) if len(self.PID.servos) > 1 else 0,
                "S3": int(self.PID.servos[2]) if len(self.PID.servos) > 2 else 0,
                "Arm": self.parsed_inputs["Arm"]
            }
            return output
        else:
            output = {
                "id": 0,
                "step_index": 0,
                "direction": "",
                "force": 0,
                "M1": 0,
                "M2": 0,
                "M3": 0,
                "M4": 0,
                "M5": 0,
                "M6": 0,
                "M7": 0,
                "M8": 0,
                "S1": 0,
                "S2": 0,
                "S3": 0,
                "Arm": 0
            }
            return output
    
    def _updateDB(self, data : dict):
        """
        @brief Update the database with the latest data
        @param data The data to update in the database
        """
        if not data:
            self.logger.warning("No data to update in the database.")
            return
        
        api_url = f"{self.config['DB_Address']}:{self.config['DB_Port']}/outputs"
        response = post_data(api_url, data)
        if 'error' in response:
            self.logger.error(f"Failed to update database: {response['error']}")
        else:
            self.logger.info("Database updated successfully.")

    def run(self):
        while True:
            self.logger.info("Fetching latest IMU data...")
            data = get_latest_data(self.config['DB_Address'] + ":" + str(self.config['DB_Port']) + "/imu/latest")
            if data:
                self.logger.info(f"Latest IMU data: {data}")
                self.logger.info("Parsing inputs...")
                data = self._parse_inputs(data)
                self.logger.info("Parsed inputs: %s", self.parsed_inputs)
                self.logger.info("Parsing outputs...")
                data = self._parse_outputs(self.parsed_inputs)
                self.logger.info("Parsed outputs: %s", self.parsed_inputs)
                self.logger.info("Updating database...")
                self._updateDB(data)
                self.logger.info("Database updated successfully.")
            else:
                self.logger.warning("No data received.")

def run():
    movement_package = MovementPackage()
    movement_package.run()