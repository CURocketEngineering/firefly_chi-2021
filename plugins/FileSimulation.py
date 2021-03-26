'''
FileSimulation.py
'''

from time import sleep
from json import loads


def FileSimulation(conf, data):
    print("FileSimulation Init")
    sim_data = None

    while conf.rocket_state is None:
        pass
    print("[FileSimulation.py]: rocket_state defined, continuing")

    data_file = open(conf.SIM_FILE, "r")
    lines = data_file.readlines()
    sim_data = [loads(line) for line in lines]
    sim_data = sim_data[1:]
    sim_zero_alt = sim_data[0]["sensors"]["alt"]
    data.ground_pressure = sim_zero_alt
    data_file.close()

    # Set state to arm
    conf.state = "ARM"
    last_state = "ARM"
    conf.rocket_state.activate_hook("arm_start")
    
    while len(sim_data) > 0:
        sleep(conf.SIM_TD)
        new_data = sim_data[0]
        new_data["sensors"]["alt"] -= sim_zero_alt
        data.add_dp(new_data["sensors"]["pres"] - data.last_pressure)
        data.last_pressure = new_data["sensors"]["pres"]
        sim_data = sim_data[1:]  # Remove first entry
        data.current_data = new_data

        # Don't continue in HALT
        while conf.state == "HALT":
            pass
        last_state = conf.state if conf.state != "HALT" else last_state
        conf.state = last_state  # Restore after HALT
        
    print("Simulation Over")
    conf.shutdown = True
