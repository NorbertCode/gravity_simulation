import errors
import numpy as np
from space_object import SpaceObject


class CenterObject(SpaceObject):
    def __init__(self, diameter: float = 1.0, mass: float = 1.0):
        """
        Diameter is a float which indicates the object's diameter in meters,
        mass is also a float, which means the mass in meters.
        """
        super().__init__(np.array([0, 0]), mass)
        if diameter <= 0:
            raise errors.NegativeDiameterError
        self._diameter = diameter

    @property
    def diameter(self) -> float:
        return self._diameter

    @classmethod
    def from_json(cls, json_data: dict):
        """Create an object from the given json data."""
        diameter = json_data["diameter"]
        mass = json_data["mass"]
        if not isinstance(diameter, (int, float)) or not isinstance(mass, (int, float)):
            raise errors.InvalidCenterObjectDataError
        return cls(diameter, mass)

    def serialize(self):
        """Convert this object's data to json."""
        return {
            "diameter": self._diameter,
            "mass": self._mass
        }
