# main.py

from modules import Comm
from modules import DataStruct
from modules import Actions
from modules import Config

shutdown = False

# Map of state to action
actions = {
    "HALT": Actions.halt,
    "IDLE": Actions.idle,
    "ARM": Actions.arm,
    "IGNITE": Actions.ignite,
    "BURN": Actions.burn,
    "COAST": Actions.coast,
    "APOGEE": Actions.apogee,
    "EJECT": Actions.eject,
    "FALL": Actions.fall,
    "RECOVER": Actions.recover,
    "WAIT": Actions.wait,
    "TEST": Actions.test,
    "SHUTDOWN": Actions.shutdown,
    "RESTART": Actions.restart,
}

# Initialization
rocket_state = "IDLE" # State of rocket
file_name = "output.json" # Name for recording json
data = DataStruct.DataStruct(file_name) # Avionics data
comm = Comm.Comm() # Communication channel

while (not shutdown):

    # Update
    if not Config.DEBUG:
        data.read_sensors() # Update sensors
    else:
        pass # Will be used for testing
    
    rocket_state = data.process(rocket_state)
    rocket_state = comm.read_comm() # Update state from comm
    comm.send(data.to_json(rocket_state))
    data.write_out(rocket_state)

    # Make Decisions
    actions[rocket_state]()
