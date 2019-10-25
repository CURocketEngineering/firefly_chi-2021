"""Low level comm implementation."""

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import serial.tools.list_ports as prtlst
import sys


class Antenna:
    def __init__(self, port="", remote_address=""):
        if port is "":
            port = self.find_port()
        self.port = port

        if self.port != "" and remote_address != "":
            self.device = XBeeDevice(self.port, 9600)
            self.active = True
            try:
                self.device.open()
                add_64 = XBee64BitAddress.from_hex_string(remote_address)
                self.remote_device = RemoteXBeeDevice(self.device, add_64)
            except:
                self.active = False
        else:
            self.active = False
            self.device = None

    def find_port(self):
        ports = prtlst.comports()
        for port in ports:
            try:
                if "FTDI" in port.manufacturer:
                    return port.device
            except Exception:
                pass
        return ""

    def send(self, data):
        print(self.active, data)
        if self.active:
            #self.device.send_data(self.remote_device, data)
            self.device.send_data_broadcast(data)


if __name__ == "__main__":
    print("DEBUG XBEE")
    ant = Antenna(remote_address="C001BEE")
    for i in [1,10,100,1000,10000]:
        input("pause")
        ant.send(str([1]*i))
