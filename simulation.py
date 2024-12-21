# ruff: noqa: PTH123
# @TODO: remove this later

import json
import numpy as np
from point_object import PointObject
from center_object import CenterObject
from math import sqrt
from PIL import Image, ImageDraw
from copy import copy


class Simulation:
    G_CONST = 6.67430e-11
    TIME_STEP = 1

    def __init__(self, resolution: tuple[int], meters_per_pixel):
        self._resolution = resolution
        self._meters_per_pixel = meters_per_pixel

    def init_objects(self, center_obj: CenterObject, point_objs: list[PointObject]):
        self._center_obj = center_obj
        self._point_objs = point_objs

        image_center = [self._resolution[0] / 2, self._resolution[1] / 2]
        self._center_obj.set_position(np.array(image_center) * self._meters_per_pixel)

    def init_from_json(self, data):
        center_obj = CenterObject(data["center_object"]["diameter"],
                                  data["center_object"]["mass"])
        point_objs = [
            PointObject(np.array(obj["position"]),
                        obj["mass"],
                        np.array(obj["velocity"]))
            for obj in data["point_objects"]
        ]
        self.init_objects(center_obj, point_objs)

    def save_as_json(self, path: str, center_obj: CenterObject,
                     point_objs: list[PointObject]):
        data = {
            "center_object": {
                "diameter": center_obj.diameter,
                "mass": center_obj.mass
            },
            "point_objects": [
                {
                    "velocity": obj.velocity.tolist(),
                    "mass": obj.mass,
                    "position": obj.position.tolist()
                }
                for obj in point_objs
            ]
        }
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def calculate_next(self, point_obj: PointObject) -> PointObject:
        dist_vector = np.array([self._center_obj.position[0] - point_obj.position[0],
                                self._center_obj.position[1] - point_obj.position[1]])
        dist = sqrt(dist_vector[0]**2 + dist_vector[1]**2)
        dist_norm = dist_vector / dist

        force = (self._center_obj.mass * point_obj.mass * self.G_CONST) / (dist**2)
        force_vector = force * dist_norm
        accel_vector = force_vector / point_obj.mass

        point_obj.update_position(self.TIME_STEP)
        point_obj.set_velocity(point_obj.velocity + (accel_vector * self.TIME_STEP))
        return copy(point_obj.position)

    def run_simulation_for_obj(self, steps: int,
                               point_object: PointObject) -> list[PointObject]:
        point_obj_steps_list = [point_object.position]
        for _ in range(steps):
            point_obj_steps_list.append(self.calculate_next(point_object))
        return point_obj_steps_list

    def draw(self, center_object: CenterObject, point_objects: list[PointObject]):
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        pixel_radius = (center_object.diameter / 2) / self._meters_per_pixel
        center_obj_fill_color = (255, 255, 255)
        draw_output.circle(center_object.position / self._meters_per_pixel,
                           pixel_radius, fill=center_obj_fill_color)

        point_obj_fill_color = (0, 255, 0)
        for obj in point_objects:
            obj_simulation = self.run_simulation_for_obj(3000, obj)
            for position_at_step in obj_simulation:
                position = position_at_step / self._meters_per_pixel
                draw_output.point(tuple(position), point_obj_fill_color)

        output.show()


# 55000 as meters per pixel so the image spans 7000000 pixels in each direction
sim = Simulation((256, 256), 55000)
with open("save.json", "r") as file:
    sim.init_from_json(json.load(file))
sim.draw(sim._center_obj, sim._point_objs)
# sim.save_as_json(sim._center_obj, sim._point_objs)
