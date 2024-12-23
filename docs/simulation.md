# Simulation
Overall logic and physics simulation. Creates and manages objects, calculates their positions and velocities and outputs the results.


## Properties
### static G_CONST
A physical constant used for gravity calculations.

### static TIME_STEP
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
#### __init__(self, resolution: tuple[int], meters_per_pixel)
Sets inner variables to given values. Loading simulation objects is not handled here, because there are multiple ways of getting them. Look: [init_objects()](#init_objects) and [init_from_json()](#init_from_json).
and calculates the output image's center, which is then passed to [_center_obj](#_center_obj).

### init_objects()
#### init_objects(self, center_obj: CenterObject, point_objs: list[PointObject])
Load simulation objects from arguments.

### init_from_json()
#### init_from_json(self, data)
Load simulation objects from file.

### save_as_json()
#### save_as_json(self, path: str, center_obj: CenterObjectm point_objs: list[PointObject])
Save the end state of the simulation as json.

### calculate_next()
#### calculate_next(self, point_obj: PointObject) -> PointObject
Calculates the next position of the given point_object, based on its and the [_center_obj](#_center_obj)'s properites.

All the calculations visible [here](https://www.desmos.com/calculator/jwtleflsny)

### run()
#### run(self, steps: int) -> tuple[list[list[np.array]], list[tuple[int, list[int]]]]
Returns a list of point objects' position per each step (for example the position of the first object at the last step would be positions_at_steps[-1][0]) and a list of tuples which indicate the step at which a collision has occured an indexes of the collided elements.

It iterates through the steps and for each of them check if any of the objects collided with the center object or each other.

### draw()
#### draw(self, simulation_steps: list[list[np.array]])
Gets the final simulation results and creates their graphical representation.