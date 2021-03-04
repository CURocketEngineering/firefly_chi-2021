"""
State.py
========
Perform actions of the rocket and manage state.

`hooks` is a dictionary mapping a hook string to a 
list of functions to thread when the hook occurs.
"""

import datetime
from os import system
from threading import Thread

class State:
    def __init__(self, conf, data, hooks={}):
        self.hooks = hooks
        self.conf = conf
        self.data = data
        
        # Map of state to function
        self.actions = {
            "HALT": self.halt,  # Rocket should not do anything
            "ARM": self.arm,  # Rocket is ready to begin state system
            "UPWARD": self.upward,  # Rocket is going up
            "APOGEE": self.apogee,  # Rocket is at apogee
            "DOWNWARD": self.downward,  # rocket is going down
            "EJECT": self.eject,  # rocket is at main ejection altitude
            "RECOVER": self.recover,  # rocket is in recovery state
            "SHUTDOWN": self.shutdown,
            "RESTART": self.restart,
        }
        self.activate_hook("halt_start")

    def act(self) -> str:
        """
        Use the correct method for the correct state.
        """
        self.conf.last_state = self.conf.state  # Update last state
        self.conf.state = self.actions[self.conf.state]()  # Perform action
        return self.conf.state  # Return current state

    def activate_hook(self, hook_name : str) -> None:
        """
        Activate a hook function.
        """
        print(f"Activating hook '{hook_name}'")
        print(self.hooks)
        for function in self.hooks.get(hook_name, []):
            print("Starting thread")
            t = Thread(target=function, args=(self.conf,self.data))
            t.start()

    def halt(self) -> str:
        """Do nothing. A halted rocket shouldn't do anything."""
        return "HALT"

    def arm(self) -> str:
        """
        Wait for launch.
        System is going up if it is 100 meters in the air and 8/10 of the last
        dp readings are negative.
        """
        # Detect if system starts to go up
        distance_above_ground = self.data.to_dict()["sensors"]["alt"]
        if self.data.check_dp_lt_val(0) and distance_above_ground > 100:
            self.activate_hook("arm_end")
            self.activate_hook("upward_start")
            return "UPWARD"
        return "ARM"

    def upward(self):
        """Change state to Use air-stoppers if necessary."""
        if self.data.check_dp_gt_val(0):
            self.activate_hook("upward_end")
            self.activate_hook("apogee_start")
            return "APOGEE"
        return "UPWARD"

    def apogee(self):
        """Eject parachute."""
        self.activate_hook("apogee_end")
        self.activate_hook("downward_start")
        return "DOWNWARD"

    def downward(self):
        """Wait until correct altitude."""
        if self.data.to_dict()["sensors"]["alt"] < self.conf.MAIN_ALTITUDE:
            self.activate_hook("wait_end")
            self.activate_hook("eject_start")
            return "EJECT"
        return "DOWNWARD"

    def eject(self):
        """Eject other parachute."""
        self.activate_hook("eject_end")
        self.activate_hook("recover_start")
        return "RECOVER"

    def recover(self):
        """Do nothing."""
        return "RECOVER"

    def restart(self):
        """Restart the system."""
        system('reboot now')

    def shutdown(self):
        """Shutdown the system."""
        system("shutdown -s")

    def __str__(self):
        return str(self.conf.state)

    def __repr__(self):
        return str(self)
