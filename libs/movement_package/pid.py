import numpy as np

class PIDController:
    def __init__(self):
        self.horizontal_motors = np.array([127, 127, 127, 127])
        self.vertical_motors = np.array([127, 127, 127, 127])
        self.servos = np.array([127, 127, 127])

        self.horizontal_mapping = np.array([
            [1, 1, -1, -1], # X
            [1, -1, -1, 1], # Y
            [1, -1, 1, -1]  # Yaw
        ])
        self.vertical_mapping = np.array([
            [1, 1, 1, 1] # Z
        ])

    def update_motors(self, x, y, z, yaw):
        """
        @title Update Motors
        @brief Updates the motor and servo outputs based on control input values.
        
        @details
        This method applies predefined mapping matrices to the given control inputs 
        (x, y, z, yaw) to compute the power levels for horizontal and vertical thrusters.
        The horizontal and vertical mappings define how each control axis contributes 
        to each motor's output. The first three inputs (x, y, z) are also stored for 
        servo control.

        @param x     Control input for the X-axis (e.g., forward/backward movement).
        @param y     Control input for the Y-axis (e.g., strafe left/right movement).
        @param z     Control input for the Z-axis (e.g., ascend/descend movement).
        @param yaw   Control input for yaw rotation (e.g., rotate left/right).

        @note 
        - The mappings `self.horizontal_mapping` and `self.vertical_mapping` must be 
        initialized before calling this method.
        - Input values are expected to be in the appropriate range for motor control.

        @return None
        """
        self.horizontal_motors = self.horizontal_mapping @ np.array([x, y, z, yaw])
        self.vertical_motors = self.vertical_mapping @ np.array([x, y, z, yaw])
        self.servos = np.array([x, y, z])

    def calculate_Error(self, imu_data : np.array) -> np.array:
        """
        @title Calculate Error
        @brief Compares the current input values with the IMU data.

        @param imu_data   The IMU data to compare against.

        @returns the error between the current inputs and the IMU data.
        """
        current_inputs = np.concatenate((self.horizontal_motors, self.vertical_motors, self.servos))
        return current_inputs - imu_data

    def calculate_correction(self, imu_data: np.array) -> np.array:
        """
        @title Calculate Correction
        @brief Computes the necessary correction to apply to the motor outputs.

        @param imu_data   The IMU data to compare against.

        @returns the correction values to be applied to the motor outputs.
        """
        error = self.calculate_Error(imu_data)
        # Simple proportional control
        correction = error * 0.1
        return correction
