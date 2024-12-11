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
        self._center_obj = center_object
        self._point_objs = point_objects

        image_center = [self._resolution[0] / 2, self._resolution[1] / 2]
        self._center_obj.set_position(np.array(image_center) * self._meters_per_pixel)

    def calculate_next(self, point_object: PointObject) -> PointObject:
        next_point = point_object  # So it creates a copy instead of changing the param

        dist_vector = np.array([self._center_obj.position[0] - next_point.position[0],
                           self._center_obj.position[1] - next_point.position[1]])
        dist = sqrt(dist_vector[0]**2 + dist_vector[1]**2)
        dist_norm = dist_vector / dist

        force = (self._center_obj.mass * next_point.mass * self.G_CONST) / (dist**2)
        force_vector = force * dist_norm
        accel_vector = force_vector / next_point.mass

        next_point.set_velocity(next_point.velocity + (accel_vector * self.TIME_STEP))
        next_point.update_position()
        return next_point

    def draw(self, center_object: CenterObject, point_objects: list[PointObject]):
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        pixel_radius = (center_object.diameter / 2) / self._meters_per_pixel
        center_obj_fill_color = (255, 255, 255)
        draw_output.circle(center_object.position / self._meters_per_pixel,
                           pixel_radius, fill=center_obj_fill_color)

        point_obj_fill_color = (0, 255, 0)
        next_point_obj_fill_color = (255, 0, 0)
        for obj in point_objects:
            obj_pos = obj.position / self._meters_per_pixel
            draw_output.point(tuple(obj_pos), point_obj_fill_color)
            next_obj_pos = self.calculate_next(obj).position / self._meters_per_pixel
            draw_output.point(tuple(next_obj_pos), next_point_obj_fill_color)

        output.show()


test_objs = [PointObject(np.array([200., 200.]), 7.348e22, np.array([100, 0]))]
sim = Simulation((128, 128), 10, CenterObject(100, 5.972e24), test_objs)
sim.draw(sim._center_obj, sim._point_objs)
