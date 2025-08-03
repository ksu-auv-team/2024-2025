from db_manager import db

class ExternalPressure(db.Model):
    """
    @brief Model for external pressure data.
    @details This model represents the external pressure data stored in the database.
    @param step_index: The index of the step in the external pressure data sequence.
    @param pressure: The external pressure, e.g. '1013.25', '1020.00', '1025.50'.

    @note The 'pressure' field is a float representing the external pressure in hPa (hectopascals).
    
    @example
    >>> external_pressure_data = ExternalPressure(step_index=1, pressure=1013.25)
    """
    __tablename__ = 'external_pressure'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the ExternalPressure model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'pressure': self.pressure
        }

    def __repr__(self):
        return f"<ExternalPressure {self.id} - step_index: {self.step_index}, Pressure: {self.pressure}>"

class ExternalDepth(db.Model):
    """
    @brief Model for external depth data.
    @details This model represents the external depth data stored in the database.
    @param step_index: The index of the step in the external depth data sequence.
    @param depth: The external depth, e.g. '5.0', '10.0', '15.0'.

    @note The 'depth' field is a float representing the external depth in meters.
    
    @example
    >>> external_depth_data = ExternalDepth(step_index=1, depth=10.0)
    """
    __tablename__ = 'external_depth'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the ExternalDepth model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'depth': self.depth
        }

    def __repr__(self):
        return f"<ExternalDepth {self.id} - step_index: {self.step_index}, Depth: {self.depth}>"
