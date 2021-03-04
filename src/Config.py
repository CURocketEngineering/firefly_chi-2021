"""Config for the rocket."""

from json import load

from plugins import plugins


class Config:
    def __init__(self, file_name, current_state):
        """Read initialization values into variables."""
        self.shutdown = False
        if isinstance(file_name, str):
            file_pointer = open(file_name, "r")
            conf_file = load(file_pointer)
            file_pointer.close()
        elif isinstance(file_name, dict):
            conf_file = file_name
        else:
            raise ValueError("Argument file_name is of an invalid type")

        # State
        self.state = current_state
        self.last_state = current_state

        # For use in debugging program
        self.DEBUG = conf_file.get("DEBUG", False)
        self.TEST = conf_file.get("test", False)
        self.SIM = conf_file.get("sim", False)
        self.SIM_FILE = conf_file.get("sim_file", "")

        self.SIM_TD = conf_file.get("sim_td", 0.1)

        # Seconds to push charge to e-match
        self.PARACHUTE_CHARGE_TIME = conf_file.get("parachute_charge_time", 0.5)

        # Seconds to wait after apogee before deploying parachute
        self.APOGEE_DELAY = conf_file.get("apogee_delay", 0)

        # Main parachute height in ft
        self.MAIN_ALTITUDE = conf_file.get("main_altitude", 1000)

        # Seconds to wait after reaching parachute
        # height before deploying parachute
        self.MAIN_DELAY = conf_file.get("main_delay", 0)

        # Up direction on rocket
        self.up = conf_file.get("up", "+z")

        # Communications
        self.COMM = conf_file.get("comm", True)
        self.REMOTE_XBEE_ID = conf_file.get("remote_xbee_id", "TEMP")

        # Threads should die if set to True
        self.should_exit = False

        # Plugin hooks
        self.plugins = self.setup_hooks(conf_file.get("plugins", {}))

        # This is a meme, but it doesn't 'really'
        # matter if true of false
        self.FIDI = conf_file.get("FIDI", False)

        # data object
        self.data = None

        # state object
        self.rocket_state = None

    def setup_hooks(self, hooks):
        '''
        Return the dictionary of hooks to plugin names as a 
        dictionary of hooks to plugin functions.
        '''
        assert isinstance(hooks, dict), "Hooks must be a dictionary"
        new_hooks = {}
        print("HOOKS",hooks)
        for hook in hooks:
            assert isinstance(hooks[hook], list), "Hooks must map to a list"
            new_hooks[hook] = []
            for plugin in hooks[hook]:
                if plugin in plugins:
                    new_hooks[hook].append(plugins[plugin])
        return new_hooks

    def add_data(self, data):
        """
        Add link to data object.
        """
        self.data = data

    def add_rocket_state(self, rs):
        """
        Add link to rocket state.
        """
        self.rocket_state = rs
