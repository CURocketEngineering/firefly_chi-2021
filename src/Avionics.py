'''Run the main avionics process.

Used for data collection, telemetry, and  parachutes.
'''

from . import Comm
from . import Data
from . import Actions
from . import Config
from . import Vis
from . import SH_Interface

from time import sleep


class Avionics():
    '''Major avionics process.'''

    def __init__(self):
        self.shutdown = False

        # Initialization
        self.rocket_state = "IDLE"  # State of rocket
        self.file_name = "output.json"  # Name for recording json
        self.conf = Config.Config( # Configuration data
            "config/config.json"
        )  
        self.data = Data.Data( # Avionics data
            self.file_name,
            self.conf
        )  
        self.comm = Comm.Comm(self.conf)  # Communication channel

    def main_process(self):
        '''
        Main processing loop.
        '''
        while (not self.shutdown) or (self.conf.FIDI):
            self.data.read_sensors()  # Update sensors
    
            if self.conf.DEBUG:
                print(f"STATE: {self.rocket_state}")
                print(self.data)

            if self.conf.SIM:
                if self.rocket_state == "IDLE":
                    self.rocket_state = "ARM"
                if self.data.last_state != self.rocket_state:
                    input(f"STATE CHANGE: {self.rocket_state}")
                if self.rocket_state in ["APOGEE"]:
                    input("PAUSE BUFFER")

                #sleep(self.conf.SIM_TD)

            # Update state by processessing data
            self.rocket_state = self.data.process(self.rocket_state)

            # Update state from comm
            self.rocket_state = self.comm.read_comm(self.rocket_state)
            
            # Send data
            if self.conf.COMM:
                self.comm.send(
                    self.data.to_json(self.rocket_state, part=0),
                    as_json=True,
                    skip_time=2.5
                )

            # Write data
            self.data.write_out(self.rocket_state)  

            # Make Decisions
            new_state = Actions.actions[self.rocket_state](
                self.data,
                self.conf
            )
            if new_state is not None:
                self.rocket_state = new_state

