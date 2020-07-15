'''
SimpleKalman.py

Kalman filter for a variable and its rate of change.
This acts as a simple linear filter for filtering out
noise during flight. 
'''

from filterpy.kalman import KalmanFilter
import numpy as np
from filterpy.common import Q_discrete_white_noise

class SimpleKalman:
    def __init__(self, starting_value):
        self._filter = KalmanFilter(dim_x=2, dim_z=1)
        self._filter.x = np.array([starting_value, starting_value])
        self._filter.F = np.array([[1.,1.],
                                   [0.,1.]])
        self._filter.H = np.array([[1.,0.]])
        self._filter.P = np.array([[1000.,    0.],
                                   [   0., 1000.] ])
        self._filter.R = np.array([[5.]])
        self._filter.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)
        
        self.inc = 0
        self.last_val = starting_value
        self.first = True

    def update(self, val):
        self.last_val = val
        self._filter.update(val)

    def predict(self):
        self._filter.predict()
        return self._filter.x

    def filter(self, val):
        if self.first:
            self.first = False
            p = [val, 0]
        else:
            p = self.predict()
        self.update(val)
        return p

if __name__ == "__main__":
    data = [1,2,3,4,5,6,7,9,9,10]
    k = SimpleKalman(0.0)
    for i in data:
        print(f"{i} -> {k.filter(i)}")
