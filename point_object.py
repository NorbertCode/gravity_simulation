from space_object import SpaceObject
import numpy as np
import errors


class PointObject(SpaceObject):
    def __init__(self, position: np.array = None, mass: float = 1.0,
                 velocity: np.array = None):
        super().__init__(position, mass)
        if velocity is None:
            self._velocity = np.array([0, 0]).astype(float)
        else:
            self._velocity = velocity

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
        pos = json_data["position"]
        mass = json_data["mass"]
        vel = json_data["velocity"]
        if (not PointObject.verify_vector(pos)
            or not isinstance(mass, (int, float))
            or not PointObject.verify_vector(vel)):
            raise errors.InvalidPointObjectDataError

        return cls(np.array(pos), mass, np.array(vel))

    def serialize(self):
        return {
            "velocity": self._velocity.tolist(),
            "mass": self._mass,
            "position": self._position.tolist()
        }

    @staticmethod
    def verify_vector(vector: np.array):
        return all([isinstance(element, (int, float)) for element in vector])
