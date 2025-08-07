import Jetson.GPIO as GPIO
import smbus2
import struct
import time

# === CONFIGURATION ===
I2C_BUS = 1
I2C_ADDRESS = 0x4B  # Depends on SA0 pin (0x4A or 0x4B)
MAX_PACKET_SIZE = 512
INT_PIN = 17  # GPIO pin for interrupt (if used)

# SHTP Header Fields
SHTP_HEADER_LENGTH = 4
CHANNEL_COMMAND = 0
CHANNEL_EXECUTABLE = 1
CHANNEL_CONTROL = 2
CHANNEL_INPUT_REPORTS = 3
CHANNEL_WAKE_REPORTS = 4
CHANNEL_GYRO_ROTATION_VECTOR = 5

# Report IDs
REPORT_ID_ROTATION_VECTOR = 0x05
REPORT_ID_ACCELEROMETER = 0x01
REPORT_ID_GYROSCOPE = 0x02

# === INIT I2C BUS ===
bus = smbus2.SMBus(I2C_BUS)

class BNO08X:
    def __init__(self, address=I2C_ADDRESS):
        self.address = address
        self.sequence_numbers = [0] * 6  # One for each channel
        self.rotation_vector_enabled = False
        self.init_sensor()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def wait_for_interrupt(self):
        """ Wait for an interrupt signal from the sensor """
        start = time.time()
        while GPIO.input(INT_PIN) == GPIO.HIGH:
            if time.time() - start > 5:
                raise TimeoutError("Timeout waiting for sensor interrupt")
            time.sleep(0.01)
        # Interrupt received
        print("Interrupt received from sensor")

    def init_sensor(self):
        """ Wait for boot and initialize rotation vector """
        print("Waiting for sensor boot...")
        time.sleep(1)
        self.flush_input()
        self.enable_rotation_vector()

    def flush_input(self):
        """ Clear existing input by reading until no data """
        while True:
            try:
                length = self.read_header_length()
                if length == 0:
                    break
                self.read_payload(length)
            except:
                break

    def read_header_length(self):
        """ Read 4-byte SHTP header and return payload length """
        try:
            data = bus.read_i2c_block_data(self.address, 0, 4)
            length = data[0] | (data[1] << 8)
            return length - 4  # remove header size
        except OSError:
            return 0

    def read_payload(self, length):
        if length <= 0:
            return []
        return bus.read_i2c_block_data(self.address, 0, length)

    def enable_rotation_vector(self, report_interval_us=10000):
        """ Enable Rotation Vector @ 100Hz (10,000 us interval) """
        feature_cmd = [
            0xFD,               # Set Feature Command
            0x05,               # Rotation Vector Feature Report ID
            0x00,               # Feature Flags
            0x00, 0x00,         # Change sensitivity (LSB/MSB)
            *self.us_to_bytes(report_interval_us),  # Report Interval
            0x00, 0x00, 0x00, 0x00,                 # Batch interval
            0x00, 0x00, 0x00, 0x00                  # Sensor-specific config
        ]
        self.send_packet(CHANNEL_CONTROL, feature_cmd)
        self.rotation_vector_enabled = True

    def us_to_bytes(self, value):
        """ Convert 32-bit microsecond value to little-endian bytes """
        return [value & 0xFF,
                (value >> 8) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 24) & 0xFF]

    def send_packet(self, channel, payload):
        length = len(payload) + 4
        header = [length & 0xFF, (length >> 8) & 0xFF, channel, self.sequence_numbers[channel]]
        self.sequence_numbers[channel] = (self.sequence_numbers[channel] + 1) % 256
        packet = header + payload
        bus.write_i2c_block_data(self.address, 0, packet)

    def read_rotation_vector(self):
        """ Poll until a rotation vector report is available """
        try:
            header = bus.read_i2c_block_data(self.address, 0, 4)
            length = header[0] | (header[1] << 8)
            channel = header[2]
            if channel != CHANNEL_INPUT_REPORTS:
                return None

            payload = bus.read_i2c_block_data(self.address, 0, length - 4)
            report_id = payload[0]

            if report_id == REPORT_ID_ROTATION_VECTOR:
                quat_i = struct.unpack_from("<hhhh", bytes(payload[5:13]))  # x, y, z, real
                accuracy = payload[13]
                return {
                    'x': quat_i[0] / 16384.0,
                    'y': quat_i[1] / 16384.0,
                    'z': quat_i[2] / 16384.0,
                    'w': quat_i[3] / 16384.0,
                    'accuracy': accuracy
                }
        except Exception as e:
            return None

    def loop_print(self):
        print("Reading rotation vector data...")
        while True:
            self.wait_for_interrupt()
            result = self.read_rotation_vector()
            if result:
                print(f"Quat: x={result['x']:.4f}, y={result['y']:.4f}, z={result['z']:.4f}, w={result['w']:.4f}, acc={result['accuracy']}")
            time.sleep(0.01)

if __name__ == "__main__":
    imu = BNO08X()
    imu.loop_print()
