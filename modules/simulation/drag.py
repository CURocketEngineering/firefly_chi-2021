"""Drag program.

This simulates zero-lift/parasite drag. This all drag is induced
parallel to flight. 

This is heavily based off of the Drag Coefficient Prediction paper.

For running as main, requires a prometheus.csv containing data from
RAS aero form the promethus rocket. I would clean it up but I'll wait
until it is more accurate.
"""

from sympy import *
from math import atan, log10, asin
from math import pi as PI, e
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import exp, sqrt


class Rocket:
    def __init__(self, verbose=False, mach=0):
        """Initialize variables for simulation.

        Variables are lbs, ft, ...
        """
        self.verbose = verbose
        
        self.nose_cone_length = 1.333  # Length of nose cone
        self.body_tube_length = 5.333  # Length of body tube
        self.length = self.nose_cone_length + self.body_tube_length

        self.radius = 0.1666  # Maximum radius of rocket
        self.boat_tail_radius = .1666  # Minumum boat tail radius
        self.diameter = 2 * self.radius 

        if mach == 0:
            self.velocity = 143.4
            self.M = self.velocity*0.0008957066031914082  # Ideal mach number
        else:
            self.M = mach
            self.velocity = self.M/0.0008957066031914082 
        
        self.K = 0.0004  # Coefficient of "paint"...

        self.number_of_fins = 4
        self.fin_length = .333
        self.fin_height_long = 1  # Fin root cord
        self.fin_height_short = 0.333  # Fin tip cord
        self.fin_thickness = .0833
        self.fin_lambda = self.fin_height_short/self.fin_height_long
        self.x = self.fin_length / 8  # Distance from fin leading edge to maximum thickness

        self.K_f = 1.04  # mutual interference factor, used to simulate interference drag, 

        a = (self.radius**2 +
             self.nose_cone_length**2)/(2*self.radius)

        # Total wetted surface area of rocket (approximation)
        self.S_B = (
            2 * PI * (
                (self.radius - a) *
                asin(self.nose_cone_length / a) + self.nose_cone_length
            )
        )
        


    def drag_coefficient(self, h=4450):
        """Total drag coefficient."""
        if self.verbose or True:
            print(f"Skin friction drag {self.skin_friction_drag(h)}\n"
                  f"Base drag {self.base_drag(h)}"
                  f"Transonic wave drag {self.transonic_wave_drag()}"
                  f"Supersonic wave drag {self.supersonic_wave_drag()}")
            
        C_d = (self.skin_friction_drag(h) +
               self.base_drag(h) +
               self.transonic_wave_drag() +
               self.supersonic_wave_drag()
        )
        return C_d

    def skin_friction_drag(self, h):
        """Drag due to skin friction.
        
        This is a sum of body friction, fin friction, 
        and protuberance friction.
        """
        if self.verbose:
            print(f"Body friction {self.body_friction_drag(h)}\n"
                  f"Fin friction {self.fin_friction_drag(h)}\n"
                  f"Protuberance {self.protuberance_friction_drag()}\n")
        sfd = (
            self.body_friction_drag(h) +
            self.K_f * self.fin_friction_drag(h) +
            self.K_f * self.protuberance_friction_drag() +
            self.excrescencies_friction_drag()
        )
        return sfd

    def body_friction_drag(self, h):
        bfd = (
            self.C_f_final(h) * (
                1 + (
                    60/((
                        self.body_tube_length+self.nose_cone_length) /
                        self.diameter
                    )**3) +
                .0025 * (
                    self.body_tube_length / self.diameter
                )
            ) * (
                (4*self.S_B) / (PI*(self.diameter**2))
            )
        )
        return bfd

    def C_f_final(self, h):
        if self.C_f(h) >= self.C_f_term():
            return self.C_f(h)
        else:
            return self.C_f_term()

    def C_f(self, h):
        val = (
            self.C_f_star(h)*(
                1 +
                0.00798*self.M -
                0.1813*self.M**2 +
                0.0632*self.M**3 -
                0.00933*self.M**4 +
                0.000549*self.M**5
            )
        )
        return val

    def C_f_star(self, h):
        return 0.037036*(self.Rn_star(h)**(-0.155079))

    def C_f_term(self):
        return self.C_f_term_star()/(1+0.2044*(self.M**2))

    def C_f_term_star(self):
        val = (
            1 / (
                1.89 +
                1.62 * log10(
                    (self.body_tube_length+self.nose_cone_length)
                    / self.K
                )
            )**2.5
        )
        return val

    def Rn_star(self, h):
        """Compressible Reynolds Number."""
        val = (
            (
                self.a(h) *
                self.M * (
                    self.body_tube_length +
                    self.nose_cone_length
                ) / (
                    12 * self.velocity
                )
            ) * (
                1 +
                0.0283 * self.M -
                0.043 * self.M*2 +
                0.2107 * self.M**3 -
                0.03829*self.M**4 +
                0.002709*self.M**5
            )
        )
            
        return val

    def fin_friction_drag(self, h):
        # Assumes fins of same thickness
        val = (
            self.C_f_lambda(h) * (
                1 +
                60*(
                    self.fin_thickness / self.fin_height_long
                )**4 +
                0.8 * (
                    1 + 5*(
                        (self.x / self.fin_height_long)**2 
                    )
                ) * (
                    self.fin_thickness / self.fin_height_long
                ) * (
                    4 * 
                    self.number_of_fins * (
                        self.fin_length / (
                            self.fin_height_long +
                            self.fin_height_short
                        )
                    ) / (
                        PI * self.diameter**2
                    )
                )
            )
        )
        return val

    def C_f_lambda(self, h):
        # Lambda will never be zero
        l = self.fin_height_short/self.fin_height_long
        val = (
            self.C_f_final(h) * (
                log10(self.R_n(h))**2.6 / (
                    (l**2)-1)
            ) * (
                (l**2 / (
                    log10(self.R_n(h)*l)
                )**2.6) -
                1 / (log10(self.R_n(h)))**2.6 +
                0.5646 * (
                    (
                        (l**2) / (log10(self.R_n(h)*l))**3.6
                    ) - (
                        1 / (log10(self.R_n(h)))**3.6)
                )
            )
        )
        return val.real # Why is this complex, TODO

    def R_n(self, h):
        val = (
            self.a(h) * self.M * self.fin_height_long /
            (12 * self.velocity)
        )
        return val

    def protuberance_friction_drag(self):
        """Drag due to protuberances"""
        return 0  # assume negligable

    def excrescencies_friction_drag(self):
        if self.M < 0.78:
            k = 0.00038
        elif self.M <= 1.04:
            k = (
                -.4501 * self.M**4 +
                1.5954 * self.M**3 -
                2.1062 * self.M**2 +
                1.2288 * self.M -
                .26717
            )
        else:
            k = (
                .0002 * self.M**2 -
                .0012 * self.M +
                .0018
            )
            
        val = (
            k * 4 * self.S_B / (PI * (2*self.radius)**2)
        )
        return val

    def base_drag(self, h):
        b_d = (
            self.K_b() * (
                (self.boat_tail_radius/self.radius)**(self.n()) /
                (self.skin_friction_drag(h))**(1/2)
            )
        )
        if self.M > 0.6:
            if self.M < 1:
                b_d *= 1 + 215.8* (self.M-.6)**6
            elif self.M < 2:
                b_d *= (
                    2.0881 * (
                        (self.M-1)**3
                    ) - 3.7938 * (
                        (self.M-1)**2
                    ) +
                    1.4618 * (self.M-1) +
                    1.883917
                )
            else:
                # M > 2
                b_d *= (0.297 * (self.M-2)**3 -
                        0.7937*(self.M-2)**2 -
                        0.1115*(self.M-2) +
                        1.64006
                )
        return b_d

    def n(self):
        val = (
            3.6542 *
            (self.body_tube_length/self.diameter)**(-0.2733)
        )
        return val

    def K_b(self):
        kb = (
            0.0274 *
            atan(
                (self.body_tube_length/self.diameter) +
                0.0116
            )
        )
        return kb

    def a(self, h):
        """Speed of sound [ft/s]."""
        if h <= 37000:
            return -.004*h + 1116.45
        elif h <= 64000:
            return 968.08
        else:
            return 0.0007*h + 924.99

    def v(self, h):
        """Kinematic Viscocity [ft^2/s]"""
        if h <= 15000:
            a = 0.00002503
            b = 0
        elif h <= 30000:
            a = 0.00002760
            b = -0.03417
        else:
            a = 0.00004664
            b = -0.6882
        return 0.000157 * e**(a*h + b)

    def transonic_wave_drag(self):
        if self.M_d() <= self.M and self.M <= self.M_f() :
            return self.C_d_max()
        else:
            return 0

    def M_d(self):
        md = (
            -.0156*(self.nose_cone_length/(2*self.radius))**2 + 
            .136*(self.nose_cone_length/(2*self.radius)) +
            .6817
        )
        return md

    def M_f(self):
        le = self.nose_cone_length + self.body_tube_length
        d = 2 * self.radius
        ln_le = (self.nose_cone_length)/le
        if ln_le < .2:
            a = 2.4
            b = -1.05
        else:
            a = (
                -321.94*(ln_le**2) +
                264.07*ln_le -
                36.348
            )
            b = (
                19.634*ln_le**2 -
                18.369*ln_le +
                1.7434
            )

        return a*(le/d)**b + 1.0275

    def C_d_max(self):
        le = self.nose_cone_length + self.body_tube_length
        ln_lb = self.nose_cone_length / self.body_tube_length
        d = 2 * self.radius
        c = 50.676*(ln_lb)**2 - 51.734*(ln_lb) + 15.642
        g = -2.2538*(ln_lb)**2 + 1.3108*(ln_lb) - 1.7344
        if (le/d) > 6:
            return (
                c*(le/d)**g
            )
        else:
            return (
                c*6**g
            )
        

    def supersonic_wave_drag(self):
        return 0

class CharlieRocket:
    def __init__(self, velocity=5, height=1000):
        self.h = height
        self.v = velocity
        
        # Initial Data
        self.r_cone = .16666*.3048 # radius of a cone, m
        self.h_cone = 1.333*.3048  # length of cone, m
        self.eta = self.h_cone/self.r_cone

        self.l_cone = (1/3)*self.r_cone*self.eta*(1+self.eta**2)**(-.5) # Charecteristic Length of nose cone, meters 
        self.l_fin = .333*.3048  # Length of fin, meters
        self.l_body = 5.333*.3048 # Length of the rocket body, meters
        self.s_cone = 3.14*self.r_cone**2 # reference area of the nose cone
        self.fin_count = 4

        self.T, self.a, self.P, self.rho = atmosisa(self.h) # Standard Atmosphere, need aerospace toolbox
        
        self.mu = ((1.458*10**-6) * self.T**(3/2))/(self.T + 110.4) # Dynamic Viscosity
        self.M = self.v/self.a # Mach Number
        self.y = 1.4

        self.Re_cone = self.rho*self.v*self.l_cone / self.mu  # Reynolds Number on the nose cone
        self.Re_fin = self.rho*self.v*self.l_fin / self.mu  # Reynolds Number on the fins
        self.Re_body = self.rho*self.v*self.l_body / self.mu  # Reynolds Number on the fins

    def drag(self):
        return (
            self.cone_drag(self.Re_cone, self.M, self.y, self.s_cone, self.r_cone) + 
            self.fin_drag(self.Re_fin) +
            self.fin_drag(self.Re_body)
        )

    def cone_drag(self, Re, M, y, S, d):
        """
        Nose Cone Skin Drag Coefficient. Takes in Gamma, Reynold's Number, Reference Area and Mach Number, 
        returns nose cone drag coefficient
        """
        cf = (1.328 / sqrt(Re)) * (1 - 0.0689 * M - 0.0343*M**2 + .0061*M**3 - .000278*M**4)  # Skin Drag Coefficient 
        cp = (.0071 * M + .782) * (.004714*M**2 - .06307*M +.2455) * (3.14 * d**2)/(4*S)

        # Equations from "Mathematical Modeling of Ogive Forbodies and Nose Cones".
        return (
            cf +
            cp
        )

    def fin_drag(self, Re):
        cd = 0
        if Re > 2335:
            cd = 1.328 / (Re**0.5) # Blassius Solution, flow needs to be turbulent
        else:
            cd = 2.9 / (Re**0.601) # Janour's Solution
        return (
            self.fin_count *
            cd
        )
    
# USES https://github.com/dieggsy/alfred-atmos/blob/master/src/atmos.py
def atmoslapse(h, g, gamma, R, L, hts, htp, rho0, P0, T0, *args):
    h = np.array(h)
    T = np.zeros(len(h))
    expon = np.zeros(len(h))
    if len(args) > 1:
        return 'Too many args'

    if len(args) == 1:
        H0 = args[0]
    else:
        H0 = 0

    for i in range(len(h)-1, -1, -1):
        if h[i] > htp:
            h[i] = htp

        if h[i] < H0:
            h[i] = H0

        if h[i] > hts:
            T[i] = T0 - L*hts
            expon[i] = exp(g/(R*T[i])*(hts-h[i]))

        else:
            T[i] = T0-L*h[i]
            expon[i] = 1.0

    a = (T*gamma*R)**(1/2.)
    theta = T/T0
    P = P0*theta**(g/(L*R))*expon
    rho = rho0*theta**((g/(L*R))-1.0)*expon
    return(T, a, P, rho)

# USES https://github.com/dieggsy/alfred-atmos/blob/master/src/atmos.py
def atmosisa(h):
    return atmoslapse([h], 9.80665, 1.4, 287.0531, 0.0065, 11000., 20000.,
                      1.225, 101325., 288.15)


if __name__ == "__main__":
    d = Rocket(verbose=False)
    height = 500
    machs = list(range(0,100))
    machs = [mach*.01 for mach in machs]
    drags = []
    for i, emach in enumerate(machs):
        r = Rocket(verbose=False, mach=emach)
        #r.velocity = r.M / 0.0008957066031914082  # Ideal mach number
        drags.append(r.drag_coefficient(h=height))

    input("continue")
    with open("prometheus.csv","r") as f:
        p = pd.read_csv(f)
        
    machs2 = []
    drags2 = []
    last_height = -5
    last_mach = -100
    for i in range(len(p)):
        if last_mach > p["Mach Number"][i]:
            continue
        last_height = p["Altitude (ft)"][i]
        last_mach = p["Mach Number"][i]
        machs2.append(p["Mach Number"][i])
        drags2.append(p["CD"][i])
    print(len(machs), len(drags))

    
    d = CharlieRocket()
    height = 500
    machs = list(range(1,101))
    machs = [mach*.01 for mach in machs]
    drags3 = []
    for i, emach in enumerate(machs):
        v = emach/0.0008957066031914082 
        drags3.append(
            CharlieRocket(
                height=height,
                velocity=v
            ).drag()
        )


    fig, ax = plt.subplots()
    ax.plot(machs, drags)
    ax.plot(machs2, drags2)
    ax.plot(machs, drags3)
    ax.set_xlabel("Mach")
    ax.set_ylabel("Drag Coefficient")
    ax.grid()
    plt.show()
    
    r_C_d = d.drag_coefficient(h=height)
    print(f"Drag Coefficient at {height} ft: {r_C_d}")
    print("Ran sim.")
