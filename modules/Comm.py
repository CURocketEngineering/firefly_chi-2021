"""Perform communication related functions."""
from digi.xbee.devices import XBeeDevice

class Comm:
    def __init__(self):
        self.device = XBeeDevice("/dev/ttyUSB0", 9600) # TODO assumes USB0
        self.active = True
        try:
            self.device.open()
        except:
            self.active = False
        return None

    def read_comm(self, rocket_state):
        """Read communication for meta-state changes."""
        return rocket_state

    def send(self,data):
        """Broadcast data on network."""
        self.device.send_data_broadcast(data)
        return None
