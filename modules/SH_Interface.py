"""Used to run avionics from sensehat."""

#from sense_hat import SenseHat
from . import Avionics

class Interface:
    def __init__(self, avionics_system):
        self.avionics_system = avionics_system

if __name__ == "__main__":
    input("DEBUG: Press <ENTER> to continue.")

