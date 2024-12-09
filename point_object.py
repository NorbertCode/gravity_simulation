class PointObject:
    def __init__(self, position, mass, velocity):
        self._position = position
        self._mass = mass
        self._velocity = velocity

    @property
    def position(self):
        return self._position
