import numpy as np


class SpaceObject:
    def __init__(self, position: np.array, mass: float):
        self._position = position
        self._mass = mass

    @property
    def position(self) -> np.array:
        return self._position

    @property
    def mass(self) -> float:
        return self._mass
