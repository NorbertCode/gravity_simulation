class CenterObject:
    def __init__(self, diameter, mass):
        self._diameter = diameter
        self._mass = mass

    @property
    def diameter(self):
        return self._diameter

    @property
    def mass(self):
        return self._mass
