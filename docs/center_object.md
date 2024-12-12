# CenterObject
The central object of the simulation. Physics don't affect it, only used to apply forces to PointObject instances.


## Properties
### _diameter
Diameter of the object in meters.

### _mass
Mass of the object in kilograms

### _position
Vector position (np.array). Should always be set to the center of the screen.


## Methods
### Constructor
#### __init__(self, diameter: float, mass: float):
Just sets inner variables to given values. [_position](#_position) is not set here, but using [set_position()](#set_position) in [Simulation's constructor](./simulation.md#constructor)

### set_position()
#### set_position(self, position: np.array)
Setter for _position.