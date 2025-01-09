import numpy as np
from point_object import PointObject
from center_object import CenterObject
from collision import Collision
from copy import copy


class Simulation:
    def __init__(self, meters_per_pixel: float, center_obj: CenterObject,
                 point_objs: list[PointObject]):
        self._meters_per_pixel = meters_per_pixel

        self._center_obj = center_obj
        self._point_objs = point_objs

        self._G_CONST = 6.67430e-11
        self._TIME_STEP = 1.0

    @property
    def center_obj(self):
        return self._center_obj

    @property
    def point_objs(self):
        return self._point_objs

    def calculate_acceleration(self, point_obj: PointObject) -> np.array:
        """Runs the simulation for a single step for a specific PointObject.
        Modifies its position and velocity, and returns a copy of the new position.
        """
        dist_vector = self._center_obj.position - point_obj.position
        dist = np.linalg.norm(dist_vector)
        dist_norm = dist_vector / dist

        force = (self._center_obj.mass * point_obj.mass * self._G_CONST) / (dist**2)
        force_vector = force * dist_norm
        accel_vector = force_vector / point_obj.mass

        return accel_vector

    def calculate_next(self, point_obj: PointObject) -> np.array:
        accel_vector = self.calculate_acceleration(point_obj)

        point_obj.set_velocity(point_obj.velocity + (accel_vector * self._TIME_STEP))
        point_obj.update_position(self._TIME_STEP)

        return copy(point_obj.position)

    def check_for_center_obj_collision(self, position: np.array) -> bool:
        dist_to_center = np.linalg.norm(self._center_obj.position - position)
        return dist_to_center <= self._center_obj.diameter / 2

    @staticmethod
    def check_for_collisions(pixel_positions: list[np.array]) -> list[int]:
        _, inverse, count = np.unique(pixel_positions, return_inverse=True,
                                      return_counts=True, axis=0)
        duplicate_indexes = np.where(count[inverse] > 1)[0]
        return duplicate_indexes

    def run(self, steps: int) -> tuple[list[list[np.array]], list[Collision]]:
        """Run the simulation with all the previously set values
        Args:
            steps: The amount of steps of the simulation to run
        Returns:
            A tuple, where the first element is a list of positions per step
            and the second element is a list of Collisions
            Accessing the position of the third PointObject at the second step
            would look like: run(10)[0][1][2]
        """
        sim_steps = [[copy(obj.position) for obj in self._point_objs]]
        collisions = []
        blacklist = []
        for step in range(steps):
            # Positions are positions in space, which are later returned
            # Pixel positions are only for collision detection
            positions = [np.array([np.nan, np.nan])] * len(self._point_objs)
            pixel_positions = [np.array([np.nan, np.nan])] * len(self._point_objs)
            for index in range(len(self._point_objs)):
                if index not in blacklist:
                    pos = self.calculate_next(self._point_objs[index])
                    if self.check_for_center_obj_collision(pos):
                        collisions.append(Collision(step, [index]))
                        blacklist.append(index)
                    else:
                        positions[index] = pos
                        pixel_positions[index] = (pos / self._meters_per_pixel).round()

            indexes = self.check_for_collisions(pixel_positions)
            if len(indexes) > 0:
                collisions.append(Collision(step, indexes))
            blacklist.extend(indexes)

            sim_steps.append(positions)
        return sim_steps, collisions
