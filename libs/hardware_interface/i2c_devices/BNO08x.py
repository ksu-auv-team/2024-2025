import smbus2
import Jetson.GPIO as GPIO
import time
import struct
from smbus2 import i2c_msg

# === CONFIG ===
I2C_BUS = 1
I2C_ADDR = 0x4B
INT_PIN = 17  # H_INTN interrupt GPIO

# === SHTP CONSTANTS ===
SHTP_HEADER_LEN = 4
sequence_numbers = [0] * 6  # one per channel

CHANNEL_CONTROL = 2
CHANNEL_INPUT_REPORT = 3

# === REPORT IDS ===
CHANNEL_NAMES = {
    0: "Command", 1: "Executable", 2: "Control",
    3: "Input Report", 4: "Wake Report", 5: "Gyro Rotation"
}
KNOWN_REPORT_IDS = {
    0xF9: "Product ID Response",
    0xFA: "Initialization Response",
    0xFB: "Error Report",
    0xFC: "Base Timestamp",
    0xFD: "Set Feature Command",
    0xFE: "Get Feature Response",
    0x05: "Rotation Vector",
    0x01: "Accelerometer",
    0x02: "Gyroscope"
}

# === INIT I2C AND GPIO ===
bus = smbus2.SMBus(I2C_BUS)
GPIO.setmode(GPIO.BCM)
GPIO.setup(INT_PIN, GPIO.IN)

def wait_for_H_INTN(timeout=3.0):
    start = time.time()
    while GPIO.input(INT_PIN) == GPIO.HIGH:
        if time.time() - start > timeout:
            return False
        time.sleep(0.1)
    return True

def read_shtp_packet():
    try:
        header = bus.read_i2c_block_data(I2C_ADDR, 0, 4)
        length = header[0] | (header[1] << 8)
        channel = header[2]
        sequence = header[3]
        payload_length = length - 4
        payload = bus.read_i2c_block_data(I2C_ADDR, 0, payload_length) if payload_length > 0 else []
        return {
            "length": length,
            "channel": channel,
            "sequence": sequence,
            "payload": payload
        }
    except Exception as e:
        print(f"❌ Error reading SHTP packet: {e}")
        return None

def parse_packet(packet):
    report_id = packet["payload"][0] if packet["payload"] else None
    report_name = KNOWN_REPORT_IDS.get(report_id, "Unknown Report")
    channel_name = CHANNEL_NAMES.get(packet["channel"], f"Unknown({packet['channel']})")
    print(f"📦 SHTP Packet")
    print(f"  ├─ Channel:  {packet['channel']} ({channel_name})")
    print(f"  ├─ Sequence: {packet['sequence']}")
    print(f"  ├─ Length:   {packet['length']} bytes")
    print(f"  ├─ Report:   0x{report_id:02X} ({report_name})")
    print(f"  └─ Payload:  {packet['payload']}")

def send_set_feature(feature_id, interval_us=10000):
    print(f"🛰️ Enabling feature: 0x{feature_id:02X}")
    payload = [
        0xFD,               # Set Feature command
        feature_id,         # Feature Report ID
        0x00,               # Feature flags
        0x00, 0x00,         # Change sensitivity
        *interval_us.to_bytes(4, 'little'),  # Report interval
        0x00, 0x00, 0x00, 0x00,              # Batch interval
        0x00, 0x00, 0x00, 0x00               # Sensor-specific config
    ]
    send_shtp_packet(CHANNEL_CONTROL, payload)

def send_shtp_packet(channel, payload):
    global sequence_numbers
    length = len(payload) + 4
    header = [length & 0xFF, (length >> 8) & 0xFF, channel, sequence_numbers[channel]]
    sequence_numbers[channel] = (sequence_numbers[channel] + 1) % 256
    packet = header + payload
    try:
        msg = i2c_msg.write(I2C_ADDR, packet)
        bus.i2c_rdwr(msg)
        print(f"📤 Sent packet on channel {channel} with payload: {payload}")
    except Exception as e:
        print(f"❌ Failed to send packet: {e}")

def wait_for_initialization():
    got_product_id = False
    got_init_response = False
    print("🕒 Waiting for Product ID + Init Response packets...")
    while not (got_product_id and got_init_response):
        if wait_for_H_INTN(timeout=3.0):
            pkt = read_shtp_packet()
            if pkt:
                parse_packet(pkt)
                rid = pkt["payload"][0] if pkt["payload"] else None
                if rid == 0xF9:
                    got_product_id = True
                elif rid == 0xFA:
                    got_init_response = True
        else:
            print("⚠️  Timeout waiting for H_INTN during boot")

def main():
    print("🟢 SHTP Initialization + Feature Enable started")
    try:
        wait_for_initialization()

        # Enable sensors
        send_set_feature(0x05)  # Rotation Vector
        send_set_feature(0x01)  # Accelerometer
        send_set_feature(0x02)  # Gyroscope

        print("📡 Initialization complete. Polling reports...")
        while True:
            if GPIO.input(INT_PIN) == GPIO.LOW:
                pkt = read_shtp_packet()
                if pkt:
                    parse_packet(pkt)
            else:
                time.sleep(0.01)
            time.sleep(0.1)  # Polling delay
    except KeyboardInterrupt:
        print("🛑 Interrupted by user")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
