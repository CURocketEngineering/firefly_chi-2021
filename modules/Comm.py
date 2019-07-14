"""Perform communication related functions."""
from digi.xbee.devices import XBeeDevice
from sys import getsizeof

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
        # TODO change from broadcast to send_data()?
        print(len(data), getsizeof(data))
        for item in self.split_data(data):
            print(len(item), getsizeof(item))
            self.device.send_data_broadcast(item)
        return None

    def split_data(self,data):
        """Split data to be <= 100 bytes."""
        return self.split_in_half(data)

    def split_in_half(self,data):
        l = len(data) // 2
        return_list = []
        d1 = data[:l]
        d2 = data[l:]
        for d in [d1,d2]:
            if getsizeof(d) > 99:
                d = self.split_in_half(d)
                return_list += d
            else:
                return_list.append(d)
        return return_list
