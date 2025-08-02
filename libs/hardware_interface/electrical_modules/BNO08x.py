import smbus2
import time

BUS_NUMBER = 1
BNO085_ADDRESS = 0x4B

def read_all_registers():
    with smbus2.SMBus(BUS_NUMBER) as bus:
        for reg in range(0x00, 0x100):  # 0x00 to 0xFF
            try:
                data = bus.read_byte_data(BNO085_ADDRESS, reg)
                print(f"Register 0x{reg:02X}: {data}")
            except Exception as e:
                print(f"Error reading register 0x{reg:02X}: {e}")

if __name__ == "__main__":
    while True:
        read_all_registers()
        time.sleep(1)
