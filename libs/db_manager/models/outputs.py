from . import db

class Outputs(db.Model):
    """
    @brief Model for user outputs.
    @details This model represents the user outputs stored in the database.
    @param step_index: The index of the step in the output sequence.
    @param direction: The direction of the output, e.g., 'left', 'right', 'forward', 'backward'.
    @param force: The force applied in the output, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M1: The force applied to motor 1, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M2: The force applied to motor 2, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M3: The force applied to motor 3, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M4: The force applied to motor 4, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M5: The force applied to motor 5, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M6: The force applied to motor 6, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M7: The force applied to motor 7, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param M8: The force applied to motor 8, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param S1: The force applied to sensor 1, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param S2: The force applied to sensor 2, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param S3: The force applied to sensor 3, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param arm: A boolean indicating whether the arm is used in the output.
    @note The 'direction' field is a string that can contain multiple directions separated by commas.

    @example
    >>> output_data = Outputs(step_index=1, direction='forward, down', force='0.5', M1=0.3, M2=0.4, M3=0.5, M4=0.6, M5=0.7,
                             M6=0.8, M7=0.9, M8=1.0, S1=0.3, S2=0.4, S3=0.5, arm=True)
    """
    __tablename__ = 'outputs'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    force = db.Column(db.Float, nullable=False)
    M1 = db.Column(db.Float, nullable=False)
    M2 = db.Column(db.Float, nullable=False)
    M3 = db.Column(db.Float, nullable=False)
    M4 = db.Column(db.Float, nullable=False)
    M5 = db.Column(db.Float, nullable=False)
    M6 = db.Column(db.Float, nullable=False)
    M7 = db.Column(db.Float, nullable=False)
    M8 = db.Column(db.Float, nullable=False)
    S1 = db.Column(db.Float, nullable=False)
    S2 = db.Column(db.Float, nullable=False)
    S3 = db.Column(db.Float, nullable=False)
    arm = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        """
        Convert the Outputs model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'direction': self.direction,
            'force': self.force,
            'M1': self.M1,
            'M2': self.M2,
            'M3': self.M3,
            'M4': self.M4,
            'M5': self.M5,
            'M6': self.M6,
            'M7': self.M7,
            'M8': self.M8,
            'S1': self.S1,
            'S2': self.S2,
            'S3': self.S3,
            'arm': self.arm
        }

    def __repr__(self):
        return f"<Outputs {self.id} - step_index: {self.step_index}, Direction: {self.direction}, Force: {self.force},\
                  M1: {self.M1}, M2: {self.M2}, M3: {self.M3}, M4: {self.M4}, M5: {self.M5}, M6: {self.M6},\
                  M7: {self.M7}, M8: {self.M8}, S1: {self.S1}, S2: {self.S2}, S3: {self.S3}, Arm: {self.arm}>"