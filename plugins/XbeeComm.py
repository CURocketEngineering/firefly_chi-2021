"""Perform communication related functions."""

from time import sleep

can_use_comm = True
try:
    from .low_level import low_comm
except Exception as e:
    print("[XbeeComm]:", e)
    can_use_comm = False

class Comm:
    def __init__(self, conf):
        self.conf = conf
        self.antenna = low_comm.Antenna(
            remote_address=conf.REMOTE_XBEE_ID
        )

    def read_comm(self, rocket_state):
        """
        Read communication for meta-state changes.
        TODO
        """
        return rocket_state

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
        ant.send(data.to_dict())
        sleep(0.25)
