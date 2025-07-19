import numpy as np
import requests
import argparse


class MovementPackage:
    """
    @brief This class is used to translate the input data into motor / servo commands.
    
    @param ip The IP address of the Movement Package.
    @param port The port of the Movement Package.
    @param debug Whether to print debug messages.

    @note Still need to implement the PID controller.
    """
    def __init__(self, ip='localhost', port=5000, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug
        
        self.horizontalMotors = [
            127, # M1
            127, # M2
            127, # M3
            127  # M4
        ]
        
        self.verticalMotors = [
            127, # M5
            127, # M6
            127, # M7
            127  # M8
        ]

        self.horizontalInputs = [
            0, # X
            0, # Y
            0 # Roll
        ]
        
        self.verticalInputs = [
            0, # Z
            0, # Pitch
            0 # Yaw
        ]

        self.input_data = {
            "X": 0,
            "Y": 0,
            "Z": 0,
            "Roll": 0,
            "Pitch": 0,
            "Yaw": 0,
            "S1": 0,
            "S2": 0,
            "S3": 0,
            "Arm": 0
        }

        self.deadzone = 0.2

        self.horizontalMapping = np.array([
            [1, 1, 1, 1],       # X
            [-1, -1, 1, 1],     # Y
            [-1, 1, -1, 1]      # Yaw
        ])
        
        self.verticalMapping = np.array([
            [1, 1, 1, 1],       # Z
            [-1, -1, 1, 1],     # Pitch
            [-1, 1, -1, 1]      # Roll
        ])
        
        self.output_data = {
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
            "S3": 0
        }

        self.url = f"http://{self.ip}:{self.port}"
    
    def _get_data(self):
        """
        @brief Gets the data from the Movement Package.
        """
        request = requests.get(f'http://{self.ip}:{self.port}/inputs')
        self.input_data = request.json() if request.status_code == 200 else {
            "X": 0,
            "Y": 0,
            "Z": 0,
            "Roll": 0,
            "Pitch": 0,
            "Yaw": 0,
            "S1": 0,
            "S2": 0,
            "S3": 0,
            "Arm": 0
        }
    
    def _split_data(self):
        """
        @brief Splits the data into horizontal and vertical inputs.
        """
        self.horizontalInputs = [
            self.input_data["X"],
            self.input_data["Y"],
            self.input_data["Roll"]
        ]

        self.verticalInputs = [
            self.input_data["Z"],
            self.input_data["Pitch"],
            self.input_data["Yaw"]
        ]

    def _calculate_motor_speeds(self):
        """
        @brief Calculates the motor speeds.
        """
        horizontal_speeds = np.dot(self.horizontalMapping, self.horizontalInputs)
        vertical_speeds = np.dot(self.verticalMapping, self.verticalInputs)

        self.horizontalMotors = np.clip(horizontal_speeds, -127, 127)
        self.verticalMotors = np.clip(vertical_speeds, -127, 127)

    def _join_data(self):
        """
        @brief Joins the data into a single dictionary.
        """
        self.output_data = {
            "M1": self.horizontalMotors[0],
            "M2": self.horizontalMotors[1],
            "M3": self.horizontalMotors[2],
            "M4": self.horizontalMotors[3],
            "M5": self.verticalMotors[0],
            "M6": self.verticalMotors[1],
            "M7": self.verticalMotors[2],
            "M8": self.verticalMotors[3],
            "S1": self.input_data["S1"],    
            "S2": self.input_data["S2"],
            "S3": self.input_data["S3"]
        }
        
    def _send_data(self):
        """
        @brief Sends the data to the Movement Package.
        """
        request = requests.post(f'{self.url}/outputs', json=self.output_data)
        if request.status_code == 200:
            print("Data sent successfully")
        else:
            print("Failed to send data")

    def _print_data(self):
        """
        @brief Prints the data.
        """
        print(f"Horizontal Motors: {self.horizontalMotors}")
        print(f"Vertical Motors: {self.verticalMotors}")
        print(f"Horizontal Inputs: {self.horizontalInputs}")
        print(f"Vertical Inputs: {self.verticalInputs}")
        print(f"Input Data: {self.input_data}")
        print(f"Output Data: {self.output_data}")

    def _manual_setInputs(self, x, y, z, roll, pitch, yaw, s1, s2, s3, arm):
        """
        @brief Manually sets the inputs.
        """
        self.input_data["X"] = x
        self.input_data["Y"] = y
        self.input_data["Z"] = z
        self.input_data["Roll"] = roll
        self.input_data["Pitch"] = pitch
        self.input_data["Yaw"] = yaw
        self.input_data["S1"] = s1
        self.input_data["S2"] = s2
        self.input_data["S3"] = s3
        self.input_data["Arm"] = arm

    def _manual_setOutputs(self, m1, m2, m3, m4, m5, m6, m7, m8, s1, s2, s3):
        """
        @brief Manually sets the outputs.
        """
        self.output_data["M1"] = m1
        self.output_data["M2"] = m2
        self.output_data["M3"] = m3
        self.output_data["M4"] = m4
        self.output_data["M5"] = m5
        self.output_data["M6"] = m6
        self.output_data["M7"] = m7
        self.output_data["M8"] = m8
        self.output_data["S1"] = s1
        self.output_data["S2"] = s2
        self.output_data["S3"] = s3

    def run(self):
        """
        @brief Runs the Movement Package.
        """
        self._get_data()
        self._split_data()
        self._calculate_motor_speeds()
        self._join_data()
        self._send_data()
        self._print_data()

    def manual_input_run(self):
        """
        @brief Manually runs the Movement Package.
        """
        data = []
        for key in self.input_data:
            data.append(input(f"{key}: "))
        
        self._manual_setInputs(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
        self._split_data()
        self._calculate_motor_speeds()
        self._join_data()
        self._send_data()
        self._print_data()

    def manual_output_run(self):
        """
        @brief Manually runs the Movement Package.
        """
        data = []
        for key in self.output_data:
            data.append(input(f"{key}: "))
        
        self._manual_setOutputs(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10])
        self._send_data()
        self._print_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", type=bool, default=False)
    parser.add_argument("--manual-inputs", type=bool, default=False)
    parser.add_argument("--manual-outputs", type=bool, default=False)
    args = parser.parse_args()

    movement_package = MovementPackage(args.ip, args.port, args.debug)
    movement_package.run()