"""
State.py
Perform actions of the rocket and manage state.

hooks is a dictionary mapping a hook string to a 
list of functions to thread when the hook occurs.
"""

import datetime
from os import system
import threading

from src.common.constants import *

class State:
    def __init__(self, conf, data, hooks={}):
        self.hooks = hooks
        self.conf = conf
        self.data = data
        
        # Map of state to function
        self.actions = {
            "HALT": self.halt,
            "IDLE": self.idle,
            "ARM": self.arm,
            "IGNITE": self.ignite,
            "BURN": self.burn,
            "COAST": self.coast,
            "APOGEE": self.apogee,
            "FALL": self.fall,
            "EJECT": self.eject,
            "RECOVER": self.recover,
            "WAIT": self.wait,
            "TEST": self.test,
            "SHUTDOWN": self.shutdown,
            "RESTART": self.restart,
        }
        self.activate_hook("idle_start")

    def act(self):
        """
        Use the correct method for the correct state.
        """
        self.conf.last_state = self.conf.state
        self.conf.state = self.actions[self.conf.state]()
        return self.conf.state

    def activate_hook(self, hook_name):
        """
        Activate a hook function.
        """
        print(f"Activating hook '{hook_name}'")
        print(self.hooks)
        for function in self.hooks.get(hook_name, []):
            print("Starting thread")
            t = threading.Thread(target=function, args=(self.conf,self.data))
            t.start()

    def halt(self):
        """Do nothing."""
        return "HALT"

    def idle(self):
        """
        Do nothing. 
        A plugin must be used to bring the rocket out of idle.
        """
        return "IDLE"

    def arm(self):
        """Wait for launch. Continue sampling ground pressure."""
        self.data.reset_zero_pressure()

        # Detect if system starts to go up
        if self.data.check_dp_gt_val(1):
            self.activate_hook("arm_end")
            self.activate_hook("ignite_start")
            return "IGNITE"
        return "ARM"

    def ignite(self):
        """Move to burn state. Might begin simulation."""
        self.activate_hook("ignite_end")
        self.activate_hook("burn_start")
        return "BURN"

    def burn(self):
        """Change state if no longer going up."""
        if self.data.get_accelerometer_up() <= 0:
            self.activate_hook("burn_end")
            self.activate_hook("coast_start")
            return "COAST"
        return "BURN"

    def coast(self):
        """Change state to Use air-stoppers if necessary."""
        if self.data.check_dp_gt_val(0):
            print(f"DP: {self.data.dp}")
            self.activate_hook("coast_end")
            self.activate_hook("apogee_start")
            return "APOGEE"
        return "COAST"

    def apogee(self):
        """Eject parachute."""
        if self.conf.SIM:
            input(self.data.to_dict("APOGEE")["sensors"]["alt"])
        self.eject_parachute("DROGUE")
        self.activate_hook("apogee_end")
        self.activate_hook("wait_start")
        return "WAIT"

    def wait(self):
        """Wait until correct altitude."""
        if self.data.to_dict("WAIT")["sensors"]["alt"] < self.conf.MAIN_ALTITUDE: # TODO test this
            self.activate_hook("wait_end")
            self.activate_hook("eject_start")
            return "EJECT"
        return "WAIT"

    def eject(self):
        """Eject other parachute."""
        self.eject_parachute("MAIN")
        self.activate_hook("eject_end")
        self.activate_hook("fall_start")
        return "FALL"

    def fall(self):
        """Do nothing."""
        if (self.data.sense.get_pressure() - self.data.last_pressure) < 1:
            self.activate_hook("fall_end")
            self.activate_hook("recover_start")
            return "RECOVER"
        return "FALL"

    def recover(self):
        """Display Data to SenseHat."""
        return "RECOVER"


    def test(self):
        """Do nothing."""
        return "TEST"

    def restart(self):
        """Restart the system."""
        system('reboot now')

    def shutdown(self):
        """Shutdown the system."""
        system("shutdown -s")


    def eject_parachute(self, parachute):
        """Eject the parachute."""
        # Actively wait for apogee or main delay
        now = datetime.datetime.now()
        if "MAIN" in parachute.upper():
            while (
                    (datetime.datetime.now() - now).total_seconds() < self.conf.MAIN_DELAY
            ):
                pass
        elif "DROGUE" in parachute.upper():
            while (
                    (datetime.datetime.now() - now).total_seconds() < self.conf.APOGEE_DELAY
            ):
                pass

        # Hold for parachute charge time seconds
        now = datetime.datetime.now()
        self.activate_hook("eject_now")
        '''
            usb_relay.turnon(parachute, conf)
            while (
                    (datetime.datetime.now() - now).total_seconds()
                   < conf.PARACHUTE_CHARGE_TIME
            ):
                pass
            usb_relay.turnoff(parachute, conf)
        '''
        return None

    def __eq__(self, other):
        if isinstance(other, int):
            return False
        if isinstance(other, str):
            return self.conf.state == other
        return False

    def __str__(self):
        return str(self.conf.state)

    def __repr__(self):
        return str(self)
