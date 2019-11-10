"""Data and related functions for the avionics system."""

from json import dumps, loads
from datetime import datetime
from math import log, e
from sys import exit as completely_exit


class DataStruct:
    """Data manipulation for telemetry/decision making."""

    def __init__(self, file_name, config):
        self.conf = config
        
        self.last_state = "IDLE"
        
        if self.conf.SIM:
            data_file = open(self.conf.SIM_FILE, "r")
            lines = data_file.readlines()
            self.sim_data = [loads(line) for line in lines]
            self.sim_data_current = self.sim_data[0]
            self.sim_data = self.sim_data[1:]
            self.sim_zero_alt = self.sim_data_current["sensors"]["alt"]
            data_file.close()
        else:
            # Only import modules if not a simulation
            from modules.low_level import gps, imu, alt
            self.imu = imu.IMU()
            self.altimeter = alt.Alt()
            self.gps = gps.GPS()
        
        self.last_pressure = 0
        self.dp = [0]
        
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
        if self.conf.SIM:
            self.read_sensors_test()
            return None
        
        self.time = datetime.now()
        self.add_dp(self.altimeter.get_pressure() - self.last_pressure)
        self.last_pressure = self.altimeter.get_pressure()
        return None

    def read_sensors_test(self):
        """Update with fake data from config."""
        if len(self.sim_data) > 0:
            data = self.sim_data[0]  # Return first entry
            data["sensors"]["alt"] -= self.sim_zero_alt
            self.add_dp(data["sensors"]["pres"] - self.last_pressure)
            self.last_pressure = data["sensors"]["pres"]
            self.sim_data = self.sim_data[1:]  # Remove first entry
            self.sim_data_current = data
            return data
        else:
            self.finish_sim()
            return None

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
            return dumps(self.to_dict(state), indent=None)
        elif part == 1:
            datajson = self.to_dict(state)
            for data in list(datajson["sensors"].keys()):
                if data not in ["alt", "pres", "pitch", "yaw", "roll"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)
        elif part == 2:
            datajson = self.to_dict(state)
            for data in datajson["sensors"]:
                if data not in ["gyro", "mag", "compass", "acc"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)
        elif part == 3:
            datajson = self.to_dict(state)
            for data in datajson["sensors"]:
                if data not in ["lat", "lon", "gps_alt"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)
        else:  # part == 4
            datajson = self.to_dict(state)
            for data in datajson["sensors"]:
                if data not in ["hum", "temp"]:
                    datajson["sensors"].pop(data)
            return dumps(datajson, indent=None)

    def to_dict(self,state):
        """Return dict of data."""
        self.last_state = state
        
        if self.conf.SIM:
            return self.sim_data_current
        
        datajson = {
            "state": state,
            "time": str(self.time),
            "sensors": {
                "alt": self.altimeter.get_altitude(),  # meters
                "pres": self.altimeter.get_pressure(),  # millibars
                "hum": self.altimeter.get_humidity(),  # %
                "temp": (self.altimeter.get_temperature() * 9 / 5) + 32.0,  # F
                "lat": self.gps.get_lat(),  # latitude
                "lon": self.gps.get_lon(),  # longitude
                "gps_alt": self.gps.get_alt(), # meters above sea level
                "pitch": self.imu.get_accelerometer()["pitch"],  # degrees
                "roll": self.imu.get_accelerometer()["roll"],  # degrees
                "yaw": self.imu.get_accelerometer()["yaw"],  # degrees
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
        if self.conf.SIM:
            self.sim_zero_alt = self.sim_data_current["sensors"]["alt"]
        else:
            self.altimeter.set_zero_pressure()
        return None

    def get_accelerometer_up(self):
        """Return upward acceleration. [Default=+z]."""
        if self.conf.SIM:
            acc = 0
            if "x" in self.conf.up:
                acc = self.sim_data[0]["sensors"]["acc"]["x"]
            elif "y" in self.conf.up:
                acc = self.sim_data[0]["sensors"]["acc"]["y"]
            else:
                acc = self.sim_data[0]["sensors"]["acc"]["z"]
            if "-" in self.conf.up:
                return -acc
        else:
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

    def add_dp(self, dp, max_count=5):
        self.dp.append(dp)
        if len(self.dp) > max_count:
            self.dp = self.dp[1:]
        return None

    def check_dp_gt_val(self, val, count=4):
        """Check if dp greater than val for a count."""
        for dp in self.dp:
            if dp > val:
                count -= 1

        if count <= 0:
            return True
        else:
            return False
    
    def finish_sim(self):
        """Exit condition for simulation."""
        print("Simulation Finished")
        completely_exit()
