import json
import numpy as np
from point_object import PointObject
from center_object import CenterObject
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

    def run(self, steps: int) -> tuple[list[list[np.array]],
                                       list[tuple[int, list[int]]]]:
        sim_steps = [[(obj.position / self._meters_per_pixel).round()
                       for obj in self._point_objs]]
        collisions = []
        blacklist = []
        for step in range(steps):
            positions = [np.array([np.nan, np.nan])] * len(self._point_objs)
            for index in range(len(self._point_objs)):
                if index not in blacklist:
                    pos = self.calculate_next(self._point_objs[index])
                    dist_to_center = np.linalg.norm(self._center_obj.position - pos)
                    if dist_to_center > self._center_obj.diameter / 2:
                        positions[index] = (pos / self._meters_per_pixel).round()
                    else:
                        collisions.append((step, [index]))
                        blacklist.append(index)

            _, inverse, count = np.unique(positions, return_inverse=True,
                                          return_counts=True, axis=0)
            duplicate_indexes = np.where(count[inverse] > 1)[0]
            if len(duplicate_indexes) > 0:
                collisions.append((step, duplicate_indexes))
            blacklist.extend(duplicate_indexes)

            sim_steps.append(positions)
        return sim_steps, collisions

    def draw(self, simulation_steps: list[list[np.array]], file_name: str = None):
        output = Image.new("RGB", self._resolution)
        draw_output = ImageDraw.Draw(output)

        # @TODO: move this somewhere else
        center_obj_fill_color = (255, 255, 255)
        point_obj_fill_color = (0, 255, 0)
        point_obj_end_color = (255, 0, 0)

        pixel_radius = round((self._center_obj.diameter / 2) / self._meters_per_pixel)
        pixel_pos = (self._center_obj.position / self._meters_per_pixel).round()
        draw_output.circle(pixel_pos, pixel_radius, fill=center_obj_fill_color)

        for step in simulation_steps:
            for obj_pos in step:
                if obj_pos is not np.nan:
                    draw_output.point(tuple(obj_pos), point_obj_fill_color)

        for obj in self._point_objs:
            pos = (obj.position / self._meters_per_pixel).round()
            draw_output.point(tuple(pos), point_obj_end_color)

        if file_name is not None:
            output.save(f"{file_name}.png")
        output.show()

    @staticmethod
    def generate_collision_report(collision_data, file_name: str = None) -> str:
        output = ""
        for collision in collision_data:
            if len(collision[1]) > 1:
                objects = ""
                for obj in collision[1]:
                    objects += f"n={obj}, "
                output += f"Objects {objects[:-2]} collided at k={collision[0]}\n"
            else:
                output += f"Object n={collision[1][0]} collided at k={collision[0]}\n"

        if file_name is not None:
            with open(f"{file_name}.txt", "w") as file:
                file.write(output)

        return output
