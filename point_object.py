from space_object import SpaceObject
import numpy as np


class PointObject(SpaceObject):
    def __init__(self, position: np.array, mass: float, velocity: np.array):
        super().__init__(position, mass)
        self._velocity = velocity

    @property
    def velocity(self) -> np.array:
        return self._velocity

    def set_velocity(self, velocity: np.array):
        self._velocity = velocity

    def update_position(self, time_step):
        self._position += self._velocity * time_step
