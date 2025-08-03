from db_manager import db

class Sonar(db.Model):
    """
    @brief Model for sonar data.
    @details This model represents the sonar data stored in the database.
    @param step_index: The index of the step in the sonar data sequence.
    @param distance: The distance measured by the sonar, e.g. '5.4', '10.2', '15.0'.
    @param angle: The angle of the sonar sensor, e.g. '0.0', '15.0', '30.0'.

    @note The 'distance' field is a float representing the distance from the sonar to the nearest object,
    and the 'angle' field is a float representing the angle of the sonar sensor in degrees.
    @example
    >>> sonar_data = Sonar(step_index=1, distance=5.4, angle=15.0)
    """
    __tablename__ = 'sonar'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    angle = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the Sonar model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'distance': self.distance,
            'angle': self.angle
        }

    def __repr__(self):
        return f"<Sonar {self.id} - step_index: {self.step_index}, Distance: {self.distance}, Angle: {self.angle}>"
