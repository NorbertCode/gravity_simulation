class NegativeMassError(Exception):
    def __init__(self):
        super().__init__("Mass cannot be negative.")


class NegativeDiameterError(Exception):
    def __init__(self):
        super().__init__("Diameter must be greater than 0.")


class NegativePointObjectAmountError(Exception):
    def __init__(self):
        super().__init__("Amount of point objects cannot be negative.")


class InvalidCenterObjectDataError(Exception):
    def __init__(self):
        super().__init__("Invalid center object data.")


class InvalidPointObjectDataError(Exception):
    def __init__(self):
        super().__init__("Invalid point object data.")


class UnableToOpenConfigError(Exception):
    def __init__(self):
        super().__init__("Unable to open config file.")


class InvalidStepsError(Exception):
    def __init__(self):
        super().__init__("Invalid amount of steps (k).")


class InvalidResolutionError(Exception):
    def __init__(self):
        super().__init__("Invalid resolution.")


class InvalidMetersPerPixelError(Exception):
    def __init__(self):
        super().__init__("Invalid meters per pixel value.")


class InvalidCloseCallDistanceError(Exception):
    def __init__(self):
        super().__init__("Invalid close call distance value.")
