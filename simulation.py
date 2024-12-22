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
        dist_vector = self._center_obj.position - point_obj.position
        dist = np.linalg.norm(dist_vector)
        dist_norm = dist_vector / dist

        force = (self._center_obj.mass * point_obj.mass * self.G_CONST) / (dist**2)
        force_vector = force * dist_norm
        accel_vector = force_vector / point_obj.mass

        point_obj.update_position(self.TIME_STEP)
        point_obj.set_velocity(point_obj.velocity + (accel_vector * self.TIME_STEP))
        return copy(point_obj.position)

    def run(self, steps: int) -> list[list[np.array]]:
        # @TODO: this allows for multiple objects to start at the same position
        # @TODO: does blacklist get duplicates?
        positions_at_steps = [[copy(obj.position) for obj in self._point_objs]]
        blacklist = []
        for _ in range(steps):
            positions_at_step = [np.array([np.nan, np.nan])] * len(self._point_objs)
            for index in range(len(self._point_objs)):
                if index not in blacklist:
                    position = self.calculate_next(self._point_objs[index])
                    dist_to_center = np.linalg.norm(self._center_obj.position - position)
                    # @TODO: should this use pixel or space coordinates?
                    if dist_to_center > self._center_obj.diameter / 2:
                        positions_at_step[index] = ((position / self._meters_per_pixel).round())
                    else:
                        blacklist.append(index)

            # @TODO: this has to be reworked to support checking which objects collided
            _, inverse, count = np.unique(positions_at_step, return_inverse=True,
                                          return_counts=True, axis=0)
            duplicate_indexes = np.where(count[inverse] > 1)[0]
            blacklist.extend(duplicate_indexes)

            positions_at_steps.append(positions_at_step)
        return positions_at_steps

    def draw(self, center_object: CenterObject, point_objects: list[PointObject]):
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        pixel_radius = (center_object.diameter / 2) / self._meters_per_pixel
        center_obj_fill_color = (255, 255, 255)
        draw_output.circle(center_object.position / self._meters_per_pixel,
                           pixel_radius, fill=center_obj_fill_color)

        point_obj_fill_color = (0, 255, 0)
        sim_data = self.run(3000)
        for step in sim_data:
            for obj_pos in step:
                if obj_pos is not np.nan:
                    draw_output.point(tuple(obj_pos), point_obj_fill_color)

        output.show()


# 55000 as meters per pixel so the image spans 7000000 pixels in each direction
sim = Simulation((256, 256), 55000)
with open("save.json", "r") as file:
    sim.init_from_json(json.load(file))
sim.draw(sim._center_obj, sim._point_objs)
# sim.save_as_json(sim._center_obj, sim._point_objs)
