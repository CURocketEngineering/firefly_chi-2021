'''
Avionics.py

Run the main avionics process.
'''

from . import Config
from . import Data
from . import State


from time import sleep


class Avionics():
    '''Major avionics process.'''

    def __init__(self):
        # Initialization
        self.conf = Config.Config()
        self.data = Data.Data(self.conf)
        self.conf.data = self.data
        self.rocket_state = State.State(
            self.conf,
            self.data,
            hooks=self.conf.plugins
        )
        self.conf.rocket_state = self.rocket_state

    def main_process(self):
        '''
        Main processing loop.
        '''
        while (not self.conf.shutdown) or (self.conf.FIDI):
            if self.conf.DEBUG:
                rdata = self.data.to_dict()
                print(f"{self.rocket_state}:  {rdata['sensors']['pres']}  {rdata['sensors']['alt']}\r", end="")
                if self.conf.last_state != self.conf.state:
                    print(f"\nSTATE CHANGE: {self.conf.state}")
                if self.conf.state in ["APOGEE", "EJECT"]:
                    rdata = self.data.to_dict()
                    print(f"\nEVENT: {rdata['sensors']['alt']}")

            # Make Decisions
            self.rocket_state.act()
