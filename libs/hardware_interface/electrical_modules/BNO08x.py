import smbus2
import time

# I2C bus number (may be different for your Jetson)
# You might need to check your Jetson's documentation or use i2cdetect to find the correct bus number.
BUS_NUMBER = 1

# BNO085 I2C address (default is 0x4A, can be 0x4B if DI pin is pulled high)
#
BNO085_ADDRESS = 0x4B

# BNO085 register addresses (you'll need to consult the BNO085 datasheet for the specific registers you want to read)
# This example reads a dummy byte, you'll need to replace this with appropriate register addresses based on the desired data type.
DUMMY_REGISTER = 0x00

def read_bno085_data():
    with smbus2.SMBus(BUS_NUMBER) as bus:
        try:
            # Read a single byte from a register (replace with appropriate register and data length)
            data = bus.read_byte_data(BNO085_ADDRESS, DUMMY_REGISTER)
            print(f"Received data: {data}")
        except Exception as e:
            print(f"Error reading from BNO085: {e}")

if __name__ == "__main__":
    while True:
        read_bno085_data()
        time.sleep(1) # Read every 1 second