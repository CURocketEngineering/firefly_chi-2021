"""
USBGPS.py
GPS low-level specific module, GPS BU-353S4.
"""

from serial import Serial
import serial.tools.list_ports as prtlst


class GPS:
    def __init__(self, port="", max_pass=8, verbose=False):
        self.verbose = verbose
        if port is "":
            self.port = self.find_port()
        else:
            self.port = port
            
        self.has_gps = True
        if self.port is "":
            self.ser = None
            self.has_gps = False
        else:
            self.ser = Serial(self.port, baudrate=4800)
        self.max_pass = 8
        self.lat = 0
        self.lon = 0
        self.alt = 0

    def find_port(self):
        ports = prtlst.comports()
        for port in ports:
            # Prolific is the manufactuerer for the BU-353S4
            try:
                if "Prolific" in port.manufacturer:
                    return "/dev/" + port.name
            except Exception:
                pass
        return ""

    def read(self):
        """If possible, reread gps from serial and update values."""
        # Don't parse if there is not a gps
        if not self.has_gps:
            return None

        try:
            self.ser.flush()
            i = 0
            while (i < self.max_pass):
                i += 1
                line = self.ser.readline().decode("utf-8")
                if "GPGGA" in line:
                    if self.verbose:
                        print(line)
                    self.process_gpgga(line)
                    return None
        except Exception:
            return None
                

    def process_gpgga(self, line):
        try:
            attributes = line.split(",")
            lat_att = attributes[2]
            lon_att = attributes[4]
            alt_att = attributes[9]

            cv = lat_att.find(".")
            self.lat = int(lat_att[:cv-2]) + (float(lat_att[cv-2:])/60)
            if "S" in attributes[3]:
                self.lat *= -1

            cv = lon_att.find(".")
            self.lon = int(lon_att[:cv-2]) + (float(lon_att[cv-2:])/60)
            if "W" in attributes[5]:
                self.lon *= -1

            self.alt = alt_att
        except Exception as e:
            if self.verbose:
                print(f"ERROR: {e}")
        return None

    def get_lat(self):
        """Lattitude."""
        return self.lat

    def get_lon(self):
        """Longitude."""
        return self.lon

    def get_alt(self):
        """Altitude according to GPS. Relative to earth."""
        return self.alt

    def __del__(self):
        try:
            if self.has_gps:
                self.ser.close()
        except Exception:
            pass

def USBGPS(conf, data):
    print("USBGPS Init")
    gps = GPS()
    while not conf.shutdown:
        gps.read()
        data.current_data["sensors"]["lat"] = gps.get_lat()
        data.current_data["sensors"]["lon"] = gps.get_lon()
        data.current_data["sensors"]["gps_alt"] = gps.get_alt()
        

# The following is used for debugging
if __name__ == "__main__":
    gps = GPS(verbose=True)
    while(True):
        gps.read()
        print(f"LAT: {gps.get_lat()}, LON: {gps.get_lon()}, ALT: {gps.get_alt()}")
