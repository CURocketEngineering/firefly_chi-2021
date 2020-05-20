"""Perform actions of the rocket."""
from lib.low_level import relay

import datetime
from os import system


usb_relay = relay.Relay()


def halt(data, conf):
    """Do nothing."""
    return "HALT"


def idle(data, conf):
    """Do nothing."""
    return "IDLE"


def arm(data, conf):
    """Wait for launch. Continue sampling ground pressure."""
    data.reset_zero_pressure()

    # Detect if system starts to go up
    if data.check_dp_gt_val(1):
        return "IGNITE"
    return "ARM"


def ignite(data, conf):
    """Move to burn state. Might begin simulation."""
    print("TODO SIMULATION HERE")
    return "BURN"


def burn(data, conf):
    """Change state if no longer going up."""
    if data.get_accelerometer_up() <= 0:
        return "COAST"
    return "BURN"


def coast(data, conf):
    """Change state to Use air-stoppers if necessary."""
    if data.check_dp_gt_val(0):
        print(f"DP: {data.dp}")
        return "APOGEE"
    return "COAST"


def apogee(data, conf):
    """Eject parachute."""
    # TODO DELAY
    if conf.SIM:
        input(data.to_dict("APOGEE")["sensors"]["alt"])
    
    eject_parachute(data, conf, "DROGUE")
    return "WAIT"


def wait(data, conf):
    """Wait until correct altitude."""
    if data.to_dict("WAIT")["sensors"]["alt"] < conf.MAIN_ALTITUDE: # TODO
        return "EJECT"
    return "WAIT"


def eject(data, conf):
    """Eject other parachute."""
    # TODO DELAY
    eject_parachute(data, conf, "MAIN")
    return "RECOVER"


def fall(data, conf):
    """Do nothing."""
    if (data.sense.get_pressure() - data.last_pressure) < 1:
        return "RECOVER"
    return "FALL"


def recover(data, conf):
    """Display Data to SenseHat."""
    # TODO Sensehat stuff
    return "RECOVER"


def test(data, conf):
    """Do nothing."""
    return "TEST"


def restart(data, conf):
    """Restart the system."""
    system('reboot now')


def shutdown(data, conf):
    """Shutdown the system."""
    system("shutdown -s")


def eject_parachute(data, conf, parachute):
    """Eject the parachute. TODO"""

    # Wait for apogee or main delay
    now = datetime.datetime.now()
    if "MAIN" in parachute.upper():
        while ((datetime.datetime.now() - now).total_seconds()
               < conf.MAIN_DELAY):
            pass
    elif "DROGUE" in parachute.upper():
        while ((datetime.datetime.now() - now).total_seconds()
               < conf.APOGEE_DELAY):
            pass

    # Hold for parachute charge time seconds
    now = datetime.datetime.now()
    usb_relay.turnon(parachute, conf)
    while ((datetime.datetime.now() - now).total_seconds()
           < conf.PARACHUTE_CHARGE_TIME):
        pass
    usb_relay.turnoff(parachute, conf)
    
    return None


# Map of state to function
actions = {
    "HALT": halt,
    "IDLE": idle,
    "ARM": arm,
    "IGNITE": ignite,
    "BURN": burn,
    "COAST": coast,
    "APOGEE": apogee,
    "FALL": fall,
    "EJECT": eject,
    "RECOVER": recover,
    "WAIT": wait,
    "TEST": test,
    "SHUTDOWN": shutdown,
    "RESTART": restart,
}
