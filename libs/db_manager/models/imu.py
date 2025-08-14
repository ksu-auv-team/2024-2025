from . import db

class IMU(db.Model):
    """
    @brief Model for IMU data.
    @details This model represents the IMU data stored in the database.
    @param step_index: The index of the step in the IMU data sequence.
    @param X: The X-axis acceleration, e.g. '0.0', '0.1', '0.2'.
    @param Y: The Y-axis acceleration, e.g. '0.0', '0.1', '0.2'.
    @param Z: The Z-axis acceleration, e.g. '0.0', '0.1', '0.2'.
    @param roll: The roll angle, e.g. '0.0', '15.0', '30.0'.
    @param pitch: The pitch angle, e.g. '0.0', '15.0', '30.0'.
    @param yaw: The yaw angle, e.g. '0.0', '15.0', '30.0'.

    @note The 'X', 'Y', and 'Z' fields are floats representing the acceleration in the respective axes,
    and the 'roll', 'pitch', and 'yaw' fields are floats representing the angles in degrees.

    @example
    >>> imu_data = IMU(step_index=1, X=0.0, Y=0.1, Z=0.2, roll=15.0, pitch=30.0, yaw=45.0)
    """
    __tablename__ = 'imu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_index = db.Column(db.Integer, nullable=False)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    roll = db.Column(db.Float, nullable=False)
    pitch = db.Column(db.Float, nullable=False)
    yaw = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the IMU model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'X': self.X,
            'Y': self.Y,
            'Z': self.Z,
            'roll': self.roll,
            'pitch': self.pitch,
            'yaw': self.yaw
        }

    def __repr__(self):
        return f"<IMU {self.id} - step_index: {self.step_index}, X: {self.X}, Y: {self.Y}, Z: {self.Z}, Roll: {self.roll}, Pitch: {self.pitch}, Yaw: {self.yaw}>"