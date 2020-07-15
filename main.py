#!/bin/python
'''
Run the main avionics process.

Used for data collection, telemetry, and  parachutes.
'''

import argparse as arg
import threading

from src.Avionics import Avionics
from src.common import parse_arguments


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
