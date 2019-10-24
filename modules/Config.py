"""Config for the rocket."""

from json import load


class Config:
    def __init__(self, file_name):
        """Read initialization values into variables."""
        file_pointer = open(file_name, "r")
        conf_file = load(file_pointer)

        # For use in debugging program
        self.DEBUG = conf_file.get("DEBUG", False)
        self.TEST = conf_file.get("test", False)
        self.SIM = conf_file.get("sim", False)
        self.SIM_FILE = conf_file.get("sim_file", "")

        # Seconds to push charge to e-match
        self.PARACHUTE_CHARGE_TIME = conf_file.get("parachute_charge_time", 0.5)

        # Seconds to wait after apogee before deploying parachute
        self.APOGEE_DELAY = conf_file.get("apogee_delay", 0)

        # Main parachute height in ft
        self.MAIN_ALTITUDE = conf_file.get("main_altitude", 1000)

        # Seconds to wait after reaching parachute height before deploying parachute
        self.MAIN_DELAY = conf_file.get("main_delay", 0)

        # Up direction on rocket
        self.up = conf_file.get("up", "+z")

        # Communications
        self.REMOTE_XBEE_ID = conf_file.get("remote_xbee_id", "")

        # This is a meme, but it doesn't 'really' matter if true of false
        self.FIDI = conf_file.get("FIDI", False)

        file_pointer.close()
