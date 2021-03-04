
can_use_relay = True
try:
    from .low_level import relay
except Exception as e:
    print("Unable to use relays")
    can_use_relay = False

from time import sleep

HOLD_TIME = 1


def RelayWatcher(conf, data):
    if not can_use_relay:
        return
    rel = relay.Relay(verbose=True)
    if conf.state == "APOGEE":
        sleep(conf.APOGEE_DELAY)
        rel.turnon(1, None)
        sleep(HOLD_TIME)
        rel.turnoff(1, None)
    if conf.state == "EJECT":
        sleep(conf.MAIN_DELAY)
        rel.turnon(2, None)
        sleep(HOLD_TIME)
        rel.turnoff(2, None)

def Relay1(conf, data):
    if not can_use_relay:
        return
    rel = relay.Relay(verbose=True)
    sleep(conf.APOGEE_DELAY)
    rel.turnon(1, None)
    sleep(HOLD_TIME)
    rel.turnoff(1, None)

def Relay2(conf, data):
    if not can_use_relay:
        return
    sleep(conf.MAIN_DELAY)
    rel.turnon(2, None)
    sleep(HOLD_TIME)
    rel.turnoff(2, None)
