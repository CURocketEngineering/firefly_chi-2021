"""Perform communication related functions."""
from modules.low_level import low_comm

class Comm:
    def __init__(self, conf):
        self.conf = conf
        self.antenna = low_comm.Antenna(remote_address=conf.REMOTE_XBEE_ID)

    def read_comm(self, rocket_state):
        """Read communication for meta-state changes."""
        return rocket_state

    def send(self, data):
        """Broadcast data on network."""
        if self.conf.SIM:
            return None
        self.antenna.send(data)
        return None
