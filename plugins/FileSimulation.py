'''
FileSimulation.py
'''

from time import sleep
from json import loads


def FileSimulation(conf, data):
    print("FileSimulation Start")
    sim_data = None

    data_file = open(conf.SIM_FILE, "r")
    lines = data_file.readlines()
    sim_data = [loads(line) for line in lines]
    data.sim_data_current = sim_data[0]
    sim_data = sim_data[1:]
    data.sim_zero_alt = data.sim_data_current["sensors"]["alt"]
    data_file.close()
    while len(sim_data) > 0:
        sleep(conf.SIM_TD)
        new_data = sim_data[0]
        new_data["sensors"]["alt"] -= data.sim_zero_alt
        data.add_dp(new_data["sensors"]["pres"] - data.last_pressure)
        data.last_pressure = new_data["sensors"]["pres"]
        sim_data = sim_data[1:]  # Remove first entry
        data.sim_data_current = new_data
    print("simulation over")
    conf.shutdown = True
