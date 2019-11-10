"""Run the main avionics process.

Used for data collection, telemetry, and  parachutes.
"""

from modules import Comm
from modules import DataStruct
from modules import Actions
from modules import Config
from modules import Vis
import argparse as arg


class Avionics():
    """Major avionics process."""

    def __init__(self):
        self.shutdown = False

        # Initialization
        self.rocket_state = "IDLE"  # State of rocket
        self.file_name = "output.json"  # Name for recording json
        self.conf = Config.Config("config.json")  # Configuration data
        self.data = DataStruct.DataStruct(self.file_name, self.conf)  # Avionics data
        self.comm = Comm.Comm(self.conf)  # Communication channel

    def main_process(self):
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
    
            self.rocket_state = self.data.process(self.rocket_state) 
            self.rocket_state = self.comm.read_comm(self.rocket_state)  # Update state from comm

            self.comm.send(self.data.to_json(self.rocket_state, part=0))  # Send data
            self.data.write_out(self.rocket_state)  # Write data

            # Make Decisions
            new_state = Actions.actions[self.rocket_state](self.data, self.conf)
            if new_state is not None:
                self.rocket_state = new_state


# Run avionics directly
if __name__ == "__main__":
    # Set up argument parsing
    parser = arg.ArgumentParser(
        description="Argument parsing for extra features"
    )
    parser.add_argument("--gui", "--curses", "-g", "-G", default=False, action="store_true")
    arguments = parser.parse_args()

    if arguments.gui:  # Use curses gui
        visualizer = Vis.Vis(Avionics())
        visualizer.menu()
    else:  # Run on the command line
        system = Avionics()
        system.main_process()
