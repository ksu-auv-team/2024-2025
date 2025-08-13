import time
import smbus2
import logging
from .config_loader import load_config
from .logic import sendDataToServer, getDataFromServer
from .i2c_devices.BNO08x import BNO08x
import multiprocessing

class HardwareInterface:
    def __init__(self):
        """
        @brief Initializes the hardware interface, loads configuration, and sets up the I2C bus.
        """
        self.config = load_config('config/hardware_config.json')

        self.bus = smbus2.SMBus(self.config['i2c_bus'])
        logging.basicConfig(level=logging.INFO)

        logging.info("Hardware Interface initialized with I2C bus %d", self.config['i2c_bus'])
        logging.info("Configuration loaded: %s", self.config)
        logging.info("Checking hardware addresses...")
        
        self.check_hardware_addresses()

        # Create the data structures for communication
        self.input_data = {
            "M1": 127,
            "M2": 127,
            "M3": 127,
            "M4": 127,
            "M5": 127,
            "M6": 127,
            "M7": 127,
            "M8": 127,
            "S1": 0,
            "S2": 0,
            "S3": 0
        }

        self.sensor_data = {
            "IMU_Data": {"X": 0.0, "Y": 0.0, "Z": 0.0, "Roll": 0, "Pitch": 0, "Yaw": 0},
            "Hydrophone_Data": {},
            "Power_Safety_Data": {}
        }

        self.bno08x = BNO08x(port=self.config['BNO08x_Port'], baudrate=self.config['BNO08x_Baudrate'], timeout=self.config['BNO08x_Timeout'])

    def _SerialIMU(self):
        """
        @brief Initializes the IMU sensor and retrieves its data.
        """
        try:
            data = self.bno08x.get_data_json_str()
            if data is not None:
                data = data.replace("{", "").replace("}", "").split(",") # Type: Ignore
                i = 0
                for key in self.sensor_data['IMU_Data']:
                    self.sensor_data['IMU_Data'][key] = float(data[i]) if i < len(data) else 0.0
                    i += 1
                logging.info("IMU data retrieved successfully: %s", self.sensor_data['IMU_Data'])
            else:
                logging.error("IMU get_data_json_str() returned None.")
        except Exception as e:
            logging.error("Failed to retrieve IMU data: %s", str(e))

    def _MotorController(self):
        """
        @brief Sends motor control data to the motor controller.
        """
        try:
            sendDataToServer(self.input_data, self.config['Motor_Controller_URL'])
            logging.info("Motor control data sent successfully: %s", self.input_data)
        except Exception as e:
            logging.error("Failed to send motor control data: %s", str(e))

    def ControlProcess(self):
        while True:
            self.input_data = getDataFromServer(self.config['Database_URL'] + '/inputs')
            self._MotorController()

    def SensorProcess(self):
        while True:
            self._SerialIMU()
            sendDataToServer(self.sensor_data['IMU_Data'], self.config['Database_URL'] + '/imu')

    def check_hardware_addresses(self):
        addresses = [
            self.config['IMU_Address'],
            self.config['Hydrophone_Address'],
            self.config['Motor_Controller_Address'],
            self.config['Blank_Address'],
            self.config['Display_Address'],
            self.config['Torpedo_Address'],
            self.config['Arm_Controller_Address'],
            self.config['Power_Safety_Address']
        ]

        for address in addresses:
            try:
                self.bus.read_byte(address)
                logging.info("Device found at address: %s", address)
            except OSError as e:
                logging.error("No device found at address: %s, Error: %s", address, str(e))

    def run(self):
        self.check_hardware_addresses()
        control_proc = multiprocessing.Process(target=self.ControlProcess)
        sensor_proc = multiprocessing.Process(target=self.SensorProcess)
        control_proc.start()
        sensor_proc.start()
        control_proc.join()
        sensor_proc.join()

    # TODO
    def _Blank(self):
        pass

    # TODO
    def _Display(self):
        pass

    # TODO
    def _Torpedo(self):
        pass

    # TODO
    def _ArmController(self):
        pass

    # TODO
    def _PowerSafety(self):
        pass

    # TODO
    def _Hydrophone(self):
        pass

    # TODO
    def _I2CIMU(self):
        pass

def run():
    hardware_interface = HardwareInterface()
    hardware_interface.run()