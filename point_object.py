from space_object import SpaceObject
import numpy as np


class PointObject(SpaceObject):
    def __init__(self, position: np.array = None, mass: float = 1.0,
                 velocity: np.array = None):
        super().__init__(position, mass)
        if velocity is None:
            self.velocity = np.array([0, 0])
        else:
            self._velocity = velocity

    @property
    def velocity(self) -> np.array:
        return self._velocity

    def set_velocity(self, velocity: np.array):
        self._velocity = velocity

    def update_position(self, time_step):
        self._position += self._velocity * time_step
