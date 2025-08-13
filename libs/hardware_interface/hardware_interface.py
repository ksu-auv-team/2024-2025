import time
import smbus2
import logging
from .config_loader import load_config
from .logic import sendDataToServer, getDataFromServer
from .i2c_devices.BNO08x import BNO08x

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

    def _IMU(self):
        pass

    def _Hydrophone(self):
        pass

    def _MotorController(self):
        pass

    def _Blank(self):
        pass

    def _Display(self):
        pass

    def _Torpedo(self):
        pass

    def _ArmController(self):
        pass

    def _PowerSafety(self):
        pass

    def ControlProcess(self):
        pass

    def SensorProcess(self):
        pass

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
                logging.info("Device found at address: %s", hex(address))
            except OSError as e:
                logging.error("No device found at address: %s, Error: %s", hex(address), str(e))

    def run(self):
        while True:
            self.ControlProcess()
            self.SensorProcess()
            time.sleep(0.1)

