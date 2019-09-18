# Flight simulation
# Harrison Hall

from sympy import *
from sympy.physics.vector import dynamicsymbols


t = Symbol('t')
h = Symbol('h')
#V = dynamicsymbols('V')
F = Symbol('F')
D = Symbol('D')
T = Symbol('T')
p = Symbol('p')
g = Symbol('g')
#m = dynamicsymbols('m')
h, m = symbols('h m', cls=Function)
C_D = Symbol('C_D')
A = Symbol('A')
u_e = Symbol('u_e')
# h = Integral(V, t)
V = h(t).diff(t)

g = 9.81 # [m/s^2], gravity


class Rocket:
    def __init__(self):
        pass

    def apogee(self):
        return

    def acceleration(self):
        return (-g - (1/2)*(p*V*Abs(V))  + (V/Abs(V)*((-m(t).diff(t)*u_e)/m)))


if __name__ == "__main__":
    rocket = Rocket()
    print(rocket.acceleration())
    print(solve(rocket.acceleration(),h))
