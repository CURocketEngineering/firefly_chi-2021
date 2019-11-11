"""Used to run avionics from sensehat."""

from sense_hat import SenseHat
import avionics

class Interface:
    def __init__(self, avionics_system):
        self.avionics_system = avionics_system

if __name__ == "__main__":
    input("DEBUG: Press <ENTER> to continue.")

