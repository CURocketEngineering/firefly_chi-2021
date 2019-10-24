"""Perform communication related functions."""
from modules.low_level import low_comm

class Comm:
    def __init__(self, conf):
        self.conf = conf
        if conf.SIM:
            pass
        else:
            self.antenna = low_comm.Antenna()

    def read_comm(self, rocket_state):
        """Read communication for meta-state changes."""
        return rocket_state

    def send(self, data):
        """Broadcast data on network."""
        if self.conf.SIM:
            return None
        else:
            self.antenna.send(data)
        return None
