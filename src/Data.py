"""Data and related functions for the avionics system."""

from json import dumps, loads
from datetime import datetime
import time


class Data:
    """Data manipulation for telemetry/decision making."""

    def __init__(self, config):
        self.conf = config

        self.time = datetime.now()
        
        self.current_data = self.get_starting_data()

        self.last_pressure = 0
        self.dp = [0]
        self.ground_pressure = 0

    def format_data(self, data_dict, end="\n"):
        """Format data."""
        data_str = ""
        tab = "\t"
        for data in data_dict:
            data_val = data_dict[data]
            print(data_val)
            if isinstance(data_val, float):
                data_str += f"[{data}: {data_val:.2f}]" + end
            elif isinstance(data_val, int):
                data_str += f"[{data}: {data_val}]" + end
            elif isinstance(data_val, dict):
                data_str += f"[{data}: {{ {self.format_data(data_val,end=(end+tab))} }}]" + end
            else:
                data_str += f"[{data}: {data_val}]" + end
        return data_str

    def to_json(self, state, part=0):
        """Return string of data.

        part indicates the part of the data to convert.
        0 is all of the data. 
        1 is the main data.
        2 is raw imu. 
        3 is gps.
        4 is other barometric data.
        All parts contain state and time info.
        """
        # indent=None has no newlines (for parsing/space), indent=4 looks pretty
        if part == 0 or part not in [0, 1, 2, 3, 4]:
            return dumps(self.to_dict(), indent=None)
        elif part == 1:
            datajson = self.to_dict()
            for data in list(datajson["sensors"].keys()):
                if data not in ["alt", "pres", "pitch", "yaw", "roll"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)
        elif part == 2:
            datajson = self.to_dict()
            for data in datajson["sensors"]:
                if data not in ["gyro", "mag", "compass", "acc"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)
        elif part == 3:
            datajson = self.to_dict()
            for data in datajson["sensors"]:
                if data not in ["lat", "lon", "gps_alt"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)
        else:  # part == 4
            datajson = self.to_dict()
            for data in datajson["sensors"]:
                if data not in ["hum", "temp"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)

    def to_dict(self):
        """Return dict of data."""
        self.current_data["time"] = str(time.time())
        self.current_data["state"] = self.conf.state
        return self.current_data

    def get_starting_data(self):
        return {
            "state": self.conf.state,
            "time": str(self.time),
            "sensors": {
                "alt": 0,  # meters
                "pres": 0,  # millibars
                "dp": 0,  # millibars
                "hum": 0,  # %
                "temp": 0,  # F
                "lat": 0,  # latitude
                "lon": 0,  # longitude
                "gps_alt": 0, # meters above sea level
                "pitch": 0,  # degrees
                "roll": 0,  # degrees
                "yaw": 0,  # degrees
                "compass": 0,  # degrees
                "acc": {
                    "x": 0, "y": 0, "z": 0
                },  # Gs
                "gyro": {
                    "x": 0, "y": 0, "z": 0
                },  # rad/sec
                "mag": {
                    "x": 0, "y": 0, "z": 0
                },  # microteslas
            }
        }

    def add_dp(self, dp, max_count=10):
        self.dp.append(dp)
        if len(self.dp) > max_count:
            self.dp = self.dp[1:]
        return None

    def check_dp_gt_val(self, val, count=8):
        """Check if dp greater than val for a count."""
        for dp in self.dp:
            if dp > val:
                count -= 1

        if count <= 0:
            return True
        return False

    def check_dp_lt_val(self, val, count=8):
        """Check if dp greater than val for a count."""
        for dp in self.dp:
            if dp < val:
                count -= 1

        if count <= 0:
            return True
        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self_str = ""
        data = self.to_dict()
        return self.format_data(data)
