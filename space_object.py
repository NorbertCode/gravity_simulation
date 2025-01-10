import errors
import numpy as np


class SpaceObject:
    def __init__(self, position: np.array = None, mass: float = 1.0):
        """
        Position is a vector, which signifies where the object is in space (meters),
        mass is in kilograms.
        """
        if position is None:
            self._position = np.array([0, 0]).astype(float)
        else:
            self._position = position

        # Mass of any space object cannot be negative
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
        """Create an object from the given json data."""
        raise NotImplementedError()

    def serialize(self) -> dict:
        """Convert this object's data to json."""
        raise NotImplementedError()
