"""imu.py 

This implimentation uses the sensehat.
"""

from sense_hat import SenseHat

class Alt:
    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.zero_pressure = self.get_pressure()


    def get_pressure():
        return self.sense.get_pressure()

    def get_altitude():
        """P = P0*e^(-Mgz/RT).

        Assumes obvious constants ie earth atmosphere avg molar mass.
        """
        try:
            M = 0.0289644 # molar mass of earth's air
            g = 9.81 # m / sec^2 acc
            R = 8.314462 # kg m^2 / s^2 K mol
            p0 = self.millibars_to_atmospheres(self.zero_pressure)
            p = self.millibars_to_atmospheres(self.get_pressure())
            T = self.get_temperature() + 273.15
            # z = ln(P/P0) * (-RT/Mg)
            return -log(p/p0) * R * T / (M * g)
        except:
            return 0

    def millibars_to_atmospheres(self, mb):
        return mb*0.0009869233

    def get_humidity():
        return self.sense.get_humidity()

    def get_temperature():
        return self.sense.get_temperature()

    def set_zero_pressure():
        """Set zero pressure relatively."""
        self.zero_pressure = (self.zero_pressure + self.get_pressure()) / 2

