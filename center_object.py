import numpy as np


class CenterObject:
    def __init__(self, diameter: float, mass: float):
        self._diameter = diameter
        self._mass = mass

        self._position = np.array([0, 0])

    @property
    def diameter(self):
        return self._diameter

    @property
    def mass(self):
        return self._mass

    @property
    def position(self):
        return self._position
