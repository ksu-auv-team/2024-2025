import smbus2
import struct
import time
import math

# I2C configuration
I2C_BUS = 1
BNO085_ADDR = 0x4B

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

# ✅ LOW-LEVEL DIAGNOSTIC CHECK
try:
    data = bus.read_byte(BNO085_ADDR)
    print(f"BNO08x responded with byte: {data}")
except Exception as e:
    print(f"Low-level I2C read failed: {e}")
    exit(1)  # Exit script early if the sensor isn't responding

# Helper to convert quaternion to Euler angles (roll, pitch, yaw)
def quaternion_to_euler(w, x, y, z):
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)

    t2 = 2.0 * (w * y - z * x)
    t2 = max(min(t2, 1.0), -1.0)
    pitch = math.asin(t2)

    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)

    # Convert from radians to degrees
    return (
        math.degrees(roll),
        math.degrees(pitch),
        math.degrees(yaw)
    )

def read_sensor_data():
    try:
        # Read the header (4 bytes)
        header = bus.read_i2c_block_data(BNO085_ADDR, 0, 4)
        packet_length = header[0] | (header[1] << 8)

        # If no data or nonsense length
        if packet_length < 4 or packet_length > 128:
            return

        # Read packet
        packet = bus.read_i2c_block_data(BNO085_ADDR, 0, packet_length)
        report_id = packet[4]

        if report_id == 0x05:  # Rotation Vector
            q_i = struct.unpack_from("<hhhh", bytearray(packet), offset=5)
            real = [val / (1 << 14) for val in q_i]
            roll, pitch, yaw = quaternion_to_euler(*real)
            print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")

        elif report_id == 0x01:  # Acceleration
            accel_raw = struct.unpack_from("<hhh", bytearray(packet), offset=5)
            accel = [val / 100.0 for val in accel_raw]
            print(f"Accel X: {accel[0]:.2f}, Y: {accel[1]:.2f}, Z: {accel[2]:.2f}")

    except OSError as e:
        if e.errno == 121:
            print("No data ready, skipping read.")
        else:
            print(f"OSError: {e}")

# Enable features (once)
def enable_features():
    # Define rotation vector feature command
    # Format: [Report ID (0xFD), Feature ID (0x05), Feature flags, sensitivity, report interval, batch interval, config]
    rotation_vector_feature = [
        0xFD, 0x05, 0x00,
        0x00, 0x00,
        0x80, 0x84, 0x1E, 0x00,  # Report Interval = 100,000 µs
        0x00, 0x00, 0x00, 0x00,  # Batch Interval
        0x00, 0x00, 0x00, 0x00   # Config
    ]
    # Send Set Feature command
    bus.write_i2c_block_data(BNO085_ADDR, 0, rotation_vector_feature)

    # Define accelerometer feature
    accel_feature = [
        0xFD, 0x01, 0x00,
        0x00, 0x00,
        0x80, 0x84, 0x1E, 0x00,  # Report Interval = 100,000 µs
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
    bus.write_i2c_block_data(BNO085_ADDR, 0, accel_feature)

    print("Features enabled")

# Main loop
if __name__ == "__main__":
    enable_features()
    time.sleep(1)

    while True:
        read_sensor_data()
        time.sleep(0.05)
