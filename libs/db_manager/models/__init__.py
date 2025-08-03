# libs/db_manager/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .inputs import Input
from .outputs import Output
from .imu import IMU
from .sonar import Sonar
from .batteries import Battery
from .internals import InternalTemperature, InternalHumidity, InternalPressure
from .externals import ExternalDepth
