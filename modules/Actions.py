"""Perform actions of the rocket."""

from os import system


def halt(data):
    """Do nothing."""
    return "HALT"


def idle(data):
    """Do nothing."""
    return "IDLE"


def arm(data):
    """Wait for launch. Continue sampling ground pressure."""
    data.reset_zero_pressure()

    # Detect if system starts to go up
    if (data.sense.get_pressure() - last_pressure) > 1: 
        return "IGNITE"
    return "ARM"


def ignite(data):
    """Move to burn state. Might begin simulation."""
    print("PASS: Not finished")
    print("TODO SIMULATION HERE")
    return "BURN"


def burn(data):
    """Change state if no longer going up."""
    if data.get_accelerometer_up() <= 0:
        return "COAST"
    return "BURN"


def coast(data):
    """Change state to Use air-stoppers if necessary."""
    if (data.sense.get_pressure() - data.last_pressure) >= 1:
        return "APOGEE"
    return "COAST"


def apogee(data):
    """Eject parachute."""
    # TODO DELAY
    eject_parachute(data, "DROGUE")
    return "WAIT"


def wait(data):
    """Wait until correct altitude."""
    if data.get_altitude() < data.MAIN_ALTITUDE: # TODO
        return "EJECT"
    return "WAIT"


def eject(data):
    """Eject other parachute."""
    # TODO DELAY
    eject_parachute("MAIN")
    return "DATA"


def fall(data):
    """Do nothing."""
    if (data.sense.get_pressure() - data.last_pressure) < 1:
        return "RECOVER"
    return "FALL"


def recover(data):
    """Display Data to SenseHat."""
    # TODO Sensehat stuff
    return "RECOVER"


def test(data):
    """Do nothing."""
    return "TEST"


def restart(data):
    """Restart the system."""
    system('reboot now')


def shutdown(data):
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
