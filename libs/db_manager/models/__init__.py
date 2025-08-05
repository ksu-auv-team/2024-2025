from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .inputs import Input  # registers Input table
from .outputs import Outputs  # registers Output table
from .batteries import Batteries  # registers Batteries table
from .externals import ExternalPressure, ExternalDepth  # registers ExternalPressure and ExternalDepth tables
from .imu import IMU  # registers IMU table
from .internals import InternalTemperature, InternalHumidity, InternalPressure  # registers InternalTemperature, InternalHumidity, and InternalPressure tables
from .sonar import Sonar  # registers Sonar table