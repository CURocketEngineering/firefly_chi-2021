"""Data and related functions for the avionics system."""

from json import dumps
from datetime import datetime
from sense_hat import SenseHat
from math import log, e
from low_level import gps, imu, alt


class DataStruct:
    """Data manipulation for telemetry/decision making."""

    def __init__(self, file_name, config):
        self.conf = config
        
        self.last_state = "IDLE"
        
        self.imu = imu.IMU()
        self.altimeter = alt.Alt()
        self.gps = gps.GPS()
        
        self.last_pressure = 0
        self.dp = 0
        
        self.time = datetime.now()
        self._file = open(file_name, "a")
        self._file.write("--- " + str(self.time)+"\n")

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        self_str = ""
        data = self.to_dict(self.last_state)
        return self.format_data(data)
    
    def format_data(self, dict, end="\n"):
        """Format data."""
        data_str = ""
        tab = "\t"
        for data in dict:
            data_val = dict[data]
            if type(data_val) == type(0.0):
                data_str += f"[{data}: {data_val:.2f}]" + end
            elif type(data_val) == type(0):
                data_str += f"[{data}: {data_val}]" + end
            elif type(data_val) == type({}):
                data_str += f"[{data}: {{ {self.format_data(data_val,end=(end+tab))} }}]" + end
            else:
                data_str += f"[{data}: {data_val}]" + end
        return data_str

    def read_sensors(self):
        """Update data."""
        if self.conf.sim:
            self.read_sensors_test()
            return None
        self.time = datetime.now()
        self.dp = self.altimeter.get_pressure() - self.last_pressure
        self.last_pressure = self.altimeter.get_pressure()
        return None

    def read_sensors_test(self):
        """Update with fake data from config."""
        return None

    def to_json(self,state):
        """Return string of data."""
        # indent=None has no newlines (for parsing/space), indent=4 looks pretty
        return dumps(self.to_dict(state),indent=None)

    def to_dict(self,state):
        """Return dict of data."""
        self.last_state = state
        datajson = {
            "state": state,
            "time": str(self.time),
            "sensors": {
                "alt": self.get_altitude(),  # meters
                "pres": self.altimeter.get_pressure(),  # millibars
                "hum": self.altimeter.get_humidity(),  # %
                "temp": (self.altimeter.get_temperature() * 9 / 5) + 32.0,  # F
                "lat": self.gps.get_lat(),  # latitude
                "lon": self.gps.get_lon(),  # longitude
                "pitch": self.imu.get_accelerometer()["pitch"],  # degrees
                "roll": self.imu.get_accelerometer()["pitch"],  # degrees
                "yaw": self.imu.get_accelerometer()["pitch"],  # degrees
                "compass": self.imu.get_compass(),  # degrees
                "acc": self.imu.get_accelerometer_raw(),  # degrees
                "gyro": self.imu.get_gyroscope_raw(),  # rad/sec
                "mag": self.imu.get_compass_raw(),  # microteslas
            }
        }
        return datajson

    def get_gps(self):
        """Parse file for gps."""
        gps = ""
        return gps

    def write_out(self, state):
        self._file.write(self.to_json(state)+"\n")

    def process(self, state):
        return state

    def reset_zero_pressure(self):
        self.altimeter.set_zero_pressure()
        return None

    def get_accelerometer_up(self):
        """Return upward acceleration. [Default=+z]."""
        acc = 0
        if "x" in self.conf.up:
            acc = self.imu.get_accelerometer_raw().x
        elif "y" in self.conf.up:
            acc = self.imu.get_accelerometer_raw().y
        else:
            acc = self.imu.get_accelerometer_raw().z
        if "-" in self.conf.up:
            return -acc
        return acc
