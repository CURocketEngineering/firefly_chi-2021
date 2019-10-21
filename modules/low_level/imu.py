"""imu.py """

from sense_hat import SenseHat

class IMU:
    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.zero_pressure = self.sense.get_pressure()

    def get_accelerometer():
        return self.sense.get_accelerometer()

    def get_compass():
        return self.sense.get_compass()

    def get_accerometer_raw():
        return self.sense.get_accelerometer_raw()

    def get_gyroscope_raw():
        return self.sense.get_gyroscope_raw()

    def get_compass_raw():
        return self.sense.get_compass_raw()
