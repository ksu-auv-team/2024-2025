from marshmallow import Schema, fields
from .models import db
from .models.inputs import Input
from .models.outputs import Outputs
from .models.batteries import Batteries
from .models.externals import ExternalPressure, ExternalDepth
from .models.imu import IMU
from .models.internals import InternalTemperature, InternalHumidity, InternalPressure
from .models.sonar import Sonar

class InputSchema(Schema):
    step_index = fields.Int(required=True)
    direction = fields.Str(required=True)
    force = fields.Float(required=True)
    s1 = fields.Float(required=True)
    s2 = fields.Float(required=True)
    s3 = fields.Float(required=True)
    arm = fields.Bool(required=True)

input_schema = InputSchema()
inputs_schema = InputSchema(many=True)

def create_input(data):
    validated = input_schema.load(data)
    new_input = Input(**validated)
    db.session.add(new_input)
    db.session.commit()
    return new_input.to_dict()

def list_inputs():
    return [i.to_dict() for i in Input.query.order_by(Input.step_index.asc()).all()]

def get_latest_input():
    input_obj = Input.query.order_by(Input.id.desc()).first()
    return input_obj.to_dict() if input_obj else None

class OutputSchema(Schema):
    step_index = fields.Int(required=True)
    direction = fields.Str(required=True)
    force = fields.Float(required=True)
    M1 = fields.Float(required=True)
    M2 = fields.Float(required=True)
    M3 = fields.Float(required=True)
    M4 = fields.Float(required=True)
    M5 = fields.Float(required=True)
    M6 = fields.Float(required=True)
    M7 = fields.Float(required=True)
    M8 = fields.Float(required=True)
    S1 = fields.Float(required=True)
    S2 = fields.Float(required=True)
    S3 = fields.Float(required=True)
    arm = fields.Bool(required=True)

output_schema = OutputSchema()
outputs_schema = OutputSchema(many=True)

def create_output(data):
    validated = output_schema.load(data)
    new_output = Outputs(**validated)
    db.session.add(new_output)
    db.session.commit()
    return new_output.to_dict()

def list_outputs():
    return [o.to_dict() for o in Outputs.query.order_by(Outputs.step_index.asc()).all()]

def get_latest_output():
    output_obj = Outputs.query.order_by(Outputs.id.desc()).first()
    return output_obj.to_dict() if output_obj else None

class BatteriesSchema(Schema):
    step_index = fields.Int(required=True)
    voltage1 = fields.Float(required=True)
    voltage2 = fields.Float(required=True)
    voltage3 = fields.Float(required=True)
    current1 = fields.Float(required=True)
    current2 = fields.Float(required=True)
    current3 = fields.Float(required=True)
    temperature1 = fields.Float(required=True)
    temperature2 = fields.Float(required=True)
    temperature3 = fields.Float(required=True)

batteries_schema = BatteriesSchema()
batteries_list_schema = BatteriesSchema(many=True)

def create_battery(data):
    validated = batteries_schema.load(data)
    new_battery = Batteries(**validated)
    db.session.add(new_battery)
    db.session.commit()
    return new_battery.to_dict()

def list_batteries():
    return [b.to_dict() for b in Batteries.query.order_by(Batteries.step_index.asc()).all()]

def get_latest_battery():
    battery_obj = Batteries.query.order_by(Batteries.id.desc()).first()
    return battery_obj.to_dict() if battery_obj else None


class ExternalPressureSchema(Schema):
    step_index = fields.Int(required=True)
    pressure = fields.Float(required=True)

external_pressure_schema = ExternalPressureSchema()
external_pressures_schema = ExternalPressureSchema(many=True)

def create_external_pressure(data):
    validated = external_pressure_schema.load(data)
    new_external_pressure = ExternalPressure(**validated)
    db.session.add(new_external_pressure)
    db.session.commit()
    return new_external_pressure.to_dict()

def list_external_pressures():
    return [ep.to_dict() for ep in ExternalPressure.query.order_by(ExternalPressure.step_index.asc()).all()]

def get_latest_external_pressure():
    external_pressure_obj = ExternalPressure.query.order_by(ExternalPressure.id.desc()).first()
    return external_pressure_obj.to_dict() if external_pressure_obj else None

class ExternalDepthSchema(Schema):
    step_index = fields.Int(required=True)
    depth = fields.Float(required=True)

external_depth_schema = ExternalDepthSchema()
external_depths_schema = ExternalDepthSchema(many=True)

def create_external_depth(data):
    validated = external_depth_schema.load(data)
    new_external_depth = ExternalDepth(**validated)
    db.session.add(new_external_depth)
    db.session.commit()
    return new_external_depth.to_dict()

def list_external_depths():
    return [ed.to_dict() for ed in ExternalDepth.query.order_by(ExternalDepth.step_index.asc()).all()]

def get_latest_external_depth():
    external_depth_obj = ExternalDepth.query.order_by(ExternalDepth.id.desc()).first()
    return external_depth_obj.to_dict() if external_depth_obj else None

class IMUSchema(Schema):
    step_index = fields.Int(required=True)
    X = fields.Float(required=True)
    Y = fields.Float(required=True)
    Z = fields.Float(required=True)
    roll = fields.Float(required=True)
    pitch = fields.Float(required=True)
    yaw = fields.Float(required=True)
imu_schema = IMUSchema()
imus_schema = IMUSchema(many=True)

def create_imu(data):
    validated = imu_schema.load(data)
    new_imu = IMU(**validated)
    db.session.add(new_imu)
    db.session.commit()
    return new_imu.to_dict()

def list_imus():
    return [imu.to_dict() for imu in IMU.query.order_by(IMU.step_index.asc()).all()]

def get_latest_imu():
    imu_obj = IMU.query.order_by(IMU.id.desc()).first()
    return imu_obj.to_dict() if imu_obj else None

class InternalTemperatureSchema(Schema):
    step_index = fields.Int(required=True)
    temperature = fields.Float(required=True)

internal_temperature_schema = InternalTemperatureSchema()
internal_temperatures_schema = InternalTemperatureSchema(many=True)

def create_internal_temperature(data):
    validated = internal_temperature_schema.load(data)
    new_internal_temperature = InternalTemperature(**validated)
    db.session.add(new_internal_temperature)
    db.session.commit()
    return new_internal_temperature.to_dict()

def list_internal_temperatures():
    return [it.to_dict() for it in InternalTemperature.query.order_by(InternalTemperature.step_index.asc()).all()]

def get_latest_internal_temperature():
    internal_temperature_obj = InternalTemperature.query.order_by(InternalTemperature.id.desc()).first()
    return internal_temperature_obj.to_dict() if internal_temperature_obj else None

class InternalHumiditySchema(Schema):
    step_index = fields.Int(required=True)
    humidity = fields.Float(required=True)

internal_humidity_schema = InternalHumiditySchema()
internal_humidities_schema = InternalHumiditySchema(many=True)

def create_internal_humidity(data):
    validated = internal_humidity_schema.load(data)
    new_internal_humidity = InternalHumidity(**validated)
    db.session.add(new_internal_humidity)
    db.session.commit()
    return new_internal_humidity.to_dict()

def list_internal_humidities():
    return [ih.to_dict() for ih in InternalHumidity.query.order_by(InternalHumidity.step_index.asc()).all()]

def get_latest_internal_humidity():
    internal_humidity_obj = InternalHumidity.query.order_by(InternalHumidity.id.desc()).first()
    return internal_humidity_obj.to_dict() if internal_humidity_obj else None

class InternalPressureSchema(Schema):
    step_index = fields.Int(required=True)
    pressure = fields.Float(required=True)

internal_pressure_schema = InternalPressureSchema()
internal_pressures_schema = InternalPressureSchema(many=True)

def create_internal_pressure(data):
    validated = internal_pressure_schema.load(data)
    new_internal_pressure = InternalPressure(**validated)
    db.session.add(new_internal_pressure)
    db.session.commit()
    return new_internal_pressure.to_dict()

def list_internal_pressures():
    return [ip.to_dict() for ip in InternalPressure.query.order_by(InternalPressure.step_index.asc()).all()]

def get_latest_internal_pressure():
    internal_pressure_obj = InternalPressure.query.order_by(InternalPressure.id.desc()).first()
    return internal_pressure_obj.to_dict() if internal_pressure_obj else None

class SonarSchema(Schema):
    step_index = fields.Int(required=True)
    distance = fields.Float(required=True)
    angle = fields.Float(required=True)

sonar_schema = SonarSchema()
sonars_schema = SonarSchema(many=True)

def create_sonar(data):
    validated = sonar_schema.load(data)
    new_sonar = Sonar(**validated)
    db.session.add(new_sonar)
    db.session.commit()
    return new_sonar.to_dict()

def list_sonars():
    return [s.to_dict() for s in Sonar.query.order_by(Sonar.step_index.asc()).all()]

def get_latest_sonar():
    sonar_obj = Sonar.query.order_by(Sonar.id.desc()).first()
    return sonar_obj.to_dict() if sonar_obj else None