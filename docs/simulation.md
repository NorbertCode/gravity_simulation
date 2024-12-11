# Simulation
Overall logic and physics simulation. Creates and manages objects, calculates their positions and velocities and outputs the results.


## Properties
### static G_CONST
A physical constant used for gravity calculations.

### TIME_STEP
Time step between each time [calculate_next()](#calculate_next) is called. A smaller value will lead to more detail, but higher number of steps needed

### _resolution
A tuple(int, int) which holds the output image's resolution.

### _meters_per_pixel
A numeric value which is used later to determine the distance to pixel conversion.

### _center_obj
An instance of [CenterObject](./center_object.md). The central point of the simulation.

### _point_objs
List of all instances of [PointObject](./point_object.md) used in the simulation.


## Methods
### Constructor
#### __init__(self, resolution: tuple[int], meters_per_pixel, center_object: CenterObject, point_objects: list[PointObject])
Sets inner variables to given values and calculates the output image's center, which is then passed to [_center_obj](#_center_obj).

### calculate_next()
#### calculate_next(self, point_object: PointObject) -> PointObject
Calculates the next position of the given point_object, based on its and the [_center_obj](#_center_obj)'s properites.

Uses a parameter passed by the function instead of the class' property to allow for running the calculation without modifying the actual instance.

### draw()
#### draw(self, center_object: CenterObject, point_objects: list[PointObject])
Gets the final simulation results and creates their graphical representation.