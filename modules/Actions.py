"""Perform actions of the rocket."""

from os import system


def halt():
    """Do nothing."""
    return None


def idle():
    """Do nothing."""
    return None


def arm():
    """Do nothing."""
    return None


def ignite():
    """Do nothing."""
    print("PASS: Not finished")
    return None


def burn():
    """Do nothing."""
    return None


def coast():
    """Use air-stoppers if necessary."""
    return None


def apogee():
    """Eject parachute."""
    return None


def eject():
    """Eject other parachute."""
    return None


def fall():
    """Do nothing."""
    return


def recover():
    """Do nothing."""
    return


def wait():
    """Do nothing."""
    return


def test():
    """Do nothing."""
    return


def restart():
    """Restart the system."""
    system('reboot now')


def shutdown():
    """Shutdown the system."""
    system("shutdown -s")
