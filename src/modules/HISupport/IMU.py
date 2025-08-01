import smbus2

class IMU:
    def __init__(self, bus_number=1, address=0x68):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address

    def read_gyro(self):
        # Read gyroscope data from the IMU
        gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
        return gyro_data

    def read_accel(self):
        # Read accelerometer data from the IMU
        accel_data = self.bus.read_i2c_block_data(self.address, 0x3B, 6)
        return accel_data
    
if __name__ == "__main__":
    imu = IMU()
    gyro = imu.read_gyro()
    accel = imu.read_accel()
    print("Gyroscope Data:", gyro)
    print("Accelerometer Data:", accel)
    imu.bus.close()