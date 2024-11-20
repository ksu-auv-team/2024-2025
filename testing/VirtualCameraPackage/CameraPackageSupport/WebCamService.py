import pyautogui
import cv2
import numpy as np
import time

class WebCam:
    '''WebCam class with automatic view-switching between right and bottom views.'''

    def __init__(self, camera_number=None):
        self.camera_number = camera_number
        self.current_view = 2  # Start with view 2 (right view)
        self.last_switch_time = time.time()  # Track the last switch time
        self.switch_interval = 5  # Interval in seconds between view switches

    def get_frame(self):
        """Capture a frame, switch views if needed, and return the frame."""
        # Check if it's time to switch views
        current_time = time.time()
        if current_time - self.last_switch_time >= self.switch_interval:
            self.switch_view()
            self.last_switch_time = current_time

        # Capture screenshot and convert it to OpenCV-compatible format
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Process frame for cropping or other transformations if needed
        if self.camera_number == 0:
            frame = self.crop_frame(frame)  # Crop for one view if applicable

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def switch_view(self):
        """Switch between views 2 (right) and 4 (bottom) automatically."""
        if self.current_view == 2:
            pyautogui.press('T')  # Switch to bottom view (view 4)
            self.current_view = 4
        else:
            pyautogui.press('G')  # Switch to right view (view 2)
            self.current_view = 2

    def crop_frame(self, frame):
        """Optional cropping for Camera 1 (modify as needed based on view)."""
        height, width, _ = frame.shape
        cropped_frame = frame[:, width // 2:]  # Example: Crop the right half
        return cropped_frame
