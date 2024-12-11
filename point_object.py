import numpy as np


class PointObject:
    def __init__(self, position: np.array, mass: float, velocity: np.array):
        self._position = position
        self._mass = mass
        self._velocity = velocity

    @property
    def position(self) -> np.array:
        return self._position

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def velocity(self) -> np.array:
        return self._velocity

    def set_velocity(self, velocity: np.array):
        self._velocity = velocity

    def update_position(self):
        self._position += self._velocity
