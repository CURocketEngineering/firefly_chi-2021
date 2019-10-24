"""Run the main avionics process.

Used for data collection, telemetry, and  parachutes.
"""

from modules import Comm
from modules import DataStruct
from modules import Actions
from modules import Config

shutdown = False


# Initialization
rocket_state = "IDLE"  # State of rocket
file_name = "output.json"  # Name for recording json
conf = Config.Config("config.json")  # Configuration data
data = DataStruct.DataStruct(file_name, conf)  # Avionics data
comm = Comm.Comm(conf)  # Communication channel


while (not shutdown) or (conf.FIDI):
    data.read_sensors()  # Update sensors 
    if conf.DEBUG:
        print(f"STATE: {rocket_state}")
        print(data)

    if conf.SIM:
        if rocket_state == "IDLE":
            rocket_state = "ARM"
        if data.last_state != rocket_state:
            input(f"STATE CHANGE: {rocket_state}")
        if rocket_state in ["APOGEE"]:
            input("PAUSE BUFFER")
    
    rocket_state = data.process(rocket_state) 
    rocket_state = comm.read_comm(rocket_state)  # Update state from comm
    
    comm.send(data.to_json(rocket_state)) # Send data
    data.write_out(rocket_state) # Write data

    # Make Decisions
    new_state = Actions.actions[rocket_state](data, conf)
    if new_state is not None:
        rocket_state = new_state
