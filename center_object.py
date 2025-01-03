import errors
import numpy as np
from space_object import SpaceObject


class CenterObject(SpaceObject):
    def __init__(self, diameter: float = 1.0, mass: float = 1.0):
        super().__init__(np.array([0, 0]), mass)
        if diameter < 0:
            raise errors.NegativeDiameterError
        self._diameter = diameter

    @property
    def diameter(self):
        return self._diameter
