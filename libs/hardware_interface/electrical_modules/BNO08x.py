import smbus2
import struct
import time
import math
import Jetson.GPIO as GPIO  # Jetson-compatible GPIO library

# === CONFIGURATION ===
I2C_BUS = 1
BNO085_ADDR = 0x4B
WAKE_GPIO = 17  # GPIO17 -> BNO08x PS0/WAKE

# === I2C SETUP ===
bus = smbus2.SMBus(I2C_BUS)

# === GPIO SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(WAKE_GPIO, GPIO.OUT, initial=GPIO.HIGH)  # Start HIGH (idle)

# === MATH UTIL ===
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

# === WAKE-UP PULSE ===
def wake_bno08x():
    print("Sending WAKE pulse to BNO08x...")
    GPIO.output(WAKE_GPIO, GPIO.LOW)
    time.sleep(0.01)  # At least 5–10 ms LOW
    GPIO.output(WAKE_GPIO, GPIO.HIGH)
    print("WAKE complete.")

# === ENABLE FEATURES ===
def enable_features():
    rotation_feature = [
        0xFD, 0x05, 0x00,
        0x00, 0x00,
        0x80, 0x84, 0x1E, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
    bus.write_i2c_block_data(BNO085_ADDR, 0, rotation_feature)

    accel_feature = [
        0xFD, 0x01, 0x00,
        0x00, 0x00,
        0x80, 0x84, 0x1E, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
    bus.write_i2c_block_data(BNO085_ADDR, 0, accel_feature)

    print("Features enabled")
    time.sleep(1)

# === READ DATA ===
def read_sensor_data():
    try:
        header = bus.read_i2c_block_data(BNO085_ADDR, 0, 4)
        packet_length = header[0] | (header[1] << 8)

        if packet_length < 4 or packet_length > 128:
            return

        packet = bus.read_i2c_block_data(BNO085_ADDR, 0, packet_length)
        report_id = packet[4]

        if report_id == 0x05:  # Rotation Vector
            q_i = struct.unpack_from("<hhhh", bytearray(packet), offset=5)
            real = [val / (1 << 14) for val in q_i]
            roll, pitch, yaw = quaternion_to_euler(*real)
            print(f"Yaw: {yaw:.2f}°, Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")

        elif report_id == 0x01:  # Accelerometer
            accel_raw = struct.unpack_from("<hhh", bytearray(packet), offset=5)
            accel = [val / 100.0 for val in accel_raw]
            print(f"Accel X: {accel[0]:.2f}, Y: {accel[1]:.2f}, Z: {accel[2]:.2f}")

    except OSError as e:
        print(f"I2C Read Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# === MAIN LOOP ===
if __name__ == "__main__":
    try:
        wake_bno08x()
        enable_features()

        print("Polling sensor data...")
        while True:
            wake_bno08x()            # Optional: wake before each poll
            read_sensor_data()
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        GPIO.cleanup()
