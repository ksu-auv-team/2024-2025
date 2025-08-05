from . import db

class InternalTemperature(db.Model):
    """
    @brief Model for internal temperature data.
    @details This model represents the internal temperature data stored in the database.
    @param step_index: The index of the step in the internal temperature data sequence.
    @param temperature: The internal temperature, e.g. '25.0', '30.0', '35.0'.

    @note The 'temperature' field is a float representing the internal temperature in degrees Celsius.
    
    @example
    >>> internal_temp_data = InternalTemperature(step_index=1, temperature=30.0)
    """
    __tablename__ = 'internal_temperature'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the InternalTemperature model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'temperature': self.temperature
        }

    def __repr__(self):
        return f"<InternalTemperature {self.id} - step_index: {self.step_index}, Temperature: {self.temperature}>"

class InternalHumidity(db.Model):
    """
    @brief Model for internal humidity data.
    @details This model represents the internal humidity data stored in the database.
    @param step_index: The index of the step in the internal humidity data sequence.
    @param humidity: The internal humidity, e.g. '30.0', '40.0', '50.0'.

    @note The 'humidity' field is a float representing the internal humidity in percentage.
    
    @example
    >>> internal_humidity_data = InternalHumidity(step_index=1, humidity=45.0)
    """
    __tablename__ = 'internal_humidity'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the InternalHumidity model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'humidity': self.humidity
        }

    def __repr__(self):
        return f"<InternalHumidity {self.id} - step_index: {self.step_index}, Humidity: {self.humidity}>"

class InternalPressure(db.Model):
    """
    @brief Model for internal pressure data.
    @details This model represents the internal pressure data stored in the database.
    @param step_index: The index of the step in the internal pressure data sequence.
    @param pressure: The internal pressure, e.g. '1013.25', '1020.00', '1025.50'.

    @note The 'pressure' field is a float representing the internal pressure in hPa (hectopascals).
    
    @example
    >>> internal_pressure_data = InternalPressure(step_index=1, pressure=1013.25)
    """
    __tablename__ = 'internal_pressure'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the InternalPressure model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'pressure': self.pressure
        }

    def __repr__(self):
        return f"<InternalPressure {self.id} - step_index: {self.step_index}, Pressure: {self.pressure}>"
  