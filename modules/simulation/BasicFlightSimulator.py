## BasicFlightSimulator.py
# Original by Andrew Billings
# Rewritten by Harrison Hall

from numpy import arange
from math import pi as PI

thrustCurve1 = [0.045, 0.067, 0.084, 0.124, 0.186, 0.231, 0.298, 0.371, 0.534, 0.979, 1.142, 2.002, 2.289, 2.761, 3.121, 3.436, 3.678, 3.79, 4.004, 4.415, 4.538, 4.656, 4.82, 5.005, 5.219, 5.371]
thrustCurve2 = [2638.366, 2528.97, 3063.078, 2426.009, 2548.275, 2599.755, 2554.71, 2644.801, 2638.366, 2561.145, 2606.19, 2638.366, 2638.366, 2580.45, 2496.795, 2335.919, 2213.653, 2129.998, 1653.805, 888.035, 630.634, 450.453, 289.577, 135.136, 25.74, 0]

# Motor
propellant_mass = 7.183 # From http://www.thrustcurve.org/simfilesearch.jsp?id=2029 [kg]
burn_time = 5.4 # [s]

# Drag Coefficient
drag_coefficient = 0.35 # 0.1; % Should be 0.1(streamlined) - 1.0(unstreamlined/bluff) %THE HARD PART

# Rocket Details
initial_mass = 75 * 0.453592; # [Kilograms]
diameter = 6 * 0.0254 # [m]
number_of_fins = 4
fin_span = 4 * 0.0254 # [m]
fin_thickness = 0.5 * 0.0254 # [m]


# Variables
initial_altitude = 0 # [m]
initial_velocity = 0 # [m/s]
time_data = arange(1, 60, .01) # [s]
mass_flow_rate = propellant_mass/burn_time # [kg/s]
g = 9.81 # [m/s^2]
## thrust_data TODO
## TODO
air_density = 1.225 # [kg/m^3]
area_of_nose = (PI/4) * (diameter**2) # [m^2]
area_of_fins = fin_span * fin_thickness * number_of_fins # [m^2]
area = area_of_nose + area_of_fins # [m^2]


# Simulator
altitude = [0]*6001
altitude[0] = initial_altitude
velocity = [0]*6001
velocity[0] = initial_velocity
mass = [0]*6001
mass[0] = initial_mass

for i in range(6000):
    dt = time_data[i+1] - time_data[i]
    altitude[i+1] = altitude[i] + altitude[i]*dt
    if velocity[i] == 0:
        velocity[i+1] = ((-g) + (thrust_data[i]/mass[i]))*dt
    else:
        velocity[i+1] = velocity[i] + (((-g)-(0.5)*air_density*velocity[i]*abs(velocity[i])*((drag_coefficient*area)/mass[i]))+((velocity[i]/abs(velocity[i])*(thrust_data[i]/mass[i])))) * dt

    if thrust_data[i] > 0:
        mass[i+1] = mass[i] + (-mass_flow_rate) * dt
    else:
        mass[i+1] = mass[i]

# Plots



