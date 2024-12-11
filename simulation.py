import numpy as np
from point_object import PointObject
from center_object import CenterObject
from math import sqrt
from PIL import Image, ImageDraw


class Simulation:
    G_CONST = 6.67430e-11
    TIME_STEP = 1e-7

    def __init__(self, resolution: tuple[int], meters_per_pixel,
                 center_object: CenterObject, point_objects: list[PointObject]):
        self._resolution = resolution
        self._meters_per_pixel = meters_per_pixel
        self._center_object = center_object
        self._point_objects = point_objects

        image_center = [self._resolution[0] / 2, self._resolution[1] / 2]
        self._center_object.set_position(np.array(image_center) * self._meters_per_pixel)

    def calculate_next(self, point_object: PointObject) -> PointObject:
        new_point_object = point_object
        distance_vector = np.array([self._center_object.position[0] - new_point_object.position[0],
                           self._center_object.position[1] - new_point_object.position[1]])
        distance = sqrt(distance_vector[0]**2 + distance_vector[1]**2)
        distance_norm = distance_vector / distance
        force_vector = (self._center_object.mass * new_point_object.mass * self.G_CONST) / (distance**2) * distance_norm
        acceleration_vector = force_vector / new_point_object.mass
        new_point_object.set_velocity(new_point_object.velocity + (acceleration_vector * self.TIME_STEP))
        new_point_object.update_position()
        return new_point_object

    def draw(self, center_object: CenterObject, point_objects: list[PointObject]):
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        pixel_radius = (center_object.diameter / 2) / self._meters_per_pixel
        center_obj_fill_color = (255, 255, 255)
        draw_output.circle(center_object.position / self._meters_per_pixel, pixel_radius, fill=center_obj_fill_color)

        point_obj_fill_color = (0, 255, 0)
        next_point_obj_fill_color = (255, 0, 0)
        for obj in point_objects:
            obj_position = obj.position / self._meters_per_pixel
            draw_output.point(tuple(obj_position), point_obj_fill_color)
            next_obj_position = self.calculate_next(obj).position / self._meters_per_pixel
            draw_output.point(tuple(next_obj_position), next_point_obj_fill_color)

        output.show()


test_objs = [PointObject(np.array([200., 200.]), 7.348e22, np.array([0, 0]))]
sim = Simulation((128, 128), 10, CenterObject(100, 5.972e24), test_objs)
sim.draw(sim._center_object, sim._point_objects)
