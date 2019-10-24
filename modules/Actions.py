"""Perform actions of the rocket."""

from os import system


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
    if (data.dp) > 1: 
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
    if (data.dp) > 0:
        return "APOGEE"
    return "COAST"


def apogee(data, conf):
    """Eject parachute."""
    # TODO DELAY
    input(data.to_dict("APOGEE")["sensors"]["alt"])
    
    eject_parachute(data, "DROGUE")
    return "WAIT"


def wait(data, conf):
    """Wait until correct altitude."""
    if data.to_dict("WAIT")["sensors"]["alt"] < conf.MAIN_ALTITUDE: # TODO
        return "EJECT"
    return "WAIT"


def eject(data, conf):
    """Eject other parachute."""
    # TODO DELAY
    eject_parachute(data, "MAIN")
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


# actions
def eject_parachute(data, parachute):
    """Eject the parachute. TODO"""
    if parachute == "MAIN":
        pass
    else: # DROGUE
        pass
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
