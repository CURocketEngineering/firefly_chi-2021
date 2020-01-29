"""Low level relay module for 5 volt USB Relay 2
SRD-5VDC-SL-C SONGLE. 

Assumes single board with 2 relays.
"""
import usbrelay_py as urelay

class Relay:
    def __init__(self, verbose=False):
        self.verbose = verbose

        self.OFF = 0
        self.ON = 1

        try:
            self.board = urelay.board_details()[0]  # Assumes single relay board
            self.active = True
        except Exception:
            self.board = None
            self.active = False

    def turnon(self, parachute, conf):
        """
        Turn on usb relay.
        """
        if not self.active:
            return None
        
        urelay.board_control(self.board[0], self.get_par(parachute), self.ON)
        return None

    def turnoff(self, parachute, conf):
        """
        Turn off usb relay.
        """
        if not self.active:
            return None
        
        urelay.board_control(self.board[0], self.get_par(parachute), self.OFF)
        return None

    def get_par(self, parachute):
        """
        Get numerical parachute from string.
        """
        if type(parachute) == int:
            return parachute
        elif type(parachute) == str:
            if "apogee" in parachute.lower():
                return 1
            elif "main" in parachute.lower():
                return 2
        return 1


# The following is used for debugging
if __name__ == "__main__":
    from time import sleep
    r = Relay(verbose=True)
    for relay in range(2):
        r.turnon(relay+1, None)
        sleep(2)
        r.turnoff(relay+1, None)
