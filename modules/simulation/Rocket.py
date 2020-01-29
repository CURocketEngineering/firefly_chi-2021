"""Drag program.

This simulates zero-lift/parasite drag. This all drag is induced
parallel to flight. 

This is heavily based off of the Drag Coefficient Prediction paper.
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
    def __init__(self):
        """Initialize variables for simulation.

        Variables are lbs, ft, ...
        """
        self.nose_cone_length = 1.333  # Length of nose cone
        self.body_tube_length = 5.333  # Length of body tube
        self.length = self.nose_cone_length + self.body_tube_length

        self.radius = 0.1666  # Maximum radius of rocket
        self.boat_tail_radius = .1666  # Minumum boat tail radius
        self.diameter = 2 * self.radius 

        self.K = 0.0004  # Coefficient of "paint"...

        self.number_of_fins = 4
        self.fin_length = .333
        self.fin_height_long = 1  # Fin root cord
        self.fin_height_short = 0.333  # Fin tip cord
        self.fin_thickness = .0833
        self.fin_lambda = self.fin_height_short/self.fin_height_long
        self.x = self.fin_length / 8  # Distance from fin leading edge to maximum thickness

        self.K_f = 1.04  # mutual interference factor, used to simulate interference drag, 

        self.a = (self.radius**2 +
             self.nose_cone_length**2)/(2*self.radius)

        # Total wetted surface area of rocket (approximation)
        self.S_B = (
            2 * PI * (
                (self.radius - self.a) *
                asin(self.nose_cone_length / self.a) + self.nose_cone_length
            )
        )

if __name__ == "__main__":
    return
