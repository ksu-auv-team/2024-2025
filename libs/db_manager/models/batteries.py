from db_manager import db

class Batteries(db.Model):
    """
    @brief Model for battery data.
    @details This model represents the battery data stored in the database.
    @param step_index: The index of the step in the battery data sequence.
    @param voltage1: The voltage of battery 1, e.g. '12.0', '12.5', '13.0'.
    @param voltage2: The voltage of battery 2, e.g. '12.0', '12.5', '13.0'.
    @param voltage3: The voltage of battery 3, e.g. '12.0', '12.5', '13.0'.
    @param current1: The current of battery 1, e.g. '1.0', '1.5', '2.0'.
    @param current2: The current of battery 2, e.g. '1.0', '1.5', '2.0'.
    @param current3: The current of battery 3, e.g. '1.0', '1.5', '2.0'.
    @param temperature1: The temperature of battery 1, e.g. '25.0', '30.0', '35.0'.
    @param temperature2: The temperature of battery 2, e.g. '25.0', '30.0', '35.0'.
    @param temperature3: The temperature of battery 3, e.g. '25.0', '30.0', '35.0'.

    @note The 'voltage' and 'current' fields are floats representing the respective values in volts and amps,
    and the 'temperature' fields are floats representing the temperature in degrees Celsius.
    
    @example
    >>> battery_data = Batteries(step_index=1, voltage1=12.0, voltage2=12.5, voltage3=13.0,
    ...                           current1=1.0, current2=1.5, current3=2.0,
    ...                           temperature1=25.0, temperature2=30.0, temperature3=35.0)
    """
    __tablename__ = 'batteries'
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    voltage1 = db.Column(db.Float, nullable=False)
    voltage2 = db.Column(db.Float, nullable=False)
    voltage3 = db.Column(db.Float, nullable=False)
    current1 = db.Column(db.Float, nullable=False)
    current2 = db.Column(db.Float, nullable=False)
    current3 = db.Column(db.Float, nullable=False)
    temperature1 = db.Column(db.Float, nullable=False)
    temperature2 = db.Column(db.Float, nullable=False)
    temperature3 = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convert the Batteries model instance to a dictionary.
        """
        return {
            'id': self.id,
            'step_index': self.step_index,
            'voltage1': self.voltage1,
            'voltage2': self.voltage2,
            'voltage3': self.voltage3,
            'current1': self.current1,
            'current2': self.current2,
            'current3': self.current3,
            'temperature1': self.temperature1,
            'temperature2': self.temperature2,
            'temperature3': self.temperature3
        }

    def __repr__(self):
        return f"<Batteries {self.id} - step_index: {self.step_index}, Voltage1: {self.voltage1}, Voltage2: {self.voltage2},\
                  Voltage3: {self.voltage3}, Current1: {self.current1}, Current2: {self.current2}, Current3: {self.current3},\
                  Temperature1: {self.temperature1}, Temperature2: {self.temperature2}, Temperature3: {self.temperature3}>"
