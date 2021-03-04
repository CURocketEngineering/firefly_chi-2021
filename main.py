#!/bin/python
'''
Run the main avionics process using config/config.json.
'''

from src.Avionics import Avionics


# Run avionics directly
if __name__ == "__main__":
    # Set up argument parsing
    system = Avionics()
    system.main_process()
