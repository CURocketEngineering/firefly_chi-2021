"""GPS low-level specific module."""
from serial import serial

class GPS:
    def __init__(self, port="/dev/ttyUSB0", max_pass=8):
        self.port = port
        self.ser = serial(port)
        self.max_pass = 8
        self.lat = 0
        self.lon = 0

    def read():
        """If possible, reread gps from serial and update values."""
        l = ""
        reevaluate = False
        i = 0
        while (i < self.max_pass):
            l += 1
            l = ser.readline()
            if "GPGGA" in l:
                reevaluate = True
                break
        if reevaluate:
            p = l.split(",")
            
    def get_lat():
        """Lattitude."""
        return ""

    def get_lon():
        """Longitude."""
        return ""
