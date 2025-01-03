class NegativeMassError(Exception):
    def __init__(self):
        super().__init__("Mass cannot be negative.")


class NegativeDiameterError(Exception):
    def __init__(self):
        super().__init__("Diameter cannot be negative.")


class IncorrectCenterObjectValuesError(Exception):
    def __init__(self):
        super().__init__("The center object's values are incorrect.")


class IncorrectPointObjectValuesError(Exception):
    def __init__(self):
        super().__init__("The point object's values are incorrect")
