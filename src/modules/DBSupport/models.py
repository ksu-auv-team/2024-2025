"""models.py

Async SQLAlchemy ORM models for sensor, actuator, and telemetry data logging.
"""

from sqlalchemy import Column, Integer, Float, DateTime, func
from modules.DBSupport.db import Base


class BaseModel(Base):
    """
    Base model with common fields shared across all models.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
class Inputs(BaseModel):
    """
    @brief Represents control input values received from the AUV interface.
    """
    __tablename__ = 'inputs'

    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)
    roll = Column(Integer, nullable=False)
    pitch = Column(Integer, nullable=False)
    yaw = Column(Integer, nullable=False)
    s1 = Column(Integer, nullable=False)
    s2 = Column(Integer, nullable=False)
    s3 = Column(Integer, nullable=False)
    arm = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<Inputs(id={self.id}, x={self.x}, y={self.y}, z={self.z}, "
                f"roll={self.roll}, pitch={self.pitch}, yaw={self.yaw}, "
                f"s1={self.s1}, s2={self.s2}, s3={self.s3}, arm={self.arm})>")


class Outputs(BaseModel):
    """
    @brief Represents motor and servo output values sent to the AUV.
    """
    __tablename__ = 'outputs'

    m1 = Column(Integer, nullable=False)
    m2 = Column(Integer, nullable=False)
    m3 = Column(Integer, nullable=False)
    m4 = Column(Integer, nullable=False)
    m5 = Column(Integer, nullable=False)
    m6 = Column(Integer, nullable=False)
    m7 = Column(Integer, nullable=False)
    m8 = Column(Integer, nullable=False)
    s1 = Column(Integer, nullable=False)
    s2 = Column(Integer, nullable=False)
    s3 = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<Outputs(id={self.id}, m1={self.m1}, m2={self.m2}, m3={self.m3}, "
                f"m4={self.m4}, m5={self.m5}, m6={self.m6}, m7={self.m7}, m8={self.m8}, "
                f"s1={self.s1}, s2={self.s2}, s3={self.s3})>")


class Sonar(BaseModel):
    """
    @brief Represents sonar readings for distance and angle.
    """
    __tablename__ = 'sonar'

    distance = Column(Float, nullable=False)
    angle = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Sonar(id={self.id}, distance={self.distance}, angle={self.angle})>"


class Batteries(BaseModel):
    """
    @brief Represents battery telemetry data.
    """
    __tablename__ = 'batteries'

    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<Batteries(id={self.id}, voltage={self.voltage}, "
                f"current={self.current}, capacity={self.capacity})>")


class IMU(BaseModel):
    """
    @brief Represents Inertial Measurement Unit data.
    """
    __tablename__ = 'imu'

    acceleration_x = Column(Float, nullable=False)
    acceleration_y = Column(Float, nullable=False)
    acceleration_z = Column(Float, nullable=False)
    gyro_x = Column(Float, nullable=False)
    gyro_y = Column(Float, nullable=False)
    gyro_z = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<IMU(id={self.id}, ax={self.acceleration_x}, ay={self.acceleration_y}, "
                f"az={self.acceleration_z}, gx={self.gyro_x}, gy={self.gyro_y}, gz={self.gyro_z})>")


class Sensors(BaseModel):
    """
    @brief Represents environmental sensor readings.
    """
    __tablename__ = 'sensors'

    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    heading = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<Sensors(id={self.id}, temperature={self.temperature}, humidity={self.humidity}, "
                f"pressure={self.pressure}, depth={self.depth}, heading={self.heading})>")

