from space_object import SpaceObject
import numpy as np
import errors


class PointObject(SpaceObject):
    def __init__(self, position: np.array = None, mass: float = 1.0,
                 velocity: np.array = None):
        """
        Position is a vector, which signifies where an object is in space (meters),
        mass is a float, which represents an object's mass in kilograms,
        velocity is a speed vector (m/s).
        """
        super().__init__(position, mass)
        if velocity is None:
            self._velocity = np.array([0, 0]).astype(float)
        else:
            self._velocity = velocity

        # Position and velocity must be two-dimensional
        if len(self._position) != 2 or len(self._velocity) != 2:
            raise errors.InvalidPointObjectDataError

    @property
    def velocity(self) -> np.array:
        return self._velocity

    def set_velocity(self, velocity: np.array):
        self._velocity = velocity

    def update_position(self, time_step: float):
        self._position += self._velocity * time_step

    @classmethod
    def from_json(cls, json_data):
        """Create an object from the given json data."""
        pos = json_data["position"]
        mass = json_data["mass"]
        vel = json_data["velocity"]
        if (not PointObject.verify_vector(pos)
            or not isinstance(mass, (int, float))
            or not PointObject.verify_vector(vel)):
            raise errors.InvalidPointObjectDataError

        return cls(np.array(pos), mass, np.array(vel))

    def serialize(self):
        """Convert this object's data to json."""
        return {
            "velocity": self._velocity.tolist(),
            "mass": self._mass,
            "position": self._position.tolist()
        }

    @staticmethod
    def _verify_vector(vector: np.array):
        """Returns true if all elements of the given vector are numeric."""
        return all([isinstance(element, (int, float)) for element in vector])
