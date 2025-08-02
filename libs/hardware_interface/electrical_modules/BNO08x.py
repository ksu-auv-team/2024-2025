import smbus2
import struct
import time
import math
import Jetson.GPIO as GPIO

# === CONFIGURATION ===
I2C_BUS = 1
BNO085_ADDR = 0x4B  # If ADDR pin is pulled HIGH
INT_GPIO = 17       # GPIO17 connected to INT pin on sensor

# === I2C SETUP ===
bus = smbus2.SMBus(I2C_BUS)

# === GPIO SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(INT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# === ENABLE SENSOR FEATURES ===
def enable_features():
    rotation_vector = [
        0xFD, 0x05, 0x00,
        0x00, 0x00,
        0x80, 0x84, 0x1E, 0x00,  # Report interval = 100ms
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
    bus.write_i2c_block_data(BNO085_ADDR, 0, rotation_vector)

    accelerometer = [
        0xFD, 0x01, 0x00,
        0x00, 0x00,
        0x80, 0x84, 0x1E, 0x00,  # Report interval = 100ms
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
    bus.write_i2c_block_data(BNO085_ADDR, 0, accelerometer)

    print("Features enabled.")
    time.sleep(1)

# === READ SENSOR DATA ===
def read_sensor_data():
    try:
        # Read the 4-byte SHTP header
        header = bus.read_i2c_block_data(BNO085_ADDR, 0, 4)
        length = header[0] | (header[1] << 8)

        if length < 4 or length > 128:
            return

        # Read entire packet
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
        print(f"I2C Read Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# === MAIN LOOP ===
if __name__ == "__main__":
    try:
        print("Initializing BNO08x...")
        enable_features()
        print("Listening for interrupts on GPIO17...")

        while True:
            GPIO.wait_for_edge(INT_GPIO, GPIO.FALLING)
            read_sensor_data()

    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        GPIO.cleanup()
        bus.close()
