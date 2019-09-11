"""Data and related functions for the avionics system."""

from json import dumps
from datetime import datetime
from sense_hat import SenseHat
from math import log, e


class DataStruct:
    """Data manipulation for telemetry/decision making."""

    def __init__(self, file_name):
        self.last_state = "IDLE"
        self.sense = SenseHat()
        self.sense.clear()
        self.zero_pressure = self.sense.get_pressure()
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

    def read_sensors(self, conf):
        """Update data."""
        self.time = datetime.now()
        self.dp = self.sense.get_pressure() - self.last_pressure
        self.last_pressure = self.sense.get_pressure()

    def read_sensors_test(self,conf):
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
                "alt": self.get_altitude(),  # units meters
                "pres": self.sense.get_pressure(),  # millibars
                "hum": self.sense.get_humidity(),  # %
                "temp": (self.sense.get_temperature() * 9 / 5) + 32.0,  # F
                "gps": self.get_gps(),  # lat, lon
                "pitch": self.sense.get_accelerometer()["pitch"],  # degrees
                "roll": self.sense.get_accelerometer()["pitch"],  # degrees
                "yaw": self.sense.get_accelerometer()["pitch"],  # degrees
                "compass": self.sense.get_compass(),  # degrees
                "acc": self.sense.get_accelerometer_raw(),  # degrees
                "gyro": self.sense.get_gyroscope_raw(),  # rad/sec
                "mag": self.sense.get_compass_raw(),  # microteslas
            }
        }
        return datajson

    def get_altitude(self):
        """P = P0*e^(-Mgz/RT).

        Assumes obvious constants ie earth atmosphere avg molar mass.
        """
        try:
            M = 0.0289644 # molar mass of earth's air
            g = 9.81 # m / sec^2 acc
            R = 8.314462 # kg m^2 / s^2 K mol
            p0 = self.millibars_to_atmospheres(self.zero_pressure)
            p = self.millibars_to_atmospheres(self.sense.get_pressure())
            T = self.sense.get_temperature() + 273.15
            # z = ln(P/P0) * (-RT/Mg)
            return -log(p/p0) * R * T / (M * g)
        except:
            return 0

    def meters_to_ft(self,meters):
        """Convert meters to ft."""
        return meters * 3.28084

    def millibars_to_atmospheres(self,mb):
        """Convert millibars into atmospheres."""
        return mb*0.0009869233

    def get_gps(self):
        """Parse file for gps."""
        gps = ""
        return gps

    def write_out(self,state):
        self._file.write(self.to_json(state)+"\n")

    def process(self,state):
        return state

    def reset_zero_pressure(self):
        self.zero_pressure = self.sense.get_pressure()
        return None

    def get_accelerometer_up(self):
        """Return upward acceleration. Assumes +z is up."""
        return self.sense.get_accelerometer_raw().z
