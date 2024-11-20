import json
import requests
import argparse
import time
import pyautogui
import logging

class VirtualHardwareInterface:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = f"http://{self.ip}:{self.port}"

        # Configure logging
        logging.basicConfig(
            filename='virtual_hardware_interface.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("VirtualHardwareInterface")
        self.logger.info("VirtualHardwareInterface initialized")

        # Define initial outputs for thrusters, torpedoes, and claw
        self.outputs = [127, 127, 127, 127, 127, 127, 127, 127, False, False, 127]
        self.control_keys = {
            'X+': 'w', 'X-': 's',
            'Z+': 'a', 'Z-': 'd',
            'Yaw+': 'q', 'Yaw-': 'e',
            'Vertical+': 'z', 'Vertical-': 'x',
            'Torpedo1': 'c', 'Torpedo2': 'v',
            'ClawOpen': 't', 'ClawClose': 'space'
        }
        self.paused = False
        self.logger.info("Control keys mapped to DOF actions")

    def get_data(self):
        """Retrieve the current control values from the server."""
        try:
            response = requests.get(self.url + "/outputs")
            data = response.json()
            self.logger.info("Data retrieved from server")
            return data
        except requests.RequestException as e:
            self.logger.error(f"Failed to retrieve data: {e}")
            return self.outputs  # return last known values if request fails

    def actuate(self, data):
        """Actuate based on thruster and control data from input."""
        thrusters = data[:8]
        torpedoes = data[8:10]
        claw = data[10]

        # Check if control is paused
        if self.paused:
            self.logger.info("Control is paused")
            return

        # First four thrusters control X, Z, and Yaw DOFs
        t1, t2, t3, t4 = thrusters[:4]

        # Forward and backward movement
        if all(t > 127 for t in [t1, t2, t3, t4]):
            pyautogui.press(self.control_keys['X+'])
            self.logger.info("Sub moving forward")
        elif all(t <= 127 for t in [t1, t2, t3, t4]):
            pyautogui.press(self.control_keys['X-'])
            self.logger.info("Sub moving backward")

        # Right and left movement
        elif t1 > 127 and t3 > 127 and t2 <= 127 and t4 <= 127:
            pyautogui.press(self.control_keys['Z+'])
            self.logger.info("Sub moving right")
        elif t2 > 127 and t4 > 127 and t1 <= 127 and t3 <= 127:
            pyautogui.press(self.control_keys['Z-'])
            self.logger.info("Sub moving left")

        # Rotation (Yaw) right and left
        elif t1 > 127 and t4 > 127 and t2 <= 127 and t3 <= 127:
            pyautogui.press(self.control_keys['Yaw+'])
            self.logger.info("Sub rotating right")
        elif t2 > 127 and t3 > 127 and t1 <= 127 and t4 <= 127:
            pyautogui.press(self.control_keys['Yaw-'])
            self.logger.info("Sub rotating left")

        # Second four thrusters control Z (vertical) DOF
        t5, t6, t7, t8 = thrusters[4:]

        if all(t > 127 for t in [t5, t6, t7, t8]):
            pyautogui.press(self.control_keys['Vertical+'])
            self.logger.info("Sub moving down")
        elif all(t <= 127 for t in [t5, t6, t7, t8]):
            pyautogui.press(self.control_keys['Vertical-'])
            self.logger.info("Sub moving up")

        # Torpedo control
        if torpedoes[0]:
            pyautogui.press(self.control_keys['Torpedo1'])
            self.logger.info("Torpedo 1 launched")
        if torpedoes[1]:
            pyautogui.press(self.control_keys['Torpedo2'])
            self.logger.info("Torpedo 2 launched")

        # Claw control
        if claw > 127:
            pyautogui.press(self.control_keys['ClawOpen'])
            self.logger.info("Claw opening")
        else:
            pyautogui.press(self.control_keys['ClawClose'])
            self.logger.info("Claw closing")

    def toggle_pause(self):
        """Toggle pause state when Escape key is pressed."""
        self.paused = not self.paused
        state = "paused" if self.paused else "resumed"
        self.logger.info(f"Control {state}")

    def run(self):
        """Main loop for continuously checking data and actuating controls."""
        while True:
            # Check for escape key to toggle pause
            if pyautogui.hotkey("esc"):
                self.toggle_pause()

            # Fetch data and actuate if not paused
            data = self.get_data()
            self.actuate(data)
            time.sleep(0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost")
    parser.add_argument("--port", type=str, default="5000")
    args = parser.parse_args()
    VirtualHardwareInterface(args.ip, args.port).run()
