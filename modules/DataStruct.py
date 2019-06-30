"""Data and related functions for the avionics system."""

from json import dumps
from datetime import datetime
from sense_hat import SenseHat


class DataStruct:
    """Data manipulation for telemetry/decision making."""
    
    def __init__(self,file_name):
        self.last_state = "?"
        self.sense = SenseHat()
        self.sense.clear()
        self.time = datetime.now()
        self._file = open(file_name,"a")
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        self_str = ""
        data = self.to_dict(self.last_state)
        for item in data:
            self_str += f"[{item}:{data[item]}] "
        return self_str

    def read_sensors(self, conf):
        """Update data."""
        self.time = datetime.now()
          
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
                "alt": self.sense.get_pressure(), # units ? TODO
                "pres": self.sense.get_pressure(), # millibars
                "hum": self.sense.get_humidity(), # %
                "temp": (self.sense.get_temperature() * 9 / 5) + 32, # F
                "gps": self.get_gps(), # lat, lon
                "pitch": self.get_accelerometer()["pitch"], # degrees
                "roll": self.get_accelerometer()["pitch"], # degrees
                "yaw": self.get_accelerometer()["pitch"], # degrees
                "compass": self.get_compass(), # degrees
                "acc": self.get_accelerometer_raw(), # degrees
                "gyro": self.get_gyroscope_raw(), # rad/sec
                "mag": self.get_compass_raw(), # microteslas
            }
        }
        return datajson

    def get_gps(self):
        """Parse file for gps"""
        gps = ""
        return gps
    
    def write_out(self,state):
        self._file.write(self.to_json(state)+"\n")

    def process(self,state):
        return state
