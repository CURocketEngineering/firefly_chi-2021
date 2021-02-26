'''
Avionics.py

Run the main avionics process.
'''

from . import Config
from . import Data
from . import State

from . import SH_Interface
from . import Vis

from time import sleep

OUTPUT_FILE = "output.json"


class Avionics():
    '''Major avionics process.'''

    def __init__(self):
        # Initialization
        self.file_name = OUTPUT_FILE
        self.conf = Config.Config( # Configuration data
            "config/config.json", "IDLE"
        )
        self.data = Data.Data( # Avionics data
            self.file_name,
            self.conf
        )
        self.rocket_state = State.State(
            self.conf,
            self.data,
            hooks=self.conf.plugins
        )
        self.conf.add_data(self.data)

    def main_process(self):
        '''
        Main processing loop.
        '''
        while (not self.conf.shutdown) or (self.conf.FIDI):
            if self.conf.DEBUG:
                print(f"STATE: {self.rocket_state}")
                print(self.data)

            if self.conf.SIM:
                if self.conf.state == "IDLE":
                    self.conf.state = "ARM"
                    self.rocket_state.activate_hook("arm_start")
                if self.conf.last_state != self.conf.state:
                    print(f"STATE CHANGE: {self.conf.state}")
                    sleep(1)
                if self.conf.state in ["APOGEE"]:
                    print("PAUSE BUFFER")
                    sleep(1)

            # Make Decisions
            self.rocket_state.act()
