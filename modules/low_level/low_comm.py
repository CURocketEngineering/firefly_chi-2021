"""Low level comm implementation."""

from digi.xbee.devices import XBeeDevice

class Antenna:
    def __init__(self):
        self.device = XBeeDevice("/dev/ttyUSB0", 9600)
        self.active = True
        try:
            self.device.open()
        except:
            self.active = False
        finally:
            return None

    def send(self, data):
        return None
