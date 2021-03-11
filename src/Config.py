"""
Config.py
=========
Config for the rocket.
"""

from json import load as jload
from yaml import load as yload
from yaml import Loader as yLoader


from plugins import plugins


class Config:
    def __init__(self, file_name="config/config.yaml", current_state="HALT"):
        """Read initialization values into variables."""
        self.shutdown = False
        self.rocket_state = None
        self.data = None

        conf_file = {}
        stream = open(file_name, "r")
        if file_name.endswith(".json") or file_name.endswith(".jsn"):
            conf_file = jload(stream)
        else:
            # Default is yaml
            conf_file = yload(stream, Loader=yLoader)
        stream.close()

        # State
        self.state = current_state
        self.last_state = current_state

        # For use in debugging program
        self.DEBUG = conf_file.get("DEBUG", False)
        self.SIM_FILE = conf_file.get("sim_file", "")
        self.SIM_TD = conf_file.get("sim_td", 0.1)

        # Seconds to push charge to e-match
        self.PARACHUTE_CHARGE_TIME = conf_file.get("parachute_charge_time", 2)

        # Seconds to wait after apogee before deploying parachute
        self.APOGEE_DELAY = conf_file.get("apogee_delay", 0.0)

        # Seconds to wait after reaching parachute
        # height before deploying parachute
        self.MAIN_DELAY = conf_file.get("main_delay", 0)

        # Main parachute height in ft
        self.MAIN_ALTITUDE = conf_file.get("main_altitude", 1000)

        # Communications
        self.REMOTE_XBEE_ID = conf_file.get("remote_xbee_id", "TEMP")

        # Threads should die if set to True
        self.should_exit = False

        # Plugin hooks
        self.plugins = self.setup_hooks(conf_file.get("plugins", {}))

        # This is a meme, but it doesn't 'really'
        # matter if true of false
        self.FIDI = conf_file.get("FIDI", False)


    def setup_hooks(self, hooks):
        """
        Return the dictionary of hooks to plugin names as a
        dictionary of hooks to plugin functions.
        """
        assert isinstance(hooks, dict), "Hooks must be a dictionary"
        new_hooks = {}
        for hook in hooks:
            assert isinstance(hooks[hook], list), "Hooks must map to a list"
            new_hooks[hook] = []
            for plugin in hooks[hook]:
                if plugin in plugins:
                    new_hooks[hook].append(plugins[plugin])
                else:
                    print(f"[Config.py]: hook {hook} is not available")
        return new_hooks
