"""Drag program.

This simulates zero-lift/parasite drag. This all drag is induced
parallel to flight. 

This is heavily based off of the Drag Coefficient Prediction paper.
"""

from sympy import *
from math import atan, log10
import matplotlib

PI = 3.14
e = 2.71 



class Rocket:
    def __init__(self, verbose=False, mach=0):
        """Initialize variables for simulation.

        Variables are lbs, ft, ...
        """
        self.verbose = verbose
        
        self.nose_cone_length = 1.666  # Length of nose cone
        self.body_tube_length = 7.5  # Length of body tube
        self.length = self.nose_cone_length + self.body_tube_length

        self.radius = 0.1666  # Maximum radius of rocket
        self.boat_tail_radius = .1666  # Minumum boat tail radius
        self.diameter = 2 * self.radius 

        if mach == 0:
            self.velocity = 143.4
            self.M = self.velocity*0.0008957066031914082  # Ideal mach number
            self.m = self.M
            self.Mach = self.M
            self.mach = self.M
        else:
            self.M = mach
            self.m = self.M
            self.Mach = self.M
            self.mach = self.M
            self.velocity = self.M/0.0008957066031914082 
        
        self.K = 0.0004  # Coefficient of "paint"...

        self.number_of_fins = 4
        self.fin_length = .1666
        self.fin_height_long = 0.4166  # Fin root cord
        self.fin_height_short = 0.1458  # Fin tip cord
        self.fin_thickness = .021
        self.fin_lambda = self.fin_height_short/self.fin_height_long

        self.K_f = 1.04  # mutual interference factor, used to simulate interference drag, 
        
        # Total wetted surface area of rocket (approximation)
        self.S_B = (PI*self.diameter*self.body_tube_length +
                    PI*self.radius**2 +
                    self.number_of_fins*(1/2)*(self.fin_height_long+self.fin_height_short)*self.fin_length)


    def drag_coefficient(self, h=4450):
        if self.verbose:
            print(f"Skin friction drag {self.skin_friction_drag(h)}\n"
                  f"Base drag {self.base_drag(h)}"
                  f"Transonic wave drag {self.transonic_wave_drag()}"
                  f"Supersonic wave drag {self.supersonic_wave_drag()}")
        C_d = (self.skin_friction_drag(h) +
               self.base_drag(h) +
               self.transonic_wave_drag() +
               self.supersonic_wave_drag())
        return C_d

    def skin_friction_drag(self, h):
        if self.verbose:
            print(f"Body friction {self.body_friction_drag(h)}\n"
                  f"Fin friction {self.fin_friction_drag(h)}\n"
                  f"Protuberance {self.protuberance_friction_drag()}\n")
        sfd = (self.body_friction_drag(h) +
               self.K_f * self.fin_friction_drag(h) +
               self.K_f * self.protuberance_friction_drag())
        return sfd

    def body_friction_drag(self, h):
        bfd = (self.C_f_final(h) * (1 +
                                   (60/((self.body_tube_length+self.nose_cone_length)/self.diameter)**3) +
                                   .0025*(self.body_tube_length/self.diameter)
        )*((4*self.S_B)/(PI*(self.diameter**2))))
        return bfd

    def C_f_final(self, h):
        if self.C_f(h) >= self.C_f_term():
            return self.C_f(h)
        else:
            return self.C_f_term()

    def C_f(self, h):
        val = (self.C_f_star(h)*(1 + 0.00798*self.M-0.1813*self.M**2+0.0632*self.M**3-0.00933*self.M**4+0.000549*self.M**5))
        return val

    def C_f_star(self, h):
        return 0.037036*(self.Rn_star(h)**(-0.155079))

    def C_f_term(self):
        return self.C_f_term_star()/(1+0.2044*(self.mach**2))

    def C_f_term_star(self):
        val = 1 / (1.89 + 1.62 * log10((self.body_tube_length+self.nose_cone_length)/self.K))**2.5
        return val

    def Rn_star(self, h):
        """Compressible Reynolds Number."""
        val = (self.a(h)*self.Mach*(self.body_tube_length+self.nose_cone_length)/(12*self.velocity))
        val *= (1 + 0.0283*self.M -0.043*self.M**2 + 0.2107*self.M**3 - 0.03829*self.M**4 + 0.002709*self.M**5)
        return val

    def fin_friction_drag(self, h):
        # Assumes fins of same thickness
        val = self.C_f_lambda(h)*(
            1 + 60*(self.fin_thickness/self.fin_height_long)**4 + 0.8*(self.fin_thickness/self.fin_height_long)
        ) * (
            self.number_of_fins * (self.fin_length/(self.fin_height_long + self.fin_height_short)) / (4 * PI * self.diameter**2)
        )
        return val

    def C_f_lambda(self, h):
        # Lambda will never be zero
        l = self.fin_height_short/self.fin_height_long
        val = (self.C_f_final(h) *
               (((log10(self.R_n(h)))**(2.6))/((l**2)-1)) *
               ((l**2)/(log10(self.R_n(h)*l))**2.6 - 1/(log10(self.R_n(h)))**2.6 + 0.5646*(((l**2)/(log10(self.R_n(h)*l))**3.6) - (1/(log10(self.R_n(h)))**3.6))))
        return abs(val) # TODO WTF

    def R_n(self, h):
        return self.a(h)*self.mach*self.fin_height_long/(12 * self.velocity)

    def protuberance_friction_drag(self):
        return 0  # assume negligable

    def excrescencies_friction_drag(self):
        return 0  # assume negligable

    def base_drag(self, h):
        b_d = (self.K_b() *
               ((self.boat_tail_radius/self.radius)**(self.n()) /
                (self.skin_friction_drag(h))**(1/2)) )
        if self.M > 0.6:
            if self.M < 1:
                b_d *= 1 + 215.8* (self.M-.6)**6
            elif self.M < 2:
                b_d *= 2.0881*(self.M-1)**3 - 3.7938*(self.M-1)**2 + 1.4618*(self.M-1) + 1.883917
            else:
                b_d *= 0.297*(self.M-2)**3 -0.7937*(self.M-2)**2 - 0.1115*(self.M-2) + 1.64006
        return b_d

    def n(self):
        return 3.6542*(self.body_tube_length/self.diameter)**(-0.2733)

    def K_b(self):
        return 0.0274 * atan((self.body_tube_length/self.diameter) + 0.0116)

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
        return 0.000157*e**(a*h + b)

    def transonic_wave_drag(self):
        return 0

    def supersonic_wave_drag(self):
        return 0



if __name__ == "__main__":
    d = Rocket(verbose=False)
    height = 500
    machs = list(range(0,1000))
    machs = [mach*.005 for mach in machs]
    drags = []
    for i, emach in enumerate(machs):
        r = Rocket(verbose=False, mach=emach)
        drags.append(r.drag_coefficient(h=height))

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(machs, drags)
    ax.grid()
    plt.show()
        
    
    r_C_d = d.drag_coefficient(h=height)
    print(f"Drag Coefficient at {height} ft: {r_C_d}")
    print("Ran sim.")
