"""Run the main avionics process.

Used for data collection, telemetry, and  parachutes.
"""

import argparse as arg

from modules.Avionics import Avionics

def parse_arguments() -> "arg.ArgumentParser.NameSpace":
    parser = arg.ArgumentParser(
        description="Argument parsing for extra features"
    )
    parser.add_argument(
        "--gui", "--curses", "-g", "-G",
        default=False, action="store_true"
    )
    parser.add_argument(
        "--sensehat", "--sense_hat", "-s", "-S",
        default=False, action="store_true"
    )
    arguments = parser.parse_args()
    return arguments


# Run avionics directly
if __name__ == "__main__":
    # Set up argument parsing
    arguments = parse_arguments()
    
    if arguments.gui:  # Use curses gui
        visualizer = Vis.Vis(Avionics())
        visualizer.menu()
    elif arguments.sensehat:  # Use sensehat interface
        s = SH_Interface.Interface()
        s.menu()
    else:  # Run on the command line
        system = Avionics()
        system.main_process()
