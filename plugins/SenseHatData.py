'''
SenseHatData.py
'''

try:
    from sense_hat import SenseHat
    from math import log
except Exception as e:
    print("[SenseHatData.py]:", e)

def get_altitude(zero_pressure, new_pressure, new_temperature):
    """P = P0*e^(-Mgz/RT).

    Assumes obvious constants ie earth atmosphere avg molar mass.
    """
    try:
        M = 0.0289644 # molar mass of earth's air
        g = 9.81 # m / sec^2 acc
        R = 8.314462 # kg m^2 / s^2 K mol
        p0 = millibars_to_atmospheres(zero_pressure)
        p = millibars_to_atmospheres(new_pressure)
        T = new_temperature + 273.15
        # z = ln(P/P0) * (-RT/Mg)
        return -log(p/p0) * R * T / (M * g)
    except:
        return 0

def SenseHatData(conf, data):
    sense = SenseHat()
    sense.clear()
    zero_pressure = sense.get_pressure()
    while not conf.shutdown:
        # Altimeter
        data["sensors"]["alt"] = get_altitude(zero_pressure, sense.get_pressure(), sense.get_temperature())  # meters
        data["sensors"]["hum"] = sense.get_humidity()  # %
        data["sensors"]["temp"] = (sense.get_temperature() * 9 / 5) + 32  # F
        data["sensors"]["pres"] = sense.get_pressure()
        conf.data.add_dp(sense.get_pressure() - conf.data.last_pressure)
        conf.data.last_pressure = sense.get_pressure()
        
        # IMU
        data["sensors"]["acc"] = sense.get_acclerometer_raw()  # Gs
        data["sensors"]["pitch"] = sense.get_acclerometer()["pitch"]  # degrees
        data["sensors"]["yaw"] = sense.get_acclerometer()["yaw"]  # degrees
        data["sensors"]["roll"] = sense.get_acclerometer()["roll"]  # degrees
        data["sensors"]["compass"] = sense.get_compass()  # rad/sec
        data["sensors"]["gyro"] = sense.get_gyroscope_raw()  # rad/sec
        data["sensors"]["mag"] = sense.get_compass_raw()  # microteslas
