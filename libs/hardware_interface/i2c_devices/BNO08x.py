import smbus2
import Jetson.GPIO as GPIO
import time
import struct

# === CONFIG ===
I2C_BUS = 1
I2C_ADDR = 0x4B
INT_PIN = 17  # H_INTN interrupt GPIO

# === SHTP CONSTANTS ===
SHTP_HEADER_LEN = 4
CHANNEL_NAMES = {
    0: "Command",
    1: "Executable",
    2: "Control",
    3: "Input Report",
    4: "Wake Report",
    5: "Gyro Rotation"
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
    """ Wait until the interrupt line goes LOW """
    start = time.time()
    while GPIO.input(INT_PIN) == GPIO.HIGH:
        if time.time() - start > timeout:
            return False
        time.sleep(0.001)
    return True

def read_shtp_packet():
    """ Read and return a complete SHTP packet from BNO08x """
    try:
        header = bus.read_i2c_block_data(I2C_ADDR, 0, SHTP_HEADER_LEN)
        length = header[0] | (header[1] << 8)
        channel = header[2]
        sequence = header[3]
        payload_length = length - SHTP_HEADER_LEN

        if payload_length > 0:
            payload = bus.read_i2c_block_data(I2C_ADDR, 0, payload_length)
        else:
            payload = []

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
    """ Optional: Decode known report IDs and fields """
    report_id = packet["payload"][0] if packet["payload"] else None
    report_name = KNOWN_REPORT_IDS.get(report_id, "Unknown Report")
    channel_name = CHANNEL_NAMES.get(packet["channel"], f"Unknown({packet['channel']})")

    print(f"📦 SHTP Packet")
    print(f"  ├─ Channel:  {packet['channel']} ({channel_name})")
    print(f"  ├─ Sequence: {packet['sequence']}")
    print(f"  ├─ Length:   {packet['length']} bytes")
    print(f"  ├─ Report:   0x{report_id:02X} ({report_name})")
    print(f"  └─ Payload:  {packet['payload']}")

def main():
    print("🟢 SHTP reader started (press Ctrl+C to stop)")
    try:
        while True:
            if wait_for_H_INTN(timeout=3.0):
                pkt = read_shtp_packet()
                if pkt:
                    parse_packet(pkt)
            else:
                print("⚠️  H_INTN timeout — no new data")
    except KeyboardInterrupt:
        print("🛑 Interrupted by user")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
