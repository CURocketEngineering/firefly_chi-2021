# Config.py
from json import load
import sys


class Config:
    def __init__(self, file_pointer):
        """Read initialization values into variables."""
        conf_file = load(file_pointer)

        # For use in debugging program
        self.DEBUG = conf_file.get("DEBUG", False)
        self.Test = conf_file.get("test", False)

        # Seconds to push charge to e-match
        self.PARACHUTE_CHARGE_TIME = conf_file.get("parachute_charge_time", 0.5)

        # Seconds to wait after apogee before deploying parachute
        self.APOGEE_DELAY = conf_file.get("apogee_delay", 0)

        # Main parachute height in ft
        self.MAIN_ALTITUDE = conf_file.get("main_altitude", 1000)

        # Seconds to wait after reaching parachute height before deploying parachute
        self.MAIN_DELAY = conf_file.get("main_delay", 0)

        self.flip_h = conf_file.get("flip_h", False)
        self.flip_v = conf_file.get("flip_v", False)
