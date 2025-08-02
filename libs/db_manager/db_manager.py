# Local imports
from .config_loader import ConfigLoader
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# Initialize ConfigLoader
config_loader = ConfigLoader()

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

    def __repr__(self):
        return f"<Outputs {self.id} - step_index: {self.step_index}, Direction: {self.direction}, Force: {self.force},\
                  M1: {self.M1}, M2: {self.M2}, M3: {self.M3}, M4: {self.M4}, M5: {self.M5}, M6: {self.M6},\
                  M7: {self.M7}, M8: {self.M8}, S1: {self.S1}, S2: {self.S2}, S3: {self.S3}, Arm: {self.arm}>"
    
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

    def __repr__(self):
        return f"<Sonar {self.id} - step_index: {self.step_index}, Distance: {self.distance}, Angle: {self.angle}>"
    
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
    id = db.Column(db.Integer, primary_key=True)
    step_index = db.Column(db.Integer, nullable=False)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    roll = db.Column(db.Float, nullable=False)
    pitch = db.Column(db.Float, nullable=False)
    yaw = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<IMU {self.id} - step_index: {self.step_index}, X: {self.X}, Y: {self.Y}, Z: {self.Z}, Roll: {self.roll}, Pitch: {self.pitch}, Yaw: {self.yaw}>"
    
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

    def __repr__(self):
        return f"<Batteries {self.id} - step_index: {self.step_index}, Voltage1: {self.voltage1}, Voltage2: {self.voltage2},\
                  Voltage3: {self.voltage3}, Current1: {self.current1}, Current2: {self.current2}, Current3: {self.current3},\
                  Temperature1: {self.temperature1}, Temperature2: {self.temperature2}, Temperature3: {self.temperature3}>"
    
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

    def __repr__(self):
        return f"<InternalPressure {self.id} - step_index: {self.step_index}, Pressure: {self.pressure}>"
    
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

    def __repr__(self):
        return f"<ExternalDepth {self.id} - step_index: {self.step_index}, Depth: {self.depth}>"

# Create the necessary routes for each model with error handling

# Inputs routes
# Post route to add a new input
@app.route('/post_input', methods=['POST'])
def post_input():
    try:
        data = request.get_json()
        new_input = Inputs(
            step_index=data['step_index'],
            direction=data['direction'],
            force=data['force'],
            s1=data['s1'],
            s2=data['s2'],
            s3=data['s3'],
            arm=data['arm']
        )
        db.session.add(new_input)
        db.session.commit()
        return jsonify({"message": "Input added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
# Get route to retrieve all inputs
@app.route('/get_inputs', methods=['GET'])
def get_inputs():
    try:
        inputs = Inputs.query.all()
        return jsonify([input.__dict__ for input in inputs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific input by step_index
@app.route('/get_input/<int:step_index>', methods=['GET'])
def get_input(step_index):
    try:
        input_data = Inputs.query.filter_by(step_index=step_index).first()
        if input_data:
            return jsonify(input_data.__dict__), 200
        else:
            return jsonify({"error": "Input not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve the latest input
@app.route('/get_latest_input', methods=['GET'])
def get_latest_input():
    try:
        latest_input = Inputs.query.order_by(Inputs.id.desc()).first()
        if latest_input:
            return jsonify(latest_input.__dict__), 200
        else:
            return jsonify({"error": "No inputs found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Outputs routes
# Post route to add a new output
@app.route('/post_output', methods=['POST'])
def post_output():
    try:
        data = request.get_json()
        new_output = Outputs(
            step_index=data['step_index'],
            direction=data['direction'],
            force=data['force'],
            M1=data['M1'],
            M2=data['M2'],
            M3=data['M3'],
            M4=data['M4'],
            M5=data['M5'],
            M6=data['M6'],
            M7=data['M7'],
            M8=data['M8'],
            S1=data['S1'],
            S2=data['S2'],
            S3=data['S3'],
            arm=data['arm']
        )
        db.session.add(new_output)
        db.session.commit()
        return jsonify({"message": "Output added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all outputs
@app.route('/get_outputs', methods=['GET'])
def get_outputs():
    try:
        outputs = Outputs.query.all()
        return jsonify([output.__dict__ for output in outputs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific output by step_index
@app.route('/get_output/<int:step_index>', methods=['GET'])
def get_output(step_index):
    try:
        output_data = Outputs.query.filter_by(step_index=step_index).first()
        if output_data:
            return jsonify(output_data.__dict__), 200
        else:
            return jsonify({"error": "Output not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest output
@app.route('/get_latest_output', methods=['GET'])
def get_latest_output():
    try:
        latest_output = Outputs.query.order_by(Outputs.id.desc()).first()
        if latest_output:
            return jsonify(latest_output.__dict__), 200
        else:
            return jsonify({"error": "No outputs found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Sonar routes
# Post route to add a new sonar data
@app.route('/post_sonar', methods=['POST'])
def post_sonar():
    try:
        data = request.get_json()
        new_sonar = Sonar(
            step_index=data['step_index'],
            distance=data['distance'],
            angle=data['angle']
        )
        db.session.add(new_sonar)
        db.session.commit()
        return jsonify({"message": "Sonar data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all sonar data
@app.route('/get_sonar', methods=['GET'])
def get_sonar():
    try:
        sonar_data = Sonar.query.all()
        return jsonify([sonar.__dict__ for sonar in sonar_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific sonar data by step_index
@app.route('/get_sonar/<int:step_index>', methods=['GET'])
def get_sonar_by_step(step_index):
    try:
        sonar_data = Sonar.query.filter_by(step_index=step_index).first()
        if sonar_data:
            return jsonify(sonar_data.__dict__), 200
        else:
            return jsonify({"error": "Sonar data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest sonar data
@app.route('/get_latest_sonar', methods=['GET'])
def get_latest_sonar():
    try:
        latest_sonar = Sonar.query.order_by(Sonar.id.desc()).first()
        if latest_sonar:
            return jsonify(latest_sonar.__dict__), 200
        else:
            return jsonify({"error": "No sonar data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# IMU routes
# Post route to add a new IMU data
@app.route('/post_imu', methods=['POST'])
def post_imu():
    try:
        data = request.get_json()
        new_imu = IMU(
            step_index=data['step_index'],
            X=data['X'],
            Y=data['Y'],
            Z=data['Z'],
            roll=data['roll'],
            pitch=data['pitch'],
            yaw=data['yaw']
        )
        db.session.add(new_imu)
        db.session.commit()
        return jsonify({"message": "IMU data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all IMU data
@app.route('/get_imu', methods=['GET'])
def get_imu():
    try:
        imu_data = IMU.query.all()
        return jsonify([imu.__dict__ for imu in imu_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific IMU data by step_index
@app.route('/get_imu/<int:step_index>', methods=['GET'])
def get_imu_by_step(step_index):
    try:
        imu_data = IMU.query.filter_by(step_index=step_index).first()
        if imu_data:
            return jsonify(imu_data.__dict__), 200
        else:
            return jsonify({"error": "IMU data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest IMU data
@app.route('/get_latest_imu', methods=['GET'])
def get_latest_imu():
    try:
        latest_imu = IMU.query.order_by(IMU.id.desc()).first()
        if latest_imu:
            return jsonify(latest_imu.__dict__), 200
        else:
            return jsonify({"error": "No IMU data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Batteries routes
# Post route to add a new battery data
@app.route('/post_battery', methods=['POST'])
def post_battery():
    try:
        data = request.get_json()
        new_battery = Batteries(
            step_index=data['step_index'],
            voltage1=data['voltage1'],
            voltage2=data['voltage2'],
            voltage3=data['voltage3'],
            current1=data['current1'],
            current2=data['current2'],
            current3=data['current3'],
            temperature1=data['temperature1'],
            temperature2=data['temperature2'],
            temperature3=data['temperature3']
        )
        db.session.add(new_battery)
        db.session.commit()
        return jsonify({"message": "Battery data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all battery data
@app.route('/get_battery', methods=['GET'])
def get_battery():
    try:
        battery_data = Batteries.query.all()
        return jsonify([battery.__dict__ for battery in battery_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific battery data by step_index
@app.route('/get_battery/<int:step_index>', methods=['GET'])
def get_battery_by_step(step_index):
    try:
        battery_data = Batteries.query.filter_by(step_index=step_index).first()
        if battery_data:
            return jsonify(battery_data.__dict__), 200
        else:
            return jsonify({"error": "Battery data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve the latest battery data
@app.route('/get_latest_battery', methods=['GET'])
def get_latest_battery():
    try:
        latest_battery = Batteries.query.order_by(Batteries.id.desc()).first()
        if latest_battery:
            return jsonify(latest_battery.__dict__), 200
        else:
            return jsonify({"error": "No battery data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Internal Temperature routes
# Post route to add a new internal temperature data
@app.route('/post_internal_temperature', methods=['POST'])
def post_internal_temperature():
    try:
        data = request.get_json()
        new_internal_temp = InternalTemperature(
            step_index=data['step_index'],
            temperature=data['temperature']
        )
        db.session.add(new_internal_temp)
        db.session.commit()
        return jsonify({"message": "Internal temperature data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get route to retrieve all internal temperature data
@app.route('/get_internal_temperature', methods=['GET'])
def get_internal_temperature():
    try:
        internal_temp_data = InternalTemperature.query.all()
        return jsonify([temp.__dict__ for temp in internal_temp_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific internal temperature data by step_index
@app.route('/get_internal_temperature/<int:step_index>', methods=['GET'])
def get_internal_temperature_by_step(step_index):
    try:
        internal_temp_data = InternalTemperature.query.filter_by(step_index=step_index).first()
        if internal_temp_data:
            return jsonify(internal_temp_data.__dict__), 200
        else:
            return jsonify({"error": "Internal temperature data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest internal temperature data
@app.route('/get_latest_internal_temperature', methods=['GET'])
def get_latest_internal_temperature():
    try:
        latest_internal_temp = InternalTemperature.query.order_by(InternalTemperature.id.desc()).first()
        if latest_internal_temp:
            return jsonify(latest_internal_temp.__dict__), 200
        else:
            return jsonify({"error": "No internal temperature data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Internal Humidity routes
# Post route to add a new internal humidity data
@app.route('/post_internal_humidity', methods=['POST'])
def post_internal_humidity():
    try:
        data = request.get_json()
        new_internal_humidity = InternalHumidity(
            step_index=data['step_index'],
            humidity=data['humidity']
        )
        db.session.add(new_internal_humidity)
        db.session.commit()
        return jsonify({"message": "Internal humidity data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all internal humidity data
@app.route('/get_internal_humidity', methods=['GET'])
def get_internal_humidity():
    try:
        internal_humidity_data = InternalHumidity.query.all()
        return jsonify([humidity.__dict__ for humidity in internal_humidity_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific internal humidity data by step_index
@app.route('/get_internal_humidity/<int:step_index>', methods=['GET'])
def get_internal_humidity_by_step(step_index):
    try:
        internal_humidity_data = InternalHumidity.query.filter_by(step_index=step_index).first()
        if internal_humidity_data:
            return jsonify(internal_humidity_data.__dict__), 200
        else:
            return jsonify({"error": "Internal humidity data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest internal humidity data
@app.route('/get_latest_internal_humidity', methods=['GET'])
def get_latest_internal_humidity():
    try:
        latest_internal_humidity = InternalHumidity.query.order_by(InternalHumidity.id.desc()).first()
        if latest_internal_humidity:
            return jsonify(latest_internal_humidity.__dict__), 200
        else:
            return jsonify({"error": "No internal humidity data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Internal Pressure routes
# Post route to add a new internal pressure data
@app.route('/post_internal_pressure', methods=['POST'])
def post_internal_pressure():
    try:
        data = request.get_json()
        new_internal_pressure = InternalPressure(
            step_index=data['step_index'],
            pressure=data['pressure']
        )
        db.session.add(new_internal_pressure)
        db.session.commit()
        return jsonify({"message": "Internal pressure data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all internal pressure data
@app.route('/get_internal_pressure', methods=['GET'])
def get_internal_pressure():
    try:
        internal_pressure_data = InternalPressure.query.all()
        return jsonify([pressure.__dict__ for pressure in internal_pressure_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific internal pressure data by step_index
@app.route('/get_internal_pressure/<int:step_index>', methods=['GET'])
def get_internal_pressure_by_step(step_index):
    try:
        internal_pressure_data = InternalPressure.query.filter_by(step_index=step_index).first()
        if internal_pressure_data:
            return jsonify(internal_pressure_data.__dict__), 200
        else:
            return jsonify({"error": "Internal pressure data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest internal pressure data
@app.route('/get_latest_internal_pressure', methods=['GET'])
def get_latest_internal_pressure():
    try:
        latest_internal_pressure = InternalPressure.query.order_by(InternalPressure.id.desc()).first()
        if latest_internal_pressure:
            return jsonify(latest_internal_pressure.__dict__), 200
        else:
            return jsonify({"error": "No internal pressure data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# External Pressure routes
# Post route to add a new external pressure data
@app.route('/post_external_pressure', methods=['POST'])
def post_external_pressure():
    try:
        data = request.get_json()
        new_external_pressure = ExternalPressure(
            step_index=data['step_index'],
            pressure=data['pressure']
        )
        db.session.add(new_external_pressure)
        db.session.commit()
        return jsonify({"message": "External pressure data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all external pressure data
@app.route('/get_external_pressure', methods=['GET'])
def get_external_pressure():
    try:
        external_pressure_data = ExternalPressure.query.all()
        return jsonify([pressure.__dict__ for pressure in external_pressure_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific external pressure data by step_index
@app.route('/get_external_pressure/<int:step_index>', methods=['GET'])
def get_external_pressure_by_step(step_index):
    try:
        external_pressure_data = ExternalPressure.query.filter_by(step_index=step_index).first()
        if external_pressure_data:
            return jsonify(external_pressure_data.__dict__), 200
        else:
            return jsonify({"error": "External pressure data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest external pressure data
@app.route('/get_latest_external_pressure', methods=['GET'])
def get_latest_external_pressure():
    try:
        latest_external_pressure = ExternalPressure.query.order_by(ExternalPressure.id.desc()).first()
        if latest_external_pressure:
            return jsonify(latest_external_pressure.__dict__), 200
        else:
            return jsonify({"error": "No external pressure data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# External Depth routes
# Post route to add a new external depth data
@app.route('/post_external_depth', methods=['POST'])
def post_external_depth():
    try:
        data = request.get_json()
        new_external_depth = ExternalDepth(
            step_index=data['step_index'],
            depth=data['depth']
        )
        db.session.add(new_external_depth)
        db.session.commit()
        return jsonify({"message": "External depth data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all external depth data
@app.route('/get_external_depth', methods=['GET'])
def get_external_depth():
    try:
        external_depth_data = ExternalDepth.query.all()
        return jsonify([depth.__dict__ for depth in external_depth_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific external depth data by step_index
@app.route('/get_external_depth/<int:step_index>', methods=['GET'])
def get_external_depth_by_step(step_index):
    try:
        external_depth_data = ExternalDepth.query.filter_by(step_index=step_index).first()
        if external_depth_data:
            return jsonify(external_depth_data.__dict__), 200
        else:
            return jsonify({"error": "External depth data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest external depth data
@app.route('/get_latest_external_depth', methods=['GET'])
def get_latest_external_depth():
    try:
        latest_external_depth = ExternalDepth.query.order_by(ExternalDepth.id.desc()).first()
        if latest_external_depth:
            return jsonify(latest_external_depth.__dict__), 200
        else:
            return jsonify({"error": "No external depth data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Create the database tables
with app.app_context():
    db.create_all()

# Run the Flask application
