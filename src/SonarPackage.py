from brping import Ping360
from brping import definitions
import requests
import numpy as np
import json
import time
from modules.SupportAll.DebugHandler import DebugHandler

class Sonar:
    def __init__(self, ip: str = "localhost", port: int = 5000):
        self.p = Ping360()
        self.url = f'http://{ip}:{port}/sonar'
        self.logData = {}

        # Initialize DebugHandler for logging
        self.debug_handler = DebugHandler("SonarSystem", ip, port)

        # Initialize sonar settings
        self.connect_sonar()
        self.initialize_sonar_settings()

    def connect_sonar(self):
        """Connect to the sonar via serial."""
        self.p.connect_serial("/dev/ttyUSB0", 115200)

    def initialize_sonar_settings(self):
        """Initialize sonar transmission settings."""
        self.p.initialize()
        self.p.set_transmit_frequency(750)
        self.p.set_sample_period(1355)
        self.p.set_number_of_samples(1200)
        self.p.set_gain_setting(0)
        self.p.set_mode(1)
        self.p.set_transmit_duration(40)

    def calculate_sample_distance(self, ping_message, v_sound=1480):
        """
        Calculates the distance that each sample covers.

        @param ping_message Ping360 data message object
        @param v_sound Speed of sound in water (default 1480 m/s)
        @return Distance per sample in meters
        """
        return v_sound * ping_message.sample_period * 12.5e-9

    def filter_data_within_range(self, data, dist_per_sample, lower_limit):
        """Filter data array to remove samples within a specified radius."""
        filtered_data = data[lower_limit:]
        return filtered_data

    def detect_highest_intensity(self, data):
        """Identify the sample with the highest intensity."""
        highest_value = 0
        highest_index = 0
        for i, intensity in enumerate(data):
            if intensity > 126 and intensity > highest_value:
                highest_value = intensity
                highest_index = i
        return highest_value, highest_index

    def process_scan(self, gradian):
        """Process sonar scan at a given gradian angle."""
        d = self.p.transmitAngle(gradian)
        dist_per_sample = self.calculate_sample_distance(d)

        # Convert and filter data
        data = np.frombuffer(d.data, dtype=np.uint8)
        lower_limit = int(0.75 / dist_per_sample)
        data = self.filter_data_within_range(data, dist_per_sample, lower_limit)

        highest_value, highest_index = self.detect_highest_intensity(data)
        return highest_value, highest_index, dist_per_sample

    def log_and_send_data(self, gradian, highest_value, highest_index, dist_per_sample):
        """Log and send sonar data if an obstacle is detected."""
        if highest_value >= 127:
            angle = float(0.9 * gradian)
            distance = float(highest_index * dist_per_sample)

            # Prepare log data
            self.logData = {'angle': angle, 'distance': distance}
            self.debug_handler.set_data("INFO", f"Object Detected at {angle} degrees, {distance} meters.")
            self.send_data()

    def send_data(self):
        """Send data to the server."""
        try:
            response = requests.post(self.url, json=self.logData)
            if response.status_code == 200:
                self.debug_handler.set_data("INFO", "Data successfully sent to the server.")
            else:
                self.debug_handler.set_data("ERROR", f"Failed to send data: {response.text}")
        except requests.exceptions.RequestException as e:
            self.debug_handler.set_data("ERROR", f"Error sending data: {str(e)}")

    def run(self):
        """Run the sonar scan and data collection process."""
        try:
            while True:
                for gradian in range(400):
                    highest_value, highest_index, dist_per_sample = self.process_scan(gradian)
                    self.log_and_send_data(gradian, highest_value, highest_index, dist_per_sample)
        except KeyboardInterrupt:
            self.debug_handler.set_data("INFO", "Sonar scan interrupted by user.")

if __name__ == "__main__":
    SonarSensor = Sonar()
    SonarSensor.run()
