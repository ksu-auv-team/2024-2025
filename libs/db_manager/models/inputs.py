from db_manager import db

class Inputs(db.Model):
    """
    @brief Model for user inputs.
    @details This model represents the user inputs stored in the database.
    @param step_index: The index of the step in the input sequence.
    @param directions: The direction of the input, e.g., 'left', 'right', 'forward', 'backward'. Directions are split by commas
    @param force: The force applied in the input, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param s1: The force applied to sensor 1, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param s2: The force applied to sensor 2, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param s3: The force applied to sensor 3, e.g. '0.0', '0.25', '0.5', '0.75', '1.0'.
    @param arm: A boolean indicating whether the arm is used in the input.
    @note The 'direction' field is a string that can contain multiple directions separated by commas.

    @example
    >>> input_data = Inputs(step_index=1, direction='forward, down', force='0.5', s1=0.3, s2=0.4, s3=0.5, arm=True)
    """
    __tablename__ = 'inputs'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    force = db.Column(db.String(10), nullable=False)
    s1 = db.Column(db.Float, nullable=False)
    s2 = db.Column(db.Float, nullable=False)
    s3 = db.Column(db.Float, nullable=False)
    arm = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Inputs {self.id} - step_index: {self.step_index}, Direction: {self.direction}, Force: {self.force},\
                  S1: {self.s1}, S2: {self.s2}, S3: {self.s3}, Arm: {self.arm}>"