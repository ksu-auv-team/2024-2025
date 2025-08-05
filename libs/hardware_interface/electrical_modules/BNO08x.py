import smbus2
import time
import struct

I2C_BUS = 1
I2C_ADDR = 0x4B

# Feature report IDs
FEATURE_ROTATION_VECTOR = 0x05
INPUT_REPORT_ID = 0x05
SHTP_HEADER_LEN = 4
SENSOR_REPORT_ROTATION_VECTOR = 0x05

# SHTP channels
CHANNEL_CONTROL = 2
CHANNEL_INPUT = 1

# Initialize I2C
bus = smbus2.SMBus(I2C_BUS)

# === Utilities ===

def shtp_send(channel, data):
    length = len(data)
    header = [length & 0xFF, (length >> 8) & 0xFF, channel, 0]
    bus.write_i2c_block_data(I2C_ADDR, 0, header + data)

def enable_rotation_vector():
    feature_cmd = [
        0xFD,  # Set Feature Command
        FEATURE_ROTATION_VECTOR,
        0x00, 0x00, 0x00, 0x00,  # Feature flags
        0x20, 0x4E, 0x00, 0x00,  # Report interval (20ms -> 50Hz)
        0x00, 0x00, 0x00, 0x00,  # Batch interval
        0x00, 0x00              # Sensor-specific config
    ]
    shtp_send(CHANNEL_CONTROL, feature_cmd)
    print("Rotation Vector feature enabled.")

def parse_quaternion(data):
    # Data format: [report_id, status, delay, quat_i, quat_j, quat_k, quat_real, accuracy]
    quat_i = struct.unpack_from("<h", bytes(data), 4)[0] / 16384.0
    quat_j = struct.unpack_from("<h", bytes(data), 6)[0] / 16384.0
    quat_k = struct.unpack_from("<h", bytes(data), 8)[0] / 16384.0
    quat_real = struct.unpack_from("<h", bytes(data), 10)[0] / 16384.0
    return quat_i, quat_j, quat_k, quat_real

# === Main Logic ===

print("Initializing BNO08x on I2C bus 1 at address 0x4B...")
time.sleep(1)
enable_rotation_vector()
time.sleep(0.5)

try:
    while True:
        # Read SHTP packet header
        try:
            raw = bus.read_i2c_block_data(I2C_ADDR, 0, 32)
        except OSError as e:
            print(f"Read error: {e}")
            continue

        packet_length = raw[0] | (raw[1] << 8)
        channel = raw[2]

        if packet_length == 0:
            continue

        if channel == CHANNEL_INPUT and raw[4] == SENSOR_REPORT_ROTATION_VECTOR:
            quat = parse_quaternion(raw)
            print(f"Quaternion: i={quat[0]:.4f}, j={quat[1]:.4f}, k={quat[2]:.4f}, real={quat[3]:.4f}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    bus.close()
