import errors
import numpy as np


class SpaceObject:
    def __init__(self, position: np.array = None, mass: float = 1.0):
        if position is None:
            self._position = np.array([0, 0])
        else:
            self._position = position

        if mass < 0:
            raise errors.NegativeMassError
        self._mass = mass

    @property
    def position(self) -> np.array:
        return self._position

    @property
    def mass(self) -> float:
        return self._mass

    # Virtual methods
    @classmethod
    def from_json(cls, json_data: dict):
        raise NotImplementedError()

    def serialize(self) -> dict:
        raise NotImplementedError()
