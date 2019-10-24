"""Perform communication related functions."""
from modules.low_level import low_comm

class Comm:
    def __init__(self):
        self.antenna = low_comm.Antenna()

    def read_comm(self, rocket_state):
        """Read communication for meta-state changes."""
        return rocket_state

    def send(self,data):
        """Broadcast data on network."""
        # TODO change from broadcast to send_data()?
        self.antenna.send(data)
        return None
