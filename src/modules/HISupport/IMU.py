import smbus2

class IMU:
    def __init__(self, bus_number=1, address=0x68):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address

    def read_bus(self, register):
        try:
            data = self.bus.read_i2c_block_data(self.address, register, 6)
            return data
        except Exception as e:
            print(f"Error reading from bus: {e}")
            return None

if __name__ == "__main__":
    imu = IMU(0x4B)
    register = 0x4B  # Example register address for gyroscope data
    data = imu.read_bus(register)
    if data:
        print("Data read from IMU:", data)
    else:
        print("Failed to read data from IMU.")