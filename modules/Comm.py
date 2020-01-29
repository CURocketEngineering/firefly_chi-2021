"""Perform communication related functions."""
from modules.low_level import low_comm

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

    def send(self, data, skip_time=0, as_json=True):
        """Async send data to specific XBee network."""
        
        return self.antenna.send(
            data,
            skip_time=skip_time,
            as_json=as_json
        )
