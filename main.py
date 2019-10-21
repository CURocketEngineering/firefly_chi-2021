"""Run the main avionics process.

Used for data collection, telemetry, and  parachutes.
"""

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
    "FALL": Actions.fall,
    "EJECT": Actions.eject,
    "RECOVER": Actions.recover,
    "WAIT": Actions.wait,
    "TEST": Actions.test,
    "SHUTDOWN": Actions.shutdown,
    "RESTART": Actions.restart,
}

# Initialization
rocket_state = "IDLE"  # State of rocket
file_name = "output.json"  # Name for recording json
conf = Config.Config(open("config.json"))  # Configuration data
data = DataStruct.DataStruct(file_name, conf)  # Avionics data
comm = Comm.Comm()  # Communication channel


while (not shutdown) or (conf.FIDI):
    data.read_sensors(conf)  # Update sensors (update sensors)
    if conf.DEBUG:
        print(data)

    rocket_state = data.process(rocket_state) 
    rocket_state = comm.read_comm(rocket_state)  # Update state from comm
    
    comm.send(data.to_json(rocket_state)) # Send data
    data.write_out(rocket_state) # Write data

    # Make Decisions
    rocket_state = actions[rocket_state](data) if (actions[rocket_state](data) != None) else rocket_state
