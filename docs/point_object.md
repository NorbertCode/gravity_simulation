# PointObject
A movable object in space. Represented by a single point in the simulation.


## Properties
### _position
Vector position (np.array) in meters, starting from top left (0, 0).

### _mass
Object mass in kilograms.

### _velocity
Vector velocity (np.array) in m/s


## Methods
### Constructor
#### __init__(self, position: np.array, mass: float, velocity: np.array)
Sets inner variables to given values

### set_velocity()
#### set_velocity(self, velocity: np.array)
Setter for [_velocity](#_velocity)

### update_position()
#### update_position(self)
Moves the object by applying the current velocity.