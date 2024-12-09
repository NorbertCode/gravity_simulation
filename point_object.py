class PointObject:
    def __init__(self, position, mass, velocity):
        self._position = position
        self._mass = mass
        self._velocity = velocity

    @property
    def position(self):
        return self._position

    @property
    def mass(self):
        return self._mass

    @property
    def velocity(self):
        return self._velocity
