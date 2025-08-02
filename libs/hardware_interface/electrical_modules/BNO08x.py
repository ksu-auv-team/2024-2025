import smbus2
import struct
import time
import math

# === CONFIGURATION ===
I2C_BUS = 1
BNO085_ADDR = 0x4B  # Use 0x4A if ADDR pin is LOW

# === I2C SETUP ===
bus = smbus2.SMBus(I2C_BUS)

# === UTIL: Quaternion → Euler ===
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

    return (
        math.degrees(roll),
        math.degrees(pitch),
        math.degrees(yaw)
    )

# === ENABLE SENSOR FEATURES ===
def enable_feature(report_id, interval_us=100_000):
    interval = list(interval_us.to_bytes(4, 'little'))
    feature_packet = [
        0xFD, report_id, 0x00,      # Command: Set Feature
        0x00, 0x00,                 # Reserved
        *interval,                 # Report Interval
        0x00, 0x00, 0x00, 0x00,     # Latency
        0x00, 0x00, 0x00, 0x00      # Duration
    ]
    bus.write_i2c_block_data(BNO085_ADDR, 0, feature_packet)

def initialize_sensor():
    print("Enabling Rotation Vector...")
    enable_feature(0x05)  # Rotation Vector
    time.sleep(0.1)
    print("Enabling Accelerometer...")
    enable_feature(0x01)  # Accelerometer
    time.sleep(0.5)
    print("Features enabled.")

# === READ SENSOR DATA ===
def read_sensor():
    try:
        header = bus.read_i2c_block_data(BNO085_ADDR, 0, 4)
        length = header[0] | (header[1] << 8)
        if length < 4 or length > 128:
            return

        packet = bus.read_i2c_block_data(BNO085_ADDR, 0, length)
        report_id = packet[4]

        if report_id == 0x05:  # Rotation Vector
            q = struct.unpack_from("<hhhh", bytearray(packet), offset=5)
            quat = [val / (1 << 14) for val in q]
            roll, pitch, yaw = quaternion_to_euler(*quat)
            print(f"[Rotation] Yaw: {yaw:.2f}°, Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")

        elif report_id == 0x01:  # Accelerometer
            accel = struct.unpack_from("<hhh", bytearray(packet), offset=5)
            accel = [val / 100.0 for val in accel]
            print(f"[Accel] X: {accel[0]:.2f}, Y: {accel[1]:.2f}, Z: {accel[2]:.2f}")

    except OSError as e:
        if e.errno == 121:
            print("No data ready.")
        else:
            print(f"I2C Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# === MAIN LOOP ===
if __name__ == "__main__":
    try:
        print("Initializing BNO08x...")
        initialize_sensor()

        print("Polling sensor...")
        while True:
            read_sensor()
            time.sleep(0.05)  # 20 Hz polling

    except KeyboardInterrupt:
        print("Stopped by user.")

    finally:
        bus.close()
