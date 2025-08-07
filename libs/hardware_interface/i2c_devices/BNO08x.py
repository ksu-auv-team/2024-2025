import smbus2
import Jetson.GPIO as GPIO
import time

# === CONFIGURATION ===
I2C_BUS = 1
I2C_ADDRESS = 0x4B
H_INTN_GPIO = 17

# === INIT GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(H_INTN_GPIO, GPIO.IN)

# === INIT I2C ===
bus = smbus2.SMBus(I2C_BUS)

def wait_for_interrupt(timeout=5.0):
    start = time.time()
    while GPIO.input(H_INTN_GPIO) == GPIO.HIGH:
        if time.time() - start > timeout:
            return False
        time.sleep(0.001)
    return True

def read_packet():
    try:
        header = bus.read_i2c_block_data(I2C_ADDRESS, 0, 4)
        length = header[0] | (header[1] << 8)
        channel = header[2]
        seq = header[3]
        payload_len = length - 4

        if payload_len > 0:
            payload = bus.read_i2c_block_data(I2C_ADDRESS, 0, payload_len)
        else:
            payload = []

        return {
            "length": length,
            "channel": channel,
            "seq": seq,
            "payload": payload
        }
    except Exception as e:
        print(f"❌ Error reading packet: {e}")
        return None

def main():
    print("🔎 Listening for BNO08x packets (press Ctrl+C to stop)...")
    try:
        while True:
            if wait_for_interrupt(timeout=2.0):
                packet = read_packet()
                if packet:
                    print(f"📦 Channel {packet['channel']} | Seq {packet['seq']} | Len {packet['length']} | Payload: {packet['payload']}")
            else:
                print("⚠️  No interrupt (H_INTN still high)")
    except KeyboardInterrupt:
        print("🛑 Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
