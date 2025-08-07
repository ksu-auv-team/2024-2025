import smbus2
import struct
import time
import Jetson.GPIO as GPIO
from smbus2 import i2c_msg

# === CONFIGURATION ===
I2C_BUS = 1
I2C_ADDRESS = 0x4B
H_INTN_GPIO = 17

# === CONSTANTS ===
SHTP_HEADER_LENGTH = 4
CHANNEL_CONTROL = 2
CHANNEL_INPUT_REPORTS = 3

REPORT_ID_ROTATION_VECTOR = 0x05
SYSTEM_REPORT_IDS = {0xF9, 0xFA, 0xFB, 0xFC}

# === INIT GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(H_INTN_GPIO, GPIO.IN)

# === INIT I2C ===
bus = smbus2.SMBus(I2C_BUS)

class BNO08X:
    def __init__(self, address=I2C_ADDRESS):
        self.address = address
        self.sequence_numbers = [0] * 6
        self.rotation_vector_enabled = False

        self.wait_for_interrupt("boot")
        self.sync_boot_messages()
        self.enable_rotation_vector()
        self.wait_for_interrupt("data ready")

    def wait_for_interrupt(self, label="", timeout=5.0):
        print(f"⏳ Waiting for H_INTN ({label}) to go LOW...")
        start = time.time()
        while GPIO.input(H_INTN_GPIO) == GPIO.HIGH:
            if time.time() - start > timeout:
                raise TimeoutError(f"Timeout waiting for H_INTN ({label})")
            time.sleep(0.01)
        print(f"✅ H_INTN ({label}) LOW")

    def read_header_length(self):
        try:
            header = bus.read_i2c_block_data(self.address, 0, 4)
            length = header[0] | (header[1] << 8)
            channel = header[2]
            return length - 4, channel
        except Exception:
            return 0, None

    def read_payload(self, length):
        if length <= 0:
            return []
        return bus.read_i2c_block_data(self.address, 0, length)

    def sync_boot_messages(self):
        print("🔍 Reading boot messages...")
        while True:
            self.wait_for_interrupt("boot sync")
            length, channel = self.read_header_length()
            if length <= 0 or channel is None:
                continue

            payload = self.read_payload(length)
            if not payload:
                continue

            report_id = payload[0]
            print(f"📥 Boot Report ID: 0x{report_id:02X} Payload: {payload}")
            if report_id in SYSTEM_REPORT_IDS:
                print("✅ Boot sync complete.")
                break

    def us_to_bytes(self, value):
        return [value & 0xFF, (value >> 8) & 0xFF,
                (value >> 16) & 0xFF, (value >> 24) & 0xFF]

    def send_packet(self, channel, payload):
        length = len(payload) + 4
        header = [length & 0xFF, (length >> 8) & 0xFF, channel, self.sequence_numbers[channel]]
        self.sequence_numbers[channel] = (self.sequence_numbers[channel] + 1) % 256
        packet = header + payload

        print(f"📤 Sending packet on channel {channel}: {packet}")
        try:
            msg = i2c_msg.write(self.address, packet)
            bus.i2c_rdwr(msg)
        except OSError as e:
            print(f"❌ Error sending packet: {e}")
            raise RuntimeError(f"Failed to send I2C packet: {e}")

    def enable_rotation_vector(self, report_interval_us=10000):
        print("🛰️ Enabling Rotation Vector...")
        feature_cmd = [
            0xFD,               # Set Feature Command
            REPORT_ID_ROTATION_VECTOR,
            0x00,               # Feature Flags
            0x00, 0x00,         # Change sensitivity
            *self.us_to_bytes(report_interval_us),  # Report Interval
            0x00, 0x00, 0x00, 0x00,                 # Batch interval
            0x00, 0x00, 0x00, 0x00                  # Sensor-specific config
        ]
        self.send_packet(CHANNEL_CONTROL, feature_cmd)
        print("✅ Rotation Vector enabled.")

    def read_rotation_vector(self):
        self.wait_for_interrupt("rotation data")
        header = bus.read_i2c_block_data(self.address, 0, 4)
        length = header[0] | (header[1] << 8)
        channel = header[2]

        if channel != CHANNEL_INPUT_REPORTS:
            return None

        payload = bus.read_i2c_block_data(self.address, 0, length - 4)
        if payload[0] != REPORT_ID_ROTATION_VECTOR:
            return None

        quat = struct.unpack_from("<hhhh", bytes(payload[5:13]))
        accuracy = payload[13]

        return {
            'x': quat[0] / 16384.0,
            'y': quat[1] / 16384.0,
            'z': quat[2] / 16384.0,
            'w': quat[3] / 16384.0,
            'accuracy': accuracy
        }

    def loop_print(self):
        print("🔁 Reading rotation vector...")
        try:
            while True:
                result = self.read_rotation_vector()
                if result:
                    print(f"Quat: x={result['x']:.4f}, y={result['y']:.4f}, z={result['z']:.4f}, w={result['w']:.4f}, acc={result['accuracy']}")
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("🛑 Exiting...")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    imu = BNO08X()
    imu.loop_print()
