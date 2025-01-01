from space_object import SpaceObject
import numpy as np


class CenterObject(SpaceObject):
    def __init__(self, diameter: float, mass: float):
        super().__init__(np.array([0, 0]), mass)
        self._diameter = diameter

    @property
    def diameter(self):
        return self._diameter
