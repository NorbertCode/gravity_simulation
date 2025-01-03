class NegativeMassError(ValueError):
    def __init__(self):
        super().__init__("Mass cannot be negative.")


class NegativeDiameterError(ValueError):
    def __init__(self):
        super().__init__("Diameter cannot be negative")
