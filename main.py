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
data = DataStruct.DataStruct(file_name)  # Avionics data
comm = Comm.Comm()  # Communication channel
conf = Config.Config()  # Configuration data

while (not shutdown):
    data.read_sensors(conf)  # Update sensors

    rocket_state = data.process(rocket_state)
    rocket_state = comm.read_comm()  # Update state from comm
    comm.send(data.to_json(rocket_state))
    data.write_out(rocket_state)

    # Make Decisions
    actions[rocket_state]()
