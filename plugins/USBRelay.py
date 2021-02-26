from .low_level import relay
from time import sleep

HOLD_TIME = 1


def Relay(conf, data):
    rel = relay.Relay(verbose=True)
    if conf.state == "COAST":
        sleep(conf.APOGEE_DELAY)
        rel.turnon(1, None)
        sleep(HOLD_TIME)
        rel.turnoff(1, None)
    if conf.state == "WAIT":
        sleep(conf.MAIN_DELAY)
        rel.turnon(2, None)
        sleep(HOLD_TIME)
        rel.turnoff(2, None)

