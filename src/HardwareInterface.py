import argparse
import requests
import smbus2
import json
import time


class HardwareInterface:
    """
    @brief This class is used to interface with the hardware of the system.
    It is used to read and write data to the hardware.

    @param ip The IP address of the hardware interface.
    @param port The port of the hardware interface.
    @param debug Whether to print debug messages.

    @note This class is used to interface with the hardware of the system.
    It is used to read and write data to the hardware.
    """

    def __init__(self, ip='localhost', port=5000, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug
        
        self.boards_on = {
            'ESCs': False,
            'Arm': False,
            'Battery_Monitor': False,
            'Hydrophones': False,
            'Depth': False,
            'Torpedo': False
        }

        self.url = f"http://{ip}:{port}"

        self.bus = smbus2.SMBus(1)

        self.addresses = {
            'ESCs': 0,
            'Arm': 0,
            'Battery_Monitor': 0,
            'Hydrophones': 0,
            'Depth': 0,
            'Torpedo': 0
        }
        
    def read_i2c_word(self, address, register):
        """
        @brief Reads a word from the I2C bus.
        """
        high = self.bus.read_byte_data(address, register)
        low = self.bus.read_byte_data(address, register + 1)
        
        value = (high << 8) + low
        
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value
        
    
