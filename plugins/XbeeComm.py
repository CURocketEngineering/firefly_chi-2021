"""Perform communication related functions."""

from time import sleep


from plugins import USBRelay


can_use_comm = True
try:
    from .low_level import low_comm
except Exception as e:
    print("[XbeeComm]:", e)
    can_use_comm = False

SECRET_KEY = "CURE"
from json import loads
    
class Comm:
    def __init__(self, conf):
        self.conf = conf
        self.antenna = low_comm.Antenna(
            remote_address=conf.REMOTE_XBEE_ID
        )

    def read_comm(self, read_time=None):
        """
        Read communication for meta-state changes.
        """
        return self.antenna.read_time(read_time)

    def send(self, data, skip_time=0.25, as_json=False):
        """Async send data to specific XBee network."""
        return self.antenna.send(
            data,
            skip_time=skip_time,
            as_json=as_json
        )


def loop(conf, data):
    if not can_use_comm:
        return
    ant = Comm(conf)
    while True:
        # Send data
        ant.send(data.to_dict())

        # Read incoming
        incoming = ant.read_comm()
        command = ""
        if incoming != "":
            try:
                info = loads(incoming)
                if info.get("key", "") == SECRET_KEY:
                    command = info.get("command", "")
            except Exception as e:
                print("ERROR!!!!", e)
                pass
        if command not in ["", "{}"]:
            print(f"\nIncoming Data: <{incoming}> <{command}>\n")
        if command == "a":
            print("\nGot command to ARM!")
            conf.state = "ARM"
        if command == "s":
            print("\nGot command to SIMULATE!")
        if command == "h":
            print("\nGot command to HALT!")
            conf.state = "HALT"
        if command == "e1":
            print("\nGot command to EJECT_APOGEE!")
            USBRelay.Relay1(conf, data)
        if command == "e2":
            print("\nGot command to EJECT_MAIN!")
            USBRelay.Relay2(conf, data)
