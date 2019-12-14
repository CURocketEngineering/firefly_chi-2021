"""Low level comm implementation."""

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import serial.tools.list_ports as prtlst
import sys
from time import time as unixtimestamp
from json import loads, dumps


class Antenna:
    def __init__(self, port="", remote_address="", verbose=False):
        self.verbose = verbose
        if port is "":
            port = self.find_port()
        self.port = port

        self.last_time_sent = 0

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

    def send(self, data, time=None, data_key=None, skip_time=0,
             parent="", as_json=False):
        if as_json:
            data = loads(data)
        # Update Time
        if time == None:
            time = unixtimestamp()
            #self.last_time_sent = time
            # Skip if time buffer too low
            if skip_time != 0:
                if time - self.last_time_sent < skip_time:
                    return None
            self.last_time_sent = time

        print("SENDING")
        self.verbose_print((self.active, data))
        if self.active:
            try:
                if type(data) == dict:
                    for key in data:
                        parent = "" if data_key == None else data_key
                        self.send(
                            data[key], time=time,
                            data_key=key, parent=parent
                        )
                else:
                    send_data = {
                        "uts" : time,
                        f"{parent}_{str(data_key)}" : data
                    }
                    to_send = dumps(send_data).encode()
                    self.verbose_print(to_send)
                    self.device.send_data_async(
                        self.remote_device,
                        to_send
                    )
            except Exception as e:
                self.verbose_print(f"COULDN'T SEND {data}, ERROR {e}")
        return None

    def verbose_print(self, message):
        if self.verbose:
            print(message)

    def read_time(self, time):
        return self.device.read_data(time)

if __name__ == "__main__":
    import json
    print("DEBUG XBEE")
    mode = input("[S]end or [R]ecieve? ")
    data = {
        "sensors": {
            "gyro": {
                "x": -5.376751,
                "y": 2.096962,
                "z": -0.705878},
            "acc": {
                "x": -1.020873,
                "y": -0.033887,
                "z": -0.028862
            },
            "mag": {
                "x": -0.082264,
                "y": 0.071932,
                "z": 0.040348
            },
            "lat": 0,
            "lon": 0,
            "pitch": 1.527222,
            "yaw": -0.960689,
            "roll": -2.276288,
            "alt": 1398.361,
            "pres": 86101.02,
            "hum": 12.02832,
            "temp": 42.3
        },
        "time": 1250310
    }
    if "r" in mode.lower():
        ant = Antenna(verbose=True, remote_address="who cares")
        f = open("tmp_data.json", "a")
        cur_data = {}
        cur_time = 0
        key_name = ""
        val = ""
        uts = 0
        while True:
            data = json.loads(ant.read_time(1000).data.decode())
            for key in data:
                if "uts" in key:
                    uts = data[key]
                else:
                    key_name = key
                    val = data[key]
            if uts != cur_time:
                f.write(dumps(data))
                data = {
                    "uts": uts,
                    key: val
                }
            else:
                data[key] = val
            
        
    else:
        ant = Antenna(remote_address="0013A20041A061E8", verbose=True)
        ant.send(data, skip_time=2.5)
