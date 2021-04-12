#!/usr/bin/env python3
'''
Run the main avionics process using `config/config.yaml`.
'''

from src.Avionics import Avionics


# Run avionics directly
if __name__ == "__main__":
    # Set up argument parsing
    system = Avionics()
    system.main_process()
