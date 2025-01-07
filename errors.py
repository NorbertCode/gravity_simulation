class NegativeMassError(Exception):
    def __init__(self):
        super().__init__("Mass cannot be negative.")


class NegativeDiameterError(Exception):
    def __init__(self):
        super().__init__("Diameter cannot be negative.")
